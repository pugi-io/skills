---
name: pugi-build
description: Write a good brief and start a Pugi build of a web app or website from it. This is the quick path from an idea to a running Pugi project, stopping at the plan for the user's approval. Use when the user wants Pugi to build an app or site, or to turn an idea into a working app. For steering the whole run through its gates to going live, use pugi-sdlc.
license: MIT (see LICENSE.txt)
compatibility: Needs @pugi/cli 1.0.0-alpha.246 or later, Node.js 18+, network access and a Pugi account (the user approves the sign-in in a browser). Builds use the user's Pugi plan and credits.
metadata:
  author: Pugi Inc.
  version: "0.1.0"
  homepage: https://pugi.io
---

# Brief Pugi to build an app

## What works today

| Step | Surface | Status (checked 2026-10-24) |
|---|---|---|
| Start a build from a brief | `pugi build` (CLI `@pugi/cli` 1.0.0-alpha.246 or later) | Available |
| Read the plan, approve it, follow the run | `pugi artifacts`, `pugi sdlc` (see `pugi-sdlc`) | Available |
| The same flow in a browser | https://app.pugi.io | Available |
| A local starter to build on yourself | `pugi scaffold web` or `pugi scaffold fullstack` | Available |
| More agent tools | Not released yet | Coming soon |

## Rules

- Starting a build and writing the plan use some of the plan allowance; approving the plan starts the build itself, which costs the most. Show the brief and get a yes before you start.
- Never run `pugi build` twice for the same brief without checking: after an error or timeout, look at the user's projects at https://app.pugi.io or read `pugi sdlc status` first.
- The plan Pugi writes back is the user's to approve. Show it; do not approve it on your own.
- The app goes live only when the user approves the preview at the end of the run (see `pugi-sdlc`).

## Steps

1. Write the brief in plain words. Cover:
   - who uses the app and the one job they come to do;
   - the pages or screens;
   - what data it keeps, and whether people sign in;
   - payments, if any (they go through the user's own Stripe account);
   - the language of the app (`en`, `ru` or `uk` today);
   - anything that must not change: name, colours, logo, existing copy.
   Keep it under 300 words. Leave out frameworks unless the user insists: Pugi chooses the stack.
2. Show the brief to the user and wait for a yes.
3. Install the CLI and sign in. `pugi login` prints a link and a code; the user approves in the browser.
   ```bash
   npm i -g @pugi/cli@latest && pugi --version     # 1.0.0-alpha.246 or later
   pugi login
   ```
4. Start the build and keep the IDs it returns.
   ```bash
   pugi build "<the brief>" --app my-app --locale en --detach --jsonl
   ```
   The JSON line has `projectId` and `sessionId`, plus the exact status and artifact commands.
5. Wait for the plan. Read the status every few minutes until `state` is `PLAN_APPROVAL`:
   ```bash
   pugi sdlc status --project <projectId> --session <sessionId> --format json
   ```
   Then read the plan and show it to the user.
   ```bash
   pugi artifacts preview --project <projectId>
   pugi artifacts show prd --project <projectId>
   ```
   Approving the plan starts the build, which the console describes as "what the run costs". When the user says yes:
   ```bash
   pugi sdlc approve-plan --project <projectId> --session <sessionId>
   ```
   If the user wants changes, use `pugi sdlc request-changes` with their reason.
6. From here, follow `pugi-sdlc`: it reads the status, explains each stage and stops for the preview approval. Every build is tested and security-scanned before it can go live.

## Exit codes

5 means not signed in: run `pugi login`. 6 means a network or server error: check whether the run started (step 4's IDs, the console, or `pugi sdlc status`) before running anything again, and ask the user first. 7 means rate limited: wait the seconds it names. A message about the plan or credits means the user needs to upgrade or top up at https://pugi.io/pricing.

## Coming soon

More agent tools are coming. Use a Pugi tool only when it appears in your tool list or in https://pugi.io/llms.txt. Until then, use the steps above.
