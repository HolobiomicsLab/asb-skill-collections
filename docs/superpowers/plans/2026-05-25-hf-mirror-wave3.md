# HuggingFace Mirror + Leaderboard Space (Wave 3b) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add HuggingFace Dataset mirroring and per-collection leaderboard Space to `asb-skill-collections`, including `mirror-to-hf.yml` CI, `generate_hf_dataset_card.py`, `generate_hf_space_config.py`, `templates/hf-space/`, `templates/HOWTO-RUN.md.template`, and a README Distribution section.

**Architecture:** A GitHub Action triggers on release tags, extracts the released collection path from the tag name (e.g. `metabolomics-v1` → `collections/metabolomics/v1/`), then uses the `huggingface_hub` Python library to create/update a HF Dataset repo and upload the directory. Two generator scripts (one per Python file) produce the Dataset card README and the HF Space skeleton, respectively. A Gradio `app.py` template reads `leaderboard.jsonld` live from GitHub raw URL and renders a sortable table. Both scripts have full unit test coverage with mocked HF API calls.

**Tech Stack:** Python 3.12, `huggingface_hub>=0.23`, `gradio>=4.0`, `pyyaml>=6.0`, `requests>=2.31`, `pytest>=8.0`, `unittest.mock` (stdlib), `responses` for HTTP mocking.

---

## File map

| Action | File |
|---|---|
| Create | `.github/workflows/mirror-to-hf.yml` |
| Create | `scripts/generate_hf_dataset_card.py` |
| Create | `scripts/generate_hf_space_config.py` |
| Create | `templates/hf-space/app.py` |
| Create | `templates/hf-space/requirements.txt` |
| Create | `templates/hf-space/README.md` |
| Create | `templates/HOWTO-RUN.md.template` |
| Modify | `README.md` |
| Modify | `pyproject.toml` |
| Create | `tests/test_generate_hf_dataset_card.py` |
| Create | `tests/test_generate_hf_space_config.py` |

---

## Task 1: Branch setup

**Files:** none

- [ ] **Step 1: Create and checkout the feature branch**

```bash
git -C /Users/holobiomicslab/git/asb-skill-collections checkout -b wave3/hf-mirror
```

Expected: `Switched to a new branch 'wave3/hf-mirror'`

---

## Task 2: Update `pyproject.toml` to add `huggingface_hub` dependency and dev extras

**Files:**
- Modify: `pyproject.toml`

- [ ] **Step 1: Write the failing test first**

The test simply imports `generate_hf_dataset_card` module; it will fail until the module exists. Place it at:
`tests/test_generate_hf_dataset_card.py` (created in Task 3 — run Task 2 step 2 first to install deps).

For now, add the dependency so `pip install` works.

- [ ] **Step 2: Edit `pyproject.toml`**

Replace the `[project.optional-dependencies]` block (currently only `test`) with:

```toml
[project.optional-dependencies]
hf = [
    "huggingface_hub>=0.23",
]
dev = [
    "pytest>=8.0",
    "pytest-cov",
    "responses>=0.25",
    "huggingface_hub>=0.23",
]
test = [
    "pytest>=8.0",
    "pytest-cov",
    "responses>=0.25",
]
```

- [ ] **Step 3: Install dev extras**

```bash
cd /Users/holobiomicslab/git/asb-skill-collections && pip install -e ".[dev]" -q
```

Expected: exits 0, `huggingface_hub` installed.

- [ ] **Step 4: Commit**

```bash
git -C /Users/holobiomicslab/git/asb-skill-collections add pyproject.toml
git -C /Users/holobiomicslab/git/asb-skill-collections commit -m "chore: add huggingface_hub to dev deps"
```

---

## Task 3: `scripts/generate_hf_dataset_card.py` — Dataset card generator

**Files:**
- Create: `scripts/generate_hf_dataset_card.py`
- Create: `tests/test_generate_hf_dataset_card.py`

The script reads `collection.yaml` (a YAML file at the collection root with at minimum keys: `title`, `slug`, `version`, `domain`, `description`) and optionally `CITATION.cff` (with keys: `doi`, `authors`, `title`) and emits a README.md string containing HF Dataset card YAML frontmatter + a short description body.

### Frontmatter schema (§11.1 of Design Doc v2)

```yaml
---
license: apache-2.0
tags: [agentic-ai, scientific-agents, <domain>, asb]
task_categories: [text-generation, question-answering]
size_categories: [n<1K]
language: [en]
pretty_name: "ASB <Title> Benchmark v<N>"
configs:
  - config_name: skills
    data_files: "skills/**/SKILL.md"
  - config_name: benchmark
    data_files: "benchmark/tasks/**/task.md"
  - config_name: tools
    data_files: "tools/**/*.yaml"
homepage: "https://github.com/HolobiomicsLab/asb-skill-collections"
doi: "<DOI or PLACEHOLDER>"
---
```

- [ ] **Step 1: Write the failing tests**

Create `tests/test_generate_hf_dataset_card.py`:

