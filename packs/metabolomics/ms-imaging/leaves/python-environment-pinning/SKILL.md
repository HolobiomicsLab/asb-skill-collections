---
name: python-environment-pinning
description: 'Use when when you have access to a research repository or README documenting a machine learning implementation (e.g., Keras/TensorFlow-based deep learning model) and need to reproduce the computational environment exactly. Triggers include: (1) README explicitly lists pinned versions (e.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3179
  tools:
  - Python 3.6.12
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
  - h5py
  - pip
  - Conda
  techniques:
  - MS-imaging
derived_from:
- doi: 10.1093/bioinformatics/btac032/6510930
  title: massNet
evidence_spans:
- Python(3.6.12)
- 1- Python(3.6.12)
- numpy(1.15.4)
- sklearn(0.23.2)
- scipy(1.0.0)
- seaborn (0.9.0)
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

# python-environment-pinning

## Summary

Extract exact software dependency versions from project documentation and generate reproducible environment specifications (requirements.txt and environment.yml) to enable consistent reimplementation across platforms. This skill is essential when legacy implementations require specific version constraints to avoid API incompatibilities.

## When to use

When you have access to a research repository or README documenting a machine learning implementation (e.g., Keras/TensorFlow-based deep learning model) and need to reproduce the computational environment exactly. Triggers include: (1) README explicitly lists pinned versions (e.g., 'Python 3.6.12', 'Keras 2.2.0'); (2) you encounter version-dependent code (e.g., TensorFlow 1.x API differences); (3) you need to validate that all dependencies are compatible with a specific Python version before deployment.

## When NOT to use

- The project provides only version ranges or 'latest' specifications without exact pinned versions — use version constraint relaxation instead.
- Input is a pre-built Docker image or container specification — extract the pinned versions from the Dockerfile/image manifest directly rather than reconstructing from documentation.
- The repository already includes a functional requirements.txt or environment.yml in its source tree — validate and use it directly rather than re-pinning.

## Inputs

- Project README or documentation text containing 'Installations' or 'Requirements' section
- Pinned package version strings extracted from source material (e.g., 'Python(3.6.12)', 'Keras (2.2.0)', 'numpy(1.15.4)')
- Target Python version specification (e.g., '3.6.12')

## Outputs

- requirements.txt file with pip-compatible pinned dependencies (format: 'package==version')
- environment.yml file with Conda-compatible environment specification including Python version
- Validated dependency graph showing absence of conflicts

## How to apply

Parse the README or project documentation (typically under 'Installation', 'Requirements', or 'Software' sections) to extract all package names and their pinned version numbers in the exact format documented. For each dependency, record the package name, operator (typically '=='), and version string (e.g., 'numpy==1.15.4'). Generate a requirements.txt file listing each dependency in pip-compatible format ('package==version', one per line). Simultaneously, create an environment.yml file for Conda format compatibility, including the pinned Python version as the base environment (e.g., 'python=3.6.12'). Validate the requirements.txt syntax and cross-check compatibility using a dependency resolver tool (e.g., `pip check` or `pipdeptree`) to confirm no transitive conflicts exist with the target Python version. Export both formats to enable reproducibility across package managers and platforms.

## Related tools

- **Python** (Language runtime and package management baseline; version 3.6.12 specified as required base environment)
- **Keras** (Deep learning framework; version 2.2.0 pinned to ensure API stability for probabilistic classification model)
- **TensorFlow** (Backend for Keras; version 1.8.0 pinned to support Keras 2.2.0 compatibility)
- **numpy** (Numerical array operations; version 1.15.4 pinned for compatibility with scipy 1.0.0 and h5py 2.7.1)
- **scikit-learn** (Machine learning utilities; version 0.23.2 pinned for preprocessing and classification support)
- **scipy** (Scientific computing; version 1.0.0 pinned for signal processing and spatial algorithms)
- **h5py** (HDF5 file I/O for mass spectrometry imaging data; version 2.7.1 pinned for data serialization)
- **pip** (Dependency resolver and validator; used to check requirements.txt syntax and transitive conflicts)
- **Conda** (Package manager for environment.yml export; enables cross-platform reproducibility)

## Examples

```
# Extract from README and create requirements.txt with pinned versions:
cat > requirements.txt << 'EOF'
Python==3.6.12
Keras==2.2.0
Tensorflow==1.8.0
numpy==1.15.4
scikit-learn==0.23.2
scipy==1.0.0
seaborn==0.9.0
Pandas==1.1.1
h5py==2.7.1
EOF
# Then validate:
pip check
# And create Conda environment.yml:
conda env create --name massNet --file environment.yml
```

## Evaluation signals

- requirements.txt parses without syntax errors and all listed package==version pairs match the documented versions exactly
- Dependency resolver (pip check / pipdeptree) confirms no version conflicts when installed into a clean Python 3.6.12 environment
- environment.yml includes 'python=3.6.12' as the base environment and all pinned packages are listed in the dependencies block
- Installation of requirements.txt into a fresh virtual environment succeeds without version downgrade warnings or unmet transitive dependencies
- Reconstructed environment can import and instantiate the core modules (Keras, TensorFlow, numpy) without ImportError or API version mismatches

## Limitations

- Pinned versions may be incompatible with newer operating systems (e.g., Python 3.6.12 and TensorFlow 1.8.0 are no longer maintained; macOS 12+ may lack binary wheels). Practitioners may need to substitute compatible versions or use Docker containerization.
- Legacy dependency versions (e.g., scikit-learn 0.23.2, scipy 1.0.0) may have unpatched security vulnerabilities; pinning is necessary for reproducibility but practitioners should assess security posture before deployment.
- The skill assumes all pinned versions are documented in plain text (README or similar). If version specifications are embedded in code comments, setup.py, or conda-lock files, the extraction workflow must be adapted.

## Evidence

- [readme] We have implemented our machine learning model using the following software items: 1- Python(3.6.12) 2- Keras (2.2.0) with a Tensorflow(1.8.0) backend. 3- Packages: numpy(1.15.4), sklearn(0.23.2), scipy(1.0.0), seaborn (0.9.0), Pandas(1.1.1.), and h5py(2.7.1): "We have implemented our machine learning model using the following software items: 1- Python(3.6.12) 2- Keras (2.2.0) with a Tensorflow(1.8.0) backend. 3- Packages: numpy(1.15.4), sklearn(0.23.2),"
- [other] Generate a requirements.txt file listing each dependency with its pinned version in the format 'package==version': "Generate a requirements.txt file listing each dependency with its pinned version in the format 'package==version'"
- [other] Validate the requirements.txt syntax and confirm all listed versions are compatible with Python 3.6.12 using dependency resolver tools: "Validate the requirements.txt syntax and confirm all listed versions are compatible with Python 3.6.12 using dependency resolver tools"
- [other] Export environment specification in both requirements.txt and environment.yml (Conda) formats for reproducibility across platforms: "Export environment specification in both requirements.txt and environment.yml (Conda) formats for reproducibility across platforms"
