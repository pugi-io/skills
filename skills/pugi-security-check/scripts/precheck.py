#!/usr/bin/env python3
"""Pre-launch check for a public URL or a local folder. Read-only.

  python3 precheck.py https://your-app.example     passive check of a live site
  python3 precheck.py ./path/to/project            secrets in a folder and its git history

URL mode reads only what a browser is given: the page, up to ten of the
site's own scripts, and the source maps those scripts declare. It sends no
form data and guesses no paths. It follows redirects only within the same
site (the host or its www. twin) and never from https to http. Each host is
resolved once, every address must be public (no private, loopback,
link-local, NAT64 or 6to4 addresses), and the connection goes to that
checked address. Reads stop at 2 MB and 30 seconds each. Output shows
addresses as scheme://host/path only.

Folder mode reads files on disk and runs git locally. Nothing is uploaded.

Found keys are reported by type, file and line only, never by value.

Exit codes:
  0  no findings, and every planned read succeeded
  1  findings (the summary also says if some reads failed)
  2  usage error, or the target could not be reached at all
  3  no findings, but some reads failed: the result is incomplete, not clean

Requires Python 3.8+ and, for history, git. Standard library only.
"""

import base64
import html.parser
import http.client
import ipaddress
import json
import os
import re
import socket
import ssl
import subprocess
import sys
import time
import urllib.parse

MAX_BYTES = 2 * 1024 * 1024   # per response and per file
MAX_SCRIPTS = 10
MAX_REDIRECTS = 5
TIMEOUT = 15
HISTORY_COMMITS = 200
HISTORY_BYTES = 64 * 1024 * 1024
SKIP_DIRS = {"node_modules", ".git", "dist", "build", ".next", ".output", ".vercel", "coverage"}

# Formats of keys that must never reach a browser or a repository.
KEY_PATTERNS = [
    ("Stripe secret key", r"(?:sk|rk)_live_[0-9A-Za-z]{20,}"),
    ("OpenAI key", r"sk-(?:proj-)?[A-Za-z0-9_-]{32,}"),
    ("Anthropic key", r"sk-ant-[A-Za-z0-9_-]{32,}"),
    ("AWS access key id", r"(?:AKIA|ASIA)[0-9A-Z]{16}"),
    ("GitHub token", r"(?:ghp|gho|ghs|ghu|ghr)_[A-Za-z0-9]{36}|github_pat_[A-Za-z0-9_]{60,}"),
    ("Slack token", r"xox[abposr]-[A-Za-z0-9-]{10,}"),
    ("Google API key", r"AIza[0-9A-Za-z_-]{35}"),
    ("Private key", r"-----BEGIN (?:[A-Z]+ )?PRIVATE KEY-----"),
]
KEY_RES = [(label, re.compile(rx)) for label, rx in KEY_PATTERNS]
JWT_RE = re.compile(r"eyJ[A-Za-z0-9_-]{10,}\.(eyJ[A-Za-z0-9_-]{10,})\.[A-Za-z0-9_-]{10,}")
SOURCEMAP_RE = re.compile(r"[#@]\s*sourceMappingURL=([^\s'\"]+)\s*$", re.M)

findings = []      # (severity, message)
incomplete = []    # reads that failed


def flag(severity, message):
    findings.append((severity, message))
    print(f"  [{severity}] {message}")


def note(message):
    print(f"  {message}")


def missed(message):
    incomplete.append(message)
    print(f"  [not checked] {message}")


def key_hits(text):
    """Yield (label, line_number) for every key-shaped match. Never the value."""
    for label, rx in KEY_RES:
        for m in rx.finditer(text):
            yield label, text.count("\n", 0, m.start()) + 1
    for m in JWT_RE.finditer(text):
        payload = m.group(1) + "=" * (-len(m.group(1)) % 4)
        try:
            claims = json.loads(base64.urlsafe_b64decode(payload))
        except Exception:
            continue
        if isinstance(claims, dict) and claims.get("role") == "service_role":
            yield "Supabase service_role key", text.count("\n", 0, m.start()) + 1


