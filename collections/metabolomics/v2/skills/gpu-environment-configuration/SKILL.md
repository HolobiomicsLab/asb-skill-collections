---
name: gpu-environment-configuration
description: Use when you need to run a PyTorch model that was trained on GPU (e.g., JESTR with released NPLIB1 weights) and require verified GPU availability (torch.cuda.is_available() returns True). Apply this skill when you have a requirements.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_3372
  tools:
  - pip
  - CUDA
  - PyTorch
  - conda
  - CUDA 11.8
derived_from:
- doi: 10.1093/bioinformatics/btaf354
  title: JESTR
evidence_spans:
- Please set up the environment as per this file using [conda](http://docs.condi.ioen/latest/)/[pip]
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

# gpu-environment-configuration

## Summary

Configure a GPU-capable Python environment with pinned package versions and CUDA 11.8 support for running PyTorch-based machine learning models. This skill ensures reproducibility and GPU detection for models trained on NVIDIA A100 hardware.

## When to use

You need to run a PyTorch model that was trained on GPU (e.g., JESTR with released NPLIB1 weights) and require verified GPU availability (torch.cuda.is_available() returns True). Apply this skill when you have a requirements.txt or requirements file specifying pinned package versions and the source model documentation specifies CUDA version and GPU hardware used for training.

## When NOT to use

- You are running inference on CPU only or have no GPU hardware available; use a CPU-compatible environment instead.
- The model was trained on CPU or a different CUDA version (e.g., CUDA 12.0); verify CUDA compatibility before applying this skill.
- Your target hardware is not NVIDIA-based (e.g., AMD GPU, Apple Silicon); PyTorch CUDA setup is specific to NVIDIA architecture.

## Inputs

- jestr_requirements.txt (or equivalent requirements file with pinned versions)
- Target Python version specification
- CUDA version specification (11.8 in this case)

## Outputs

- Activated conda environment with all dependencies installed
- Confirmed GPU availability (torch.cuda.is_available() == True)
- Environment report file documenting installed package versions and CUDA configuration

## How to apply

Parse the jestr_requirements.txt file to extract pinned Python package versions and the target Python version. Create a new conda environment with the specified Python version, then install PyTorch with CUDA 11.8 support using pip or conda to ensure NVIDIA A100 or equivalent GPU compatibility. Install all remaining dependencies from the requirements file into the activated conda environment using pip. Verify the configuration by running a test script that imports torch and confirms torch.cuda.is_available() returns True, indicating the GPU is properly detected. Document the final environment configuration including all installed package versions in an environment report file.

## Related tools

- **PyTorch** (Deep learning framework requiring GPU support via CUDA; code execution environment for JESTR model) — https://pytorch.org
- **conda** (Environment manager for creating isolated Python environments with pinned package versions) — http://docs.condi.ioen/latest/
- **pip** (Package installer for dependencies and PyTorch CUDA variants within conda environment) — https://pip.pypa.io/en/stable/cli/pip_install/
- **CUDA 11.8** (GPU compute platform required for PyTorch GPU execution on NVIDIA hardware)

## Examples

```
conda create -n jestr python=3.10 && conda activate jestr && pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 && pip install -r jestr_requirements.txt && python -c "import torch; print('GPU available:', torch.cuda.is_available())"
```

## Evaluation signals

- torch.cuda.is_available() returns True when importing torch in the activated environment
- All pinned package versions from jestr_requirements.txt are installed (verify with pip list or conda list)
- Environment report file exists and documents CUDA version as 11.8 and GPU hardware availability
- No import errors occur when running `import torch; import [all_major_dependencies]` in the environment
- PyTorch can instantiate and move a test tensor to GPU without errors (e.g., torch.zeros(1).cuda())

## Limitations

- Setup is specific to NVIDIA GPU hardware (A100 or equivalent); will not provide GPU acceleration on non-NVIDIA platforms.
- CUDA 11.8 compatibility is fixed for the released JESTR weights; attempting newer PyTorch or CUDA versions may cause model loading or numerical discrepancies, though README notes code likely works on newer package versions.
- Large package downloads and compilation time required; network access and sufficient disk space (typically 5–15 GB) are prerequisites.
- GPU memory requirements vary by model size and batch size; this skill configures the environment but does not handle out-of-memory errors during model execution.

## Evidence

- [readme] The model was trained and tested on GPU nVidia A100 with CUDA 11.8. The released weights are also for GPU trained models. Please ensure that the environment is set up for GPU.: "The model was trained and tested on GPU nVidia A100 with CUDA 11.8. The released weights are also for GPU trained models. Please ensure that the environment is set up for GPU."
- [readme] The python packages required for JESTR are given in jestr_requirements.txt. Please set up the environment as per this file using [conda](http://docs.condi.ioen/latest/)/[pip](https://pip.pypa.io/en/stable/cli/pip_install/). All code runs under the [PyTorch framework](https://pytorch.org).: "The python packages required for JESTR are given in jestr_requirements.txt. Please set up the environment as per this file using [conda]/[pip]. All code runs under the [PyTorch framework]"
- [readme] The code and the models have been tested on the package versions mentioned in the jestr_requirements.txt file, but it is likely the code will work on newer versions of the packages as well: "The code and the models have been tested on the package versions mentioned in the jestr_requirements.txt file, but it is likely the code will work on newer versions"
- [other] Verify CUDA availability and PyTorch GPU detection by running a test script that imports torch and confirms torch.cuda.is_available() returns True.: "Verify CUDA availability and PyTorch GPU detection by running a test script that imports torch and confirms torch.cuda.is_available() returns True."
