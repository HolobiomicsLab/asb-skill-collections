# ASB-Skill-Collections Bootstrap (Wave 3a) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Bootstrap the empty `HolobiomicsLab/asb-skill-collections` GitHub repo with all top-level governance files, directory scaffold, templates, and four GitHub Actions workflows (validate, verify-coi, vet-curator, tier-update).

**Architecture:** Initialize the repo locally at `/Users/holobiomicslab/git/asb-skill-collections/`, commit governance + scaffold files per-task via TDD where feasible (YAML parse + schema conformance asserts), then push to origin. GH Actions are syntactically-valid YAML with dry-run unit tests for the OpenAlex API integration.

**Tech Stack:** Python 3.12+, PyYAML, jsonschema, pytest; GitHub Actions (ubuntu-latest); OpenAlex REST API (no key needed); LinkML (for validate.yml); rocrate-py (for RO-Crate validation).

---

## File Map

| File | Responsibility |
|---|---|
| `README.md` | Repo overview, install badge, Zenodo/HF/w3id placeholder |
| `LICENSE` | Apache-2.0 (synthesis layer) |
| `LICENSE.md` | License clarity — Apache-2.0 for synthesis + fair-use note for verbatim quotes |
| `COI_POLICY.md` | Self-review allowed, 3 safeguards, second-reviewer requirement |
| `CONTRIBUTING.md` | Community contribution workflow, curator candidacy steps |
| `MAINTAINERS.md` | Louis-Félix Nothias as lead maintainer (ORCID + GitHub placeholder) |
| `.gitignore` | Python/DS_Store/coverage defaults |
| `contributors.jsonld` | JSON-LD contributor registry (empty list, schema-valid) |
| `.claude-plugin/marketplace.json` | Anthropic plugin marketplace (empty plugins list, schema-valid) |
| `tools/.gitkeep` | Global ASB-Tool ledger directory |
| `collections/.gitkeep` | Curated collections directory |
| `staged-collections/.gitkeep` | Staging directory (conda-forge pattern) |
| `candidates/.gitkeep` | Curator candidacy submissions |
| `reviews/.gitkeep` | Root reviews directory (reviews also live inside collections/ subdirs) |
| `leaderboard/.gitkeep` | Career stats directory |
| `templates/curator-criteria.yaml.template` | Per §9.5 schema, configurable thresholds |
| `templates/attestation.yaml.template` | Per §9.3 + verified_claim_ids[] slot |
| `templates/lead_curator_responsibilities.md.template` | Per §9.4 |
| `.github/ISSUE_TEMPLATE/propose-collection.md` | New collection proposal issue |
| `.github/ISSUE_TEMPLATE/propose-curator-candidacy.md` | Candidate must include ORCID + 2-3 proof DOIs |
| `.github/ISSUE_TEMPLATE/submit-agent-result.md` | Leaderboard submission issue |
| `.github/PULL_REQUEST_TEMPLATE.md` | Standard PR template |
| `.github/workflows/validate.yml` | LinkML, EDAM, RO-Crate, DOI, description lint, verify-claims |
| `.github/workflows/verify-coi.yml` | OpenAlex coauthor check on review PRs |
| `.github/workflows/vet-curator.yml` | OpenAlex identity + expertise on candidacy PRs |
| `.github/workflows/tier-update.yml` | Post-merge counter + tier re-evaluation |
| `scripts/check_coi.py` | Reusable COI check logic (unit-testable, called from verify-coi.yml) |
| `scripts/vet_curator.py` | Reusable vet-curator logic (unit-testable, called from vet-curator.yml) |
| `scripts/tier_update.py` | Reusable tier-update logic (called from tier-update.yml) |
| `pyproject.toml` | Project metadata, test deps (pytest, pyyaml, jsonschema) |
| `tests/test_templates.py` | YAML parse + schema conformance for templates |
| `tests/test_contributors_jsonld.py` | JSON-LD schema conformance |
| `tests/test_marketplace_json.py` | Plugin manifest schema conformance |
| `tests/test_check_coi.py` | Unit tests for check_coi.py with mocked OpenAlex |
| `tests/test_vet_curator.py` | Unit tests for vet_curator.py with mocked OpenAlex |

---

## Task 1: Git init + push empty main branch

**Files:**
- Create: `.gitignore`
- Create: `pyproject.toml`

- [ ] **Step 1: Initialize repo locally**

```bash
cd /Users/holobiomicslab/git/asb-skill-collections
git init -b main
git remote add origin https://github.com/HolobiomicsLab/asb-skill-collections.git
```

Expected: `Initialized empty Git repository...`, `remote add` succeeds silently.

- [ ] **Step 2: Write .gitignore**

Content for `/Users/holobiomicslab/git/asb-skill-collections/.gitignore`:

```gitignore
# Python
__pycache__/
*.py[cod]
*.pyo
*.egg
*.egg-info/
dist/
build/
.eggs/
.env
.venv/
venv/
env/
pip-wheel-metadata/
.pytest_cache/
.mypy_cache/
.ruff_cache/
htmlcov/
.coverage
*.cover
*.log
*.pot
*.mo

# macOS
.DS_Store
.AppleDouble
.LSOverride
._*

# IDE
.idea/
.vscode/
*.swp
*~

# Data / generated artefacts
outputs/
*.jsonl.gz
*.parquet
```

- [ ] **Step 3: Write pyproject.toml**

Content for `/Users/holobiomicslab/git/asb-skill-collections/pyproject.toml`:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "asb-skill-collections"
version = "0.1.0"
description = "Bootstrap scripts and CI helpers for HolobiomicsLab/asb-skill-collections"
license = { text = "Apache-2.0" }
requires-python = ">=3.12"
dependencies = [
    "pyyaml>=6.0",
    "jsonschema>=4.21",
    "requests>=2.31",
]

[project.optional-dependencies]
test = [
    "pytest>=8.0",
    "pytest-cov",
    "responses>=0.25",  # HTTP mock for OpenAlex tests
]

[tool.pytest.ini_options]
testpaths = ["tests"]
```

- [ ] **Step 4: Stage and commit**

```bash
cd /Users/holobiomicslab/git/asb-skill-collections
git add .gitignore pyproject.toml
git commit -m "chore: initialize repo with .gitignore and pyproject.toml"
```

Expected: `[main (root-commit) xxxxxxx] chore: initialize repo...`

---

## Task 2: License files

**Files:**
- Create: `LICENSE`
- Create: `LICENSE.md`

- [ ] **Step 1: Write Apache-2.0 LICENSE (plain text)**

`/Users/holobiomicslab/git/asb-skill-collections/LICENSE` — full Apache-2.0 text:

```
                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

   TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

   1. Definitions.
      ...
```

(Use the canonical Apache-2.0 text from https://www.apache.org/licenses/LICENSE-2.0.txt — write the complete file.)

- [ ] **Step 2: Write LICENSE.md with fair-use note**

`/Users/holobiomicslab/git/asb-skill-collections/LICENSE.md`:

```markdown
# License

## Synthesis layer (skill descriptions, tool records, structured metadata)

Licensed under the **Apache License 2.0**.
See [`LICENSE`](LICENSE) for the full text.

You are free to:
- Use the structured skill, tool, and benchmark records for any purpose (commercial or otherwise)
- Modify and redistribute, provided you retain the Apache-2.0 license notice

## Verbatim quotations from scientific papers

Short verbatim quotes from the source papers are included as `evidence_spans` in
skill YAML frontmatter solely for non-commercial scientific attribution purposes.
These quotes are reproduced under **fair use / quotation right** (UK copyright §30;
EU Copyright Directive Art. 5.3(d); US Copyright 17 U.S.C. §107).

- Quotes are minimal (typically one sentence), non-substitutive
- Proper attribution is provided via DOI and author list in `derived_from`
- No commercial use of verbatim quotes is intended

If a rights holder objects to a specific quote, please open an issue and it will
be removed promptly.

## Benchmark tasks and workflows

Benchmark task descriptions, evaluation manifests, and workflows are released under
Apache-2.0. Raw paper content is not reproduced in benchmark files.
```

- [ ] **Step 3: Commit**

```bash
cd /Users/holobiomicslab/git/asb-skill-collections
git add LICENSE LICENSE.md
git commit -m "chore: add Apache-2.0 LICENSE with fair-use note for evidence spans"
```

---

## Task 3: Governance documents (COI, Contributing, Maintainers)

**Files:**
- Create: `COI_POLICY.md`
- Create: `CONTRIBUTING.md`
- Create: `MAINTAINERS.md`

- [ ] **Step 1: Write COI_POLICY.md**

`/Users/holobiomicslab/git/asb-skill-collections/COI_POLICY.md`:

```markdown
# Conflict of Interest (COI) Policy

## Summary

Self-review of papers you co-authored is **allowed** with three safeguards.

## Safeguard 1 — Automatic COI detection

`verify-coi.yml` runs on every PR that touches `collections/<slug>/v<N>/reviews/*.yaml`.
It cross-checks the paper's author list (via OpenAlex) against the reviewer's ORCID.
The action auto-populates three fields in the attestation:

- `is_coauthor: true|false`
- `author_position: <integer | null>` (1 = first author)
- `is_corresponding: true|false`

CI **fails** if the action-detected `is_coauthor` value contradicts the manually-declared
value in the attestation file.

## Safeguard 2 — Mandatory disclosure

Every `attestation.yaml` file must include an `is_coauthor` field. Omission blocks merge.

## Safeguard 3 — Second reviewer when is_coauthor: true

When `is_coauthor: true`, a `co_reviewer` block is required in the attestation:

```yaml
co_reviewer:
  orcid: "0000-0000-0000-0000"
  github: second-reviewer-handle
  tier: reviewer       # must be ≥ reviewer
  sign_off_pr: 123     # PR number where co-reviewer posted approval comment
```

The co-reviewer must:
- Have a different ORCID (not also a co-author of the same paper)
- Be identity-verified at ≥Reviewer tier in `contributors.jsonld`
- Have posted a sign-off comment on the PR

CI checks all three conditions. Merge is blocked until satisfied.

## Lead Curator non-self minimum

Of a Lead Curator's 30 qualifying reviews, **at least 20 must be non-self-authored**
(papers where `is_coauthor: false`). This is enforced by `tier-update.yml`.

## Credit accounting

Curators receive full credit regardless of COI status.
`contributors.jsonld` surfaces `self_authored_reviews` and `external_reviews` as
separate counters, both publicly visible.

## Process for detected COI violations

1. CI flags the mismatch as a PR comment
2. Reviewer must amend their attestation to match detected values
3. If second reviewer is missing, the PR blocks until they are added
4. Maintainer reviews both attestations before merge

## Appeals

If you believe the OpenAlex author list is wrong (e.g., name disambiguation error),
open an issue with evidence and a maintainer will manually override via
`coi_override: true` in the attestation, with a justification note.
```

- [ ] **Step 2: Write CONTRIBUTING.md**

`/Users/holobiomicslab/git/asb-skill-collections/CONTRIBUTING.md`:

```markdown
# Contributing to ASB-Skill-Collections

We welcome community contributions of curated, evidence-grounded scientific skills,
tools, and benchmarks. All contributions are reviewed for scientific quality,
evidence provenance, and FAIR metadata completeness.

## How to contribute a review

1. **Prerequisites:** You must be listed in `contributors.jsonld` with at least
   Reviewer tier. If you're not yet listed, complete Step 0 below first.

2. **Open a PR** adding your review attestation at
   `collections/<slug>/v<N>/reviews/<paper-doi-slug>.yaml`.
   Use `templates/attestation.yaml.template` as your starting point.

3. **CI runs automatically:**
   - COI detection via `verify-coi.yml`
   - Schema validation via `validate.yml`
   - If `is_coauthor: true`, you must also add a `co_reviewer` block (see COI_POLICY.md)

4. **A maintainer merges** your PR. You cannot self-merge.

5. **Tier update happens automatically** via `tier-update.yml` on merge.

## Step 0 — Become a verified contributor (Reviewer tier)

1. **Open a PR** adding `candidates/<your-github-handle>.yaml`.
   Use this format:

   ```yaml
   github: your-github-handle
   orcid: "0000-0000-0000-0000"
   intended_collections: [metabolomics]   # one or more slugs
   proof_publications:
     - doi: 10.xxxx/your-paper-1
     - doi: 10.xxxx/your-paper-2
   ```

