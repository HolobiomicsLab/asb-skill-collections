---
description: Normalize a local skill, match it to the collection, tier it community/hold, and stage a reviewable proposal PR (you never auto-open it — a maintainer merges).
argument-hint: "[path-to-local-SKILL.md] [collection-dir]"
---
You are helping a contributor turn a local skill into a **community-tier proposal**
staged on this collection's `proposals/` rail. You do the matching, grounding, and
normalization; the deterministic file-writing is `scripts/propose_skill.py`. You
**never** open the PR — you hand the contributor the exact commands to review and
fire themselves, and a maintainer makes the final merge decision.

Read first: [`governance/COMMUNITY_SKILLS.md`](../../../../governance/COMMUNITY_SKILLS.md)
(curation model), [`governance/PROVENANCE_TIERS.md`](../../../../governance/PROVENANCE_TIERS.md)
(the `community` tier + its `related_skills` invariant), and
[`governance/LICENSE_TIERS.md`](../../../../governance/LICENSE_TIERS.md) (set
`license_tier` from the tool the skill grounds on).

Inputs: `$ARGUMENTS` — the path to the local `SKILL.md` to propose (required) and
the collection dir (default `collections/metabolomics/v2`).

Steps:

1. **Read the local skill.** Load the candidate `SKILL.md`. Note its `name`,
   `description`, EDAM block, and the tool(s) it grounds on.

2. **Normalize.** Validate the frontmatter against the same gates a published skill
   must pass (description prefix ∈ {`Use when`, `Reference for`, `Explains`,
   `Decision support for`}, 50–300 chars, no marketing terms; EDAM IRIs start
   `http://edamontology.org/`; valid `license_tier` ∈ {open, noncommercial,
   restricted}):
   `python -m scripts.normalize_skill --skill-md "<path>"`
   If it reports violations, surface them and help the contributor fix the prose —
   do **not** fabricate a description or EDAM IRIs.

3. **Match against the collection.** Find the related skills and the tools this
   skill should declare. Use the matcher (Perspicacité KB-first, lexical fallback;
   no server required):
   ```python
   import json
   from scripts.skill_match import match_skills, match_tools, near_duplicates
   skills_index = json.load(open("<collection-dir>/skills_index.json"))
   tools_index  = json.load(open("<collection-dir>/tools_index.json"))
   text = "<name + description + tool names>"
   skills = match_skills(text, "<collection-dir>")          # [{slug, score, backend}]
   tools  = match_tools([s["slug"] for s in skills], skills_index, tools_index, text=text)
   dups   = near_duplicates(skills, threshold=0.85)         # caller-chosen threshold
   ```
   Surface the suggested `related_skills` (matched slugs) and `tools_used` (tool
   slugs) for the contributor to confirm. If `near_duplicates` flags anything,
   **warn** that the skill may overlap an existing one and suggest **annotating or
   merging** into that skill (via `CONTRIBUTING.md`) rather than adding a duplicate.

4. **Ground (optional, best-effort).** If a Perspicacité server is reachable, ground
   the skill's claims against its source the same way `/ground` does
   (`scripts/perspicacite_kb_bind.py`). This is optional — a community skill is not
   required to derive from a paper. If grounding is unavailable, proceed ungrounded
   and say so.

5. **Tier it `community` / `hold`.** Assemble the schema-correct frontmatter:
   `provenance_tier: community` (so the `related_skills` key is present — empty list
   allowed), `status: hold` (the proposal-rail invariant), and the confirmed
   `related_skills` + `tools_used` + `license_tier`. Use
   `scripts.normalize_skill.normalized_frontmatter(...)` and write the result to a
   temporary `SKILL.md` to stage.

6. **Stage the proposal (writes files, no git).** Call the deterministic stager —
   it writes `proposals/skills/<slug>/SKILL.md` + appends the
   `proposals/wave-skills-<date>.yaml` ledger (`asb-skill-proposals/1.0`), and is
   idempotent. Preview first with `--dry-run`:
   ```bash
   python -m scripts.propose_skill --collection "<collection-dir>" \
       --skill-md "<normalized-SKILL.md>" --dry-run
   python -m scripts.propose_skill --collection "<collection-dir>" \
       --skill-md "<normalized-SKILL.md>"          # --date YYYY-MM-DD optional
   ```
   (`propose_skill` flags: `--collection`, `--skill-md`, `--date`, `--dry-run`. Run
   from the repo root so `scripts` is importable.)

7. **Validate what was staged** with the same gate CI runs, so the contributor's PR
   is green before they push:
   `python -m scripts.check_proposals "<collection-dir>"`

8. **Print a review summary + the exact PR commands — then stop.** Show the
   contributor: the staged paths, the chosen `related_skills` / `tools_used` /
   `license_tier`, any near-duplicate warnings, and whether grounding succeeded.
   Then print the exact fork-and-PR commands for them to review and run **themselves**:
   ```bash
   gh repo fork HolobiomicsLab/asb-skill-collections --clone --remote
   git checkout -b propose-skill/<slug>
   git add collections/<...>/proposals/skills/<slug>/SKILL.md \
           collections/<...>/proposals/wave-skills-<date>.yaml
   git commit -m "propose(community): <slug>"
   git push -u origin propose-skill/<slug>
   gh pr create --fill --label propose,community-skill
   ```
   State explicitly: **this command never opens the PR for them** — the contributor
   reviews the staged files and runs the commands, and **a maintainer makes the
   final merge decision** (no self-merge). Remind them the PR template asks them to
   confirm they license their skill prose under **CC-BY-4.0**.

Arguments: $ARGUMENTS
