# Catalogue + Leaderboard Infrastructure (Wave 3c) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver `catalogue.jsonld` generator, leaderboard JSON-LD validator, career-stats rebuilder, two updated templates, three GitHub Actions workflows, and a minimal GitHub Pages site for `HolobiomicsLab/asb-skill-collections`.

**Architecture:** All Python logic lives in `scripts/` (one file per concern); tests in `tests/` using pytest with fixtures in `tests/fixtures/`. GitHub Actions workflows call the scripts. The Pages site is static HTML + vanilla JS under `docs-site/`, deployed by a fourth workflow. Branch is `wave3/catalogue-leaderboard`; 3b runs in parallel on `wave3/hf-mirror` — never touch `mirror-to-hf.yml`, `templates/hf-space/`, `templates/HOWTO-RUN.md.template`, `scripts/generate_hf_*`, or `README.md`.

**Tech Stack:** Python 3.12, PyYAML, jsonschema, pytest, pathlib (stdlib only for scripts). JSON-LD output via stdlib `json`. GitHub Actions (ubuntu-latest). Plain HTML + vanilla JS for Pages site.

---

## File Map

| File | Responsibility |
|---|---|
| `scripts/regen_catalogue.py` | Walk `collections/`, emit `catalogue.jsonld` (`SkillCollectionRegistry`). CLI entry: `python scripts/regen_catalogue.py [--repo-root .] [--output catalogue.jsonld]` |
| `scripts/validate_leaderboard.py` | Validate `benchmark/leaderboard.jsonld` against schema with `result_type` discriminator. CLI: `python scripts/validate_leaderboard.py <leaderboard.jsonld>` |
| `scripts/regen_career_stats.py` | Rebuild `leaderboard/career.jsonld`, `leaderboard/annual-<year>.jsonld`, `leaderboard/by-domain/<domain>.jsonld` from `contributors.jsonld` + per-collection `reviews/` dirs. CLI: `python scripts/regen_career_stats.py [--repo-root .]` |
| `templates/leaderboard.jsonld.template` | Empty leaderboard JSON-LD with schema + `_doc` keys inline |
| `templates/attestation.yaml.template` | Existing file — add `verified_claim_ids[]` slot with comment (§10.4 gold-tier) |
| `.github/workflows/release.yml` | Tag-triggered: validate → regen catalogue → commit → Zenodo upload → update CITATION.cff → trigger `mirror-to-hf.yml` |
| `.github/workflows/leaderboard-validate.yml` | PR-triggered on `collections/**/benchmark/leaderboard.jsonld` changes; runs validator, posts PR comment |
| `.github/workflows/career-stats-regen.yml` | Push-to-main-triggered on `collections/**/reviews/*.yaml` or `contributors.jsonld` changes; runs regen + commits |
| `docs-site/index.html` | Static catalogue + leaderboard browser (fetches JSON-LD live from GitHub raw) |
| `docs-site/app.js` | Vanilla JS: fetch + render catalogue entries and career leaderboard tables |
| `docs-site/style.css` | Minimal CSS (system font, readable table layout) |
| `.github/workflows/pages.yml` | Deploy `docs-site/` to GitHub Pages on push to main |
| `tests/fixtures/mini_collection/collection.yaml` | Minimal collection YAML for regen_catalogue tests |
| `tests/fixtures/leaderboard_valid.jsonld` | Valid leaderboard fixture |
| `tests/fixtures/leaderboard_invalid.jsonld` | Invalid leaderboard fixture (missing required fields) |
| `tests/test_regen_catalogue.py` | Unit tests for regen_catalogue with fixture collection |
| `tests/test_validate_leaderboard.py` | Unit tests: valid passes, invalid fails, unknown result_type fails |
| `tests/test_regen_career_stats.py` | Unit tests with mini contributors.jsonld + one review fixture |

---

## Task 1: Branch + fixtures + attestation template update

**Files:**
- Modify: `templates/attestation.yaml.template` (add `verified_claim_ids[]` comment + slot)
- Create: `tests/fixtures/mini_collection/collection.yaml`
- Create: `tests/fixtures/leaderboard_valid.jsonld`
- Create: `tests/fixtures/leaderboard_invalid.jsonld`

- [ ] **Step 1.1: Create the branch**

```bash
git -C /Users/holobiomicslab/git/asb-skill-collections checkout -b wave3/catalogue-leaderboard
```

Expected: `Switched to a new branch 'wave3/catalogue-leaderboard'`

- [ ] **Step 1.2: Update `templates/attestation.yaml.template` to add `verified_claim_ids[]` with gold-tier comment**

Read the file first, then add the `verified_claim_ids` block. The current file already has a placeholder `verified_claim_ids: []` at line 36 — verify it and add the detailed comment block above/around it. The target state for that section is:

```yaml
# List claim IDs you manually verified (gold-tier ground truth for benchmark).
# These claims are marked as verified in benchmark/claims/ ground truth.
# Gold-tier claims enable absolute calibration of RAG-system benchmarks (§10.4).
# A claim ID is a URN of the form "urn:asb:claim:<slug>".
# Only list claims you have personally verified by reading the verbatim evidence span
# and confirming it matches the paper text. Leave empty if not applicable.
# Silver tier (auto): all ASB-extracted claims with trace_status: exact_match.
# Gold tier (human): claims listed here by a reviewer with ≥reviewer identity tier.
verified_claim_ids: []              # e.g., ["urn:asb:claim:abc123", "urn:asb:claim:def456"]
```

Replace the current 3-line block (lines 33-36) with the above. The file already has this:
```
# List claim IDs you manually verified (gold-tier ground truth for benchmark).
# These claims are marked as verified in benchmark/claims/ ground truth.
# Leave empty if you did not verify claims to ground-truth level.
verified_claim_ids: []                  # e.g., ["urn:asb:claim:abc123", ...]
```

- [ ] **Step 1.3: Create fixture collection YAML**

Create `tests/fixtures/mini_collection/collection.yaml`:

```yaml
# Minimal collection YAML for regen_catalogue unit tests.
"@context":
  "@vocab": "https://schema.org/"
  asb: "https://w3id.org/holobiomicslab/asb-skill/"
  edam: "http://edamontology.org/"
"@type": "asb:SkillCollection"
"@id": "https://w3id.org/holobiomicslab/asb-skill/collection/test-domain/v1"
title: "Test Domain Collection"
version: "1"
slug: "test-domain"
domain_topics:
  - "http://edamontology.org/topic_0091"
doi: null
released_at: null
lead_curators:
  - orcid: "0000-0001-0000-0000"
    github: "test-curator"
skills_count: 2
tools_count: 1
```

- [ ] **Step 1.4: Create valid leaderboard fixture**

Create `tests/fixtures/leaderboard_valid.jsonld`:

```json
{
  "@context": {
    "asb": "https://w3id.org/holobiomicslab/asb-skill/",
    "xsd": "http://www.w3.org/2001/XMLSchema#"
  },
  "@type": "asb:Leaderboard",
  "collection": "https://w3id.org/holobiomicslab/asb-skill/collection/test-domain/v1",
  "entries": [
    {
      "result_type": "agent",
      "submitter_handle": "test-user",
      "submitter_orcid": "0000-0001-2345-6789",
      "agent_or_system_name": "TestAgent v1.0",
      "image_digest": "sha256:abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890ab",
      "submitted_at": "2026-05-25T00:00:00Z",
      "scores": {"task-001": 0.85, "task-002": 0.72},
      "metrics": {"latency_s": 12.3, "cost_usd": 0.045}
    },
    {
      "result_type": "rag_system",
      "submitter_handle": "rag-team",
      "submitter_orcid": null,
      "agent_or_system_name": "FastRAG 2.0",
      "image_digest": "sha256:1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef12",
      "submitted_at": "2026-05-25T01:00:00Z",
      "scores": {"claim-q001": 0.91, "claim-q002": 0.88},
      "metrics": {"recall_at_5": 0.93, "mrr": 0.87}
    },
    {
      "result_type": "hybrid",
      "submitter_handle": "hybrid-lab",
      "submitter_orcid": null,
      "agent_or_system_name": "HybridSys",
      "image_digest": "abc123def456abc123def456abc123def456abc123def456abc123def456abc123de",
      "submitted_at": "2026-05-25T02:00:00Z",
      "scores": {"task-001": 0.80},
      "metrics": {}
    }
  ]
}
```

- [ ] **Step 1.5: Create invalid leaderboard fixture**

Create `tests/fixtures/leaderboard_invalid.jsonld`:

```json
{
  "@context": {"asb": "https://w3id.org/holobiomicslab/asb-skill/"},
  "@type": "asb:Leaderboard",
  "collection": "https://w3id.org/holobiomicslab/asb-skill/collection/test-domain/v1",
  "entries": [
    {
      "result_type": "robot",
      "submitter_handle": "bad-actor",
      "agent_or_system_name": "BadBot"
    }
  ]
}
```

- [ ] **Step 1.6: Verify fixtures are valid YAML/JSON**

```bash
cd /Users/holobiomicslab/git/asb-skill-collections && python -c "
import yaml, json, pathlib
yaml.safe_load(pathlib.Path('tests/fixtures/mini_collection/collection.yaml').read_text())
json.loads(pathlib.Path('tests/fixtures/leaderboard_valid.jsonld').read_text())
json.loads(pathlib.Path('tests/fixtures/leaderboard_invalid.jsonld').read_text())
print('All fixtures parse OK')
"
```

Expected: `All fixtures parse OK`

