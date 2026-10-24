---
name: pugi-deploy-repo
description: Bring an existing app from a GitHub repository into Pugi and publish it to a live *.pugi.app address. Good for apps built elsewhere (Lovable, Bolt, v0, or by hand). Covers the console's Import from GitHub, connecting GitHub for private repositories, setting the app's environment, and the CLI path (clone, then pugi publish). Use when the user wants to host, deploy or move an existing repo or AI-built app to Pugi.
license: MIT (see LICENSE.txt)
compatibility: Console import needs a browser and a Pugi account; private repositories need the Pugi GitHub App connected. The CLI path needs @pugi/cli 1.0.0-alpha.246 or later, Node.js 18+, git, and Python 3.8+ for the check.
metadata:
  author: Pugi Inc.
  version: "0.1.0"
  homepage: https://pugi.io
---

# Deploy an existing GitHub repo with Pugi

## What works today

| Step | Surface | Status (checked 2026-10-24) |
|---|---|---|
| **Import from GitHub** (paste the repository URL) | New project dialog at https://app.pugi.io | Available, every plan |
| **Connect GitHub** for private repositories | Same dialog | Available |
| Publish the imported project | **Publish** button in the project | Available. Publishing on a pugi.app address is included on every plan (https://pugi.io/pricing) |
| Clone locally, then `pugi publish` | CLI `@pugi/cli` 1.0.0-alpha.246 or later (see `pugi-publish`) | Available |
| Push changes back to GitHub as a pull request | None today | Not available today |
| More agent tools | Not released yet | Coming soon |

## Rules

- Publishing makes the app public. Get the user's clear yes before **Publish** or `pugi publish`.
- Any work the user asks Pugi to do on the imported code uses the plan allowance. Ask first.
- Never copy secret values into chat. Server-only keys go into the app's environment, not into the code.
- Review the environment before publishing: list the key names (not the values) to the user and get a yes for the list. Then publish once.
- Do not re-run a publish on your own after an error; check first (see `pugi-publish`).

## Path A: in the console

1. The user signs in at https://app.pugi.io, starts a new project and picks **Import from GitHub** ("Clone an existing repository").
2. For a private repository, they press **Connect GitHub** first and install the Pugi GitHub App on that repository. In an organisation, an owner may have to approve the install.
3. They paste the repository URL (`https://github.com/owner/repo`) and press **Import**.
4. Go through the app's environment with the user. Apps from AI builders often need keys such as a Supabase URL and anon key. Anything with a `VITE_` or `NEXT_PUBLIC_` prefix ends up in the browser, so it must never be a server secret such as a Supabase service_role key.
5. Run `pugi-security-check` on the repository before going live.
6. With the user's yes, press **Publish**. If the console says the plan does not allow it, send the user to https://pugi.io/pricing. That decision is the user's.

## Path B: with the CLI

1. Clone and sign in:
   ```bash
   git clone https://github.com/owner/repo my-app && cd my-app
   npm i -g @pugi/cli@latest && pugi --version     # 1.0.0-alpha.246 or later
   pugi login
   ```
2. Check it (recommended). `<pugi-security-check folder>` is the folder of that skill; installed as a Claude Code plugin it is `${CLAUDE_PLUGIN_ROOT}/skills/pugi-security-check`.
   ```bash
   python3 "<pugi-security-check folder>/scripts/precheck.py" .
   ```
3. Review the environment. Unless you pass `--no-env`, `pugi publish` sends the values in `.env` and `.env.production` as the app's production environment. Show the user the key names in those files (never the values) and ask which belong in production. Remove the others from those files or move them to `.env.local`, which is not sent.
4. With the user's yes to the key list and to publishing, publish once:
   ```bash
   pugi publish --json
   ```
   Use `pugi publish --no-env --json` instead only if the user says no key belongs in production.

- Commit or stash local work first.
- `pugi publish` uploads the folder's files to Pugi. It never pushes to GitHub.
- The CLI states its own limits (5,000 files, 10 MB per file, 25 MB in total in 1.0.0-alpha.246).
- Exit code 4 means the account's plan does not allow this publish right now: send the user to https://pugi.io/pricing. The other exit codes are in `pugi-publish`.

## Good to know

- Pugi detects how to build the app: a static site, a Node app, or an app with its own container build.
- Changes Pugi makes to an imported project stay in the Pugi project. Sending them back to the GitHub repository as a pull request is not available today.
- For a custom domain after publishing, see `pugi-publish`.

## Coming soon

More agent tools are coming. Use a Pugi tool only when it appears in your tool list or in https://pugi.io/llms.txt. Until then, use the steps above.
