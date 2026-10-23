---
name: pugi-design
description: Use Pugi's Design mode to draw or change the design and clickable prototype of an app before or after it is built - point at an element and change its text, colours, font size, padding or margin, or describe the change in words; keep versions; apply the design to the app's source; save the prototype as a Pugi design file for a later Figma import (not a .fig file, and no public import plugin yet). Use when the user wants to see or change how their Pugi app looks or wants a prototype first.
license: MIT (see LICENSE.txt)
compatibility: Design mode is in the Pugi console at https://app.pugi.io (a person in a browser, or a browser-capable agent). Editing needs the Founder plan or higher.
metadata:
  author: Pugi Inc.
  version: "0.1.0"
  homepage: https://pugi.io/pricing
---

# Design an app in Pugi's Design mode

## What works today

| Step | Surface | Status (checked 2026-10-24) |
|---|---|---|
| Design tab, prototype, element editing, versions, Apply to app | Pugi console, https://app.pugi.io | Available, **Founder plan or higher** |
| View a design read-only | Pugi console | Available on every plan |
| Save the prototype as a Pugi design file (`.od-figma.json`) | **Download for Figma** on the Design tab and plan-approval screen | Available. Not a Figma file; see below |
| Import that file into Figma | — | Not available today |
| More agent tools | — | Coming soon |

There is no CLI command for Design mode. Guide the user through the console, or drive the browser if you can.

## Rules

- On the Free plan the Design tab is read-only and editing opens an upgrade offer ("Upgrade to Founder, $20/month"). Tell the user before they hit it. Upgrading is their decision.
- Anything that asks Pugi to do work can use the plan's allowance: a new design, **Send to agent**, **Apply changes**, **Send to chat**, **Critique**, "Brand from a website or a screenshot", **Apply to app**, and style changes from Preview. Get the user's yes before each one. Looking, switching widths and browsing versions are free.
- **Apply to app** changes the app's code. Get a clear yes before you press it.

## Get to Design mode

Use any of these:
- In a project, open the **Design** tab (next to Preview, Files and Security).
- In Preview, press the palette button **Open in Design**.
- Add `?pane=design` to the project's address.
- For a new project, turn on **Design first** on the message box before sending the first brief. The team plans, the designer draws the prototype, and nothing is built until the user approves it.

## Make a new design

1. Start a new project with **Design first** on, and send the brief (see `pugi-build` for how to write one).
2. Wait: "The designer is drawing your design" takes a few minutes. The tab refreshes on its own.
3. At the plan approval, the prototype shows as "Prototype of your app". The user clicks through it, then presses **Approve** or **Request changes**. Nothing is built before Approve.

## Change a design

1. On the Design tab, press **Edit**, then click any element.
2. Either:
   - type the change in words (for example "make this button larger and emerald green") and press **Send to agent**: the designer redraws that screen; or
   - press **Edit element** and change **Text**, **Text color**, **Background**, **Font size**, **Padding** or **Margin**, then **Apply changes**.
   Every change saves a new version ("Prototype updated to v3").
3. Elements shared by every screen, such as the header, cannot be edited this way. Use **Send to chat** with a note instead.
4. Other tools on the tab:
   - **Versions**: open or restore any version.
   - Desktop, Tablet and Phone widths.
   - **Design system**: colours, fonts, spacing and corners, or "Brand from a website or a screenshot".
   - **Critique**: asks for a review of the design in the chat (ask first; see Rules).

## Put the design into the app

- Design edits change the prototype only, not the app's code.
- When the newest version is not in the app yet, the tab shows "v4 not in your app yet" and an **Apply to app** button. With the user's yes, press it. The team is asked to implement that version in the code while keeping the app's data, logic and routes working. The view switches to Preview; check the result there with the user.
- In **Preview** (the built app), the same Edit tool sends a style change straight to the agent, which edits the source. A chat session must be open.

## Download for Figma (a Pugi design file)

On the Design tab or the plan-approval prototype, the button is **Download for Figma**. It saves `<project>-v<n>.od-figma.json`: a Pugi JSON capture of the prototype's layers, not a Figma file. Figma cannot open it without an import plugin, and that plugin is not published for users today. Tell the user plainly that the file is for a later import. Photos are not included, and complex styles are simplified.

## Coming soon

More agent tools are coming. Use a Pugi tool only when it appears in your tool list or in https://pugi.io/llms.txt. Until then, use the steps above.
