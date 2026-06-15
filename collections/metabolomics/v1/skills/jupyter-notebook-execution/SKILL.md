---
name: jupyter-notebook-execution
description: Use when you have access to a published study that provides a Jupyter notebook (.ipynb) containing executable code for reproducing simulations, analyses, or figures, and you need to verify that the reported results can be regenerated in your own environment or adapt the code for a related analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3552
  edam_topics:
  - http://edamontology.org/topic_3577
  - http://edamontology.org/topic_0092
  tools:
  - Jupyter
  - Python
  - cwieder/metabolomics-ORA
derived_from:
- doi: 10.1371/journal.pcbi.1009105
  title: ORA
evidence_spans:
- The Python code to generate the results is contained within the Jupyter notebook
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ora
    doi: 10.1371/journal.pcbi.1009105
    title: ORA
  dedup_kept_from: coll_ora
schema_version: 0.2.0
---

# jupyter-notebook-execution

## Summary

Execute a Jupyter notebook sequentially to regenerate computational results, figures, and tables from a published study. This skill validates reproducibility by running all cells in order within a controlled Python environment and comparing outputs against reported findings.

## When to use

Use this skill when you have access to a published study that provides a Jupyter notebook (.ipynb) containing executable code for reproducing simulations, analyses, or figures, and you need to verify that the reported results can be regenerated in your own environment or adapt the code for a related analysis.

## When NOT to use

- The notebook requires proprietary software, commercial datasets, or restricted access that you do not have available.
- The article does not provide sufficient documentation of dependencies, input data paths, or expected outputs to validate correct execution.
- Your computing environment is fundamentally incompatible (e.g., Windows-only Python 3.8 code on macOS, or GPU requirements unavailable).

## Inputs

- Jupyter notebook file (.ipynb) with executable Python code
- Python environment with version specification and dependency list
- Published article or supplementary methods describing expected outputs

## Outputs

- Regenerated figures and plots from notebook execution
- Simulation results, numerical tables, and summary statistics
- Console output, logs, and any generated data files
- Verification report comparing generated outputs to published results

## How to apply

First, clone or download the repository containing the notebook and review the dependencies listed in the README or environment specification. Set up a Python environment matching the tested version (e.g., Python 3.8) with all required packages installed. Launch Jupyter and open the notebook file, then execute all cells sequentially from top to bottom using the 'Run All' command or by stepping through each cell individually. Monitor for runtime errors, warnings, or unexpected outputs during execution. After completion, compare the generated figures, tables, and numerical outputs against those reported in the publication to confirm reproducibility. Document any discrepancies in environment, library versions, or hardware that may affect result fidelity.

## Related tools

- **Python** (Core execution environment for running notebook cells and simulation code)
- **Jupyter** (Notebook interface for sequential cell execution and interactive result visualization)
- **cwieder/metabolomics-ORA** (Repository containing the reproducible simulation notebook and source code) — https://github.com/cwieder/metabolomics-ORA

## Examples

```
cd metabolomics-ORA && jupyter notebook src/reproducible_simulations.ipynb
```

## Evaluation signals

- All notebook cells execute without errors or with only expected warnings documented in the article.
- Generated figures (plots, heatmaps) are visually consistent with those published in the article or supplementary materials.
- Numerical outputs (summary statistics, p-values, counts) match the reported values within acceptable tolerance (e.g., floating-point precision).
- No missing or undefined variable references occur during execution—all dependencies are correctly installed and importable.
- Runtime completes within a reasonable timeframe for the documented hardware (e.g., 'tested using standard hardware on MacOS').

## Limitations

- Reproducibility may fail if the Python version or library versions differ significantly from those tested; pinned dependency files (requirements.txt, environment.yml) are essential.
- Platform-specific code paths or system dependencies (e.g., graphics rendering, temporary file handling) may cause notebooks to behave differently across operating systems.
- No changelog was provided for the repository, making it unclear whether updates to the notebook or dependencies have introduced breaking changes since publication.
- Results depend on random seed initialization; notebooks must document random seeds or disable stochasticity to ensure exact numerical reproducibility.
- Large simulations or data processing may require more memory or compute time than the documented test environment, leading to timeout or out-of-memory failures.

## Evidence

- [intro] The Python code to generate the results is contained within the Jupyter notebook: "The Python code to generate the results is contained within the Jupyter notebook"
- [other] Clone the cwieder/metabolomics-ORA repository from GitHub and set up Python 3.8 environment with dependencies: "Clone the cwieder/metabolomics-ORA repository from GitHub. 2. Set up a Python 3.8 environment with all required dependencies listed in the repository."
- [other] Execute all cells sequentially and verify outputs match publication: "Execute all cells in the notebook sequentially to regenerate simulation outputs. 5. Verify that generated figures and tables match those reported in the publication"
- [other] Code tested using Python 3.8 on MacOS with standard hardware: "with the code tested using Python 3.8 on MacOS with standard hardware"
- [intro] Repository contains code to run simulations presented in the study: "This repository contains the code to run the simulations presented in the study"