- [ ] **Step 1.7: Commit**

```bash
git -C /Users/holobiomicslab/git/asb-skill-collections add templates/attestation.yaml.template tests/fixtures/
git -C /Users/holobiomicslab/git/asb-skill-collections commit -m "feat: add leaderboard/collection fixtures; expand verified_claim_ids comment in attestation template"
```

---

## Task 2: `scripts/regen_catalogue.py` + tests

**Files:**
- Create: `scripts/regen_catalogue.py`
- Create: `tests/test_regen_catalogue.py`

- [ ] **Step 2.1: Write the failing test first**

Create `tests/test_regen_catalogue.py`:

```python
"""Unit tests for regen_catalogue.py."""
import json
import pathlib
import pytest
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

FIXTURES = pathlib.Path(__file__).parent / "fixtures"
MINI_COLLECTION_DIR = FIXTURES / "mini_collection"


@pytest.fixture()
def tmp_repo(tmp_path):
    """A minimal fake repo root with one collection."""
    collections_dir = tmp_path / "collections" / "test-domain" / "v1"
    collections_dir.mkdir(parents=True)
    # Copy mini collection YAML
    import shutil
    shutil.copy(MINI_COLLECTION_DIR / "collection.yaml", collections_dir / "collection.yaml")
    return tmp_path


def test_catalogue_has_context(tmp_repo):
    from scripts.regen_catalogue import build_catalogue
    cat = build_catalogue(tmp_repo)
    assert "@context" in cat
    assert "@type" in cat
    assert cat["@type"] == "asb:SkillCollectionRegistry"


def test_catalogue_lists_collection(tmp_repo):
    from scripts.regen_catalogue import build_catalogue
    cat = build_catalogue(tmp_repo)
    assert "collections" in cat
    assert len(cat["collections"]) == 1
    entry = cat["collections"][0]
    assert entry["title"] == "Test Domain Collection"


def test_catalogue_has_required_fields(tmp_repo):
    from scripts.regen_catalogue import build_catalogue
    cat = build_catalogue(tmp_repo)
    entry = cat["collections"][0]
    required = ["@id", "title", "version", "slug", "skills_count", "tools_count"]
    for field in required:
        assert field in entry, f"Missing field: {field}"


def test_catalogue_is_alphabetically_ordered(tmp_path):
    """Multiple collections should be sorted alphabetically by slug."""
    from scripts.regen_catalogue import build_catalogue
    for slug in ["zebra-domain", "alpha-domain", "metabolomics"]:
        col_dir = tmp_path / "collections" / slug / "v1"
        col_dir.mkdir(parents=True)
        import yaml
        (col_dir / "collection.yaml").write_text(yaml.dump({
            "@type": "asb:SkillCollection",
            "@id": f"https://w3id.org/holobiomicslab/asb-skill/collection/{slug}/v1",
            "title": f"{slug.title()} Collection",
            "version": "1",
            "slug": slug,
            "domain_topics": [],
            "doi": None,
            "released_at": None,
            "lead_curators": [],
            "skills_count": 0,
            "tools_count": 0,
        }))
    cat = build_catalogue(tmp_path)
    slugs = [e["slug"] for e in cat["collections"]]
    assert slugs == sorted(slugs)


def test_catalogue_generated_at_is_iso(tmp_repo):
    from scripts.regen_catalogue import build_catalogue
    import re
    cat = build_catalogue(tmp_repo)
    ts = cat.get("generated_at", "")
    # ISO 8601 UTC: 2026-05-25T00:00:00Z
    assert re.match(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", ts), f"Bad timestamp: {ts}"


def test_catalogue_write_to_file(tmp_repo, tmp_path):
    from scripts.regen_catalogue import build_catalogue, write_catalogue
    cat = build_catalogue(tmp_repo)
    out = tmp_path / "catalogue.jsonld"
    write_catalogue(cat, out)
    reloaded = json.loads(out.read_text())
    assert reloaded["@type"] == "asb:SkillCollectionRegistry"
```

- [ ] **Step 2.2: Run tests to verify they fail (script not yet created)**

```bash
cd /Users/holobiomicslab/git/asb-skill-collections && python -m pytest tests/test_regen_catalogue.py -v 2>&1 | head -20
```

Expected: All tests FAIL with `ModuleNotFoundError: No module named 'scripts.regen_catalogue'`

- [ ] **Step 2.3: Create `scripts/regen_catalogue.py`**

```python
"""
Regenerate catalogue.jsonld at the repo root by walking collections/ directory.

JSON-LD schema: @type SkillCollectionRegistry (LinkML class from asb-schema).
Each collection entry carries: @id (w3id IRI), title, version, slug, domain_topics
(EDAM IRIs), doi, released_at, skills_count, tools_count, lead_curators[].

Output is deterministic: collections sorted alphabetically by slug; timestamps
are UTC ISO 8601 with Z suffix.

Usage:
    python scripts/regen_catalogue.py [--repo-root .] [--output catalogue.jsonld]
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
from datetime import datetime, timezone

import yaml


CATALOGUE_CONTEXT = {
    "@vocab": "https://schema.org/",
    "asb": "https://w3id.org/holobiomicslab/asb-skill/",
    "edam": "http://edamontology.org/",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "collections": {"@id": "asb:collections", "@container": "@set"},
    "domain_topics": {"@id": "asb:domainTopics", "@type": "@id", "@container": "@set"},
    "lead_curators": {"@id": "asb:leadCurators", "@container": "@set"},
    "skills_count": {"@id": "asb:skillsCount", "@type": "xsd:integer"},
    "tools_count": {"@id": "asb:toolsCount", "@type": "xsd:integer"},
    "generated_at": {"@id": "asb:generatedAt", "@type": "xsd:dateTime"},
    "released_at": {"@id": "asb:releasedAt", "@type": "xsd:dateTime"},
    "slug": "asb:slug",
}

REGISTRY_ID = "https://w3id.org/holobiomicslab/asb-skill/registry"


def _load_collection_yaml(path: pathlib.Path) -> dict:
    """Load and return a collection.yaml, raising ValueError on bad content."""
    with open(path) as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"Expected dict in {path}, got {type(data)}")
    return data


def _collection_entry(col_yaml: dict) -> dict:
    """Convert a collection.yaml dict to a catalogue entry dict."""
    entry: dict = {}

    # @id: use explicit or construct from slug + version
    iri = col_yaml.get("@id")
    if not iri:
        slug = col_yaml.get("slug", "")
        version = col_yaml.get("version", "")
        iri = f"https://w3id.org/holobiomicslab/asb-skill/collection/{slug}/v{version}"
    entry["@id"] = iri

    # Required fields
    entry["title"] = col_yaml.get("title", "")
    entry["version"] = str(col_yaml.get("version", ""))
    entry["slug"] = col_yaml.get("slug", "")
    entry["skills_count"] = int(col_yaml.get("skills_count", 0))
    entry["tools_count"] = int(col_yaml.get("tools_count", 0))

    # Optional fields
    domain_topics = col_yaml.get("domain_topics") or []
    entry["domain_topics"] = list(domain_topics)

    doi = col_yaml.get("doi")
    if doi:
        entry["doi"] = doi

    released_at = col_yaml.get("released_at")
    if released_at:
        entry["released_at"] = str(released_at)

    lead_curators = col_yaml.get("lead_curators") or []
    entry["lead_curators"] = list(lead_curators)

    return entry


def build_catalogue(repo_root: pathlib.Path) -> dict:
    """
    Walk repo_root/collections/ and build a catalogue dict.

    Args:
        repo_root: Path to the repository root.

    Returns:
        A dict suitable for serialisation as JSON-LD.
    """
    collections_dir = repo_root / "collections"
    entries: list[dict] = []

    if collections_dir.exists():
        # Walk all collection.yaml files: collections/<slug>/v<N>/collection.yaml
        for col_yaml_path in sorted(collections_dir.glob("**/collection.yaml")):
            try:
                col_data = _load_collection_yaml(col_yaml_path)
                entry = _collection_entry(col_data)
                entries.append(entry)
            except Exception as exc:
                print(
                    f"WARNING: skipping {col_yaml_path}: {exc}",
                    file=sys.stderr,
                )

    # Sort deterministically by slug
    entries.sort(key=lambda e: (e.get("slug", ""), e.get("version", "")))

    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    return {
        "@context": CATALOGUE_CONTEXT,
        "@type": "asb:SkillCollectionRegistry",
        "@id": REGISTRY_ID,
        "name": "ASB Skill Collection Registry",
        "description": (
            "Auto-generated registry of all released ASB Skill Collections."
        ),
        "generated_at": now_utc,
        "collections": entries,
    }


def write_catalogue(catalogue: dict, output_path: pathlib.Path) -> None:
    """Serialise catalogue dict to JSON-LD at output_path (deterministic, 2-space indent)."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(catalogue, f, indent=2, ensure_ascii=False)
        f.write("\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Regenerate catalogue.jsonld from collections/ directory."
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Path to the repository root (default: current directory)",
    )
    parser.add_argument(
        "--output",
        default="catalogue.jsonld",
        help="Output path for catalogue.jsonld (default: catalogue.jsonld)",
    )
    args = parser.parse_args()

    repo_root = pathlib.Path(args.repo_root).resolve()
    output_path = pathlib.Path(args.output)
    if not output_path.is_absolute():
        output_path = repo_root / output_path

    catalogue = build_catalogue(repo_root)
    write_catalogue(catalogue, output_path)

    count = len(catalogue["collections"])
    print(
        f"catalogue.jsonld written to {output_path} "
        f"({count} collection{'s' if count != 1 else ''})"
    )


if __name__ == "__main__":
    main()
```

