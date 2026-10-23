---
name: pugi-publish
description: Publish a website or web app to a live *.pugi.app address with HTTPS, then connect the user's own domain. Use when the user asks to deploy, publish, host, ship or put a site online with Pugi, or to point a custom domain at a Pugi app.
license: MIT (see LICENSE.txt)
compatibility: Needs @pugi/cli 1.0.0-alpha.246 or later, Node.js 18+, git, network access, and a Pugi account (the user approves the sign-in in a browser).
metadata:
  author: Pugi Inc.
  version: "0.1.0"
  homepage: https://pugi.io
---

# Publish a site with Pugi

## What works today

| Step | Surface | Status (checked 2026-10-24) |
|---|---|---|
| Publish a folder to `*.pugi.app` | `pugi publish` (CLI `@pugi/cli` 1.0.0-alpha.246 or later) | Available. Publishing on a pugi.app address is included on every plan (https://pugi.io/pricing) |
| Check publish status (`publish_status`) and credit (`get_balance`, `buy_credits_link`) | Pugi MCP server `https://api.pugi.io/api/agent/v1/mcp`, see "Pugi MCP server" below | Available, free |
| Connect your own domain | Publish panel at https://app.pugi.io | Available; see https://pugi.io/pricing for the plans that include it |
| Check the domain's DNS | `scripts/check-domain.sh` in this skill | Available |
| Publish through the MCP server | — | Not available today |
| More agent tools | — | Coming soon |

Use only the available rows. Publishing itself goes through the CLI or the console.

## Rules

- Publishing makes the site public. Ask the user before you run `pugi publish`, and wait for a clear yes. Pugi never publishes on its own, and you should not either.
- Never print or paste secret values. `pugi publish` prints only the names of env keys.
- Do not re-run a publish on your own. A timeout does not mean the first publish failed. Check first (see Exit codes), then ask the user.
- Changing DNS moves the domain's traffic. Show the user the current and the new record and get a yes before anyone changes it.

## Steps

1. Install the CLI and check the version is 1.0.0-alpha.246 or later.
   ```bash
   npm i -g @pugi/cli@latest
   pugi --version
   ```
2. Sign in. `pugi login` prints a link and a code. Tell the user to open the link and approve. Wait until the command finishes.
   ```bash
   pugi login
   ```
3. Check the folder.
   - Run it from the project root. Pugi builds it on its side. A folder of plain static files (an `index.html` at its root) also works.
   - The CLI states its own limits (5,000 files, 10 MB per file, 25 MB in total in 1.0.0-alpha.246) and leaves out files that `.gitignore` ignores.
   - Environment: unless you pass `--no-env`, the CLI sends the values in `.env` and `.env.production` as the app's production environment. Before publishing, list the key names (not the values) to the user and ask which belong in production. Remove any key that does not belong from those files, or move it to `.env.local`, which is not sent. Use `--no-env` only if the user says no key belongs in production. Add `--env-file <file>` only for a file the user names.
   - Run the `pugi-security-check` skill on the folder first if it is installed.
4. Publish and read the JSON result.
   ```bash
   pugi publish --json                       # after the user approved the env key list
   pugi publish --directory ./site --json    # a folder of static files
   pugi publish --no-env --json              # only if no key belongs in production
   ```
   The result has `deployment.url` and `deployment.status`. `ready` means live. Any other status that is not `error` means the build is still running: open the URL again later instead of publishing again.
5. Give the user the live URL.

## Exit codes of `pugi publish`

| Code | Meaning | What to do |
|---|---|---|
| 0 | Published, or still building | Share `deployment.url` |
| 1 | Error (message says which) | Fix what the message names and run again |
| 4 | The account's plan does not allow this publish right now (for example the plan changed or a limit was reached) | Send the user to https://pugi.io/pricing |
| 5 | Not signed in | Run `pugi login` |
| 6 | Network or server error | Do not re-run yet. Check whether the publish went through: the project's Publish panel at https://app.pugi.io, the app's URL, or the MCP tool `publish_status`. Run again only if it did not, and only with the user's yes |
| 7 | Rate limited | Wait the seconds it names |

## Pugi MCP server

Live since 2026-10-24: `https://api.pugi.io/api/agent/v1/mcp` (Streamable HTTP, POST, JSON). It needs an agent key sent as `Authorization: Bearer <key>`.

- Creating a key (`POST https://api.pugi.io/api/agent/v1/keys`) creates a Pugi agent account, or adds the key to the user's account when the request is signed in. The key is shown once. Ask the user before creating one, and store it where they say, never in the repository.
- Tools open today, all free and read-only: `scan_url` (passive check of a public site, graded A+ to F), `publish_status` (the account's published apps with status and live address), `get_balance` (credit, today's spend and the key's daily cap) and `buy_credits_link` (a checkout link a person opens; it never charges by itself).
- Prices and which tools are open: `GET https://api.pugi.io/api/agent/v1/pricing`. Other tools listed there as not available must not be called.
- Revoke a key with `DELETE https://api.pugi.io/api/agent/v1/keys/self` sent with that key.

## Connect your own domain

1. Publish first (above). Note the app's host, for example `your-app.pugi.app`.
2. The user opens the project at https://app.pugi.io, then Publish, then **Custom domain**, enters a subdomain they control, for example `app.example.com`, and presses **Add**. The panel then shows the exact DNS record to create.
3. Before anyone edits DNS, look at what the domain has now:
   ```bash
   dig +short app.example.com
   ```
   If it already points somewhere (a live site, email, another service), show the user the current record next to the new one and say that the change moves the domain's traffic to the Pugi app. Get a clear yes.
4. At the domain's registrar, the user creates the record. It is normally:
   - Type: `CNAME`
   - Name: the subdomain part (`app` for `app.example.com`, `www` for `www.example.com`)
   - Value: the app's `*.pugi.app` host
   If the panel shows a different value, use the panel's value. A root domain such as `example.com` cannot take a CNAME at most registrars. Use `www.` or `app.`.
5. When the record exists, press **Check**. The domain shows **Verified** when Pugi serves the app there. This is the authoritative check.
6. To see what DNS and HTTPS say from here. `<skill folder>` is the folder that holds this SKILL.md; installed as a Claude Code plugin it is `${CLAUDE_PLUGIN_ROOT}/skills/pugi-publish`.
   ```bash
   bash <skill folder>/scripts/check-domain.sh app.example.com your-app.pugi.app      # add --resolver <ip> to pick a resolver
   ```
   It uses your system's DNS resolver and makes one HTTPS request to the domain. It reports DNS, HTTPS and Pugi's check separately. Exit 0: the CNAME chain reaches the app and HTTPS answers. 1: not yet. 3: DNS only shows addresses (a flattened or proxied record), so rely on the panel's Check. DNS changes can take a while to spread.

## Coming soon

More agent tools are coming. Use a Pugi tool only when it appears in your tool list or in https://pugi.io/llms.txt. Until then, use the steps above.
