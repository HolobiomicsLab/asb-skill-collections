---
name: installation-validation-reporting
description: Use when when deploying a new Python package in a reproducible analysis environment or continuous integration pipeline, and you need to confirm that all required core modules (e.g., pyteomics.mass, pyteomics.pepxml, pyteomics.mzid, pyteomics.tandem, pyteomics.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - pip
  - Python
  - conda
derived_from:
- doi: 10.1021/acs.jproteome.8b00717
  title: pyteomics
evidence_spans:
- The main way to obtain Pyteomics is via `pip Python package manager
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pyteomics
    doi: 10.1021/acs.jproteome.8b00717
    title: pyteomics
  dedup_kept_from: coll_pyteomics
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.8b00717
  all_source_dois:
  - 10.1021/acs.jproteome.8b00717
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# installation-validation-reporting

## Summary

Verify successful installation of a Python package and its core functional modules by performing sequential imports and generating a validation report. This skill ensures that a package installation from PyPI (or other distribution channels) is complete and that critical modules are accessible before downstream analysis workflows commence.

## When to use

When deploying a new Python package in a reproducible analysis environment or continuous integration pipeline, and you need to confirm that all required core modules (e.g., pyteomics.mass, pyteomics.pepxml, pyteomics.mzid, pyteomics.tandem, pyteomics.auxiliary) are available and importable before proceeding to data analysis tasks.

## When NOT to use

- When validating an already-running installation for which you only need to check specific functionality (use targeted import tests instead of full validation)
- When the package is already integrated into a locked environment (e.g., conda environment.yml, Docker image, or virtual environment snapshot) and you only need to verify runtime behavior, not installation completeness

## Inputs

- Package name and optional version specifier (e.g., 'pyteomics' or 'pyteomics>=0.4.0')
- List of core module names to validate (e.g., ['pyteomics.mass', 'pyteomics.pepxml', 'pyteomics.mzid'])
- Python 3 environment with pip available

## Outputs

- Installation success/failure status
- Per-module import validation report (success/failure for each module)
- Structured validation report (JSON, CSV, or plain text) documenting module readiness
- Package version information
- Error logs for any failed imports

## How to apply

Install the target package using pip in a clean Python 3 environment by executing `pip install <package_name>`. Immediately after installation, attempt sequential imports of each core module listed in the package documentation, capturing import success and any error messages. Log the import status (success/failure) for each module alongside version information. Generate a structured validation report documenting which modules are ready for use and which failed, allowing downstream workflows to make informed decisions about available functionality or halt gracefully if critical modules are unavailable.

## Related tools

- **pip** (Package installer used to obtain Pyteomics and its dependencies from PyPI) — https://pypi.org/project/pyteomics/
- **Python** (Runtime environment in which package imports are executed and validated)
- **conda** (Alternative package manager that can be used to install Pyteomics from Bioconda as an alternative to pip) — http://bioconda.github.io/recipes/pyteomics/README.html

## Examples

```
pip install pyteomics && python -c "import pyteomics.mass, pyteomics.pepxml, pyteomics.mzid, pyteomics.tandem, pyteomics.auxiliary; print('All core modules imported successfully')"
```

## Evaluation signals

- All core modules listed in the validation plan produce successful import statements with no ImportError or ModuleNotFoundError exceptions
- Version string is retrievable and matches or exceeds the minimum specified version requirement
- Validation report file is created and contains structured entries for each module (pass/fail state)
- No unresolved dependency errors during installation (pip install completes with exit code 0)
- Import test script executes without runtime exceptions and produces human-readable summary (e.g., '5 of 5 modules imported successfully')

## Limitations

- The skill validates import-time availability but does not test functional correctness or runtime behavior of individual modules
- Optional dependencies (e.g., matplotlib, pandas, sqlalchemy, pynumpress) may not be installed; validation should distinguish between core and optional module imports
- Platform-specific issues (e.g., lxml compilation on certain systems, numpy binary compatibility) may cause failures that are outside the scope of the validation report
- No changelog is available in the repository to document breaking changes between versions, so version mismatch errors may not be immediately obvious from the validation report alone

## Evidence

- [other] Pyteomics provides a growing set of modules designed to facilitate common proteomics data analysis tasks: "Pyteomics provides a growing set of modules to facilitate the most common tasks in proteomics data analysis"
- [other] pip is the main distribution channel for Pyteomics: "The main way to obtain Pyteomics is via `pip Python package manager"
- [other] Core modules must be imported sequentially to verify installation: "Verify installation by attempting sequential imports of pyteomics.mass, pyteomics.pepxml, pyteomics.mzid, pyteomics.tandem, and pyteomics.auxiliary modules"
- [other] A validation report documents installation completion and module readiness: "Log import success/failure status for each module and generate a validation report documenting installation completion and module readiness"
- [readme] Pyteomics is a Python-based collection of tools: "Pyteomics is a collection of lightweight and handy tools for Python that help to handle various sorts of proteomics data"
