---
name: Propose a meta-skill (super-skill / pipeline)
about: Suggest a workflow-level super-skill that orchestrates several existing sub-skills into a canonical pipeline. Keep it short — a maintainer (or the synthesize-meta-skill command) fills in the rest.
title: "Propose meta-skill: <name>"
labels: ["propose", "meta-skill", "needs-triage"]
---

<!--
Keep this short. A meta-skill (super-skill) does NOT re-implement a procedure — it
SEQUENCES existing sub-skills into a canonical end-to-end pipeline (e.g. "molecular
networking": feature detection/alignment → spectral similarity/networking →
annotation/propagation → visualization). Tell us WHAT pipeline it captures, WHICH
sub-skills/tools it should orchestrate, and WHY it's worth shipping as a super-skill.
The `synthesize-meta-skill` command does the synthesis, grounding, and normalization,
and stages a reviewable PR. A maintainer makes the final merge decision — you cannot
self-merge.
See governance/META_SKILLS.md for how super-skills are defined and curated.
-->

**What pipeline does the meta-skill capture?** <!-- one line, e.g. "End-to-end untargeted LC-MS molecular networking" -->

**Why it matters (one or two sentences):**
<!-- What canonical workflow does it name, and why is it worth grounding agent retrieval on at the workflow level rather than per-step? -->

**Sub-skills / tools to orchestrate (ordered):**
<!--
The ordered stages the pipeline sequences, and the sub-skill slug(s) / tool(s) that
carry each stage — as much as you know. The command resolves and completes these.
e.g.
  1. feature detection/alignment — <slug or tool>
  2. spectral similarity / networking — <slug or tool>
  3. annotation / propagation — <slug or tool>
  4. visualization — <slug or tool>
-->

**Target collection:** <!-- metabolomics (default), or another collection slug -->

---
<!-- Optional, all skippable — a maintainer/the command resolves these: -->
- **Decision points between stages?** <!-- the choices a user makes moving stage→stage, if you know them -->
- **Related existing skills or super-skills?** <!-- slugs it overlaps or composes, if you know them -->
- **You:** <!-- @handle, ORCID -->
- **Conflict of interest?** <!-- disclosure only, never disqualifying -->

## Licensing

- [ ] I license my contributed meta-skill prose (description + body) under **CC-BY-4.0**.

<!--
This CC-BY-4.0 grant covers the text you wrote. A synthesized super-skill still
declares the `license_tier` of the tools its orchestrated stages ground on (open /
noncommercial / restricted) — see governance/LICENSE_TIERS.md.
-->
