---
name: python-environment-setup
description: Use when when you have cloned a scientific Python repository (e.g., ROIAL-NMR) and need to verify that the documented dependencies can be installed and the main entrypoint is invokable without errors. Use this skill before attempting to run the application's core analysis workflows.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0227
  edam_topics:
  - http://edamontology.org/topic_0769
  tools:
  - Python >=3.9
  - Python
  - XlsxWriter
  - pandas
  - PyQt5
  - openpyxl
  techniques:
  - NMR
derived_from:
- doi: 10.1002/nbm.70131
  title: ROIAL-NMR
evidence_spans:
- Python>=3.9
- '[Python](https://www.anaconda.com/download/)>=3.9'
- XlsxWriter 3.2.2
- pandas 2.2.3
- PyQt5 5.15.11
- openpyxl 3.1.5
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_falcon_cq
    doi: 10.1002/rcm.9153
    title: falcon
  - build: coll_ora
    doi: 10.1371/journal.pcbi.1009105
    title: ORA
  - build: coll_ora_cq
    doi: 10.1371/journal.pcbi.1009105
    title: ORA
  - build: coll_roial_nmr_cq
    doi: 10.1002/nbm.70131
    title: ROIAL-NMR
  dedup_kept_from: coll_roial_nmr_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1002/nbm.70131
  all_source_dois:
  - 10.1002/nbm.70131
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# python-environment-setup

## Summary

Establish a reproducible Python virtual environment with pinned dependencies for a scientific application. This skill ensures that all required packages are installed at exact versions, preventing import errors and runtime incompatibilities.

## When to use

When you have cloned a scientific Python repository (e.g., ROIAL-NMR) and need to verify that the documented dependencies can be installed and the main entrypoint is invokable without errors. Use this skill before attempting to run the application's core analysis workflows.

## When NOT to use

- The application is already installed and running successfully in your current environment — reinstalling may break existing workflows.
- You need to modify or patch dependencies beyond their pinned versions — use a development/editable install instead.
- The repository does not provide explicit version pinning — use a different skill to establish a compatible environment through testing.

## Inputs

- Repository source code (cloned from GitHub or similar)
- Python version specification (e.g., >=3.9)
- Pinned dependency list with exact version numbers
- System environment (shell, pip package manager)

## Outputs

- Active Python virtual environment
- Installed packages at specified versions (verified in pip freeze output)
- Successfully invoked application entrypoint
- Log output confirming initialization without errors

## How to apply

First, verify the Python version requirement (ROIAL-NMR requires Python ≥3.9) and check your system's installed version. Create a new virtual environment to isolate dependencies from your system Python. Install each pinned dependency using pip with exact version specifiers (e.g., `pip install XlsxWriter==3.2.2 pandas==2.2.3 PyQt5==5.15.11 openpyxl==3.1.5`). After installation, invoke the documented entrypoint (`python main.py`) to confirm the application initializes without import or runtime errors. Document the exact versions installed for reproducibility.

## Related tools

- **Python** (Interpreter and runtime for the virtual environment and entrypoint execution) — https://www.anaconda.com/download/
- **XlsxWriter** (Dependency for generating Excel output files (version 3.2.2 required))
- **pandas** (Dependency for tabular data manipulation and analysis (version 2.2.3 required))
- **PyQt5** (Dependency for graphical user interface rendering (version 5.15.11 required))
- **openpyxl** (Dependency for reading and writing Excel files (version 3.1.5 required))

## Examples

```
python -m venv roial_env && source roial_env/bin/activate && pip install XlsxWriter==3.2.2 pandas==2.2.3 PyQt5==5.15.11 openpyxl==3.1.5 && python main.py
```

## Evaluation signals

- Python version check returns ≥3.9 (e.g., `python --version` outputs 3.9.x, 3.10.x, 3.11.x, etc.)
- All five dependencies appear in `pip freeze` output at exact pinned versions: XlsxWriter==3.2.2, pandas==2.2.3, PyQt5==5.15.11, openpyxl==3.1.5, and the application's own package if present
- Invoking `python main.py` completes without ModuleNotFoundError, ImportError, or VersionConflict exceptions
- Application initializes and reaches a stable state (GUI window opens, or no errors printed to stdout/stderr within 5 seconds)
- Virtual environment is isolated: `which python` or `where python` (Windows) points to the venv directory, not system Python

## Limitations

- Pinned versions are specific to ROIAL-NMR and may not be compatible with other packages in a shared environment — use a dedicated virtual environment.
- No changelog or version history is documented, so users cannot trace what changed between versions or understand breaking changes.
- GUI dependencies (PyQt5) require a display server; headless environments may fail at initialization despite correct package installation.
- Platform-specific binary wheels (e.g., for PyQt5) may not be available for all Python versions or architectures; installation may fail on uncommon systems.

## Evidence

- [other] ROIAL-NMR requires Python >=3.9 and five pinned dependencies (XlsxWriter 3.2.2, pandas 2.2.3, PyQt5 5.15.11, openpyxl 3.1.5): "ROIAL-NMR requires Python >=3.9 and five pinned dependencies (XlsxWriter 3.2.2, pandas 2.2.3, PyQt5 5.15.11, openpyxl 3.1.5)"
- [other] Execute `python main.py` to confirm the entrypoint is invokable and the application initializes without import or runtime errors.: "Execute `python main.py` to confirm the entrypoint is invokable and the application initializes without import or runtime errors"
- [other] Create a Python virtual environment with Python ≥3.9. 3. Install dependencies using pip with exact versions: "Create a Python virtual environment with Python ≥3.9. 3. Install dependencies using pip with exact versions"
- [readme] 1. [Python](https://www.anaconda.com/download/)>=3.9
2. XlsxWriter 3.2.2
3. pandas 2.2.3
4. PyQt5  5.15.11
5. openpyxl 3.1.5: "1. [Python](https://www.anaconda.com/download/)>=3.9
2. XlsxWriter 3.2.2
3. pandas 2.2.3
4. PyQt5  5.15.11
5. openpyxl 3.1.5"