# ---------------------------------------------------------------- URL mode

BLOCKED_NETS = [ipaddress.ip_network(n) for n in ("64:ff9b::/96", "64:ff9b:1::/48", "2002::/16", "100.64.0.0/10")]
FETCH_DEADLINE = 30  # seconds of wall time per request, including the body


def resolve_public(host):
    """Resolve host once. Return one public IP to connect to, or raise
    ValueError if any address is not public (private, loopback, link-local,
    NAT64, 6to4 and so on)."""
    try:
        infos = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror:
        raise ValueError(f"{host} does not resolve")
    ips = []
    for info in infos:
        ip = ipaddress.ip_address(info[4][0].split("%")[0])
        if getattr(ip, "ipv4_mapped", None):
            ip = ip.ipv4_mapped
        if not ip.is_global or any(ip in net for net in BLOCKED_NETS):
            raise ValueError(f"{host} resolves to a non-public address; not read")
        ips.append(ip)
    if not ips:
        raise ValueError(f"{host} does not resolve")
    return str(ips[0])


def same_site(a, b):
    strip = lambda h: h[4:] if h.startswith("www.") else h
    return strip(a.lower()) == strip(b.lower())


def shown(url):
    """scheme://host/path only: never userinfo, query or fragment."""
    u = urllib.parse.urlsplit(url)
    return f"{u.scheme}://{u.hostname or ''}{u.path or '/'}"


def tls_context():
    """Verified TLS. Some Python builds ship without CA certificates; then
    use certifi if present, or the system bundle. Verification is never off."""
    ctx = ssl.create_default_context()
    if ctx.cert_store_stats().get("x509_ca", 0) == 0:
        try:
            import certifi
            ctx.load_verify_locations(certifi.where())
        except Exception:
            for bundle in ("/etc/ssl/cert.pem", "/etc/ssl/certs/ca-certificates.crt", "/etc/pki/tls/certs/ca-bundle.crt"):
                if os.path.exists(bundle):
                    ctx.load_verify_locations(bundle)
                    break
    return ctx


TLS = tls_context()


class PinnedHTTPConnection(http.client.HTTPConnection):
    """Connects to the IP checked in resolve_public, not to a fresh lookup."""
    def __init__(self, host, ip, port, timeout):
        super().__init__(host, port, timeout=timeout)
        self._ip = ip

    def connect(self):
        self.sock = socket.create_connection((self._ip, self.port), self.timeout)


class PinnedHTTPSConnection(http.client.HTTPSConnection):
    def __init__(self, host, ip, port, timeout):
        super().__init__(host, port, timeout=timeout, context=TLS)
        self._ip = ip

    def connect(self):
        raw = socket.create_connection((self._ip, self.port), self.timeout)
        self.sock = TLS.wrap_socket(raw, server_hostname=self.host)  # SNI and certificate check use the host name


