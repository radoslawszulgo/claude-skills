---
name: mongodb-security-alerts
description: Turn a MongoDB security advisory from the MongoDB Alerts feed (https://www.mongodb.com/alerts/rss) into Percona-specific outputs — a Slack alert draft, a customer-facing Percona docs page, an OpenVEX statement, or a CVE/CPE JSON skeleton. Use when asked to triage a MongoDB CVE/security advisory for Percona's MongoDB-family products, draft a security Slack post, write customer security guidance, generate a VEX/OpenVEX statement, or produce CPE/CVE JSON for Percona Server, ClusterSync, Backup, or Search for MongoDB.
---

# MongoDB security alerts → Percona outputs

One input (a MongoDB security advisory), up to four possible outputs. Parse the advisory
deterministically, triage which Percona products it plausibly affects, confirm scope with the
user, then generate only the output(s) requested using the matching reference file.

## Step 1 — Get the advisory

The feed is https://www.mongodb.com/alerts/rss. Depending on what the user gave you:

- A URL or "check the feed" → fetch it (e.g. with WebFetch, or `curl` it to a file in the
  scratchpad) and pass it to the parser.
- Pasted advisory text / a CVE ID / a specific item → still run it through the parser if you have
  the raw XML; otherwise work directly from the pasted text using the same extraction fields
  (title, CVE ID(s), pubDate, summary, link).

Parse with the stdlib-only script — never hand-parse the XML yourself:

```bash
python3 scripts/parse_advisory.py --file <path-to-feed.xml>          # all items, newest first
python3 scripts/parse_advisory.py --file <path-to-feed.xml> --cve CVE-2025-XXXXX
python3 scripts/parse_advisory.py --url https://www.mongodb.com/alerts/rss --limit 5
```

**The feed itself is not in chronological order** — verified directly against the live feed;
items jump around by months or even years with no consistent ordering. Don't rely on feed order,
and don't hand-roll your own date sort either: the script always sorts by parsed `pubDate`
(newest first) before applying `--index`/`--limit`/`--cve`, so `--limit 5` reliably means "the 5
most recent advisories," not "the first 5 as the feed happened to list them." If the script warns
on stderr about an unparseable `pubDate`, that item is sorted last, not dropped — mention it to
the user rather than silently ignoring it.

Each item comes back as `{title, link, guid, pub_date, pub_date_iso, summary, cve_ids}`. Note
that on this feed, `link` is the **upstream MongoDB Jira ticket** for the CVE (e.g.
`jira.mongodb.org/browse/SERVER-XXXXX` or `CDRIVER-XXXXX`), occasionally a GitHub release page for
driver advisories — not a mongodb.com page. That's the ticket to check in Step 2 when affected
versions aren't stated.

If the user didn't name a specific advisory, show them the recent items (title + CVE + date, now
correctly ordered) and ask which one(s) to triage — don't pick for them.

## Step 2 — Triage: which Percona products does this affect?

