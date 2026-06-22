---
name: pip-package-manager-operation
description: Use when when you have cloned or downloaded a Python project repository and need to install all declared dependencies to make the package importable and functional. Use this skill at the start of any local setup workflow when a requirements.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0224
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_0592
  tools:
  - pip
  - conda
derived_from:
- doi: 10.1038/s41587-025-02663-3
  title: DreaMS
evidence_spans:
- pip install -r requirements.txt
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_dreams_cq
    doi: 10.1038/s41587-025-02663-3
    title: DreaMS
  dedup_kept_from: coll_dreams_cq
schema_version: 0.2.0
---

# pip-package-manager-operation

## Summary

Install and manage Python package dependencies declared in a requirements.txt file using pip, enabling a reproducible and importable development environment. This is the foundational step for setting up software projects that depend on external Python libraries.

## When to use

When you have cloned or downloaded a Python project repository and need to install all declared dependencies to make the package importable and functional. Use this skill at the start of any local setup workflow when a requirements.txt file is present in the project root or when you need to ensure all pinned versions of dependencies are installed into your current Python environment.

## When NOT to use

- Packages are already installed in the current environment and you only need to update or modify specific versions — use 'pip install --upgrade package_name' instead.
- You need to install development or optional dependencies not listed in the base requirements.txt — look for alternative requirement files (e.g., requirements-dev.txt) or use 'pip install -e .[dev]' if extras are defined in setup.py.
- You are in a locked or offline environment without PyPI access — pre-stage wheels or use a local package index instead.

## Inputs

- requirements.txt file (plain text, one package per line, optionally with version pinning using ==, >=, <=, or ~= operators)
- Active Python environment (conda, venv, or system Python)
- Network access to PyPI or other configured package index

## Outputs

- Installed Python packages in the active environment site-packages directory
- pip installation log (stdout/stderr) documenting success or error details
- Importable Python modules matching the project's declared dependencies

## How to apply

Locate the requirements.txt file in the project repository root. Ensure you have activated the target conda environment or Python virtual environment where you want dependencies installed. Run 'pip install -r requirements.txt' from the directory containing requirements.txt. The pip package manager will parse each dependency line, resolve version constraints, download pre-built wheels or source distributions from PyPI, and install them into the active environment. Verify success by attempting to import a key package listed in requirements.txt (e.g., 'python -c "import dreams"') or by checking the output log for any 'ERROR' or 'FAILED' messages.

## Related tools

- **pip** (Command-line package installer that resolves and downloads dependencies from PyPI and installs them into the active Python environment) — https://pip.pypa.io/
- **conda** (Environment and package manager used to create isolated Python environments before invoking pip) — https://conda.io/projects/conda/en/latest/user-guide/getting-started.html

## Examples

```
pip install -r requirements.txt
```

## Evaluation signals

- pip install command exits with status code 0 (success) and no ERROR or FAILED messages appear in the output log
- All packages listed in requirements.txt are present in the output of 'pip list' or 'pip freeze' with the specified or compatible versions
- Key imports from the installed packages succeed without ModuleNotFoundError (e.g., 'python -c "import dreams; import ppiref"')
- The installed package versions match or exceed the minimum versions declared in requirements.txt (no version downgrade warnings)
- Subsequent workflow steps that depend on these packages (e.g., running scripts or tests) execute without ImportError

## Limitations

- requirements.txt does not capture optional or environment-specific dependencies; if a project has platform-specific or development-only packages, separate requirements files (e.g., requirements-dev.txt, requirements-gpu.txt) must be installed separately.
- Dependency resolution may fail or take extended time if version constraints in requirements.txt are overly strict or conflict with each other; consider using 'pip-compile' or 'poetry' for deterministic lock files.
- Binary wheels may not be available for all packages or platforms; installation falls back to building from source, which requires a C compiler and development headers (e.g., python-devel package on Linux), and can fail if build dependencies are missing.
- pip does not isolate packages per-project by default; installing into the system Python or a shared conda environment can cause version conflicts with other projects — always use a dedicated virtual environment.

## Evidence

- [other] DreaMS Python dependencies are declared in a requirements.txt file and can be installed using pip with the command 'pip install -r requirements.txt'.: "DreaMS Python dependencies are declared in a requirements.txt file and can be installed using pip with the command 'pip install -r requirements.txt'."
- [methods] pip install -r requirements.txt: "pip install -r requirements.txt"
- [readme] Install DreaMS
pip install -e .: "Install DreaMS
pip install -e ."
- [readme] conda create -n ppiref python=3.10
conda activate ppiref
git clone https://github.com/anton-bushuiev/PPIRef.git
cd PPIRef; pip install -e .: "Install the PPIRef package.

```bash
conda create -n ppiref python=3.10
conda activate ppiref"
