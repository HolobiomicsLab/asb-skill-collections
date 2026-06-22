---
name: installation-validation-and-diagnostics
description: Use when after installing a package via conda or pip from a distribution channel (e.g., Bioconda, PyPI), run this skill to confirm the installation succeeded and that critical submodules are importable before proceeding to use the package in analysis workflows.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0335
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - conda
  - Bioconda
  - pip
  - Python
derived_from:
- doi: 10.1021/acs.jproteome.8b00717
  title: pyteomics
evidence_spans:
- 'using `conda <https://docs.conda.io/projects/conda/en/latest/index.html>`_::'
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

# installation-validation-and-diagnostics

## Summary

Verify that a Python package (here, Pyteomics) has been successfully installed through a package manager and that its core modules load without import errors. This skill confirms both package availability in a distribution channel and functional integrity of the installed codebase.

## When to use

After installing a package via conda or pip from a distribution channel (e.g., Bioconda, PyPI), run this skill to confirm the installation succeeded and that critical submodules are importable before proceeding to use the package in analysis workflows.

## When NOT to use

- Package is already running successfully in an active analysis pipeline — validation is redundant.
- You need to verify package *functionality* beyond imports (e.g., correctness of calculations, expected output formats) — this skill confirms import integrity only, not algorithmic correctness.
- Installation is expected to fail (e.g., testing a package that is intentionally unsupported on your OS or Python version).

## Inputs

- Package name and version specifier (e.g., 'pyteomics', 'pyteomics>=4.0')
- List of core module names to validate (e.g., ['pyteomics.mass', 'pyteomics.pepxml', 'pyteomics.mzid'])
- Target conda channel or pip repository (e.g., 'bioconda', 'PyPI')

## Outputs

- Installation verification report (text or markdown) documenting Python version, package version, and import success/failure status
- Error messages and tracebacks (if any imports fail)
- Confirmation of package availability in the target distribution channel

## How to apply

Install the target package using the appropriate package manager (conda or pip). Once installation completes, launch a Python interpreter and systematically attempt to import each core module that your analysis depends on (e.g., pyteomics.mass, pyteomics.pepxml, pyteomics.mzid for Pyteomics). Record the Python version, package version, and import status for each module. If all imports execute without errors, document the success in an installation verification report; if any import fails, capture the error message and traceback to diagnose missing dependencies or version conflicts.

## Related tools

- **conda** (Package manager used to install Pyteomics from the Bioconda channel)
- **Bioconda** (Distribution channel (conda-based repository) from which Pyteomics can be installed) — http://bioconda.github.io/recipes/pyteomics/README.html
- **pip** (Alternative Python package manager for installing Pyteomics from PyPI) — https://pypi.org/project/pyteomics/
- **Python** (Runtime environment in which module imports are tested)

## Examples

```
conda install -c bioconda pyteomics && python -c "import pyteomics.mass; import pyteomics.pepxml; import pyteomics.mzid; print('All imports successful')"
```

## Evaluation signals

- All listed core modules (e.g., pyteomics.mass, pyteomics.pepxml, pyteomics.mzid) import without raising ImportError, ModuleNotFoundError, or SyntaxError.
- Python interpreter version and package version are captured and recorded in the verification report.
- No unresolved dependency warnings or version conflicts appear during import.
- Installation report explicitly states success status (e.g., 'Installation and import validation: PASS').
- If any import fails, the error message and traceback are documented to enable diagnosis of the root cause (missing dependency, incompatible version, platform-specific issue).

## Limitations

- This skill validates only import-time correctness; it does not test package functionality, algorithm correctness, or performance.
- Import success does not guarantee that optional dependencies are present. Some Pyteomics modules (e.g., pyteomics.pylab_aux) require optional packages like matplotlib that may not be installed.
- No changelog is provided in the Pyteomics repository, making it difficult to track which modules or features are available in a specific version.
- Validation is environment-specific (Python version, OS, architecture); an installation may pass validation in one environment and fail in another.

## Evidence

- [other] Can Pyteomics be successfully installed via the Bioconda conda channel and do its core modules import without errors?: "Can Pyteomics be successfully installed via the Bioconda conda channel and do its core modules import without errors?"
- [other] Use conda to install Pyteomics from the Bioconda channel with the command `conda install -c bioconda pyteomics`.: "Use conda to install Pyteomics from the Bioconda channel with the command `conda install -c bioconda pyteomics`"
- [other] After installation completes, launch a Python interpreter and attempt to import pyteomics.mass. Attempt to import pyteomics.pepxml. Attempt to import pyteomics.mzid. If all three imports execute without errors, record the success and the Python and Pyteomics versions in an installation verification report.: "After installation completes, launch a Python interpreter and attempt to import pyteomics.mass. Attempt to import pyteomics.pepxml. Attempt to import pyteomics.mzid. If all three imports execute"
- [readme] You can also install Pyteomics from `Bioconda` using `conda`: "You can also install Pyteomics from `Bioconda` using `conda`"