- [ ] **Step 2.4: Run tests to verify they pass**

```bash
cd /Users/holobiomicslab/git/asb-skill-collections && python -m pytest tests/test_regen_catalogue.py -v
```

Expected: 6 tests PASS

- [ ] **Step 2.5: Commit**

```bash
git -C /Users/holobiomicslab/git/asb-skill-collections add scripts/regen_catalogue.py tests/test_regen_catalogue.py
git -C /Users/holobiomicslab/git/asb-skill-collections commit -m "feat: add regen_catalogue.py with unit tests"
```

---

## Task 3: `scripts/validate_leaderboard.py` + tests

**Files:**
- Create: `scripts/validate_leaderboard.py`
- Create: `tests/test_validate_leaderboard.py`

- [ ] **Step 3.1: Write the failing test**

Create `tests/test_validate_leaderboard.py`:

```python
"""Unit tests for validate_leaderboard.py."""
import json
import pathlib
import pytest
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

FIXTURES = pathlib.Path(__file__).parent / "fixtures"


@pytest.fixture()
def valid_lb(tmp_path):
    src = FIXTURES / "leaderboard_valid.jsonld"
    dst = tmp_path / "leaderboard.jsonld"
    import shutil
    shutil.copy(src, dst)
    return dst


@pytest.fixture()
def invalid_lb(tmp_path):
    src = FIXTURES / "leaderboard_invalid.jsonld"
    dst = tmp_path / "leaderboard.jsonld"
    import shutil
    shutil.copy(src, dst)
    return dst


def test_valid_leaderboard_passes(valid_lb):
    from scripts.validate_leaderboard import validate_leaderboard
    errors = validate_leaderboard(valid_lb)
    assert errors == [], f"Unexpected validation errors: {errors}"


def test_invalid_result_type_fails(invalid_lb):
    from scripts.validate_leaderboard import validate_leaderboard
    errors = validate_leaderboard(invalid_lb)
    assert len(errors) > 0
    assert any("result_type" in e for e in errors)


def test_missing_required_fields_fails(tmp_path):
    from scripts.validate_leaderboard import validate_leaderboard
    lb = {
        "@context": {"asb": "https://w3id.org/holobiomicslab/asb-skill/"},
        "@type": "asb:Leaderboard",
        "entries": [
            {
                "result_type": "agent",
                # missing: submitter_handle, agent_or_system_name, image_digest, submitted_at, scores
            }
        ]
    }
    path = tmp_path / "lb.jsonld"
    path.write_text(json.dumps(lb))
    errors = validate_leaderboard(path)
    assert len(errors) > 0


def test_all_three_result_types_accepted(tmp_path):
    from scripts.validate_leaderboard import validate_leaderboard
    entries = []
    for rt in ("agent", "rag_system", "hybrid"):
        entries.append({
            "result_type": rt,
            "submitter_handle": f"user-{rt}",
            "agent_or_system_name": f"System {rt}",
            "image_digest": "sha256:" + "a" * 64,
            "submitted_at": "2026-05-25T00:00:00Z",
            "scores": {"q1": 0.9},
            "metrics": {},
        })
    lb = {
        "@context": {"asb": "https://w3id.org/holobiomicslab/asb-skill/"},
        "@type": "asb:Leaderboard",
        "entries": entries,
    }
    path = tmp_path / "lb.jsonld"
    path.write_text(json.dumps(lb))
    errors = validate_leaderboard(path)
    assert errors == [], f"Unexpected errors: {errors}"


def test_scores_must_be_numeric(tmp_path):
    from scripts.validate_leaderboard import validate_leaderboard
    lb = {
        "@context": {"asb": "https://w3id.org/holobiomicslab/asb-skill/"},
        "@type": "asb:Leaderboard",
        "entries": [
            {
                "result_type": "agent",
                "submitter_handle": "user1",
                "agent_or_system_name": "Sys",
                "image_digest": "sha256:" + "b" * 64,
                "submitted_at": "2026-05-25T00:00:00Z",
                "scores": {"q1": "high"},  # invalid: string not numeric
                "metrics": {},
            }
        ],
    }
    path = tmp_path / "lb.jsonld"
    path.write_text(json.dumps(lb))
    errors = validate_leaderboard(path)
    assert len(errors) > 0
    assert any("scores" in e for e in errors)


def test_cli_exit_zero_on_valid(valid_lb):
    import subprocess
    result = subprocess.run(
        [sys.executable, "scripts/validate_leaderboard.py", str(valid_lb)],
        capture_output=True,
        text=True,
        cwd=str(pathlib.Path(__file__).parent.parent),
    )
    assert result.returncode == 0, f"stdout={result.stdout}\nstderr={result.stderr}"


def test_cli_exit_nonzero_on_invalid(invalid_lb):
    import subprocess
    result = subprocess.run(
        [sys.executable, "scripts/validate_leaderboard.py", str(invalid_lb)],
        capture_output=True,
        text=True,
        cwd=str(pathlib.Path(__file__).parent.parent),
    )
    assert result.returncode != 0, "Expected non-zero exit on invalid leaderboard"
```

- [ ] **Step 3.2: Run tests to verify they fail**

```bash
cd /Users/holobiomicslab/git/asb-skill-collections && python -m pytest tests/test_validate_leaderboard.py -v 2>&1 | head -15
```

Expected: All FAIL with `ModuleNotFoundError`

- [ ] **Step 3.3: Create `scripts/validate_leaderboard.py`**

```python
"""
Validate a benchmark/leaderboard.jsonld file against the ASB leaderboard schema.

Schema has a result_type discriminator: agent | rag_system | hybrid.

Each entry must include:
  result_type        -- "agent" | "rag_system" | "hybrid"
  submitter_handle   -- GitHub handle (string)
  submitter_orcid    -- ORCID (string, optional)
  agent_or_system_name  -- display name (string)
  image_digest       -- Docker SHA256 or commit SHA (string)
  submitted_at       -- ISO 8601 timestamp (string)
  scores             -- dict mapping challenge_id (str) to numeric score
  metrics            -- dict of any additional metrics (optional, default {})

Usage:
    python scripts/validate_leaderboard.py <leaderboard.jsonld>

Exit codes:
  0 -- valid
  1 -- validation errors found
  2 -- invocation error (file not found, JSON parse error)
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
from typing import Any

VALID_RESULT_TYPES = {"agent", "rag_system", "hybrid"}

ENTRY_REQUIRED_FIELDS = [
    "result_type",
    "submitter_handle",
    "agent_or_system_name",
    "image_digest",
    "submitted_at",
    "scores",
]


def _validate_entry(entry: dict, index: int) -> list[str]:
    """Return list of error strings for one leaderboard entry."""
    errors: list[str] = []
    prefix = f"Entry[{index}]"

    # Check result_type discriminator first
    rt = entry.get("result_type")
    if rt not in VALID_RESULT_TYPES:
        errors.append(
            f"{prefix}: result_type={rt!r} is not one of "
            f"{sorted(VALID_RESULT_TYPES)}"
        )

    # Check required fields
    for field in ENTRY_REQUIRED_FIELDS:
        if field not in entry:
            errors.append(f"{prefix}: missing required field '{field}'")

    # Validate scores: must be dict with numeric values
    scores = entry.get("scores")
    if scores is not None:
        if not isinstance(scores, dict):
            errors.append(f"{prefix}: 'scores' must be a dict, got {type(scores).__name__}")
        else:
            for challenge_id, score in scores.items():
                if not isinstance(score, (int, float)):
                    errors.append(
                        f"{prefix}: scores[{challenge_id!r}]={score!r} is not numeric"
                    )

    # Validate submitted_at: must look like ISO 8601
    submitted_at = entry.get("submitted_at", "")
    if submitted_at and not re.match(
        r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", submitted_at
    ):
        errors.append(
            f"{prefix}: submitted_at={submitted_at!r} is not a valid ISO 8601 timestamp"
        )

    # submitter_handle must be a non-empty string
    handle = entry.get("submitter_handle", "")
    if handle is not None and not isinstance(handle, str):
        errors.append(f"{prefix}: submitter_handle must be a string")
    elif not handle:
        errors.append(f"{prefix}: submitter_handle must be a non-empty string")

    return errors


def validate_leaderboard(path: pathlib.Path) -> list[str]:
    """
    Validate the leaderboard.jsonld file at path.

    Args:
        path: Path to leaderboard.jsonld.

    Returns:
        List of error strings. Empty list means valid.

    Raises:
        FileNotFoundError: if path does not exist.
        json.JSONDecodeError: if file is not valid JSON.
    """
    data = json.loads(path.read_text())
    errors: list[str] = []

    # Top-level type check
    top_type = data.get("@type", "")
    if "Leaderboard" not in str(top_type):
        errors.append(
            f"Top-level @type={top_type!r} does not contain 'Leaderboard'"
        )

    # entries must be a list
    entries = data.get("entries", [])
    if not isinstance(entries, list):
        errors.append("'entries' must be a list")
        return errors

    for i, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"Entry[{i}] is not a dict")
            continue
        errors.extend(_validate_entry(entry, i))

    return errors


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate a leaderboard.jsonld against the ASB leaderboard schema."
    )
    parser.add_argument("leaderboard", help="Path to leaderboard.jsonld")
    args = parser.parse_args()

    path = pathlib.Path(args.leaderboard)

    try:
        errors = validate_leaderboard(path)
    except FileNotFoundError:
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        sys.exit(2)
    except json.JSONDecodeError as exc:
        print(f"ERROR: JSON parse error: {exc}", file=sys.stderr)
        sys.exit(2)

    if errors:
        print(f"VALIDATION FAILED: {len(errors)} error(s)")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    else:
        entries = json.loads(path.read_text()).get("entries", [])
        print(f"OK: leaderboard is valid ({len(entries)} entries)")
        sys.exit(0)


if __name__ == "__main__":
    main()
```

