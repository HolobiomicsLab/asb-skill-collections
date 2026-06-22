---
name: pep8-standard-enforcement
description: Use when preparing code for contribution to a Python project that mandates PEP8 compliance, or when setting up pre-commit quality gates for a codebase.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - flake8
  - black
derived_from:
- doi: 10.1038/s41589-019-0400-9
  title: BiG-SCAPE biosynthetic diversity
evidence_spans:
- uses flake8 for linting
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_big_scape_biosynthetic_diversity_cq
    doi: 10.1038/s41589-019-0400-9
    title: BiG-SCAPE biosynthetic diversity
  dedup_kept_from: coll_big_scape_biosynthetic_diversity_cq
schema_version: 0.2.0
---

# pep8-standard-enforcement

## Summary

Enforce PEP8 code style compliance across a Python source tree using flake8 linting to detect style violations before code submission. This skill ensures consistent code quality and maintainability within collaborative development workflows.

## When to use

Apply this skill when preparing code for contribution to a Python project that mandates PEP8 compliance, or when setting up pre-commit quality gates for a codebase. Use it specifically when you have a complete Python source tree and need to identify all style violations (line length, indentation, naming conventions, imports, whitespace) before merging to a development or main branch.

## When NOT to use

- Code that is already auto-formatted by a formatter like black (use black for formatting first, then flake8 for additional checks).
- Projects that use a different code style standard (e.g., Google style guide, project-specific configuration) not compatible with PEP8.

## Inputs

- Python source tree (directory structure with .py files)
- Project repository (e.g., GitHub clone of medema-group/BiG-SCAPE)

## Outputs

- Structured lint report (file paths, line numbers, PEP8 violation codes and messages)
- Remediated Python source files (after style corrections)

## How to apply

Obtain the complete source tree from the project repository (e.g., by cloning medema-group/BiG-SCAPE). Run flake8 across all Python source files in the repository to scan for PEP8 violations. Capture the structured output documenting all identified violations, including their file paths, line numbers, and violation codes. Review the report systematically and either remediate violations directly or use complementary tools (e.g., black for auto-formatting) to resolve style issues. Re-run flake8 after remediation to confirm all violations are eliminated before submitting a pull request.

## Related tools

- **flake8** (Primary linter tool to detect PEP8 style violations across Python source files)
- **black** (Complementary auto-formatter to remediate PEP8 violations before flake8 re-validation)

## Examples

```
flake8 . --max-line-length=79 --count --statistics --output-file=lint_report.txt
```

## Evaluation signals

- flake8 exit code is 0 (all violations resolved) when run on the entire source tree
- Lint report shows zero violations for all files in the repository after remediation
- All Python files conform to PEP8 naming conventions, line length (typically ≤ 79 characters), indentation (4 spaces), and import ordering
- No new violations are introduced in modified or new source files compared to baseline report

## Limitations

- flake8 enforces style compliance but does not guarantee functional correctness or logical soundness of code.
- Project-specific PEP8 configuration (e.g., max line length, ignored violation codes) may differ and must be applied via flake8 configuration files (.flake8, setup.cfg, or tox.ini).
- Some legitimate code patterns may trigger false-positive violations; exceptions require explicit configuration or inline annotations (e.g., # noqa).

## Evidence

- [other] The BiG-SCAPE project uses flake8 for linting to enforce PEP8 standards across the source tree.: "uses flake8 for linting"
- [other] Instructions specify running flake8 linter across all Python source files and generating a structured lint report.: "Run flake8 linter across all Python source files in the repository to detect PEP8 violations. 3. Generate and save a structured lint report documenting all identified violations, their file"
- [intro] Contributors are directed to the medema-group/BiG-SCAPE repository for obtaining the source tree.: "![License](https://img.shields.io/github/license/medema-group/BiG-SCAPE)"
- [other] The project mentions complementary use of black for auto-formatting alongside flake8 linting.: "We use black for auto formatting"
