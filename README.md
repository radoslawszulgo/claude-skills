# claude-skills

A collection of [Claude Code skills](https://docs.claude.com/en/docs/claude-code/skills).

## Skills

| Skill | Description |
|---|---|
| [mongodb-security-alerts](mongodb-security-alerts/SKILL.md) | Turns a MongoDB security advisory from the [MongoDB Alerts feed](https://www.mongodb.com/alerts/rss) into Percona-specific outputs: a Slack alert draft, a customer-facing Percona docs page, an OpenVEX statement, or a CVE/CPE JSON skeleton. |

## Usage

Each skill lives in its own directory with a `SKILL.md` that Claude Code loads automatically once
the skill is installed. To use a skill from this repo, copy its directory into your project's
`.claude/skills/` folder (or your user-level `~/.claude/skills/`):

```bash
cp -r mongodb-security-alerts /path/to/project/.claude/skills/
```

See each skill's `SKILL.md` for what it does and when Claude will invoke it.

## Sample usage

Once `mongodb-security-alerts` is installed, just ask Claude for what you want in plain language
— no slash command needed, the skill's description is enough for Claude to pick it up:

- *"Check last 7 days CVEs for MongoDB and create a draft Slack message."*
- *"Is Percona Server for MongoDB affected by CVE-2026-4359? Give me an OpenVEX statement."*
- *"Triage the latest MongoDB security advisory for Percona Backup and Percona Search, and write
  a customer-facing docs page."*
- *"Pull the newest item from the MongoDB alerts feed and give me both a Slack draft and a
  CVE/CPE JSON skeleton."*

Claude will parse the feed, tell you which Percona products it thinks are affected (and why)
before generating anything, and ask which output format(s) you want if you didn't already say.

## Verifying a skill is installed correctly

Skills are indexed when a Claude Code session starts, so a check only works in a **new** session
started after the copy — not one already running.

1. **Check the file landed in the right place.** Project-level skills are picked up from
   `.claude/skills/<skill-name>/SKILL.md` in the project root; user-level skills from
   `~/.claude/skills/<skill-name>/SKILL.md`.

   ```bash
   ls .claude/skills/mongodb-security-alerts/SKILL.md
   ```

2. **Check the frontmatter is well-formed.** Claude only discovers a skill if `SKILL.md` starts
   with a `---`-delimited YAML block containing at least `name` and `description`:

   ```bash
   head -5 .claude/skills/mongodb-security-alerts/SKILL.md
   ```

3. **Start a fresh Claude Code session** in that project (or with that user-level config) and ask
   Claude directly, e.g. *"What skills do you have available?"* or *"Do you have the
   mongodb-security-alerts skill?"* — an installed skill's name and description are loaded into
   the session up front, so Claude can confirm it without searching the filesystem.

4. **Trigger it for real.** Ask something that matches the skill's description — e.g. *"Check the
   MongoDB alerts feed for anything relevant to Percona Server for MongoDB"* — and confirm Claude
   follows the skill's workflow (parsing the feed, triaging affected products, asking which output
   you want) instead of improvising an ad hoc answer.

If step 3 or 4 doesn't show the skill, re-check step 1/2 first — a missing `name`/`description`
field or a wrong directory is the most common cause.

## License

[Apache License 2.0](LICENSE)
