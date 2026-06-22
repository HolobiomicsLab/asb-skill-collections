"""Tests for scripts/validate_hf_card.py."""
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = REPO_ROOT / "scripts" / "validate_hf_card.py"


def _run(card_text: str, tmp_path: Path, strict: bool = False) -> tuple[int, str, str]:
    """Write card_text to a tempfile and run the validator. Returns (rc, stdout, stderr)."""
    card = tmp_path / "README_HF.md"
    card.write_text(card_text)
    args = [sys.executable, str(VALIDATOR), "--card", str(card)]
    if strict:
        args.append("--strict")
    r = subprocess.run(args, capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr


COMPLETE_CARD = """---
license: apache-2.0
tags: [agentic-ai, scientific-agents, metabolomics, asb]
task_categories: [text-generation, question-answering]
size_categories: [n<1K]
language: [en]
pretty_name: "Test"
annotations_creators: [machine-generated]
language_creators: [expert-generated]
multilinguality: [monolingual]
source_datasets: [original]
configs:
  - config_name: skills
    data_files: "skills/**/SKILL.md"
homepage: "https://example.org"
doi: "10.5281/zenodo.123"
---

# Test

Description here.

## Dataset Description

Stuff.

## Dataset Structure

Stuff.

## Dataset Creation

Stuff.

## Considerations for Using the Data

Stuff.

## Additional Information

### Dataset Curators

Test curators.

### Licensing Information

Apache-2.0.

## Citation Information

```bibtex
@misc{test, title={Test}}
```

## Programmatic access

```python
from datasets import load_dataset
ds = load_dataset("test")
```
"""


def test_complete_card_passes(tmp_path: Path):
    rc, stdout, stderr = _run(COMPLETE_CARD, tmp_path)
    assert rc == 0, f"Expected rc=0, got {rc}\nstdout: {stdout}\nstderr: {stderr}"
    assert "validation passed" in stdout


def test_missing_required_frontmatter_key_fails(tmp_path: Path):
    card = COMPLETE_CARD.replace("license: apache-2.0\n", "")
    rc, stdout, stderr = _run(card, tmp_path)
    assert rc == 1
    assert "missing required keys" in stdout
    assert "license" in stdout


def test_missing_required_h2_section_fails(tmp_path: Path):
    card = COMPLETE_CARD.replace("## Considerations for Using the Data\n\nStuff.\n\n", "")
    rc, stdout, stderr = _run(card, tmp_path)
    assert rc == 1
    assert "missing required H2 sections" in stdout
    assert "Considerations" in stdout


def test_missing_optional_only_returns_warnings(tmp_path: Path):
    # Remove optional best-practice keys → should produce warnings (rc=2), not errors.
    card = COMPLETE_CARD
    for opt in ("annotations_creators:", "language_creators:", "multilinguality:", "source_datasets:"):
        card = "\n".join(line for line in card.splitlines() if not line.startswith(opt))
    rc, stdout, stderr = _run(card, tmp_path)
    assert rc == 2, f"Expected rc=2 (warnings-only), got {rc}\nstdout: {stdout}"
    assert "warning" in stdout.lower()


def test_strict_mode_treats_warnings_as_errors(tmp_path: Path):
    card = COMPLETE_CARD
    for opt in ("annotations_creators:", "language_creators:", "multilinguality:", "source_datasets:"):
        card = "\n".join(line for line in card.splitlines() if not line.startswith(opt))
    rc, _, _ = _run(card, tmp_path, strict=True)
    assert rc == 1, "strict mode should escalate warnings to errors"


def test_missing_frontmatter_block_errors(tmp_path: Path):
    card = "# Just a body, no frontmatter\n\nStuff.\n"
    rc, stdout, stderr = _run(card, tmp_path)
    assert rc == 1
    assert "missing YAML frontmatter" in stderr or "missing YAML frontmatter" in stdout


def test_invalid_yaml_frontmatter_errors(tmp_path: Path):
    card = "---\n  invalid: : yaml: :::\n---\n# Body\n"
    rc, stdout, stderr = _run(card, tmp_path)
    assert rc == 1


def test_configs_must_be_list_of_dicts_with_required_keys(tmp_path: Path):
    card = COMPLETE_CARD.replace(
        "configs:\n  - config_name: skills\n    data_files: \"skills/**/SKILL.md\"",
        "configs:\n  - whatever: skills"
    )
    rc, stdout, stderr = _run(card, tmp_path)
    assert rc == 1
    assert "config_name" in stdout
