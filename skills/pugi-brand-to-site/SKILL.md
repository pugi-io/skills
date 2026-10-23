---
name: pugi-brand-to-site
description: Turn a brand made on logo.pugi.io (logo, palette, fonts and brand brief) into a new website in the same brand on Pugi, in one handoff - the site uses the user's own logo files and colours instead of drawing new ones. Use when the user has a Pugi logo or brand kit and wants a website for it, or asks to build a site in their brand.
license: MIT (see LICENSE.txt)
compatibility: A person or a browser-capable agent in the browser; needs a Pugi account (free sign-up). Building uses the plan allowance; publishing on a pugi.app address is included on every plan.
metadata:
  author: Pugi Inc.
  version: "0.1.0"
  homepage: https://logo.pugi.io
---

# Build a website in a logo.pugi.io brand

## What works today

| Step | Surface | Status (checked 2026-10-24) |
|---|---|---|
| Make the brand | https://logo.pugi.io (see `pugi-logo`) | Available, free |
| **Build my website with this brand**: handoff to a new project | logo.pugi.io, then https://app.pugi.io | Available, sign-in required |
| Edit the website brief, then **Build my website** | Console brief card | Available, every plan, within the plan's project limit |
| Put the brand on an existing site | Console: "The logo on the site isn't yours?", then **Put my brand in** | Available |
| More agent tools | — | Coming soon |

## Rules

- Building the site uses the user's plan allowance. Show the brief and get a clear yes before **Build my website**.
- **Fill with AI** and **Put my brand in** also ask Pugi to do work, which can use allowance. Ask before pressing either.
- Pressing **Build my website with this brand** on logo.pugi.io sends the brand (name, trade, palette, fonts, logo files) to the user's Pugi account and creates a project. Tell the user and get a yes before pressing it.
- A new project counts toward the plan's project limit (Free has 3).
- Publishing the site on a pugi.app address is included on every plan (https://pugi.io/pricing). Going live is the user's decision (see `pugi-sdlc` and `pugi-publish`).

## Steps

1. Make or open the brand on https://logo.pugi.io (see `pugi-logo`).
2. With the user's yes (see Rules), press **Build my website with this brand** on the brand kit page. It opens app.pugi.io with the brief filled in. New visitors sign up there; the brand carries through sign-in.
3. Pugi creates a project named after the business, with the brand attached, and shows a card "Website brief for <name>" with the logo, the colour swatches and the fonts.
4. Go through the brief with the user and change anything they want:
   - Business name, what it is or sells, sections, tone, main and second button, tagline, look, site language, opening hours.
   - "How should customers reach you?": booking form, contact form, call or WhatsApp, or an email link.
   - "How many pages?": one page with sections, or separate pages.
   **Fill with AI** drafts the empty fields (ask first; see Rules). **Edit as text** shows the whole brief.
5. With the user's yes, press **Build my website**. The build starts only then. Pugi is told to use the brand's own logo files, favicon, palette and fonts, and not to draw a new logo.
6. Follow the run with `pugi-sdlc`. If the finished site shows a different logo, the console offers "The logo on the site isn't yours?". With the user's yes, press **Put my brand in**.

## If something fails

- "This brand link has expired": the console says brand links from logo.pugi.io last 7 days and open for one account. Open the brand on logo.pugi.io again and press the button again.
- "Choose a model, then press Build my website again": the user picks a model in the console and presses the button again.

## Coming soon

More agent tools are coming. Use a Pugi tool only when it appears in your tool list or in https://pugi.io/llms.txt. Until then, use the steps above.
