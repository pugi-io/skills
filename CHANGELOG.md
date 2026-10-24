# Changelog

## Unreleased

- `server.json`: the Pugi MCP server (`io.pugi/pugi`, remote Streamable HTTP at `https://api.pugi.io/api/agent/v1/mcp`) in the official MCP Registry, version 0.1.0.
- `smithery/`: listing text and config schema for the Smithery listing.
- README: MCP server section.

## 0.1.0 (2026-10-24)

- First version, 11 skills: `pugi-build`, `pugi-sdlc`, `pugi-artifacts`, `pugi-design`, `pugi-start-from-template`, `pugi-logo`, `pugi-brand-to-site`, `pugi-security-check`, `pugi-fix-security`, `pugi-deploy-repo`, `pugi-publish`.
- Claude Code plugin and marketplace; Agent Plugins root manifest with Codex settings, Codex fallback manifest and marketplace; Cursor plugin.
- `pugi-publish` and `pugi-security-check` describe the live Pugi MCP server (`scan_url`, `publish_status`, `get_balance`, `buy_credits_link`).
- `pugi-security-check/scripts/precheck.py`: passive URL check (same-site redirects only, public addresses only, bounded reads, incomplete scans reported as incomplete) and folder secrets check (committed, not ignored, or local).
- `pugi-publish/scripts/check-domain.sh`: checks that a custom domain points at a Pugi app.
- Tested against `@pugi/cli` 1.0.0-alpha.246. Every step that builds, spends allowance, publishes, overwrites files or changes DNS asks for the user's yes first.
