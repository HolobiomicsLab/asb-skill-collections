---
name: repository-cloning-and-initialization
description: Use when you have a GitHub repository URL, a documented Python version requirement, and a list of pinned package versions, and you need to verify that the application will initialize without import or runtime errors before proceeding to data analysis or method replication.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3429
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3361
  tools:
  - XlsxWriter
  - pandas
  - PyQt5
  - openpyxl
  - Python
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# repository-cloning-and-initialization

## Summary

Clone a scientific software repository and install its pinned dependencies in an isolated Python environment to verify the documented entrypoint is executable. This skill establishes a reproducible runtime for metabolomics analysis tools (or similar bioinformatics software) before conducting analysis.

## When to use

You have a GitHub repository URL, a documented Python version requirement, and a list of pinned package versions, and you need to verify that the application will initialize without import or runtime errors before proceeding to data analysis or method replication.

## When NOT to use

- The repository documentation does not specify pinned dependency versions (use a requirements file discovery step first).
- The application has no documented entrypoint or README with setup instructions.
- You already have a pre-configured containerized or conda environment and do not need to verify manual installation.

## Inputs

- GitHub repository URL
- Python version requirement (e.g., >=3.9)
- Pinned dependency list with exact version numbers

## Outputs

- Activated Python virtual environment with all dependencies installed
- Successful entrypoint invocation confirmation (no import or runtime errors)
- Initialized application instance ready for analysis

## How to apply

Clone the repository from the documented GitHub URL (e.g., github.com/Leo-Cheng-Lab/ROIAL-NMR). Create a new Python virtual environment with the required Python version (≥3.9 for ROIAL-NMR) to isolate dependencies. Install each pinned dependency using pip with exact version numbers (e.g., XlsxWriter==3.2.2, pandas==2.2.3, PyQt5==5.15.11, openpyxl==3.1.5). Execute the documented entrypoint command (e.g., `python main.py`) to confirm the application initializes, all imports resolve, and no runtime errors occur. Record success as confirmation that the environment is correctly configured and the tool is ready for use.

## Related tools

- **Python** (Runtime interpreter and environment manager for dependency installation and entrypoint execution) — https://www.anaconda.com/download/
- **XlsxWriter** (Excel file output generation for metabolite analysis results)
- **pandas** (Data manipulation and tabular data handling for metabolite identification results)
- **PyQt5** (GUI framework for ROIAL-NMR interactive analysis interface)
- **openpyxl** (Excel file reading and writing for parameter input and result export)

## Examples

```
git clone https://github.com/Leo-Cheng-Lab/ROIAL-NMR && cd ROIAL-NMR && python -m venv env && source env/bin/activate && pip install XlsxWriter==3.2.2 pandas==2.2.3 PyQt5==5.15.11 openpyxl==3.1.5 && python main.py
```

## Evaluation signals

- Virtual environment successfully created and activated with the specified Python version.
- All pinned dependencies install without version conflicts or deprecation warnings.
- Entrypoint command (`python main.py`) executes without ImportError, ModuleNotFoundError, or AttributeError.
- Application initializes to a usable state (GUI window displays, or CLI prompt appears, with no stderr tracebacks).
- No runtime errors occur during the first interaction with the application (e.g., opening the default analysis template or viewing the main window).

## Limitations

- This skill verifies only that the documented environment can be instantiated; it does not validate that analysis results are correct or that the tool functions correctly on real data.
- Platform-specific issues (e.g., PyQt5 on headless servers, macOS vs. Linux linker differences) may cause entrypoint failures despite correct dependency versions.
- No changelog is provided in the repository, so it is not possible to trace which dependency versions correspond to which feature set or bug fixes.
- Pinned dependency versions may become outdated or unavailable on PyPI, requiring alternative versions or manual source builds.

## Evidence

- [other] ROIAL-NMR requires Python >=3.9 and five pinned dependencies (XlsxWriter 3.2.2, pandas 2.2.3, PyQt5 5.15.11, openpyxl 3.1.5): "ROIAL-NMR requires Python >=3.9 and five pinned dependencies (XlsxWriter 3.2.2, pandas 2.2.3, PyQt5 5.15.11, openpyxl 3.1.5) to be installed"
- [other] Clone the ROIAL-NMR repository from github.com/Leo-Cheng-Lab/ROIAL-NMR. Create a Python virtual environment with Python ≥3.9.: "Clone the ROIAL-NMR repository from github.com/Leo-Cheng-Lab/ROIAL-NMR. 2. Create a Python virtual environment with Python ≥3.9."
- [other] Install dependencies using pip with exact versions and Execute `python main.py` to confirm the entrypoint is invokable and the application initializes without import or runtime errors.: "Install dependencies using pip with exact versions: XlsxWriter 3.2.2, pandas 2.2.3, PyQt5 5.15.11, and openpyxl 3.1.5. 4. Execute `python main.py` to confirm the entrypoint is invokable and the"
- [readme] Python version and packages requirements with exact pinned versions: "1. [Python](https://www.anaconda.com/download/)>=3.9
2. XlsxWriter 3.2.2
3. pandas 2.2.3
4. PyQt5  5.15.11
5. openpyxl 3.1.5"