Percona's MongoDB-family products depend on specific upstream components. Match the advisory's
affected component (from its title/summary — e.g. "mongod", "MongoDB Server", "MongoDB C
Driver", "MongoDB Go Driver", "MongoDB Java Driver", "mongosh") against this table:

| Percona product | Depends on | Bundled version | CPE |
|---|---|---|---|
| Percona Server for MongoDB | MongoDB Server itself (it's a downstream build of MongoDB Community Server) **and** the MongoDB C driver | C driver 1.28.1 | `cpe:2.3:a:percona:percona_server:*:*:*:*:*:mongodb:*:*` |
| Percona ClusterSync for MongoDB | MongoDB Go driver | Go driver 2.8.5 | `cpe:2.3:a:percona:percona_clustersync:-:*:*:*:*:mongodb:*:*` |
| Percona Backup for MongoDB | MongoDB Go driver | Go driver 2.6.0 | `cpe:2.3:a:percona:percona_backup:-:*:*:*:*:mongodb:*:*` |
| Percona Search for MongoDB | MongoDB Java driver (a Go driver dependency was also flagged previously, version unconfirmed) | Java driver 4.11.5 | `cpe:2.3:a:percona:percona_search:-:*:*:*:*:mongodb:*:*` |

Rules of thumb:

- Advisory affects MongoDB Server core (storage engine, replication, auth, wire protocol) →
  Percona Server for MongoDB is implicated.
- Advisory affects the **C driver** (libmongoc/libbson) → Percona Server for MongoDB only.
- Advisory affects the **Go driver** (mongo-go-driver) → Percona ClusterSync and Percona Backup
  for MongoDB; possibly Percona Search for MongoDB too (Go dependency unconfirmed — flag it, don't
  assert a version).
- Advisory affects the **Java driver** → Percona Search for MongoDB only.
- Advisory affects something none of these touch (Atlas-only, Compass, Realm, Node/Python/C#/PHP/
  Ruby/Rust drivers, BI Connector, Kafka Connector, VS Code extension, etc.) → no Percona
  MongoDB-family product is affected. Say so plainly rather than forcing a match.

**When triaging more than one advisory at once** (e.g. all recent feed items, or a batch of CVE
IDs), don't run every CVE through the full version-level check below — first filter out any
advisory whose affected component is clearly unrelated per the rule of thumb above (a driver
Percona doesn't bundle, BI Connector, Compass, Realm, Atlas-only, VS Code extension, etc.). Skip
those automatically without asking the user first — only continue triaging the ones that plausibly
touch a component from the table. But always report what was skipped, before presenting the
triage result, as one line per item:

`CVE-ID — title — affected component (skipped: not used by any Percona MongoDB-family product)`

This lets the user verify nothing relevant was dropped. If a component is ambiguous (e.g. it's
unclear whether "MongoDB Server" text refers to a subsystem that touches Percona Server, or a
driver name isn't stated clearly enough to confirm it's not Go/C/Java), don't skip it — treat it
as plausibly affected and carry it into the full triage instead.

**Once you know which product(s) are implicated by component, check the exact version.** If the
advisory states an affected driver-version range or MongoDB Server-version range, load
[references/version-mapping.md](references/version-mapping.md) to check whether the version
Percona actually bundles/is built from falls inside that range — component-level match alone can
over-flag a product that's already on a fixed version.

**If the advisory's own summary doesn't state affected versions** (this happens on a real, non-
trivial minority of items — roughly 1 in 20 — usually ones that just say "see the linked ticket"),
follow the item's `link` field and fetch that Jira ticket (e.g. with WebFetch) before falling back
to a manual placeholder. MongoDB's public Jira tickets commonly carry an "Affects Version/s" and
"Fix Version/s" field that the RSS description omits entirely. Only fall back to a
`<MANUAL: affected versions not stated in advisory or linked ticket>` placeholder if the ticket
itself is also silent, inaccessible (private/restricted ticket), or the `link` doesn't point to a
Jira ticket at all (e.g. a GitHub release page) — in the GitHub case, still fetch it, since release
notes usually state the fixed version even without a formal affected-range.

**If Percona Server for MongoDB is one of the implicated products, check whether Percona has
already published a real determination for this CVE** before relying on your own triage of it.
Load [references/existing-vex-data.md](references/existing-vex-data.md) and fetch the published
OpenVEX file for the specific release(s) in scope — when the CVE is already covered there, its
`status`/`justification`/`impact_statement` is Percona's own answer and should be reported as such
(and reused verbatim if the output is an OpenVEX statement), not re-derived from the advisory
text. This only exists for Percona Server for MongoDB — there's no equivalent for Backup, Search,
or ClusterSync, and it only covers a small rolling window of releases, so most triage will still
fall through to the steps above.

Present the triage result (which products, and why, including the version-level check and any
existing published VEX determination) to the user before generating any output — this is a
judgment call from advisory text, not a certainty, and it's the input every downstream format
depends on.

## Step 3 — Ask which output(s) to generate

Confirm with the user (they may want more than one):

1. **Slack draft** — quick-alert message for a channel.
2. **Percona docs page** — customer-facing advisory/guidance page.
3. **OpenVEX statement** — machine-readable vulnerability exploitability exchange JSON.
4. **CVE/CPE JSON skeleton** — structured record for internal tracking or another security tool.

## Step 4 — Generate

Load only the reference file(s) for the output(s) chosen — don't load all four:

- Slack → [references/slack-format.md](references/slack-format.md)
- Percona docs → [references/percona-docs-format.md](references/percona-docs-format.md)
- OpenVEX → [references/openvex-schema.md](references/openvex-schema.md)
- CVE/CPE JSON → [references/cve-cpe-format.md](references/cve-cpe-format.md)

Any output that needs a specific "affected version" or "fixed in" value (docs page, CVE/CPE JSON,
or an OpenVEX statement with status `fixed`/`not_affected`) should pull that value from
[references/version-mapping.md](references/version-mapping.md) rather than leaving it fully
manual, when the advisory's version range makes a lookup possible.

Each reference file has its own field-by-field format and rules. Shared rules across all of them:

- Never invent a CVSS score, fixed version, workaround, or affected version range that isn't in
  the source advisory or derivable from [references/version-mapping.md](references/version-mapping.md) —
  use the `<MANUAL: ...>` placeholders each format defines otherwise.
- Use the CPEs from the table in Step 2 verbatim — don't construct new ones.
- The **Slack draft is draft-only**: never post it via a Slack tool even if one is available in
  this session — hand it back as text for the user to post themselves.
- For Percona Server for MongoDB, always check
  [references/existing-vex-data.md](references/existing-vex-data.md) first — if Percona has
  already published a real statement for this CVE/release, use its `status`/`justification`/
  `impact_statement` instead of a placeholder, in every output format, not just OpenVEX.
- Absent an existing published statement, OpenVEX `justification` is a manual placeholder (see
  [references/openvex-schema.md](references/openvex-schema.md)) — never auto-select one of the
  five allowed values yourself.