```python
"""Tests for generate_hf_dataset_card.py"""
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch

# Add scripts dir to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import generate_hf_dataset_card as gen


MINIMAL_COLLECTION_YAML = """
title: "Metabolomics Skills"
slug: metabolomics
version: 1
domain: metabolomics
description: "Curated metabolomics skills for scientific AI agents."
"""

MINIMAL_CITATION_CFF = """
cff-version: 1.2.0
title: "ASB Metabolomics v1"
doi: "10.5281/zenodo.12345"
authors:
  - family-names: Nothias
    given-names: Louis-Felix
    orcid: https://orcid.org/0000-0001-6191-3389
"""


class TestGenerateDatasetCard(unittest.TestCase):

    def test_minimal_collection_yaml_only(self):
        """generate_readme from collection.yaml only, no CITATION.cff"""
        result = gen.generate_readme(
            collection=gen.parse_collection_yaml(MINIMAL_COLLECTION_YAML),
            citation=None,
        )
        assert "license: apache-2.0" in result
        assert "agentic-ai" in result
        assert "metabolomics" in result
        assert "ASB Metabolomics Skills Benchmark v1" in result
        assert "config_name: skills" in result
        assert "config_name: benchmark" in result
        assert "config_name: tools" in result
        assert "PLACEHOLDER" in result  # no doi without CITATION.cff

    def test_with_citation_cff(self):
        """DOI from CITATION.cff appears in frontmatter"""
        result = gen.generate_readme(
            collection=gen.parse_collection_yaml(MINIMAL_COLLECTION_YAML),
            citation=gen.parse_citation_cff(MINIMAL_CITATION_CFF),
        )
        assert "10.5281/zenodo.12345" in result
        assert "PLACEHOLDER" not in result

    def test_tags_include_domain_and_asb(self):
        collection = gen.parse_collection_yaml(MINIMAL_COLLECTION_YAML)
        result = gen.generate_readme(collection=collection, citation=None)
        assert "scientific-agents" in result
        assert "asb" in result

    def test_pretty_name_format(self):
        collection = gen.parse_collection_yaml(MINIMAL_COLLECTION_YAML)
        result = gen.generate_readme(collection=collection, citation=None)
        assert 'pretty_name: "ASB Metabolomics Skills Benchmark v1"' in result

    def test_parse_collection_yaml_missing_required_key(self):
        """Missing required key raises ValueError"""
        with self.assertRaises(ValueError):
            gen.parse_collection_yaml("title: Test\n")  # missing slug, version, domain

    def test_configs_data_files(self):
        collection = gen.parse_collection_yaml(MINIMAL_COLLECTION_YAML)
        result = gen.generate_readme(collection=collection, citation=None)
        assert 'data_files: "skills/**/SKILL.md"' in result
        assert 'data_files: "benchmark/tasks/**/task.md"' in result
        assert 'data_files: "tools/**/*.yaml"' in result

    def test_body_contains_description(self):
        collection = gen.parse_collection_yaml(MINIMAL_COLLECTION_YAML)
        result = gen.generate_readme(collection=collection, citation=None)
        assert "Curated metabolomics skills" in result

    def test_generate_readme_returns_string(self):
        collection = gen.parse_collection_yaml(MINIMAL_COLLECTION_YAML)
        result = gen.generate_readme(collection=collection, citation=None)
        assert isinstance(result, str)
        assert result.startswith("---\n")


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd /Users/holobiomicslab/git/asb-skill-collections && python -m pytest tests/test_generate_hf_dataset_card.py -v 2>&1 | head -30
```

Expected: `ModuleNotFoundError: No module named 'generate_hf_dataset_card'`

- [ ] **Step 3: Write `scripts/generate_hf_dataset_card.py`**

```python
"""
Generate HuggingFace Dataset card README.md from collection.yaml + CITATION.cff.

Usage:
    python scripts/generate_hf_dataset_card.py \\
        --collection collections/metabolomics/v1/collection.yaml \\
        [--citation collections/metabolomics/v1/CITATION.cff] \\
        [--output collections/metabolomics/v1/hf_README.md]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

import yaml


REQUIRED_COLLECTION_KEYS = {"title", "slug", "version", "domain"}


def parse_collection_yaml(text: str) -> dict:
    """Parse collection.yaml text. Raises ValueError if required keys missing."""
    data = yaml.safe_load(text)
    if not data:
        raise ValueError("Empty collection YAML")
    missing = REQUIRED_COLLECTION_KEYS - set(data.keys())
    if missing:
        raise ValueError(f"collection.yaml missing required keys: {missing}")
    return data


def parse_citation_cff(text: str) -> dict:
    """Parse CITATION.cff text. Returns dict (may be empty on parse error)."""
    try:
        return yaml.safe_load(text) or {}
    except yaml.YAMLError:
        return {}


def generate_readme(collection: dict, citation: Optional[dict]) -> str:
    """
    Generate the full HF Dataset card README.md content.

    Parameters
    ----------
    collection : dict
        Parsed collection.yaml (must contain title, slug, version, domain).
    citation : dict or None
        Parsed CITATION.cff (may be None or empty).

    Returns
    -------
    str
        Full README.md content (YAML frontmatter + body).
    """
    title = collection["title"]
    slug = collection["slug"]
    version = collection["version"]
    domain = str(collection["domain"]).lower()
    description = collection.get("description", "")

    doi = "PLACEHOLDER"
    if citation:
        doi = citation.get("doi", "PLACEHOLDER") or "PLACEHOLDER"

    pretty_name = f"ASB {title} Benchmark v{version}"

    tags = ["agentic-ai", "scientific-agents", domain, "asb"]
    tags_str = "[" + ", ".join(tags) + "]"

    frontmatter = f"""---
license: apache-2.0
tags: {tags_str}
task_categories: [text-generation, question-answering]
size_categories: [n<1K]
language: [en]
pretty_name: "{pretty_name}"
configs:
  - config_name: skills
    data_files: "skills/**/SKILL.md"
  - config_name: benchmark
    data_files: "benchmark/tasks/**/task.md"
  - config_name: tools
    data_files: "tools/**/*.yaml"
homepage: "https://github.com/HolobiomicsLab/asb-skill-collections"
doi: "{doi}"
---"""

    body = f"""
# {pretty_name}

{description}

## Programmatic access

```python
from datasets import load_dataset

ds_skills = load_dataset("HolobiomicsLab/asb-{slug}-v{version}", "skills")
ds_bench  = load_dataset("HolobiomicsLab/asb-{slug}-v{version}", "benchmark")
ds_tools  = load_dataset("HolobiomicsLab/asb-{slug}-v{version}", "tools")
```

## Citation

If you use this dataset in research, please cite using the DOI above.
See `CITATION.cff` in the source repository for the full citation.

## License

Apache-2.0 for synthesis layer; fair-use for verbatim paper quotes.
"""

    return frontmatter + "\n" + body


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--collection", required=True, help="Path to collection.yaml")
    parser.add_argument("--citation", default=None, help="Path to CITATION.cff (optional)")
    parser.add_argument("--output", default=None, help="Output path (default: stdout)")
    args = parser.parse_args(argv)

    collection_path = Path(args.collection)
    if not collection_path.exists():
        print(f"ERROR: collection.yaml not found: {collection_path}", file=sys.stderr)
        return 1

    collection = parse_collection_yaml(collection_path.read_text())

    citation = None
    if args.citation:
        cit_path = Path(args.citation)
        if cit_path.exists():
            citation = parse_citation_cff(cit_path.read_text())

    readme = generate_readme(collection=collection, citation=citation)

    if args.output:
        Path(args.output).write_text(readme)
        print(f"Written to {args.output}")
    else:
        print(readme)

    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
cd /Users/holobiomicslab/git/asb-skill-collections && python -m pytest tests/test_generate_hf_dataset_card.py -v
```

