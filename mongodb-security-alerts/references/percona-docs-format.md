# Percona docs (customer guidance) output format

Load this file only when the requested output is a customer-facing security advisory page.

## Before drafting

If the `percona-dk` MCP connector is available in this session, use `search_percona_docs` (and
`get_percona_doc`) to pull 1-2 of Percona's own recent security advisory pages first, and match
their tone and section order rather than the generic structure below. Prefer the real house style
over this template whenever the two disagree. If the connector isn't available or returns
nothing usable, fall back to the structure below — it's a reasonable generic shape for a
vendor security advisory, not a verified Percona template.

## Structure

```markdown
# <Product> — <CVE-ID(s)> Security Advisory

**Date:** <publication date>
**CVE:** <CVE-ID(s), linked to nvd.nist.gov or the MITRE record>
**Severity:** <CVSS score/vector if the advisory states one, else "Not rated">

## Affected products and versions

| Product | Affected versions | CPE |
|---|---|---|
| <Percona product> | <version range — from SKILL.md Step 2's version check / version-mapping.md, or the linked Jira ticket if the advisory itself doesn't state one; only `<MANUAL: ...>` if neither source resolves it> | <CPE from cve-cpe-format.md> |

## Description

<Plain-language explanation of the vulnerability, written for a customer/operator audience —
not a copy of MongoDB's advisory text. Explain what the flaw is and how it could be triggered,
without security-researcher jargon.>

## Impact

<What happens if exploited, scoped to how the affected Percona product actually uses the
vulnerable component — e.g. "affects the bundled MongoDB C driver used internally by
mongod" vs. "affects only the MongoDB Server code Percona Server for MongoDB is built from.">

## Fixed in

<MANUAL: Percona release/version that includes the fix, or "A fix is being evaluated;
this page will be updated once a release date is confirmed.">

## Workaround

<MANUAL: mitigation customers can apply before upgrading, if one exists — otherwise state
"No workaround is available; upgrading is the only mitigation.">

## References

- <the parsed item's `link` field — the upstream MongoDB Jira ticket on this feed>
- <link to the CVE record>
```

## Tone rules

- Write for a customer/operator, not a security researcher — define acronyms on first use.
- State facts only; never claim a fix version, CVSS score, or workaround that isn't confirmed.
  Everything not in the source advisory is a `<MANUAL: ...>` placeholder, not a guess.
- Keep the "Description" and "Impact" sections scoped to the *Percona* product's exposure, not a
  restatement of MongoDB's own advisory — that's the whole point of this doc existing separately
  from the Slack draft.
