"""Validate a HuggingFace Dataset card README against required structure.

Checks both YAML frontmatter (required keys + sane values) and body
(required H2 sections per https://huggingface.co/docs/hub/datasets-cards).

Usage:
    python scripts/validate_hf_card.py --card collections/<slug>/v<N>/hf_README.md

Exit codes:
    0 — card passes all checks
    1 — card has at least one error (missing key, missing section)
    2 — card has warnings only (missing optional best-practice items)

Wired into `.github/workflows/mirror-to-hf.yml` between card generation
and HF upload so a malformed card never reaches HuggingFace.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml


REQUIRED_FRONTMATTER_KEYS = {
    "license",
    "tags",
    "task_categories",
    "language",
    "pretty_name",
    "configs",
}

OPTIONAL_FRONTMATTER_KEYS = {
    "size_categories",
    "annotations_creators",
    "language_creators",
    "multilinguality",
    "source_datasets",
    "homepage",
    "doi",
}

REQUIRED_SECTIONS = {
    "Dataset Description",
    "Dataset Structure",
    "Dataset Creation",
    "Considerations for Using the Data",
    "Additional Information",
}

ENCOURAGED_SECTIONS = {
    "Citation Information",
    "Licensing Information",
    "Dataset Curators",
    "Programmatic access",
}

VALID_LICENSE_SPDX_ROOTS = {
    "apache-2.0", "mit", "bsd-3-clause", "bsd-2-clause", "cc-by-4.0",
    "cc-by-sa-4.0", "cc0-1.0", "gpl-3.0", "agpl-3.0", "lgpl-3.0",
    "unlicense", "other",
}


def parse_card(text: str) -> tuple[dict, str]:
    """Return (frontmatter_dict, body_text) from a HF card README.

    HF cards open with a `---\\n...\\n---` YAML block.
    """
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.DOTALL)
    if not m:
        raise ValueError("Card is missing YAML frontmatter block (--- ... ---).")
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as e:
        raise ValueError(f"YAML frontmatter is not valid: {e}") from e
    return fm, m.group(2)


def check_frontmatter(fm: dict) -> tuple[list[str], list[str]]:
    """Return (errors, warnings)."""
    errors: list[str] = []
    warnings: list[str] = []

    missing_req = REQUIRED_FRONTMATTER_KEYS - set(fm.keys())
    if missing_req:
        errors.append(
            f"Frontmatter missing required keys: {sorted(missing_req)}"
        )

    missing_opt = OPTIONAL_FRONTMATTER_KEYS - set(fm.keys())
    if missing_opt:
        warnings.append(
            f"Frontmatter missing optional best-practice keys: {sorted(missing_opt)}"
        )

    # license: SPDX-like string (lower-case canonical form expected)
    lic = fm.get("license")
    if lic:
        if not isinstance(lic, str):
            errors.append(f"license must be a string, got {type(lic).__name__}")
        elif lic.lower() not in VALID_LICENSE_SPDX_ROOTS and lic != "other":
            warnings.append(
                f"license value {lic!r} not in common SPDX set (may still be valid)"
            )

    # tags: list of strings
    tags = fm.get("tags")
    if tags is not None:
        if not isinstance(tags, list) or not all(isinstance(t, str) for t in tags):
            errors.append("tags must be a list of strings")
        elif len(tags) < 3:
            warnings.append("tags list has <3 entries — consider adding more discoverability tags")

    # task_categories: list of strings
    tc = fm.get("task_categories")
    if tc is not None and (not isinstance(tc, list) or not all(isinstance(t, str) for t in tc)):
        errors.append("task_categories must be a list of strings")

    # language: list of ISO codes
    lang = fm.get("language")
    if lang is not None and (not isinstance(lang, list) or not all(isinstance(t, str) for t in lang)):
        errors.append("language must be a list of ISO-639 codes")

    # configs: list of dicts each with config_name + data_files
    configs = fm.get("configs")
    if configs is not None:
        if not isinstance(configs, list):
            errors.append("configs must be a list")
        else:
            for i, c in enumerate(configs):
                if not isinstance(c, dict):
                    errors.append(f"configs[{i}] must be a dict")
                    continue
                if "config_name" not in c:
                    errors.append(f"configs[{i}] missing 'config_name'")
                if "data_files" not in c:
                    errors.append(f"configs[{i}] missing 'data_files'")

    return errors, warnings


def check_body(body: str) -> tuple[list[str], list[str]]:
    """Check H2 sections."""
    errors: list[str] = []
    warnings: list[str] = []

    # Find all H2 + H3 headings. HF cards put `Dataset Curators` and
    # `Licensing Information` as H3 subsections of Additional Information,
    # while the five canonical sections are H2.
    h2_headings = set(re.findall(r"^##\s+(.+?)\s*$", body, re.MULTILINE))
    h3_headings = set(re.findall(r"^###\s+(.+?)\s*$", body, re.MULTILINE))
    any_heading_text = " ".join(h2_headings | h3_headings)

    missing_req = {
        sec for sec in REQUIRED_SECTIONS
        if not any(sec.lower() in h.lower() for h in h2_headings)
    }
    if missing_req:
        errors.append(
            f"Body missing required H2 sections: {sorted(missing_req)}"
        )

    # Encouraged sections may be H2 OR H3 (e.g. Dataset Curators is
    # typically H3 under Additional Information).
    missing_enc = {
        sec for sec in ENCOURAGED_SECTIONS
        if sec.lower() not in any_heading_text.lower()
    }
    if missing_enc:
        warnings.append(
            f"Body missing encouraged sections: {sorted(missing_enc)}"
        )

    # BibTeX block check — encouraged inside Citation Information
    if "citation" in any_heading_text.lower():
        if "@" not in body or "```bibtex" not in body.lower():
            warnings.append("No BibTeX block detected — Citation section should include one")

    # Programmatic access — code block check
    if "programmatic access" in any_heading_text.lower():
        if "load_dataset" not in body:
            warnings.append("Programmatic access section should show load_dataset() example")

    return errors, warnings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--card", required=True, help="Path to HF README to validate")
    parser.add_argument(
        "--strict", action="store_true",
        help="Treat warnings as errors (exit 1 instead of 2)"
    )
    args = parser.parse_args(argv)

    card_path = Path(args.card)
    if not card_path.exists():
        print(f"ERROR: card not found: {card_path}", file=sys.stderr)
        return 1

    text = card_path.read_text(encoding="utf-8")
    try:
        fm, body = parse_card(text)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    fm_errors, fm_warnings = check_frontmatter(fm)
    body_errors, body_warnings = check_body(body)
    errors = fm_errors + body_errors
    warnings = fm_warnings + body_warnings

    if errors:
        print(f"::error::HF card validation failed: {len(errors)} error(s)")
        for e in errors:
            print(f"  ✗ {e}")
    if warnings:
        print(f"::warning::HF card has {len(warnings)} warning(s)")
        for w in warnings:
            print(f"  ⚠ {w}")
    if not errors and not warnings:
        print(f"✓ HF card validation passed: {card_path}")

    if errors:
        return 1
    if warnings and args.strict:
        return 1
    if warnings:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
