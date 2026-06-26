---
description: Synthesize a workflow-level super-skill from a pipeline seed — cluster the sub-skills, identify the canonical ordered pipeline, write the orchestration, tier it synthetic/super/hold, and stage a reviewable proposal PR (you never auto-merge — a maintainer merges after open curation).
argument-hint: "[pipeline-name] [short-description] [collection-dir]"
---
You are auto-creating a **super-skill** — a workflow-level meta-skill that
orchestrates several existing sub-skills (e.g. "molecular networking") — and
staging it `provenance_tier: synthetic` on this collection's `proposals/` rail.
You do the clustering, the agentic identify-the-pipeline reasoning, and the body
writing; the deterministic clustering / frontmatter / file-writing is
`scripts/synthesize_meta_skill.py` (a **helper library**, not a CLI — you drive
its functions inline, the way `commands/propose-skill.md` drives the matcher). You
**never** open or merge the PR: you hand over the exact commands to review and
fire, and a maintainer makes the final merge decision **after open community/expert
curation**. This is the same staging + curation rail as the community pipeline —
only *creation* is automated synthesis rather than human contribution.

Read first: [`governance/META_SKILLS.md`](../../../../governance/META_SKILLS.md)
(the super-skill concept, `skill_kind: super`/`orchestrates`, and the open-curation
model), [`governance/PROVENANCE_TIERS.md`](../../../../governance/PROVENANCE_TIERS.md)
(the `synthetic` tier + its `synthesized_from` invariant), and
[`governance/LICENSE_TIERS.md`](../../../../governance/LICENSE_TIERS.md) (set
`license_tier` from the tools the orchestrated sub-skills ground on). The precedent:
`skills/asb-metabolomics/SKILL.md` and `skills/_router/SKILL.md` are hand-authored
meta-skills — this command generalizes them into a synthesizable, openly-curated rail.

Inputs: `$ARGUMENTS` — the pipeline `name` (required), a short `description` of what
the pipeline does (required), and the collection dir (default
`collections/metabolomics/v2`).

Steps:

1. **Cluster the candidate sub-skills + tools around the seed.** Build the seed text
   (`name + description`) and run the synthesizer's clustering wrapper. It calls the
   community matcher (Perspicacité KB-first, **lexical fallback — no server
   required**, never raises) and resolves the tools the matched sub-skills ground
   on. Run from the repo root so `scripts` is importable:
   ```python
   from scripts.synthesize_meta_skill import cluster_subskills
   from scripts.skill_match import near_duplicates

   seed = "<name> — <short description>"
   cluster = cluster_subskills(seed, "<collection-dir>", k=15)   # matcher injectable for tests
   # cluster == {"subskills": [{slug, score, backend}], "tools": [{slug, score}]}
   subskills = cluster["subskills"]
   tools     = cluster["tools"]
   dups      = near_duplicates(subskills, threshold=0.85)        # warn on overlap, don't dedupe silently
   ```
   Surface the clustered sub-skill slugs (with scores) and tool slugs.
   `near_duplicates` returns the clustered sub-skills whose match score clears the
   threshold — i.e. the most strongly-overlapping sub-skills in the cluster, not an
   existing duplicate super-skill. Treat a dense cluster of high-scoring overlaps as a
   **signal to curate/merge stages** (and to check the collection for an existing
   super-skill covering the same pipeline before synthesizing) rather than as proof a
   duplicate already exists — **warn**, don't dedupe silently.

2. **Identify the canonical ordered pipeline (the agentic step — this is you, not the
   helper).** From the cluster, extract the recurring end-to-end workflow:
   - the ordered **stages** (for a metabolomics pipeline, typically: feature
     detection/alignment → spectral similarity/networking → annotation/propagation
     → visualization);
   - the **key sub-skill(s) per stage** — pick the highest-signal clustered slugs
     that actually belong to each stage (do **not** dump the whole cluster; curate);
   - the **tools** each stage grounds on (from `cluster["tools"]`);
   - the **decision points** (e.g. polarity handling, similarity threshold,
     library-vs-analog search, when to stop propagating annotations).
   Every slug you keep MUST be a real entry in `<collection-dir>/skills_index.json`
   — verify before citing it. Do not invent sub-skills, stages, tools, or DOIs; if
   the cluster is too thin to form an honest pipeline, say so and stop.

3. **Write the super-skill `Use when…` description + the ordered orchestration body.**
   - **Description** — start with an allowed prefix (`Use when` for a super-skill),
     50–300 chars, no marketing terms; say which pipeline it orchestrates and when to
     reach for it.
   - **Body** — the orchestration narrative: the ordered stages from step 2, each
     stage **referencing its sub-skills by their actual slug**, the tools per stage,
     the decision points, and grounding pointers (how to `/ground` a stage against
     its source). This is genuine synthesis — write the real workflow, cite real
     slugs, don't fabricate.

