---
name: python-dependency-management
description: Use when when initializing a new Python project environment, reproducing a published analysis, or building documentation that requires external dependencies. Specifically apply this skill when you have a requirements.txt file listing pinned versions and need to ensure all downstream tools (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3365
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - pip
  - conda
  - Sphinx
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

# Python Dependency Management

## Summary

Install and configure Python package dependencies using pip and requirements files, ensuring reproducible environments for scientific software. This skill is essential for setting up projects that depend on specific versions of libraries for documentation building, data processing, or model inference.

## When to use

When initializing a new Python project environment, reproducing a published analysis, or building documentation that requires external dependencies. Specifically apply this skill when you have a requirements.txt file listing pinned versions and need to ensure all downstream tools (e.g., Sphinx, data loaders, neural network inference) have their dependencies available before execution.

## When NOT to use

- When using a pre-built Docker container or conda-lock file that already bundles all dependencies—dependency management is already resolved in those contexts.
- When the project uses non-Python dependencies (e.g., C libraries, system packages) that require apt-get, brew, or manual compilation—use system package managers instead.
- When working in a Jupyter notebook or cloud environment (e.g., Google Colab, HuggingFace Spaces) where dependencies are pre-installed or managed separately via notebook magic commands.

## Inputs

- requirements.txt file with pinned package versions
- Python interpreter (3.9+, ideally 3.10 or 3.11 for modern projects)
- pip package manager
- Optional: conda environment specification or environment.yml

## Outputs

- Installed Python packages in the active environment
- Ready-to-use environment for running downstream tools
- pip freeze output or requirements lock file (optional verification)

## How to apply

Create a Python virtual environment or conda environment at the desired version (e.g., python==3.11.0 for DreaMS). Install the requirements file using `pip install -r requirements.txt`, which reads all pinned package versions and installs them in a single pass. Verify successful installation by importing critical packages in Python or running a sanity check on a tool that depends on them. If building documentation or running models, perform dependency installation before invoking downstream tools like Sphinx or the model API, since these tools will fail silently or with cryptic errors if their imports are not satisfied.

## Related tools

- **pip** (Command-line package installer that reads requirements.txt and installs pinned package versions into the active Python environment) — https://pip.pypa.io/
- **conda** (Alternative package and environment manager; used to create isolated Python environments before pip-based dependency installation) — https://conda.io/projects/conda/en/latest/user-guide/getting-started.html
- **Sphinx** (Documentation generator tool invoked after dependency installation; requires packages listed in requirements.txt (e.g., sphinx, sphinx_rtd_theme)) — https://www.sphinx-doc.org/

## Examples

```
conda create -n dreams python==3.11.0 --yes && conda activate dreams && pip install -r requirements.txt
```

## Evaluation signals

- pip install -r requirements.txt completes without error and exits with status 0
- Python -c 'import <package>; print(<package>.__version__)' succeeds for each critical package in requirements.txt
- Downstream tools that depend on these packages (e.g., `sphinx-apidoc`, `from dreams.api import dreams_embeddings`) execute without ImportError
- pip freeze output or `pip list` confirms that installed versions match or satisfy the pinned versions in requirements.txt
- No warnings or deprecation notices that would prevent reproducible builds in CI/CD pipelines

## Limitations

- Platform-specific wheels may be required for packages with C extensions; pip will fail if pre-built wheels are not available for your Python version and OS combination.
- Pinned version conflicts can arise if requirements.txt specifies incompatible transitive dependencies; manual resolution of dependency graphs may be needed.
- Installation time scales with the number of packages and their build complexity; large requirement files (>50 packages) can take several minutes, especially if compilation is required.
- This skill assumes pip and Python are already installed; it does not cover system-level package manager setup (e.g., apt-get for Debian/Ubuntu, brew for macOS).

## Evidence

- [methods] Install Python dependencies from requirements.txt using pip: "Install Python dependencies from requirements.txt using pip"
- [readme] pip install -r requirements.txt: "pip install -r requirements.txt"
- [readme] Create conda environment with specified Python version before activating it: "conda create -n dreams python==3.11.0 --yes
conda activate dreams"
- [readme] Installation documentation for PPIRef notes conda environment creation: "conda create -n ppiref python=3.10
conda activate ppiref
git clone https://github.com/anton-bushuiev/PPIRef.git
cd PPIRef; pip install -e ."
