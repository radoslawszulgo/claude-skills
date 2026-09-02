# Version mapping (driver versions + Percona Server ↔ MongoDB Server)

Load this file whenever an advisory states an affected *version range* (driver or MongoDB
Server) and you need to determine whether Percona's currently-bundled version actually falls
inside it, or which Percona Server for MongoDB release corresponds to a given upstream MongoDB
Server version. Step 2 in [SKILL.md](../SKILL.md) tells you *which product* a component maps to;
this file tells you *whether the specific version Percona ships* is in scope.

## Bundled driver versions (current)

These are the exact upstream driver versions each Percona product currently bundles. Compare
these — not just the driver name — against the advisory's stated affected range.

| Percona product | Driver | Version |
|---|---|---|
| Percona Server for MongoDB | MongoDB C driver | 1.28.1 |
| Percona ClusterSync for MongoDB | MongoDB Go driver | 2.8.5 |
| Percona Backup for MongoDB | MongoDB Go driver | 2.6.0 |
| Percona Search for MongoDB | MongoDB Java driver | 4.11.5 |

If an advisory says, e.g., "MongoDB C driver versions prior to 1.28.0 are affected," Percona
Server for MongoDB (bundling 1.28.1) is **not affected by version** — but still flag it in the
triage output rather than silently dropping it, since bundled versions change over time and this
table needs to be kept current by the user.

**Percona Search for MongoDB's driver dependency:** only a Java driver version is confirmed here
(4.11.5). An earlier triage pass also noted a Go driver dependency for Search, but no version for
it has been confirmed — treat any Go-driver advisory against Search as "possibly affected,
version unconfirmed" rather than asserting a specific version is or isn't in range.

## Latest releases (current)

The current latest release of each Percona MongoDB-family product line. Use this to answer
"is a customer already safe on the latest version" and to fill in a docs/Slack/CVE `Fixed in` or
`Planned Fixed` field when the fix has already shipped — point at the latest release of the
affected line rather than leaving it `<MANUAL: ...>` if the advisory's fix version is at or before
it.

| Product / line | Latest release |
|---|---|
| Percona Server for MongoDB 8.3 | 8.3.8-2 |
| Percona Server for MongoDB 8.0 | 8.0.29-13 |
| Percona Server for MongoDB 7.0 | 7.0.40-22 |
| Percona Backup for MongoDB | 2.15.0 |
| Percona Search for MongoDB | 1.70.4-2 |
| Percona ClusterSync for MongoDB | 0.9.0 |

The three Percona Server lines here match the newest row of their respective line in the
version-mapping table below — that's expected, not a coincidence, since both come from the same
release history. If they ever disagree, trust whichever was updated more recently and flag the
mismatch to the user rather than picking one silently.

For Percona Server for MongoDB, "latest" is per **line** (8.3 / 8.0 / 7.0), not a single global
latest — a customer on the 7.0 line who's current (7.0.40-22) is not "behind" just because 8.3
exists; only compare within the same line unless the user is asking about a major-version upgrade.

Percona Backup, Percona Search, and Percona ClusterSync for MongoDB don't have this
line-versioning — a single latest release each.

## Percona Server for MongoDB → MongoDB Server version mapping

Use this when an advisory's affected range is stated in terms of MongoDB *Server* versions (not
a driver) and you need the corresponding Percona Server for MongoDB release(s) — e.g. to fill in
"Affected versions" in the docs/CVE output, or to decide `fixed` vs `affected` in an OpenVEX
statement. Match on the "based on" MongoDB version(s), then use the paired Percona release +
release date as the affected/fixed Percona version.

