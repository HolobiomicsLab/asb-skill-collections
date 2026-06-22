# Release Train: v0 Collections → Zenodo + HuggingFace

**Version:** 0.1 · **Date:** 2026-06-14 · **Status:** active for ASB v0 releases

This runbook documents the complete **linear release pipeline** for ASB-Skill-Collections v0 releases. It is intended for the lead maintainer and release operators.

---

## Quick reference

**Normal release flow (45–90 min human time, all automation):**

```
[1. Human] Draft collection in staged-collections/
   ↓
[2. Contrib PR] → validate.yml gates → Lead maintainer merge
   ↓
[3. Human] Tag release: git tag <slug>-v<N> && git push origin <slug>-v<N>
   ↓
[4. Auto] release.yml triggers on tag
   ├─ pytest: validate collection passes all CI gates
   ├─ regen_catalogue.py: regenerate catalogue.jsonld
   ├─ Upload to Zenodo (fail-soft if ZENODO_TOKEN missing)
   ├─ Update CITATION.cff with minted DOI
   └─ workflow_dispatch: trigger mirror-to-hf.yml
   ↓
[5. Auto] mirror-to-hf.yml (explicit dispatch from release.yml)
   ├─ Generate HF Dataset README card
   ├─ Generate HF Space leaderboard config
   ├─ Upload to HuggingFace Datasets (fail-soft if HF_TOKEN missing)
   └─ Create/update HF Space leaderboard
   ↓
[6. Human] Verify DOI + HF mirrors appear; close PR if any
```

---

## 1. Pipeline stages & automation

### Stage 0: Authoring (in `staged-collections/`)

**Responsibility:** Lead Curator (or nominated contributor) + Holobiomics Lab.

**What happens here:**
- Skill files (SKILL.md), tools, benchmarks, and metadata go into `staged-collections/<slug>/v<N>/`
- Use the templates in `templates/` and follow the structure doc in [CONTRIBUTING.md](../.github/CONTRIBUTING.md)
- Reviews are accumulated in `staged-collections/<slug>/v<N>/reviews/*.yaml` (one file per reviewed paper)
- Contributor PRs reference external papers, linked by DOI via `derived_from` fields in SKILL.md frontmatter

**CI gates run here:** None yet. Staged collections bypass all gates.

**Output:** Complete, review-annotated collection directory under `staged-collections/`

---

### Stage 1: Promotion (Human action)

**Responsibility:** Lead maintainer only.

**What happens:**
1. Review the collection in `staged-collections/<slug>/v<N>/` for completeness
2. Verify all SKILL.md frontmatter is properly formed (see gate 5, 6, 8 in validate.yml)
3. Move directory from `staged-collections/` → `collections/` (or via PR)
4. Commit: `git add collections/<slug>/v<N>` && `git commit -m "promote: <slug>/v<N> to collections"`
5. Push to `main`: `git push origin main`

**CI gates run here:** Yes — validate.yml runs on all push-to-main events (gates 1, 2, 5, 6, 8, 9, 10).

