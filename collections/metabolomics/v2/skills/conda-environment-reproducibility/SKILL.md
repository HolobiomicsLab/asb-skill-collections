---
name: conda-environment-reproducibility
description: Use when you have received a conda/pip requirements file (e.g., jestr_requirements.txt) and need to run code that was trained and tested on a specific GPU setup (e.g., NVIDIA A100 with CUDA 11.8).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0338
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - conda
  - pip
  - CUDA
  - PyTorch
  - CUDA 11.8
  - NVIDIA GPU drivers
derived_from:
- doi: 10.1093/bioinformatics/btaf354
  title: JESTR
evidence_spans:
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
---

# conda-environment-reproducibility

## Summary

Reconstruct a GPU-capable Python environment from a pinned requirements file using conda and pip, ensuring reproducibility of package versions and CUDA compatibility for PyTorch-based scientific code. This skill validates that the environment correctly detects GPU hardware and matches the original training conditions.

## When to use

You have received a conda/pip requirements file (e.g., jestr_requirements.txt) and need to run code that was trained and tested on a specific GPU setup (e.g., NVIDIA A100 with CUDA 11.8). Use this skill when you must guarantee that all transitive dependencies, version pinning, and GPU detection match the original computational environment to avoid model weight incompatibility or silent numerical divergence.

## When NOT to use

- Code is CPU-only and has no GPU dependencies; standard pip install in a venv is simpler.
- You are working with pre-compiled Docker/Singularity containers that already bundle the frozen environment; use the container directly.
- The requirements file is known to be stale or incompatible with your hardware (e.g., CUDA 11.8 requirements on a machine with only CUDA 12.x drivers installed); negotiate driver/toolkit compatibility first.

## Inputs

- jestr_requirements.txt or equivalent pinned requirements file
- Python version specification (from requirements or documentation)
- Target CUDA version (from README or model metadata)
- NVIDIA GPU hardware availability and driver version

## Outputs

- Activated conda environment with all dependencies installed
- Confirmed torch.cuda.is_available() == True
- Environment report documenting package versions and GPU device name
- Successfully imported PyTorch model weights compatible with GPU

## How to apply

Parse the requirements file to extract pinned package versions and dependencies. Create a new conda environment with the Python version specified in the file. Install PyTorch with the matching CUDA version (e.g., CUDA 11.8 for A100-trained models) using pip or conda, ensuring the CUDA toolkit matches the GPU hardware available. Install all remaining dependencies from the requirements file into the activated environment. Verify GPU detection by running a test script that imports torch and confirms torch.cuda.is_available() returns True and the detected device matches your hardware (e.g., 'cuda:0'). Document the final environment state by capturing conda list output and confirmed CUDA/GPU details.

## Related tools

- **conda** (Environment manager; creates isolated Python environments and installs packages from conda-forge and defaults channels) — http://docs.condi.ioen/latest/
- **pip** (Package installer; installs PyPI packages and respects pinned versions in requirements files) — https://pip.pypa.io/en/stable/cli/pip_install/
- **PyTorch** (Deep learning framework; provides CUDA-aware tensor operations and model weight loading for GPU training) — https://pytorch.org
- **CUDA 11.8** (GPU compute toolkit; enables PyTorch and other libraries to compile and execute kernels on NVIDIA A100 and compatible GPUs)
- **NVIDIA GPU drivers** (Hardware interface layer; must match CUDA toolkit version to enable torch.cuda.is_available() detection)

## Examples

```
conda create -n jestr python=3.9 && conda activate jestr && pip install torch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia && pip install -r jestr_requirements.txt && python -c "import torch; print('GPU available:', torch.cuda.is_available()); print('Device:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'N/A')"
```

## Evaluation signals

- torch.cuda.is_available() returns True in a Python interpreter within the environment
- torch.cuda.get_device_name(0) matches your GPU model (e.g., 'NVIDIA A100-SXM4-40GB')
- conda list output shows exact pinned versions matching jestr_requirements.txt with no unintended upgrades
- Pretrained model weights load without dtype or device mismatch errors; inference runs on GPU (observable via nvidia-smi showing GPU memory consumption)
- Environment report documents final package manifest and confirmed CUDA version matching the original training hardware

## Limitations

- Code has been tested on package versions in jestr_requirements.txt but may work on newer versions; no guarantee of forward compatibility with future package majors.
- GPU-trained model weights are incompatible with CPU environments; attempting to load them on CPU will fail or produce incorrect results.
- CUDA version mismatch (e.g., installing CUDA 12.x binaries into an environment intended for CUDA 11.8) will cause runtime device errors or silent numerical divergence.
- Other datasets beyond NPLIB1 are under licensing agreements that prohibit public release; environment reproducibility does not grant data access.
- conda environment is machine-specific; conda-lock files are recommended for true cross-platform reproducibility (not provided in this README).

## Evidence

- [readme] The python packages required for JESTR are given in jestr_requirements.txt. Please set up the environment as per this file using conda/pip.: "The python packages required for JESTR are given in jestr_requirements.txt. Please set up the environment as per this file using [conda](http://docs.condi.ioen/latest/)/[pip]"
- [readme] The code and the models have been tested on the package versions mentioned in the jestr_requirements.txt file, but it is likely the code will work on newer versions of the packages as well.: "The code and the models have been tested on the package versions mentioned in the jestr_requirements.txt file, but it is likely the code will work on newer versions of the packages as well"
- [readme] The model was trained and tested on GPU nVidia A100 with CUDA 11.8. The released weights are also for GPU trained models. Please ensure that the environment is set up for GPU.: "The model was trained and tested on GPU nVidia A100 with CUDA 11.8. The released weights are also for GPU trained models. Please ensure that the environment is set up for GPU"
- [intro] Install PyTorch with CUDA 11.8 support using pip or conda, ensuring GPU compatibility with NVIDIA A100 or equivalent hardware.: "Install PyTorch with CUDA 11.8 support using pip or conda, ensuring GPU compatibility with NVIDIA A100 or equivalent hardware"
- [intro] Verify CUDA availability and PyTorch GPU detection by running a test script that imports torch and confirms torch.cuda.is_available() returns True.: "Verify CUDA availability and PyTorch GPU detection by running a test script that imports torch and confirms torch.cuda.is_available() returns True"
