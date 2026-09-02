# OpenVEX output format

Load this file only when the requested output is an OpenVEX statement.

## Check for an existing statement first

Before writing anything from the template below, check whether Percona has already published a
real OpenVEX statement for this exact CVE and Percona Server for MongoDB release — see
[existing-vex-data.md](existing-vex-data.md). If one exists, reuse its `status`, `justification`,
and `impact_statement` verbatim instead of generating a fresh statement with placeholders; this
only applies to Percona Server for MongoDB (no equivalent data exists for Backup, Search, or
ClusterSync). The template and placeholder rules below are for the case where no existing
statement covers this CVE/release — which is still the common case for Backup, Search,
ClusterSync, and for CVEs/releases outside the small published window.

## Shape

```json
{
  "@context": "https://openvex.dev/ns/v0.2.0",
  "@id": "https://percona.com/vex/<CVE-ID>-<product-slug>",
  "author": "Percona Security Team",
  "role": "Vendor",
  "timestamp": "<ISO-8601 generation timestamp>",
  "version": 1,
  "statements": [
    {
      "vulnerability": {
        "name": "<CVE-ID>",
        "description": "<one-line summary from the advisory>"
      },
      "products": [
        {
          "@id": "<CPE from cve-cpe-format.md for the affected Percona product>",
          "identifiers": {
            "cpe23": "<same CPE string>"
          }
        }
      ],
      "status": "<affected | not_affected | fixed | under_investigation>",
      "justification": "<MANUAL: required only when status = not_affected — pick one of the 5 values below>",
      "impact_statement": "<MANUAL: fill in>",
      "action_statement": "<MANUAL: fill in, e.g. upgrade path or 'no action required'>",
      "timestamp": "<ISO-8601, same as top-level unless the statement was revised later>"
    }
  ]
}
```

## Rules

- One `statements[]` entry per affected Percona product (multiple CPEs = multiple statements, not multiple CPEs in one `products[]` array, unless status/justification are identical across products).
- `status` is the only field to set from the triage itself:
  - `under_investigation` — default when Percona hasn't yet confirmed impact. Use this unless the user tells you otherwise.
  - `affected` — confirmed vulnerable, no fix yet.
  - `fixed` — confirmed vulnerable, fix shipped (needs a version in `action_statement`).
  - `not_affected` — confirmed not exploitable in the Percona product's context.
- **`justification` is never inferred by the skill** when writing a fresh statement (i.e. no
  existing published statement covers this CVE/release — see the check above). Always leave it as
  the literal placeholder string above when `status` is `not_affected`, and drop the field
  entirely for any other status. The user fills it in by hand. Valid OpenVEX justification values
  (for reference, do not auto-select):
  - `component_not_present`
  - `vulnerable_code_not_present`
  - `vulnerable_code_not_in_execute_path`
  - `vulnerable_code_cannot_be_controlled_by_adversary`
  - `inline_mitigations_already_exist`
- Leave `impact_statement` and `action_statement` as `<MANUAL: fill in>` placeholders too — these depend on Percona's own release timeline, which the feed knows nothing about.
