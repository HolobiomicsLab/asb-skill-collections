---
name: python-environment-configuration
description: Use when when you have installed a Python package (e.g., via pip or conda) and need to confirm that the installation succeeded and all expected submodules can be imported.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0336
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - pip
  - conda
derived_from:
- doi: 10.1021/acs.jproteome.8b00717
  title: pyteomics
evidence_spans:
- Pyteomics supports recent versions of Python 3
- Pyteomics supports recent versions of Python 3.
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
---

# Python Environment Configuration

## Summary

Validate a Python package installation and verify that core functional modules are accessible after package manager installation. This skill ensures reproducible environment setup by confirming module availability before downstream analysis.

## When to use

When you have installed a Python package (e.g., via pip or conda) and need to confirm that the installation succeeded and all expected submodules can be imported. Apply this skill before attempting to use the package in a larger pipeline or analysis workflow to catch dependency or installation issues early.

## When NOT to use

- The package is already confirmed to be installed and used successfully in the current environment.
- You are in a containerized or reproducible environment (e.g., Docker, conda-lock) where installation is guaranteed by the build definition.
- You are performing a dynamic package discovery task (e.g., listing all available submodules programmatically) rather than validating a known set of modules.

## Inputs

- Python package name and version (string or pip specifier, e.g., 'pyteomics')
- List of target submodules to validate (e.g., [pyteomics.mass, pyteomics.pepxml, ...])
- Python 3 interpreter environment

## Outputs

- Import validation report (text or structured log)
- Per-module status table (module name, import success/failure, error message if applicable)
- Installation completion confirmation (boolean or exit code)

## How to apply

Execute a sequential import test of the core modules provided by the package (e.g., pyteomics.mass, pyteomics.pepxml, pyteomics.mzid, pyteomics.tandem, pyteomics.auxiliary for Pyteomics). For each module, attempt an import statement and log the success or failure status. Document any ImportError or ModuleNotFoundError messages. Generate a validation report listing which modules are ready for use and which (if any) failed to import. This approach catches missing dependencies, incomplete installations, or environment configuration issues before they propagate to downstream analysis code.

## Related tools

- **pip** (Package manager used to install Pyteomics and its dependencies from PyPI) — https://pypi.org/
- **conda** (Alternative package manager for installing Pyteomics from Bioconda channel) — http://bioconda.github.io/recipes/pyteomics/README.html
- **Python** (Runtime environment for executing import tests and validating module availability)

## Examples

```
import sys; modules = ['pyteomics.mass', 'pyteomics.pepxml', 'pyteomics.mzid', 'pyteomics.tandem', 'pyteomics.auxiliary']; results = {m: 'OK' if __import__(m) else 'FAIL' for m in modules}; print(results)
```

## Evaluation signals

- All target modules import without raising ImportError or ModuleNotFoundError.
- Each module import returns a module object that can be queried for attributes or submodules (e.g., dir(module) returns a non-empty list).
- The validation report lists no missing or failed imports; 100% success rate across all expected modules.
- The import sequence completes within expected time (no hanging on circular dependencies or network calls).
- Version of installed package matches or exceeds the minimum required version specified in documentation.

## Limitations

- This skill only confirms that modules can be imported; it does not test the correctness or functionality of those modules.
- Optional dependencies (e.g., lxml for XML parsing, sqlalchemy for Unimod access, matplotlib for plotting) may not trigger import errors in the core modules but will fail only when those features are actually used.
- The validation does not capture runtime environment issues (e.g., missing system libraries, incompatible NumPy ABI versions) that may surface only during computation.
- No changelog is maintained for Pyteomics in the repository, so version compatibility issues must be inferred from release notes or error messages.

## Evidence

- [other] The workflow and rationale for sequential module import testing: "Verify installation by attempting sequential imports of pyteomics.mass, pyteomics.pepxml, pyteomics.mzid, pyteomics.tandem, and pyteomics.auxiliary modules. 3. Log import success/failure status for"
- [readme] Primary installation method and package availability: "The main way to obtain Pyteomics is via `pip Python package manager"
- [other] Alternative installation method: "You can also install Pyteomics from `Bioconda` using `conda`"
- [intro] Core module availability and scope: "Pyteomics provides a growing set of modules designed to facilitate common proteomics data analysis tasks"
