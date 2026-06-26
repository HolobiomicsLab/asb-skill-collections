# Meta-skills (super-skills)

Most ASB-Skills are **single-procedure** skills: one method, one source. A
**super-skill** (a *meta-skill*) is the workflow level — it **orchestrates** several
existing sub-skills into a canonical end-to-end pipeline (e.g. "molecular
networking": feature detection/alignment → spectral similarity/networking →
annotation/propagation → visualization). It does not re-implement those procedures;
it sequences them, names the decision points between stages, and points each stage
at the sub-skill(s) and tool(s) that carry it.

This document defines the super-skill concept (`skill_kind: super` /
`orchestrates`), the three provenance origins a skill may have, and the
**open-curation** model that governs how a synthesized super-skill reaches the
shipped collection. It complements:

- [`PROVENANCE_TIERS.md`](PROVENANCE_TIERS.md) — defines the `synthetic` tier and its
  enforced invariant (`metadata.synthesized_from` non-empty). `provenance_tier` is
  **origin** ("where did the content come from?"); a super-skill is `synthetic` when
  it is auto-derived from other skills.
- [`COMMUNITY_SKILLS.md`](COMMUNITY_SKILLS.md) — the contributed-skill intake path.
  Super-skills reuse the **same proposal rail + maintainer merge gate**; only the
  *creation* differs (automated synthesis vs. a human contributor).
- [`LICENSE_TIERS.md`](LICENSE_TIERS.md) — the **consumer** axis: a super-skill still
  declares the `license_tier` of the tools its orchestrated stages ground on (`open`
  / `noncommercial` / `restricted`), independent of its provenance.

## What makes a skill a super-skill

A super-skill is distinguished by two `metadata` fields, both checked by the
proposals gate ([`check_proposals.py`](../scripts/check_proposals.py)):

| Field | Meaning | Invariant |
|---|---|---|
| `metadata.skill_kind` | `skill` (default, stands alone) or `super` (orchestrates others) | must be in {`skill`, `super`} |
| `metadata.orchestrates` | the ordered sub-skill slugs the pipeline sequences | for `super`: non-empty list, **every slug resolves in `skills_index.json`** |

A `super` skill is usually `provenance_tier: synthetic` (it is derived from the
skills it orchestrates), so its `metadata.synthesized_from` lists those same
sub-skill slugs. When the canonical pipeline is instead **grounded in a review
article** — a survey/tutorial that defines the workflow's stages — the super-skill
is `provenance_tier: literature` with that review's DOI in `metadata.dois` and
`derived_from` (see *The three provenance origins* below). Either way the body is
**genuine synthesis** — it writes the real ordered workflow and cites each stage's
sub-skills by their actual slug; it never fabricates stages, slugs, tools, or DOIs.

## The three provenance origins

`provenance_tier` answers *where did this skill's content come from?* (see
[`PROVENANCE_TIERS.md`](PROVENANCE_TIERS.md)). The three origins:

- **`synthetic`** — *auto-derived from other skills.* A super-skill synthesized by
  the [`synthesize-meta-skill`](../collections/metabolomics/v2/commands/synthesize-meta-skill.md)
  command lands here: the clustering + frontmatter assembly + staging are
  deterministic (`scripts/synthesize_meta_skill.py`), the identify-the-pipeline and
  body-writing are agentic. Invariant: `metadata.synthesized_from` non-empty.
- **`community`** — *hand-written and contributed* outside the literature pipeline
  (see [`COMMUNITY_SKILLS.md`](COMMUNITY_SKILLS.md)). Invariant: a `related_skills`
  key is present.
- **`literature`** — *distilled from one or more peer-reviewed source papers* by the
  curation pipeline (the origin of every shipped single-procedure skill today).
  Invariant: ≥1 source DOI. A super-skill lands here when its **pipeline is grounded
  in a review article** rather than merely composed from existing skills: the
  `synthesize-meta-skill` command is given a `--review-doi`, and `meta_frontmatter`
  sets `provenance_tier: literature`, `metadata.dois: [<review-doi>]`, and
  `derived_from: [{doi: <review-doi>}]` (while keeping `skill_kind: super` +
  `orchestrates`). This is a **review-grounded meta-skill** — the survey defines the
  canonical stages, the sub-skills carry each stage.

A super-skill therefore has **three** possible origins: `synthetic` (composed from
the orchestrated skills, the default), `literature` (review-grounded, via a review
DOI), or `community` (a hand-authored workflow skill contributed outside the
pipeline). `skill_kind` (`skill` / `super`) is **orthogonal** to provenance: a
`super` skill is usually `synthetic`, but it can be `literature` (review-grounded)
or `community` and still set `skill_kind: super`. The two precedents below are
hand-authored meta-skills that this rail generalizes into a synthesizable,
openly-curated form.

