---
name: python-code-style-validation
description: Use when preparing Python code for contribution to a project that documents style requirements (black and/or flake8), during pre-commit validation in a CI/CD pipeline, or when reviewing pull requests to enforce uniform code standards across the repository.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0227
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3372
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

# python-code-style-validation

## Summary

Automated validation of Python source code conformance to project style standards (black formatting and PEP8 linting) to maintain code quality and consistency in collaborative development. This skill combines automated formatting checks and lint analysis to detect style violations before code review.

## When to use

Apply this skill when preparing Python code for contribution to a project that documents style requirements (black and/or flake8), during pre-commit validation in a CI/CD pipeline, or when reviewing pull requests to enforce uniform code standards across the repository.

## When NOT to use

- The project does not document use of black or flake8 in its contribution guidelines.
- Input code is not Python source files (e.g., Jupyter notebooks, YAML, JSON configuration).
- Style validation has already been applied and code is confirmed to conform; re-running is redundant unless code has been modified.

## Inputs

- Python source tree (directory of .py files)
- Project contribution guidelines or style configuration files (pyproject.toml, setup.cfg, .flake8)
- medema-group/BiG-SCAPE repository or equivalent GitHub source

## Outputs

- Black formatting conformance report (list of non-conforming files)
- Flake8 lint report (structured list of PEP8 violations with file paths and line numbers)
- Binary pass/fail status for code style validation
- Consolidated style compliance report

## How to apply

Clone or obtain the target Python repository. Run black in check mode on all Python source files to detect formatting violations without applying changes, then parse the output to identify non-conforming files. Subsequently run flake8 across the entire source tree to detect PEP8 compliance violations, including logical errors and style issues beyond formatting. Generate and preserve a structured conformance report documenting file locations, line numbers, and violation types. Pass/fail judgment is based on zero violations from both tools; any violation indicates the code does not meet the project's documented style standards.

## Related tools

- **black** (Detect Python source code formatting violations against the black auto-formatting standard in check mode; identifies files that do not conform without modifying them) — https://github.com/psf/black
- **flake8** (Enforce PEP8 compliance across the Python source tree; detects style violations, logical errors, and code quality issues; generates structured violation reports with file locations and line numbers) — https://github.com/PyCQA/flake8

## Examples

```
black --check . && flake8 . --format=json > flake8_report.json
```

## Evaluation signals

- Black check mode reports zero formatting violations (exit code 0; all files listed as 'would reformat' or similar have been corrected).
- Flake8 reports zero PEP8 violations (exit code 0; output contains no violation lines).
- All identified violations in the conformance report can be traced to specific files, line numbers, and rule codes (e.g., E501, W503).
- Conformance report is machine-parseable and can be compared against prior runs to track remediation.
- Violations reported by both tools match the project's documented style configuration (black version, flake8 rules, exclusion patterns).

## Limitations

- Black and flake8 enforce syntactic and stylistic rules only; they do not validate logical correctness, algorithmic efficiency, or semantic intent.
- Configuration drift: different versions of black or flake8, or undocumented local configuration files, may produce inconsistent results across environments.
- Some violations may be false positives or project-specific exceptions (e.g., deliberately long lines in generated code); manual review is required to distinguish legitimate exceptions from true violations.
- The skill does not guarantee that passing code is ready for production; it only confirms adherence to documented style standards.

## Evidence

- [other] The BiG-SCAPE project documents that it uses black for auto-formatting of Python source code.: "The BiG-SCAPE project documents that it uses black for auto-formatting of Python source code."
- [other] Run black in check mode on all Python files in the repository to detect formatting violations without applying changes.: "Run black in check mode on all Python files in the repository to detect formatting violations without applying changes."
- [other] The BiG-SCAPE project uses flake8 for linting to enforce PEP8 standards across the source tree.: "The BiG-SCAPE project uses flake8 for linting to enforce PEP8 standards across the source tree."
- [other] Run flake8 linter across all Python source files in the repository to detect PEP8 violations.: "Run flake8 linter across all Python source files in the repository to detect PEP8 violations."
- [other] Generate and save a structured lint report documenting all identified violations, their file locations, and line numbers.: "Generate and save a structured lint report documenting all identified violations, their file locations, and line numbers."
