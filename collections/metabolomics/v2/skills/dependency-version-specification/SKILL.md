---
name: dependency-version-specification
description: Use when you encounter a scientific implementation (particularly deep learning or complex data processing pipelines) where the original authors have documented specific software versions, and you need to reproduce the exact computational environment.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - numpy 1.15.4
  - scikit-learn 0.23.2
  - scipy 1.0.0
  - seaborn 0.9.0
  - Pandas 1.1.1
  - h5py 2.7.1
  - Python
  - Keras
  - TensorFlow
  - numpy, scikit-learn, scipy, seaborn, Pandas, h5py
  - pip (requirements.txt)
  - Conda (environment.yml)
derived_from:
- doi: 10.1093/bioinformatics/btac032/6510930
  title: massNet
evidence_spans:
- numpy(1.15.4)
- sklearn(0.23.2)
- scipy(1.0.0)
- seaborn (0.9.0)
- Pandas(1.1.1.)
- h5py(2.7.1)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_massnet_cq
    doi: 10.1093/bioinformatics/btac032/6510930
    title: massNet
  dedup_kept_from: coll_massnet_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btac032/6510930
  all_source_dois:
  - 10.1093/bioinformatics/btac032/6510930
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# dependency-version-specification

## Summary

Extract and document exact software dependency versions and their pinning requirements from project documentation to enable reproducible computational environments. This skill is essential when reconstructing legacy or specialized scientific software stacks where version compatibility is critical to replicating results.

## When to use

Apply this skill when you encounter a scientific implementation (particularly deep learning or complex data processing pipelines) where the original authors have documented specific software versions, and you need to reproduce the exact computational environment. Triggers include: presence of version numbers in README/documentation, legacy code requiring older library versions (e.g., Python 3.6, Tensorflow 1.x), or when standard dependency resolver tools fail due to version conflicts.

## When NOT to use

- The project uses dynamic or floating version constraints (e.g., 'package>=1.0', 'package~=2.3') without pinned versions—extract the constraints as-is but do not attempt to pin.
- The documentation is incomplete or version information is scattered across multiple files without a canonical source—prioritize README; note missing or conflicting versions.
- The software is actively maintained and designed to work with current stable releases—pinning to old versions may introduce security or compatibility issues with downstream dependencies.

## Inputs

- Project README or documentation file (plain text, Markdown, or PDF)
- Software dependency declarations (inline version specifications)
- Base Python or runtime version specification

## Outputs

- requirements.txt file with pinned package versions (format: 'package==version')
- environment.yml file with Conda environment specification
- Validated dependency compatibility report

## How to apply

Parse the project README or supplementary documentation to extract all pinned package versions with their exact version numbers (e.g., 'Keras (2.2.0)', 'numpy(1.15.4)'). Organize these into a structured requirements.txt file using the format 'package==version' for each dependency. Validate the requirements.txt syntax and cross-check version compatibility with the base Python version (in this case Python 3.6.12) using a dependency resolver or by attempting installation in an isolated environment. Export the specification in both requirements.txt (pip) and environment.yml (Conda) formats to ensure portability across different package managers and platforms. The rationale is that pinned versions preserve exact API behaviors and avoid breakage from transitive dependency updates.

## Related tools

- **Python** (Runtime environment specification and base for dependency pinning)
- **Keras** (Deep learning library with pinned version to ensure API stability)
- **TensorFlow** (Backend for Keras; version pinning critical for compatibility with specific Keras version)
- **numpy, scikit-learn, scipy, seaborn, Pandas, h5py** (Scientific and data processing packages; version pinning prevents API drift and numerical differences)
- **pip (requirements.txt)** (Python package manager for reading and installing pinned dependencies)
- **Conda (environment.yml)** (Cross-platform environment manager for reproducible environment export and import)

## Examples

```
# Parse README, extract versions, and generate requirements.txt:
echo 'Python==3.6.12
Keras==2.2.0
Tensorflow==1.8.0
numpy==1.15.4
scikit-learn==0.23.2
scipy==1.0.0
seaborn==0.9.0
pandas==1.1.1
h5py==2.7.1' > requirements.txt && pip install --dry-run -r requirements.txt
```

## Evaluation signals

- requirements.txt file is syntactically valid (parseable by pip) and contains exactly one version per package in 'package==version' format with no floating constraints.
- environment.yml is valid YAML and specifies Python 3.6.12 as the base interpreter with all eight dependency packages and their exact versions listed.
- Dry-run dependency resolution (e.g., `pip install --dry-run -r requirements.txt` or `conda env create --dry-run -f environment.yml`) succeeds without version conflicts or unresolvable transitive dependencies.
- All nine pinned dependency versions (Python 3.6.12, Keras 2.2.0, TensorFlow 1.8.0, numpy 1.15.4, scikit-learn 0.23.2, scipy 1.0.0, seaborn 0.9.0, Pandas 1.1.1, h5py 2.7.1) are extracted and match the README documentation.
- The generated environment, when installed in a fresh virtual environment, allows import of all specified packages without version warnings or deprecation errors.

## Limitations

- Very old package versions (e.g., Python 3.6.12, TensorFlow 1.8.0) may no longer be available on PyPI or conda-forge; mirror or archived package repositories may be required.
- Pinned versions may introduce security vulnerabilities if the specific versions contain known CVEs; practitioners should audit versions against security advisories.
- Platform-specific dependencies (e.g., compiled extensions, GPU drivers for TensorFlow) are not captured in requirements.txt and must be specified separately.
- The approach assumes the README is the authoritative source; if implementation code imports versions at runtime or uses version detection, those runtime constraints are not captured by static documentation parsing.

## Evidence

- [readme] Keras (2.2.0) with a Tensorflow(1.8.0) backend: "Keras (2.2.0) with a Tensorflow(1.8.0) backend."
- [readme] Python 3.6.12 and eight pinned packages: "Python(3.6.12)...Packages: numpy(1.15.4), sklearn(0.23.2), scipy(1.0.0), seaborn (0.9.0), Pandas(1.1.1.), and h5py(2.7.1)"
- [intro] Requirements format specification: "Generate a requirements.txt file listing each dependency with its pinned version in the format 'package==version'."
- [intro] Conda and pip export formats: "Export environment specification in both requirements.txt and environment.yml (Conda) formats for reproducibility across platforms."
