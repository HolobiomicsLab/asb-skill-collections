---
name: pytorch-installation-and-verification
description: Use when when setting up a computational environment to run pre-trained
  PyTorch models that were trained on GPU hardware (e.g., NVIDIA A100 with CUDA 11.8),
  and the released model weights are GPU-trained artifacts. Specifically, when you
  have a jestr_requirements.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3346
  edam_topics:
  - http://edamontology.org/topic_3372
  tools:
  - PyTorch
  - pip
  - CUDA
  - conda
  - CUDA 11.8
  license_tier: open
derived_from:
- doi: 10.1093/bioinformatics/btaf354
  title: JESTR
evidence_spans:
- All code runs under the [PyTorch framework](https://pytorch.org)
- All code runs under the [PyTorch framework](https://pytorch.org).
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btaf354
  all_source_dois:
  - 10.1093/bioinformatics/btaf354
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# pytorch-installation-and-verification

## Summary

Install PyTorch with CUDA 11.8 support in a conda environment and verify GPU availability for running GPU-trained deep learning models. This skill ensures that a machine learning workflow has access to GPU compute resources required by pre-trained PyTorch models.

## When to use

When setting up a computational environment to run pre-trained PyTorch models that were trained on GPU hardware (e.g., NVIDIA A100 with CUDA 11.8), and the released model weights are GPU-trained artifacts. Specifically, when you have a jestr_requirements.txt file specifying PyTorch dependencies and need to confirm GPU detection before attempting inference or training.

## When NOT to use

- CPU-only workflows or when GPU acceleration is not required for your analysis
- Systems without NVIDIA GPU hardware or CUDA 11.8 toolkit support
- When you are using pre-trained model weights for a CPU environment (README states released weights are GPU-trained models)

## Inputs

- jestr_requirements.txt (pinned package versions and dependencies file)
- Python version specification (from requirements file)
- System with NVIDIA GPU hardware and compatible drivers

## Outputs

- Activated conda environment with PyTorch and CUDA 11.8 installed
- Boolean confirmation that torch.cuda.is_available() == True
- Environment report file documenting installed versions

## How to apply

Parse jestr_requirements.txt to extract the pinned PyTorch version and CUDA specification. Create a new conda environment with the Python version specified in the requirements file. Install PyTorch with CUDA 11.8 support using pip or conda, ensuring GPU compatibility with NVIDIA A100 or equivalent hardware. After installation, verify CUDA availability and PyTorch GPU detection by running a test script that imports torch and confirms torch.cuda.is_available() returns True. If verification fails, check that NVIDIA drivers are installed and CUDA 11.8 toolkit is accessible on the system. Document the environment configuration and installed versions in an environment report file for reproducibility.

## Related tools

- **PyTorch** (Deep learning framework in which all JESTR code runs; must be installed with CUDA 11.8 support for GPU execution) — https://pytorch.org
- **conda** (Environment manager used to create isolated Python environment and install PyTorch with CUDA support) — http://docs.condi.ioen/latest/
- **pip** (Package installer used to install PyTorch and remaining dependencies from jestr_requirements.txt) — https://pip.pypa.io/en/stable/cli/pip_install/
- **CUDA 11.8** (GPU compute framework that PyTorch requires; model was trained and tested with this specific version on NVIDIA A100)

## Examples

```
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}'); print(f'CUDA version: {torch.version.cuda}'); print(f'Device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU"}')"
```

## Evaluation signals

- torch.cuda.is_available() returns True when test script is executed
- CUDA version reported by torch.version.cuda matches or is compatible with 11.8
- GPU device is detected and named correctly (e.g., 'NVIDIA A100' or equivalent in torch.cuda.get_device_name(0))
- All packages in jestr_requirements.txt are installed with versions matching or exceeding the pinned versions
- Environment report file documents the PyTorch version, CUDA version, and GPU device information without errors

## Limitations

- Code has only been tested on the specific package versions mentioned in jestr_requirements.txt; newer package versions may introduce compatibility issues despite the README stating the code 'is likely' to work on newer versions
- Released model weights are GPU-trained artifacts and may not work correctly in CPU-only environments
- CUDA 11.8 and NVIDIA A100 (or equivalent GPU with CUDA 11.8 support) are required; other CUDA versions or GPU architectures are not documented as supported

## Evidence

- [readme] All code runs under the PyTorch framework: "All code runs under the [PyTorch framework](https://pytorch.org)"
- [readme] The model was trained and tested on GPU nVidia A100 with CUDA 11.8: "The model was trained and tested on GPU nVidia A100 with CUDA 11.8"
- [readme] Released weights are for GPU trained models requiring GPU setup: "The released weights are also for GPU trained models. Please ensure that the environment is set up for GPU"
- [readme] Environment setup via conda/pip from jestr_requirements.txt: "The python packages required for JESTR are given in jestr_requirements.txt. Please set up the environment as per this file using [conda](http://docs.condi.ioen/latest/)/[pip]"
- [readme] Code tested on package versions in requirements but likely works on newer versions: "The code and the models have been tested on the package versions mentioned in the jestr_requirements.txt file, but it is likely the code will work on newer versions of the packages as well"
