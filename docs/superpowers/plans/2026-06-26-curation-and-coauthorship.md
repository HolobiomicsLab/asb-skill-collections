# Beta — curation infra (#5) + issue→PR→co-authorship

> Subagent-driven TDD. Curation-UX features that share issue templates / CI /
> governance, plus the author co-authorship flow.

**Worktree:** `/Users/holobiomicslab/git/asb-wt-beta` (branch
`feat/curation-and-coauthorship`, off `dev`). Work + commit THERE.
**Collection:** `collections/metabolomics/v2`.

## Vision (issue → PR → author reviews → merge with co-authorship)
Lower the contribution barrier and turn the rails into an *attribution engine*: a
tool's author files an issue; a maintainer runs Claude Code to draft a staged-skill
PR (normalize→match→ground via the existing propose-skill flow) crediting the author
as **co-author**; the author reviews their own contribution; a maintainer merges
(never self-merge) and the author is credited in `contributors.jsonld` + the merge
commit's `Co-authored-by:`. Reuse identity (`vet-curator` ORCID/OpenAlex) + COI guards.

## Global Constraints
- Reuse, don't reimplement; READ first: `.github/CONTRIBUTING.md`, the existing
  `.github/ISSUE_TEMPLATE/propose-skill.md`, `scripts/tier_update.py` +
  `.github/workflows/tier-update.yml`, `scripts/normalize_skill.py`,
  `scripts/check_proposals.py`, `scripts/build_grounding_bundle.py` +
  `scripts/build_all_grounding.sh`, `governance/COMMUNITY_SKILLS.md`, `contributors.jsonld`.
- NO auto-merge, NO CI bot that opens PRs — the issue→PR transform is a
  **maintainer-run** Claude Code flow (documented), keeping the "you cannot
  self-merge" norm. NO git/gh/network in scripts. Keep full pytest green
  (dev baseline 385). New scripts in `scripts/`, tests in `tests/`.

---

### Task 1 (#5a): synthesize-meta-skill issue template
Create `.github/ISSUE_TEMPLATE/propose-meta-skill.md` (mirror `propose-skill.md`):
suggest a pipeline/super-skill (name, the sub-skills/tools it should orchestrate,
why). Link `governance/META_SKILLS.md`. (Docs/templates only.)

### Task 2 (#5b): proposals CI feedback action
Create `.github/workflows/proposals.yml` — on PRs touching
`collections/*/proposals/**`, run `python -m scripts.check_proposals
collections/metabolomics/v2` and post a short pass/fail comment so contributors get
fast structural feedback. Keep it additive (don't disturb `validate.yml`).
(CI config only — validate by `yamllint`/parse, no test harness.)

### Task 3 (#5c): rebuild shipped per-technique packs
The new commands (`propose-skill`, `synthesize-meta-skill`) only reach installed
plugins after the units are rebuilt. Run `bash scripts/build_all_grounding.sh`
(or `python -m scripts.build_grounding_bundle` per unit). VERIFY each rebuilt unit's
`commands/` now contains `propose-skill.md` + `synthesize-meta-skill.md` (spot-check
2 units). Commit the regenerated units. (Mechanical regen — large diff is expected;
reviewer spot-checks, does not enumerate.)

### Task 4 (issue→PR): SKILL.md `contributors` field + gate support
**Files:** modify `scripts/normalize_skill.py` + test; `scripts/check_proposals.py`
+ test; the skills LinkML schema if needed.
- Define an optional frontmatter `contributors: [{name, role, orcid?, github?}]`
  (role ∈ {author, reviewer, curator}). `normalize_skill.normalized_frontmatter`
  gains a `contributors=None` param that, when given, emits a well-formed block.
- `check_proposals`: if `contributors` is present, validate each entry is a mapping
  with a non-empty `name` and `role` ∈ the allowed set (do NOT require it).
- Tests: a staged skill with a valid contributors block passes; a malformed one
  (missing name/role, bad role) fails.

### Task 5 (issue→PR): claim-skill flow + author credit
**Files:** create `.github/ISSUE_TEMPLATE/claim-skill.md`,
`collections/metabolomics/v2/commands/claim-skill.md`, `governance/AUTHORSHIP.md`;
modify `scripts/tier_update.py` + test; `.github/CONTRIBUTING.md`.
- `claim-skill.md` issue template: a tool's author claims/contributes a skill —
  self-IDs (ORCID + GitHub), the tool/paper, a one-line description; notes that
  authorship is **verified** (ORCID/OpenAlex via `vet-curator`) before credit.
- `commands/claim-skill.md`: the **maintainer-run** transform — read the issue →
  run the propose-skill flow (normalize→match→ground→stage) → write the author into
  the staged skill's `contributors` (role: author) → prepare a PR with
  `Co-authored-by: <name> <email>`, `Closes #<issue>`, and the author requested as
  reviewer. Explicit: never auto-open/merge; a maintainer reviews + merges.
- `tier_update.py`: add an author-credit path — on merge, a contributor listed as a
  skill `author` is credited in `contributors.jsonld` (increment a contributions
  counter, re-evaluate tier) ALONGSIDE the existing review-attestation path. Keep
  backward compatibility; add a focused test.
- `governance/AUTHORSHIP.md`: the co-authorship model (verified identity, COI of
  self-review acknowledged + maintainer is the independent gate, credit surfaces in
  `contributors.jsonld` + `Co-authored-by` + CITATION). Cross-link COMMUNITY_SKILLS.
- `CONTRIBUTING.md`: a "Claim/contribute a skill for your tool (become a co-author)"
  section.

- [ ] TDD where code is involved (Tasks 4, 5) → commit. Final: full pytest green;
  `check_proposals` passes on real data; all referenced paths/links resolve; the
  claim-skill command's script invocations match the real `--flags`.
