# Existing OpenVEX data (Percona Server for MongoDB)

Percona already publishes hand-reviewed OpenVEX statements for Percona Server for MongoDB.
**Check these before generating anything from scratch** — reusing a real, human-authored
determination is always better than this skill guessing at one, and it's the whole reason
`justification`/`impact_statement` are placeholders elsewhere in this skill: a real answer exists
for a lot of CVE/version combinations already.

- Source repo: https://github.com/percona/percona-server-mongodb/tree/master/vex
- Published, fetchable copies (no auth needed):
  `https://percona.github.io/percona-server-mongodb/vex/percona-server-mongodb-<version>.vex.json`
  — e.g. version `8.3.7-1` → `https://percona.github.io/percona-server-mongodb/vex/percona-server-mongodb-8.3.7-1.vex.json`

## Coverage — what to expect

- **Percona Server for MongoDB only.** No equivalent exists for Percona Backup, Percona Search, or
  Percona ClusterSync for MongoDB — don't construct an analogous URL for those, there's nothing
  there to fetch.
- **Not every release has a file.** As verified directly, only a small rolling window is published
  — currently the current and previous release of each Server line (7.0 / 8.0 / 8.3), e.g.
  `8.3.8-2` and `8.3.7-1` exist but older 8.3.x releases don't. A missing file returns HTTP 404 —
  treat that as "no existing data for this version," not as an error to retry or work around.
- **Each file covers many CVEs across several vendored components, not just Server itself.**
  A sample file's `products[]` included `pkg:github/mongodb/mongo@<version>` (Server itself) and
  `pkg:github/mongodb/mongo-c-driver@<version>` (the bundled C driver — see the driver table in
  [version-mapping.md](version-mapping.md)), plus several vendored third-party libraries built
  into that release (ICU, libtomcrypt, gRPC, PCRE2, libdwarf, in the sample checked — the exact
  set can change release to release, don't assume it's fixed). So this is also the right place to
  check C-driver CVEs, not only Server-core ones.
- **Products are identified by Package URL (purl), not CPE** — e.g.
  `pkg:github/mongodb/mongo-c-driver@1.28.1`, not the CPE from
  [cve-cpe-format.md](cve-cpe-format.md). Keep the purl form when reusing an existing statement
  verbatim; only reach for the CPE table when writing a brand-new statement that has no existing
  counterpart to draw from.
- Statements carry real `justification` and `impact_statement` text written by Percona's security
  team — specific, technical, version-accurate (e.g. "Mongo C Driver comprises two libraries:
  `libbson` and `libmongoc`. The vulnerability is in `libmongoc`, but Percona Server for MongoDB
  includes only `libbson`."). Never overwrite one of these with a generic placeholder, and never
  paraphrase it into something vaguer.

## How to use this

Applies both during triage ([SKILL.md](../SKILL.md) Step 2) and when generating an OpenVEX
statement ([openvex-schema.md](openvex-schema.md)), for any CVE that plausibly affects Percona
Server for MongoDB:

1. Once Step 2 has narrowed the affected version(s) down to specific Percona Server for MongoDB
   releases (via [version-mapping.md](version-mapping.md)), fetch the corresponding VEX file(s)
   for those releases (e.g. with WebFetch).
2. If the file exists, search its `statements[]` for a `vulnerability.name` matching the CVE.
   - **Found** → use its `status`, `justification`, and `impact_statement` directly and report it
     to the user as Percona's own published determination, not as something this skill inferred.
     Don't generate a competing `under_investigation` statement for that release.
   - **File exists but this CVE isn't in it** → Percona hasn't triaged this CVE for that release
     yet. That's genuinely `under_investigation` — the absence is not evidence of `not_affected`.
3. **No file exists for that release at all** (404, or it falls outside the currently-published
   two-per-line window) → there's nothing to check. Fall back to Step 2's normal advisory-text
   triage and generate the statement per openvex-schema.md's standard `<MANUAL: ...>` rules.
4. If the user asks for a fresh OpenVEX statement for a release that already has a published file,
   and what you'd derive independently would ever disagree with the published verdict, don't
   silently pick one — surface the conflict to the user and let them resolve it.
