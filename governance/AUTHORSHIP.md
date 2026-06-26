# Authorship & co-authorship of contributed skills

Most ASB-Skills are distilled from peer-reviewed method papers, where authorship
sits with the **paper**. This document defines authorship for the **second intake
path** — skills a tool's author **contributes or claims** for their own tool
(`provenance_tier: community`) — and how that authorship is *verified*, *credited*,
and kept honest under the project's no-self-merge norm.

It complements:

- [`COMMUNITY_SKILLS.md`](COMMUNITY_SKILLS.md) — the curation model these claimed
  skills travel through (the `proposals/` rail + maintainer merge gate). A claimed
  skill **is** a community skill; this doc adds the *attribution* layer on top.
- [`PROVENANCE_TIERS.md`](PROVENANCE_TIERS.md) — `provenance_tier` is **origin**;
  authorship is **attribution**. A skill is `community` because of where its content
  came from, and carries an author because a verified person contributed it.
- [`COI_POLICY.md`](COI_POLICY.md) — the same self-review-is-allowed-with-safeguards
  spirit that governs co-authored *paper reviews* governs *self-authored skills* here.
- [`MAINTAINERS.md`](MAINTAINERS.md) — who the independent merge gate is.

## The co-authorship model

A tool's author files a **claim-skill** issue
([`.github/ISSUE_TEMPLATE/claim-skill.md`](../.github/ISSUE_TEMPLATE/claim-skill.md));
a maintainer runs the **maintainer-run** `claim-skill` command
([`collections/metabolomics/v2/commands/claim-skill.md`](../collections/metabolomics/v2/commands/claim-skill.md)),
which reuses the `propose-skill` flow (normalize → match → ground → stage), writes
the author into the staged skill, and prepares a reviewable PR. The author reviews
their own contribution; **a different maintainer merges** (never self-merge); the
author is then credited. Three properties make this safe and durable:

### 1. Verified identity (credit is never granted to an unverified claim)

Authorship credit is granted **only to a verified identity**, using the **same**
machinery as curator candidacy (`vet-curator`):

- **L1** — the author's GitHub URL appears in their **ORCID public record**.
- **L2** — the author's **ORCID is an author on the tool's paper DOI**, via OpenAlex.

If the author is not yet a verified contributor, they complete
[`CONTRIBUTING.md`](../.github/CONTRIBUTING.md) **Step 0** (a
`candidates/<handle>.yaml` PR) first; their authorship is credited once that lands.
Identity verification is a **hard gate** in the claim-skill command — no verified
identity, no credit.

### 2. Conflict of interest is acknowledged; the maintainer is the independent gate

Authoring a skill for **your own tool** is a conflict of interest, and the author
**reviewing their own contribution** is a self-review. As in
[`COI_POLICY.md`](COI_POLICY.md), this is **disclosed, not disqualifying**:

- the COI is disclosed on the claim-skill issue and is visible in the staged PR
  (author requested as reviewer of their own skill);
- the **independent gate** is the **merging maintainer**, who must be a *different*
  person than the author and who judges quality/fit/originality (annotate or merge
  into an existing skill rather than accepting a near-duplicate);
- **no self-merge** — the project-wide invariant. CI checks structure only
  (`check_proposals.py`); merit and the COI judgement are the maintainer's.

### 3. Credit surfaces in three durable places

Once merged, an author's contribution is credited in:

- **`contributors.jsonld`** — the author-credit path of
  [`scripts/tier_update.py`](../scripts/tier_update.py) increments the contributor's
  `asb:authored_skills` counter and re-evaluates their tier. This path is
  independent of the review counters and **never downgrades** an already-higher
  tier (an authored skill reaches only the *reviewer* entry tier on its own):

  ```bash
  python scripts/tier_update.py --orcid "<author-ORCID>" \
      --collection "<slug>" --credit-author \
      --contributors contributors.jsonld \
      --criteria "collections/<slug>/<vN>/curator-criteria.yaml"
  ```

- **The merge commit's `Co-authored-by:` trailer** — `Co-authored-by: <Name>
  <email>` on the PR's commit, so the contribution shows on the author's GitHub
  history. The claim-skill command emits this trailer for the merging maintainer.

- **`CITATION.cff`** — at release, collection authorship (the Zenodo author list)
  is reconciled from `contributors.jsonld`, so a verified skill author appears in
  the citable record of the release they contributed to.

The author is also written into the **skill's own** `contributors` frontmatter
block as `role: author` (keys `name`/`role`/`orcid`/`github`; roles validated
against `VALID_CONTRIBUTOR_ROLES` by `check_proposals.py`), so attribution travels
with the skill file itself.

## Invariants (summary)

| Concern | Rule | Enforced by |
|---|---|---|
| Identity | author credited only after L1+L2 verification | `vet-curator`, claim-skill command (hard gate) |
| COI | self-authoring/self-review disclosed; merging maintainer is independent | claim-skill command, `MAINTAINERS.md` |
| Merge | maintainer-only; merger ≠ author; no self-merge | `MAINTAINERS.md`, `CODEOWNERS` |
| In-skill credit | `contributors` entry `role: author`, well-formed keys | `normalize_skill.contributor_violations`, `check_proposals.py` |
| Registry credit | `asb:authored_skills` ++ , tier re-evaluated, never downgraded | `scripts/tier_update.py --credit-author` |
| Commit credit | `Co-authored-by:` trailer on the merge commit | claim-skill command |
| Licensing | skill prose contributed under **CC-BY-4.0** | claim-skill issue + PR template |

## Licensing of contributed prose

The **skill prose** a contributing author writes (description, body) is contributed
under **CC-BY-4.0** — the same grant as any community skill
([`COMMUNITY_SKILLS.md`](COMMUNITY_SKILLS.md)). This is distinct from the
`license_tier` axis, which describes the **tool the skill grounds on**.
