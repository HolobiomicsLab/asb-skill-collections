---
name: repository-code-quality-assessment
description: Use when you need to validate that all Python files in a repository meet the project's stated code formatting and style guidelines before merging a pull request, onboarding a new contributor, or establishing a baseline for code quality.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0226
  edam_topics:
  - http://edamontology.org/topic_0769
  tools:
  - black
  - flake8
derived_from:
- doi: 10.1038/s41589-019-0400-9
  title: BiG-SCAPE biosynthetic diversity
evidence_spans: []
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41589-019-0400-9
  all_source_dois:
  - 10.1038/s41589-019-0400-9
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# repository-code-quality-assessment

## Summary

Systematically verify that Python source files in a scientific repository conform to documented code formatting and linting standards (e.g., black, flake8) by running automated checkers in non-destructive mode and generating a conformance report. This skill ensures code quality consistency before accepting contributions.

## When to use

Apply this skill when you need to validate that all Python files in a repository meet the project's stated code formatting and style guidelines before merging a pull request, onboarding a new contributor, or establishing a baseline for code quality. Use it particularly when a project's contribution guidelines explicitly document the use of tools like black or flake8.

## When NOT to use

- The repository does not use black or flake8, or no code formatting standard is documented in contribution guidelines.
- The codebase is written in a language other than Python (e.g., R, JavaScript).
- The goal is to automatically fix formatting violations rather than detect and report them; use black --diff or black directly (without --check) instead.

## Inputs

- GitHub repository URL or local repository directory
- Python source files (.py)
- Project contribution guidelines (text or markdown)
- Documented code formatting standard (e.g., black configuration in pyproject.toml or setup.cfg)

## Outputs

- Conformance report (text or structured data) listing non-conforming files and violations
- black check output (stdout/stderr or parsed summary)
- flake8 output (optional, for additional linting violations)
- Exit code indicating pass/fail status

## How to apply

Clone or access the target repository (e.g., medema-group/BiG-SCAPE from GitHub). Run black in check mode (non-destructive) on all Python files to detect formatting violations without applying changes. Parse the black output to identify non-conforming files. Optionally run flake8 for linting to catch style and logical errors. Generate a conformance report that lists files that violate the documented standard, the specific violations, and their locations (line/column). Decide whether to request fixes from the contributor or apply auto-formatting if the project workflow permits it.

## Related tools

- **black** (Check Python source files for conformance to black code formatting standard without modifying files; parse output to identify non-conforming files and violations.) — https://github.com/psf/black
- **flake8** (Lint Python source files for style violations and logical errors complementary to black formatting checks.) — https://github.com/PyCQA/flake8

## Examples

```
black --check --verbose /path/to/medema-group/BiG-SCAPE
```

## Evaluation signals

- All Python files in the repository pass black --check with exit code 0 (no violations reported).
- The conformance report correctly identifies all files that differ from the black standard (verified by manual inspection or by running black --diff).
- When black violations are fixed and the check is re-run, exit code becomes 0 and no files are listed in the report.
- The tool output is reproducible: running the check a second time on the same code yields identical results.
- flake8 output (if included) does not report false positives; violations align with the project's linting configuration (e.g., setup.cfg or .flake8).

## Limitations

- black and flake8 enforce style and formatting conventions, not functional correctness or algorithmic validity; a passing check does not guarantee the code is scientifically correct or performant.
- The check depends on the project's documented black and flake8 configuration (e.g., line length, ignore rules); if configuration is missing or outdated, results may not match the project's actual standards.
- Some code quality issues (e.g., complexity, maintainability, type safety) are not caught by black or flake8 alone and may require additional tools (e.g., pylint, mypy).
- Contributors must have black and flake8 installed and available in their environment; CI/CD pipelines must be configured to run these checks automatically to enforce compliance.

## Evidence

- [other] The BiG-SCAPE project documents that it uses black for auto-formatting of Python source code.: "We use black for auto formatting"
- [other] The project uses flake8 for linting in addition to black.: "uses flake8 for linting"
- [full_text] Task definition describes running black in check mode on all Python files to detect violations without applying changes.: "Run black in check mode on all Python files in the repository to detect formatting violations without applying changes"
- [full_text] Task explicitly defines parsing black output to generate a conformance report.: "Parse the black output to identify non-conforming files and generate a conformance report"