| Percona Server for MongoDB | Release date | Based on MongoDB Server version(s) |
|---|---|---|
| 8.3.8-2 | 2026-08-24 | 8.3.8 |
| 8.3.7-1 | 2026-07-30 | 8.3.7 |
| 8.0.29-13 | 2026-08-20 | 8.0.29 |
| 8.0.28-12 | 2026-08-10 | 8.0.28, 8.0.27 |
| 8.0.26-11 | 2026-06-25 | 8.0.26, 8.0.25, 8.0.24 |
| 8.0.23-10 | 2026-05-21 | 8.0.23, 8.0.22 |
| 8.0.21-9 | 2026-05-06 | 8.0.21 |
| 8.0.20-8 | 2026-04-01 | 8.0.20 |
| 8.0.19-7 | 2026-02-19 | 8.0.19, 8.0.18 |
| 8.0.17-6 | 2026-01-06 | 8.0.17 |
| 8.0.16-5 | 2025-12-02 | 8.0.16, 8.0.15, 8.0.14, 8.0.13 |
| 8.0.12-4 | 2025-08-21 | 8.0.12, 8.0.11, 8.0.10, 8.0.9 |
| 8.0.8-3 | 2025-05-01 | 8.0.8, 8.0.7, 8.0.6, 8.0.5 |
| 8.0.4-2 | 2025-02-19 | 8.0.4 |
| 8.0.4-1 | 2024-12-17 | 8.0.4, 8.0.3, 8.0.2, 8.0.1, 8.0.0 |
| 7.0.40-22 | 2026-08-19 | 7.0.40 |
| 7.0.39-21 | 2026-08-05 | 7.0.39, 7.0.38 |
| 7.0.37-20 | 2026-06-23 | 7.0.37, 7.0.36, 7.0.35 |
| 7.0.34-19 | 2026-05-20 | 7.0.34, 7.0.33 |
| 7.0.32-18 | 2026-05-07 | 7.0.32 |
| 7.0.31-17 | 2026-03-30 | 7.0.31 |
| 7.0.30-16 | 2026-02-18 | 7.0.30, 7.0.29 |
| 7.0.28-15 | 2026-01-06 | 7.0.28, 7.0.27 |
| 7.0.26-14 | 2025-11-25 | 7.0.26, 7.0.25 |
| 7.0.24-13 | 2025-09-11 | 7.0.24, 7.0.23 |
| 7.0.22-12 | 2025-07-28 | 7.0.22, 7.0.21, 7.0.20, 7.0.19 |
| 7.0.18-11 | 2025-04-24 | 7.0.18, 7.0.17 |
| 7.0.16-10 | 2025-02-19 | 7.0.16 |
| 7.0.15-9 | 2024-11-27 | 7.0.15 |
| 7.0.14-8 | 2024-09-23 | 7.0.14, 7.0.13 |
| 7.0.12-7 | 2024-07-23 | 7.0.12 |
| 7.0.11-6 | 2024-06-03 | 7.0.11, 7.0.10, 7.0.9 |
| 7.0.8-5 | 2024-04-24 | 7.0.8 |
| 7.0.7-4 | 2024-04-04 | 7.0.7, 7.0.6 |
| 7.0.5-3 | 2024-01-23 | 7.0.5 |
| 7.0.4-2 | 2023-12-11 | 7.0.4, 7.0.3 |
| 7.0.2-1 | 2023-10-05 | 7.0.2, 7.0.1, 7.0.0 |

## How to use this table

- **Advisory names one MongoDB Server version** (e.g. "fixed in 8.0.21") → find the row(s) whose
  "based on" column contains it, or the nearest *later* version if the exact patch isn't listed —
  the fix likely landed in the first Percona release built on that version or later.
- **Advisory names a version range** (e.g. "affects 7.0.0 through 7.0.14") → every Percona row
  whose "based on" list intersects that range is affected; the earliest such row is where the
  vulnerability was introduced from Percona's side, the latest is where the fix should land.
- **A version genuinely isn't in this table** (e.g. it predates 7.0.2-1, or postdates 8.3.8-2) →
  say so explicitly and use a `<MANUAL: not covered by the current version-mapping table>`
  placeholder rather than extrapolating a release that doesn't exist yet.
- This table is a point-in-time snapshot the user provided — if it looks stale (missing a release
  you'd expect given the advisory's date), ask the user to refresh it rather than guessing newer
  rows.
