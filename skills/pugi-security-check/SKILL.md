---
name: pugi-security-check
description: Check a website or a code repository for security problems before launch, such as leaked API keys (Supabase service_role, Stripe, OpenAI, Anthropic, AWS, GitHub, Slack, Google, private keys), missing security headers, insecure cookies, public source maps, committed .env files. Use before publishing, when the user asks if their site or AI-built app (Lovable, Bolt, v0 or any other) is safe, or asks for a security check or audit.
license: MIT (see LICENSE.txt)
compatibility: Needs Python 3.8+ (standard library only); git for the history check. URL mode needs network access.
metadata:
  author: Pugi Inc.
  version: "0.1.0"
  homepage: https://pugi.io/security/audit
---

# Check a site or repo before launch

## What works today

| Check | Surface | Status (checked 2026-10-24) |
|---|---|---|
| Passive check of a live URL | `scripts/precheck.py <url>` in this skill | Available |
| Secrets in a folder and its git history | `scripts/precheck.py <folder>` in this skill | Available |
| Graded report A+ to F, full list by email | https://pugi.io/security/audit (web page, free, no account) | Available, for a person in a browser |
| Scan of every build made with Pugi | Runs on every Pugi build before it can be published | Available, automatic |
| Pentest of the running preview | Paid Pugi plans, the customer's own preview only | Available, see https://pugi.io/security/pentest |
| Passive URL check as a tool (`scan_url`), graded A+ to F | Pugi MCP server `https://api.pugi.io/api/agent/v1/mcp`, see "Pugi MCP server" below | Available, free. It answered "temporarily unavailable" in a test on 2026-10-24; if so, use the script |
| Repository scan as a tool | None today | Not available today |
| More agent tools | Not released yet | Coming soon |

## Rules

- Check only sites and repos the user owns or is allowed to test.
- URL mode reads what a browser is given: the page, up to ten of the site's own scripts, and the source maps those scripts declare. It sends no form data and guesses no paths. It follows redirects only within the same site (the host or its `www.` twin) and never from https to http. It resolves each host once, refuses non-public addresses (private, loopback, link-local, NAT64, 6to4), and connects only to the address it checked. Output shows addresses without credentials or query strings.
- Never paste a found key into chat, a commit or an issue. The script reports the key type, file and line only, never the value. Do the same.

## Steps

1. Pick the target: a live URL, or the project folder.
2. Run the check. `<skill folder>` is the folder that holds this SKILL.md; installed as a Claude Code plugin it is `${CLAUDE_PLUGIN_ROOT}/skills/pugi-security-check`.
   ```bash
   python3 "<skill folder>/scripts/precheck.py" https://your-app.example
   python3 "<skill folder>/scripts/precheck.py" /path/to/project
   ```
   For a live URL you can instead call the MCP tool `scan_url` if it is set up (see below).
   | Exit | Meaning |
   |---|---|
   | 0 | No findings, and everything planned was read |
   | 1 | Findings, by severity. The summary says if some reads also failed |
   | 2 | Usage error, or the target could not be reached |
   | 3 | No findings, but some reads failed (`[not checked]` lines). This is not a clean result: tell the user what was not checked |
3. Read each key finding by where the key is:
   - **In the page, a script, a source map, a committed file or git history**: the key is exposed. Ask the user to revoke it at the provider and create a new one first. Then move it to a server-side environment variable and remove it from the code. Deleting it from the latest commit does not remove it from history.
   - **In a file git does not ignore**: it is not shared yet, but it would be committed. Add the file to `.gitignore` (or move the key) before the next commit. No revoke is needed if it was never pushed or shared.
   - **`[info]` in a local file git ignores** (such as `.env.local`): normal for a server secret. Make sure it is never used in browser code.
   - **Supabase service_role key**: it bypasses Row Level Security. If exposed, revoke it. In the browser use only the anon key, with Row Level Security on for every table the anon role can reach.
4. Fix the rest:
   - **high: env file committed, no HTTPS redirect, session cookie without HttpOnly.** Stop tracking the file (`git rm --cached .env`, add it to `.gitignore`), redirect `http://` to `https://`, and set `HttpOnly` on session cookies.
   - **medium and low: headers and source maps.** Add `Strict-Transport-Security`, `Content-Security-Policy`, `X-Content-Type-Options: nosniff`, `X-Frame-Options` (or CSP `frame-ancestors`) and `Referrer-Policy`. Turn off public source maps in the production build.
5. Run the check again until critical and high are gone. To have Pugi make the fixes, see `pugi-fix-security`.
6. For a graded report the user can keep, send them to https://pugi.io/security/audit with the URL.

## Pugi MCP server

Live since 2026-10-24: `https://api.pugi.io/api/agent/v1/mcp` (Streamable HTTP, POST, JSON). It needs an agent key sent as `Authorization: Bearer <key>`.

- Creating a key (`POST https://api.pugi.io/api/agent/v1/keys`) creates a Pugi agent account, or adds the key to the user's account when the request is signed in. The key is shown once. Ask the user before creating one, and store it where they say, never in the repository.
- Tools open today, all free and read-only: `scan_url` (passive check of a public site, graded A+ to F), `publish_status` (the account's published apps with status and live address), `get_balance` (credit, today's spend and the key's daily cap) and `buy_credits_link` (a checkout link a person opens; it never charges by itself).
- Prices and which tools are open: `GET https://api.pugi.io/api/agent/v1/pricing`. Other tools listed there as not available must not be called.
- Revoke a key with `DELETE https://api.pugi.io/api/agent/v1/keys/self` sent with that key.

## Limits

- Not a pentest, and it does not prove a site is secure. Keys that live only on a server are out of its reach.
- URL mode: at most ten scripts from the site itself, 2 MB and 30 seconds per response. Scripts from other hosts are not read.
- Folder mode: files up to 2 MB; skips `node_modules`, `.git`, `dist`, `build`, `.next`, `.output`, `.vercel`, `coverage`; does not follow symlinks out of the folder; git history is the last 200 commits, up to 64 MB of it (more is reported as not checked).
- Dependency and code review need a full scan. Every app built with Pugi gets one on each build.

## Coming soon

More agent tools are coming. Use a Pugi tool only when it appears in your tool list or in https://pugi.io/llms.txt. Until then, use the steps above.
