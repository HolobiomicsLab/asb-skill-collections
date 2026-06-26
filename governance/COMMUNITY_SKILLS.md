# Community skills

Most ASB-Skills are distilled from peer-reviewed method papers by the curation
pipeline (`provenance_tier: literature`). This document defines the **second**
intake path: skills **contributed or curated outside that pipeline**
(`provenance_tier: community`). A community skill carries its own attribution, is
not required to derive from a paper, and is held to the **same structural
discipline** as a published skill so a maintainer's review is about quality and
fit — not formatting.

It complements:

- [`PROVENANCE_TIERS.md`](PROVENANCE_TIERS.md) — defines the `community` tier and
  its enforced invariant (a `related_skills` key must be present; an empty list is
  allowed). `provenance_tier` is **origin** ("where did the content come from?").
- [`LICENSE_TIERS.md`](LICENSE_TIERS.md) — the **consumer** axis: a community skill
  still declares the `license_tier` of the tool it grounds on (`open` /
  `noncommercial` / `restricted`), independent of its provenance.
- [`SOURCES.md`](SOURCES.md) — the **scientific** gate for paper-derived sources.
  Community skills are not anchored to the review series, but the same spirit of
  auditable, principled inclusion applies.

## The curation model

Community skills move along a one-way **proposal rail** with a human merge gate.
No contributor self-merges; CI checks structure; a maintainer judges fit.

1. **Open submission.** Anyone may propose a skill. The contributor runs the
   `propose-skill` command
   ([`collections/metabolomics/v2/commands/propose-skill.md`](../collections/metabolomics/v2/commands/propose-skill.md)),
   which normalizes the local skill, matches it against the collection to suggest
   `related_skills` + `tools_used`, warns about near-duplicates, best-effort grounds
   it, tiers it `community` / `hold`, and **stages** files via
   `scripts/propose_skill.py`. Lighter-weight intake (issue first) is described in
   [`CONTRIBUTING.md`](../.github/CONTRIBUTING.md).

2. **Staging.** Staged proposals land on the proposal rail, never directly in the
   shipped tree:
   - `collections/<slug>/v<N>/proposals/skills/<skill-slug>/SKILL.md` — the
     normalized skill, frontmatter `provenance_tier: community`, `status: hold`.
   - `collections/<slug>/v<N>/proposals/wave-skills-<date>.yaml` — the proposal
     ledger (schema `asb-skill-proposals/1.0`), the skill analogue of the paper
     `wave-*.yaml` ledgers.

3. **CI validation.** On the PR, `scripts/check_proposals.py` (wired into
   `validate.yml` as the **Proposals gate**) holds every staged
   `proposals/skills/*/SKILL.md` to the same discipline a published skill must pass:
   - `metadata.provenance_tier == "community"` **and** a `related_skills` key is
     present (the community provenance invariant);
   - top-level `status == "hold"` (the proposal-rail invariant);
   - description discipline (prefix ∈ {`Use when`, `Reference for`, `Explains`,
     `Decision support for`}, 50–300 chars, no marketing terms), EDAM IRIs start
     `http://edamontology.org/`, valid `license_tier`;
   - every `metadata.tools_used` slug resolves in `tools_index.json`.

   CI checks **structure**, never scientific merit — that is the maintainer's call.

4. **Maintainer merge.** A maintainer (see [`MAINTAINERS.md`](MAINTAINERS.md))
   reviews the proposal for quality, originality (not a near-duplicate of an
   existing skill — annotate/merge instead), and fit, then merges. **No self-merge.**

5. **Optional expert attestation.** Stronger trust signals may be attached, but are
   **not required** to accept a community skill:
   - an **expert attestation** — a verified domain reviewer (Reviewer tier or above,
     per [`CONTRIBUTING.md`](../.github/CONTRIBUTING.md)) signs off on the skill via a
     `reviews/` attestation, the same mechanism used for paper reviews; and/or
   - a **community signal** — e.g. issue/PR endorsements, downstream use, or a
     downstream maintainer vouching for the skill.

   These raise confidence and inform promotion priority; their absence does not
   block acceptance at the `community` tier.

6. **Wave promotion.** Accepted community skills are promoted out of `proposals/`
   into the shipped collection in **curation waves** (the same batched cadence as
   paper inclusion). At a wave, a maintainer moves the staged `SKILL.md` into
   `collections/<slug>/v<N>/skills/<slug>/`, registers it in `skills_index.json` (so
   it is discoverable and its `tools_used` are reflected in each tool's
   `used_by_skills`), and the ledger entry's `status` is flipped from `hold` to its
   accepted state. The skill keeps `provenance_tier: community` — promotion changes
   its *location and discoverability*, not its origin.

## Invariants (summary)

| Concern | Rule | Enforced by |
|---|---|---|
| Origin | `provenance_tier: community` + `related_skills` key present | `check_proposals.py`, `check_provenance_tiers.py` |
| Rail | `status: hold` while in `proposals/` | `check_proposals.py` |
| Structure | description / EDAM / `license_tier` discipline | `normalize_skill.frontmatter_violations` |
| Tools | every `tools_used` slug resolves in `tools_index.json` | `check_proposals.py` |
| Merge | maintainer-only; no self-merge | `MAINTAINERS.md`, `CODEOWNERS` |
| Licensing | skill prose contributed under **CC-BY-4.0** | issue + PR template checkbox |

## Licensing of contributed prose

The **skill prose** a contributor writes (description, body) is contributed under
**CC-BY-4.0**. This is the contributor's grant on their own text and is distinct
from the `license_tier` axis, which describes the **tool the skill grounds on**.
The CC-BY-4.0 grant is confirmed via the checkbox on the
[`propose-skill` issue template](../.github/ISSUE_TEMPLATE/propose-skill.md) and on
the [pull-request template](../.github/PULL_REQUEST_TEMPLATE.md).
