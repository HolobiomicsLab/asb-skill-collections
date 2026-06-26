---
name: dependency-version-management
description: Use when when you need to document or reproduce a Python-based research
  application (or any package-dependent workflow) and discover that the original publication
  or repository specifies dependencies without versions, or when you want to verify
  that a documented set of pinned versions can be.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_0769
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
  license_tier: open
  provenance_tier: literature
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

# dependency-version-management

## Summary

Identify, pin, and validate exact versions of software dependencies required to reproduce a runnable computational environment. This skill ensures that a documented research workflow can be reliably installed and executed across different systems by capturing and enforcing specific package versions.

## When to use

When you need to document or reproduce a Python-based research application (or any package-dependent workflow) and discover that the original publication or repository specifies dependencies without versions, or when you want to verify that a documented set of pinned versions can be successfully installed and will allow the application's primary entrypoint to execute without import or runtime errors.

## When NOT to use

- The dependency documentation already includes exact version pins and you have already verified entrypoint execution in a fresh environment — re-pinning is redundant.
- The research workflow is language-agnostic or relies on containerization (e.g., Docker) that already encapsulates dependency versions — use container verification instead.
- You only need to understand which packages are used, not to reproduce the executable environment — a simpler package inventory skill is more appropriate.

## Inputs

- Repository README or supplementary documentation listing dependencies
- Project source code with import statements or requirements file (if present)
- Documented application entrypoint (e.g., main.py, CLI command, script path)
- Target runtime environment specification (OS, Python version, etc.)

## Outputs

- Pinned dependency list with exact version strings
- Virtual environment configuration (venv or conda environment)
- Verification log confirming entrypoint invocation and absence of import/runtime errors
- Reproducible installation workflow (e.g., pip install commands or requirements.txt)

## How to apply

First, extract the language (Python, R, Node.js, etc.) and identify all direct dependencies mentioned in the repository or supplementary materials. For each dependency, record the exact version number (e.g., XlsxWriter 3.2.2, pandas 2.2.3) rather than using version ranges or floating versions. Create a virtual or isolated environment using the specified language's environment manager (e.g., Python venv or conda) and install each pinned dependency with the exact version using the package manager (e.g., `pip install package==version`). Finally, invoke the documented entrypoint (e.g., `python main.py` for Python applications) and verify that the application initializes without import errors, missing module errors, or incompatibility warnings. Document any version constraints for the base runtime (e.g., Python >=3.9) alongside the pinned packages.

## Related tools

- **Python** (Base runtime and package manager for installing dependencies; version >=3.9 required) — https://www.anaconda.com/download/
- **pip** (Package installer for Python used to install exact versions of dependencies)
- **venv** (Python standard library tool for creating isolated virtual environments to avoid system-wide dependency conflicts)
- **XlsxWriter** (Pinned dependency (version 3.2.2) for writing Excel output files)
- **pandas** (Pinned dependency (version 2.2.3) for tabular data manipulation and analysis)
- **PyQt5** (Pinned dependency (version 5.15.11) for GUI components and user interface)
- **openpyxl** (Pinned dependency (version 3.1.5) for reading and writing Excel spreadsheets)

## Examples

```
python -m venv roial_env && source roial_env/bin/activate && pip install XlsxWriter==3.2.2 pandas==2.2.3 PyQt5==5.15.11 openpyxl==3.1.5 && python main.py
```

## Evaluation signals

- All five pinned dependencies (XlsxWriter 3.2.2, pandas 2.2.3, PyQt5 5.15.11, openpyxl 3.1.5, plus the base runtime Python >=3.9) are explicitly recorded with exact version strings in the environment configuration.
- A fresh virtual environment created with the documented Python version and pinned dependencies can successfully execute `python main.py` without ImportError, ModuleNotFoundError, or version incompatibility warnings.
- Installation command succeeds without dependency resolution conflicts or backtracking; all packages install cleanly in order.
- The application entrypoint reaches initialization (GUI window appears, or main execution block runs) before any analysis-level errors, confirming no import-time issues.
- Reproducible installation workflow (e.g., pip install commands with ==version syntax) can be re-run on a separate machine or account and produces an identical working environment.

## Limitations

- Pinned versions may become deprecated or unavailable on package repositories over time; periodic re-validation against live package indices is needed for long-term reproducibility.
- Platform-specific or compiled dependencies (e.g., PyQt5 wheels) may require additional system libraries or build tools that are not captured in the Python package specification alone.
- The README does not document transitive (indirect) dependencies — only direct imports are pinned. Transitive versions may vary across installation dates and pip resolver behavior.
- No changelog or version history is provided in the repository, making it unclear whether the pinned versions are the original development versions or have been tested post-hoc for reproducibility.

## Evidence

- [other] ROIAL-NMR requires Python >=3.9 and five pinned dependencies (XlsxWriter 3.2.2, pandas 2.2.3, PyQt5 5.15.11, openpyxl 3.1.5): "ROIAL-NMR requires Python >=3.9 and five pinned dependencies (XlsxWriter 3.2.2, pandas 2.2.3, PyQt5 5.15.11, openpyxl 3.1.5)"
- [other] Install dependencies using pip with exact versions: XlsxWriter 3.2.2, pandas 2.2.3, PyQt5 5.15.11, and openpyxl 3.1.5: "Install dependencies using pip with exact versions: XlsxWriter 3.2.2, pandas 2.2.3, PyQt5 5.15.11, and openpyxl 3.1.5"
- [other] Execute `python main.py` to confirm the entrypoint is invokable and the application initializes without import or runtime errors: "Execute `python main.py` to confirm the entrypoint is invokable and the application initializes without import or runtime errors"
- [readme] Python>=3.9, XlsxWriter 3.2.2, pandas 2.2.3, PyQt5  5.15.11, openpyxl 3.1.5: "Python>=3.9, XlsxWriter 3.2.2, pandas 2.2.3, PyQt5  5.15.11, openpyxl 3.1.5"
