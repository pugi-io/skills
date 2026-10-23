---
name: pugi-sdlc
description: Run Pugi's full delivery loop for an app and steer it through every gate - brief, written plan, the user's plan approval, build, automated tests and security scan, live preview, the user's preview approval, and going live - reading status as JSON at each step. Use when the user wants Pugi to deliver an app end to end, asks where a Pugi run is, or needs to approve, reject or retry a stage. For just starting a build from a brief, pugi-build is enough.
license: MIT (see LICENSE.txt)
compatibility: Needs @pugi/cli 1.0.0-alpha.246 or later, Node.js 18+, network access and a Pugi account (the user approves the sign-in in a browser). Runs use the user's Pugi plan and credits.
metadata:
  author: Pugi Inc.
  version: "0.1.0"
  homepage: https://pugi.io
---

# Steer a full Pugi delivery run

Use this skill for the whole run and its gates. `pugi-build` covers writing the brief and starting the run. This skill covers everything after that.

## What works today

| Step | Surface | Status (checked 2026-10-24) |
|---|---|---|
| Start a run from a brief | `pugi build` (or `pugi sdlc start` on an existing project) | Available |
| Status as JSON | `pugi sdlc status --format json` | Available |
| Plan gate: approve or send back | `pugi sdlc approve-plan`, `pugi sdlc request-changes` | Available |
| Preview gate: approve (go live) or send back | `pugi sdlc approve`, `pugi sdlc reject` | Available |
| Resume or retry | `pugi sdlc drive`, `pugi sdlc retry` | Available |
| The same run with buttons | https://app.pugi.io | Available |
| More agent tools | — | Coming soon |

## Rules

- The run has two gates that wait for a person: the plan and the preview. Only the user decides them. Show what they are approving, then run the command only after a clear yes.
- Starting a run and writing the plan use some of the plan allowance. Approving the plan starts the build, which the console describes as "what the run costs".
- Approving the preview puts the app live on the internet.
- Every command needs `--project` and `--session`. Keep both from the start.
- Never repeat a command that can spend or deploy (`build`, `start`, `approve-plan`, `approve`, `retry`, `drive`) without reading the status first. A timeout does not mean the command failed. Never retry in a loop; each retry needs the user's yes.

## The stages, in plain words

| Stage | What happens | Who acts |
|---|---|---|
| Brief | Pugi reads the brief and expands it into a concept | Automatic |
| Plan documents | Pugi writes the brief, business and product requirements, user flow, mockups, technical spec and test plan (see `pugi-artifacts`) | Automatic |
| **Plan approval** | The run stops. `state` is `PLAN_APPROVAL` | **The user** |
| Tasks and build | The plan is split into tasks and the team writes the code | Automatic |
| Tests | The app's tests run | Automatic |
| Security scan | The exact commit is scanned for secrets, vulnerable dependencies and risky code | Automatic |
| Repository and database | The code is saved to the project's repository and the database is set up, so the preview is a real working app | Automatic |
| **Preview approval** | The run stops on a live preview. `state` is `PREVIEW_APPROVE` | **The user** |
| Going live | The app is deployed, checked and its usage recorded | Automatic |
| Done or failed | `state` is `DONE` or `FAILED` | — |

## Steps

1. Start the run with `pugi-build` steps 1 to 4. Keep `projectId` and `sessionId`. For a project that already exists:
   ```bash
   pugi sdlc start --project <projectId> --brief "<the brief>" --format json
   ```
2. Read the status. Check every few minutes; do not poll in a tight loop.
   ```bash
   pugi sdlc status --project <projectId> --session <sessionId> --format json
   ```
   The top-level `state` field says where the run is. Any value other than the gates, `DONE` and `FAILED` means Pugi is working.
3. At `PLAN_APPROVAL`, show the plan (`pugi artifacts preview --project <projectId>`) and ask the user.
   - Yes:
     ```bash
     pugi sdlc approve-plan --project <projectId> --session <sessionId>
     ```
   - Changes: pass the user's reason. Pugi rewrites the plan from it, at most 3 times.
     ```bash
     pugi sdlc request-changes --project <projectId> --session <sessionId> --reason "<what is wrong>"
     ```
4. While the build, tests and scan run, keep reading the status. Report each stage the user cares about.
5. At `PREVIEW_APPROVE`, give the user the preview link from the status or from the project at https://app.pugi.io. Ask whether it should go live.
   - Yes, put it live:
     ```bash
     pugi sdlc approve --project <projectId> --session <sessionId>
     ```
   - Not yet: send it back to the build with a reason.
     ```bash
     pugi sdlc reject --project <projectId> --session <sessionId> --reason "<what to change>"
     ```
6. At `DONE`, share the live address. For a custom domain, see `pugi-publish`.
7. At `FAILED`, read the failing stage's evidence in the status and tell the user. A retry runs the failed stage again and can use allowance. With the user's yes, once:
   ```bash
   pugi sdlc retry --project <projectId> --session <sessionId>
   ```
   Then read the status again before doing anything else.
8. If the run has not moved for a long time and is not at a gate, tell the user. With their yes, nudge it once with `pugi sdlc drive --project <projectId> --session <sessionId>`, then read the status again.

## Exit codes

5 means not signed in: run `pugi login`. 6 means a network or server error: read `pugi sdlc status` before anything else, because the command may have gone through. Run it again only if the status shows it did not, and only with the user's yes. 7 means rate limited: wait the seconds it names.

## Coming soon

More agent tools are coming. Use a Pugi tool only when it appears in your tool list or in https://pugi.io/llms.txt. Until then, use the steps above.
