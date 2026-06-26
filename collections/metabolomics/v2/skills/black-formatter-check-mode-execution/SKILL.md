---
name: black-formatter-check-mode-execution
description: Use when when you need to audit whether Python source files in a repository
  conform to black formatting standards before accepting contributions, merging code,
  or running CI/CD pipelines.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0199
  tools:
  - black
  - flake8
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1038/s41589-019-0400-9
  title: BiG-SCAPE biosynthetic diversity
evidence_spans:
- We use black for auto formatting
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

# black-formatter-check-mode-execution

## Summary

Execute the black code formatter in check mode to detect Python source file formatting violations without applying automatic fixes. This skill validates conformance to the black formatting standard as documented in a project's contribution guidelines.

## When to use

When you need to audit whether Python source files in a repository conform to black formatting standards before accepting contributions, merging code, or running CI/CD pipelines. Use this when the project documents black as its auto-formatting tool and you want to generate a conformance report without modifying files.

## When NOT to use

- The project does not use black as its documented formatter (check contribution guidelines first).
- You intend to automatically fix formatting issues (use black without --check flag instead).
- Input contains non-Python source code files (black operates only on .py files).

## Inputs

- Python source code files (.py)
- Local repository or cloned codebase directory
- Project contribution guidelines (for context on formatting standards)

## Outputs

- Black check-mode output (formatted violations report)
- List of non-conforming files
- Conformance status report (pass/fail per file)

## How to apply

Clone or access the target repository (e.g., medema-group/BiG-SCAPE). Run black in check mode on all Python files using `black --check` to detect formatting violations without applying changes. Parse the black output to identify non-conforming files, line counts, and formatting issues. Generate a conformance report listing files that fail the check. This is typically integrated into CI/CD workflows or pre-commit hooks to enforce code quality standards documented in the project's contribution guidelines.

## Related tools

- **black** (Code formatter executed in check mode to detect but not apply formatting violations)
- **flake8** (Complementary linting tool used alongside black in BiG-SCAPE for code quality)

## Examples

```
black --check .
```

## Evaluation signals

- Black check mode returns exit code 0 (all files conform) or non-zero (violations detected)
- Output lists specific files that violate black formatting standards
- No files are modified during check-mode execution (read-only validation)
- Conformance report can be parsed to generate a per-file pass/fail summary
- Output is reproducible across runs on the same codebase state

## Limitations

- Check mode only detects violations; it does not fix them automatically (requires separate black execution without --check).
- Black's formatting rules are opinionated and may conflict with other style preferences in the codebase.
- Check mode does not validate logical correctness or functional issues—only formatting conformance.

## Evidence

- [other] We use black for auto formatting: "We use black for auto formatting"
- [other] Run black in check mode on all Python files in the repository to detect formatting violations without applying changes.: "Run black in check mode on all Python files in the repository to detect formatting violations without applying changes"
- [other] Parse the black output to identify non-conforming files and generate a conformance report.: "Parse the black output to identify non-conforming files and generate a conformance report"
