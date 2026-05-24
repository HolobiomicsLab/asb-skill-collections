# Conflict of Interest (COI) Policy

## Summary

Self-review of papers you co-authored is **allowed** with three safeguards.

## Safeguard 1 — Automatic COI detection

`verify-coi.yml` runs on every PR that touches `collections/<slug>/v<N>/reviews/*.yaml`.
It cross-checks the paper's author list (via OpenAlex) against the reviewer's ORCID.
The action auto-populates three fields in the attestation:

- `is_coauthor: true|false`
- `author_position: <integer | null>` (1 = first author)
- `is_corresponding: true|false`

CI **fails** if the action-detected `is_coauthor` value contradicts the manually-declared
value in the attestation file.

## Safeguard 2 — Mandatory disclosure

Every `attestation.yaml` file must include an `is_coauthor` field. Omission blocks merge.

## Safeguard 3 — Second reviewer when is_coauthor: true

When `is_coauthor: true`, a `co_reviewer` block is required in the attestation:

```yaml
co_reviewer:
  orcid: "0000-0000-0000-0000"
  github: second-reviewer-handle
  tier: reviewer       # must be >= reviewer
  sign_off_pr: 123     # PR number where co-reviewer posted approval comment
```

The co-reviewer must:
- Have a different ORCID (not also a co-author of the same paper)
- Be identity-verified at >=Reviewer tier in `contributors.jsonld`
- Have posted a sign-off comment on the PR

CI checks all three conditions. Merge is blocked until satisfied.

## Lead Curator non-self minimum

Of a Lead Curator's 30 qualifying reviews, **at least 20 must be non-self-authored**
(papers where `is_coauthor: false`). This is enforced by `tier-update.yml`.

## Credit accounting

Curators receive full credit regardless of COI status.
`contributors.jsonld` surfaces `self_authored_reviews` and `external_reviews` as
separate counters, both publicly visible.

## Process for detected COI violations

1. CI flags the mismatch as a PR comment
2. Reviewer must amend their attestation to match detected values
3. If second reviewer is missing, the PR blocks until they are added
4. Maintainer reviews both attestations before merge

## Appeals

If you believe the OpenAlex author list is wrong (e.g., name disambiguation error),
open an issue with evidence and a maintainer will manually override via
`coi_override: true` in the attestation, with a justification note.