def get_once(url):
    """One GET without following redirects. Returns (status, headers, body)."""
    u = urllib.parse.urlsplit(url)
    if u.scheme not in ("http", "https") or not u.hostname:
        raise ValueError(f"not an http(s) address: {shown(url)}")
    ip = resolve_public(u.hostname)
    port = u.port or (443 if u.scheme == "https" else 80)
    cls = PinnedHTTPSConnection if u.scheme == "https" else PinnedHTTPConnection
    conn = cls(u.hostname, ip, port, TIMEOUT)
    path = (u.path or "/") + (f"?{u.query}" if u.query else "")
    started = time.monotonic()
    try:
        conn.request("GET", path, headers={"Host": u.netloc.rsplit("@", 1)[-1], "User-Agent": "pugi-precheck/0.3 (+https://pugi.io/security/audit)", "Accept-Encoding": "identity"})
        resp = conn.getresponse()
        chunks, size = [], 0
        while True:
            if time.monotonic() - started > FETCH_DEADLINE:
                raise ValueError(f"{shown(url)} took longer than {FETCH_DEADLINE} s; stopped")
            chunk = resp.read(65536)
            if not chunk:
                break
            chunks.append(chunk)
            size += len(chunk)
            if size > MAX_BYTES:
                missed(f"{shown(url)} is larger than {MAX_BYTES // (1024 * 1024)} MB; only the first part was read")
                break
        body = b"".join(chunks)[:MAX_BYTES]
        return resp.status, resp.headers, body.decode("utf-8", "replace")
    except ValueError:
        raise
    except Exception as e:
        raise ValueError(f"could not read {shown(url)}: {getattr(e, 'reason', None) or e.__class__.__name__}")
    finally:
        conn.close()


def fetch(url, site_host, follow=True):
    """GET url. With follow, follow redirects only within the site and never
    from https to http. Returns (final_url, status, headers, body)."""
    for _ in range(MAX_REDIRECTS + 1):
        u = urllib.parse.urlsplit(url)
        if u.username or u.password:
            url = urllib.parse.urlunsplit((u.scheme, u.hostname + (f":{u.port}" if u.port else ""), u.path, u.query, ""))
            u = urllib.parse.urlsplit(url)
        if not same_site(u.hostname or "", site_host):
            raise ValueError(f"leads to another host ({u.hostname}); not followed")
        status, headers, body = get_once(url)
        loc = headers.get("Location")
        if follow and status in (301, 302, 303, 307, 308) and loc:
            nxt = urllib.parse.urljoin(url, loc)
            if u.scheme == "https" and urllib.parse.urlsplit(nxt).scheme == "http":
                raise ValueError(f"{shown(url)} redirects from https to http; not followed")
            url = nxt
            continue
        return url, status, headers, body
    raise ValueError(f"more than {MAX_REDIRECTS} redirects from {shown(url)}")


class ScriptParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.srcs = []

    def handle_starttag(self, tag, attrs):
        if tag == "script":
            src = dict(attrs).get("src")
            if src:
                self.srcs.append(src)


def scan_text(text, where):
    for label, line in key_hits(text):
        if label == "Supabase service_role key":
            flag("critical", f"Supabase service_role key in {where} (line {line}); it bypasses Row Level Security")
        else:
            flag("critical", f"{label} in {where} (line {line})")


