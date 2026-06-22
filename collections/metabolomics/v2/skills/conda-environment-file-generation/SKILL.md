---
name: conda-environment-file-generation
description: Use when when you have identified all software dependencies and their exact pinned versions from project documentation (README, setup files, or supplementary materials) and need to create portable environment specifications for a scientific implementation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3813
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
  - Tensorflow
  - numpy
  - scikit-learn
  - scipy
  - h5py
  - Conda
  - pip
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
---

# conda-environment-file-generation

## Summary

Generate reproducible Conda environment specifications (environment.yml and requirements.txt) from documented software dependencies and pinned package versions. This skill ensures that scientific implementations can be reliably reconstructed across different computing platforms by capturing exact dependency versions and their compatibility constraints.

## When to use

When you have identified all software dependencies and their exact pinned versions from project documentation (README, setup files, or supplementary materials) and need to create portable environment specifications for a scientific implementation. Use this skill specifically when reproducing legacy or historical code that requires strict version compatibility—such as older deep learning stacks (e.g., Keras 2.2.0 with Tensorflow 1.8.0 backend on Python 3.6.12) where version mismatches cause runtime failures.

## When NOT to use

- Input dependencies are already expressed in a locked environment file (lock.txt, Pipfile.lock, or conda-lock.yml); use those directly instead of re-generating.
- The project uses dynamic or floating version specifiers (e.g., 'numpy>=1.15') rather than exact pinning; this skill requires hard version constraints to ensure reproducibility.
- Target environment must support packages that are not available in public repositories (e.g., proprietary or internal packages); version pinning alone cannot resolve missing packages.

## Inputs

- project README or documentation file containing software dependency declarations
- list of pinned package names and version strings (e.g., 'numpy==1.15.4')
- base Python version specification (e.g., 'Python 3.6.12')

## Outputs

- requirements.txt file with pip-compatible pinned dependencies
- environment.yml file with Conda-compatible environment specification
- validation report confirming dependency resolver compatibility with base Python version

## How to apply

Extract all pinned package versions and the base Python version from project documentation or supplementary materials. Parse each dependency into the format 'package==version', verifying that version numbers are exact and syntactically correct. Use a dependency resolver tool (e.g., pip-compile, conda-forge, or the conda solver) to validate that all listed versions are compatible with the specified Python runtime and with each other. Generate two export formats: a requirements.txt file in pip format (one dependency per line with ==version pinning) and an environment.yml file in Conda YAML format that includes the Python version, channel specifications, and all pinned dependencies. Test the environment specification by attempting to resolve it in a clean virtual environment to catch any undetectable conflicts before sharing.

## Related tools

- **Python** (Base runtime language version; must be specified as a dependency in environment files)
- **Keras** (Deep learning framework; pinned to version 2.2.0 as core dependency for massNet)
- **Tensorflow** (Neural network backend for Keras; pinned to version 1.8.0 for legacy compatibility)
- **numpy** (Numerical computing library; pinned to version 1.15.4 for array operations)
- **scikit-learn** (Machine learning utilities; pinned to version 0.23.2)
- **scipy** (Scientific computing library; pinned to version 1.0.0)
- **h5py** (HDF5 file format handler; pinned to version 2.7.1 for data I/O)
- **Conda** (Environment management and package resolution tool for generating and validating environment.yml files)
- **pip** (Package installer for generating and validating requirements.txt files)

## Examples

```
pip freeze > requirements.txt && conda env export --no-builds > environment.yml && conda env create --name massnet-env --file environment.yml
```

## Evaluation signals

- Syntax validation: Both requirements.txt and environment.yml parse without errors in pip and conda, respectively.
- Version pinning consistency: Every package is specified with ==MAJOR.MINOR.PATCH format; no floating or range specifiers present.
- Dependency resolution success: Running 'conda env create -f environment.yml' or 'pip install -r requirements.txt' in a clean virtual environment completes without version conflicts or unsatisfiable constraints.
- Python version compatibility: All pinned package versions are confirmed compatible with the specified Python version (e.g., Python 3.6.12) using conda's dependency resolver or pip-audit.
- Reproducibility test: Two independent environment installations from the same specification files produce bit-identical package manifests and pass a smoke test (import of core libraries succeeds).

## Limitations

- Pinned versions may depend on platform-specific wheel availability; packages available on Linux may not have wheels for macOS or Windows at identical versions, requiring fallback to source builds or manual resolution.
- Old package versions (e.g., Tensorflow 1.8.0, Keras 2.2.0) may have been delisted from public repositories, requiring use of archive mirrors or local builds.
- Transitive dependencies (dependencies of dependencies) are not always fully documented in README files; conda and pip resolvers may discover additional pinned versions not mentioned in the original documentation.
- Python 3.6.12 reached end-of-life on December 23, 2021; reproducing massNet in current environments may require containerization (Docker) or conda lock files rather than direct system installation.

## Evidence

- [other] The massNet implementation requires Python 3.6.12, Keras 2.2.0 with Tensorflow 1.8.0 backend, and eight pinned dependency packages: "The massNet implementation requires Python 3.6.12, Keras 2.2.0 with Tensorflow 1.8.0 backend, and eight pinned dependency packages: numpy 1.15.4, sklearn 0.23.2, scipy 1.0.0, seaborn 0.9.0, Pandas"
- [other] Generate a requirements.txt file listing each dependency with its pinned version: "Generate a requirements.txt file listing each dependency with its pinned version in the format 'package==version'."
- [other] Validate the requirements.txt syntax and confirm all listed versions are compatible: "Validate the requirements.txt syntax and confirm all listed versions are compatible with Python 3.6.12 using dependency resolver tools."
- [other] Export environment specification in both requirements.txt and environment.yml formats: "Export environment specification in both requirements.txt and environment.yml (Conda) formats for reproducibility across platforms."
- [readme] We have implemented our machine learning model using the following software items: "We have implemented our machine learning model using the following software items: 1- Python(3.6.12) 2- Keras (2.2.0) with a Tensorflow(1.8.0) backend. 3- Packages: numpy(1.15.4), sklearn(0.23.2),"
