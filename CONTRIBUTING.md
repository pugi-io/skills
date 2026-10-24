# Contributing

Thanks for helping improve the Pugi skills.

## Issues

- **Bugs.** Use the bug report form. Say which skill and which agent, and include the output with secrets removed.
- **Skill requests.** Use the skill request form and describe the task as you would ask your agent.
- **Vulnerabilities.** Email security@pugi.io. See [SECURITY.md](SECURITY.md).

## Pull requests

1. Keep each skill in its own folder under `skills/`, with a `SKILL.md` whose `name` matches the folder.
2. Describe only what works today. Every step goes in the skill's status table as **Available**, **Not available today** or **Coming soon**.
3. Any step that builds, spends allowance, publishes, overwrites files or changes DNS asks for the user's yes first.
4. Never put keys, tokens or other credentials in a skill, a script or an example.
5. Run the release check and make sure it passes:

   ```bash
   bash scripts/check.sh
   ```

   It needs `uvx` and `gitleaks` installed.

6. Add a line to [CHANGELOG.md](CHANGELOG.md) for any change people will notice.

By contributing, you agree that your contribution is licensed under the [MIT License](LICENSE).