- [ ] **Step 3.4: Run tests to verify they pass**

```bash
cd /Users/holobiomicslab/git/asb-skill-collections && python -m pytest tests/test_validate_leaderboard.py -v
```

Expected: 7 tests PASS

- [ ] **Step 3.5: Commit**

```bash
git -C /Users/holobiomicslab/git/asb-skill-collections add scripts/validate_leaderboard.py tests/test_validate_leaderboard.py
git -C /Users/holobiomicslab/git/asb-skill-collections commit -m "feat: add validate_leaderboard.py with result_type discriminator and unit tests"
```

---

## Task 4: `scripts/regen_career_stats.py` + tests

**Files:**
- Create: `scripts/regen_career_stats.py`
- Create: `tests/fixtures/mini_contributors.jsonld`
- Create: `tests/fixtures/mini_review.yaml`
- Create: `tests/test_regen_career_stats.py`

- [ ] **Step 4.1: Create career-stats test fixtures**

Create `tests/fixtures/mini_contributors.jsonld`:

```json
{
  "@context": {
    "@vocab": "https://schema.org/",
    "asb": "https://w3id.org/holobiomicslab/asb-skill/",
    "orcid": "https://orcid.org/",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
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
  "version": "0.1.0",
  "dateModified": "2026-05-25",
  "contributors": [
    {
      "orcid": "0000-0001-0000-0001",
      "github": "alice",
      "name": "Alice Smith",
      "asb:tier": "curator",
      "asb:total_reviews": 12,
      "asb:external_reviews": 10,
      "asb:self_authored_reviews": 2,
      "asb:identity_verified_layers": ["L1", "L2"],
      "asb:tier_since": "2026-05-01",
      "asb:collections": ["metabolomics"]
    },
    {
      "orcid": "0000-0001-0000-0002",
      "github": "bob",
      "name": "Bob Jones",
      "asb:tier": "reviewer",
      "asb:total_reviews": 3,
      "asb:external_reviews": 3,
      "asb:self_authored_reviews": 0,
      "asb:identity_verified_layers": ["L1"],
      "asb:tier_since": "2026-05-10",
      "asb:collections": ["metabolomics"]
    }
  ]
}
```

Create `tests/fixtures/mini_review.yaml`:

```yaml
reviewer:
  orcid: "0000-0001-0000-0001"
  github: alice
  tier: curator
paper:
  doi: "10.1234/test-paper"
  title: "Test Paper"
review_date: "2026-05-15"
summary: "Reviewed feature detection skills."
skill_quality: 4
evidence_spans_accurate: true
verified_claim_ids: ["urn:asb:claim:abc123"]
is_coauthor: false
author_position: null
is_corresponding: false
notes: ""
```

- [ ] **Step 4.2: Write the failing test**

Create `tests/test_regen_career_stats.py`:

```python
"""Unit tests for regen_career_stats.py."""
import json
import pathlib
import shutil
import pytest
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

FIXTURES = pathlib.Path(__file__).parent / "fixtures"


@pytest.fixture()
def tmp_repo(tmp_path):
    """A minimal fake repo with contributors.jsonld and one review."""
    shutil.copy(FIXTURES / "mini_contributors.jsonld", tmp_path / "contributors.jsonld")
    # Create a collection with a reviews dir
    reviews_dir = tmp_path / "collections" / "metabolomics" / "v1" / "reviews"
    reviews_dir.mkdir(parents=True)
    shutil.copy(FIXTURES / "mini_review.yaml", reviews_dir / "10.1234_test-paper.yaml")
    (tmp_path / "leaderboard").mkdir(exist_ok=True)
    (tmp_path / "leaderboard" / "by-domain").mkdir(exist_ok=True)
    return tmp_path


def test_career_jsonld_is_created(tmp_repo):
    from scripts.regen_career_stats import regen_career_stats
    regen_career_stats(tmp_repo)
    career_path = tmp_repo / "leaderboard" / "career.jsonld"
    assert career_path.exists()


def test_career_jsonld_has_contributors(tmp_repo):
    from scripts.regen_career_stats import regen_career_stats
    regen_career_stats(tmp_repo)
    data = json.loads((tmp_repo / "leaderboard" / "career.jsonld").read_text())
    assert "contributors" in data
    assert len(data["contributors"]) == 2


def test_career_stats_has_required_fields(tmp_repo):
    from scripts.regen_career_stats import regen_career_stats
    regen_career_stats(tmp_repo)
    data = json.loads((tmp_repo / "leaderboard" / "career.jsonld").read_text())
    alice = next(c for c in data["contributors"] if c["github"] == "alice")
    # Required aggregated fields
    assert "total_reviews" in alice
    assert "lead_curator_of" in alice
    assert "curator_of" in alice
    assert "domain_contributor_of" in alice
    assert "reviewer_of" in alice
    assert "self_authored_percentage" in alice


def test_self_authored_percentage(tmp_repo):
    from scripts.regen_career_stats import regen_career_stats
    regen_career_stats(tmp_repo)
    data = json.loads((tmp_repo / "leaderboard" / "career.jsonld").read_text())
    alice = next(c for c in data["contributors"] if c["github"] == "alice")
    # Alice: 12 total, 2 self_authored => 2/12 = ~16.67%
    assert abs(alice["self_authored_percentage"] - (2 / 12 * 100)) < 0.01


def test_annual_jsonld_is_created(tmp_repo):
    from scripts.regen_career_stats import regen_career_stats
    regen_career_stats(tmp_repo)
    # At least the current year file should exist
    from datetime import datetime
    year = datetime.now().year
    annual_path = tmp_repo / "leaderboard" / f"annual-{year}.jsonld"
    assert annual_path.exists()


def test_by_domain_jsonld_is_created(tmp_repo):
    from scripts.regen_career_stats import regen_career_stats
    regen_career_stats(tmp_repo)
    domain_path = tmp_repo / "leaderboard" / "by-domain" / "metabolomics.jsonld"
    assert domain_path.exists()


def test_by_domain_lists_reviewers(tmp_repo):
    from scripts.regen_career_stats import regen_career_stats
    regen_career_stats(tmp_repo)
    data = json.loads(
        (tmp_repo / "leaderboard" / "by-domain" / "metabolomics.jsonld").read_text()
    )
    assert "contributors" in data
    assert len(data["contributors"]) >= 1
```

- [ ] **Step 4.3: Run tests to verify they fail**

```bash
cd /Users/holobiomicslab/git/asb-skill-collections && python -m pytest tests/test_regen_career_stats.py -v 2>&1 | head -15
```

Expected: All FAIL with `ModuleNotFoundError`

- [ ] **Step 4.4: Create `scripts/regen_career_stats.py`**

