# Security policy

## Report a vulnerability

Email **security@pugi.io**. Please include:

- what you found and where (file, skill, or Pugi page);
- steps to reproduce;
- what an attacker could do with it.

Do not open a public issue for a vulnerability. We acknowledge reports within 72 hours, as https://pugi.io/security says, and tell you when a fix ships.

## Scope

- This repository: the skills, their scripts and the plugin manifests.
- The Pugi surfaces the skills call: the `pugi` CLI (`@pugi/cli`), pugi.io, app.pugi.io, logo.pugi.io, and `*.pugi.app` apps you own.

Out of scope: apps on `*.pugi.app` that belong to other people, denial of service, and social engineering.

This list says what you can report. It is not permission to test. Testing Pugi's own systems (pugi.io, app.pugi.io, logo.pugi.io and the services behind them) needs our written consent first: ask at security@pugi.io before you start. You may test code in this repository on your own machine, and apps you own.

## What this repository never contains

No API keys, tokens or credentials, and no server code. The skills call only Pugi's public surfaces. `scripts/check.sh` scans every file for key formats before every release and reports matches without printing them.

## If a skill finds a leaked key in your project

The `pugi-security-check` skill reports only the file and the type of key, never the value. Revoke the key at its provider first, then remove it from your code.
