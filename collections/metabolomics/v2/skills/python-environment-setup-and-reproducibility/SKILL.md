---
name: python-environment-setup-and-reproducibility
description: Use when when you need to execute a multi-backend visualization library
  (e.g., pyOpenMS-Viz with matplotlib, Bokeh, and Plotly) and must measure or validate
  execution times, memory usage, and output consistency across runs or team members.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3372
  tools:
  - Python
  - conda
  - pip
  - pyOpenMS-Viz
  - matplotlib
  - Bokeh
  - Plotly
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.jproteome.4c00873
  title: pyopenmsviz
evidence_spans:
- conda create --name=pyopenms-viz python=3.12
- pyOpenMS-Viz is a Python library
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pyopenmsviz
    doi: 10.1021/acs.jproteome.4c00873
    title: pyopenmsviz
  dedup_kept_from: coll_pyopenmsviz
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.4c00873
  all_source_dois:
  - 10.1021/acs.jproteome.4c00873
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Python Environment Setup and Reproducibility

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Establish isolated Python environments with pinned dependency versions to ensure reproducible execution of scientific workflows across multiple plotting backends and systems. This skill ensures that gallery scripts and benchmarking studies produce consistent results independent of global Python installations.

## When to use

When you need to execute a multi-backend visualization library (e.g., pyOpenMS-Viz with matplotlib, Bokeh, and Plotly) and must measure or validate execution times, memory usage, and output consistency across runs or team members. Use this skill before running gallery scripts or performance benchmarks to eliminate dependency version conflicts.

## When NOT to use

- When using a shared HPC cluster with centralized module management (e.g., LMOD) — use the cluster's module system instead of conda.
- When the target package is already installed globally and you have no performance benchmarking or validation requirement — skip environment isolation if reproducibility across runs is not a concern.
- When working in a pre-built Docker container with pinned dependencies — the container already provides reproducibility; do not create redundant conda environments inside it.

## Inputs

- Project repository or package source (local or GitHub URL)
- Requirements specification (package names with optional version constraints)
- Python version specification (e.g., 3.12)

## Outputs

- Activated conda environment with isolated dependency tree
- Installation log or confirmation of all plotting backends available
- Environment specification file (conda YAML or pip requirements.txt for future recreation)

## How to apply

Create a new conda environment with a specific Python version (e.g., Python 3.12) using `conda create --name=<env_name> python=<version>`. Activate the environment with `conda activate <env_name>`. Install the target package and all required backends via pip with version pinning if needed (e.g., `pip install pyopenms_viz --upgrade` for the latest, or specify exact versions for reproducibility). Verify the installation by importing the package and confirming that all plotting backends (matplotlib, Bokeh, Plotly) are available in the environment. Document the environment specification (e.g., Python version, package versions) so that others can recreate the same environment. Execute scripts within this activated environment to ensure consistent behavior during benchmarking or validation studies.

## Related tools

- **conda** (Environment and dependency management for creating isolated Python namespaces with pinned package versions)
- **pip** (Package installer for pyOpenMS-Viz and plotting backends (matplotlib, Bokeh, Plotly) within the conda environment)
- **pyOpenMS-Viz** (Target visualization library that integrates with multiple backends; installation validates environment setup) — https://github.com/OpenMS/pyopenms_viz
- **matplotlib** (Static plotting backend integrated by pyOpenMS-Viz for benchmark validation)
- **Bokeh** (Interactive plotting backend integrated by pyOpenMS-Viz for benchmark validation)
- **Plotly** (Interactive plotting backend integrated by pyOpenMS-Viz for benchmark validation)

## Examples

```
conda create --name=pyopenms-viz python=3.12 && conda activate pyopenms-viz && pip install pyopenms_viz --upgrade && python -c 'import pyopenms_viz, matplotlib, bokeh, plotly; print("All backends available")'
```

## Evaluation signals

- Successful execution of `conda activate <env_name>` and confirmation via `which python` that the environment's Python is active, not the system Python.
- All required packages are importable without errors within the environment: `python -c 'import pyopenms_viz, matplotlib, bokeh, plotly'` returns no errors.
- Gallery scripts execute with consistent wall-clock times across multiple runs in the same environment (within ±2–3% variance for CPU-bound tasks), confirming isolation from system-level process interference.
- The installed package version matches the intended pinned version (e.g., `pip show pyopenms_viz` reports the expected version).
- Benchmarking results (execution times, memory usage) are reproducible when the environment is recreated on a different machine using the same environment specification file.

## Limitations

- Conda environments require disk space (~500 MB–2 GB per environment); storage constraints on small partitions or HPC systems may limit the number of isolated environments.
- Environment creation and package installation can take 5–10 minutes depending on package size and network latency; this overhead is one-time but must be factored into workflow initialization time.
- Conda and pip version pinning ensure reproducibility at the package level but do not control OS-level libraries (e.g., system libc, OpenGL versions), which may differ across machines and affect visualization backend behavior.
- Cross-platform reproducibility (Windows, macOS, Linux) may fail if platform-specific wheels or binary dependencies are unavailable for some packages; always test the environment on the target deployment platform.

## Evidence

- [readme] First create a new environment: conda create --name=pyopenms-viz python=3.12: "First create a new environment: conda create --name=pyopenms-viz python=3.12"
- [readme] conda activate pyopenms-viz: "conda activate pyopenms-viz"
- [readme] pip install pyopenms_viz --upgrade: "pip install pyopenms_viz --upgrade"
- [other] Set up a Python 3.12 environment with pyOpenMS-Viz installed via pip and all three plotting backends (matplotlib, Bokeh, Plotly) available.: "Set up a Python 3.12 environment with pyOpenMS-Viz installed via pip and all three plotting backends (matplotlib, Bokeh, Plotly) available."
- [readme] It integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly) and leverages the power of Pandas for data manipulation and representation.: "It integrates seamlessly with various plotting library backends (matpotlib, bokeh and plotly) and leverages the power of Pandas for data manipulation and representation."
