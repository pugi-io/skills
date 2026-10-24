---
name: pugi-logo
description: Make logos and a brand kit (SVG and PNG logo files, palette, fonts, brand guide) for a business with Pugi, then wire the kit into the user's site. Use when the user needs a logo, a brand kit, brand colours or a favicon for a business or project.
license: MIT (see LICENSE.txt)
compatibility: The logo maker is a web page; a person or a browser-capable agent fills it in, and downloading needs a free Pugi sign-in. Wiring the kit into a project needs file access.
metadata:
  author: Pugi Inc.
  version: "0.1.0"
  homepage: https://logo.pugi.io
---

# Make a logo and brand kit with Pugi

## What works today

| Step | Surface | Status (checked 2026-10-24) |
|---|---|---|
| Logo concepts and a brand kit | https://logo.pugi.io (web page) | Available in a browser. Downloading the kit needs a free Pugi sign-in |
| Website in the same brand | **Build my website with this brand**, see `pugi-brand-to-site` | Available on every plan; publishing on a pugi.app address is included on every plan |
| More agent tools | Not released yet | Coming soon |

## Steps

1. Ask the user for:
   - the business name, exactly as it should be lettered;
   - one line about the business and its trade (for example "family bakery in Lisbon, sourdough and pastries");
   - colours or styles to avoid, if any.
2. Send the user to https://logo.pugi.io with those two lines to type. If you can drive a browser, open the page and enter them yourself, then let the user choose.
3. Pugi writes a short brand brief and draws logo concepts from it. The user picks one, adjusts colours and type, signs in (free) and downloads the kit. The download button names what it includes on the user's plan, for example PNG files and the brand book, or SVG, PNG and the brand book. The kit also lists the palette and the fonts.
4. When the user gives you the kit, wire it into the project:
   - Put the files in the site's public folder, for example `public/brand/`.
   - Use the SVG in the header if the kit has one, otherwise the PNG. Keep a PNG for social previews (`og:image`) and email.
   - Make a favicon from the symbol, for example `public/favicon.svg` linked with `<link rel="icon" href="/favicon.svg" type="image/svg+xml">`, or a PNG.
   - Turn the palette into CSS variables (`--brand-primary`, `--brand-accent`, and so on) and use them instead of hard-coded colours.
   - Load the kit's fonts from the source the kit names.
5. Show the user the result in light and dark mode and at phone width before you commit.

## Coming soon

More agent tools are coming. Use a Pugi tool only when it appears in your tool list or in https://pugi.io/llms.txt. Until then, use the steps above.