4. **Assemble the frontmatter (synthetic / super / hold).** Use the synthesizer's
   `meta_frontmatter` — it reuses `normalize_skill.normalized_frontmatter` then
   layers the super-skill invariants (`metadata.skill_kind="super"`,
   `metadata.orchestrates`, `metadata.synthesized_from`), mirrors `related_skills`
   onto the orchestrated slugs, and sets `provenance_tier="synthetic"`,
   `status="hold"`:
   ```python
   from scripts.synthesize_meta_skill import meta_frontmatter

   orchestrates    = ["<stage-1-slug>", "<stage-2-slug>", ...]   # curated, ordered, real
   synthesized_from = orchestrates + ["doi:10...."]              # sub-slugs (+ review DOIs if any)
   tools_used       = ["<tool-slug>", ...]                       # from cluster["tools"]

   fm = meta_frontmatter(
       name="<name>",
       description="<Use when … 50–300 chars …>",
       orchestrates=orchestrates,
       synthesized_from=synthesized_from,
       tools_used=tools_used,
       license_tier="open",            # set from LICENSE_TIERS.md / the grounded tools
   )
   ```

5. **Gate-check the frontmatter before staging.** Run the same description/EDAM/tier
   gate a published skill must pass — `meta_frontmatter` is built to yield zero
   violations, so a non-empty result means your description/tier needs fixing
   (surface it, fix the prose; do **not** fabricate EDAM IRIs):
   ```python
   from scripts.normalize_skill import frontmatter_violations
   v = frontmatter_violations(fm)
   assert not v, v
   ```

6. **Stage the proposal (writes files, no git/gh).** Call the synthesizer's stager —
   it delegates to `scripts/propose_skill.py` (same rail; idempotent), writing
   `proposals/skills/<slug>/SKILL.md` + appending the
   `proposals/wave-meta-skills-<date>.yaml` ledger. The wave `date` is read from
   `ledger_meta` (`date` / `submitted_on`) — there is no `Date.now` in importable
   code, so supply the date explicitly:
   ```python
   from scripts.synthesize_meta_skill import stage_meta_skill

   ledger_meta = {
       "slug": "<slug>",
       "date": "<YYYY-MM-DD>",            # required (no implicit today in the helper)
       "related_skills": orchestrates,
       "tools_used": tools_used,
       "license_tier": fm["metadata"]["license_tier"],
       "status": "hold",
       "skill_kind": "super",
       "synthesized_from": synthesized_from,
   }
   paths = stage_meta_skill("<collection-dir>", fm, body, ledger_meta)
   # paths == {"slug", "skill_md", "ledger"}  → proposals/skills/<slug>/SKILL.md + wave-meta-skills-<date>.yaml
   ```

7. **Validate what was staged** with the same gate CI runs — it enforces the
   synthetic/super invariants (`synthesized_from` non-empty; `skill_kind ∈
   {skill,super}`; for `super`, `orchestrates` non-empty and **every** orchestrated
   slug resolves in `skills_index.json`), so the PR is green before any push:
   ```bash
   python -m scripts.check_proposals "<collection-dir>"
   ```

8. **Print a review summary + the exact PR commands — then stop.** Show: the staged
   paths, the ordered pipeline (stages → orchestrated slugs → tools → decision
   points), the chosen `synthesized_from` / `tools_used` / `license_tier`, any
   near-duplicate warnings, and whether grounding was available. Then print the exact
   fork-and-PR commands for review and to run **themselves**:
   ```bash
   gh repo fork HolobiomicsLab/asb-skill-collections --clone --remote
   git checkout -b synthesize-meta-skill/<slug>
   git add collections/<...>/proposals/skills/<slug>/SKILL.md \
           collections/<...>/proposals/wave-meta-skills-<date>.yaml
   git commit -m "synthesize(super): <slug>"
   git push -u origin synthesize-meta-skill/<slug>
   gh pr create --fill --label propose,synthetic-meta-skill
   ```
   State explicitly: **this command never auto-merges and never opens the PR for
   you.** The synthesized super-skill is staged `status: hold` and the PR **waits for
   open community/expert curation** — a maintainer makes the final merge decision (no
   self-merge), exactly as a synthetic meta-skill is never auto-promoted into
   `v2/skills/` (promotion stays a maintainer wave action).

Arguments: $ARGUMENTS
