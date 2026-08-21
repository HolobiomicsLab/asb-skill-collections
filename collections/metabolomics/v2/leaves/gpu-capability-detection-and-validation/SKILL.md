---
name: gpu-capability-detection-and-validation
description: Use when after setting up a conda/pip environment with PyTorch and CUDA,
  before loading pretrained model weights or running inference/training pipelines.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - pip
  - CUDA
  - PyTorch
  - conda / pip
  license_tier: open
  provenance_tier: literature
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

# GPU capability detection and validation

## Summary

Verify that a PyTorch environment has GPU support enabled and can access NVIDIA hardware (e.g., A100, CUDA 11.8), critical for running pre-trained deep learning models that were trained on GPU. This skill confirms the environment is correctly configured before attempting to load and execute GPU-trained model weights.

## When to use

After setting up a conda/pip environment with PyTorch and CUDA, before loading pretrained model weights or running inference/training pipelines. Use this skill whenever the artifact documentation specifies that released weights are GPU-trained models (as in JESTR) or when deployment target requires a specific GPU generation (e.g., NVIDIA A100) or CUDA version (e.g., 11.8).

## When NOT to use

- Model is CPU-only by design or inference latency is not a constraint and CPU execution is acceptable.
- Working with CPU-trained model weights; validation is unnecessary if the model was never trained or deployed on GPU.
- Running on a headless cluster node where no NVIDIA hardware is present and CPU fallback is the intended deployment target.

## Inputs

- Initialized PyTorch installation (torch module importable)
- CUDA Toolkit installation (if GPU is present)
- Optional: requirements.txt or params.yaml specifying target GPU model and CUDA version

## Outputs

- Boolean confirmation of GPU availability (torch.cuda.is_available() result)
- GPU device name and properties (device model, compute capability, memory)
- Active CUDA version string
- Environment report file (text or JSON) documenting GPU configuration and validation outcome

## How to apply

Import torch in Python and execute torch.cuda.is_available() to confirm GPU detection at runtime. If True, query torch.cuda.get_device_name(0) to identify the GPU model and verify it matches documented requirements (e.g., A100 for JESTR). Check torch.version.cuda to confirm the active CUDA version matches the training environment (e.g., 11.8). Document the GPU device name, CUDA version, and availability status in a configuration or environment report file. If is_available() returns False, the environment setup is incomplete and must be corrected before proceeding with model loading.

## Related tools

- **PyTorch** (Provides torch.cuda.is_available(), torch.cuda.get_device_name(), and torch.version.cuda to query GPU state and CUDA version at runtime) — https://pytorch.org
- **CUDA** (Underlying GPU compute framework; version (e.g., 11.8) must match the environment where pretrained weights were generated to ensure numerical consistency)
- **conda / pip** (Environment managers used to install PyTorch with CUDA support; correct installation is prerequisite for GPU detection) — http://docs.conda.io/latest/ or https://pip.pypa.io/en/stable/cli/pip_install/

## Examples

```
import torch; print(f'GPU available: {torch.cuda.is_available()}'); print(f'Device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else "None"}'); print(f'CUDA version: {torch.version.cuda}')
```

## Evaluation signals

- torch.cuda.is_available() returns True (GPU is detected and accessible to PyTorch)
- torch.cuda.get_device_name(0) matches documented target hardware (e.g., 'NVIDIA A100-SXM4-40GB' for JESTR)
- torch.version.cuda string matches or is compatible with training CUDA version (e.g., '11.8' for JESTR)
- Environment report file is created and contains non-empty GPU device name and CUDA version (indicates validation completed)
- Subsequent model.to('cuda') or model.cuda() commands execute without errors and move model to GPU memory

## Limitations

- torch.cuda.is_available() may return True even if only one of multiple GPUs is functional; full validation requires querying all devices.
- CUDA version string from torch.version.cuda may differ slightly from system nvcc --version; compatibility is approximate, not exact.
- If pretrained weights were trained on A100 but inference environment has A10G or V100, numerical differences may arise due to different compute capabilities, even with matching CUDA versions.
- Docker or containerized environments may report GPU as unavailable if --gpus flag or nvidia-docker runtime is not configured correctly, masking a valid underlying installation.

## Evidence

- [readme] The model was trained and tested on GPU nVidia A100 with CUDA 11.8: "The model was trained and tested on GPU nVidia A100 with CUDA 11.8"
- [readme] The released weights are also for GPU trained models. Please ensure that the environment is set up for GPU.: "The released weights are also for GPU trained models. Please ensure that the environment is set up for GPU"
- [intro] Verify CUDA availability and PyTorch GPU detection by running a test script that imports torch and confirms torch.cuda.is_available() returns True: "Verify CUDA availability and PyTorch GPU detection by running a test script that imports torch and confirms torch.cuda.is_available() returns True"