Expected: 8 tests, all PASS.

- [ ] **Step 5: Commit**

```bash
git -C /Users/holobiomicslab/git/asb-skill-collections add scripts/generate_hf_dataset_card.py tests/test_generate_hf_dataset_card.py
git -C /Users/holobiomicslab/git/asb-skill-collections commit -m "feat: add generate_hf_dataset_card.py with unit tests"
```

---

## Task 4: `scripts/generate_hf_space_config.py` — Space metadata + app.py generator

**Files:**
- Create: `scripts/generate_hf_space_config.py`
- Create: `tests/test_generate_hf_space_config.py`

The script generates two strings: (1) the HF Space `README.md` frontmatter+header, and (2) the `app.py` content for a Gradio leaderboard Space. It accepts a `collection` dict and a `leaderboard_url` string (the GitHub raw URL of `leaderboard.jsonld`).

The generated `app.py` does NOT embed data — it fetches `leaderboard_url` at runtime via `requests`.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_generate_hf_space_config.py`:

```python
"""Tests for generate_hf_space_config.py"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import generate_hf_space_config as gen


MINIMAL_COLLECTION = {
    "title": "Metabolomics Skills",
    "slug": "metabolomics",
    "version": 1,
    "domain": "metabolomics",
    "description": "Curated metabolomics skills.",
}

LEADERBOARD_URL = (
    "https://raw.githubusercontent.com/HolobiomicsLab/"
    "asb-skill-collections/main/collections/metabolomics/v1/benchmark/leaderboard.jsonld"
)


class TestGenerateSpaceConfig(unittest.TestCase):

    def test_space_readme_has_yaml_frontmatter(self):
        readme = gen.generate_space_readme(
            collection=MINIMAL_COLLECTION,
            leaderboard_url=LEADERBOARD_URL,
        )
        assert readme.startswith("---\n")
        assert "sdk: gradio" in readme
        assert "title:" in readme

    def test_space_readme_sdk_version(self):
        readme = gen.generate_space_readme(
            collection=MINIMAL_COLLECTION,
            leaderboard_url=LEADERBOARD_URL,
        )
        assert "sdk_version:" in readme

    def test_space_readme_has_leaderboard_env(self):
        readme = gen.generate_space_readme(
            collection=MINIMAL_COLLECTION,
            leaderboard_url=LEADERBOARD_URL,
        )
        assert "LEADERBOARD_URL" in readme

    def test_app_py_fetches_leaderboard_url(self):
        app_py = gen.generate_app_py(
            collection=MINIMAL_COLLECTION,
            leaderboard_url=LEADERBOARD_URL,
        )
        assert "LEADERBOARD_URL" in app_py
        assert "requests" in app_py
        assert "gradio" in app_py or "gr" in app_py

    def test_app_py_renders_sortable_table(self):
        app_py = gen.generate_app_py(
            collection=MINIMAL_COLLECTION,
            leaderboard_url=LEADERBOARD_URL,
        )
        # Must have a DataFrame or table component
        assert "DataFrame" in app_py or "dataframe" in app_py.lower()

    def test_app_py_has_result_type_filter(self):
        app_py = gen.generate_app_py(
            collection=MINIMAL_COLLECTION,
            leaderboard_url=LEADERBOARD_URL,
        )
        assert "result_type" in app_py

    def test_app_py_has_submit_button(self):
        app_py = gen.generate_app_py(
            collection=MINIMAL_COLLECTION,
            leaderboard_url=LEADERBOARD_URL,
        )
        assert "Submit" in app_py or "submit" in app_py.lower()

    def test_app_py_submit_opens_github_issue(self):
        app_py = gen.generate_app_py(
            collection=MINIMAL_COLLECTION,
            leaderboard_url=LEADERBOARD_URL,
        )
        assert "github.com" in app_py
        assert "issues" in app_py.lower() or "new" in app_py.lower()

    def test_generate_space_config_returns_both(self):
        result = gen.generate_space_config(
            collection=MINIMAL_COLLECTION,
            leaderboard_url=LEADERBOARD_URL,
        )
        assert "readme" in result
        assert "app_py" in result
        assert isinstance(result["readme"], str)
        assert isinstance(result["app_py"], str)

    def test_space_title_includes_collection_title(self):
        readme = gen.generate_space_readme(
            collection=MINIMAL_COLLECTION,
            leaderboard_url=LEADERBOARD_URL,
        )
        assert "Metabolomics" in readme


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd /Users/holobiomicslab/git/asb-skill-collections && python -m pytest tests/test_generate_hf_space_config.py -v 2>&1 | head -20
```

Expected: `ModuleNotFoundError: No module named 'generate_hf_space_config'`

- [ ] **Step 3: Write `scripts/generate_hf_space_config.py`**

```python
"""
Generate HuggingFace Space skeleton (README.md + app.py) for a per-collection leaderboard.

Usage:
    python scripts/generate_hf_space_config.py \\
        --collection collections/metabolomics/v1/collection.yaml \\
        --leaderboard-url https://raw.githubusercontent.com/.../leaderboard.jsonld \\
        --output templates/hf-space/
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml


def generate_space_readme(collection: dict, leaderboard_url: str) -> str:
    """
    Generate HF Space README.md with YAML frontmatter.

    Parameters
    ----------
    collection : dict
        Parsed collection.yaml with title, slug, version, domain.
    leaderboard_url : str
        GitHub raw URL of leaderboard.jsonld for this collection.

    Returns
    -------
    str
        Full README.md for the HF Space.
    """
    title = collection["title"]
    slug = collection["slug"]
    version = collection["version"]
    space_title = f"ASB {title} v{version} Leaderboard"

    frontmatter = f"""---
title: {space_title}
emoji: 🔬
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: "4.42.0"
app_file: app.py
pinned: false
license: apache-2.0
tags:
  - leaderboard
  - agentic-ai
  - scientific-agents
  - asb
  - {collection.get('domain', slug).lower()}
variables:
  LEADERBOARD_URL: "{leaderboard_url}"
---"""

    body = f"""
# {space_title}

Live leaderboard for the [ASB {title} v{version}](https://github.com/HolobiomicsLab/asb-skill-collections/tree/main/collections/{slug}/v{version}) collection.

Tracks agent (`result_type: agent`), RAG-system (`result_type: rag_system`), and hybrid (`result_type: hybrid`) results.

## Submit a result

Click **Submit a result** in the app to open a pre-filled GitHub Issue.
A maintainer will review and merge your PR to `leaderboard.jsonld`.

## Data source

Leaderboard data is fetched live from:
`{leaderboard_url}`
"""

    return frontmatter + "\n" + body


