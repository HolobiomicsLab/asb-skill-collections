---
name: bioconda-package-installation
description: Use when you have identified a package available in the Bioconda channel
  (indicated by a conda version badge or Bioconda recipe URL) and need to verify that
  installation succeeds and that the package's critical modules are importable in
  the target Python environment, especially before integrating.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0335
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_0121
  tools:
  - conda
  - Bioconda
  - Python
  license_tier: open
derived_from:
- doi: 10.1021/acs.jproteome.8b00717
  title: pyteomics
evidence_spans:
- 'using `conda <https://docs.conda.io/projects/conda/en/latest/index.html>`_::'
- You can also install Pyteomics from `Bioconda <https://bioconda.github.io/index.html>`_
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# bioconda-package-installation

## Summary

Install a Python package from the Bioconda conda channel and verify that core modules import without errors. Use this skill when you need to deploy a bioinformatics tool in a reproducible, cross-platform environment and confirm functional installation before downstream analysis.

## When to use

You have identified a package available in the Bioconda channel (indicated by a conda version badge or Bioconda recipe URL) and need to verify that installation succeeds and that the package's critical modules are importable in the target Python environment, especially before integrating it into a larger analysis workflow.

## When NOT to use

- The package is not available in Bioconda (check conda or PyPI availability first).
- You need a specific pinned version that is not present in Bioconda; use PyPI/pip as an alternative.
- The installation environment requires conda-forge or other non-Bioconda channels for dependency resolution.

## Inputs

- Bioconda channel identifier (package name)
- conda package repository
- Python interpreter environment

## Outputs

- Installation verification report (plain text or markdown)
- Python version string
- Package version string
- Module import test results

## How to apply

First, use conda to install the package from the Bioconda channel with the command `conda install -c bioconda <package_name>`. After installation completes, launch a Python interpreter and systematically attempt to import the package's core modules (e.g., pyteomics.mass, pyteomics.pepxml, pyteomics.mzid for Pyteomics). If all imports execute without errors, record the success along with the Python and package versions in an installation verification report. This approach isolates dependency resolution to conda's Bioconda channel and provides a clear pass/fail signal for module availability.

## Related tools

- **conda** (Package manager for installing Bioconda packages and managing isolated Python environments) — https://docs.conda.io/
- **Bioconda** (Channel providing pre-built conda packages for bioinformatics tools, including Pyteomics) — http://bioconda.github.io/
- **Python** (Runtime environment in which to test module imports after package installation) — https://www.python.org/

## Examples

```
conda install -c bioconda pyteomics && python -c "import pyteomics.mass; import pyteomics.pepxml; import pyteomics.mzid; print('All imports successful')"
```

## Evaluation signals

- All three module imports (pyteomics.mass, pyteomics.pepxml, pyteomics.mzid) execute without errors or exception tracebacks.
- The installation verification report captures Python version and Pyteomics version strings without missing or malformed fields.
- Conda install command exits with status code 0 and reports successful package resolution.
- No ImportError, ModuleNotFoundError, or dependency-related exceptions are raised during import attempts.
- The installed package version matches the expected Bioconda recipe version (check via `conda list` or `pip show`).

## Limitations

- Bioconda availability is limited to packages curated for the Bioconda channel; not all Python packages are available there.
- Import success does not guarantee functional correctness of downstream analyses; additional integration tests may be needed.
- Conda-resolved dependencies may differ across operating systems (Linux, macOS, Windows), so verification should occur in the target deployment environment.
- The verification workflow tests only module import; it does not test function calls, data I/O, or API compatibility.

## Evidence

- [readme] You can also install Pyteomics from `Bioconda` using `conda`: "You can also install Pyteomics from `Bioconda` using `conda`"
- [other] Use conda to install Pyteomics from the Bioconda channel with the command `conda install -c bioconda pyteomics`: "Use conda to install Pyteomics from the Bioconda channel with the command `conda install -c bioconda pyteomics`"
- [other] After installation completes, launch a Python interpreter and attempt to import pyteomics.mass. Attempt to import pyteomics.pepxml. Attempt to import pyteomics.mzid. If all three imports execute without errors, record the success and the Python and Pyteomics versions in an installation verification report.: "After installation completes, launch a Python interpreter and attempt to import pyteomics.mass. Attempt to import pyteomics.pepxml. Attempt to import pyteomics.mzid. If all three imports execute"
- [readme] https://img.shields.io/conda/vn/bioconda/pyteomics: "https://img.shields.io/conda/vn/bioconda/pyteomics"
