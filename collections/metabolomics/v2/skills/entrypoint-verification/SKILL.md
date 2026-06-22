---
name: entrypoint-verification
description: Use when when you have obtained a Python package from a repository (e.g., via git clone) and need to confirm that the documented Python version constraint and pinned dependency versions are sufficient to execute the package's main entry point (typically main.py or a console script).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - XlsxWriter
  - pandas
  - PyQt5
  - openpyxl
  - Python
  - pip
  - venv
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
---

# entrypoint-verification

## Summary

Verify that a Python package's documented environment and dependencies can be successfully installed and configured to invoke its primary executable entrypoint without import or runtime errors. This skill validates reproducibility of the software stack before attempting analysis workflows.

## When to use

When you have obtained a Python package from a repository (e.g., via git clone) and need to confirm that the documented Python version constraint and pinned dependency versions are sufficient to execute the package's main entry point (typically main.py or a console script). Apply this skill before attempting to use the package for downstream analysis to catch environment misconfigurations early.

## When NOT to use

- The Python package is already installed in your active environment and you are only verifying a single function or module—use unit testing instead.
- You are debugging a specific algorithmic or scientific result (not an installation issue)—use package debugging or profiling skills instead.
- The entrypoint is a command-line tool that requires specific input files or parameters to run—first verify the entrypoint without parameters, then validate with typical inputs.

## Inputs

- Python package repository (source code directory or cloned git repository)
- Documented Python version constraint (e.g., '>=3.9')
- List of pinned dependency names and versions (e.g., 'XlsxWriter 3.2.2')
- Entrypoint command or module name (e.g., 'main.py')

## Outputs

- Confirmed working Python virtual environment with all dependencies installed
- Successful execution of the entrypoint without import or runtime errors
- Evidence that the application initialized (e.g., GUI window launched, console output, or process exit status 0)

## How to apply

First, clone or obtain the package repository. Create a new Python virtual environment using a Python version that meets or exceeds the documented minimum (e.g., Python ≥3.9 for ROIAL-NMR). Install all pinned dependencies using pip with exact version specifiers to ensure reproducibility—do not allow transitive dependency resolution to substitute versions. Once installation completes without errors, invoke the documented entrypoint command (e.g., `python main.py`) and verify that the application initializes, imports all required modules, and runs without raising ImportError, ModuleNotFoundError, or other runtime exceptions. Success is indicated by the application launching its primary interface or process without stderr output related to missing modules or version conflicts.

## Related tools

- **Python** (Runtime interpreter; must be version ≥3.9 for ROIAL-NMR compatibility) — https://www.anaconda.com/download/
- **pip** (Package installer; used to install pinned versions of dependencies (XlsxWriter, pandas, PyQt5, openpyxl))
- **venv** (Python virtual environment manager; creates isolated environment to test dependencies without affecting system Python)
- **XlsxWriter** (Excel file generation library; version 3.2.2 pinned for ROIAL-NMR)
- **pandas** (Data manipulation library; version 2.2.3 pinned for ROIAL-NMR)
- **PyQt5** (GUI framework for ROIAL-NMR interface; version 5.15.11 pinned)
- **openpyxl** (Excel spreadsheet library; version 3.1.5 pinned for ROIAL-NMR)

## Examples

```
python -m venv roial_env && source roial_env/bin/activate && pip install XlsxWriter==3.2.2 pandas==2.2.3 PyQt5==5.15.11 openpyxl==3.1.5 && python main.py
```

## Evaluation signals

- Virtual environment creation completes without errors and Python version matches or exceeds the documented minimum (e.g., `python --version` returns 3.9 or higher for ROIAL-NMR).
- pip install with exact pinned versions (e.g., `pip install XlsxWriter==3.2.2 pandas==2.2.3 PyQt5==5.15.11 openpyxl==3.1.5`) completes with exit status 0 and reports successful installation of all packages.
- Entrypoint invocation (`python main.py`) executes without raising ImportError, ModuleNotFoundError, or AttributeError; if the application is GUI-based (as ROIAL-NMR is), the primary window launches without stderr warnings.
- No version conflict or dependency resolution warnings appear in pip output or during entrypoint execution.
- The application's main process does not terminate unexpectedly or emit tracebacks related to missing or incompatible modules within 5 seconds of invocation (or until the application fully initializes).

## Limitations

- This skill verifies only that the entrypoint can be invoked and initialized; it does not validate the correctness of the package's scientific algorithms or outputs.
- GUI-based applications (such as ROIAL-NMR with PyQt5) may require a display server or headless rendering setup; verification in a headless environment may require additional configuration (e.g., Xvfb).
- Pinned dependency versions may have known security vulnerabilities or platform-specific issues; verification of the entrypoint does not constitute a security or compatibility audit.
- No changelog is documented for ROIAL-NMR, making it difficult to determine whether dependency updates or backward-incompatible changes have been introduced since the package was released.

## Evidence

- [other] ROIAL-NMR requires Python >=3.9 and five pinned dependencies (XlsxWriter 3.2.2, pandas 2.2.3, PyQt5 5.15.11, openpyxl 3.1.5) to be installed, with the primary entrypoint invoked via 'Run python main.py'.: "ROIAL-NMR requires Python >=3.9 and five pinned dependencies (XlsxWriter 3.2.2, pandas 2.2.3, PyQt5 5.15.11, openpyxl 3.1.5) to be installed, with the primary entrypoint invoked via 'Run python"
- [other] Execute `python main.py` to confirm the entrypoint is invokable and the application initializes without import or runtime errors.: "Execute `python main.py` to confirm the entrypoint is invokable and the application initializes without import or runtime errors."
- [readme] 1. Python>=3.9 2. XlsxWriter 3.2.2 3. pandas 2.2.3 4. PyQt5  5.15.11 5. openpyxl 3.1.5: "1. [Python](https://www.anaconda.com/download/)>=3.9
2. XlsxWriter 3.2.2
3. pandas 2.2.3
4. PyQt5  5.15.11
5. openpyxl 3.1.5"
- [other] Clone the ROIAL-NMR repository from github.com/Leo-Cheng-Lab/ROIAL-NMR. Create a Python virtual environment with Python ≥3.9. Install dependencies using pip with exact versions.: "Clone the ROIAL-NMR repository from github.com/Leo-Cheng-Lab/ROIAL-NMR. Create a Python virtual environment with Python ≥3.9. Install dependencies using pip with exact versions"
