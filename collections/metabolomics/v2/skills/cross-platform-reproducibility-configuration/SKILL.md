---
name: cross-platform-reproducibility-configuration
description: Use when when you have documented pinned package versions for a Python-based scientific implementation (e.g., from a README or project documentation) and need to distribute a reproducible computational environment to other users or CI/CD systems.
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
  - pip
  - Conda
  - pip-tools
  - Keras
  - Tensorflow
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

# cross-platform-reproducibility-configuration

## Summary

Generate and validate pinned software dependency specifications in multiple formats (requirements.txt and environment.yml) to enable exact reproduction of a computational environment across platforms. This skill ensures that all transitive dependencies and their exact versions are captured and compatible with the target Python runtime.

## When to use

When you have documented pinned package versions for a Python-based scientific implementation (e.g., from a README or project documentation) and need to distribute a reproducible computational environment to other users or CI/CD systems. Apply this skill when downstream users must achieve bit-identical or functionally identical results without dependency resolution ambiguity.

## When NOT to use

- When dependencies are specified only by major version or version ranges without exact pinning — the skill requires concrete version numbers, not semantic ranges like '>=1.0,<2.0'.
- When the target runtime environment is not Python or uses a non-standard package manager (e.g., R-only projects, compiled binaries without package metadata).
- When the project has no documented version pinning and dependency versions must be inferred or reverse-engineered from source code — this skill assumes authoritative source documentation exists.

## Inputs

- Project README or documentation containing pinned software versions
- Target Python version specification
- List of direct dependencies with exact version numbers

## Outputs

- requirements.txt (pip-compatible dependency specification with pinned versions)
- environment.yml (Conda-compatible environment specification)
- Dependency compatibility validation report

## How to apply

Parse the project documentation (README, setup.py, or pinned version lists) to extract all direct dependencies with their exact version numbers. Generate a requirements.txt file in the format 'package==version' for each pinned dependency. Generate a parallel environment.yml (Conda) specification listing the same versions. Validate syntax of both files and use a dependency resolver (e.g., pip-tools or Conda's solver) to confirm that all listed versions are compatible with the target Python runtime (e.g., Python 3.6.12 in the massNet case). Export both formats to enable reproducibility across different installation workflows (pip on Linux/macOS/Windows and Conda on any platform).

## Related tools

- **Python** (Runtime environment for which dependency specifications are generated and validated)
- **pip** (Package installer and requirements.txt format validator)
- **Conda** (Cross-platform package manager for which environment.yml specifications are generated and validated)
- **pip-tools** (Dependency resolver and requirements.txt syntax validator)
- **Keras** (Deep learning framework with pinned version requirement (2.2.0 with Tensorflow 1.8.0 backend)) — github.com/wabdelmoula/massNet
- **Tensorflow** (Backend for Keras with pinned version requirement (1.8.0)) — github.com/wabdelmoula/massNet

## Examples

```
pip install -r requirements.txt; conda env create -f environment.yml
```

## Evaluation signals

- requirements.txt contains all nine pinned dependencies in format 'package==version' with no version ranges or wildcards
- environment.yml syntax is valid YAML and specifies dependencies in Conda format with matching pinned versions
- Dependency resolver confirms all pinned versions are mutually compatible and compatible with Python 3.6.12
- Both requirements.txt and environment.yml can be used to successfully install the environment without dependency conflicts or unmet version constraints
- Checksum or hash verification of installed packages matches expected versions across independent installation runs

## Limitations

- Version pinning does not account for binary incompatibilities or platform-specific wheels (e.g., numpy 1.15.4 may not have pre-built wheels for all platforms); validation must be run on target platforms.
- Requirements.txt format does not capture environment variables, system dependencies, or CUDA/GPU library versions required by Tensorflow 1.8.0; supplementary documentation is needed.
- Very old pinned versions (e.g., Python 3.6.12, Tensorflow 1.8.0) may have security vulnerabilities or lack compatibility with modern operating systems; reproducibility may be achievable only in containers or legacy environments.
- Transitive dependencies of pinned packages are not explicitly listed; if a pinned package has its own dependencies with floating versions, reproducibility across time may degrade as those transitive packages are updated.

## Evidence

- [other] The massNet implementation requires Python 3.6.12, Keras 2.2.0 with Tensorflow 1.8.0 backend, and eight pinned dependency packages: numpy 1.15.4, sklearn 0.23.2, scipy 1.0.0, seaborn 0.9.0, Pandas 1.1.1, and h5py 2.7.1.: "Python 3.6.12, Keras 2.2.0 with Tensorflow 1.8.0 backend, and eight pinned dependency packages: numpy 1.15.4, sklearn 0.23.2, scipy 1.0.0, seaborn 0.9.0, Pandas 1.1.1, and h5py 2.7.1"
- [other] Generate a requirements.txt file listing each dependency with its pinned version in the format 'package==version'.: "Generate a requirements.txt file listing each dependency with its pinned version in the format 'package==version'"
- [other] Validate the requirements.txt syntax and confirm all listed versions are compatible with Python 3.6.12 using dependency resolver tools.: "Validate the requirements.txt syntax and confirm all listed versions are compatible with Python 3.6.12 using dependency resolver tools"
- [other] Export environment specification in both requirements.txt and environment.yml (Conda) formats for reproducibility across platforms.: "Export environment specification in both requirements.txt and environment.yml (Conda) formats for reproducibility across platforms"
- [readme] We have implemented our machine learning model using the following software items: 1- Python(3.6.12) 2- Keras (2.2.0) with a Tensorflow(1.8.0) backend. 3- Packages: numpy(1.15.4), sklearn(0.23.2), scipy(1.0.0), seaborn (0.9.0), Pandas(1.1.1.), and h5py(2.7.1): "Python(3.6.12) 2- Keras (2.2.0) with a Tensorflow(1.8.0) backend. 3- Packages: numpy(1.15.4), sklearn(0.23.2), scipy(1.0.0), seaborn (0.9.0), Pandas(1.1.1.), and h5py(2.7.1)"
