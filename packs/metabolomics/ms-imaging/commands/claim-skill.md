---
description: Maintainer-run — turn a tool author's claim-skill issue into a staged community-skill PR that credits the author as a verified co-author (contributors role:author + Co-authored-by). You never auto-open or merge it.
argument-hint: "[issue-number-or-url] [collection-dir]"
---
You are a **maintainer** turning a tool author's *claim-skill* issue
([`.github/ISSUE_TEMPLATE/claim-skill.md`](../../../../.github/ISSUE_TEMPLATE/claim-skill.md))
into a staged **community-tier** proposal PR that credits the author as a
**verified co-author**. This is the issue→PR transform: it is **maintainer-run**
(it preserves the "you cannot self-merge" norm), it reuses the entire
`propose-skill` flow, and it **never opens or merges the PR** — you hand the exact
commands to a human to review and run, and a *different* maintainer merges.

Read first: [`governance/AUTHORSHIP.md`](../../../../governance/AUTHORSHIP.md)
(the co-authorship model + the verified-identity / COI gate),
[`governance/COMMUNITY_SKILLS.md`](../../../../governance/COMMUNITY_SKILLS.md)
(curation model), and the sibling command
[`propose-skill.md`](propose-skill.md) (the normalize→match→ground→stage flow this
reuses).

Inputs: `$ARGUMENTS` — the claim-skill **issue** (number or URL, required) and the
collection dir (default `collections/metabolomics/v2`).

Steps:

1. **Read the issue.** Extract: the skill (what it does + the linked `SKILL.md` or
   pasted prose), the **tool/method and its paper DOI**, and the author's identity
   block — **name** (as it should appear in credit), **ORCID**, **GitHub**, and the
   **email** for the `Co-authored-by:` trailer. If the skill prose is only linked,
   fetch it into a local `SKILL.md`. If the identity block is incomplete, ask for the
   missing fields on the issue and **stop** — do not invent an identity.

2. **Verify authorship identity — this gate is mandatory.** Authorship credit is
   only granted to a **verified** identity (governance/AUTHORSHIP.md). Confirm the
   author is (or becomes) a verified contributor via the **same** mechanism as
   curators: L1 (their GitHub URL is in their ORCID public record) and L2 (their
   ORCID is an author on the tool's paper DOI, via OpenAlex) — i.e. the `vet-curator`
   checks. If they are not yet in `contributors.jsonld`, point them at
   [`CONTRIBUTING.md`](../../../../.github/CONTRIBUTING.md) Step 0 (open a
   `candidates/<handle>.yaml` PR) **first**; their authorship can be credited once
   that lands. Do not proceed to crediting until identity is verified.

3. **Run the propose-skill flow (normalize → match → ground → tier).** Follow
   [`propose-skill.md`](propose-skill.md) steps 2–5 verbatim on the author's
   `SKILL.md`:
   - normalize: `python -m scripts.normalize_skill --skill-md "<path>"`;
   - match: `scripts.skill_match.match_skills` / `match_tools` / `near_duplicates`
     over the collection's `skills_index.json` + `tools_index.json` to fill
     `related_skills` + `tools_used` (warn + suggest annotate/merge on a near-dup);
   - ground (best-effort, this is where Perspicacité fits) against the **tool's own
     paper DOI** from the issue:
     `python -m scripts.ground_skill --doi "<DOI>" --skill-md "<normalized-SKILL.md>"`
     — never fails the flow; attach `derived_from` only on a `supported: true`
     (`confidence` ∈ {high, medium}) verdict you've eyeballed.

4. **Write the author into the staged skill's `contributors` (role: author).**
   Assemble the frontmatter with `scripts.normalize_skill.normalized_frontmatter`,
   passing the `contributors=` list with the author entry — keys
   `name`/`role`/`orcid`/`github` (role **`author`**); unknown keys are dropped and
   the role is gate-validated (`VALID_CONTRIBUTOR_ROLES`, enforced by
   `check_proposals`). Keep `provenance_tier: community`, `status: hold`:
   ```python
   from scripts.normalize_skill import normalized_frontmatter
   fm = normalized_frontmatter(
       raw_fm,
       related_skills=related,           # from step 3
       tools_used=tools,                 # from step 3
       license_tier=license_tier,        # from the tool the skill grounds on
       contributors=[{
           "name":   "<author name>",
           "role":   "author",
           "orcid":  "<0000-0000-0000-0000>",
           "github": "<@handle>",
       }],
       # derived_from=["<DOI>"]  # only if grounding was supported (step 3)
   )
   ```
   Write `fm` into a temporary `SKILL.md` to stage.

5. **Stage the proposal (writes files, no git).** Same deterministic stager as
   `propose-skill`, idempotent; preview with `--dry-run` first:
   ```bash
   python -m scripts.propose_skill --collection "<collection-dir>" \
       --skill-md "<normalized-SKILL.md>" --dry-run
   python -m scripts.propose_skill --collection "<collection-dir>" \
       --skill-md "<normalized-SKILL.md>"          # --date YYYY-MM-DD optional
   ```
   (`propose_skill` flags: `--collection`, `--skill-md`, `--date`, `--dry-run`.)

6. **Validate the staged proposal** with the same gate CI runs — this also confirms
   the `contributors` block is well-formed (CI `Proposals gate`):
   `python -m scripts.check_proposals "<collection-dir>"`

7. **Print the review summary + the exact PR commands — then stop.** Show: the
   staged paths, the chosen `related_skills` / `tools_used` / `license_tier`, the
   author `contributors` entry, any near-duplicate warnings, and whether grounding
   succeeded. Then print the exact commands for a human to review and run — note the
   `Co-authored-by:` trailer (credits the author on the commit), `Closes #<issue>`,
   and requesting the **author as a reviewer** of their own contribution (the
   self-review is disclosed; the *merging* maintainer is the independent gate —
   governance/AUTHORSHIP.md):
   ```bash
   git checkout -b claim-skill/<slug>
   git add collections/<...>/proposals/skills/<slug>/SKILL.md \
           collections/<...>/proposals/wave-skills-<date>.yaml
   git commit -m "claim(community): <slug>" \
     -m "Closes #<issue>" \
     -m "Co-authored-by: <Author Name> <author-email>"
   git push -u origin claim-skill/<slug>
   gh pr create --fill --label claim,community-skill,co-authorship \
     --reviewer <author-github-handle> \
     --body "Closes #<issue>. Author credited as co-author (contributors role:author)."
   ```
   State explicitly: **this never opens or merges the PR.** A maintainer reviews fit
   and merges; **no self-merge**, and the *merging* maintainer must not be the
   author. On merge, the author's credit is recorded in `contributors.jsonld` via the
   author-credit path:
   ```bash
   python scripts/tier_update.py --orcid "<author-ORCID>" \
       --collection "<slug>" --credit-author \
       --contributors contributors.jsonld \
       --criteria "collections/<slug>/<vN>/curator-criteria.yaml"
   ```
   (`tier_update --credit-author` increments `asb:authored_skills` and re-evaluates
   tier; it never downgrades an already-higher tier — governance/AUTHORSHIP.md.)

Arguments: $ARGUMENTS
