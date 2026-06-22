---
name: python-dependency-management-with-conda
description: Use when you have a requirements file (e.g., jestr_requirements.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3937
  edam_topics:
  - http://edamontology.org/topic_0769
  tools:
  - Python
  - conda
  - pip
  - CUDA
  - PyTorch
  - CUDA 11.8
derived_from:
- doi: 10.1093/bioinformatics/btaf354
  title: JESTR
evidence_spans:
- This repository contains the python code to train and test the JESTR model
- Please set up the environment as per this file using [conda](http://docs.condi.ioen/latest/)/[pip]
- Please set up the environment as per this file using [conda]
- The model was trained and tested on GPU nVidia A100 with CUDA 11.8
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_jestr_cq
    doi: 10.1093/bioinformatics/btaf354
    title: JESTR
  dedup_kept_from: coll_jestr_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btaf354
  all_source_dois:
  - 10.1093/bioinformatics/btaf354
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Python dependency management with conda

## Summary

Set up and validate a reproducible Python environment with pinned package versions and GPU support using conda and pip, ensuring compatibility with frameworks like PyTorch and specific hardware (e.g., NVIDIA A100 with CUDA 11.8). This skill is essential when reproducing computational workflows that depend on exact package versions and GPU acceleration.

## When to use

You have a requirements file (e.g., jestr_requirements.txt) specifying pinned Python package versions for a GPU-accelerated PyTorch workflow, and you need to reproduce the exact computational environment on your local machine or cluster to run model training, testing, or inference without dependency conflicts or version mismatches.

## When NOT to use

- The workflow does not require GPU acceleration or uses CPU-only PyTorch builds — conda environment setup is still useful but GPU-specific CUDA version pinning is unnecessary.
- You are working in a containerized environment (Docker, Singularity) where dependencies are already baked into the image — redundant environment setup.
- The project uses only pure Python with no binary or compiled dependencies (e.g., CUDA, PyTorch wheels) — simpler pip-only approaches may suffice.

## Inputs

- requirements file (e.g., jestr_requirements.txt with pinned package versions)
- target Python version specification
- target CUDA version and GPU hardware specification (e.g., CUDA 11.8, NVIDIA A100)

## Outputs

- activated conda environment with installed dependencies
- verified GPU availability and PyTorch CUDA detection
- environment report documenting installed package versions and CUDA configuration

## How to apply

Parse the requirements file to extract pinned package versions and Python version. Create a new conda environment with the specified Python version using `conda create`. Install PyTorch with the matching CUDA version (e.g., CUDA 11.8 for NVIDIA A100) using conda or pip to ensure GPU compatibility. Install remaining dependencies listed in the requirements file via `pip install -r jestr_requirements.txt` in the activated environment. Verify GPU availability by running a test script that imports torch and confirms `torch.cuda.is_available()` returns True. Document the final environment state (installed versions, CUDA availability) in an environment report file for reproducibility and troubleshooting.

## Related tools

- **conda** (creates isolated Python environments and resolves package dependencies across OS platforms) — http://docs.conda.ioen/latest/
- **pip** (installs Python packages and dependencies from PyPI within the activated conda environment) — https://pip.pypa.io/en/stable/cli/pip_install/
- **PyTorch** (deep learning framework; installed with CUDA support to enable GPU computation for model training and inference) — https://pytorch.org
- **CUDA 11.8** (GPU computing toolkit; version pinning ensures compatibility with PyTorch wheels and GPU hardware (NVIDIA A100))
- **Python** (host language; version is specified in requirements to ensure compatibility with all downstream packages)

## Examples

```
conda create -n jestr python=3.10 && conda activate jestr && pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 && pip install -r jestr_requirements.txt && python -c 'import torch; print(torch.cuda.is_available())'
```

## Evaluation signals

- Successfully create a new conda environment without package resolution conflicts or version constraint violations
- Import PyTorch inside the environment and confirm `torch.cuda.is_available()` returns True, indicating GPU detection
- Run a simple GPU computation test (e.g., `torch.ones(100, 100).cuda()`) to verify GPU memory allocation works
- Compare output of `pip list` or `conda list` against the pinned versions in the requirements file — all packages should match or be newer (if stated as compatible in README)
- Verify that the environment report documents CUDA version, PyTorch version, and GPU device name (e.g., 'NVIDIA A100') for audit trail

## Limitations

- The README states 'the code and the models have been tested on the package versions mentioned in the jestr_requirements.txt file, but it is likely the code will work on newer versions of the packages as well' — exact version pinning may be overly strict; newer versions often work but are not guaranteed.
- GPU environment setup assumes NVIDIA hardware and CUDA compatibility; workflows running on AMD, Intel, or other GPU architectures will fail or require alternative CUDA/PyTorch configurations.
- Precompiled PyTorch wheels for CUDA 11.8 may not be available or may be deprecated in future conda/pip repositories, forcing manual compilation or version substitution.
- Large package dependencies (e.g., PyTorch with CUDA) require significant disk space and download bandwidth; environment creation can fail on systems with storage or connectivity constraints.

## Evidence

- [readme] The python packages required for JESTR are given in jestr_requirements.txt. Please set up the environment as per this file using conda/pip.: "The python packages required for JESTR are given in jestr_requirements.txt. Please set up the environment as per this file using [conda](http://docs.condi.ioen/latest/)/[pip]"
- [readme] All code runs under the PyTorch framework. The code and the models have been tested on the package versions mentioned in the jestr_requirements.txt file, but it is likely the code will work on newer versions of the packages as well.: "All code runs under the [PyTorch framework](https://pytorch.org). The code and the models have been tested on the package versions mentioned in the jestr_requirements.txt file, but it is likely the"
- [readme] The model was trained and tested on GPU nVidia A100 with CUDA 11.8. The released weights are also for GPU trained models. Please ensure that the environment is set up for GPU.: "The model was trained and tested on GPU nVidia A100 with CUDA 11.8. The released weights are also for GPU trained models. Please ensure that the environment is set up for GPU"
- [other] Verify CUDA availability and PyTorch GPU detection by running a test script that imports torch and confirms torch.cuda.is_available() returns True.: "Verify CUDA availability and PyTorch GPU detection by running a test script that imports torch and confirms torch.cuda.is_available() returns True"