def generate_app_py(collection: dict, leaderboard_url: str) -> str:
    """
    Generate the Gradio app.py for a per-collection leaderboard Space.

    Parameters
    ----------
    collection : dict
        Parsed collection.yaml with title, slug, version.
    leaderboard_url : str
        GitHub raw URL of leaderboard.jsonld.

    Returns
    -------
    str
        Contents of app.py.
    """
    title = collection["title"]
    slug = collection["slug"]
    version = collection["version"]

    issue_url = (
        f"https://github.com/HolobiomicsLab/asb-skill-collections/issues/new"
        f"?template=submit-agent-result.md"
        f"&labels=leaderboard-submission,{slug}"
        f"&title=Result+submission:+ASB+{slug}+v{version}"
    )

    return f'''"""
Gradio leaderboard for ASB {title} v{version}.
Reads leaderboard.jsonld live from GitHub raw URL.
"""
import os
import json

import gradio as gr
import pandas as pd
import requests

LEADERBOARD_URL = os.environ.get(
    "LEADERBOARD_URL",
    "{leaderboard_url}",
)

GITHUB_ISSUE_URL = "{issue_url}"

RESULT_TYPES = ["all", "agent", "rag_system", "hybrid"]

COLUMNS = [
    "system_name",
    "result_type",
    "overall_score",
    "task_score",
    "claim_score",
    "workflow_tier",
    "submitted_by",
    "date",
]


def fetch_leaderboard(leaderboard_url: str = LEADERBOARD_URL) -> list[dict]:
    """Fetch leaderboard.jsonld from GitHub raw URL."""
    try:
        resp = requests.get(leaderboard_url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        # Support both a bare list and a JSON-LD graph with @graph key
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            return data.get("@graph", data.get("results", [data]))
        return []
    except Exception as exc:
        print(f"WARNING: could not fetch leaderboard: {{exc}}")
        return []


def load_table(result_type_filter: str = "all") -> pd.DataFrame:
    """Load leaderboard into a DataFrame, optionally filtered by result_type."""
    entries = fetch_leaderboard()
    if not entries:
        return pd.DataFrame(columns=COLUMNS)
    rows = []
    for entry in entries:
        if result_type_filter != "all":
            if entry.get("result_type") != result_type_filter:
                continue
        row = {{col: entry.get(col, "") for col in COLUMNS}}
        rows.append(row)
    df = pd.DataFrame(rows, columns=COLUMNS)
    if "overall_score" in df.columns and not df.empty:
        df = df.sort_values("overall_score", ascending=False).reset_index(drop=True)
    return df


def refresh_table(result_type_filter: str) -> pd.DataFrame:
    return load_table(result_type_filter)


with gr.Blocks(title="ASB {title} v{version} Leaderboard") as demo:
    gr.Markdown("# ASB {title} v{version} Leaderboard")
    gr.Markdown(
        "Results for [asb-skill-collections/{slug}/v{version}]"
        "(https://github.com/HolobiomicsLab/asb-skill-collections/tree/main/collections/{slug}/v{version}). "
        "Sorted by `overall_score` descending."
    )

    with gr.Row():
        result_type_dd = gr.Dropdown(
            choices=RESULT_TYPES,
            value="all",
            label="Filter by result_type",
        )
        refresh_btn = gr.Button("Refresh", variant="secondary")

    table = gr.DataFrame(
        value=load_table("all"),
        interactive=False,
        wrap=True,
    )

    with gr.Row():
        submit_btn = gr.Button("Submit a result", variant="primary")
        submit_info = gr.Markdown("")

    result_type_dd.change(
        fn=refresh_table,
        inputs=[result_type_dd],
        outputs=[table],
    )
    refresh_btn.click(
        fn=refresh_table,
        inputs=[result_type_dd],
        outputs=[table],
    )

    def on_submit():
        return gr.Markdown(
            f"Open a GitHub Issue to submit your result: "
            f"[Click here]({GITHUB_ISSUE_URL})"
        )

    submit_btn.click(fn=on_submit, inputs=[], outputs=[submit_info])


if __name__ == "__main__":
    demo.launch()
'''