def check_url(target):
    if "://" not in target:
        target = "https://" + target
    parts = urllib.parse.urlsplit(target)
    host = parts.hostname or ""
    if parts.scheme not in ("http", "https") or not re.fullmatch(r"[a-z0-9.-]+", host.lower()) or "." not in host:
        print("Not a public web address.")
        sys.exit(2)
    print(f"Checking {shown(target)}")

    try:
        final_url, status, headers, body = fetch(target, host)
    except ValueError as e:
        print(f"Could not check: {e}")
        sys.exit(2)
    note(f"page: HTTP {status} at {shown(final_url)}")

    # Plain http:// must end on https:// of the same site, within a few hops.
    try:
        url, verdict = f"http://{host}/", None
        for _ in range(MAX_REDIRECTS):
            _, code, hdrs, _ = fetch(url, host, follow=False)
            loc = hdrs.get("Location")
            if code not in (301, 302, 303, 307, 308) or not loc:
                verdict = f"http:// answers HTTP {code} without redirecting to https://"
                break
            nxt = urllib.parse.urlsplit(urllib.parse.urljoin(url, loc))
            if not same_site(nxt.hostname or "", host):
                verdict = f"http:// redirects to another host ({nxt.hostname})"
                break
            if nxt.scheme == "https":
                break
            url = nxt.geturl()
        else:
            verdict = "http:// redirects too many times"
        if verdict:
            flag("high", verdict)
        else:
            note("ok: http:// redirects to https://")
    except ValueError as e:
        missed(f"http:// redirect: {e}")

    def has(name):
        return headers.get(name) is not None

    csp = headers.get("Content-Security-Policy", "") or ""
    note("ok: Strict-Transport-Security") if has("Strict-Transport-Security") else flag("medium", "missing Strict-Transport-Security")
    note("ok: Content-Security-Policy") if csp else flag("medium", "missing Content-Security-Policy")
    note("ok: X-Content-Type-Options") if has("X-Content-Type-Options") else flag("low", "missing X-Content-Type-Options: nosniff")
    if has("X-Frame-Options") or "frame-ancestors" in csp:
        note("ok: frame protection")
    else:
        flag("medium", "missing frame protection (X-Frame-Options or CSP frame-ancestors)")
    note("ok: Referrer-Policy") if has("Referrer-Policy") else flag("low", "missing Referrer-Policy")

    for cookie in headers.get_all("Set-Cookie") or []:
        name = cookie.split("=", 1)[0].strip()
        attrs = cookie.lower()
        if "; secure" not in attrs and ";secure" not in attrs:
            flag("medium", f"cookie {name} has no Secure flag")
        if re.search(r"sess|auth|token|sid", name, re.I) and "httponly" not in attrs:
            flag("high", f"session cookie {name} has no HttpOnly flag")

    scan_text(body, "the page")

    parser = ScriptParser()
    try:
        parser.feed(body)
    except Exception:
        missed("the page's HTML could not be parsed for scripts")
    scripts, other_hosts = [], 0
    for src in parser.srcs:
        url = urllib.parse.urljoin(final_url, src)
        u = urllib.parse.urlsplit(url)
        if u.scheme not in ("http", "https"):
            continue
        if not same_site(u.hostname or "", host):
            other_hosts += 1
            continue
        if url not in scripts:
            scripts.append(url)
    if other_hosts:
        note(f"{other_hosts} script(s) from other hosts not read (they are not this site's code)")
    if len(scripts) > MAX_SCRIPTS:
        missed(f"{len(scripts) - MAX_SCRIPTS} of the site's scripts beyond the first {MAX_SCRIPTS}")
        scripts = scripts[:MAX_SCRIPTS]

    for js_url in scripts:
        try:
            js_final, js_status, js_headers, js = fetch(js_url, host)
        except ValueError as e:
            missed(str(e))
            continue
        if js_status >= 400:
            missed(f"{shown(js_url)} answered HTTP {js_status}")
            continue
        scan_text(js, shown(js_url))
        refs = SOURCEMAP_RE.findall(js[-4096:])
        for h in ("SourceMap", "X-SourceMap"):
            if js_headers.get(h):
                refs.append(js_headers[h])
        for ref in refs:
            if ref.startswith("data:"):
                flag("low", f"inline source map in {shown(js_url)}")
                continue
            map_url = urllib.parse.urljoin(js_final, ref)
            try:
                _, map_status, _, src_map = fetch(map_url, host)
            except ValueError as e:
                missed(f"declared source map: {e}")
                continue
            if map_status == 200 and '"mappings"' in src_map[:4096]:
                flag("low", f"public source map: {shown(map_url)}")
                scan_text(src_map, shown(map_url))
    note(f"scripts read: {len(scripts)}")


# ------------------------------------------------------------- folder mode

def git(args, cwd):
    return subprocess.run(["git", "-C", cwd] + args, capture_output=True, text=True, errors="replace")


