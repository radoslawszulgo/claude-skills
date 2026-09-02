# Slack output format

Load this file only when the requested output is a Slack draft.

**This skill only drafts the message. Never call a Slack MCP tool to post it** — hand the draft
back as text (in a code block so it's easy to copy) and let the user post it themselves.

One draft can cover a single CVE or a batch of them (e.g. everything new on the feed this week) —
the header and summary describe the batch, and the "Detailed information" section repeats once
per CVE.

## Plain mrkdwn draft (default — use this unless the user asks for Block Kit)

```
:warning: *Security Advisory: Percona for MongoDB*
*Date:* <today's date>

<2-3 sentence overall summary in plain language, covering everything in this batch — not a
copy-paste of the advisory body>

*Affected software:*
• <Percona product> <affected version(s)> — <why: server-level / C driver / Go driver / Java driver>
  (repeat per affected product+version from the triage step and version-mapping.md; if nothing
  is affected, say so explicitly and stop here — skip the detailed section)

*Detailed information:*

<severity emoji> *<CVE-ID>* — <CVE title>
<optional 1-2 sentence CVE description, plain language>
*CVSS Score:* <score from advisory, or "not stated in advisory">
*Affects:* <Percona product and version>
*Planned Fixed:* <MANUAL: fix timeline — the user provides this, never infer it>

*Details:* <the parsed item's `link` field — on this feed that's the upstream MongoDB Jira ticket,
e.g. jira.mongodb.org/browse/SERVER-XXXXX (occasionally a GitHub release page for driver
advisories) — use it verbatim, don't construct a URL yourself>
*Percona ticket that solves it:* <MANUAL: optional — only include if the user supplies a
jira.percona.com link; omit the line entirely rather than leaving a placeholder if they don't>

(repeat the block above once per CVE in this batch)
```

### Severity emoji

Pick from the CVE's CVSS base score, using the official CVSS qualitative severity ratings — don't
invent a severity if the advisory doesn't carry a score. Use the Slack shortcode form (not the
raw unicode glyph) so it renders as the workspace's emoji:

| Score range | Severity | Emoji |
|---|---|---|
| 9.0 – 10.0 | Critical | `:red_circle:` |
| 7.0 – 8.9 | High | `:large_orange_circle:` |
| 4.0 – 6.9 | Medium | `:large_yellow_circle:` |
| 0.1 – 3.9 | Low | `:large_blue_circle:` |
| 0.0 | None | `:white_circle:` |
| not stated | Unknown | `:white_circle:` |

### Rules

- *Planned Fixed* is always a manual placeholder — Percona's release timeline isn't in the
  MongoDB advisory and the skill must never guess one.
- *Details* is just the parsed item's `link` field (MongoDB's own public Jira, `jira.mongodb.org`,
  or occasionally a GitHub release page) — copy it verbatim, never construct one from a
  ticket-key guess. If it's ever genuinely missing from the parsed item, say "not linked in
  advisory" rather than leaving the field blank.
- *Percona ticket that solves it* links to Percona's internal Jira (`jira.percona.com`) — this is
  optional and only appears when the user hands you the link directly; don't ask the user to go
  find it as a blocking step, just omit the line.
- Keep the summary and per-CVE description short and skimmable — this is a first-alert channel
  message, not the full customer doc ([references/percona-docs-format.md](percona-docs-format.md)
  is for that).

## Block Kit variant (only if the user asks for it)

```json
{
  "blocks": [
    {
      "type": "header",
      "text": {"type": "plain_text", "text": "⚠️ Security Advisory: Percona for MongoDB"}
    },
    {
      "type": "context",
      "elements": [{"type": "mrkdwn", "text": "Date: <today's date>"}]
    },
    {
      "type": "section",
      "text": {"type": "mrkdwn", "text": "<2-3 sentence overall summary>"}
    },
    {
      "type": "section",
      "text": {"type": "mrkdwn", "text": "*Affected software:*\n• <Percona product> <version> — <reason>"}
    },
    {"type": "divider"},
    {
      "type": "section",
      "text": {"type": "mrkdwn", "text": "<severity emoji> *<CVE-ID>* — <CVE title>\n<optional description>"}
    },
    {
      "type": "section",
      "fields": [
        {"type": "mrkdwn", "text": "*CVSS Score:*\n<score>"},
        {"type": "mrkdwn", "text": "*Affects:*\n<product and version>"},
        {"type": "mrkdwn", "text": "*Planned Fixed:*\n<MANUAL>"},
        {"type": "mrkdwn", "text": "*Details:*\n<the item's `link` field verbatim>"}
      ]
    }
  ]
}
```

Repeat the divider + two sections above once per CVE. Add a `*Percona ticket that solves it:*`
field only when the user supplies one.
