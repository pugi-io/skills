---
name: pugi-artifacts
description: Have Pugi write a project's delivery documents from a brief - customer brief, business requirements (BRD), product requirements (PRD), user flow, mockups, technical spec and test plan, plus a design spec and a clickable prototype in the console - then list, read, preview and revise them. Use when the user wants a PRD, BRD, spec, test plan or other planning documents for an app, or wants to read or change the plan Pugi wrote.
license: MIT (see LICENSE.txt)
compatibility: Needs @pugi/cli 1.0.0-alpha.246 or later, Node.js 18+, network access and a Pugi account (the user approves the sign-in in a browser). Writing documents uses the user's Pugi plan allowance.
metadata:
  author: Pugi Inc.
  version: "0.1.0"
  homepage: https://pugi.io
---

# Get project documents from Pugi

## What works today

| Step | Surface | Status (checked 2026-10-24) |
|---|---|---|
| Write the documents from a brief | `pugi artifacts generate` | Available |
| List, preview, read one | `pugi artifacts list`, `preview`, `show <kind>` | Available |
| Revise the plan during a run | `pugi sdlc request-changes` (see `pugi-sdlc`) | Available |
| The same documents with buttons | Delivery bundle view at https://app.pugi.io (**Generate bundle**, **Refresh**) | Available |
| Edit a document's text directly | — | Not available: revise through the brief or a change request |
| More agent tools | — | Coming soon |

## The documents

`pugi artifacts show` takes these kinds:

| Kind | Document |
|---|---|
| `brief` | Customer brief: intent, constraints and open questions |
| `brd` | Business requirements: goals, users, scope, assumptions and success metrics |
| `prd` | Product requirements: features, user stories, acceptance criteria and edge cases |
| `userflow` | User flow across the key screens and states |
| `mockups` | Screen wireframes and interaction notes |
| `spec` | Technical spec: architecture, API contracts, data models and deployment notes |
| `test-plan` | Test cases, coverage targets and acceptance criteria |

The console also shows a **Design spec** and a clickable **Prototype** (see `pugi-design`).

## Rules

- Writing the documents uses some of the user's plan allowance. Show the brief and get a yes first. Approving the plan afterwards starts the build, which costs more (see `pugi-sdlc`).
- Do not run `generate` again after an error or timeout before checking `pugi artifacts list`: the first one may be running. Each new generation needs the user's yes.
- Never paste a document's full text into a public place without the user's say-so. It describes their product.

## Steps

1. Install the CLI and sign in. `pugi login` prints a link and a code, and the user approves in the browser.
   ```bash
   npm i -g @pugi/cli@latest && pugi --version     # 1.0.0-alpha.246 or later
   pugi login
   ```
2. Write the documents. Add `--project <projectId>` to write them for an existing project.
   ```bash
   pugi artifacts generate --brief "<the brief>" --format json
   ```
   This is the planning part of a Pugi run, the same one `pugi build` starts. It can take several minutes, then waits at plan approval. The build does not start until the user approves the plan. Keep the project id from the output, and track progress with `pugi artifacts list`.
3. Check which documents are ready, then read them.
   ```bash
   pugi artifacts list --project <projectId> --format json
   pugi artifacts preview --project <projectId>
   pugi artifacts show prd --project <projectId>
   ```
   Without `--project`, the commands use the latest run's project.
4. Revise:
   - Inside a run waiting at plan approval, send the user's reason with `pugi sdlc request-changes`. Pugi rewrites the plan from it; the CLI allows up to 3 change requests per run. See `pugi-sdlc`.
   - Outside a run, edit the brief and generate again. The console shows each document's version.
5. To build from the approved documents, continue with `pugi-sdlc`.

## Exit codes

5 means not signed in: run `pugi login`. 6 means a network or server error, or that the documents are not ready yet: wait, then read `pugi artifacts list` again. Reading is safe to repeat; generating is not. 7 means rate limited: wait the seconds it names.

## Coming soon

More agent tools are coming. Use a Pugi tool only when it appears in your tool list or in https://pugi.io/llms.txt. Until then, use the steps above.
