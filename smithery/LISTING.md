# Pugi on Smithery

Текст и настройки для публикации Pugi MCP в Smithery. Это локальный черновик, не подтверждение опубликованной карточки.

Сверка кода 28.10.2026: `pugi` @ `a5b05f6e2`, модуль `apps/admin-api/src/agent-api/`. Публичные pricing и `tools/list` вернули 403; доступность на проде и актуальные цены нужно подтвердить перед публикацией.

## Server

- URL: `https://api.pugi.io/api/agent/v1/mcp`
- Transport: Streamable HTTP, JSON responses
- Для этой конфигурации: `Authorization: Bearer pugi_agent_...`. Сервер также реализует OAuth; эта схема описывает только ввод агентского ключа.
- Config schema: [`config-schema.json`](config-schema.json)

## Listing

Name: Pugi

Short description:

> Passive website security checks, credit balance, card top-up links and published app status.

Long description:

> Pugi проверяет сайты и публичные репозитории, создаёт логотипы и ищет стартеры. В базовой таблице кода включены `scan_url`, `make_logo`, `scan_repo`, `get_balance`, `buy_credits_link`, `publish_status`, `catalog_search`. Фактический набор зависит от клиента, scopes и конфигурации сервера; цены и лимиты сверяются через `/api/agent/v1/pricing`. Сборка, редактирование и публикация дополнительно требуют включённого `PUGI_AGENT_BUILDS` и готового runtime.
>
> `buy_credits_link` возвращает ссылку на оплату, которую открывает человек. Создание ключа и платные вызовы требуют разрешения пользователя.

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

Публикация, создание и отзыв тестового ключа меняют внешние ресурсы и выполняются только по явному разрешению владельца.

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
