---
name: pugi-fix-security
description: After a Pugi security check, have Pugi fix the findings ("Let Pugi fix all" on a project's security findings, or "Let Pugi fix it" after the free website check), then verify the fix with a new check before the app goes live. Use when the user has security findings (leaked keys, missing headers, vulnerable dependencies, risky code) on a Pugi project or on a site checked at pugi.io/security/audit and wants them fixed.
license: MIT (see LICENSE.txt)
compatibility: A person or a browser-capable agent in the Pugi console (sign-in required). Fixes use the plan allowance.
metadata:
  author: Pugi Inc.
  version: "0.1.0"
  homepage: https://pugi.io/security
---

# Let Pugi fix security findings

## What works today

| Step | Surface | Status (checked 2026-10-24) |
|---|---|---|
| **Let Pugi fix all (N)** and per-finding **Let Pugi fix it** | A project's Security tab at https://app.pugi.io | Available, every plan. Free has a daily number of checks |
| **Let Pugi fix it** after the free website check | https://pugi.io/security/audit, then sign-up | Available |
| Fixes delivered as a pull request on the user's GitHub repository | None today | Not available today |
| More agent tools | Not released yet | Coming soon |

Today the fixes are made in the Pugi project. They are not sent to GitHub as a pull request.

## Rules

- A fix run uses the plan allowance. The fix brief is put into the chat **unsent**: show it to the user and send it only after a clear yes.
- A fix does not go live by itself. Publishing is a separate yes (see `pugi-sdlc` or `pugi-publish`).
- A leaked key must be revoked at its provider by the user. Removing it from the code is not enough.

## For a Pugi project

1. Open the project at https://app.pugi.io, then its **Security** tab. Free plans show "{left} of {limit} free checks left today."
2. Press **Let Pugi fix all (N)**, or **Let Pugi fix it** on one finding. Pugi writes a brief into the project's chat and switches to it: "Fix these security findings in <project>. Keep the app working and change only what each fix needs."
3. Read the brief with the user. Remove any finding they want to keep as it is. With their yes, send it.
4. When the team is done, run the check again on the Security tab and confirm the findings are gone.
5. If a finding was a leaked key, remind the user to revoke it and set the new key in the app's environment.
6. Put the fixed app live only after the user says yes.

## For a site checked with the free website check

1. On https://pugi.io/security/audit, after the result, press **Let Pugi fix it** ("Sign up free. Pugi opens a project with these fixes already written into the brief."). pugi.io says a result is kept for about an hour, so press it soon.
2. The user signs in or signs up. A project opens with a brief listing the findings.
   - For a site on `*.pugi.app`, the fixes are made in that project.
   - For a site built elsewhere, bring its code into Pugi first with `pugi-deploy-repo`, then send the brief in that project.
3. Continue from step 3 above.

## Coming soon

More agent tools are coming. Use a Pugi tool only when it appears in your tool list or in https://pugi.io/llms.txt. Until then, use the steps above.