def generate_space_config(collection: dict, leaderboard_url: str) -> dict[str, str]:
    """
    Convenience wrapper returning both Space files as a dict.

    Returns
    -------
    dict with keys "readme" and "app_py".
    """
    return {
        "readme": generate_space_readme(collection=collection, leaderboard_url=leaderboard_url),
        "app_py": generate_app_py(collection=collection, leaderboard_url=leaderboard_url),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--collection", required=True, help="Path to collection.yaml")
    parser.add_argument(
        "--leaderboard-url",
        required=True,
        help="GitHub raw URL of leaderboard.jsonld",
    )
    parser.add_argument(
        "--output",
        default="templates/hf-space/",
        help="Output directory (default: templates/hf-space/)",
    )
    args = parser.parse_args(argv)

    collection_path = Path(args.collection)
    if not collection_path.exists():
        print(f"ERROR: collection.yaml not found: {collection_path}", file=sys.stderr)
        return 1

    import generate_hf_dataset_card as dc  # noqa: local import after path setup

    collection = dc.parse_collection_yaml(collection_path.read_text())
    config = generate_space_config(
        collection=collection,
        leaderboard_url=args.leaderboard_url,
    )

    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "README.md").write_text(config["readme"])
    (out_dir / "app.py").write_text(config["app_py"])
    print(f"Written Space files to {out_dir}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
cd /Users/holobiomicslab/git/asb-skill-collections && python -m pytest tests/test_generate_hf_space_config.py -v
```

Expected: 10 tests, all PASS.

- [ ] **Step 5: Commit**

```bash
git -C /Users/holobiomicslab/git/asb-skill-collections add scripts/generate_hf_space_config.py tests/test_generate_hf_space_config.py
git -C /Users/holobiomicslab/git/asb-skill-collections commit -m "feat: add generate_hf_space_config.py with unit tests"
```

---

## Task 5: `templates/hf-space/` — static Space template files

**Files:**
- Create: `templates/hf-space/app.py`
- Create: `templates/hf-space/requirements.txt`
- Create: `templates/hf-space/README.md`

These are *template* files that get copied into a per-collection HF Space by `mirror-to-hf.yml`. The `app.py` here is a concrete generic version (not parameterized), suitable for metabolomics-v1.

- [ ] **Step 1: Create `templates/hf-space/requirements.txt`**

```
gradio>=4.42.0
requests>=2.31.0
pyyaml>=6.0
pandas>=2.0
```

- [ ] **Step 2: Create `templates/hf-space/README.md`**

This is the HF Space card YAML frontmatter template (literal `{{TITLE}}` etc. are replaced by the workflow):

```markdown
---
title: "{{SPACE_TITLE}}"
emoji: 🔬
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: "4.42.0"
app_file: app.py
pinned: false
license: apache-2.0
tags:
  - leaderboard
  - agentic-ai
  - scientific-agents
  - asb
variables:
  LEADERBOARD_URL: "{{LEADERBOARD_URL}}"
---

# {{SPACE_TITLE}}

Live leaderboard for the ASB skill collection. Tracks agent, RAG-system, and hybrid results.

Click **Submit a result** in the app to open a GitHub Issue.
```

- [ ] **Step 3: Create `templates/hf-space/app.py`**

This is the generic/concrete fallback app (uses env var `LEADERBOARD_URL` with no slug-specific default):

```python
"""
ASB Collection Leaderboard — Gradio Space app.
Reads leaderboard.jsonld live from LEADERBOARD_URL env var.
"""
import os
import json

import gradio as gr
import pandas as pd
import requests

LEADERBOARD_URL = os.environ.get("LEADERBOARD_URL", "")
GITHUB_ISSUES_URL = os.environ.get(
    "GITHUB_ISSUES_URL",
    "https://github.com/HolobiomicsLab/asb-skill-collections/issues/new"
    "?template=submit-agent-result.md&labels=leaderboard-submission",
)

RESULT_TYPES = ["all", "agent", "rag_system", "hybrid"]

COLUMNS = [
    "system_name",
    "result_type",
    "overall_score",
    "task_score",
    "claim_score",
    "workflow_tier",
    "submitted_by",
    "date",
]


def fetch_leaderboard() -> list[dict]:
    if not LEADERBOARD_URL:
        return []
    try:
        resp = requests.get(LEADERBOARD_URL, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            return data.get("@graph", data.get("results", []))
        return []
    except Exception as exc:
        print(f"WARNING: could not fetch leaderboard: {exc}")
        return []


def load_table(result_type_filter: str = "all") -> pd.DataFrame:
    entries = fetch_leaderboard()
    if not entries:
        return pd.DataFrame(columns=COLUMNS)
    rows = []
    for entry in entries:
        if result_type_filter != "all" and entry.get("result_type") != result_type_filter:
            continue
        rows.append({col: entry.get(col, "") for col in COLUMNS})
    df = pd.DataFrame(rows, columns=COLUMNS)
    if "overall_score" in df.columns and not df.empty:
        df = df.sort_values("overall_score", ascending=False).reset_index(drop=True)
    return df


with gr.Blocks(title="ASB Leaderboard") as demo:
    gr.Markdown("# ASB Collection Leaderboard")

    with gr.Row():
        result_type_dd = gr.Dropdown(
            choices=RESULT_TYPES, value="all", label="Filter by result_type"
        )
        refresh_btn = gr.Button("Refresh", variant="secondary")

    table = gr.DataFrame(value=load_table("all"), interactive=False, wrap=True)

    with gr.Row():
        submit_btn = gr.Button("Submit a result", variant="primary")
        submit_info = gr.Markdown("")

    result_type_dd.change(
        fn=lambda rt: load_table(rt), inputs=[result_type_dd], outputs=[table]
    )
    refresh_btn.click(
        fn=lambda rt: load_table(rt), inputs=[result_type_dd], outputs=[table]
    )

    def on_submit():
        return gr.Markdown(f"[Open GitHub Issue to submit]({GITHUB_ISSUES_URL})")

    submit_btn.click(fn=on_submit, inputs=[], outputs=[submit_info])


if __name__ == "__main__":
    demo.launch()
```

- [ ] **Step 4: Commit**

```bash
git -C /Users/holobiomicslab/git/asb-skill-collections add templates/hf-space/
git -C /Users/holobiomicslab/git/asb-skill-collections commit -m "feat: add templates/hf-space/ (Gradio leaderboard Space template)"
```

---

## Task 6: `templates/HOWTO-RUN.md.template`

**Files:**
- Create: `templates/HOWTO-RUN.md.template`

This template is copied into `benchmark/` at the collection root during collection promotion.

- [ ] **Step 1: Create `templates/HOWTO-RUN.md.template`**

```markdown
# How to Run — ASB {{COLLECTION_TITLE}} Benchmark v{{COLLECTION_VERSION}}

This guide explains how to install the skill collection, run agent challenges, run the
claim-retrieval eval, and submit results to the leaderboard.

## 1. Install the skill collection

In Claude Code (or any ASB-compatible agent environment):

```
/plugin install {{COLLECTION_SLUG}}-v{{COLLECTION_VERSION}}@HolobiomicsLab/asb-skill-collections
```

This installs the `_router/SKILL.md` as the default router plus all domain skills.

## 2. Run agent challenges (benchmark/tasks/)

Each task lives in `benchmark/tasks/<paper-doi>/`.

```bash
# List available tasks
ls benchmark/tasks/

# Inspect a task
cat benchmark/tasks/<paper-doi>/task.md
cat benchmark/tasks/<paper-doi>/workflow_metadata.yaml

# Run with Snakemake (full-tier tasks only)
snakemake --snakefile benchmark/tasks/<paper-doi>/workflow.smk \
    --directory benchmark/tasks/<paper-doi>/ \
    --cores 4

# Evaluate results
asb run-eval benchmark/tasks/<paper-doi>/eval.json \
    --results-dir benchmark/tasks/<paper-doi>/outputs/
```

## 3. Run the claim-retrieval eval (benchmark/claims/)

```bash
# Per-paper eval (silver tier)
python -m pytest benchmark/claims/per_paper/ -v

# Or with a RAG system implementing the ASB eval API:
asb eval-claims \
    --claims benchmark/claims/per_paper/ \
    --rag-endpoint http://localhost:8765 \
    --output results/claim_eval_$(date +%Y%m%d).json
```

See `benchmark/claims/HOWTO-EVAL.md` for metric definitions (MRR, NDCG, recall@k).

## 4. Submit results to the leaderboard

1. Run your agent or RAG system against the benchmark.
2. Collect your results in the format required by `leaderboard.jsonld` (see schema in `benchmark/leaderboard.jsonld`).
3. Open a GitHub Issue using the template:
   https://github.com/HolobiomicsLab/asb-skill-collections/issues/new?template=submit-agent-result.md
4. A maintainer will review your PR and merge it to `benchmark/leaderboard.jsonld`.

Your result will appear on the live HuggingFace Space leaderboard:
https://huggingface.co/spaces/HolobiomicsLab/asb-{{COLLECTION_SLUG}}-v{{COLLECTION_VERSION}}-leaderboard

## 5. Cite

If you benchmark against this collection, please cite:

```
{{COLLECTION_CITATION}}
```

See the Zenodo DOI at the top of the collection README for the machine-readable citation.
```

- [ ] **Step 2: Commit**

```bash
git -C /Users/holobiomicslab/git/asb-skill-collections add templates/HOWTO-RUN.md.template
git -C /Users/holobiomicslab/git/asb-skill-collections commit -m "feat: add templates/HOWTO-RUN.md.template for benchmark instructions"
```

---

## Task 7: `.github/workflows/mirror-to-hf.yml`

**Files:**
- Create: `.github/workflows/mirror-to-hf.yml`

The workflow triggers on push of tags matching `*-v[0-9]*` (e.g. `metabolomics-v1`).

**Tag → collection path logic:**
- Tag `metabolomics-v1` → slug=`metabolomics`, version=`1` → path=`collections/metabolomics/v1/`
- Tag `proteomics-v2` → slug=`proteomics`, version=`2` → path=`collections/proteomics/v2/`
- The tag must be `<slug>-v<N>` (exactly one hyphen+v before the digits).

**Fail-soft:** if `HF_TOKEN` secret is absent, the step logs a warning and exits 0 (does not block release).

- [ ] **Step 1: Create `.github/workflows/mirror-to-hf.yml`**

```yaml
# mirror-to-hf.yml — Push a release tag to HuggingFace Datasets
# Triggered on tags matching <slug>-v<N> (e.g. metabolomics-v1).
# Requires HF_TOKEN secret in repo settings.
# Fail-soft: missing HF_TOKEN logs a warning but does not block the release.

name: Mirror to HuggingFace

on:
  push:
    tags:
      - "*-v[0-9]*"

permissions:
  contents: read

jobs:
  mirror:
    name: Mirror collection to HF Datasets
    runs-on: ubuntu-22.04

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Python 3.12
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install huggingface_hub
        run: pip install "huggingface_hub>=0.23" pyyaml

      - name: Parse tag → slug + version
        id: tag_parse
        run: |
          TAG="${GITHUB_REF_NAME}"
          # Validate format: must be <slug>-v<N>
          if [[ ! "$TAG" =~ ^([a-z][a-z0-9_-]+)-v([0-9]+)$ ]]; then
            echo "ERROR: Tag '$TAG' does not match pattern <slug>-v<N>" >&2
            exit 1
          fi
          SLUG="${BASH_REMATCH[1]}"
          VERSION="${BASH_REMATCH[2]}"
          COLLECTION_PATH="collections/${SLUG}/v${VERSION}"
          HF_REPO="HolobiomicsLab/asb-${SLUG}-v${VERSION}"
          echo "slug=${SLUG}"       >> "$GITHUB_OUTPUT"
          echo "version=${VERSION}" >> "$GITHUB_OUTPUT"
          echo "collection_path=${COLLECTION_PATH}" >> "$GITHUB_OUTPUT"
          echo "hf_repo=${HF_REPO}" >> "$GITHUB_OUTPUT"
          echo "Parsed: slug=${SLUG}, version=${VERSION}, path=${COLLECTION_PATH}"

      - name: Check collection path exists
        run: |
          CPATH="${{ steps.tag_parse.outputs.collection_path }}"
          if [ ! -d "$CPATH" ]; then
            echo "ERROR: Collection directory not found: $CPATH" >&2
            exit 1
          fi
          echo "Collection found at $CPATH"

      - name: Generate HF Dataset card README
        run: |
          CPATH="${{ steps.tag_parse.outputs.collection_path }}"
          COLLECTION_YAML="${CPATH}/collection.yaml"
          CITATION_CFF="${CPATH}/CITATION.cff"
          OUTPUT="${CPATH}/README_HF.md"

          if [ ! -f "$COLLECTION_YAML" ]; then
            echo "WARNING: $COLLECTION_YAML not found; generating minimal card" >&2
          fi

          CITATION_ARG=""
          if [ -f "$CITATION_CFF" ]; then
            CITATION_ARG="--citation ${CITATION_CFF}"
          fi

          python scripts/generate_hf_dataset_card.py \
            --collection "$COLLECTION_YAML" \
            $CITATION_ARG \
            --output "$OUTPUT"
          echo "Generated HF dataset card at $OUTPUT"

      - name: Generate HF Space files
        run: |
          CPATH="${{ steps.tag_parse.outputs.collection_path }}"
          SLUG="${{ steps.tag_parse.outputs.slug }}"
          VERSION="${{ steps.tag_parse.outputs.version }}"
          COLLECTION_YAML="${CPATH}/collection.yaml"

          LEADERBOARD_URL="https://raw.githubusercontent.com/HolobiomicsLab/asb-skill-collections/main/${CPATH}/benchmark/leaderboard.jsonld"

          python scripts/generate_hf_space_config.py \
            --collection "$COLLECTION_YAML" \
            --leaderboard-url "$LEADERBOARD_URL" \
            --output "${CPATH}/.hf-space/"
          echo "Generated Space files at ${CPATH}/.hf-space/"

      - name: Upload collection to HF Datasets (fail-soft on missing token)
        env:
          HF_TOKEN: ${{ secrets.HF_TOKEN }}
        run: |
          if [ -z "${HF_TOKEN}" ]; then
            echo "WARNING: HF_TOKEN secret not set. Skipping HuggingFace upload." >&2
            exit 0
          fi

          CPATH="${{ steps.tag_parse.outputs.collection_path }}"
          HF_REPO="${{ steps.tag_parse.outputs.hf_repo }}"
          TAG="${GITHUB_REF_NAME}"

          python - <<'PYEOF'
          import os
          import sys
          from pathlib import Path
          from huggingface_hub import HfApi, create_repo

          token  = os.environ["HF_TOKEN"]
          repo   = os.environ["HF_REPO"]
          cpath  = Path(os.environ["CPATH"])
          tag    = os.environ["TAG"]

          api = HfApi(token=token)

          # Create the HF Dataset repo (no-op if it already exists)
          try:
              create_repo(
                  repo_id=repo,
                  repo_type="dataset",
                  token=token,
                  private=False,
                  exist_ok=True,
              )
              print(f"Ensured HF Dataset repo: {repo}")
          except Exception as e:
              print(f"ERROR creating HF repo: {e}", file=sys.stderr)
              sys.exit(1)

          # Upload collection directory contents
          try:
              api.upload_folder(
                  folder_path=str(cpath),
                  repo_id=repo,
                  repo_type="dataset",
                  commit_message=f"Mirror release {tag} from HolobiomicsLab/asb-skill-collections",
                  ignore_patterns=[".hf-space"],
              )
              print(f"Uploaded {cpath} to {repo}")
          except Exception as e:
              print(f"ERROR uploading folder: {e}", file=sys.stderr)
              sys.exit(1)

          # Upload the generated README as the dataset card
          readme_path = cpath / "README_HF.md"
          if readme_path.exists():
              try:
                  api.upload_file(
                      path_or_fileobj=str(readme_path),
                      path_in_repo="README.md",
                      repo_id=repo,
                      repo_type="dataset",
                      commit_message=f"Update dataset card for {tag}",
                  )
                  print("Uploaded README_HF.md as dataset card README.md")
              except Exception as e:
                  print(f"WARNING: Could not upload README card: {e}", file=sys.stderr)

          print(f"Done. View at: https://huggingface.co/datasets/{repo}")
          PYEOF
        env:
          HF_TOKEN: ${{ secrets.HF_TOKEN }}
          HF_REPO: ${{ steps.tag_parse.outputs.hf_repo }}
          CPATH: ${{ steps.tag_parse.outputs.collection_path }}
          TAG: ${{ github.ref_name }}

      - name: Create or update HF Space (fail-soft on missing token)
        env:
          HF_TOKEN: ${{ secrets.HF_TOKEN }}
        run: |
          if [ -z "${HF_TOKEN}" ]; then
            echo "WARNING: HF_TOKEN not set. Skipping HF Space creation." >&2
            exit 0
          fi

          CPATH="${{ steps.tag_parse.outputs.collection_path }}"
          SLUG="${{ steps.tag_parse.outputs.slug }}"
          VERSION="${{ steps.tag_parse.outputs.version }}"
          SPACE_REPO="HolobiomicsLab/asb-${SLUG}-v${VERSION}-leaderboard"
          TAG="${GITHUB_REF_NAME}"

          python - <<'PYEOF'
          import os
          import sys
          from pathlib import Path
          from huggingface_hub import HfApi, create_repo

          token      = os.environ["HF_TOKEN"]
          space_repo = os.environ["SPACE_REPO"]
          cpath      = Path(os.environ["CPATH"])
          tag        = os.environ["TAG"]
          space_src  = cpath / ".hf-space"

          if not space_src.exists():
              print("WARNING: .hf-space dir not found, skipping Space creation", file=sys.stderr)
              sys.exit(0)

          api = HfApi(token=token)

          try:
              create_repo(
                  repo_id=space_repo,
                  repo_type="space",
                  space_sdk="gradio",
                  token=token,
                  private=False,
                  exist_ok=True,
              )
              print(f"Ensured HF Space: {space_repo}")
          except Exception as e:
              print(f"ERROR creating Space: {e}", file=sys.stderr)
              sys.exit(1)

          # Upload Space files (README.md, app.py)
          try:
              api.upload_folder(
                  folder_path=str(space_src),
                  repo_id=space_repo,
                  repo_type="space",
                  commit_message=f"Update leaderboard Space for {tag}",
              )
              print(f"Uploaded Space files from {space_src} to {space_repo}")
          except Exception as e:
              print(f"ERROR uploading Space: {e}", file=sys.stderr)
              sys.exit(1)

          print(f"Done. View Space at: https://huggingface.co/spaces/{space_repo}")
          PYEOF
        env:
          HF_TOKEN: ${{ secrets.HF_TOKEN }}
          SPACE_REPO: HolobiomicsLab/asb-${{ steps.tag_parse.outputs.slug }}-v${{ steps.tag_parse.outputs.version }}-leaderboard
          CPATH: ${{ steps.tag_parse.outputs.collection_path }}
          TAG: ${{ github.ref_name }}
```

- [ ] **Step 2: Validate YAML syntax**

```bash
python -c "import yaml; yaml.safe_load(open('/Users/holobiomicslab/git/asb-skill-collections/.github/workflows/mirror-to-hf.yml'))" && echo "YAML valid"
```

Expected: `YAML valid`

- [ ] **Step 3: Commit**

```bash
git -C /Users/holobiomicslab/git/asb-skill-collections add .github/workflows/mirror-to-hf.yml
git -C /Users/holobiomicslab/git/asb-skill-collections commit -m "ci: add mirror-to-hf.yml workflow for HuggingFace Dataset + Space mirroring"
```

---

## Task 8: Update `README.md` — add Distribution section and badges

**Files:**
- Modify: `README.md`

Append a `## Distribution` section with Zenodo, HuggingFace, and w3id badges + "How to install" snippet. Do NOT change any existing content — append only.

- [ ] **Step 1: Read current README.md**

```bash
cat /Users/holobiomicslab/git/asb-skill-collections/README.md
```

- [ ] **Step 2: Append the Distribution section**

The current README ends after the License section. Append below it:

```markdown

---

## Distribution

### Badges

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.PLACEHOLDER.svg)](https://doi.org/10.5281/zenodo.PLACEHOLDER)
[![HuggingFace Datasets](https://img.shields.io/badge/HuggingFace-Datasets-yellow?logo=huggingface)](https://huggingface.co/HolobiomicsLab)
[![HuggingFace Spaces](https://img.shields.io/badge/HuggingFace-Spaces-orange?logo=huggingface)](https://huggingface.co/spaces/HolobiomicsLab)
[![w3id IRI](https://img.shields.io/badge/IRI-w3id.org%2Fholobiomicslab-blue)](https://w3id.org/holobiomicslab)

### How to install a collection (Claude Code)

```bash
# Install latest metabolomics collection
/plugin install metabolomics-v1@HolobiomicsLab/asb-skill-collections

# Or point directly to the marketplace.json
/plugin install https://raw.githubusercontent.com/HolobiomicsLab/asb-skill-collections/main/.claude-plugin/marketplace.json
```

Collections are listed in [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json).

### HuggingFace mirror

Each tagged release (`<slug>-v<N>`) is automatically mirrored to a HuggingFace Dataset repo:

```
HolobiomicsLab/asb-<slug>-v<N>
```

Programmatic access:

```python
from datasets import load_dataset
ds = load_dataset("HolobiomicsLab/asb-metabolomics-v1", "benchmark")
```

A live leaderboard HF Space is created at:

```
https://huggingface.co/spaces/HolobiomicsLab/asb-<slug>-v<N>-leaderboard
```

### Zenodo

Each collection release mints a Zenodo DOI. See `CITATION.cff` at the collection root for the full citation. The Zenodo badge above links to the latest parent record.

### w3id.org IRIs

Skills and tools are addressable via stable IRIs under `w3id.org/holobiomicslab/`:

```
https://w3id.org/holobiomicslab/asb-skill/<slug>
https://w3id.org/holobiomicslab/asb-tool/<slug>
https://w3id.org/holobiomicslab/asb-benchmark/<slug>/v<N>
```
```

- [ ] **Step 3: Commit**

```bash
git -C /Users/holobiomicslab/git/asb-skill-collections add README.md
git -C /Users/holobiomicslab/git/asb-skill-collections commit -m "docs: add Distribution section to README (HF mirror + w3id + Zenodo)"
```

---

## Task 9: Run full test suite + verify YAML syntax

**Files:** none (verification only)

- [ ] **Step 1: Install dev extras if not already installed**

```bash
cd /Users/holobiomicslab/git/asb-skill-collections && pip install -e ".[dev]" -q
```

- [ ] **Step 2: Run all tests**

```bash
cd /Users/holobiomicslab/git/asb-skill-collections && python -m pytest tests/ -v
```

Expected: all existing tests from 3a (test_check_coi, test_contributors_jsonld, test_marketplace_json, test_templates, test_vet_curator) plus new tests (test_generate_hf_dataset_card, test_generate_hf_space_config) all PASS.

- [ ] **Step 3: Validate mirror-to-hf.yml YAML syntax**

```bash
python -c "
import yaml
with open('/Users/holobiomicslab/git/asb-skill-collections/.github/workflows/mirror-to-hf.yml') as f:
    yaml.safe_load(f)
print('mirror-to-hf.yml: YAML valid')
"
```

Expected: `mirror-to-hf.yml: YAML valid`

- [ ] **Step 4: Push branch to origin**

```bash
git -C /Users/holobiomicslab/git/asb-skill-collections push -u origin wave3/hf-mirror
```

Expected: branch pushed to `HolobiomicsLab/asb-skill-collections`.

---

## Self-review

### Spec coverage check

| Design Doc §11 requirement | Covered by task |
|---|---|
| `mirror-to-hf.yml` on release tag | Task 7 |
| Creates/updates HF Dataset repo | Task 7 (create_repo + upload_folder) |
| Uploads collection directory | Task 7 |
| Auto-generated dataset card from collection.yaml + CITATION.cff | Task 3 + Task 7 |
| Fail-soft if HF_TOKEN missing | Task 7 (all HF steps fail-soft) |
| §11.1 frontmatter schema (license, tags, configs: skills/benchmark/tools, doi) | Task 3 |
| `generate_hf_dataset_card.py` unit tests | Task 3 |
| `generate_hf_space_config.py` Space metadata + app.py | Task 4 |
| Per-collection leaderboard Space: reads leaderboard.jsonld from GitHub raw URL | Task 4 + 5 |
| Sortable table by result_type | Task 4 (result_type filter + sort by overall_score) |
| "Submit a result" button → GitHub Issue | Task 4 + 5 |
| `templates/hf-space/` with app.py + requirements.txt + README.md | Task 5 |
| `templates/HOWTO-RUN.md.template` with install/run/eval/submit instructions | Task 6 |
| README Distribution section (Zenodo DOI, HuggingFace, w3id badges) | Task 8 |
| "How to install" snippet in README | Task 8 |
| Don't touch 3a files (check_coi, vet_curator, tier_update, 4 existing workflows) | All tasks (only adds new files) |
| Branch: wave3/hf-mirror | Task 1 |
| TDD (failing test first) | Tasks 3, 4 |
| Per-task commits | All tasks |

### Placeholder scan

- All code blocks are complete and concrete.
- No "TBD", "TODO", or "implement later" in any step.
- Test data (MINIMAL_COLLECTION_YAML, MINIMAL_CITATION_CFF, LEADERBOARD_URL) defined in test files.

### Type consistency

- `generate_hf_dataset_card.parse_collection_yaml()` → `dict` (used by tests Task 3 and imported in `generate_hf_space_config.main()`).
- `generate_hf_dataset_card.parse_citation_cff()` → `dict` (tests call it directly).
- `generate_hf_dataset_card.generate_readme(collection: dict, citation: Optional[dict])` → `str`.
- `generate_hf_space_config.generate_space_readme(collection: dict, leaderboard_url: str)` → `str`.
- `generate_hf_space_config.generate_app_py(collection: dict, leaderboard_url: str)` → `str`.
- `generate_hf_space_config.generate_space_config(collection: dict, leaderboard_url: str)` → `dict[str, str]` with keys `"readme"` and `"app_py"`.
- All consistent throughout Tasks 3, 4, 7.

### Cross-repo concerns for Wave 4

- Wave 4 step 9 ("HF mirror created") requires `HF_TOKEN` set in the GitHub repo secrets before tagging `metabolomics-v1`. User action required.
- The workflow assumes `collections/metabolomics/v1/collection.yaml` exists with required keys (`title`, `slug`, `version`, `domain`). Wave 4 step 1 (`asb collection promote`) must produce this file.
- `leaderboard.jsonld` need not exist at tag time (the Space fetches it live at runtime); but it must exist before any results are displayed.
- Plan 3c (running in parallel) generates `leaderboard.jsonld` schema — these files are disjoint from all files in this plan.
