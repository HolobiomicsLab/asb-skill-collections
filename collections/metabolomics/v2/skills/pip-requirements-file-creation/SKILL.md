---
name: pip-requirements-file-creation
description: Use when you have identified all pinned software dependencies for a Python project (typically from README, setup.py, or environment documentation) and need to create a machine-readable artifact that can reliably reconstruct that exact environment.
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
  - numpy
  - scikit-learn
  - scipy
  - seaborn
  - Pandas
  - h5py
  - pip-compile or pipdeptree
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# pip-requirements-file-creation

## Summary

Generate a pinned requirements.txt file that captures exact software dependency versions for a Python project, enabling reproducible environment reconstruction across platforms. This skill is essential when documenting machine learning implementations that depend on specific, incompatible library versions.

## When to use

Apply this skill when you have identified all pinned software dependencies for a Python project (typically from README, setup.py, or environment documentation) and need to create a machine-readable artifact that can reliably reconstruct that exact environment. Specifically useful for deep learning or scientific computing projects where minor version mismatches cause incompatibility (e.g., Keras 2.2.0 with TensorFlow 1.8.0 backend).

## When NOT to use

- When dependency versions are intentionally flexible or use version ranges (e.g., >=2.0,<3.0) rather than pinned versions — use a different versioning strategy.
- When the project uses non-Python dependencies or C/C++ extensions that require system-level package managers — supplement with additional environment specification formats.
- When the target environment is already containerized (e.g., Docker) — consider whether requirements.txt addition provides value beyond the container specification.

## Inputs

- Project README or documentation containing pinned software versions
- Python version specification (e.g., Python 3.6.12)
- List of dependency packages with explicit version numbers

## Outputs

- requirements.txt file with format 'package==version' for each dependency
- environment.yml file (Conda format) for cross-platform reproducibility
- Validation report confirming version compatibility

## How to apply

Parse the project's documentation (README, setup.py, or supplementary materials) to extract all pinned package names and their exact version numbers. For each dependency, create a single line in requirements.txt using the format 'package==version', listing all eight packages with pinned versions. Validate the requirements.txt syntax and confirm compatibility with the target Python version (e.g., Python 3.6.12) using a dependency resolver tool such as pip-compile or pipdeptree. Finally, generate both requirements.txt (pip) and environment.yml (Conda) formats to maximize reproducibility across different package managers and operating systems.

## Related tools

- **Python** (Runtime environment; version 3.6.12 specified as requirement)
- **Keras** (Deep learning library dependency; version 2.2.0 pinned)
- **TensorFlow** (Backend for Keras; version 1.8.0 pinned)
- **numpy** (Numerical computing dependency; version 1.15.4 pinned)
- **scikit-learn** (Machine learning library dependency; version 0.23.2 pinned)
- **scipy** (Scientific computing dependency; version 1.0.0 pinned)
- **seaborn** (Visualization library dependency; version 0.9.0 pinned)
- **Pandas** (Data manipulation dependency; version 1.1.1 pinned)
- **h5py** (HDF5 file format handling dependency; version 2.7.1 pinned)
- **pip-compile or pipdeptree** (Dependency resolver tool for validating version compatibility)

## Evaluation signals

- requirements.txt file exists and contains all nine dependencies (Python 3.6.12 plus eight packages) with format 'package==version'
- Syntax validation passes: no malformed lines, all version specifiers are recognized by pip
- Dependency resolver confirms no version conflicts when installing against Python 3.6.12 target
- environment.yml (Conda format) successfully parses and lists equivalent pinned versions
- Freshly installed environment from requirements.txt produces identical package versions to documented specification

## Limitations

- Python 3.6.12 is deprecated and no longer receives security updates; users may encounter platform incompatibility or security vulnerabilities when using this old environment.
- Some pinned versions (e.g., TensorFlow 1.8.0) are incompatible with modern CUDA versions, limiting reproducibility on newer hardware.
- Windows and macOS may have different binary availability for old package versions; platform-specific dependency resolution may fail silently.

## Evidence

- [other] The massNet implementation requires Python 3.6.12, Keras 2.2.0 with Tensorflow 1.8.0 backend, and eight pinned dependency packages: numpy 1.15.4, sklearn 0.23.2, scipy 1.0.0, seaborn 0.9.0, Pandas 1.1.1, and h5py 2.7.1.: "Python 3.6.12, Keras 2.2.0 with Tensorflow 1.8.0 backend, and eight pinned dependency packages: numpy 1.15.4, sklearn 0.23.2, scipy 1.0.0, seaborn 0.9.0, Pandas 1.1.1, and h5py 2.7.1"
- [other] Generate a requirements.txt file listing each dependency with its pinned version in the format 'package==version'.: "Generate a requirements.txt file listing each dependency with its pinned version in the format 'package==version'"
- [readme] We have implemented our machine learning model using the following software items: 1- Python(3.6.12) 2- Keras (2.2.0) with a Tensorflow(1.8.0) backend. 3- Packages: numpy(1.15.4), sklearn(0.23.2), scipy(1.0.0), seaborn (0.9.0), Pandas(1.1.1.), and h5py(2.7.1): "Python(3.6.12) 2- Keras (2.2.0) with a Tensorflow(1.8.0) backend. 3- Packages: numpy(1.15.4), sklearn(0.23.2), scipy(1.0.0), seaborn (0.9.0), Pandas(1.1.1.), and h5py(2.7.1)"
- [other] Validate the requirements.txt syntax and confirm all listed versions are compatible with Python 3.6.12 using dependency resolver tools.: "Validate the requirements.txt syntax and confirm all listed versions are compatible with Python 3.6.12 using dependency resolver tools"
- [other] Export environment specification in both requirements.txt and environment.yml (Conda) formats for reproducibility across platforms.: "Export environment specification in both requirements.txt and environment.yml (Conda) formats for reproducibility across platforms"