```python
"""
Rebuild career-stats leaderboard files from contributors.jsonld + per-collection reviews.

Outputs:
  leaderboard/career.jsonld              -- all-time career stats per contributor
  leaderboard/annual-<year>.jsonld       -- per-year breakdown (uses review_date)
  leaderboard/by-domain/<domain>.jsonld  -- domain-scoped contributor list

Aggregated fields per contributor entry:
  total_reviews, lead_curator_of[], curator_of[], domain_contributor_of[],
  reviewer_of[], self_authored_percentage

Usage:
    python scripts/regen_career_stats.py [--repo-root .]
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
from collections import defaultdict
from datetime import datetime, timezone
from typing import Any

import yaml


def _load_json(path: pathlib.Path) -> dict:
    with open(path) as f:
        return json.load(f)


def _write_json(data: dict, path: pathlib.Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def _load_review_yaml(path: pathlib.Path) -> dict | None:
    try:
        with open(path) as f:
            return yaml.safe_load(f)
    except Exception as exc:
        print(f"WARNING: skipping review {path}: {exc}", file=sys.stderr)
        return None


def _collect_reviews(repo_root: pathlib.Path) -> list[dict]:
    """Walk all reviews/*.yaml files under collections/ and return list of parsed dicts."""
    reviews: list[dict] = []
    collections_dir = repo_root / "collections"
    if not collections_dir.exists():
        return reviews
    for review_path in sorted(collections_dir.glob("**/reviews/*.yaml")):
        review = _load_review_yaml(review_path)
        if review is None:
            continue
        # Annotate with collection slug (parent of reviews/)
        # Path pattern: collections/<slug>/v<N>/reviews/<doi>.yaml
        parts = review_path.parts
        try:
            col_idx = parts.index("collections")
            slug = parts[col_idx + 1]
        except (ValueError, IndexError):
            slug = "unknown"
        review["_collection_slug"] = slug
        reviews.append(review)
    return reviews


def _build_contributor_stats(
    contributors: list[dict],
    reviews: list[dict],
) -> list[dict]:
    """Build aggregated career stats for each contributor."""
    # Index contributors by ORCID
    by_orcid: dict[str, dict] = {}
    for contrib in contributors:
        orcid = contrib.get("orcid", "").replace("https://orcid.org/", "").strip()
        if orcid:
            by_orcid[orcid] = contrib

    # Aggregate review counts per (orcid, collection) pair
    # These come from contributors.jsonld (already accumulated by tier_update.py)
    # We re-derive role lists from the tier field

    result: list[dict] = []
    for contrib in contributors:
        orcid = contrib.get("orcid", "").replace("https://orcid.org/", "").strip()
        tier = contrib.get("asb:tier", "reviewer")
        collections = contrib.get("asb:collections", []) or []
        total = int(contrib.get("asb:total_reviews", 0))
        self_authored = int(contrib.get("asb:self_authored_reviews", 0))

        # Self-authored percentage
        pct = (self_authored / total * 100) if total > 0 else 0.0

        # Role lists: assign collection to the appropriate role bucket
        lead_curator_of: list[str] = []
        curator_of: list[str] = []
        domain_contributor_of: list[str] = []
        reviewer_of: list[str] = []

        for col in collections:
            if tier == "lead_curator":
                lead_curator_of.append(col)
            elif tier == "curator":
                curator_of.append(col)
            elif tier == "domain_contributor":
                domain_contributor_of.append(col)
            else:
                reviewer_of.append(col)

        result.append({
            "orcid": orcid,
            "github": contrib.get("github", ""),
            "name": contrib.get("name", ""),
            "tier": tier,
            "total_reviews": total,
            "self_authored_percentage": round(pct, 4),
            "lead_curator_of": lead_curator_of,
            "curator_of": curator_of,
            "domain_contributor_of": domain_contributor_of,
            "reviewer_of": reviewer_of,
        })
    return result


def _build_annual(
    contributors: list[dict],
    reviews: list[dict],
    year: int,
) -> dict:
    """Build per-year stats for the given year using review_date fields."""
    # Count reviews per orcid for this year
    year_counts: dict[str, int] = defaultdict(int)
    year_collections: dict[str, set] = defaultdict(set)

    for review in reviews:
        rd = review.get("review_date", "") or ""
        try:
            review_year = int(str(rd)[:4])
        except (ValueError, TypeError):
            continue
        if review_year != year:
            continue
        reviewer_info = review.get("reviewer", {}) or {}
        orcid = reviewer_info.get("orcid", "").replace("https://orcid.org/", "").strip()
        if orcid:
            year_counts[orcid] += 1
            year_collections[orcid].add(review.get("_collection_slug", "unknown"))

    # Build contributor entries for this year
    year_contributors: list[dict] = []
    for contrib in contributors:
        orcid = contrib.get("orcid", "").replace("https://orcid.org/", "").strip()
        n = year_counts.get(orcid, 0)
        if n == 0:
            continue
        year_contributors.append({
            "orcid": orcid,
            "github": contrib.get("github", ""),
            "name": contrib.get("name", ""),
            "tier": contrib.get("asb:tier", "reviewer"),
            "reviews_this_year": n,
            "collections": sorted(year_collections.get(orcid, set())),
        })
    year_contributors.sort(key=lambda c: -c["reviews_this_year"])
    return year_contributors


def _build_by_domain(
    contributors: list[dict],
    domain: str,
) -> list[dict]:
    """Return contributor entries scoped to one domain/collection slug."""
    result: list[dict] = []
    for contrib in contributors:
        collections = contrib.get("asb:collections", []) or []
        if domain not in collections:
            continue
        orcid = contrib.get("orcid", "").replace("https://orcid.org/", "").strip()
        result.append({
            "orcid": orcid,
            "github": contrib.get("github", ""),
            "name": contrib.get("name", ""),
            "tier": contrib.get("asb:tier", "reviewer"),
            "total_reviews": int(contrib.get("asb:total_reviews", 0)),
        })
    result.sort(key=lambda c: -c["total_reviews"])
    return result


JSONLD_CONTEXT = {
    "@vocab": "https://schema.org/",
    "asb": "https://w3id.org/holobiomicslab/asb-skill/",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "generated_at": {"@id": "asb:generatedAt", "@type": "xsd:dateTime"},
}


def regen_career_stats(repo_root: pathlib.Path) -> None:
    """
    Rebuild all leaderboard/*.jsonld files.

    Args:
        repo_root: Path to the repository root.
    """
    contributors_path = repo_root / "contributors.jsonld"
    if not contributors_path.exists():
        print(f"ERROR: contributors.jsonld not found at {contributors_path}", file=sys.stderr)
        sys.exit(1)

    registry = _load_json(contributors_path)
    contributors: list[dict] = registry.get("contributors", [])

    reviews = _collect_reviews(repo_root)

    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    current_year = datetime.now(timezone.utc).year

    # 1. career.jsonld
    career_stats = _build_contributor_stats(contributors, reviews)
    career_data: dict[str, Any] = {
        "@context": JSONLD_CONTEXT,
        "@type": "asb:CareerLeaderboard",
        "@id": "https://w3id.org/holobiomicslab/asb-skill/leaderboard/career",
        "name": "ASB Contributor Career Stats",
        "generated_at": now_utc,
        "contributors": career_stats,
    }
    _write_json(career_data, repo_root / "leaderboard" / "career.jsonld")

    # 2. annual-<year>.jsonld for current year (and any year with reviews)
    years_seen: set[int] = set()
    years_seen.add(current_year)
    for review in reviews:
        rd = review.get("review_date", "") or ""
        try:
            years_seen.add(int(str(rd)[:4]))
        except (ValueError, TypeError):
            pass

    for year in sorted(years_seen):
        year_contribs = _build_annual(contributors, reviews, year)
        annual_data = {
            "@context": JSONLD_CONTEXT,
            "@type": "asb:AnnualLeaderboard",
            "@id": f"https://w3id.org/holobiomicslab/asb-skill/leaderboard/annual-{year}",
            "name": f"ASB Contributor Leaderboard {year}",
            "year": year,
            "generated_at": now_utc,
            "contributors": year_contribs,
        }
        _write_json(annual_data, repo_root / "leaderboard" / f"annual-{year}.jsonld")

    # 3. by-domain/<slug>.jsonld — one per unique domain in asb:collections
    domains: set[str] = set()
    for contrib in contributors:
        for col in (contrib.get("asb:collections") or []):
            if col:
                domains.add(col)

    for domain in sorted(domains):
        domain_contribs = _build_by_domain(contributors, domain)
        domain_data = {
            "@context": JSONLD_CONTEXT,
            "@type": "asb:DomainLeaderboard",
            "@id": f"https://w3id.org/holobiomicslab/asb-skill/leaderboard/by-domain/{domain}",
            "name": f"ASB {domain.title()} Domain Contributors",
            "domain": domain,
            "generated_at": now_utc,
            "contributors": domain_contribs,
        }
        _write_json(
            domain_data,
            repo_root / "leaderboard" / "by-domain" / f"{domain}.jsonld",
        )

    print(
        f"Career stats written: {len(contributors)} contributors, "
        f"{len(years_seen)} year(s), {len(domains)} domain(s)"
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Rebuild leaderboard career stats from contributors.jsonld + reviews."
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Path to the repository root (default: current directory)",
    )
    args = parser.parse_args()
    repo_root = pathlib.Path(args.repo_root).resolve()
    regen_career_stats(repo_root)


if __name__ == "__main__":
    main()
```

- [ ] **Step 4.5: Run tests to verify they pass**

```bash
cd /Users/holobiomicslab/git/asb-skill-collections && python -m pytest tests/test_regen_career_stats.py -v
```

Expected: 7 tests PASS

- [ ] **Step 4.6: Commit**

```bash
git -C /Users/holobiomicslab/git/asb-skill-collections add scripts/regen_career_stats.py tests/fixtures/mini_contributors.jsonld tests/fixtures/mini_review.yaml tests/test_regen_career_stats.py
git -C /Users/holobiomicslab/git/asb-skill-collections commit -m "feat: add regen_career_stats.py with career/annual/by-domain leaderboard outputs and unit tests"
```

---

## Task 5: `templates/leaderboard.jsonld.template`

**Files:**
- Create: `templates/leaderboard.jsonld.template`

- [ ] **Step 5.1: Create the template**

Create `templates/leaderboard.jsonld.template`:

```json
{
  "_doc": "ASB Benchmark Leaderboard — JSON-LD template. Copy to collections/<slug>/vN/benchmark/leaderboard.jsonld and fill in. Remove all _doc keys before submitting.",

  "@context": {
    "_doc": "JSON-LD context. Do not modify.",
    "asb": "https://w3id.org/holobiomicslab/asb-skill/",
    "xsd": "http://www.w3.org/2001/XMLSchema#"
  },

  "@type": "asb:Leaderboard",
  "@id": "https://w3id.org/holobiomicslab/asb-skill/collection/SLUG/vN/leaderboard",
  "_doc_id": "Replace SLUG and N with the collection slug and version number.",

  "collection": "https://w3id.org/holobiomicslab/asb-skill/collection/SLUG/vN",
  "_doc_collection": "The canonical @id of the collection this leaderboard belongs to.",

  "entries": [
    {
      "_doc": "One entry per submitted result. Duplicate this block for each entry.",

      "result_type": "agent",
      "_doc_result_type": "DISCRIMINATOR — must be one of: 'agent' | 'rag_system' | 'hybrid'. 'agent' = executes benchmark tasks end-to-end. 'rag_system' = retrieves claims from benchmark/claims/. 'hybrid' = both.",

      "submitter_handle": "your-github-handle",
      "_doc_submitter_handle": "Your GitHub username. Required.",

      "submitter_orcid": null,
      "_doc_submitter_orcid": "Your ORCID (optional but recommended for credit). Format: '0000-0001-2345-6789'.",

      "agent_or_system_name": "MyAgent v1.0",
      "_doc_agent_or_system_name": "Human-readable name of your agent or RAG system, including version.",

      "image_digest": "sha256:AAAA...ZZZZ",
      "_doc_image_digest": "Docker image digest (sha256:<64-hex>) for reproducibility, OR a git commit SHA. Required.",

      "submitted_at": "2026-01-01T00:00:00Z",
      "_doc_submitted_at": "ISO 8601 UTC timestamp when this result was produced. Required.",

      "scores": {
        "_doc": "Map of challenge_id → numeric score (float in [0,1] unless otherwise specified). challenge_id matches benchmark/tasks/<paper-doi>/ or benchmark/claims/<topic>/.",
        "task-001": 0.0,
        "claim-q001": 0.0
      },

      "metrics": {
        "_doc": "Optional additional metrics. Common fields: latency_s, cost_usd, recall_at_5, mrr, ndcg.",
        "latency_s": 0.0,
        "cost_usd": 0.0
      }
    }
  ]
}
```