## The open-curation model

A synthesized super-skill moves along the **same one-way proposal rail** as a
community skill, with a human merge gate. **The synthesis is never auto-promoted.**

1. **Automated synthesis (creation).** A maintainer or contributor runs the
   `synthesize-meta-skill` command with a pipeline seed (name + short description).
   It clusters the candidate sub-skills + tools, the agent identifies the canonical
   ordered pipeline and writes the orchestration body, then it stages the proposal
   `provenance_tier: synthetic`, `skill_kind: super`, `status: hold`. The command
   **never opens or merges the PR** — it hands over the exact fork-and-PR commands to
   review and fire.

2. **Staging.** The synthesized skill lands on the proposal rail, never directly in
   the shipped tree:
   - `collections/<slug>/v<N>/proposals/skills/<skill-slug>/SKILL.md` — the
     synthesized super-skill, frontmatter `provenance_tier: synthetic`,
     `skill_kind: super`, `status: hold`.
   - `collections/<slug>/v<N>/proposals/wave-meta-skills-<date>.yaml` — the proposal
     ledger (its own wave, distinct from the community `wave-skills-<date>.yaml`).

3. **CI validation.** On the PR, `scripts/check_proposals.py` (the **Proposals gate**)
   holds the staged skill to the same discipline a published skill must pass, plus the
   provenance + super invariants (reusing the `scripts/provenance_tier.py` kernel): a
   `synthetic` proposal needs non-empty `metadata.synthesized_from`; a `literature`
   (review-grounded) proposal needs ≥1 `metadata.dois`; a `community` proposal needs a
   `related_skills` key. For `super` (any origin): `metadata.skill_kind ∈ {skill,
   super}`, `metadata.orchestrates` non-empty, and **every orchestrated slug resolves
   in `skills_index.json`**. CI checks **structure**, never scientific merit.

4. **Open community/expert review.** The public PR waits for open review — the same
   community-signal / expert-attestation mechanisms described in
   [`COMMUNITY_SKILLS.md`](COMMUNITY_SKILLS.md) §5. A synthesized pipeline is held to
   the same bar as a contributed one: is the workflow honest, are the stages and slugs
   real, is it a genuine pipeline rather than a near-duplicate of an existing
   super-skill (annotate/extend instead).

5. **Maintainer merge.** A maintainer (see [`MAINTAINERS.md`](MAINTAINERS.md)) makes
   the final merge decision after curation. **No self-merge** — and the command never
   auto-merges.

6. **Wave promotion.** Accepted super-skills are promoted out of `proposals/` into the
   shipped collection in curation waves (a maintainer wave action), the same batched
   cadence as paper and community-skill inclusion. The skill keeps
   `provenance_tier: synthetic` — promotion changes its *location and discoverability*,
   not its origin.

## Precedent

`skills/asb-metabolomics/SKILL.md` (the collection guide + license-tier governance
meta-skill) and `skills/_router/SKILL.md` (the routing meta-skill) are **hand-authored
meta-skills** already shipped in the collection. The `synthesize-meta-skill` rail
generalizes that pattern into a synthesizable, openly-curated form: instead of a
maintainer hand-writing each workflow-level skill, the pipeline is clustered and
drafted by synthesis, then held to the same open-review + maintainer-merge gate as
any other proposal.

## Invariants (summary)

| Concern | Rule | Enforced by |
|---|---|---|
| Origin | `synthetic` ⇒ `metadata.synthesized_from` non-empty; `literature` (review-grounded) ⇒ ≥1 `metadata.dois`; `community` ⇒ `related_skills` key | `check_proposals.py`, `check_provenance_tiers.py` |
| Kind | `metadata.skill_kind ∈ {skill, super}` (default `skill`) | `check_proposals.py` |
| Orchestration | for `super`: `metadata.orchestrates` non-empty + every slug in `skills_index.json` | `check_proposals.py` |
| Rail | `status: hold` while in `proposals/` | `check_proposals.py` |
| Structure | description / EDAM / `license_tier` discipline | `normalize_skill.frontmatter_violations` |
| Tools | every `tools_used` slug resolves in `tools_index.json` | `check_proposals.py` |
| Merge | maintainer-only; no self-merge; never auto-promoted | `MAINTAINERS.md`, `CODEOWNERS` |
