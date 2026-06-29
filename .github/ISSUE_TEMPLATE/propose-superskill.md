---
name: Propose a super-skill
about: Propose a composite workflow super-skill (a DAG of existing leaf skills)
title: "Propose super-skill: <short name>"
labels: ["propose-superskill", "needs-triage"]
---

> 🧩 **What this is:** a super-skill is a *composite workflow* — an ordered DAG of
> **existing leaf skills** for an end-to-end task (e.g. `mzML → annotation`). It is
> generated from a short **skeleton** (stages + goals + preferred leaf skills) by
> the ASB factory, not hand-written. It reuses leaves; it does not add new ones.
> To add a *new tool/paper*, file a [Propose a paper](./propose-paper.md) instead.

## Super-skill

- **Name:** <!-- e.g. untargeted-lcmsms-annotation -->
- **One-line goal:** <!-- the end-to-end task it accomplishes -->
- **Target collection / version:** <!-- e.g. metabolomics/v2, or "next" -->
- **Techniques / platforms:** <!-- e.g. LC-MS/MS, DDA; or NMR 1D/2D -->

## Stages (the skeleton outline)

List the ordered stages. For each: the goal, and the **leaf skill(s)** it should
use (by slug from `skills_index.json`) plus any tools. Earlier stages feed later
ones. Aim for 4–8 stages.

| # | Stage goal | Preferred leaf skill(s) / tools | Feeds stage(s) |
|---|---|---|---|
| 1 | <!-- e.g. preprocess raw files --> | <!-- e.g. xcms-peak-picking --> | 2 |
| 2 | <!-- e.g. quality control --> | <!-- ... --> | 3 |
| … | | | |

## Grounding

<!--
Which source papers / DOIs back this pipeline as a recognized end-to-end method?
Each stage's leaves already carry their own DOIs; cite the papers that justify the
*overall* workflow shape (a protocol/review/benchmark), if any.
-->

## Rationale

<!--
3-6 sentences: why this workflow, who runs it, what agent task / benchmark it
enables, and how it differs from existing super-skills in the collection.
-->

## Proposer

- **GitHub:** <!-- @your-handle -->
- **ORCID (optional but recommended):** <!-- 0000-0000-0000-0000 -->
- **Affiliation (optional):**

## Conflicts of interest

- [ ] I authored a paper grounding a stage of this workflow
- [ ] I maintain a tool used by this workflow
- [ ] None of the above

<!-- COI doesn't disqualify a proposal — it just gets disclosed for transparency. -->

## Checklist for the curator reviewing this proposal

(For maintainers; leave unchecked when filing.)

- [ ] Every preferred leaf slug resolves in the target `skills_index.json`
- [ ] Stages form a valid DAG (no cycles, no dangling feeds)
- [ ] No leaf appears in two stages (de-collision)
- [ ] Scientific ordering is sound (a domain reviewer signed off)
- [ ] Not a duplicate of an existing super-skill
- [ ] Skeleton authored under `skeletons/<collection>/<slug>.yaml`
- [ ] Generated with `compose_workflows.py`; passes `validate_workflows.py`
- [ ] Decision: accept / reject / defer-pending-info