- [ ] **Step 5.2: Verify the template is valid JSON (after stripping _doc keys mentally — it is valid as-is)**

```bash
cd /Users/holobiomicslab/git/asb-skill-collections && python -c "
import json, pathlib
data = json.loads(pathlib.Path('templates/leaderboard.jsonld.template').read_text())
print('leaderboard.jsonld.template parses as valid JSON OK')
print('Top-level keys:', list(data.keys()))
"
```

Expected: Parses OK; lists keys including `@context`, `@type`, `entries`.

- [ ] **Step 5.3: Commit**

```bash
git -C /Users/holobiomicslab/git/asb-skill-collections add templates/leaderboard.jsonld.template
git -C /Users/holobiomicslab/git/asb-skill-collections commit -m "feat: add leaderboard.jsonld.template with result_type discriminator and inline _doc schema"
```

---

## Task 6: GitHub Actions — `release.yml`

**Files:**
- Create: `.github/workflows/release.yml`

- [ ] **Step 6.1: Create `.github/workflows/release.yml`**

```yaml
# release.yml — triggered on tags matching <collection-slug>-v<N>
# Steps:
#   1. Validate the tagged collection passes all CI gates
#   2. Call regen_catalogue.py and commit the updated catalogue.jsonld
#   3. Upload the collection directory to Zenodo (fail-soft if ZENODO_TOKEN missing)
#   4. Update CITATION.cff with the minted DOI
#   5. Trigger mirror-to-hf.yml via workflow_dispatch
name: Release

on:
  push:
    tags:
      - "*-v[0-9]*"

permissions:
  contents: write

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
          token: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract collection slug and version from tag
        id: tag
        run: |
          TAG="${GITHUB_REF_NAME}"
          # Tag format: <slug>-v<N>  e.g. metabolomics-v1
          VERSION="${TAG##*-v}"
          SLUG="${TAG%-v${VERSION}}"
          echo "slug=${SLUG}" >> "$GITHUB_OUTPUT"
          echo "version=${VERSION}" >> "$GITHUB_OUTPUT"
          echo "tag=${TAG}" >> "$GITHUB_OUTPUT"
          echo "Releasing slug=${SLUG} version=${VERSION}"

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: pip install -e ".[test]"

      - name: Run CI validation gates
        run: |
          python -m pytest tests/ -v
          echo "All CI gates passed"

      - name: Regenerate catalogue.jsonld
        run: |
          python scripts/regen_catalogue.py --repo-root . --output catalogue.jsonld
          echo "catalogue.jsonld regenerated"

      - name: Commit updated catalogue.jsonld
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add catalogue.jsonld
          if git diff --cached --quiet; then
            echo "No catalogue changes to commit"
          else
            git commit -m "chore: regen catalogue.jsonld for ${{ steps.tag.outputs.tag }}"
            git push origin HEAD:main
          fi

      - name: Upload to Zenodo (fail-soft if token missing)
        id: zenodo
        env:
          ZENODO_TOKEN: ${{ secrets.ZENODO_TOKEN }}
          COLLECTION_SLUG: ${{ steps.tag.outputs.slug }}
          COLLECTION_VERSION: ${{ steps.tag.outputs.version }}
        run: |
          if [ -z "${ZENODO_TOKEN}" ]; then
            echo "ZENODO_TOKEN not set — skipping Zenodo upload"
            echo "doi=" >> "$GITHUB_OUTPUT"
            exit 0
          fi
          python - <<'PYEOF'
          import json, os, pathlib, requests, sys, zipfile, tempfile

          token = os.environ["ZENODO_TOKEN"]
          slug = os.environ["COLLECTION_SLUG"]
          version = os.environ["COLLECTION_VERSION"]
          collection_dir = pathlib.Path("collections") / slug / f"v{version}"

          if not collection_dir.exists():
            print(f"Collection dir not found: {collection_dir}", file=sys.stderr)
            sys.exit(1)

          headers = {"Authorization": f"Bearer {token}"}
          base_url = "https://zenodo.org/api"

          # Create a new deposition
          resp = requests.post(f"{base_url}/deposit/depositions",
              json={}, headers=headers, timeout=30)
          resp.raise_for_status()
          dep = resp.json()
          dep_id = dep["id"]
          bucket_url = dep["links"]["bucket"]
          print(f"Created Zenodo deposition {dep_id}")

          # Zip the collection directory
          with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tf:
            zip_path = tf.name
          with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for f in sorted(collection_dir.rglob("*")):
              if f.is_file():
                zf.write(f, f.relative_to(collection_dir.parent.parent))

          # Upload zip
          with open(zip_path, "rb") as fh:
            upload_resp = requests.put(
              f"{bucket_url}/{slug}-v{version}.zip",
              data=fh,
              headers=headers,
              timeout=120,
            )
            upload_resp.raise_for_status()
          print(f"Uploaded {slug}-v{version}.zip")

          # Set metadata
          citation_path = collection_dir / "CITATION.cff"
          title = f"ASB Skill Collection: {slug} v{version}"
          creators = [{"name": "HolobiomicsLab"}]
          if citation_path.exists():
            import yaml
            cff = yaml.safe_load(citation_path.read_text())
            title = cff.get("title", title)
            if "authors" in cff:
              creators = [{"name": f"{a.get('family-names', '')} {a.get('given-names', '')}".strip(),
                           "orcid": a.get("orcid", "")} for a in cff["authors"] if a]

          meta = {
            "metadata": {
              "title": title,
              "upload_type": "dataset",
              "description": f"ASB Skill Collection release: {slug} version {version}.",
              "creators": creators,
              "keywords": ["agentic-ai", "scientific-agents", slug, "asb"],
              "license": "apache-2.0",
              "version": version,
            }
          }
          meta_resp = requests.put(
            f"{base_url}/deposit/depositions/{dep_id}",
            json=meta,
            headers={"Content-Type": "application/json", **headers},
            timeout=30,
          )
          meta_resp.raise_for_status()

          # Publish
          pub_resp = requests.post(
            f"{base_url}/deposit/depositions/{dep_id}/actions/publish",
            headers=headers,
            timeout=30,
          )
          pub_resp.raise_for_status()
          doi = pub_resp.json().get("doi", "")
          print(f"Published. DOI: {doi}")

          # Write DOI to GITHUB_OUTPUT
          with open(os.environ["GITHUB_OUTPUT"], "a") as gho:
            gho.write(f"doi={doi}\n")
          PYEOF

      - name: Update CITATION.cff with minted DOI
        if: steps.zenodo.outputs.doi != ''
        env:
          DOI: ${{ steps.zenodo.outputs.doi }}
          COLLECTION_SLUG: ${{ steps.tag.outputs.slug }}
          COLLECTION_VERSION: ${{ steps.tag.outputs.version }}
        run: |
          python - <<'PYEOF'
          import os, pathlib, re

          doi = os.environ["DOI"]
          slug = os.environ["COLLECTION_SLUG"]
          version = os.environ["COLLECTION_VERSION"]

          # Update root CITATION.cff if it exists
          root_cff = pathlib.Path("CITATION.cff")
          if root_cff.exists():
            text = root_cff.read_text()
            text = re.sub(r'^(doi:\s*).*$', f'doi: {doi}', text, flags=re.MULTILINE)
            root_cff.write_text(text)
            print(f"Updated root CITATION.cff with doi: {doi}")

          # Update collection-level CITATION.cff
          col_cff = pathlib.Path("collections") / slug / f"v{version}" / "CITATION.cff"
          if col_cff.exists():
            text = col_cff.read_text()
            text = re.sub(r'^(doi:\s*).*$', f'doi: {doi}', text, flags=re.MULTILINE)
            col_cff.write_text(text)
            print(f"Updated collection CITATION.cff with doi: {doi}")
          PYEOF
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add CITATION.cff "collections/${{ steps.tag.outputs.slug }}/v${{ steps.tag.outputs.version }}/CITATION.cff" 2>/dev/null || true
          if git diff --cached --quiet; then
            echo "No CITATION.cff changes"
          else
            git commit -m "chore: update CITATION.cff with Zenodo DOI ${{ steps.zenodo.outputs.doi }}"
            git push origin HEAD:main
          fi

      - name: Trigger mirror-to-hf.yml
        if: always()
        uses: actions/github-script@v7
        with:
          script: |
            await github.rest.actions.createWorkflowDispatch({
              owner: context.repo.owner,
              repo: context.repo.repo,
              workflow_id: 'mirror-to-hf.yml',
              ref: 'main',
              inputs: {
                collection_slug: '${{ steps.tag.outputs.slug }}',
                collection_version: '${{ steps.tag.outputs.version }}'
              }
            });
            console.log('Triggered mirror-to-hf.yml for ${{ steps.tag.outputs.tag }}');
```