def check_dir(folder):
    folder = os.path.abspath(folder)
    print(f"Checking folder {folder}")
    in_git = git(["rev-parse", "--is-inside-work-tree"], folder).stdout.strip() == "true"
    tracked, ignored = set(), set()
    if in_git:
        top = git(["rev-parse", "--show-toplevel"], folder).stdout.strip()
        tracked = {os.path.join(top, p) for p in git(["ls-files", "-z"], folder).stdout.split("\0") if p}
        ign = git(["ls-files", "-z", "--others", "--ignored", "--exclude-standard"], folder).stdout
        ignored = {os.path.join(top, p) for p in ign.split("\0") if p}

    too_big, outside = 0, 0
    real_root = os.path.realpath(folder)
    for root, dirs, files in os.walk(folder):  # does not follow symlinked folders
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            path = os.path.join(root, name)
            rel = os.path.relpath(path, folder)
            if os.path.islink(path) and not os.path.realpath(path).startswith(real_root + os.sep):
                outside += 1
                continue
            try:
                if os.path.getsize(path) > MAX_BYTES:
                    too_big += 1
                    continue
                with open(path, "rb") as fh:
                    raw = fh.read()
            except OSError as e:
                missed(f"{rel}: {e.strerror}")
                continue
            if b"\0" in raw[:4096]:
                continue  # binary
            text = raw.decode("utf-8", "replace")
            for label, line in key_hits(text):
                where = f"{rel}:{line}"
                if not in_git:
                    flag("high", f"{label} in {where} (not a git repository: cannot tell if it is shared)")
                elif path in tracked:
                    flag("critical", f"{label} in {where}, which is committed to git")
                elif path in ignored:
                    note(f"[info] {label} in {where}, a local file git ignores. Fine for a server secret, as long as it never ships to the browser")
                else:
                    flag("high", f"{label} in {where}, which git does not ignore: it would be committed")
    if too_big:
        note(f"{too_big} file(s) over {MAX_BYTES // (1024 * 1024)} MB were not read")
    if outside:
        note(f"{outside} symlink(s) pointing outside the folder were not followed")
    note("skipped folders: " + ", ".join(sorted(SKIP_DIRS)))

    if not in_git:
        note("not a git repository: history not checked")
        return
    env_files = [p for p in tracked if re.search(r"(^|/)\.env(\.[A-Za-z]+)?$", p) and not re.search(r"\.(example|sample|template)$", p)]
    for p in sorted(env_files):
        flag("high", f"env file committed to git: {os.path.relpath(p, folder)}")
    # Stream the history with a byte cap; scan in pieces that overlap so a
    # key split across two pieces is still found.
    proc = subprocess.Popen(["git", "-C", folder, "log", "-p", "--all", f"-n{HISTORY_COMMITS}", "--no-color"],
                            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    labels, read, tail, truncated = set(), 0, "", False
    while True:
        chunk = proc.stdout.read(1024 * 1024)
        if not chunk:
            break
        read += len(chunk)
        text = tail + chunk.decode("utf-8", "replace")
        labels.update(label for label, _ in key_hits(text))
        tail = text[-4096:]
        if read >= HISTORY_BYTES:
            truncated = True
            proc.kill()
            break
    proc.wait()
    if truncated:
        missed(f"git history beyond the first {HISTORY_BYTES // (1024 * 1024)} MB of the last {HISTORY_COMMITS} commits")
    elif proc.returncode not in (0, None):
        missed("git history could not be read")
    for label in sorted(labels):
        flag("critical", f"{label} in git history (last {HISTORY_COMMITS} commits); deleting it now does not remove it from history")


def main():
    if len(sys.argv) != 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(2)
    target = sys.argv[1]
    if os.path.isdir(target):
        check_dir(target)
    else:
        check_url(target)
    print()
    if findings:
        print(f"{len(findings)} finding(s). Fix critical and high before launch.")
        if incomplete:
            print(f"Also incomplete: {len(incomplete)} read(s) failed, listed as [not checked].")
        sys.exit(1)
    if incomplete:
        print(f"No findings in what was read, but {len(incomplete)} read(s) failed. This is not a clean result.")
        sys.exit(3)
    print("No findings.")
    sys.exit(0)


if __name__ == "__main__":
    main()
