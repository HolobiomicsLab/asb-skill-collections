# Conflict of Interest (COI) Policy

## Summary

Self-review of papers you co-authored is **allowed** with three safeguards.

## Safeguard 1: COI detection by a script a maintainer runs

COI detection is not automatic. A maintainer runs `scripts/check_coi.py` on a PR that touches `collections/<slug>/v<N>/reviews/*.yaml`
in the domain repository. (The `verify-coi.yml` workflow that once ran it on every such PR no longer
exists.) It cross-checks the paper's author list (via OpenAlex) against the reviewer's ORCID.
The script reports three fields for the attestation:

- `is_coauthor: true|false`
- `author_position: <integer | null>` (1 = first author)
- `is_corresponding: true|false`

The detected `is_coauthor` value is compared with the manually-declared value in the
attestation file by the maintainer who runs the script; no workflow of this repository
fails a PR on a mismatch any more.

## Safeguard 2 — Mandatory disclosure

Every `attestation.yaml` file must include an `is_coauthor` field. Omission blocks merge.
No workflow checks for the field; the maintainer who reviews the PR does not merge an
attestation without it.

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
`CONTENT_POLICY.md` §9 (LOCKED 2026-06-14) and §13. What the removed `verify-coi.yml` workflow did was
narrower and worth stating exactly, because a reader who takes the previous paragraph at face
value believes a check ran:

- it compared the **declared** COI against the one detected from OpenAlex authorship, and failed on a
  mismatch — this was a real check and it was the one with teeth;
- it tested that a `co_reviewer` block is **present** (truthy), and looked at nothing inside it;
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
(papers where `is_coauthor: false`). This is enforced by `scripts/tier_update.py`, which a maintainer runs after a merge.

## Credit accounting

Curators receive full credit regardless of COI status.
`contributors.jsonld` surfaces `self_authored_reviews` and `external_reviews` as
separate counters, both publicly visible.

## Process for detected COI violations

1. The maintainer who runs `scripts/check_coi.py` reports the mismatch on the PR (no
   workflow posts it)
2. Reviewer must amend their attestation to match detected values
3. If second reviewer is missing, the PR blocks until they are added (from v1; gate 13
   is waived at v0, see Safeguard 3)
4. Maintainer reviews both attestations before merge

## Appeals

If you believe the OpenAlex author list is wrong (e.g., name disambiguation error),
open an issue with evidence and a maintainer will manually override via
`coi_override: true` in the attestation, with a justification note.
