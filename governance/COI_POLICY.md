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

**At v0, CI checks none of the three, and gate 13 is formally waived** — see
`CONTENT_POLICY.md` §9 (LOCKED 2026-06-14) and §13. What `verify-coi.yml` actually does is
narrower and worth stating exactly, because a reader who takes the previous paragraph at face
value believes a check ran:

- it compares the **declared** COI against the one detected from OpenAlex authorship, and fails on a
  mismatch — this is a real check and it is the one with teeth;
- it tests that a `co_reviewer` block is **present** (truthy), and looks at nothing inside it;
- ORCID distinctness, the >=Reviewer tier lookup and the sign-off comment are **not implemented**.
  `sign_off_pr` appears three times in this repository, all in documentation and none in code.

It has also never run: its path filter is `collections/**/reviews/*.yaml` and no `reviews/`
directory exists under `collections/` or `staged-collections/` — the only one in the tree holds a
lone `.gitkeep`. No review attestation has been committed, so v0 has no attestation for the gate to
check.

**v1.** The three conditions become enforced when gate 13's waiver expires (§9, ~Q4 2026). Of the
three, ORCID distinctness is the one with genuine integrity value and the one that is not blocked:
it is a string comparison plus one further `check_coi.py` call. The tier lookup cannot be switched
on before `contributors.jsonld` has a record — it currently reads `"contributors": []`, so the check
would fail closed on every PR.

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