**Human review checkpoint:**
- ✓ All derived_from DOIs exist and resolve
- ✓ No orphan skills (every skill is rooted in at least one paper)
- ✓ Description discipline: starts with approved prefix, 50–300 chars, no marketing terms
- ✓ EDAM IRIs are well-formed (http://edamontology.org/...)
- ✓ RO-Crate metadata is present and valid
- ✓ verify-claims round-trip (indicium adapter) passes (gate 9)
- ✓ Marketplace.json declares all skills

**If CI fails:** Revert the commit and fix the issue(s) in staged-collections/ before re-promoting.

**Output:** Collection now in `collections/<slug>/v<N>/`, passing all CI gates, ready for release tag.

---

### Stage 2: Release tagging (Human action)

**Responsibility:** Lead maintainer only.

**What happens:**
```bash
git tag <slug>-v<N> main
git push origin <slug>-v<N>
```

**Tag format (STRICT):** `<slug>-v<N>`
- `<slug>` = lowercase domain name, alphanumeric + hyphens (e.g., `metabolomics`, `epigenomics`, `transcriptomics`)
- `<N>` = integer version (e.g., `1`, `2`, `3`)
- Examples: `metabolomics-v1`, `epigenomics-v1`, `transcriptomics-v2`

**Dispatch reality (BEFORE this PR):** `release.yml` attempts to trigger `mirror-to-hf.yml` via `github.rest.actions.createWorkflowDispatch(...)`, but `mirror-to-hf.yml` had **NO `workflow_dispatch:` trigger** — so that dispatch call **no-ops** (you cannot dispatch a workflow that does not declare a `workflow_dispatch` trigger). Meanwhile `mirror-to-hf.yml` DID have `on: push: tags: "*-v[0-9]*"`, so it fired from the tag push. Net effect: the explicit dispatch from `release.yml` did nothing, and the tag push fired the mirror — and because `release.yml` itself also runs on the same tag pattern, the tag **double-fires** across the two workflows.

**TARGET (fixed in THIS PR):** `mirror-to-hf.yml` becomes **dispatch-only**: a `workflow_dispatch:` trigger with inputs `{collection_slug, collection_version}` is ADDED (matching what `release.yml` dispatches), and the `on: push: tags: "*-v[0-9]*"` trigger is REMOVED. After this PR, `release.yml`'s dispatch call actually drives the mirror, and the tag double-fire is eliminated.

---

### Stage 3: Validation (Automated via release.yml)

**Responsibility:** GitHub Actions (ubuntu-latest, python 3.12).

**What happens:**

#### Step 1: Extract tag and parse slug/version
```
TAG: metabolomics-v1
→ SLUG=metabolomics, VERSION=1
```

#### Step 2: Run all CI gates (pytest)
```bash
pytest tests/ -v
```
Runs gates: 1, 2, 5, 6, 8, 9, 10 (same as validate.yml; gates 3, 4, 7, 11–14 not automated in v0).

**If pytest fails:** release.yml **stops**. The tag is pushed but the workflow fails. The maintainer must fix the code, amend the collection in `collections/`, re-run pytest locally to confirm, then (optionally) re-push to `main` and re-tag.

---

### Stage 4: Catalogue regeneration (Automated via release.yml)

**Responsibility:** GitHub Actions.

**What happens:**
```bash
python scripts/regen_catalogue.py --repo-root . --output catalogue.jsonld
```

**Output:** `catalogue.jsonld` (machine-readable index of all released collections, skills, tools, benchmarks).

**Commit behavior:** If catalogue.jsonld changed, github-actions[bot] commits and pushes to `main`.

---

### Stage 5: Zenodo deposit (Automated via release.yml, fail-soft)

**Responsibility:** GitHub Actions (Zenodo API).

**Secret required:** `ZENODO_TOKEN` (GitHub secret, scope: create & publish depositions).

**Behavior:**
```
IF ZENODO_TOKEN not set:
  → Log warning and skip (fail-soft; does not block release)
  → Set output.doi = "" (empty)

ELSE (token is set):
  → Create new Zenodo deposition
  → Zip collections/<slug>/v<N>/ → <slug>-v<N>.zip
  → Upload zip to bucket
  → Extract metadata from CITATION.cff (title, authors, ORCID)
  → Set metadata: upload_type=dataset, license=apache-2.0, keywords=[agentic-ai, slug, ...]
  → Publish deposition
  → Extract DOI from response
  → Write doi=10.5281/zenodo.XXXXXXX to $GITHUB_OUTPUT
```

**Zenodo topology (v0, LOCKED):**
- **Exactly ONE concept-DOI per collection-release** (versioned deposition, all versions linked under one concept).
- **The KB snapshot, the indicium schema version, and the asb: ontology Turtle ride as FILES inside that single deposition — they do NOT get separate DOIs.**
- **indicium has its OWN concept-DOI** (minted by the indicium repo's own Zenodo releases). The collection deposition only pins/attaches the indicium version as a file; it does not re-mint a DOI for indicium.
- **Attached files inside the versioned deposition:**
  - `<slug>-v<N>.zip` (the collection directory)
  - the **KB snapshot** for this collection (grounding KB archive)
  - `indicium_version.txt` (the indicium release version pinned by this release; indicium itself is DOI'd separately — see "Indicium co-release" below)
  - `asb_ontology.ttl` (the asb: ontology Turtle snapshot at this release; see SPEC.md §5.1)
  - `CITATION.cff` (for reproducibility)

**DOI output:** Minted DOI is passed to the next step via GitHub output `steps.zenodo.outputs.doi`.

**TODO:** Obtain a real `ZENODO_TOKEN` from https://zenodo.org/account/settings/applications/ and add to GitHub secrets before the first release tag.

---

### Stage 6: CITATION.cff update (Automated via release.yml, conditional on Zenodo DOI)

**Responsibility:** GitHub Actions.

**What happens:**

Only if `steps.zenodo.outputs.doi` is not empty:

```bash
python << 'EOF'
# Update both root CITATION.cff and collections/<slug>/v<N>/CITATION.cff
# regex: ^(doi:\s*).*$ → doi: <minted-doi>
EOF
```

**Commit behavior:** If CITATION.cff changed, github-actions[bot] commits and pushes to `main`.

**Output:** Both root-level and collection-level CITATION.cff files now carry the versioned DOI.

---

### Stage 7: Trigger mirror-to-hf.yml (Automated via release.yml)

**Responsibility:** GitHub Actions (workflow_dispatch).

**What happens:**
```javascript
// release.yml step: "Trigger mirror-to-hf.yml"
github.rest.actions.createWorkflowDispatch({
  workflow_id: 'mirror-to-hf.yml',
  ref: 'main',
  inputs: {
    collection_slug: 'metabolomics',
    collection_version: '1'
  }
})
```

**Dispatch contract (fixed in this PR):** mirror-to-hf.yml is now **dispatch-only** — it declares `workflow_dispatch:` with inputs `{collection_slug, collection_version}` and no longer has a `push: tags` trigger. So this `createWorkflowDispatch` call is the *only* thing that starts the mirror; there is no tag double-fire.

**Pre-PR behavior (for reference):** Before this PR, mirror-to-hf.yml had NO `workflow_dispatch:` trigger, so this dispatch call **no-opped**, while mirror-to-hf.yml fired from its own `push: tags: "*-v[0-9]*"` trigger — and release.yml fired on the same tag, so the tag double-fired across the two workflows.

---

### Stage 8: Mirror to HuggingFace (Automated via mirror-to-hf.yml)

**Responsibility:** GitHub Actions (HuggingFace API).

**Secret required:** `HF_TOKEN` (HuggingFace user access token, scope: create & write datasets & spaces).

**What happens:**

#### Step 1: Parse tag to slug & version
```bash
TAG=metabolomics-v1 → SLUG=metabolomics, VERSION=1
COLLECTION_PATH=collections/metabolomics/v1
HF_REPO=HolobiomicsLab/asb-metabolomics-v1
SPACE_REPO=HolobiomicsLab/asb-metabolomics-v1-leaderboard
```

#### Step 2: Generate HF Dataset README
```bash
python scripts/generate_hf_dataset_card.py \
  --collection collections/metabolomics/v1/collection.yaml \
  --citation collections/metabolomics/v1/CITATION.cff \
  --output collections/metabolomics/v1/README_HF.md
```
Output: `README_HF.md` (markdown, suitable for HF Datasets front page).

#### Step 3: Generate HF Space leaderboard config
```bash
python scripts/generate_hf_space_config.py \
  --collection collections/metabolomics/v1/collection.yaml \
  --leaderboard-url https://raw.githubusercontent.com/HolobiomicsLab/asb-skill-collections/main/collections/metabolomics/v1/benchmark/leaderboard.jsonld \
  --output collections/metabolomics/v1/.hf-space/
```
Output: `.hf-space/` directory with `app.py` (Streamlit), `requirements.txt`, etc.

#### Step 4: Upload collection to HF Datasets (fail-soft)
```bash
env HF_STEP=upload_dataset python scripts/mirror_to_hf.py
```

**Behavior:**
```
IF HF_TOKEN not set:
  → Log warning and skip (fail-soft; does not block)

ELSE:
  → Create dataset repo: HolobiomicsLab/asb-metabolomics-v1
  → Push README_HF.md as the dataset card
  → Push collection files (skills, tools, benchmarks, reviews)
  → Set visibility to public
```

#### Step 5: Create/update HF Space leaderboard (fail-soft)
```bash
env HF_STEP=upload_space python scripts/mirror_to_hf.py
```

**Behavior:**
```
IF HF_TOKEN not set:
  → Log warning and skip

ELSE:
  → Create Space repo: HolobiomicsLab/asb-metabolomics-v1-leaderboard
  → Push .hf-space/ files
  → HF auto-deploys Streamlit app from app.py
  → Space becomes public & linked from Dataset page
```

**TODO:** Obtain a real `HF_TOKEN` from https://huggingface.co/settings/tokens and add to GitHub secrets before the first release.

---

## 2. Indicium co-release pinning

**Context:** indicium (claim/evidence schema) is released in sync with ASB and the skill-collections. They share the same preprint and the same ~monthly release cadence.

**What this means for the release train:**

1. **Before tagging a collection**, check the indicium version pinned in the release/profile.
   - Lookup: `agenticsciencebuilder_dev/docs/asbb/RELEASE.yaml` (not yet finalized; assume it exists and carries `indicium_version: <tag>`)
   - Or, look at the pinned version in the AgenticScienceBuilder codebase (e.g., `setup.py` or `pyproject.toml`).

2. **At Zenodo deposit time**, attach the indicium version as a metadata file:
   - Create `indicium_version.txt` containing the tag (e.g., `v1.11.0`) or full version identifier
   - Include it in the zipped collection
   - This makes the pin publicly discoverable

3. **If indicium is released AFTER the collection tag**, update the collection CITATION.cff manually and push a patch commit (e.g., `git commit -m "chore: pin indicium to <tag>"`) before the Zenodo step runs.
   - v0 guidance: keep releases close together; synchronize tags within 24 hours.

4. **Breaking change policy:** If a new major version of indicium ships before your release:
   - Rebase collection against the new indicium
   - Re-tag with a new version (e.g., `metabolomics-v1.1` if it's a patch, or `metabolomics-v2` if it's a major bump)
   - Document the change in CHANGELOG.md

---

## 3. Self-merge waiver (v0 governance)

**v0 governance decision (LOCKED 2026-06-14):**

The release-gate reviews (gates 13, 14 in the SPEC: independent co-reviewer and >=20 external reviews) are **FORMALLY WAIVED** for v0. The lead maintainer has sole authority and **may self-merge all PRs**, including those they authored.

**Recorded waiver:** See `CONTENT_POLICY.md` (or equivalent governance doc) for the formal logging.

**Implication for the release train:**
- No additional PR review beyond the automated CI gates is required before promotion or tagging.
- The lead maintainer is the sole gatekeeper for v0.
- v1 will reintroduce gates 13 (independent co-reviewer) and 14 (>=20 external reviews).

---

## 4. CI gates (v0 coverage)

**Implemented gates** (validate.yml + release.yml):

| Gate | Description | Trigger | Automated | Blocking |
|---|---|---|---|---|
| 1 | LinkML schema validation (collection.yaml, tools/*.yaml) | PR, push-main, tag | ✓ | ✓ |
| 2 | No orphan skills (DOI resolution sample) | PR, push-main, tag | ✓ | ✓ |
| 5 | Description discipline lint | PR, push-main, tag | ✓ | ✓ |
| 6 | EDAM IRI resolution | PR, push-main, tag | ✓ | ✓ |
| 8 | RO-Crate validation (Workflow Run Profile 0.5) | PR, push-main, tag | ✓ | ✓ |
| 9 | indicium round-trip (verify-claims CLI) | PR, push-main, tag | ✓ | warn-only (indicium-adapters not yet on PyPI) |
| 10 | Plugin manifest validation (.claude-plugin/marketplace.json) | PR, push-main, tag | ✓ | ✓ |
| 3, 4, 7 | PII/dual-use gate (FAIL on clinical IDs, WARN else) | TBD | ✗ | n/a |
| 11 | License compliance (TDM audit) | TBD | ✗ | n/a |
| 12 | Consensus review tally | TBD | ✗ | n/a |
| 13 | Independent co-reviewer | TBD | ✗ | **WAIVED v0** |
| 14 | >=20 external reviews | TBD | ✗ | **WAIVED v0** |

**Not yet automated (v0 limitations):**
- Gates 3, 4, 7 (PII/dual-use) require human review in release.yml; advisory only for now
- Gates 11, 12 (license, consensus) deferred to v1
- Gates 13, 14 (governance gates) waived for v0

---

## 5. Required secrets & environment setup

### GitHub secrets (repo settings > Secrets and variables > Actions)

**For release.yml:**
- `ZENODO_TOKEN` — Zenodo personal access token (fail-soft: no token = skip upload)
  - Obtain from: https://zenodo.org/account/settings/applications/
  - Scopes: `write:deposit`, `publish:deposit`
  - Status: **TODO** — not yet set (placeholder/sandbox mode)

**For mirror-to-hf.yml:**
- `HF_TOKEN` — HuggingFace user access token (fail-soft: no token = skip upload)
  - Obtain from: https://huggingface.co/settings/tokens
  - Scopes: `repo` (write access to datasets & spaces)
  - Status: **Partially set** — works for public mirrors (verify on first release)

### Local environment (for manual validation)

```bash
# Clone the repo
git clone https://github.com/HolobiomicsLab/asb-skill-collections
cd asb-skill-collections

# Install dev dependencies
pip install -e ".[test]"

# Run validate.yml gates locally (before tagging)
pytest tests/ -v

# Regenerate catalogue locally (optional, release.yml does this)
python scripts/regen_catalogue.py --repo-root . --output catalogue.jsonld
```

---

## 6. Linear workflow diagram

```
┌──────────────────────────────────────────────────────────────────────────┐
│ PRE-RELEASE: Contribution cycle (in staged-collections/, any contributor │
│ Main step: open PR, CI validates via validate.yml, lead maintainer merges)
└──────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ STAGE 0: Authoring                                                       │
│ Location: staged-collections/<slug>/v<N>/                              │
│ No CI gates; review happens in GitHub PRs                              │
└──────────────────────────────────────────────────────────────────────────┘
                                    │
         ┌──────────────────────────┘
         │ [Lead maintainer action]
         │ Promote to collections/
         │
         ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ STAGE 1: Promotion                                                       │
│ Location: collections/<slug>/v<N>/                                     │
│ CI gates: validate.yml (gates 1, 2, 5, 6, 8, 9, 10) on push-main    │
│ Status: ready for release tag                                          │
└──────────────────────────────────────────────────────────────────────────┘
                                    │
         ┌──────────────────────────┘
         │ [Lead maintainer action]
         │ git tag <slug>-v<N> main
         │ git push origin <slug>-v<N>
         │
         ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ STAGE 2: Release tagging                                                │
│ Tag format: <slug>-v<N> (strict)                                       │
│ Trigger: release.yml on push:tags. mirror-to-hf.yml is dispatch-only   │
│ (no tag trigger) — driven by release.yml's workflow_dispatch.          │
└──────────────────────────────────────────────────────────────────────────┘
                        │
                        ▼
    ┌────────────────┐
    │ release.yml    │   (only workflow on the tag)
    │ (auto)         │
    ├─ pytest gates
    ├─ regen_catalogue.jsonld
    ├─ Zenodo upload (fail-soft, ONE concept-DOI)
    ├─ Update CITATION.cff
    └─ workflow_dispatch ──────────► ┌───────────────────────────────┐
    └────────────────┘               │ mirror-to-hf.yml              │
                                     │ (dispatch-only, no tag trigger)│
                                     ├─ Generate HF Dataset README   │
                                     ├─ Generate HF Space config     │
                                     ├─ Upload to HF Datasets (soft) │
                                     └─ Create/update HF Space       │
                                     └───────────────────────────────┘
                        │ [Both complete]
                        │
                        ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ POST-RELEASE: Verification                                              │
│ [Human action] Verify:                                                  │
│   ✓ Zenodo DOI appears in CITATION.cff                                 │
│   ✓ HuggingFace Dataset: HolobiomicsLab/asb-<slug>-v<N>               │
│   ✓ HuggingFace Space: HolobiomicsLab/asb-<slug>-v<N>-leaderboard    │
│   ✓ catalogue.jsonld updated on main                                   │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Troubleshooting

### Release.yml fails at pytest stage

**Symptom:** Tag is pushed but release.yml workflow shows "FAILED" and no Zenodo upload happens.

**Diagnosis:**
```bash
# Check the failing test
cd asb-skill-collections
git checkout <tag>
pytest tests/ -v
```

**Fix:**
1. Commit fixes to `collections/<slug>/v<N>/` on main
2. Optionally re-tag (delete old tag, create new one) if the fix is critical
3. Or wait for next release cycle

### Zenodo upload is skipped

**Symptom:** release.yml step "Upload to Zenodo (fail-soft if token missing)" succeeds with message "ZENODO_TOKEN not set — skipping Zenodo upload".

**Diagnosis:** `ZENODO_TOKEN` is not set in GitHub secrets.

**Fix:**
1. Obtain token from https://zenodo.org/account/settings/applications/ (create new token with `write:deposit`, `publish:deposit` scopes)
2. Add to GitHub repo settings: **Settings > Secrets and variables > Actions > New repository secret**
   - Name: `ZENODO_TOKEN`
   - Value: (paste token)
3. Re-run release.yml: either re-tag the collection or manually trigger the workflow

### HuggingFace mirror fails

**Symptom:** mirror-to-hf.yml step "Upload collection to HF Datasets" fails with "HF_TOKEN not set" or auth error.

**Diagnosis:** `HF_TOKEN` missing or invalid.

**Fix:**
1. Obtain token from https://huggingface.co/settings/tokens (User Access Token, `repo` scope)
2. Add to GitHub secrets (same as ZENODO_TOKEN)
3. Re-run mirror-to-hf.yml manually or re-tag

### Double-fire of mirror-to-hf.yml (resolved in this PR)

**Symptom (pre-PR):** The tag double-fires — release.yml runs on the tag, and mirror-to-hf.yml ALSO ran on the same tag via its own `push: tags` trigger, while release.yml's `createWorkflowDispatch` to mirror-to-hf.yml silently no-opped (mirror-to-hf.yml had no `workflow_dispatch:` trigger to receive it).

**Fix (this PR):** mirror-to-hf.yml is now **dispatch-only**: `workflow_dispatch:` with inputs `{collection_slug, collection_version}` is added and the `push: tags` trigger is removed. release.yml's dispatch now actually drives the mirror, and the tag no longer double-fires.

**Note:** mirror_to_hf.py is still idempotent (checks if files exist on HF and skips redundant uploads), so re-runs remain safe.

---

## 8. Checklist for release day

### Pre-release (1 day before)

- [ ] Confirm collection in `collections/<slug>/v<N>/` is complete
- [ ] Run local pytest: `pytest tests/ -v` (passes)
- [ ] Review `CITATION.cff` (authors, DOIs, license)
- [ ] Check that `indicium_version` is pinned (in release manifest, if it exists)

### Release (tag push)

- [ ] Decide version: is this v1 (first), v2 (next), etc.?
- [ ] Tag: `git tag <slug>-v<N> main && git push origin <slug>-v<N>`
- [ ] Watch release.yml run in GitHub Actions (takes ~5–10 min)
- [ ] If release.yml fails, check pytest output and fix

### Post-release (1–2 hours after tag)

- [ ] Verify Zenodo record: https://zenodo.org/search?q=HolobiomicsLab (or concept-DOI from CITATION.cff)
- [ ] Verify HF Dataset: https://huggingface.co/HolobiomicsLab/asb-<slug>-v<N>
- [ ] Verify HF Space: https://huggingface.co/spaces/HolobiomicsLab/asb-<slug>-v<N>-leaderboard
- [ ] Update README.md if needed (e.g., badge with new DOI)
- [ ] Close any associated GitHub issues (e.g., "Release v<N>")

---

## 9. Known issues & v0 → v1 gaps

### v0 limitations (design intent, not bugs)

- **PII/dual-use gates (3, 4, 7):** Not automated. Manual review required before promotion. Gate enforcement deferred to v1.
- **License compliance gate (11):** Not automated. TDM audit deferred to v1.
- **Governance gates (13, 14):** Waived for v0 (self-merge allowed). v1 will require independent co-reviewer + >=20 external reviews.
- **indicium co-release pinning:** Manual process (check version in release manifest). v1 will automate via shared release.yaml.

### Known bugs (to fix before v1)

- **Mirror-to-hf.yml double-fire (FIXED in this PR):** Previously release.yml fired on the tag and mirror-to-hf.yml ALSO fired on the same tag, while release.yml's `workflow_dispatch` to mirror-to-hf.yml no-opped (no `workflow_dispatch:` trigger existed to receive it).
  - **Fix (this PR):** mirror-to-hf.yml is dispatch-only — `workflow_dispatch:` with inputs `{collection_slug, collection_version}` added; `push: tags` trigger removed. release.yml's dispatch now drives the mirror; no double-fire.
  - HF uploads remain idempotent as defense-in-depth.
- **ZENODO_TOKEN missing:** Zenodo uploads fail silently. No warning in main workflow summary.
  - **Workaround (v0):** Check release.yml logs manually.
  - **Fix (v1):** Add explicit workflow step to validate token at start.

---

## 10. References

- **Release workflow:** `.github/workflows/release.yml`
- **Mirror workflow:** `.github/workflows/mirror-to-hf.yml`
- **Validation workflow:** `.github/workflows/validate.yml`
- **Contributing guide:** `CONTRIBUTING.md`
- **Maintainers guide:** `MAINTAINERS.md`
- **COI policy:** `COI_POLICY.md`
- **ASB specification:** `/Users/nothiasl/git/agenticsciencebuilder_dev/docs/asbb/SPEC.md`
- **Zenodo API docs:** https://developers.zenodo.org/
- **HuggingFace API docs:** https://huggingface.co/docs/hub/api

---

## 11. Human-gated steps & TODOs

The following require real input before the first release:

### TODO: ZENODO_TOKEN

- **Status:** Placeholder ("PLACEHOLDER DOI" in badges)
- **What to do:**
  1. Go to https://zenodo.org/account/settings/applications/
  2. Create a new token with name "asb-skill-collections" and scopes `write:deposit`, `publish:deposit`
  3. Copy the token
  4. Go to https://github.com/HolobiomicsLab/asb-skill-collections/settings/secrets/actions
  5. Create a new secret named `ZENODO_TOKEN` and paste the token
- **When:** Before first release tag
- **Owned by:** Lead maintainer (Louis-Felix Nothias)

### TODO: HF_TOKEN verification

- **Status:** Likely set but not verified on this project yet
- **What to do:**
  1. Confirm `HF_TOKEN` is set in GitHub secrets (ask repo admin)
  2. On first release, watch mirror-to-hf.yml logs to confirm dataset upload succeeds
  3. If auth fails, obtain a new token from https://huggingface.co/settings/tokens
- **When:** Before first release tag (or on first release, fix immediately after)
- **Owned by:** Lead maintainer

### TODO: Real ORCID for lead maintainer

- **Current:** Placeholder "0000-0002-XXXX-XXXX" in MAINTAINERS.md and marketplace.json
- **What to do:**
  1. Confirm real ORCID (https://orcid.org/)
  2. Update:
     - `MAINTAINERS.md` (profile section)
     - `.claude-plugin/marketplace.json` (publisher.orcid_org)
     - Any CITATION.cff files with author blocks
- **When:** Before Wave 4 (likely before or concurrent with first release)
- **Owned by:** Lead maintainer (Louis-Felix Nothias, louisfelix.nothias@gmail.com)

### TODO: Author/CRediT list for collection

- **Status:** Per-collection-release, declared in CITATION.cff
- **What to do:**
  1. For each collection release, populate `authors` array in collections/<slug>/v<N>/CITATION.cff with:
     - given-names, family-names
     - orcid (optional but encouraged)
     - role (optional, from CRediT taxonomy if desired)
  2. Example:
     ```yaml
     authors:
       - given-names: Louis-Félix
         family-names: Nothias
         orcid: "0000-0002-XXXX-XXXX"
         role: curator
     ```
- **When:** Before tagging each release
- **Owned by:** Lead Curator (per collection)

### TODO: Corpus DOIs

- **Status:** Each collection may reference an `asb-corpus-<domain>` repository (not yet created)
- **What to do:**
  1. If a corpus repo exists (e.g., asb-corpus-metabolomics), mint a Zenodo concept-DOI for it
  2. Link the corpus DOI in collection metadata (e.g., CITATION.cff `references` section)
  3. Attach the corpus as a file to the collection's Zenodo deposition (optional but recommended)
- **When:** If/when corpus repos are published; deferred to v1 for most domains
- **Owned by:** Lead Curator + Zenodo admin

### TODO: indicium version pinning

- **Status:** Currently manual; check release manifest before tagging
- **What to do:**
  1. Before tagging a collection, verify indicium version in the pinned release manifest
  2. If indicium has a new version, ensure the collection is compatible (run verify-claims)
  3. Optionally add indicium version to collection CITATION.cff references
- **When:** Concurrent with each collection release
- **Owned by:** Lead maintainer (coordinate with indicium maintainers)

---

**Version:** 0.1 · **Last updated:** 2026-06-14 · **Status:** FINAL for v0 releases
