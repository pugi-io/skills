---
name: pugi-start-from-template
description: Start a new Pugi project from one of Pugi's 31 ready-made starters (landing pages, SaaS with sign-in and subscriptions, marketplaces, booking, online courses, events and tickets, menus with ordering, job boards, CRM, help desk, invoices, inventory, admin panels and more), or lay a starter down locally with the CLI. Use when the user wants to begin from a template, asks what kinds of apps Pugi can start from, or wants a known-good starter project.
license: MIT (see LICENSE.txt)
compatibility: The gallery is in the Pugi console at https://app.pugi.io (sign-in required). The local starters need Node.js 18+ and @pugi/cli 1.0.0-alpha.246 or later.
metadata:
  author: Pugi Inc.
  version: "0.1.0"
  homepage: https://pugi.io/ideas
---

# Start from a Pugi template

## What works today

| Step | Surface | Status (checked 2026-10-24) |
|---|---|---|
| Templates gallery, 31 starters, **Use this template** | https://app.pugi.io/templates (also Projects, then Templates, and New project, then Browse Templates) | Available, every plan, within the plan's project limit |
| Ideas built on starters, **Build one like this** | https://pugi.io/ideas | Available |
| Local starter: `pugi scaffold web`, `web-static`, `fullstack` | CLI `@pugi/cli` 1.0.0-alpha.246 or later | Available |
| Any gallery starter by id from the CLI | None today | Not in the published CLI (1.0.0-alpha.246) |
| More agent tools | Not released yet | Coming soon |

## The 31 starters in the gallery

| Tab | Starters |
|---|---|
| Landing Pages | Landing page / website · Product landing (centred) · Multi-page business site · Donations for a non-profit · Coming soon + waitlist · Link in bio · Mobile app landing page |
| SaaS Starters | SaaS with sign-in and subscriptions · Product with accounts (no payments) · App with user/admin roles and billing portal · Multi-tenant app with teams · Paid community · Job board |
| E-commerce | Online courses · Listings with a map · Marketplace · Booking and rental · Menu with online ordering · Events and tickets |
| Blog & Content | Magazine |
| Portfolio | Agency or studio site |
| Internal Tools | Admin panel over a database table · Kanban board · Records admin (CRUD) · Help desk · Online appointment booking · CRM with a deal pipeline · Status page · Invoices · Inventory · Forms and surveys |

Most starters come in two or three looks. For an idea that fits none of them, skip the template and write a brief (see `pugi-build`): Pugi builds from scratch.

## Rules

- Using a template starts a build, which uses the user's plan allowance. Get a yes first.
- A new project counts toward the plan's project limit (Free has 3). If the limit is reached, the console says so and offers **See plans**. Upgrading is the user's decision.
- Nothing goes live until the user approves it (see `pugi-sdlc` and `pugi-publish`).

## Steps in the console

1. Help the user pick a starter from the table above.
2. The user opens https://app.pugi.io/templates and signs in.
3. They open the card, choose a look, and press **Use this template**.
4. Pugi creates a new project with a brief built from the starter and the look, and starts the first build. If no model is chosen yet, the console asks the user to choose one and press Send.
5. Continue with `pugi-sdlc` to follow the run.

## Steps with the CLI (a local starter you build on yourself)

Always scaffold into a new, empty folder:

```bash
npm i -g @pugi/cli@latest && pugi --version     # 1.0.0-alpha.246 or later
pugi scaffold web my-app          # Vite + React + TypeScript + Tailwind + shadcn/ui
pugi scaffold web-static my-site  # browser-only, no server
pugi scaffold fullstack my-app    # API and single-page app in one repo, one port
```

In a folder that already has files, the command writes only the files that are missing and lists every file it skipped. It never overwrites without `--force`.

`--force` overwrites existing files, and the user's work in them is lost. Use it only when the user asks: run the command once without `--force`, show the user the list of skipped files that would be replaced, and get a clear yes for that list. Suggest committing or backing up first.

To put the result online, use `pugi-publish`.

## Coming soon

More agent tools are coming. Use a Pugi tool only when it appears in your tool list or in https://pugi.io/llms.txt. Until then, use the steps above.
