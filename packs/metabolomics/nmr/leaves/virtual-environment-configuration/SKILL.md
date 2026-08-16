---
name: virtual-environment-configuration
description: Use when you have a Python application (e.g., ROIAL-NMR) with documented dependencies and version constraints, and you need to install it on a fresh machine or verify that the environment can be reconstructed without import or runtime errors.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - XlsxWriter
  - pandas
  - PyQt5
  - openpyxl
  - Python
  - pip
  - venv
  techniques:
  - NMR
derived_from:
- doi: 10.1002/nbm.70131
  title: ROIAL-NMR
evidence_spans:
- XlsxWriter 3.2.2
- pandas 2.2.3
- PyQt5 5.15.11
- openpyxl 3.1.5
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
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

# virtual-environment-configuration

## Summary

Configure a reproducible Python virtual environment with pinned dependencies to enable reliable execution of a scientific application. This skill ensures that exact package versions are installed in isolation, preventing dependency conflicts and enabling consistent behavior across machines.

## When to use

You have a Python application (e.g., ROIAL-NMR) with documented dependencies and version constraints, and you need to install it on a fresh machine or verify that the environment can be reconstructed without import or runtime errors. Use this skill when the application specifies a minimum Python version and explicitly pins package versions.

## When NOT to use

- Dependencies are already installed in the system Python or an existing virtual environment — use environment introspection or validation instead.
- The application does not provide version pinning or the documentation is incomplete — consider dependency inference tools or container-based solutions first.
- You need to modify or develop the application itself — this skill is for environment setup, not source code modification or debugging.

## Inputs

- GitHub repository URL
- Python version constraint (e.g., >=3.9)
- Pinned dependency list with exact versions

## Outputs

- Activated virtual environment with installed dependencies
- Confirmation that application entrypoint is invokable
- Running application instance or successful initialization without errors

## How to apply

Clone the source repository, then create a Python virtual environment specifying the minimum required version (Python ≥3.9 for ROIAL-NMR). Install each pinned dependency using pip with exact version specifiers (e.g., `pip install XlsxWriter==3.2.2 pandas==2.2.3 PyQt5==5.15.11 openpyxl==3.1.5`). After installation, invoke the documented entrypoint command (e.g., `python main.py`) to verify that all imports resolve and the application initializes without errors. Success is confirmed when the application launches without import errors, runtime exceptions, or missing dependency warnings.

## Related tools

- **Python** (Runtime interpreter; minimum version 3.9 required to execute ROIAL-NMR and its dependencies.) — https://www.anaconda.com/download/
- **pip** (Package installer used to install exact versions of XlsxWriter, pandas, PyQt5, and openpyxl into the virtual environment.)
- **venv** (Python standard library module for creating isolated virtual environments to prevent system-wide package conflicts.)
- **XlsxWriter** (Dependency version 3.2.2; used by ROIAL-NMR for Excel output file generation.)
- **pandas** (Dependency version 2.2.3; used for data manipulation and tabular data handling in ROIAL-NMR.)
- **PyQt5** (Dependency version 5.15.11; provides the graphical user interface (GUI) framework for ROIAL-NMR.)
- **openpyxl** (Dependency version 3.1.5; used for reading and writing Excel spreadsheet files.)

## Examples

```
python -m venv roial-env && source roial-env/bin/activate && pip install XlsxWriter==3.2.2 pandas==2.2.3 PyQt5==5.15.11 openpyxl==3.1.5 && python main.py
```

## Evaluation signals

- Virtual environment created successfully with Python version ≥3.9 confirmed via `python --version`.
- All five pinned dependencies installed without version conflicts: `pip list` shows XlsxWriter 3.2.2, pandas 2.2.3, PyQt5 5.15.11, openpyxl 3.1.5, plus transitive dependencies.
- Entrypoint `python main.py` executes without ImportError, ModuleNotFoundError, or missing dependency warnings.
- Application initializes and reaches a ready state (GUI appears, no traceback, or application reports successful startup).
- No runtime errors occur during the first interaction (e.g., opening a GUI dialog, loading a dataset) that would indicate incomplete or incompatible dependencies.

## Limitations

- This skill does not address runtime errors that arise from input data, configuration files, or application logic — only environment correctness.
- Platform-specific issues (e.g., PyQt5 GUI rendering on headless systems, system library dependencies) may prevent application execution even with correct Python packages.
- No changelog or version history was provided, so pinned versions may become outdated or incompatible with new operating systems or Python minor versions.
- The skill assumes the application's main.py entrypoint is the correct verification target; some applications may require additional setup steps not documented in the README.

## Evidence

- [other] ROIAL-NMR requires Python >=3.9 and five pinned dependencies (XlsxWriter 3.2.2, pandas 2.2.3, PyQt5 5.15.11, openpyxl 3.1.5): "ROIAL-NMR requires Python >=3.9 and five pinned dependencies (XlsxWriter 3.2.2, pandas 2.2.3, PyQt5 5.15.11, openpyxl 3.1.5)"
- [other] Create a Python virtual environment with Python ≥3.9. 3. Install dependencies using pip with exact versions: XlsxWriter 3.2.2, pandas 2.2.3, PyQt5 5.15.11, and openpyxl 3.1.5. 4. Execute `python main.py` to confirm the entrypoint is invokable and the application initializes without import or runtime errors.: "Create a Python virtual environment with Python ≥3.9. 3. Install dependencies using pip with exact versions: XlsxWriter 3.2.2, pandas 2.2.3, PyQt5 5.15.11, and openpyxl 3.1.5. 4. Execute `python"
- [readme] Python>=3.9: "[Python](https://www.anaconda.com/download/)>=3.9"
