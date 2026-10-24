# Pugi on Smithery

Text and settings for the Smithery listing of the Pugi MCP server.

## Server

- URL: `https://api.pugi.io/api/agent/v1/mcp`
- Transport: Streamable HTTP, JSON responses
- Auth: `Authorization: Bearer pugi_agent_...` (no OAuth)
- Config schema: [`config-schema.json`](config-schema.json)

## Listing

Name: Pugi

Short description:

> Passive website security checks, credit balance, card top-up links and published app status.

Long description:

> Pugi is an AI product team that builds, checks and publishes websites and apps. This MCP server gives agents four tools today:
>
> - `scan_url`: a passive, read-only security check of a public website, graded A+ to F. Free, 10 a day per key. It reads only what a browser receives. It is not a pentest and does not prove a site is secure.
> - `get_balance`: credit balance, today's spend, the daily cap and the price list. Free.
> - `buy_credits_link`: a card checkout link a person opens to add credit. It never charges by itself. Free.
> - `publish_status`: status and address of the apps this account has published. Free.
>
> Create a key with `POST https://api.pugi.io/api/agent/v1/keys`. A new key comes with $0.50 of free credit. Each key has a rate limit and a daily spend cap.

Links:

- Website: https://pugi.io
- Docs for agents: https://pugi.io/agents.md
- LLM index: https://pugi.io/llms.txt
- Skills: https://github.com/pugi-io/skills
- Terms: https://pugi.io/terms
- Privacy: https://pugi.io/privacy
- Support: support@pugi.io
- Publisher: Pugi Inc.
- Icon: `assets/icon.png` (512x512)

Categories: Security, Developer tools.

## Steps

1. Sign in at https://smithery.ai with GitHub.
2. Open https://smithery.ai/new and choose to publish by URL.
3. Enter `https://api.pugi.io/api/agent/v1/mcp`.
4. When asked for configuration, paste the schema from `config-schema.json`. Users enter their key as `Bearer pugi_agent_...`; Smithery forwards it as the `Authorization` header.
5. If Smithery asks for a test key to scan the tools, create one key, use it for the scan, and revoke it after with `DELETE https://api.pugi.io/api/agent/v1/keys/self`.
6. Fill in the name, descriptions, links and icon from this file and publish.

The same publish from the Smithery CLI, after `smithery login`:

```bash
smithery mcp publish "https://api.pugi.io/api/agent/v1/mcp" -n @<smithery-namespace>/pugi \
  --config-schema "$(cat smithery/config-schema.json)"
```
