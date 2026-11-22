---
name: pugi-local-start-prompts
description: Help a non-technical teammate open Pugi web apps locally, choose staging or production safely, or ask for help when startup fails. Use when someone needs a simple copy-and-paste request for local Pugi apps; this does not deploy or publish anything.
license: MIT (see LICENSE.txt)
metadata:
  author: Pugi Inc.
  version: "0.1.0"
  homepage: https://pugi.io
---

# Help someone start Pugi locally

Use the matching ready-to-copy Russian prompt from [prompts.md](references/prompts.md). The prompts ask an assistant with access to the Pugi workspace to do the local setup and startup, then explain which page to open and how to stop it in everyday language.

## Source of truth

- Local app IDs, setup, login, environment profiles, ports, and known limits: `pugi-frontend-devbox/docs/run-openchamber-locally.md`.
- App ownership and local UI map: `docs/PUGI-FRONTEND-MAP.md` in the Pugi workspace.
- Devbox registry and profile behavior: `pugi-frontend-devbox/config/apps.mjs` and `config/backends.mjs`.

Check these sources before changing the prompts or telling someone a service is ready. URLs and prerequisites can change.

## Guidance

- Default to staging for QA. If staging access or a required tunnel is unavailable, stop and explain the one missing prerequisite; never silently switch to production.
- For production, use the production-specific prompt and keep the session read-only unless the user separately authorizes an action that changes data, generates content, publishes, or spends credits.
- Do not ask a non-technical user to paste passwords, tokens, cookies, or SSH keys. Use an existing authorized local setup; if it is missing, explain who can grant access.
- Starting a local UI is not proof that login, APIs, or the full product flow work. Say which page and checks actually succeeded, and call out anything skipped.
- Keep the local server running until the user is done. Explain that closing the terminal stops it; give `Ctrl+C` as the normal stop action.
- Do not deploy, publish, merge, push code, or change remote data as part of a local-start request.