- [ ] **Step 6.2: Validate YAML syntax**

```bash
cd /Users/holobiomicslab/git/asb-skill-collections && python -c "
import yaml, pathlib
data = yaml.safe_load(pathlib.Path('.github/workflows/release.yml').read_text())
print('release.yml YAML syntax OK')
print('Trigger:', list(data['on'].keys()))
print('Job:', list(data['jobs'].keys()))
"
```

Expected: `release.yml YAML syntax OK`

- [ ] **Step 6.3: Commit**

```bash
git -C /Users/holobiomicslab/git/asb-skill-collections add .github/workflows/release.yml
git -C /Users/holobiomicslab/git/asb-skill-collections commit -m "ci: add release.yml workflow (tag → validate → catalogue regen → Zenodo → CITATION.cff → trigger HF mirror)"
```

---

## Task 7: GitHub Actions — `leaderboard-validate.yml`

**Files:**
- Create: `.github/workflows/leaderboard-validate.yml`

- [ ] **Step 7.1: Create `.github/workflows/leaderboard-validate.yml`**

```yaml
# leaderboard-validate.yml — validates leaderboard.jsonld on PRs that touch it.
# Posts a PR comment with the validation report (pass or fail with error list).
name: Leaderboard Validate

on:
  pull_request:
    paths:
      - "collections/**/benchmark/leaderboard.jsonld"

permissions:
  contents: read
  pull-requests: write

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: pip install -e ".[test]"

      - name: Find changed leaderboard files
        id: changed
        run: |
          # List leaderboard.jsonld files changed in this PR
          git fetch origin ${{ github.base_ref }} --depth=1
          FILES=$(git diff --name-only origin/${{ github.base_ref }}...HEAD \
            | grep 'benchmark/leaderboard.jsonld' || true)
          echo "files=${FILES}" >> "$GITHUB_OUTPUT"
          echo "Changed leaderboard files: ${FILES}"

      - name: Validate each leaderboard file
        id: validate
        run: |
          ERRORS=""
          REPORT=""
          FILES="${{ steps.changed.outputs.files }}"

          if [ -z "$FILES" ]; then
            echo "No leaderboard files changed — nothing to validate"
            echo "report=No leaderboard.jsonld files changed." >> "$GITHUB_OUTPUT"
            exit 0
          fi

          for FILE in $FILES; do
            if [ ! -f "$FILE" ]; then
              continue
            fi
            echo "Validating: $FILE"
            OUTPUT=$(python scripts/validate_leaderboard.py "$FILE" 2>&1)
            EXIT_CODE=$?
            REPORT="${REPORT}\n### \`${FILE}\`\n\`\`\`\n${OUTPUT}\n\`\`\`\n"
            if [ $EXIT_CODE -ne 0 ]; then
              ERRORS="${ERRORS} ${FILE}"
            fi
          done

          # Use heredoc for multi-line output
          {
            echo "report<<EOF"
            printf '%b' "$REPORT"
            echo "EOF"
          } >> "$GITHUB_OUTPUT"

          if [ -n "$ERRORS" ]; then
            echo "failed=true" >> "$GITHUB_OUTPUT"
          else
            echo "failed=false" >> "$GITHUB_OUTPUT"
          fi

      - name: Post PR comment
        uses: actions/github-script@v7
        with:
          script: |
            const failed = '${{ steps.validate.outputs.failed }}' === 'true';
            const report = `${{ steps.validate.outputs.report }}`;
            const header = failed
              ? '## Leaderboard Validation FAILED'
              : '## Leaderboard Validation PASSED';
            const body = `${header}\n\n${report}`;
            await github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: body
            });

      - name: Fail job if validation errors
        if: steps.validate.outputs.failed == 'true'
        run: |
          echo "Leaderboard validation failed — see PR comment for details"
          exit 1
```

- [ ] **Step 7.2: Validate YAML syntax**

```bash
cd /Users/holobiomicslab/git/asb-skill-collections && python -c "
import yaml, pathlib
data = yaml.safe_load(pathlib.Path('.github/workflows/leaderboard-validate.yml').read_text())
print('leaderboard-validate.yml YAML syntax OK')
print('Trigger:', list(data['on'].keys()))
"
```

Expected: `leaderboard-validate.yml YAML syntax OK`

- [ ] **Step 7.3: Commit**

```bash
git -C /Users/holobiomicslab/git/asb-skill-collections add .github/workflows/leaderboard-validate.yml
git -C /Users/holobiomicslab/git/asb-skill-collections commit -m "ci: add leaderboard-validate.yml (PR path filter + result_type schema validation + PR comment)"
```

---

## Task 8: GitHub Actions — `career-stats-regen.yml`

**Files:**
- Create: `.github/workflows/career-stats-regen.yml`

- [ ] **Step 8.1: Create `.github/workflows/career-stats-regen.yml`**

```yaml
# career-stats-regen.yml — rebuilds leaderboard/ files on push to main when reviews
# or contributors.jsonld change.
name: Career Stats Regen

on:
  push:
    branches:
      - main
    paths:
      - "collections/**/reviews/*.yaml"
      - "contributors.jsonld"

permissions:
  contents: write

jobs:
  regen:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          token: ${{ secrets.GITHUB_TOKEN }}

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: pip install -e ".[test]"

      - name: Rebuild leaderboard stats
        run: |
          python scripts/regen_career_stats.py --repo-root .
          echo "Career stats rebuilt"

      - name: Commit updated leaderboard files
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add leaderboard/
          if git diff --cached --quiet; then
            echo "No leaderboard changes to commit"
          else
            git commit -m "chore: regen leaderboard stats [skip ci]"
            git push origin HEAD:main
          fi
```

- [ ] **Step 8.2: Validate YAML syntax**

```bash
cd /Users/holobiomicslab/git/asb-skill-collections && python -c "
import yaml, pathlib
data = yaml.safe_load(pathlib.Path('.github/workflows/career-stats-regen.yml').read_text())
print('career-stats-regen.yml YAML syntax OK')
print('Trigger:', list(data['on'].keys()))
"
```

Expected: `career-stats-regen.yml YAML syntax OK`

- [ ] **Step 8.3: Commit**

```bash
git -C /Users/holobiomicslab/git/asb-skill-collections add .github/workflows/career-stats-regen.yml
git -C /Users/holobiomicslab/git/asb-skill-collections commit -m "ci: add career-stats-regen.yml (push-to-main path filter + auto-commit leaderboard/ updates)"
```

---

## Task 9: GitHub Pages site + `pages.yml`

**Files:**
- Create: `docs-site/index.html`
- Create: `docs-site/app.js`
- Create: `docs-site/style.css`
- Create: `.github/workflows/pages.yml`

- [ ] **Step 9.1: Create `docs-site/style.css`**

```css
/* ASB Skill Collections — minimal Pages site */
*, *::before, *::after { box-sizing: border-box; }

body {
  font-family: system-ui, -apple-system, sans-serif;
  margin: 0;
  padding: 0 1rem 2rem;
  max-width: 900px;
  margin-inline: auto;
  color: #1a1a1a;
  background: #fff;
}

h1 { font-size: 1.6rem; margin-top: 2rem; }
h2 { font-size: 1.2rem; margin-top: 1.8rem; border-bottom: 1px solid #e0e0e0; padding-bottom: .3rem; }

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
  margin-top: .8rem;
}
th, td {
  text-align: left;
  padding: .4rem .6rem;
  border-bottom: 1px solid #e0e0e0;
}
th { background: #f5f5f5; font-weight: 600; }
tr:hover td { background: #fafafa; }

a { color: #0066cc; }
.badge { display: inline-block; padding: .15rem .5rem; border-radius: 3px;
         font-size: .75rem; background: #e8f0fe; color: #1a3d7c; }
.error { color: #c62828; font-style: italic; }
.loading { color: #666; font-style: italic; }
```

- [ ] **Step 9.2: Create `docs-site/app.js`**

```javascript
// app.js — fetch catalogue.jsonld + career.jsonld from GitHub raw and render tables.
// Paths are relative to the repo root on the main branch.
const REPO = "HolobiomicsLab/asb-skill-collections";
const BRANCH = "main";
const RAW = `https://raw.githubusercontent.com/${REPO}/${BRANCH}`;

async function fetchJSON(path) {
  const url = `${RAW}/${path}`;
  const resp = await fetch(url);
  if (!resp.ok) throw new Error(`HTTP ${resp.status} for ${url}`);
  return resp.json();
}

function el(tag, attrs = {}, ...children) {
  const e = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) e.setAttribute(k, v);
  for (const c of children) {
    if (typeof c === "string") e.appendChild(document.createTextNode(c));
    else if (c) e.appendChild(c);
  }
  return e;
}

function makeTable(headers, rows) {
  const thead = el("thead", {}, el("tr", {}, ...headers.map(h => el("th", {}, h))));
  const tbody = el("tbody", {}, ...rows.map(r =>
    el("tr", {}, ...r.map(c => el("td", {}, ...(Array.isArray(c) ? c : [c]))))
  ));
  return el("table", {}, thead, tbody);
}