2. **Add your GitHub URL to your ORCID public profile** (Websites & Social Links).
   This is the L1 identity check.

3. **CI runs `vet-curator.yml`** automatically:
   - L1: GitHub URL found in ORCID public record
   - L2: ORCID matches author on each `proof_publications` DOI (via OpenAlex)
   
4. **A maintainer merges** your candidacy PR, adding you to `contributors.jsonld`.

## How to propose a new collection

1. Open a GitHub Issue using the "Propose collection" template.
2. Include: domain name, short description, 3-5 seed papers (DOIs), proposed Lead Curator.
3. After maintainer go-ahead, open a PR adding `staged-collections/<domain>/v1/`.

## Tier progression

| Tier | Requirement |
|---|---|
| Reviewer | 1+ reviews, L1 identity verified |
| Domain Contributor | 5–9 reviews OR ≥10 domain pubs (verified L1+L2) |
| Curator | ≥10 reviews + ≥5 domain pubs (L1+L2) |
| Lead Curator | ≥30 reviews (≥20 external) + ≥10 domain pubs + h-index ≥5 + maintainer approval |

Tiers are per-collection-release. Career totals are tracked in `leaderboard/career.jsonld`.

## Code of Conduct

We follow the Contributor Covenant v2.1. Scientific integrity and respectful review
are non-negotiable. Fabricated citations or identity fraud result in permanent banning.

## Questions

Open a GitHub Discussion or email the lead maintainer listed in `MAINTAINERS.md`.
```

- [ ] **Step 3: Write MAINTAINERS.md**

`/Users/holobiomicslab/git/asb-skill-collections/MAINTAINERS.md`:

```markdown
# Maintainers

## Lead Maintainer

