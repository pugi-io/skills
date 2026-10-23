#!/usr/bin/env bash
# Release check for this repository. Run from anywhere: bash scripts/check.sh
#  1. skills: Agent Skills front matter, validated with the reference validator
#     (skills-ref, through uvx) when available, plus this repo's own rules;
#  2. manifests: JSON parses and the required fields of each format are set;
#  3. secrets: no file has a key-shaped string (reported by rule, file and
#     line only, never the matched text); scripts are scanned too;
#  4. gitleaks, when installed, on the tree and the git history (redacted).
# Any check that cannot run fails the release. Exit 0 only when all pass.
# Requires bash, git, python3.

set -u
cd "$(dirname "$0")/.." || exit 1

python3 -I - <<'PY'
import json, os, re, subprocess, sys, shutil

fail = False
def bad(msg):
    global fail
    fail = True
    print("FAIL", msg)

def ok(msg):
    print("ok  ", msg)

# ---- 1. skills ---------------------------------------------------------
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
ALLOWED = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}

def front_matter(path):
    text = open(path, encoding="utf-8").read()
    if not text.startswith("---\n"):
        raise ValueError("no front matter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("front matter not closed")
    fields, current = {}, None
    for raw in text[4:end].split("\n"):
        if not raw.strip():
            continue
        if raw.startswith("  "):
            if current != "metadata":
                raise ValueError(f"unexpected indented line: {raw.strip()}")
            k, sep, v = raw.strip().partition(":")
            if not sep:
                raise ValueError(f"bad metadata line: {raw.strip()}")
            fields["metadata"][k.strip()] = v.strip().strip('"')
            continue
        k, sep, v = raw.partition(":")
        if not sep:
            raise ValueError(f"not a key: value line: {raw}")
        k, v = k.strip(), v.strip()
        if k in fields:
            raise ValueError(f"duplicate key {k}")
        if k == "metadata":
            if v:
                raise ValueError("metadata must be a mapping")
            fields[k] = {}
        else:
            if v.startswith(("'", '"', "[", "{", "|", ">")) or ": " in v or " #" in v:
                raise ValueError(f"{k}: use a plain one-line value without ': ' or ' #'")
            fields[k] = v
        current = k
    return fields, text[end + 5:]

skills = sorted(d for d in os.listdir("skills") if os.path.isdir(os.path.join("skills", d)))
for d in skills:
    p = f"skills/{d}/SKILL.md"
    try:
        fm, body = front_matter(p)
    except Exception as e:
        bad(f"{p}: {e}"); continue
    extra = set(fm) - ALLOWED
    if extra: bad(f"{p}: unknown fields {sorted(extra)}")
    name, desc = fm.get("name", ""), fm.get("description", "")
    if name != d: bad(f"{p}: name '{name}' must match folder '{d}'")
    if not NAME_RE.match(name) or len(name) > 64: bad(f"{p}: invalid name")
    if not desc or len(desc) > 1024: bad(f"{p}: description must be 1-1024 chars ({len(desc)})")
    if len(fm.get("compatibility", "")) > 500: bad(f"{p}: compatibility over 500 chars")
    if body.count("\n") > 500: bad(f"{p}: over 500 lines")
    if not os.path.exists(f"skills/{d}/LICENSE.txt"): bad(f"skills/{d}: LICENSE.txt missing")
    oy = f"skills/{d}/agents/openai.yaml"
    if os.path.exists(oy):
        y = open(oy).read()
        if "interface:" not in y or "display_name:" not in y: bad(f"{oy}: needs interface.display_name")
    ok(f"{p} ({len(desc)}-char description)")

uvx = shutil.which("uvx")
if uvx:
    for d in skills:
        r = subprocess.run([uvx, "--quiet", "--from", "git+https://github.com/agentskills/agentskills@69ef37e9424c0a7ea9dd2293b559e43ec8176379#subdirectory=skills-ref",
                            "skills-ref", "validate", f"skills/{d}"], capture_output=True, text=True, timeout=300)
        if r.returncode != 0: bad(f"skills-ref skills/{d}: {(r.stdout + r.stderr).strip()[-300:]}")
    if not fail: ok(f"skills-ref validate: {len(skills)} skills")
else:
    bad("uvx not installed: the reference validator (skills-ref) could not run")

# ---- 2. manifests ------------------------------------------------------
def load(p):
    try:
        return json.load(open(p))
    except Exception as e:
        bad(f"{p}: invalid JSON ({e})"); return None

KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
m = load(".claude-plugin/plugin.json")
if m is not None:
    if not KEBAB.match(m.get("name", "")): bad(".claude-plugin/plugin.json: name must be kebab-case")
    for k in ("version", "description", "author", "license"):
        if k not in m: bad(f".claude-plugin/plugin.json: {k} missing")
    if "icon" in m and not os.path.exists(m["icon"]): bad(".claude-plugin/plugin.json: icon file missing")
    ok(".claude-plugin/plugin.json")
mk = load(".claude-plugin/marketplace.json")
if mk is not None:
    if not mk.get("name") or not mk.get("owner", {}).get("name") or not mk.get("plugins"): bad(".claude-plugin/marketplace.json: name, owner.name and plugins required")
    for e in mk.get("plugins", []):
        if not e.get("name") or not str(e.get("source", "")).startswith("./"): bad(".claude-plugin/marketplace.json: each plugin needs name and a ./ source")
        if m and e.get("name") != m.get("name"): bad(".claude-plugin/marketplace.json: entry name differs from plugin.json name")
    ok(".claude-plugin/marketplace.json")
c = load(".codex-plugin/plugin.json")
if c is not None:
    if not KEBAB.match(c.get("name", "")) or not c.get("version") or not c.get("description"): bad(".codex-plugin/plugin.json: name, version, description required")
    if c.get("skills") and not os.path.isdir(c["skills"]): bad(".codex-plugin/plugin.json: skills path missing")
    ok(".codex-plugin/plugin.json")
a = load(".agents/plugins/marketplace.json")
if a is not None:
    for e in a.get("plugins", []):
        pol = e.get("policy", {})
        if pol.get("installation") not in ("AVAILABLE", "INSTALLED_BY_DEFAULT", "NOT_AVAILABLE") or not pol.get("authentication") or not e.get("category"):
            bad(".agents/plugins/marketplace.json: policy.installation, policy.authentication and category required")
        if not str(e.get("source", {}).get("path", "")).startswith("./"): bad(".agents/plugins/marketplace.json: source.path must start with ./")
    ok(".agents/plugins/marketplace.json")
cu = load(".cursor-plugin/plugin.json")
if cu is not None:
    # The README promises name, description, version and author.
    if not KEBAB.match(cu.get("name", "")): bad(".cursor-plugin/plugin.json: name must be kebab-case")
    for k in ("description", "version"):
        if not cu.get(k): bad(f".cursor-plugin/plugin.json: {k} missing")
    if not cu.get("author", {}).get("name"): bad(".cursor-plugin/plugin.json: author.name missing")
    unknown = set(cu) - {"name", "description", "version", "author", "homepage", "repository", "license", "keywords", "logo"}
    if unknown: bad(f".cursor-plugin/plugin.json: fields not in the template {sorted(unknown)}")
    if cu.get("logo") and not os.path.exists(cu["logo"]): bad(".cursor-plugin/plugin.json: logo file missing")
    if os.path.exists(".cursor-plugin/marketplace.json"): bad(".cursor-plugin/marketplace.json must not exist in a single-plugin repo")
    ok(".cursor-plugin/plugin.json")
rp = load("plugin.json")
if rp is not None:
    if not KEBAB.match(rp.get("name", "")) or not rp.get("version") or not rp.get("description"): bad("plugin.json: name, version, description required")
    oi = rp.get("extensions", {}).get("com.openai", {}).get("interface", {})
    if not oi.get("displayName"): bad("plugin.json: extensions.com.openai.interface.displayName missing")
    if oi.get("logo") and not os.path.exists(oi["logo"]): bad("plugin.json: interface logo file missing")
    if c and (c.get("name"), c.get("version")) != (rp.get("name"), rp.get("version")): bad("plugin.json and .codex-plugin/plugin.json disagree on name or version")
    ok("plugin.json (Agent Plugins, extensions.com.openai)")

# ---- 3. secrets --------------------------------------------------------
RULES = [
    ("stripe-secret", r"(?:sk|rk)_live_[0-9A-Za-z]{20,}"),
    ("anthropic-key", r"sk-ant-[A-Za-z0-9_-]{32,}"),
    ("openai-key", r"sk-(?:proj-)?[A-Za-z0-9]{32,}"),
    ("aws-key-id", r"(?:AKIA|ASIA)[0-9A-Z]{16}"),
    ("github-token", r"(?:ghp|gho|ghs|ghu|ghr)_[A-Za-z0-9]{36}|github_pat_[A-Za-z0-9_]{60,}"),
    ("slack-token", r"xox[abposr]-[A-Za-z0-9-]{10,}"),
    ("google-api-key", r"AIza[0-9A-Za-z_-]{35}"),
    ("private-key", r"-----BEGIN (?:[A-Z]+ )?PRIVATE KEY-----"),
    ("jwt", r"eyJ[A-Za-z0-9_-]{20,}\.eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}"),
]
files = subprocess.run(["git", "ls-files", "-co", "--exclude-standard", "-z"], capture_output=True, text=True).stdout.split("\0")
hits = 0
for f in filter(None, files):
    try:
        raw = open(f, "rb").read()
    except OSError:
        continue
    if b"\0" in raw[:4096]:
        continue
    text = raw.decode("utf-8", "replace")
    for rule, rx in RULES:
        for mt in re.finditer(rx, text):
            hits += 1
            print(f"FAIL secret-shaped string: {f}:{text.count(chr(10), 0, mt.start()) + 1} ({rule})")
if hits: fail = True
else: ok(f"no key-shaped strings in {len([f for f in files if f])} files")

sys.exit(1 if fail else 0)
PY
py=$?

gl=0
if command -v gitleaks >/dev/null 2>&1; then
  if gitleaks dir . --no-banner --redact --exit-code 1 >/dev/null 2>&1; then echo "ok   gitleaks dir"; else echo "FAIL gitleaks dir (run: gitleaks dir . --redact -v)"; gl=1; fi
  if git rev-parse --verify HEAD >/dev/null 2>&1; then
    if gitleaks git . --no-banner --redact --exit-code 1 >/dev/null 2>&1; then echo "ok   gitleaks git history"; else echo "FAIL gitleaks git (run: gitleaks git . --redact -v)"; gl=1; fi
  fi
else
  echo "FAIL gitleaks not installed"; gl=1
fi

if [ "$py" -eq 0 ] && [ "$gl" -eq 0 ]; then echo "All checks passed."; exit 0; fi
echo "Checks failed."; exit 1
