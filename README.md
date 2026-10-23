# Pugi skills

Agent Skills for [Pugi](https://pugi.io), the AI product team that turns a plain brief into a live, tested app. Install them in Claude Code, Cursor, Codex or any agent that reads the [Agent Skills](https://agentskills.io/specification) format, and your agent can brief Pugi to build and deliver an app, design it, start from a template, make a brand and a site in it, check and fix security, and publish.

| Skill | What it does | Works today through |
|---|---|---|
| [`pugi-build`](skills/pugi-build/SKILL.md) | Writes a good brief and starts a Pugi build: the quick path from an idea to a project | `pugi build` (CLI) and app.pugi.io |
| [`pugi-sdlc`](skills/pugi-sdlc/SKILL.md) | Steers the full delivery run: plan, plan approval, build, tests, security scan, preview approval, going live, with JSON status | `pugi sdlc` (CLI) and app.pugi.io |
| [`pugi-artifacts`](skills/pugi-artifacts/SKILL.md) | Gets the project documents (brief, BRD, PRD, user flow, mockups, spec, test plan), then reads, previews and revises them | `pugi artifacts` (CLI) and the Delivery bundle view |
| [`pugi-design`](skills/pugi-design/SKILL.md) | Draws or changes the app's design in Design mode and applies it to the code. It can save a Pugi design file for a later Figma import (no public import plugin yet) | app.pugi.io, Founder plan or higher |
| [`pugi-start-from-template`](skills/pugi-start-from-template/SKILL.md) | Starts a project from one of 31 starters, or lays a starter down locally | app.pugi.io/templates and `pugi scaffold` |
| [`pugi-logo`](skills/pugi-logo/SKILL.md) | Gets logo concepts and a brand kit for a business, then wires the kit into the site | [logo.pugi.io](https://logo.pugi.io) |
| [`pugi-brand-to-site`](skills/pugi-brand-to-site/SKILL.md) | Turns a logo.pugi.io brand into a new website in the same brand | logo.pugi.io, then app.pugi.io |
| [`pugi-security-check`](skills/pugi-security-check/SKILL.md) | Checks a live site or a repo for leaked keys, missing security headers, insecure cookies, public source maps and committed `.env` files | A bundled script, plus [pugi.io/security/audit](https://pugi.io/security/audit) |
| [`pugi-fix-security`](skills/pugi-fix-security/SKILL.md) | Has Pugi fix the findings ("Let Pugi fix all") and checks again | app.pugi.io and pugi.io/security/audit |
| [`pugi-deploy-repo`](skills/pugi-deploy-repo/SKILL.md) | Imports an existing GitHub repo (from Lovable, Bolt, v0 or anywhere) and publishes it | Import from GitHub at app.pugi.io, or `git clone` + `pugi publish` |
| [`pugi-publish`](skills/pugi-publish/SKILL.md) | Publishes a folder to a live `*.pugi.app` address with HTTPS, then connects your own domain | `pugi publish` (CLI) and the Publish panel |

Which one to use: `pugi-build` starts a run; `pugi-sdlc` takes a run through its gates to going live; `pugi-publish` and `pugi-deploy-repo` put code you already have online.

Each skill has a status table that marks every step as **Available**, **Not available today** or **Coming soon**. The skills use only what is live: the `pugi` CLI (`@pugi/cli` 1.0.0-alpha.246 or later, the version the commands were tested against) and pugi.io pages. More agent tools are coming; the skills tell the agent to use them only once they appear in its tool list or in https://pugi.io/llms.txt.

## Requirements

- For the CLI skills (`pugi-build`, `pugi-sdlc`, `pugi-artifacts`, `pugi-publish`, `pugi-deploy-repo`): Node.js 18+, git, and a Pugi account. Install the CLI with `npm i -g @pugi/cli` and sign in with `pugi login`. The sign-in is a device flow: you approve it in your browser.
- For `pugi-security-check`: Python 3.8+ and git. The script uploads nothing; the optional MCP tool `scan_url` sends the URL to Pugi.
- For the console skills (`pugi-design`, `pugi-start-from-template`, `pugi-brand-to-site`, `pugi-fix-security`, `pugi-logo`): a browser. `pugi-design` needs the Founder plan or higher.

Plans and limits: [pugi.io/pricing](https://pugi.io/pricing).

## Install

### Claude Code

As a plugin from this repository's marketplace:

```bash
claude plugin marketplace add pugi-io/skills
claude plugin install pugi@pugi
```

Inside a session the same commands are `/plugin marketplace add pugi-io/skills` and `/plugin install pugi@pugi`. The skills then run as `/pugi:<skill>` (for example `/pugi:pugi-publish`), and Claude also picks them up on its own when a task matches.

Without the plugin, copy the skill folders into your skills directory:

```bash
git clone https://github.com/pugi-io/skills pugi-skills
mkdir -p ~/.claude/skills
cp -r pugi-skills/skills/* ~/.claude/skills/        # or .claude/skills/ in a project
```

### Cursor

Cursor loads Agent Skills from `.cursor/skills/` and `.agents/skills/` in a project, and from `~/.cursor/skills/` and `~/.agents/skills/` for your user. It also reads `.claude/skills/` and `.codex/skills/`.

```bash
git clone https://github.com/pugi-io/skills pugi-skills
mkdir -p ~/.cursor/skills && cp -r pugi-skills/skills/* ~/.cursor/skills/
```

The repository is also laid out as a single Cursor plugin, following https://github.com/cursor/plugin-template: `.cursor-plugin/plugin.json` at the root with `name`, `description`, `version` and `author`, and the skills in `skills/`. It is not in the Cursor Marketplace yet.

### Codex

Codex reads skills from `.agents/skills/` in the repository (from the working directory up to the repository root) and from `~/.agents/skills/` for your user.

```bash
git clone https://github.com/pugi-io/skills pugi-skills
mkdir -p ~/.agents/skills && cp -r pugi-skills/skills/* ~/.agents/skills/
```

Or ask the built-in installer for one skill:

```text
$skill-installer install https://github.com/pugi-io/skills/tree/main/skills/pugi-publish
```

Restart Codex so it picks up new skills. Each skill has an `agents/openai.yaml` with its display name and default prompt. Skills whose main action can spend credits, publish or change a project set `allow_implicit_invocation: false`, so Codex runs them only when you call them, for example `$pugi-publish`. Only `pugi-security-check` and `pugi-logo` may start on their own. Every skill asks for the user's yes before anything is built, spends credits or goes live.

The repository is also a plugin in the open Agent Plugins format (`plugin.json` at the root, with Codex settings under `extensions.com.openai`), with `.codex-plugin/plugin.json` kept as a fallback and a marketplace file at `.agents/plugins/marketplace.json`:

```bash
codex plugin marketplace add pugi-io/skills
```

### Any other agent

Each skill is a folder with a `SKILL.md` (YAML front matter plus Markdown) and optional `scripts/`. Copy `skills/<name>/` to wherever your agent loads skills from.

## Layout

```text
.
├── .claude-plugin/
│   ├── plugin.json          Claude Code plugin manifest
│   └── marketplace.json     Claude Code marketplace (one plugin: this repo)
├── plugin.json              Agent Plugins manifest (Codex reads extensions.com.openai)
├── .codex-plugin/plugin.json  Codex fallback manifest
├── .agents/plugins/marketplace.json
├── .cursor-plugin/plugin.json
├── assets/icon.png  assets/NOTICE
├── skills/                 one folder per skill: SKILL.md, agents/openai.yaml, optional scripts/
│   ├── pugi-build/  pugi-sdlc/  pugi-artifacts/  pugi-design/
│   ├── pugi-start-from-template/  pugi-logo/  pugi-brand-to-site/
│   ├── pugi-security-check/     scripts/precheck.py
│   ├── pugi-fix-security/  pugi-deploy-repo/
│   └── pugi-publish/            scripts/check-domain.sh
└── scripts/check.sh         Validates front matter and scans this repo for secrets
```

The skills format is the same for every agent: one `SKILL.md` per folder. Only the plugin manifests differ, so each agent gets its own manifest next to the shared `skills/` folder.

## Formats this repository follows

- Agent Skills specification: https://agentskills.io/specification
- Claude Code plugins, manifest reference: https://code.claude.com/docs/en/plugins/manifest-reference
- Claude Code plugin marketplaces: https://code.claude.com/docs/en/plugin-marketplaces and https://code.claude.com/docs/en/plugins/marketplace-reference
- Codex skills: https://learn.chatgpt.com/docs/build-skills
- Codex plugins and marketplaces, and the portable root plugin.json: https://developers.openai.com/plugins/build/plugins
- Cursor skills: https://cursor.com/docs/skills
- Cursor plugins: https://cursor.com/docs/plugins and the single-plugin layout in https://github.com/cursor/plugin-template

## Check before you contribute

```bash
bash scripts/check.sh
```

It validates every skill with the Agent Skills reference validator (`skills-ref`, run through `uvx`) and this repository's own rules, checks that each manifest has the fields its format requires, and scans every file, scripts included, for key-shaped strings. It reports a match by rule, file and line, never by its text. It also runs `gitleaks` on the tree and the history with redaction. Any check that cannot run fails the release, so it needs `uvx` and `gitleaks` installed.

## Security

Report a vulnerability to security@pugi.io. See [SECURITY.md](SECURITY.md).

## License

The skills, scripts and documentation are under the MIT License. See [LICENSE](LICENSE). Each skill folder carries its own copy as `LICENSE.txt`, so a skill copied on its own keeps the notice.

`assets/icon.png` is the Pugi logo. It is not under the MIT License. It is included only so that plugin directories can show this plugin with its icon, and you may redistribute it unchanged as part of this repository for that purpose. "Pugi" and the Pugi logo are trademarks of Pugi Inc.; the license gives no right to use them otherwise. See [assets/NOTICE](assets/NOTICE).