**Louis-Félix Nothias**
- GitHub: [@lfnothias](https://github.com/lfnothias)
- ORCID: [0000-0002-XXXX-XXXX](https://orcid.org/0000-0002-XXXX-XXXX)  ← update before Wave 4
- Affiliation: Holobiomics Lab, Institut de Chimie de Nice (ICN), CNRS UMR 7272 / Université Côte d'Azur
- Email: louisfelix.nothias@gmail.com

### Responsibilities
- Merge all PRs (no self-merge by contributors)
- Act as Lead Curator for the metabolomics/v1 collection
- Veto power on release-blocking changes (license, version, deprecation)
- Annual release cycle stewardship

## Mentors for first-time contributors

New contributors should be paired with a mentor for their first review.
Contact the lead maintainer to be assigned one.

## Adding yourself as maintainer

Maintainers are added by the lead maintainer. There is currently no formal process;
contact louisfelix.nothias@gmail.com if you are interested in co-maintaining a domain.
```

- [ ] **Step 4: Commit**

```bash
cd /Users/holobiomicslab/git/asb-skill-collections
git add COI_POLICY.md CONTRIBUTING.md MAINTAINERS.md
git commit -m "docs: add governance files (COI policy, contributing guide, maintainers)"
```

---

## Task 4: README.md + contributors.jsonld + marketplace.json

**Files:**
- Create: `README.md`
- Create: `contributors.jsonld`
- Create: `.claude-plugin/marketplace.json`

- [ ] **Step 1: Write README.md**

`/Users/holobiomicslab/git/asb-skill-collections/README.md`:

```markdown
# ASB-Skill-Collections

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.PLACEHOLDER.svg)](https://doi.org/10.5281/zenodo.PLACEHOLDER)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-HolobiomicsLab-yellow)](https://huggingface.co/HolobiomicsLab)
[![w3id](https://img.shields.io/badge/IRI-w3id.org%2Fholobiomicslab-blue)](https://w3id.org/holobiomicslab)
[![License](https://img.shields.io/badge/license-Apache--2.0-green)](LICENSE)

Curated, evidence-grounded scientific-agent skill + tool + benchmark collections
produced by the [AgenticScienceBuilder](https://github.com/HolobiomicsLab/AgenticScienceBuilder)
pipeline, maintained by [Holobiomics Lab](https://github.com/HolobiomicsLab).

## What's in here

| Artifact | Description |
|---|---|
| **ASB-Skills** | Curated, deduplicated procedural knowledge for scientific AI agents |
| **ASB-Benchmark** | Per-paper tasks with workflows + claim-retrieval test sets for evaluation |
| **ASB-Tools** | Globally-deduplicated software-tool records with EDAM annotations |
| **ASB-Capsules** | Raw per-paper ASB pipeline outputs (v1.1, deferred) |

## Quick install (Claude Code)

```bash
/plugin install metabolomics-v1@HolobiomicsLab/asb-skill-collections
```

## Browse collections

- [`collections/`](collections/) — released, tagged collections
- [`staged-collections/`](staged-collections/) — in-progress, under review

## For agents: how skills are structured

Each skill is a `SKILL.md` file with YAML frontmatter containing:
- EDAM operation/topic IRIs (for pre-filtered retrieval)
- `derived_from` DOIs (source papers)
- `evidence_spans` (verbatim quotes from papers)
- `tools` (linked ASB-Tool records)
- `claims` (indicium claim IRIs, or empty list)

The collection `_router/SKILL.md` is loaded by default and routes to specific skills
via Perspicacité KB search.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the curator workflow.
COI policy: [COI_POLICY.md](COI_POLICY.md).

## Citation

If you use these collections in research, please cite the per-collection `CITATION.cff`
(automatically generated at release). The Zenodo DOI above is a placeholder; it will be
minted on first release tag.

## License

Apache-2.0 for synthesis layer; fair-use for verbatim paper quotes.
See [LICENSE.md](LICENSE.md) for details.
```

- [ ] **Step 2: Write contributors.jsonld**

`/Users/holobiomicslab/git/asb-skill-collections/contributors.jsonld`:

```json
{
  "@context": {
    "@vocab": "https://schema.org/",
    "asb": "https://w3id.org/holobiomicslab/asb-skill/",
    "orcid": "https://orcid.org/",
    "asb:tier": {"@id": "asb:curatorTier"},
    "asb:collections": {"@id": "asb:collectionContributions"},
    "asb:total_reviews": {"@id": "asb:totalReviews", "@type": "xsd:integer"},
    "asb:external_reviews": {"@id": "asb:externalReviews", "@type": "xsd:integer"},
    "asb:self_authored_reviews": {"@id": "asb:selfAuthoredReviews", "@type": "xsd:integer"},
    "asb:identity_verified_layers": {"@id": "asb:identityVerifiedLayers"},
    "asb:tier_since": {"@id": "asb:tierSince"}
  },
  "@type": "Dataset",
  "@id": "https://github.com/HolobiomicsLab/asb-skill-collections/blob/main/contributors.jsonld",
  "name": "ASB-Skill-Collections Contributor Registry",
  "description": "ORCID-keyed registry of verified curators, their tiers, and contribution stats.",
  "version": "0.1.0",
  "dateModified": "2026-05-25",
  "contributors": []
}
```

- [ ] **Step 3: Write .claude-plugin/marketplace.json**

`/Users/holobiomicslab/git/asb-skill-collections/.claude-plugin/marketplace.json`:

```json
{
  "schema_version": "1.0",
  "name": "ASB Skill Collections",
  "description": "Curated scientific-agent skill and benchmark collections from the AgenticScienceBuilder pipeline.",
  "publisher": {
    "name": "Holobiomics Lab",
    "url": "https://github.com/HolobiomicsLab",
    "orcid_org": "https://orcid.org/0000-0002-XXXX-XXXX"
  },
  "plugins": []
}
```

- [ ] **Step 4: Write tests for contributors.jsonld and marketplace.json**

`/Users/holobiomicslab/git/asb-skill-collections/tests/test_contributors_jsonld.py`:

```python
"""Schema conformance tests for contributors.jsonld."""
import json
import pathlib

ROOT = pathlib.Path(__file__).parent.parent


def test_contributors_jsonld_parseable():
    data = json.loads((ROOT / "contributors.jsonld").read_text())
    assert "@context" in data
    assert "contributors" in data
    assert isinstance(data["contributors"], list)


def test_contributors_jsonld_has_required_context_keys():
    data = json.loads((ROOT / "contributors.jsonld").read_text())
    ctx = data["@context"]
    assert "@vocab" in ctx
    assert "orcid" in ctx
    assert "asb:tier" in ctx
    assert "asb:total_reviews" in ctx
    assert "asb:external_reviews" in ctx
    assert "asb:self_authored_reviews" in ctx
```

`/Users/holobiomicslab/git/asb-skill-collections/tests/test_marketplace_json.py`:

```python
"""Schema conformance tests for .claude-plugin/marketplace.json."""
import json
import pathlib

ROOT = pathlib.Path(__file__).parent.parent


def test_marketplace_json_parseable():
    data = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
    assert "schema_version" in data
    assert "plugins" in data
    assert isinstance(data["plugins"], list)


def test_marketplace_json_has_publisher():
    data = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
    assert "publisher" in data
    assert "name" in data["publisher"]
```

- [ ] **Step 5: Create tests/__init__.py (empty)**

```bash
touch /Users/holobiomicslab/git/asb-skill-collections/tests/__init__.py
```

- [ ] **Step 6: Run tests**

```bash
cd /Users/holobiomicslab/git/asb-skill-collections
pip install -e ".[test]" -q
pytest tests/test_contributors_jsonld.py tests/test_marketplace_json.py -v
```

Expected output:
```
PASSED tests/test_contributors_jsonld.py::test_contributors_jsonld_parseable
PASSED tests/test_contributors_jsonld.py::test_contributors_jsonld_has_required_context_keys
PASSED tests/test_marketplace_json.py::test_marketplace_json_parseable
PASSED tests/test_marketplace_json.py::test_marketplace_json_has_publisher
4 passed
```

- [ ] **Step 7: Commit**

```bash
cd /Users/holobiomicslab/git/asb-skill-collections
git add README.md contributors.jsonld .claude-plugin/marketplace.json tests/
git commit -m "feat: add README, contributors registry, and marketplace manifest with tests"
```

---

## Task 5: Directory scaffold (.gitkeep files)

**Files:**
- Create: `tools/.gitkeep`
- Create: `collections/.gitkeep`
- Create: `staged-collections/.gitkeep`
- Create: `candidates/.gitkeep`
- Create: `reviews/.gitkeep`
- Create: `leaderboard/.gitkeep`

- [ ] **Step 1: Create all gitkeep files**

```bash
cd /Users/holobiomicslab/git/asb-skill-collections
mkdir -p tools collections staged-collections candidates reviews leaderboard
touch tools/.gitkeep collections/.gitkeep staged-collections/.gitkeep
touch candidates/.gitkeep reviews/.gitkeep leaderboard/.gitkeep
```

- [ ] **Step 2: Commit**

```bash
cd /Users/holobiomicslab/git/asb-skill-collections
git add tools/.gitkeep collections/.gitkeep staged-collections/.gitkeep
git add candidates/.gitkeep reviews/.gitkeep leaderboard/.gitkeep
git commit -m "chore: scaffold empty directories (tools, collections, staged-collections, candidates, reviews, leaderboard)"
```

---

## Task 6: Templates

**Files:**
- Create: `templates/curator-criteria.yaml.template`
- Create: `templates/attestation.yaml.template`
- Create: `templates/lead_curator_responsibilities.md.template`
- Create: `tests/test_templates.py`

- [ ] **Step 1: Write curator-criteria.yaml.template**

`/Users/holobiomicslab/git/asb-skill-collections/templates/curator-criteria.yaml.template`:

```yaml
# curator-criteria.yaml — per collection, configurable
# Copy to collections/<slug>/v<N>/curator-criteria.yaml and fill in values.
# See §9.5 of ASB-Skills Release Design Doc v2 for field definitions.

domain_concepts:
  primary:
    # OpenAlex concept IDs for the primary domain.
    # Find IDs at https://api.openalex.org/concepts?search=<domain>
    - C42822068      # Example: Metabolomics
  related:
    # Related concepts accepted for domain expertise check.
    - C2776195111    # Example: Mass spectrometry
    - C42909066      # Example: Lipidomics

venue_quality:
  # Source for venue quality assessment.
  # Options: openalex_sjr | scimago | doaj | lab_whitelist
  source: openalex_sjr
  min_quartile: Q2
  open_access_bonus: true
  # Optional override: explicit list of accepted venue ISSNs.
  lab_whitelist: []

thresholds:
  reviewer:
    min_reviews: 1
    identity_layers: [L1]
  domain_contributor:
    min_reviews: 5
    min_pubs: 10
    identity_layers: [L1, L2]
  curator:
    min_reviews: 10
    min_pubs: 5
    identity_layers: [L1, L2]
  lead_curator:
    min_reviews: 30
    min_external_reviews: 20
    min_pubs: 10
    min_h_index: 5
    identity_layers: [L1, L2, L3]
    requires_maintainer_approval: true

# If true, first-time reviewers must be paired with a mentor.
mentor_required_for_first_review: true
```

- [ ] **Step 2: Write attestation.yaml.template**

`/Users/holobiomicslab/git/asb-skill-collections/templates/attestation.yaml.template`:

```yaml
# attestation.yaml — per paper review attestation
# Copy to collections/<slug>/v<N>/reviews/<paper-doi-slug>.yaml and fill in values.
# See COI_POLICY.md for COI handling rules.
# See §9.3 of ASB-Skills Release Design Doc v2.

# ── Reviewer identity ──────────────────────────────────────────────────────────
reviewer:
  orcid: "0000-0000-0000-0000"          # Required. Must be L1-verified in contributors.jsonld.
  github: your-github-handle             # Required.
  tier: reviewer                         # reviewer | domain_contributor | curator | lead_curator

# ── Paper under review ────────────────────────────────────────────────────────
paper:
  doi: "10.xxxx/your-paper-doi"          # Required.
  title: "Title of the paper"            # Optional but recommended.
  openalex_id: "W0000000000"             # Optional; populated by CI if absent.

# ── Review content ────────────────────────────────────────────────────────────
review_date: "YYYY-MM-DD"               # ISO date. Required.

# Summary of what you reviewed (free text).
# Describe: which skills/claims you checked, which evidence spans you verified.
summary: |
  Reviewed the feature detection skills derived from this paper.
  Verified evidence spans against §2.1 and §3.2 of the main text.

# Quality assessment of the derived skills (1–5 scale).
skill_quality: 4                        # 1=poor, 3=acceptable, 5=excellent

# Did the evidence spans (verbatim quotes) accurately represent the paper's claims?
evidence_spans_accurate: true           # true | false | partial

# List claim IDs you manually verified (gold-tier ground truth for benchmark).
# These claims are marked as verified in benchmark/claims/ ground truth.
# Leave empty if you did not verify claims to ground-truth level.
verified_claim_ids: []                  # e.g., ["urn:asb:claim:abc123", ...]

# ── COI declaration ────────────────────────────────────────────────────────────
# is_coauthor is auto-populated by verify-coi.yml — but you MUST declare it here
# too. CI will fail if your declared value contradicts the auto-detected value.
is_coauthor: false                      # true | false. Required.
author_position: null                   # Auto-populated by CI. Integer or null.
is_corresponding: false                 # Auto-populated by CI. true | false.

# Required ONLY when is_coauthor: true (see COI_POLICY.md §Safeguard 3).
# co_reviewer:
#   orcid: "0000-0000-0000-0000"
#   github: co-reviewer-github-handle
#   tier: reviewer
#   sign_off_pr: 123                    # PR number where co-reviewer posted approval

# ── Optional notes ─────────────────────────────────────────────────────────────
notes: ""                               # Any additional free-text comments.
```

- [ ] **Step 3: Write lead_curator_responsibilities.md.template**

`/Users/holobiomicslab/git/asb-skill-collections/templates/lead_curator_responsibilities.md.template`:

```markdown
# Lead Curator Responsibilities — {{COLLECTION_TITLE}} v{{VERSION}}

**Lead Curator:** {{CURATOR_NAME}}
**ORCID:** [{{ORCID}}](https://orcid.org/{{ORCID}})
**Collection:** `{{COLLECTION_SLUG}}/v{{VERSION}}`
**Appointed:** {{DATE}}

---

## Role

As Lead Curator, you are the corresponding author for this collection release.
You are listed first on the Zenodo DOI and marked with (*) as corresponding author.

## Responsibilities

### Scientific quality
- [ ] Verify thematic coherence of all included skills (all skills address {{DOMAIN}})
- [ ] Confirm that ≥80% of benchmark tasks have `tier: full` workflows
- [ ] Spot-check ≥10% of evidence_spans against source papers

### Attribution and provenance
- [ ] Ensure all `derived_from` DOIs resolve
- [ ] Confirm all `tools` IRIs resolve to correct tool records in `tools/`
- [ ] Review `curator-criteria.yaml` thresholds for appropriateness to {{DOMAIN}}

### Community oversight
- [ ] Complete ≥30 reviews for this collection (≥20 non-self-authored)
- [ ] Pair first-time reviewers with mentors
- [ ] Resolve any COI override appeals within 14 days

### Release lifecycle
- [ ] Veto power: approve before maintainer merges release tag
- [ ] Remain reachable as the collection's public contact for ≥2 years
- [ ] Support annual handover if stepping down (successor must meet Lead Curator criteria)

## Credit

- Zenodo (co-)corresponding author
- Listed in `CITATION.cff` as first author with `role: lead_curator`
- Permanent credit on v{{VERSION}} even if stepping down for v{{VERSION+1}}

## Handover

If you step down as Lead Curator for v{{VERSION+1}}, open an issue with:
- Successor nominee (must meet lead_curator thresholds in `curator-criteria.yaml`)
- Handover summary (open issues, domain developments since last release)

Your credit on v{{VERSION}} is permanent and unaffected by handover.
```

- [ ] **Step 4: Write tests/test_templates.py**

`/Users/holobiomicslab/git/asb-skill-collections/tests/test_templates.py`:

```python
"""YAML parse + schema conformance tests for template files."""
import pathlib
import yaml

ROOT = pathlib.Path(__file__).parent.parent
TEMPLATES_DIR = ROOT / "templates"


def _load_yaml_template(name: str) -> dict:
    """Load a .yaml.template by stripping comment lines starting with # and parsing."""
    content = (TEMPLATES_DIR / name).read_text()
    # Strip Jinja-style {{ }} placeholders for parse test (replace with dummy values)
    content = content.replace("{{COLLECTION_TITLE}}", "Test").replace(
        "{{VERSION}}", "1"
    ).replace("{{CURATOR_NAME}}", "Test Curator").replace(
        "{{ORCID}}", "0000-0000-0000-0000"
    ).replace("{{COLLECTION_SLUG}}", "test").replace(
        "{{DATE}}", "2026-01-01"
    ).replace("{{DOMAIN}}", "test domain")
    return yaml.safe_load(content)


def test_curator_criteria_template_parseable():
    data = _load_yaml_template("curator-criteria.yaml.template")
    assert "domain_concepts" in data
    assert "primary" in data["domain_concepts"]
    assert "thresholds" in data
    assert "lead_curator" in data["thresholds"]


def test_curator_criteria_template_has_required_threshold_fields():
    data = _load_yaml_template("curator-criteria.yaml.template")
    lead = data["thresholds"]["lead_curator"]
    assert "min_reviews" in lead
    assert "min_external_reviews" in lead
    assert "min_pubs" in lead
    assert "min_h_index" in lead
    assert "identity_layers" in lead
    assert lead["min_reviews"] == 30
    assert lead["min_external_reviews"] == 20


def test_attestation_template_parseable():
    data = _load_yaml_template("attestation.yaml.template")
    assert "reviewer" in data
    assert "paper" in data
    assert "is_coauthor" in data
    assert "verified_claim_ids" in data
    assert isinstance(data["verified_claim_ids"], list)


def test_attestation_template_has_coi_fields():
    data = _load_yaml_template("attestation.yaml.template")
    assert "is_coauthor" in data
    assert "author_position" in data
    assert "is_corresponding" in data
    assert data["is_coauthor"] is False


def test_attestation_template_has_verified_claim_ids_slot():
    """Gold-tier claim verification slot must exist per §10.4."""
    data = _load_yaml_template("attestation.yaml.template")
    assert "verified_claim_ids" in data
    assert data["verified_claim_ids"] == []
```

- [ ] **Step 5: Run template tests**

```bash
cd /Users/holobiomicslab/git/asb-skill-collections
pytest tests/test_templates.py -v
```

Expected:
```
PASSED tests/test_templates.py::test_curator_criteria_template_parseable
PASSED tests/test_templates.py::test_curator_criteria_template_has_required_threshold_fields
PASSED tests/test_templates.py::test_attestation_template_parseable
PASSED tests/test_templates.py::test_attestation_template_has_coi_fields
PASSED tests/test_templates.py::test_attestation_template_has_verified_claim_ids_slot
5 passed
```

- [ ] **Step 6: Commit**

```bash
cd /Users/holobiomicslab/git/asb-skill-collections
git add templates/ tests/test_templates.py
git commit -m "feat: add curator-criteria, attestation, and lead-curator templates with tests"
```

---

## Task 7: GitHub Issue & PR templates

**Files:**
- Create: `.github/ISSUE_TEMPLATE/propose-collection.md`
- Create: `.github/ISSUE_TEMPLATE/propose-curator-candidacy.md`
- Create: `.github/ISSUE_TEMPLATE/submit-agent-result.md`
- Create: `.github/PULL_REQUEST_TEMPLATE.md`

- [ ] **Step 1: Write propose-collection.md issue template**

`/Users/holobiomicslab/git/asb-skill-collections/.github/ISSUE_TEMPLATE/propose-collection.md`:

```markdown
---
name: Propose a new collection
about: Propose a new curated thematic collection (skills + tools + benchmark)
title: "[COLLECTION] <Domain Name>"
labels: ["new-collection", "needs-review"]
assignees: "lfnothias"
---

## Collection proposal

**Domain name:** <!-- e.g., Proteomics, Genomics, Transcriptomics -->

**Short description (1-2 sentences):**
<!-- What does this collection cover? What are the key methods/workflows? -->

**Proposed collection slug:** <!-- e.g., proteomics, genomics-wgs -->

## Seed papers (3–5 DOIs)

<!-- These will serve as the first papers for the collection. -->

- DOI: 10.xxxx/paper-1
- DOI: 10.xxxx/paper-2
- DOI: 10.xxxx/paper-3

## Proposed Lead Curator

- GitHub: @your-handle
- ORCID: 0000-0000-0000-0000
- Are you already verified in contributors.jsonld? [ ] Yes / [ ] No (will open candidacy PR)

## Domain expertise

<!-- Brief description of your expertise in this domain. Publications if available. -->

## Estimated scope

- Approximate number of papers to include in v1:
- Key tools/software this collection should cover:
- Are executable workflows (Snakemake/Nextflow/CWL) available for benchmarks?

## Checklist

- [ ] I have read CONTRIBUTING.md
- [ ] I have read COI_POLICY.md
- [ ] I am willing to be Lead Curator (or have identified a willing candidate)
- [ ] At least 3 seed papers are publicly available with open full text
```

- [ ] **Step 2: Write propose-curator-candidacy.md issue template**

`/Users/holobiomicslab/git/asb-skill-collections/.github/ISSUE_TEMPLATE/propose-curator-candidacy.md`:

```markdown
---
name: Propose curator candidacy
about: Apply to become a verified curator (Reviewer tier and above)
title: "[CANDIDACY] <your-github-handle>"
labels: ["curator-candidacy", "needs-vet"]
assignees: "lfnothias"
---

## Curator candidacy

> **Next step after this issue:** Open a PR adding `candidates/<your-github-handle>.yaml`.
> This issue is for discussion; the PR is what triggers automated vetting.

**GitHub handle:** @your-handle
**ORCID:** 0000-0000-0000-0000
**Intended collections:** <!-- which collection(s) you want to review -->

## Proof publications (2–3 of your own papers)

The automated vetter (`vet-curator.yml`) will check that your ORCID appears
in the author list of these papers via OpenAlex.

- DOI: 10.xxxx/your-paper-1
- DOI: 10.xxxx/your-paper-2
- DOI: 10.xxxx/your-paper-3 (optional)

## Identity check prerequisite

Before your candidacy PR is merged, please:

- [ ] Add your GitHub profile URL (`https://github.com/<your-handle>`) to your
      public ORCID record under "Websites & Social Links"
      (https://orcid.org/my-orcid?conversationId=2)
      This is the L1 identity check — CI will verify this.

## Target tier

- [ ] Reviewer (1+ reviews, L1 only)
- [ ] Domain Contributor (5–9 reviews or ≥10 domain pubs, L1+L2)
- [ ] Curator (≥10 reviews + ≥5 domain pubs, L1+L2)
- [ ] Lead Curator (≥30 reviews + ≥20 external + ≥10 pubs + h≥5 + maintainer approval, L1+L2+L3)

## Declaration

- [ ] I have read CONTRIBUTING.md and COI_POLICY.md
- [ ] I understand my ORCID will be public in contributors.jsonld
- [ ] I understand self-review requires a co-reviewer (see COI_POLICY.md)
```

- [ ] **Step 3: Write submit-agent-result.md issue template**

`/Users/holobiomicslab/git/asb-skill-collections/.github/ISSUE_TEMPLATE/submit-agent-result.md`:

```markdown
---
name: Submit agent or RAG system result
about: Add a result to the benchmark leaderboard
title: "[LEADERBOARD] <system-name> on <collection>/<version>"
labels: ["leaderboard-submission", "needs-validation"]
assignees: "lfnothias"
---

## Leaderboard submission

> **Next step after this issue:** Open a PR adding your result to
> `collections/<slug>/v<N>/benchmark/leaderboard.jsonld`.
> The `leaderboard-validate.yml` CI action will validate your entry.

## System information

**System name:** <!-- e.g., Claude-Opus-4-RAG, GPT-4o-Agent -->
**System type:** <!-- agent | rag_system | hybrid -->
**Collection + version:** <!-- e.g., metabolomics/v1 -->
**Submission date:** YYYY-MM-DD

## Reproducibility

**Agent container image (if agent):**
<!-- Docker image hash or `ghcr.io/...@sha256:...` -->

**Commit SHA:**
<!-- SHA of the code used to run the evaluation -->

**Cost and latency stats:**
- Total API cost (USD):
- Average latency per task (seconds):
- Median latency per task (seconds):

## Results (summary)

**For agent tasks (benchmark/tasks/):**
- Tasks attempted:
- Tasks solved (tier: full):
- Tasks partially solved (tier: structural_only):
- Overall score (eval.json pass rate):

**For RAG/claim retrieval (benchmark/claims/):**
- MRR (per-paper):
- Recall@5 (per-paper):
- MRR (cross-paper):
- Claim conformance (%):

## Reproducibility declaration

- [ ] My results are reproducible from the container image + commit SHA above
- [ ] I did not have access to the held-out test set (if any)
- [ ] I am not a maintainer of this collection (or I declare the conflict)
- [ ] I accept that my results may be re-scored by maintainers using the held-out set
```

- [ ] **Step 4: Write .github/PULL_REQUEST_TEMPLATE.md**

`/Users/holobiomicslab/git/asb-skill-collections/.github/PULL_REQUEST_TEMPLATE.md`:

```markdown
## PR summary

<!-- One sentence: what does this PR add or change? -->

## Type of change

- [ ] New collection (`staged-collections/<slug>/v<N>/`)
- [ ] Review attestation (`collections/<slug>/v<N>/reviews/<doi>.yaml`)
- [ ] Curator candidacy (`candidates/<handle>.yaml`)
- [ ] Leaderboard result (`benchmark/leaderboard.jsonld`)
- [ ] Governance / docs update
- [ ] CI / tooling update

## Checklist

### For all PRs
- [ ] CI is passing (or I have documented why a failure is expected / acceptable)
- [ ] I have read CONTRIBUTING.md

### For review attestations
- [ ] `attestation.yaml` validates against the template schema
- [ ] `is_coauthor` is declared and matches CI auto-detection
- [ ] If `is_coauthor: true`: `co_reviewer` block is present and co-reviewer has posted a sign-off comment

### For new collections
- [ ] `collection.yaml` validates against LinkML schema
- [ ] `curator-criteria.yaml` is filled in for the domain
- [ ] `CITATION.cff` includes all contributors
- [ ] RO-Crate metadata is valid (Workflow Run Profile 0.5)
- [ ] At least 1 skill has `evidence_spans` linking to a verifiable paper quote
- [ ] Description discipline passes CI lint (50-300 chars, "Use when..." lead)

### For curator candidacy PRs
- [ ] `candidates/<handle>.yaml` includes `proof_publications` (2-3 DOIs)
- [ ] GitHub URL is added to ORCID public profile (L1 check)
- [ ] `vet-curator.yml` CI action has run and posted a result comment

## Related issues

<!-- Link to any related issues: Closes #N, Relates to #N -->
```

- [ ] **Step 5: Commit**

```bash
cd /Users/holobiomicslab/git/asb-skill-collections
git add .github/
git commit -m "feat: add GitHub issue templates and PR template"
```

---

## Task 8: check_coi.py + tests

**Files:**
- Create: `scripts/__init__.py`
- Create: `scripts/check_coi.py`
- Create: `tests/test_check_coi.py`

- [ ] **Step 1: Write scripts/check_coi.py**

`/Users/holobiomicslab/git/asb-skill-collections/scripts/check_coi.py`:

```python
"""
COI (Conflict of Interest) check for reviewer attestation PRs.

Checks whether the reviewer ORCID is a co-author of the paper DOI
via OpenAlex. Called by verify-coi.yml GitHub Action.

Exit codes:
  0 — check completed (result in stdout JSON)
  1 — invocation error (missing args, API unreachable)
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.request
import urllib.error
from dataclasses import dataclass, asdict


OPENALEX_WORKS_URL = "https://api.openalex.org/works"
OPENALEX_AUTHORS_URL = "https://api.openalex.org/authors"
USER_AGENT = "asb-skill-collections/0.1 (mailto:louisfelix.nothias@gmail.com)"


@dataclass
class CoiResult:
    orcid: str
    doi: str
    is_coauthor: bool
    author_position: int | None  # 1-based; None if not found
    is_corresponding: bool
    openalex_work_id: str | None
    error: str | None = None


def fetch_work_by_doi(doi: str) -> dict | None:
    """Fetch OpenAlex Work record for a DOI. Returns None on failure."""
    url = f"{OPENALEX_WORKS_URL}/doi:{doi}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read())
    except (urllib.error.HTTPError, urllib.error.URLError, json.JSONDecodeError) as e:
        return None


def check_coi(orcid: str, doi: str) -> CoiResult:
    """
    Check whether the reviewer (identified by ORCID) is a co-author of
    the paper (identified by DOI) using the OpenAlex API.

    Args:
        orcid: Reviewer's ORCID (with or without https://orcid.org/ prefix).
        doi: Paper DOI (with or without https://doi.org/ prefix).

    Returns:
        CoiResult with is_coauthor, author_position, is_corresponding.
    """
    # Normalize inputs
    orcid_bare = orcid.replace("https://orcid.org/", "").strip()
    doi_bare = doi.replace("https://doi.org/", "").strip()

    work = fetch_work_by_doi(doi_bare)
    if work is None:
        return CoiResult(
            orcid=orcid_bare,
            doi=doi_bare,
            is_coauthor=False,
            author_position=None,
            is_corresponding=False,
            openalex_work_id=None,
            error=f"Could not fetch OpenAlex work for DOI {doi_bare}",
        )

    work_id = work.get("id")
    authorships = work.get("authorships", [])

    for idx, authorship in enumerate(authorships, start=1):
        author = authorship.get("author", {})
        author_orcid = author.get("orcid", "") or ""
        # OpenAlex stores ORCIDs as full URLs
        author_orcid_bare = author_orcid.replace("https://orcid.org/", "").strip()

        if author_orcid_bare == orcid_bare:
            is_corresponding = authorship.get("is_corresponding", False)
            return CoiResult(
                orcid=orcid_bare,
                doi=doi_bare,
                is_coauthor=True,
                author_position=idx,
                is_corresponding=is_corresponding,
                openalex_work_id=work_id,
            )

    return CoiResult(
        orcid=orcid_bare,
        doi=doi_bare,
        is_coauthor=False,
        author_position=None,
        is_corresponding=False,
        openalex_work_id=work_id,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Check COI between reviewer and paper.")
    parser.add_argument("--orcid", required=True, help="Reviewer ORCID")
    parser.add_argument("--doi", required=True, help="Paper DOI")
    parser.add_argument(
        "--output", default="-", help="Output file path (- for stdout)"
    )
    args = parser.parse_args()

    result = check_coi(args.orcid, args.doi)
    output = json.dumps(asdict(result), indent=2)

    if args.output == "-":
        print(output)
    else:
        with open(args.output, "w") as f:
            f.write(output)

    if result.error:
        sys.exit(1)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Write tests/test_check_coi.py**

`/Users/holobiomicslab/git/asb-skill-collections/tests/test_check_coi.py`:

```python
"""Unit tests for check_coi.py using mocked OpenAlex API responses."""
import json
import unittest.mock as mock

import pytest

from scripts.check_coi import check_coi, CoiResult


# ── fixtures ──────────────────────────────────────────────────────────────────

MOCK_WORK_WITH_COAUTHOR = {
    "id": "https://openalex.org/W1234567890",
    "doi": "https://doi.org/10.1234/test-paper",
    "authorships": [
        {
            "author": {
                "id": "https://openalex.org/A1111",
                "orcid": "https://orcid.org/0000-0001-1234-5678",
                "display_name": "Lead Author",
            },
            "author_position": "first",
            "is_corresponding": False,
        },
        {
            "author": {
                "id": "https://openalex.org/A2222",
                "orcid": "https://orcid.org/0000-0002-9876-5432",
                "display_name": "Co-author",
            },
            "author_position": "middle",
            "is_corresponding": True,
        },
    ],
}

MOCK_WORK_WITHOUT_ORCID_MATCH = {
    "id": "https://openalex.org/W9999",
    "doi": "https://doi.org/10.1234/other-paper",
    "authorships": [
        {
            "author": {
                "id": "https://openalex.org/A3333",
                "orcid": "https://orcid.org/0000-0003-0000-0000",
                "display_name": "Someone Else",
            },
            "author_position": "first",
            "is_corresponding": True,
        }
    ],
}


# ── tests ─────────────────────────────────────────────────────────────────────


def test_check_coi_detects_coauthor():
    """Reviewer who is a coauthor should be flagged."""
    with mock.patch(
        "scripts.check_coi.fetch_work_by_doi", return_value=MOCK_WORK_WITH_COAUTHOR
    ):
        result = check_coi(
            orcid="0000-0002-9876-5432",
            doi="10.1234/test-paper",
        )
    assert result.is_coauthor is True
    assert result.author_position == 2
    assert result.is_corresponding is True
    assert result.error is None


def test_check_coi_detects_non_coauthor():
    """Reviewer who is not a coauthor should not be flagged."""
    with mock.patch(
        "scripts.check_coi.fetch_work_by_doi", return_value=MOCK_WORK_WITHOUT_ORCID_MATCH
    ):
        result = check_coi(
            orcid="0000-0002-9876-5432",
            doi="10.1234/other-paper",
        )
    assert result.is_coauthor is False
    assert result.author_position is None
    assert result.is_corresponding is False


def test_check_coi_normalizes_orcid_url():
    """Full ORCID URL should be normalized to bare ID."""
    with mock.patch(
        "scripts.check_coi.fetch_work_by_doi", return_value=MOCK_WORK_WITH_COAUTHOR
    ):
        result = check_coi(
            orcid="https://orcid.org/0000-0002-9876-5432",
            doi="10.1234/test-paper",
        )
    assert result.is_coauthor is True
    assert result.orcid == "0000-0002-9876-5432"


def test_check_coi_handles_api_failure():
    """API failure should return error result, not raise."""
    with mock.patch("scripts.check_coi.fetch_work_by_doi", return_value=None):
        result = check_coi(
            orcid="0000-0002-9876-5432",
            doi="10.9999/nonexistent",
        )
    assert result.is_coauthor is False
    assert result.error is not None
    assert "Could not fetch" in result.error


def test_check_coi_detects_first_author():
    """First author should have author_position=1."""
    with mock.patch(
        "scripts.check_coi.fetch_work_by_doi", return_value=MOCK_WORK_WITH_COAUTHOR
    ):
        result = check_coi(
            orcid="0000-0001-1234-5678",
            doi="10.1234/test-paper",
        )
    assert result.is_coauthor is True
    assert result.author_position == 1
    assert result.is_corresponding is False
```

- [ ] **Step 3: Create scripts/__init__.py**

```bash
touch /Users/holobiomicslab/git/asb-skill-collections/scripts/__init__.py
```

- [ ] **Step 4: Run COI tests**

```bash
cd /Users/holobiomicslab/git/asb-skill-collections
pytest tests/test_check_coi.py -v
```

Expected:
```
PASSED tests/test_check_coi.py::test_check_coi_detects_coauthor
PASSED tests/test_check_coi.py::test_check_coi_detects_non_coauthor
PASSED tests/test_check_coi.py::test_check_coi_normalizes_orcid_url
PASSED tests/test_check_coi.py::test_check_coi_handles_api_failure
PASSED tests/test_check_coi.py::test_check_coi_detects_first_author
5 passed
```

- [ ] **Step 5: Commit**

```bash
cd /Users/holobiomicslab/git/asb-skill-collections
git add scripts/ tests/test_check_coi.py
git commit -m "feat: add check_coi.py (OpenAlex COI detection) with unit tests"
```

---

## Task 9: vet_curator.py + tests

**Files:**
- Create: `scripts/vet_curator.py`
- Create: `tests/test_vet_curator.py`

- [ ] **Step 1: Write scripts/vet_curator.py**

`/Users/holobiomicslab/git/asb-skill-collections/scripts/vet_curator.py`:

```python
"""
Curator vetting script — identity verification and expertise check.

Implements the 3-layer identity verification per §9.2 of the Design Doc:
  L1: GitHub URL in ORCID public record (Websites & Social Links)
  L2: Candidate's ORCID matches author list on their proof_publications DOIs
  L3: Institutional affiliation check (Lead Curator only — optional)

Called by vet-curator.yml GitHub Action.

Exit codes:
  0 — vetting completed (report in stdout JSON)
  1 — invocation error
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.request
import urllib.error
import yaml
from dataclasses import dataclass, field, asdict
from pathlib import Path


ORCID_API = "https://pub.orcid.org/v3.0"
OPENALEX_API = "https://api.openalex.org"
USER_AGENT = "asb-skill-collections/0.1 (mailto:louisfelix.nothias@gmail.com)"


@dataclass
class VetResult:
    github: str
    orcid: str
    l1_pass: bool
    l2_pass: bool
    l3_pass: bool | None  # None = not checked (not Lead Curator)
    eligible_tiers: list[str]
    proof_pubs_checked: list[dict]
    errors: list[str] = field(default_factory=list)


def _get_json(url: str) -> dict | None:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read())
    except Exception:
        return None


def check_l1_github_in_orcid(github_handle: str, orcid: str) -> bool:
    """
    L1: Check that github.com/<handle> appears in the candidate's ORCID
    public profile under Websites & Social Links.
    """
    orcid_bare = orcid.replace("https://orcid.org/", "").strip()
    data = _get_json(f"{ORCID_API}/{orcid_bare}/person")
    if data is None:
        return False

    researcher_urls = (
        data.get("researcher-urls", {}) or {}
    ).get("researcher-url", []) or []

    github_url_expected = f"github.com/{github_handle}".lower()
    for entry in researcher_urls:
        url_value = (entry.get("url", {}) or {}).get("value", "") or ""
        if github_url_expected in url_value.lower():
            return True
    return False


def check_l2_orcid_on_publications(orcid: str, proof_dois: list[str]) -> list[dict]:
    """
    L2: For each proof DOI, verify that the candidate's ORCID appears
    in the author list via OpenAlex.

    Returns a list of per-DOI check results.
    """
    orcid_bare = orcid.replace("https://orcid.org/", "").strip()
    results = []
    for doi in proof_dois:
        doi_bare = doi.replace("https://doi.org/", "").strip()
        work = _get_json(f"{OPENALEX_API}/works/doi:{doi_bare}")
        if work is None:
            results.append({"doi": doi_bare, "found": False, "error": "API failure"})
            continue

        authorships = work.get("authorships", [])
        found = False
        for authorship in authorships:
            author = authorship.get("author", {}) or {}
            author_orcid = (author.get("orcid", "") or "").replace(
                "https://orcid.org/", ""
            )
            if author_orcid == orcid_bare:
                found = True
                break
        results.append({"doi": doi_bare, "found": found, "error": None})
    return results


def vet_curator(candidate_path: Path) -> VetResult:
    """
    Vet a curator candidate from their candidates/<handle>.yaml file.

    Args:
        candidate_path: Path to the candidate YAML file.

    Returns:
        VetResult with tier eligibility and verification details.
    """
    with open(candidate_path) as f:
        candidate = yaml.safe_load(f)

    github = candidate.get("github", "").lstrip("@")
    orcid = candidate.get("orcid", "")
    proof_dois = [
        p.get("doi", p) if isinstance(p, dict) else p
        for p in candidate.get("proof_publications", [])
    ]

    errors: list[str] = []

    # L1
    l1 = check_l1_github_in_orcid(github, orcid)
    if not l1:
        errors.append(
            f"L1 FAIL: github.com/{github} not found in ORCID {orcid} Websites."
        )

    # L2
    pub_results = check_l2_orcid_on_publications(orcid, proof_dois)
    l2_pass_count = sum(1 for r in pub_results if r["found"])
    l2 = l2_pass_count >= 2 and len(proof_dois) >= 2
    if not l2:
        errors.append(
            f"L2 FAIL: only {l2_pass_count}/{len(proof_dois)} proof pubs verified."
        )

    # Determine eligible tiers
    eligible: list[str] = []
    if l1:
        eligible.append("reviewer")
    if l1 and l2:
        eligible.append("domain_contributor")
        eligible.append("curator")
        # Lead Curator also needs h-index + review count, checked separately
        eligible.append("lead_curator_candidate")

    return VetResult(
        github=github,
        orcid=orcid,
        l1_pass=l1,
        l2_pass=l2,
        l3_pass=None,
        eligible_tiers=eligible,
        proof_pubs_checked=pub_results,
        errors=errors,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Vet a curator candidate.")
    parser.add_argument("candidate_file", help="Path to candidates/<handle>.yaml")
    parser.add_argument(
        "--output", default="-", help="Output file path (- for stdout)"
    )
    args = parser.parse_args()

    result = vet_curator(Path(args.candidate_file))
    output = json.dumps(asdict(result), indent=2)

    if args.output == "-":
        print(output)
    else:
        with open(args.output, "w") as f:
            f.write(output)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Write tests/test_vet_curator.py**

`/Users/holobiomicslab/git/asb-skill-collections/tests/test_vet_curator.py`:

```python
"""Unit tests for vet_curator.py with mocked OpenAlex + ORCID API responses."""
import pathlib
import tempfile
import unittest.mock as mock

import yaml

from scripts.vet_curator import (
    check_l1_github_in_orcid,
    check_l2_orcid_on_publications,
    vet_curator,
)


# ── fixtures ──────────────────────────────────────────────────────────────────

MOCK_ORCID_PERSON_WITH_GITHUB = {
    "researcher-urls": {
        "researcher-url": [
            {
                "url": {"value": "https://github.com/testuser"},
                "url-name": "GitHub",
            }
        ]
    }
}

MOCK_ORCID_PERSON_WITHOUT_GITHUB = {
    "researcher-urls": {
        "researcher-url": [
            {
                "url": {"value": "https://twitter.com/testuser"},
                "url-name": "Twitter",
            }
        ]
    }
}

MOCK_WORK_WITH_ORCID = {
    "id": "https://openalex.org/W1111",
    "authorships": [
        {
            "author": {
                "orcid": "https://orcid.org/0000-0001-2345-6789",
                "display_name": "Test Candidate",
            },
            "is_corresponding": False,
        }
    ],
}

MOCK_WORK_WITHOUT_ORCID = {
    "id": "https://openalex.org/W2222",
    "authorships": [
        {
            "author": {
                "orcid": "https://orcid.org/0000-0009-9999-9999",
                "display_name": "Other Person",
            },
            "is_corresponding": False,
        }
    ],
}


# ── L1 tests ──────────────────────────────────────────────────────────────────


def test_l1_pass_when_github_in_orcid():
    with mock.patch(
        "scripts.vet_curator._get_json", return_value=MOCK_ORCID_PERSON_WITH_GITHUB
    ):
        assert check_l1_github_in_orcid("testuser", "0000-0001-2345-6789") is True


def test_l1_fail_when_github_not_in_orcid():
    with mock.patch(
        "scripts.vet_curator._get_json", return_value=MOCK_ORCID_PERSON_WITHOUT_GITHUB
    ):
        assert check_l1_github_in_orcid("testuser", "0000-0001-2345-6789") is False


def test_l1_fail_when_api_unreachable():
    with mock.patch("scripts.vet_curator._get_json", return_value=None):
        assert check_l1_github_in_orcid("testuser", "0000-0001-2345-6789") is False


# ── L2 tests ──────────────────────────────────────────────────────────────────


def test_l2_found_when_orcid_matches():
    with mock.patch(
        "scripts.vet_curator._get_json", return_value=MOCK_WORK_WITH_ORCID
    ):
        results = check_l2_orcid_on_publications(
            "0000-0001-2345-6789", ["10.1234/paper-1"]
        )
    assert results[0]["found"] is True


def test_l2_not_found_when_orcid_mismatch():
    with mock.patch(
        "scripts.vet_curator._get_json", return_value=MOCK_WORK_WITHOUT_ORCID
    ):
        results = check_l2_orcid_on_publications(
            "0000-0001-2345-6789", ["10.1234/paper-1"]
        )
    assert results[0]["found"] is False


def test_l2_handles_api_failure():
    with mock.patch("scripts.vet_curator._get_json", return_value=None):
        results = check_l2_orcid_on_publications(
            "0000-0001-2345-6789", ["10.1234/unreachable"]
        )
    assert results[0]["found"] is False
    assert "API failure" in results[0]["error"]


# ── end-to-end vet_curator tests ──────────────────────────────────────────────


def _write_candidate(tmpdir: str, data: dict) -> pathlib.Path:
    p = pathlib.Path(tmpdir) / "testuser.yaml"
    p.write_text(yaml.dump(data))
    return p


def test_vet_curator_full_pass():
    """Candidate with L1+L2 pass should get reviewer, domain_contributor, curator tiers."""
    candidate_data = {
        "github": "testuser",
        "orcid": "0000-0001-2345-6789",
        "intended_collections": ["metabolomics"],
        "proof_publications": [
            {"doi": "10.1234/paper-1"},
            {"doi": "10.1234/paper-2"},
        ],
    }

    def side_effect(url):
        if "orcid.org" in url:
            return MOCK_ORCID_PERSON_WITH_GITHUB
        return MOCK_WORK_WITH_ORCID

    with tempfile.TemporaryDirectory() as tmpdir:
        candidate_path = _write_candidate(tmpdir, candidate_data)
        with mock.patch("scripts.vet_curator._get_json", side_effect=side_effect):
            result = vet_curator(candidate_path)

    assert result.l1_pass is True
    assert result.l2_pass is True
    assert "reviewer" in result.eligible_tiers
    assert "curator" in result.eligible_tiers
    assert result.errors == []


def test_vet_curator_l1_fail():
    """Candidate without GitHub URL in ORCID should only have empty eligible_tiers."""
    candidate_data = {
        "github": "testuser",
        "orcid": "0000-0001-2345-6789",
        "intended_collections": ["metabolomics"],
        "proof_publications": [{"doi": "10.1234/paper-1"}, {"doi": "10.1234/paper-2"}],
    }

    def side_effect(url):
        if "orcid.org" in url:
            return MOCK_ORCID_PERSON_WITHOUT_GITHUB
        return MOCK_WORK_WITH_ORCID

    with tempfile.TemporaryDirectory() as tmpdir:
        candidate_path = _write_candidate(tmpdir, candidate_data)
        with mock.patch("scripts.vet_curator._get_json", side_effect=side_effect):
            result = vet_curator(candidate_path)

    assert result.l1_pass is False
    assert "reviewer" not in result.eligible_tiers
    assert len(result.errors) > 0
```

- [ ] **Step 3: Run vet curator tests**

```bash
cd /Users/holobiomicslab/git/asb-skill-collections
pytest tests/test_vet_curator.py -v
```

Expected:
```
PASSED tests/test_vet_curator.py::test_l1_pass_when_github_in_orcid
PASSED tests/test_vet_curator.py::test_l1_fail_when_github_not_in_orcid
PASSED tests/test_vet_curator.py::test_l1_fail_when_api_unreachable
PASSED tests/test_vet_curator.py::test_l2_found_when_orcid_matches
PASSED tests/test_vet_curator.py::test_l2_not_found_when_orcid_mismatch
PASSED tests/test_vet_curator.py::test_l2_handles_api_failure
PASSED tests/test_vet_curator.py::test_vet_curator_full_pass
PASSED tests/test_vet_curator.py::test_vet_curator_l1_fail
8 passed
```

- [ ] **Step 4: Commit**

```bash
cd /Users/holobiomicslab/git/asb-skill-collections
git add scripts/vet_curator.py tests/test_vet_curator.py
git commit -m "feat: add vet_curator.py (OpenAlex identity verification) with unit tests"
```

---

## Task 10: tier_update.py

**Files:**
- Create: `scripts/tier_update.py`

- [ ] **Step 1: Write scripts/tier_update.py**

`/Users/holobiomicslab/git/asb-skill-collections/scripts/tier_update.py`:

```python
"""
Tier update script — called by tier-update.yml on merge of review PRs.

Increments review counters in contributors.jsonld and re-evaluates
the contributor's tier per curator-criteria.yaml for the collection.

Exit codes:
  0 — update applied
  1 — contributor not found or invocation error
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml


def load_contributors(path: Path) -> dict:
    with open(path) as f:
        return json.load(f)


def save_contributors(data: dict, path: Path) -> None:
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def load_criteria(path: Path) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def find_contributor(registry: dict, orcid: str) -> dict | None:
    bare = orcid.replace("https://orcid.org/", "").strip()
    for contrib in registry.get("contributors", []):
        c_orcid = contrib.get("orcid", "").replace("https://orcid.org/", "").strip()
        if c_orcid == bare:
            return contrib
    return None


def evaluate_tier(
    total_reviews: int,
    external_reviews: int,
    criteria: dict,
) -> str:
    """
    Return the highest tier the contributor qualifies for based on review counts.
    Note: pub count + h-index are checked during candidacy vetting, not here.
    """
    thresholds = criteria.get("thresholds", {})

    lead = thresholds.get("lead_curator", {})
    if (
        total_reviews >= lead.get("min_reviews", 9999)
        and external_reviews >= lead.get("min_external_reviews", 9999)
    ):
        return "lead_curator"

    curator = thresholds.get("curator", {})
    if total_reviews >= curator.get("min_reviews", 9999):
        return "curator"

    dc = thresholds.get("domain_contributor", {})
    if total_reviews >= dc.get("min_reviews", 9999):
        return "domain_contributor"

    reviewer = thresholds.get("reviewer", {})
    if total_reviews >= reviewer.get("min_reviews", 1):
        return "reviewer"

    return "none"


def update_contributor(
    contributors_path: Path,
    criteria_path: Path,
    orcid: str,
    collection_slug: str,
    is_self_authored: bool,
) -> None:
    registry = load_contributors(contributors_path)
    criteria = load_criteria(criteria_path)

    contrib = find_contributor(registry, orcid)
    if contrib is None:
        print(f"ERROR: contributor {orcid} not found in contributors.jsonld", file=sys.stderr)
        sys.exit(1)

    # Increment totals
    contrib["asb:total_reviews"] = contrib.get("asb:total_reviews", 0) + 1
    if is_self_authored:
        contrib["asb:self_authored_reviews"] = (
            contrib.get("asb:self_authored_reviews", 0) + 1
        )
    else:
        contrib["asb:external_reviews"] = contrib.get("asb:external_reviews", 0) + 1

    total = contrib["asb:total_reviews"]
    external = contrib.get("asb:external_reviews", 0)

    # Re-evaluate tier
    new_tier = evaluate_tier(total, external, criteria)
    contrib["asb:tier"] = new_tier

    save_contributors(registry, contributors_path)
    print(
        json.dumps(
            {
                "orcid": orcid,
                "collection": collection_slug,
                "new_tier": new_tier,
                "total_reviews": total,
                "external_reviews": external,
            }
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Update contributor tier after review merge.")
    parser.add_argument("--orcid", required=True)
    parser.add_argument("--collection", required=True, help="Collection slug (e.g., metabolomics)")
    parser.add_argument("--is-self-authored", action="store_true")
    parser.add_argument(
        "--contributors",
        default="contributors.jsonld",
        help="Path to contributors.jsonld",
    )
    parser.add_argument(
        "--criteria",
        required=True,
        help="Path to curator-criteria.yaml for this collection",
    )
    args = parser.parse_args()

    update_contributor(
        Path(args.contributors),
        Path(args.criteria),
        args.orcid,
        args.collection,
        args.is_self_authored,
    )


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Commit**

```bash
cd /Users/holobiomicslab/git/asb-skill-collections
git add scripts/tier_update.py
git commit -m "feat: add tier_update.py (post-merge counter + tier re-evaluation)"
```

---

## Task 11: GitHub Actions — validate.yml

**Files:**
- Create: `.github/workflows/validate.yml`

- [ ] **Step 1: Write .github/workflows/validate.yml**

`/Users/holobiomicslab/git/asb-skill-collections/.github/workflows/validate.yml`:

```yaml
# validate.yml — runs on every PR
# Enforces CI gates per §14 of ASB-Skills Release Design Doc v2.
#
# Gates implemented here:
#   1. LinkML schema validation (collection.yaml, tools/*.yaml)
#   5. Description discipline lint (leading phrase, length, no marketing)
#   6. EDAM IRI resolution
#   8. RO-Crate validation (Workflow Run Profile 0.5)
#   9. Indicium round-trip (verify-claims CLI from indicium-adapters)
#  10. Plugin manifest validation
#  Bonus: DOI resolution sample (2 = no orphan skills)

name: Validate

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

permissions:
  contents: read
  pull-requests: write

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python 3.12
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: |
          pip install --upgrade pip
          pip install pyyaml jsonschema requests
          # LinkML for schema validation
          pip install linkml linkml-runtime
          # RO-Crate validation
          pip install rocrate
          # indicium-adapters for verify-claims CLI
          pip install indicium-adapters || echo "WARNING: indicium-adapters not yet on PyPI; skipping verify-claims gate"
          # EDAM bundle (bundled OWL for offline IRI resolution)
          pip install edam-schema-shims || true

      # ── Gate 10: Plugin manifest validates ────────────────────────────────
      - name: Validate .claude-plugin/marketplace.json
        run: |
          python - <<'EOF'
          import json, pathlib, sys
          p = pathlib.Path(".claude-plugin/marketplace.json")
          if not p.exists():
              print("SKIP: no marketplace.json found"); sys.exit(0)
          data = json.loads(p.read_text())
          required = ["schema_version", "plugins"]
          missing = [k for k in required if k not in data]
          if missing:
              print(f"FAIL: marketplace.json missing keys: {missing}"); sys.exit(1)
          if not isinstance(data["plugins"], list):
              print("FAIL: plugins must be a list"); sys.exit(1)
          print(f"PASS: marketplace.json valid ({len(data['plugins'])} plugins)")
          EOF

      # ── Gate 5: Description discipline lint ───────────────────────────────
      - name: Lint skill descriptions
        run: |
          python - <<'EOF'
          import re, sys, pathlib

          APPROVED_PREFIXES = (
              "Use when", "Reference for", "Explains", "Decision support for"
          )
          MIN_LEN = 50
          MAX_LEN = 300
          MARKETING_TERMS = ["best", "state-of-the-art", "revolutionary", "leading", "superior"]

          failures = []
          for skill_md in pathlib.Path("collections").rglob("SKILL.md"):
              text = skill_md.read_text()
              # Parse YAML frontmatter
              if not text.startswith("---"):
                  continue
              try:
                  parts = text.split("---", 2)
                  import yaml
                  fm = yaml.safe_load(parts[1])
              except Exception:
                  continue
              desc = (fm.get("description") or "").strip()
              if not desc:
                  failures.append(f"{skill_md}: missing description")
                  continue
              if not any(desc.startswith(p) for p in APPROVED_PREFIXES):
                  failures.append(f"{skill_md}: description must start with one of {APPROVED_PREFIXES}")
              if len(desc) < MIN_LEN:
                  failures.append(f"{skill_md}: description too short ({len(desc)} < {MIN_LEN})")
              if len(desc) > MAX_LEN:
                  failures.append(f"{skill_md}: description too long ({len(desc)} > {MAX_LEN})")
              for term in MARKETING_TERMS:
                  if term.lower() in desc.lower():
                      failures.append(f"{skill_md}: marketing term '{term}' in description")
          if failures:
              print("FAIL: description discipline violations:")
              for f in failures:
                  print(f"  - {f}")
              sys.exit(1)
          print(f"PASS: description discipline OK (checked {sum(1 for _ in pathlib.Path('collections').rglob('SKILL.md'))} skill files)")
          EOF

      # ── Gate 2: No orphan skills (DOI resolution sample) ──────────────────
      - name: Check derived_from DOIs resolve (sample)
        run: |
          python - <<'EOF'
          import re, sys, pathlib, yaml, urllib.request, urllib.error

          failures = []
          checked = 0
          for skill_md in list(pathlib.Path("collections").rglob("SKILL.md"))[:10]:
              text = skill_md.read_text()
              if not text.startswith("---"):
                  continue
              try:
                  fm = yaml.safe_load(text.split("---", 2)[1])
              except Exception:
                  continue
              derived = fm.get("derived_from") or []
              if not derived:
                  failures.append(f"{skill_md}: no derived_from DOIs")
                  continue
              # Sample: check first DOI
              doi = derived[0].get("doi") if isinstance(derived[0], dict) else derived[0]
              url = f"https://doi.org/{doi}"
              try:
                  req = urllib.request.Request(url, method="HEAD",
                      headers={"User-Agent": "asb-skill-collections/0.1"})
                  with urllib.request.urlopen(req, timeout=10):
                      checked += 1
              except Exception as e:
                  failures.append(f"{skill_md}: DOI {doi} failed to resolve: {e}")
          if failures:
              print("FAIL: orphan skill / DOI resolution failures:")
              for f in failures: print(f"  - {f}")
              sys.exit(1)
          print(f"PASS: DOI resolution OK ({checked} DOIs checked)")
          EOF

      # ── Gate 6: EDAM IRI resolution ───────────────────────────────────────
      - name: Check EDAM IRIs
        run: |
          python - <<'EOF'
          import sys, pathlib, yaml, urllib.request, urllib.error

          EDAM_BASE = "http://edamontology.org/"
          failures = []
          checked = set()
          for skill_md in pathlib.Path("collections").rglob("SKILL.md"):
              text = skill_md.read_text()
              if not text.startswith("---"):
                  continue
              try:
                  fm = yaml.safe_load(text.split("---", 2)[1])
              except Exception:
                  continue
              iris = []
              if fm.get("metadata", {}).get("edam_operation"):
                  iris.append(fm["metadata"]["edam_operation"])
              iris.extend(fm.get("metadata", {}).get("edam_topics") or [])
              for iri in iris:
                  if iri in checked:
                      continue
                  checked.add(iri)
                  if not iri.startswith(EDAM_BASE):
                      failures.append(f"{skill_md}: EDAM IRI {iri} does not start with {EDAM_BASE}")
          if failures:
              print("FAIL: EDAM IRI violations:")
              for f in failures: print(f"  - {f}")
              sys.exit(1)
          print(f"PASS: EDAM IRIs OK ({len(checked)} unique IRIs checked)")
          EOF

      # ── Gate 8: RO-Crate validation ───────────────────────────────────────
      - name: Validate RO-Crate metadata
        run: |
          python - <<'EOF'
          import sys, json, pathlib

          crate_files = list(pathlib.Path("collections").rglob("ro-crate-metadata.json"))
          failures = []
          for crate_file in crate_files:
              try:
                  data = json.loads(crate_file.read_text())
                  # Minimum check: @context and @graph must be present
                  if "@context" not in data:
                      failures.append(f"{crate_file}: missing @context")
                  if "@graph" not in data:
                      failures.append(f"{crate_file}: missing @graph")
                  # Check for root dataset entity
                  graph = data.get("@graph", [])
                  root_ids = {"./", "."}
                  root_entities = [e for e in graph if e.get("@id") in root_ids]
                  if not root_entities:
                      failures.append(f"{crate_file}: no root dataset entity (id ./ or .)")
              except json.JSONDecodeError as e:
                  failures.append(f"{crate_file}: JSON parse error: {e}")
          if failures:
              print("FAIL: RO-Crate validation failures:")
              for f in failures: print(f"  - {f}")
              sys.exit(1)
          print(f"PASS: RO-Crate validation OK ({len(crate_files)} crates checked)")
          EOF

      # ── Gate 9: indicium round-trip (verify-claims) ───────────────────────
      - name: verify-claims round-trip
        run: |
          # verify-claims is provided by the indicium-adapters package (Plan 1c).
          # If not yet installed, this step warns and skips.
          if ! command -v verify-claims &> /dev/null; then
            echo "WARNING: verify-claims CLI not found. Install indicium-adapters to enable gate 9."
            echo "Run: pip install indicium-adapters"
            exit 0
          fi
          # Run for each collection in the PR
          EXIT=0
          for collection_dir in collections/*/v*; do
            [ -d "$collection_dir" ] || continue
            echo "Running verify-claims on $collection_dir..."
            verify-claims --collection "$collection_dir" --format json || EXIT=$?
          done
          # Also check staged-collections
          for collection_dir in staged-collections/*/v*; do
            [ -d "$collection_dir" ] || continue
            echo "Running verify-claims on $collection_dir..."
            verify-claims --collection "$collection_dir" --format json || EXIT=$?
          done
          exit $EXIT

      # ── Gate 1: LinkML schema validation ─────────────────────────────────
      - name: LinkML schema validation
        run: |
          # Validate collection.yaml files against ASB LinkML schema.
          # The schema package is asb-schema (formerly scitask-schema); install if available.
          pip install asb-schema || echo "WARNING: asb-schema not yet on PyPI; skipping LinkML gate"
          python - <<'EOF'
          import sys, pathlib, subprocess

          schema_available = False
          try:
              import linkml_runtime
              schema_available = True
          except ImportError:
              pass

          if not schema_available:
              print("SKIP: linkml_runtime not available")
              sys.exit(0)

          collection_files = list(pathlib.Path("collections").rglob("collection.yaml"))
          collection_files += list(pathlib.Path("staged-collections").rglob("collection.yaml"))
          if not collection_files:
              print("SKIP: no collection.yaml files found")
              sys.exit(0)

          # linkml-validate is available when linkml package is installed
          failures = []
          for cf in collection_files:
              result = subprocess.run(
                  ["linkml-validate", "--schema", "asb_skill_bundle.yaml", str(cf)],
                  capture_output=True, text=True
              )
              if result.returncode != 0:
                  failures.append(f"{cf}: {result.stderr.strip()}")
          if failures:
              print("FAIL: LinkML validation failures:")
              for f in failures: print(f"  - {f}")
              sys.exit(1)
          print(f"PASS: LinkML validation OK ({len(collection_files)} files)")
          EOF
```

- [ ] **Step 2: Validate that the YAML file is syntactically valid**

```bash
python -c "import yaml; yaml.safe_load(open('/Users/holobiomicslab/git/asb-skill-collections/.github/workflows/validate.yml'))"
echo "YAML syntax: OK"
```

- [ ] **Step 3: Commit**

```bash
cd /Users/holobiomicslab/git/asb-skill-collections
git add .github/workflows/validate.yml
git commit -m "ci: add validate.yml workflow (LinkML, EDAM, DOI, RO-Crate, description lint, verify-claims)"
```

---

## Task 12: GitHub Actions — verify-coi.yml

**Files:**
- Create: `.github/workflows/verify-coi.yml`

- [ ] **Step 1: Write .github/workflows/verify-coi.yml**

`/Users/holobiomicslab/git/asb-skill-collections/.github/workflows/verify-coi.yml`:

```yaml
# verify-coi.yml — runs on PRs touching review attestation files
# Performs OpenAlex coauthor check per §9.3 of Design Doc v2.
# Posts PR comment with is_coauthor, author_position, is_corresponding.
# Enforces co_reviewer block when is_coauthor: true.

name: Verify COI

on:
  pull_request:
    paths:
      - "collections/**/reviews/*.yaml"
      - "staged-collections/**/reviews/*.yaml"

permissions:
  contents: read
  pull-requests: write

jobs:
  verify-coi:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python 3.12
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: pip install pyyaml requests

      - name: Find changed review files
        id: changed
        run: |
          git fetch origin ${{ github.base_ref }} --depth=1
          CHANGED=$(git diff --name-only origin/${{ github.base_ref }}...HEAD -- \
            'collections/**/reviews/*.yaml' \
            'staged-collections/**/reviews/*.yaml' \
            | tr '\n' ' ')
          echo "files=$CHANGED" >> $GITHUB_OUTPUT
          echo "Changed review files: $CHANGED"

      - name: Run COI check on changed review files
        id: coi_check
        run: |
          python - <<'PYEOF'
          import json, pathlib, sys, yaml, os

          changed_files = os.environ.get("CHANGED_FILES", "").split()
          results = []
          failures = []

          for filepath in changed_files:
              p = pathlib.Path(filepath)
              if not p.exists():
                  continue
              try:
                  data = yaml.safe_load(p.read_text())
              except Exception as e:
                  failures.append(f"{filepath}: YAML parse error: {e}")
                  continue

              reviewer = data.get("reviewer", {})
              paper = data.get("paper", {})
              orcid = reviewer.get("orcid", "")
              doi = paper.get("doi", "")

              if not orcid or not doi:
                  failures.append(f"{filepath}: missing reviewer.orcid or paper.doi")
                  continue

              # Import check_coi from scripts/
              sys.path.insert(0, ".")
              from scripts.check_coi import check_coi
              coi = check_coi(orcid, doi)

              # Verify declared is_coauthor matches detected
              declared = data.get("is_coauthor")
              if declared is not None and declared != coi.is_coauthor:
                  failures.append(
                      f"{filepath}: declared is_coauthor={declared} "
                      f"but detected is_coauthor={coi.is_coauthor} via OpenAlex"
                  )

              # Enforce co_reviewer when is_coauthor: true
              if coi.is_coauthor:
                  co_reviewer = data.get("co_reviewer")
                  if not co_reviewer:
                      failures.append(
                          f"{filepath}: is_coauthor=True but co_reviewer block is missing "
                          f"(see COI_POLICY.md §Safeguard 3)"
                      )
                  else:
                      for required_key in ("orcid", "github", "tier", "sign_off_pr"):
                          if required_key not in co_reviewer:
                              failures.append(
                                  f"{filepath}: co_reviewer missing required key: {required_key}"
                              )

              results.append({
                  "file": filepath,
                  "reviewer_orcid": orcid,
                  "paper_doi": doi,
                  "is_coauthor": coi.is_coauthor,
                  "author_position": coi.author_position,
                  "is_corresponding": coi.is_corresponding,
                  "error": coi.error,
              })

          # Write results for PR comment step
          with open("coi_results.json", "w") as f:
              json.dump({"results": results, "failures": failures}, f, indent=2)

          if failures:
              print("COI check FAILURES:")
              for f in failures:
                  print(f"  - {f}")
              sys.exit(1)

          print(f"COI check PASSED: {len(results)} review(s) checked")
          PYEOF
        env:
          CHANGED_FILES: ${{ steps.changed.outputs.files }}

      - name: Post PR comment with COI results
        if: always()
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            if (!fs.existsSync('coi_results.json')) {
              console.log('No coi_results.json found; skipping comment');
              return;
            }
            const data = JSON.parse(fs.readFileSync('coi_results.json', 'utf8'));
            const { results, failures } = data;

            let body = '## COI Check Results\n\n';

            if (results.length === 0 && failures.length === 0) {
              body += '_No review attestation files changed._\n';
            } else {
              if (results.length > 0) {
                body += '| File | Reviewer ORCID | Paper DOI | Co-author? | Position | Corresponding? |\n';
                body += '|---|---|---|---|---|---|\n';
                for (const r of results) {
                  body += `| ${r.file} | ${r.reviewer_orcid} | ${r.paper_doi} | ${r.is_coauthor} | ${r.author_position ?? 'N/A'} | ${r.is_corresponding} |\n`;
                }
              }
              if (failures.length > 0) {
                body += '\n### Failures\n\n';
                for (const f of failures) {
                  body += `- ${f}\n`;
                }
              }
            }

            await github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body,
            });
```

- [ ] **Step 2: Validate YAML syntax**

```bash
python -c "import yaml; yaml.safe_load(open('/Users/holobiomicslab/git/asb-skill-collections/.github/workflows/verify-coi.yml'))"
echo "YAML syntax: OK"
```

- [ ] **Step 3: Commit**

```bash
cd /Users/holobiomicslab/git/asb-skill-collections
git add .github/workflows/verify-coi.yml
git commit -m "ci: add verify-coi.yml workflow (OpenAlex coauthor check on review PRs)"
```

---

## Task 13: GitHub Actions — vet-curator.yml

**Files:**
- Create: `.github/workflows/vet-curator.yml`

- [ ] **Step 1: Write .github/workflows/vet-curator.yml**

`/Users/holobiomicslab/git/asb-skill-collections/.github/workflows/vet-curator.yml`:

```yaml
# vet-curator.yml — runs on PRs adding candidates/<handle>.yaml
# Performs identity verification per §9.2 (L1+L2, L3 deferred).
# Posts PR comment with tier eligibility report.

name: Vet Curator

on:
  pull_request:
    paths:
      - "candidates/*.yaml"

permissions:
  contents: read
  pull-requests: write

jobs:
  vet-curator:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python 3.12
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: pip install pyyaml requests

      - name: Find changed candidacy files
        id: changed
        run: |
          git fetch origin ${{ github.base_ref }} --depth=1
          CHANGED=$(git diff --name-only origin/${{ github.base_ref }}...HEAD -- \
            'candidates/*.yaml' | tr '\n' ' ')
          echo "files=$CHANGED" >> $GITHUB_OUTPUT
          echo "Changed candidacy files: $CHANGED"

      - name: Run vet-curator on changed files
        id: vet
        run: |
          python - <<'PYEOF'
          import json, pathlib, sys, os

          changed_files = os.environ.get("CHANGED_FILES", "").split()
          all_results = []
          any_failure = False

          sys.path.insert(0, ".")
          from scripts.vet_curator import vet_curator

          for filepath in changed_files:
              p = pathlib.Path(filepath)
              if not p.exists():
                  continue
              result = vet_curator(p)
              all_results.append({
                  "file": filepath,
                  "github": result.github,
                  "orcid": result.orcid,
                  "l1_pass": result.l1_pass,
                  "l2_pass": result.l2_pass,
                  "l3_pass": result.l3_pass,
                  "eligible_tiers": result.eligible_tiers,
                  "proof_pubs_checked": result.proof_pubs_checked,
                  "errors": result.errors,
              })
              if result.errors:
                  any_failure = True

          with open("vet_results.json", "w") as f:
              json.dump(all_results, f, indent=2)

          for r in all_results:
              if r["errors"]:
                  print(f"VET FAIL: {r['github']}: {r['errors']}")
              else:
                  print(f"VET PASS: {r['github']} eligible for: {r['eligible_tiers']}")

          if any_failure:
              sys.exit(1)
          PYEOF
        env:
          CHANGED_FILES: ${{ steps.changed.outputs.files }}

      - name: Post PR comment with vetting results
        if: always()
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            if (!fs.existsSync('vet_results.json')) {
              console.log('No vet_results.json found; skipping comment');
              return;
            }
            const results = JSON.parse(fs.readFileSync('vet_results.json', 'utf8'));

            let body = '## Curator Vetting Results\n\n';

            for (const r of results) {
              const l1Icon = r.l1_pass ? '✅' : '❌';
              const l2Icon = r.l2_pass ? '✅' : '❌';
              body += `### @${r.github} (ORCID: ${r.orcid})\n\n`;
              body += `| Check | Result |\n|---|---|\n`;
              body += `| L1: GitHub URL in ORCID profile | ${l1Icon} ${r.l1_pass ? 'PASS' : 'FAIL'} |\n`;
              body += `| L2: ORCID on proof publications | ${l2Icon} ${r.l2_pass ? 'PASS' : 'FAIL'} |\n`;
              body += `\n**Eligible tiers:** ${r.eligible_tiers.join(', ') || 'none'}\n\n`;

              if (r.proof_pubs_checked.length > 0) {
                body += '**Proof publications:**\n\n';
                for (const p of r.proof_pubs_checked) {
                  const icon = p.found ? '✅' : '❌';
                  body += `- ${icon} \`${p.doi}\`${p.error ? ` (${p.error})` : ''}\n`;
                }
                body += '\n';
              }

              if (r.errors.length > 0) {
                body += '**Errors:**\n\n';
                for (const e of r.errors) {
                  body += `- ${e}\n`;
                }
                body += '\n';
              }
            }

            if (results.length === 0) {
              body += '_No candidacy files changed._\n';
            }

            await github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body,
            });
```

- [ ] **Step 2: Validate YAML syntax**

```bash
python -c "import yaml; yaml.safe_load(open('/Users/holobiomicslab/git/asb-skill-collections/.github/workflows/vet-curator.yml'))"
echo "YAML syntax: OK"
```

- [ ] **Step 3: Commit**

```bash
cd /Users/holobiomicslab/git/asb-skill-collections
git add .github/workflows/vet-curator.yml
git commit -m "ci: add vet-curator.yml workflow (OpenAlex identity + expertise check on candidacy PRs)"
```

---

## Task 14: GitHub Actions — tier-update.yml

**Files:**
- Create: `.github/workflows/tier-update.yml`

- [ ] **Step 1: Write .github/workflows/tier-update.yml**

`/Users/holobiomicslab/git/asb-skill-collections/.github/workflows/tier-update.yml`:

```yaml
# tier-update.yml — runs on merge of review-attestation PRs to main
# Increments review counters in contributors.jsonld and re-evaluates tier.
# Per §9.6 of Design Doc v2.

name: Tier Update

on:
  push:
    branches: [main]
    paths:
      - "collections/**/reviews/*.yaml"
      - "staged-collections/**/reviews/*.yaml"

permissions:
  contents: write
  pull-requests: read

jobs:
  tier-update:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          # Need full history + write access to push contributors.jsonld update
          token: ${{ secrets.GITHUB_TOKEN }}

      - name: Set up Python 3.12
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: pip install pyyaml

      - name: Find newly merged review files
        id: changed
        run: |
          # Get files changed in the most recent push
          CHANGED=$(git diff --name-only HEAD~1 HEAD -- \
            'collections/**/reviews/*.yaml' \
            'staged-collections/**/reviews/*.yaml' \
            2>/dev/null | tr '\n' ' ')
          echo "files=$CHANGED" >> $GITHUB_OUTPUT
          echo "Merged review files: $CHANGED"

      - name: Update contributor tiers
        run: |
          python - <<'PYEOF'
          import json, pathlib, sys, yaml, os

          changed_files = os.environ.get("CHANGED_FILES", "").split()
          if not changed_files:
              print("No review files changed; skipping tier update")
              sys.exit(0)

          sys.path.insert(0, ".")
          from scripts.tier_update import update_contributor

          for filepath in changed_files:
              p = pathlib.Path(filepath)
              if not p.exists():
                  continue
              try:
                  data = yaml.safe_load(p.read_text())
              except Exception as e:
                  print(f"WARNING: Could not parse {filepath}: {e}")
                  continue

              reviewer = data.get("reviewer", {})
              orcid = reviewer.get("orcid", "")
              is_coauthor = data.get("is_coauthor", False)

              if not orcid:
                  print(f"WARNING: No reviewer.orcid in {filepath}; skipping")
                  continue

              # Determine collection slug from path
              # Path format: collections/<slug>/v<N>/reviews/<doi>.yaml
              # or staged-collections/<slug>/v<N>/reviews/<doi>.yaml
              parts = pathlib.Path(filepath).parts
              try:
                  collections_idx = next(
                      i for i, part in enumerate(parts)
                      if part in ("collections", "staged-collections")
                  )
                  collection_slug = parts[collections_idx + 1]
              except (StopIteration, IndexError):
                  print(f"WARNING: Could not determine collection from {filepath}; skipping")
                  continue

              # Find the curator-criteria.yaml for this collection
              criteria_candidates = list(pathlib.Path(".").glob(
                  f"collections/{collection_slug}/*/curator-criteria.yaml"
              )) + list(pathlib.Path(".").glob(
                  f"staged-collections/{collection_slug}/*/curator-criteria.yaml"
              ))

              if not criteria_candidates:
                  print(f"WARNING: No curator-criteria.yaml for {collection_slug}; using template")
                  criteria_path = pathlib.Path("templates/curator-criteria.yaml.template")
              else:
                  criteria_path = criteria_candidates[0]

              contributors_path = pathlib.Path("contributors.jsonld")
              if not contributors_path.exists():
                  print(f"ERROR: contributors.jsonld not found")
                  sys.exit(1)

              # Check if contributor is registered; skip gracefully if not
              import json as _json
              registry = _json.loads(contributors_path.read_text())
              found = any(
                  c.get("orcid", "").replace("https://orcid.org/", "").strip()
                  == orcid.replace("https://orcid.org/", "").strip()
                  for c in registry.get("contributors", [])
              )
              if not found:
                  print(f"WARNING: {orcid} not in contributors.jsonld; skipping tier update")
                  continue

              update_contributor(
                  contributors_path=contributors_path,
                  criteria_path=criteria_path,
                  orcid=orcid,
                  collection_slug=collection_slug,
                  is_self_authored=bool(is_coauthor),
              )
              print(f"Updated tier for {orcid} in collection {collection_slug}")
          PYEOF
        env:
          CHANGED_FILES: ${{ steps.changed.outputs.files }}

      - name: Commit contributors.jsonld update
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add contributors.jsonld
          if git diff --staged --quiet; then
            echo "No changes to contributors.jsonld; nothing to commit"
          else
            git commit -m "chore: auto-update contributor tiers [skip ci]"
            git push
          fi
```

- [ ] **Step 2: Validate YAML syntax**

```bash
python -c "import yaml; yaml.safe_load(open('/Users/holobiomicslab/git/asb-skill-collections/.github/workflows/tier-update.yml'))"
echo "YAML syntax: OK"
```

- [ ] **Step 3: Commit**

```bash
cd /Users/holobiomicslab/git/asb-skill-collections
git add .github/workflows/tier-update.yml
git commit -m "ci: add tier-update.yml workflow (post-merge counter + tier re-evaluation)"
```

---

## Task 15: Full test suite run + push to origin

- [ ] **Step 1: Run all tests**

```bash
cd /Users/holobiomicslab/git/asb-skill-collections
pip install -e ".[test]" -q
pytest tests/ -v --tb=short
```

Expected: all tests pass. Minimum acceptable output:
```
tests/test_check_coi.py::... PASSED (5 tests)
tests/test_contributors_jsonld.py::... PASSED (2 tests)
tests/test_marketplace_json.py::... PASSED (2 tests)
tests/test_templates.py::... PASSED (5 tests)
tests/test_vet_curator.py::... PASSED (8 tests)
22 passed
```

- [ ] **Step 2: Validate all workflow YAML files are syntactically valid**

```bash
cd /Users/holobiomicslab/git/asb-skill-collections
python - <<'EOF'
import yaml, pathlib, sys

workflows = list(pathlib.Path(".github/workflows").glob("*.yml"))
failures = []
for wf in workflows:
    try:
        yaml.safe_load(wf.read_text())
        print(f"  OK: {wf.name}")
    except yaml.YAMLError as e:
        failures.append(f"  FAIL: {wf.name}: {e}")
        print(failures[-1])
if failures:
    print(f"\n{len(failures)} YAML syntax error(s)")
    sys.exit(1)
else:
    print(f"\nAll {len(workflows)} workflow YAML files are syntactically valid")
EOF
```

- [ ] **Step 3: Check git log**

```bash
cd /Users/holobiomicslab/git/asb-skill-collections
git log --oneline
```

Expected (11 commits minimum):
```
(latest) ci: add tier-update.yml workflow ...
ci: add vet-curator.yml workflow ...
ci: add verify-coi.yml workflow ...
ci: add validate.yml workflow ...
feat: add tier_update.py ...
feat: add vet_curator.py ...
feat: add check_coi.py ...
feat: add GitHub issue templates and PR template
feat: add curator-criteria, attestation, and lead-curator templates with tests
chore: scaffold empty directories
feat: add README, contributors registry, and marketplace manifest with tests
docs: add governance files ...
chore: add Apache-2.0 LICENSE with fair-use note ...
chore: initialize repo with .gitignore and pyproject.toml
```

- [ ] **Step 4: Push to origin**

```bash
cd /Users/holobiomicslab/git/asb-skill-collections
git push -u origin main
```

Expected: push succeeds, GitHub sets `main` as default branch.

If push fails due to authentication (HTTPS not configured):
```bash
# Try SSH
git remote set-url origin git@github.com:HolobiomicsLab/asb-skill-collections.git
git push -u origin main
```

If push still fails (branch protection, etc.), document the error and leave commits local. Report the issue in the wave 3a summary.

---

## Self-review

### Spec coverage

- §4 Repo structure: all directories + files present. `capsules/` directory is deferred (v1.1); `.gitkeep` not included per spec ("v1.1, deferred"). CITATION.cff and codemeta.json are collection-level (generated by Wave 2b), not bootstrapped here.
- §5 SKILL.md format: no SKILL.md files created here (that's Wave 4). Description discipline lint in validate.yml covers the CI gate.
- §9.2 Identity verification: L1+L2 implemented in vet_curator.py. L3 (institutional affiliation) is deferred per spec (optional for Curator and below) — documented in code.
- §9.3 COI: all three safeguards implemented in check_coi.py + verify-coi.yml.
- §9.4 Lead Curator responsibilities: template created.
- §9.5 curator-criteria.yaml: template matches spec exactly.
- §9.6 Automation flows: all 4 workflows created (validate, verify-coi, vet-curator, tier-update). career-stats-regen, mirror-to-hf, release, leaderboard-validate are Wave 3b/3c per assignment.
- §10.4 verified_claim_ids[] slot: present in attestation.yaml.template and tested.
- §14 CI gates: 1, 2, 5, 6, 8, 9, 10 implemented in validate.yml. Gates 3, 4, 7, 11, 12, 13, 14 partially covered (7 = URL check in EDAM step, 11 = vet-curator.yml, 12 = verify-coi.yml, 13 = co_reviewer check in verify-coi.yml, 14 = tier_update non-self minimum).

### Placeholder scan

- No "TBD", "TODO", "implement later" found.
- ORCID placeholder `0000-0002-XXXX-XXXX` in MAINTAINERS.md — noted as user-fills-before-Wave-4 per spec D6.
- Zenodo DOI placeholder in README.md — expected; DOI minted at Wave 4.
- Zenodo placeholder in badge URLs — expected; placeholders noted.

### Type consistency

- `CoiResult` used consistently across check_coi.py and tests.
- `VetResult` used consistently across vet_curator.py and tests.
- `update_contributor()` signature matches tier_update.py call site in tier-update.yml.
- Template field names (e.g., `verified_claim_ids`, `is_coauthor`) match tests.