async function renderCatalogue() {
  const section = document.getElementById("catalogue");
  try {
    const data = await fetchJSON("catalogue.jsonld");
    const cols = data.collections || [];
    if (cols.length === 0) {
      section.innerHTML += "<p class='loading'>No collections released yet.</p>";
      return;
    }
    const rows = cols.map(c => {
      const doiLink = c.doi
        ? [el("a", { href: `https://doi.org/${c.doi}`, target: "_blank" }, c.doi)]
        : ["—"];
      const topics = (c.domain_topics || []).map(t => {
        const label = t.split("/").pop();
        return el("span", { class: "badge" }, label);
      });
      return [
        [el("a", { href: c["@id"] || "#", target: "_blank" }, c.title || c.slug)],
        c.version || "—",
        String(c.skills_count || 0),
        String(c.tools_count || 0),
        topics.length ? topics : ["—"],
        doiLink,
        c.released_at ? [c.released_at.substring(0, 10)] : ["pending"],
      ];
    });
    section.appendChild(makeTable(
      ["Collection", "Version", "Skills", "Tools", "EDAM Topics", "DOI", "Released"],
      rows
    ));
    section.querySelector(".loading")?.remove();
  } catch (err) {
    section.querySelector(".loading").className = "error";
    section.querySelector(".error").textContent = `Failed to load catalogue: ${err.message}`;
  }
}

async function renderLeaderboard() {
  const section = document.getElementById("leaderboard");
  try {
    const data = await fetchJSON("leaderboard/career.jsonld");
    const contribs = data.contributors || [];
    if (contribs.length === 0) {
      section.innerHTML += "<p class='loading'>No contributors yet.</p>";
      return;
    }
    const rows = contribs.map(c => {
      const tierBadge = el("span", { class: "badge" }, c.tier || "reviewer");
      const collections = [
        ...(c.lead_curator_of || []),
        ...(c.curator_of || []),
        ...(c.domain_contributor_of || []),
        ...(c.reviewer_of || []),
      ];
      const colBadges = collections.length
        ? collections.map(col => el("span", { class: "badge" }, col))
        : ["—"];
      const pct = typeof c.self_authored_percentage === "number"
        ? `${c.self_authored_percentage.toFixed(1)}%`
        : "—";
      const orcidLink = c.orcid
        ? [el("a", { href: `https://orcid.org/${c.orcid}`, target: "_blank" }, c.orcid)]
        : ["—"];
      return [
        c.name || c.github || "—",
        orcidLink,
        [tierBadge],
        String(c.total_reviews || 0),
        pct,
        colBadges,
      ];
    });
    section.appendChild(makeTable(
      ["Name", "ORCID", "Tier", "Reviews", "Self-authored %", "Collections"],
      rows
    ));
    section.querySelector(".loading")?.remove();
  } catch (err) {
    section.querySelector(".loading").className = "error";
    section.querySelector(".error").textContent = `Failed to load leaderboard: ${err.message}`;
  }
}

document.addEventListener("DOMContentLoaded", () => {
  renderCatalogue();
  renderLeaderboard();
});
```

- [ ] **Step 9.3: Create `docs-site/index.html`**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>ASB Skill Collections</title>
  <link rel="stylesheet" href="style.css" />
</head>
<body>
  <h1>ASB Skill Collections</h1>
  <p>
    Curated, evidence-grounded scientific-agent skill and benchmark collections
    maintained by <a href="https://github.com/HolobiomicsLab" target="_blank">HolobiomicsLab</a>.
    Source: <a href="https://github.com/HolobiomicsLab/asb-skill-collections" target="_blank">GitHub</a>.
  </p>

  <h2>Collections</h2>
  <div id="catalogue">
    <p class="loading">Loading catalogue...</p>
  </div>

  <h2>Contributor Leaderboard</h2>
  <div id="leaderboard">
    <p class="loading">Loading leaderboard...</p>
  </div>

  <script src="app.js"></script>
</body>
</html>
```

- [ ] **Step 9.4: Create `.github/workflows/pages.yml`**

```yaml
# pages.yml — deploy docs-site/ to GitHub Pages on push to main.
name: GitHub Pages

on:
  push:
    branches:
      - main
    paths:
      - "docs-site/**"
      - "catalogue.jsonld"
      - "leaderboard/**"

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Pages
        uses: actions/configure-pages@v4

      - name: Upload Pages artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: "docs-site"

      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

- [ ] **Step 9.5: Validate YAML syntax for pages.yml**

```bash
cd /Users/holobiomicslab/git/asb-skill-collections && python -c "
import yaml, pathlib
data = yaml.safe_load(pathlib.Path('.github/workflows/pages.yml').read_text())
print('pages.yml YAML syntax OK')
print('Trigger:', list(data['on'].keys()))
"
```

Expected: `pages.yml YAML syntax OK`

- [ ] **Step 9.6: Commit**

```bash
git -C /Users/holobiomicslab/git/asb-skill-collections add docs-site/ .github/workflows/pages.yml
git -C /Users/holobiomicslab/git/asb-skill-collections commit -m "feat: add GitHub Pages site (docs-site/) and pages.yml deploy workflow"
```

---

## Task 10: Full test suite + final push

**Files:** (no new files)

- [ ] **Step 10.1: Run the complete test suite**

```bash
cd /Users/holobiomicslab/git/asb-skill-collections && python -m pytest tests/ -v --tb=short
```

Expected: All tests PASS (22 pre-existing + ~20 new = ~42 total). Zero failures.

- [ ] **Step 10.2: Validate all three new workflow YAML files are syntactically valid**

```bash
cd /Users/holobiomicslab/git/asb-skill-collections && python -c "
import yaml, pathlib
for wf in ['release.yml', 'leaderboard-validate.yml', 'career-stats-regen.yml']:
    data = yaml.safe_load(pathlib.Path(f'.github/workflows/{wf}').read_text())
    print(f'{wf}: OK — jobs: {list(data[\"jobs\"].keys())}')
"
```

Expected: All three print OK.

- [ ] **Step 10.3: Confirm attestation.yaml.template has `verified_claim_ids[]` slot with gold-tier comment**

```bash
cd /Users/holobiomicslab/git/asb-skill-collections && grep -A3 "verified_claim_ids" templates/attestation.yaml.template
```

Expected: Shows the multi-line comment including "Gold-tier" and the `verified_claim_ids: []` line.

- [ ] **Step 10.4: Run smoke test of regen_catalogue.py against the repo itself**

```bash
cd /Users/holobiomicslab/git/asb-skill-collections && python scripts/regen_catalogue.py --repo-root . --output /tmp/catalogue_smoke.jsonld && python -c "import json; d=json.load(open('/tmp/catalogue_smoke.jsonld')); print('Smoke OK — type:', d['@type'], '— collections:', len(d['collections']))"
```

Expected: `Smoke OK — type: asb:SkillCollectionRegistry — collections: 0` (collections/ is empty at this point)

- [ ] **Step 10.5: Push branch**

```bash
git -C /Users/holobiomicslab/git/asb-skill-collections push -u origin wave3/catalogue-leaderboard
```

Expected: Branch pushed to remote. If conflict with main, run:
```bash
git -C /Users/holobiomicslab/git/asb-skill-collections fetch origin && git -C /Users/holobiomicslab/git/asb-skill-collections rebase origin/main && git -C /Users/holobiomicslab/git/asb-skill-collections push -u origin wave3/catalogue-leaderboard
```

---

## Self-Review Against Spec

**Spec coverage check:**

| Spec item | Task covering it |
|---|---|
| `scripts/regen_catalogue.py` — SkillCollectionRegistry, @id IRI, title, version, domain_topics, doi, released_at, skills_count, tools_count, lead_curators[], alphabetical order, ISO timestamps, unit tests | Task 2 |
| `scripts/validate_leaderboard.py` — result_type discriminator, required fields, fail-fast, unit tests valid+invalid | Task 3 |
| `scripts/regen_career_stats.py` — career.jsonld, annual-<year>.jsonld, by-domain/<domain>.jsonld, total reviews, lead_curator_of[], curator_of[], domain_contributor_of[], reviewer_of[], self_authored_percentage, unit tests | Task 4 |
| `templates/leaderboard.jsonld.template` — empty template with _doc keys, result_type discriminator | Task 5 |
| `templates/attestation.yaml.template` — add verified_claim_ids[] slot, gold-tier comment §10.4 | Task 1 |
| `.github/workflows/release.yml` — tag trigger, validate, regen catalogue, commit, Zenodo upload, fail-soft on missing token, CITATION.cff update, trigger mirror-to-hf.yml via workflow_dispatch | Task 6 |
| `.github/workflows/leaderboard-validate.yml` — PR path filter, validate_leaderboard.py, PR comment | Task 7 |
| `.github/workflows/career-stats-regen.yml` — push/main path filter, regen, commit | Task 8 |
| GitHub Pages site — docs-site/, renders catalogue.jsonld + leaderboard/career.jsonld as HTML | Task 9 |
| `.github/workflows/pages.yml` — deploy docs-site/ to Pages | Task 9 |
| Branch wave3/catalogue-leaderboard | Task 1 step 1.1 |
| TDD — failing test before implementation | Tasks 2, 3, 4 each have fail step |
| No touching mirror-to-hf.yml, templates/hf-space/, README.md | Verified — none of those files appear in this plan |

**Placeholder scan:** No TBD/TODO/placeholder patterns found. All code blocks are complete.

**Type consistency:** `build_catalogue(repo_root: Path) → dict`, `write_catalogue(catalogue: dict, output_path: Path) → None`, `validate_leaderboard(path: Path) → list[str]`, `regen_career_stats(repo_root: Path) → None` — names are consistent across tasks 2/3/4 and their respective test files.
