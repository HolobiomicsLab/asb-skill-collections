---
name: gpu-accelerated-neural-network-training
description: Use when when you have a trainable neural network model (e.g., MSNovelist),
  labeled training data with known input/output pairs, GPU resource availability on
  a compute cluster, and need to optimize model weights via backpropagation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3445
  edam_topics:
  - http://edamontology.org/topic_3474
  - http://edamontology.org/topic_0091
  tools:
  - MSNovelist
  - Python
  - AWS CLI
  - SLURM
  - Singularity
  - PyTorch / TensorFlow
  license_tier: open
derived_from:
- doi: 10.1038/s41592-022-01486-3
  title: MSNovelist
evidence_spans:
- singularity build $SCRATCH_PATH/MSNovelist-image/msnovelist.sif docker://stravsm/msnovelist6
- 'run_train.sh: run MSNovelist Singularity container and start `train.sh`'
- 'train.py: train one fold of the model'
- aws s3 cp --recursive s3://sirius-novelist/dataset-s6-202311 data
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_msnovelist_cq
    doi: 10.1038/s41592-022-01486-3
    title: MSNovelist
  dedup_kept_from: coll_msnovelist_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41592-022-01486-3
  all_source_dois:
  - 10.1038/s41592-022-01486-3
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# gpu-accelerated-neural-network-training

## Summary

Train deep neural network models on GPU-enabled compute nodes using containerized environments and SLURM job scheduling. This skill enables efficient, scalable model training with automatic differentiation and batch processing across single or multiple cross-validation folds.

## When to use

When you have a trainable neural network model (e.g., MSNovelist), labeled training data with known input/output pairs, GPU resource availability on a compute cluster, and need to optimize model weights via backpropagation. Specifically use this skill when training requires iterating over multiple epochs on large batches and you want to measure validation performance per fold.

## When NOT to use

- Input data is already a fully trained model checkpoint — use model evaluation/inference instead.
- Training data is too small to benefit from GPU (rule of thumb: <10 M parameters or <1 GB data) — CPU training may be simpler and faster.
- No GPU resource is available or compute cluster does not support Singularity containerization — fall back to local Docker or conda environments.

## Inputs

- Training dataset (splits by cross-validation fold, e.g., as HDF5, NumPy, or CSV files)
- Model architecture code (e.g., train.py with PyTorch/TensorFlow model definition)
- Dockerfile or container definition for packaging dependencies
- Configuration file (.env with DATA_LOC, SIF_LOC, CODE_LOC, RESULTS_LOC paths)
- SLURM job submission script (e.g., run_singularity.sh with sbatch directives)

## Outputs

- Trained model weights and checkpoints (saved per fold, e.g., .pt or .h5 files)
- Training logs (loss, accuracy, validation metrics per epoch)
- Configuration snapshot (e.g., msnovelist-config-RUNID.yaml recording hyperparameters and data versioning)

## How to apply

Prepare training data and organize it by cross-validation fold. Configure environment variables (.env file) pointing to data location, Singularity container image path, code location, and results output directory. Build a Singularity container on a job node (not login node, as it may fail) that packages the model code, dependencies, and PyTorch/TensorFlow runtime with GPU support. Submit training jobs via sbatch, specifying GPU allocation (typically one GPU per job) and pointing to a training script (e.g., train.py) that loads one fold's data, instantiates the model, runs forward/backward passes, and logs loss per epoch. Monitor training logs for convergence and check for GPU memory errors or shape mismatches indicating incorrect input format. After training, save model checkpoints to the results directory for subsequent evaluation.

## Related tools

- **SLURM** (Job scheduler and resource manager; submits training jobs to compute nodes and allocates GPU)
- **Singularity** (Container runtime; packages model code, Python environment, and PyTorch/TensorFlow with GPU libraries; must be built on job node, not login node)
- **Python** (Language for implementing train.py; orchestrates data loading, model instantiation, training loop, and checkpoint saving)
- **PyTorch / TensorFlow** (Deep learning framework providing automatic differentiation, GPU kernels, and model serialization (implicit in containerized environment))
- **MSNovelist** (Example model architecture trained in this context; receives fingerprint inputs and outputs de novo molecular structures) — https://github.com/meowcat/MSNovelist

## Examples

```
sbatch run_singularity.sh  # Submits training job to SLURM; internally runs singularity exec $SIF_LOC bash run_train.sh, which calls train.py with GPU enabled
```

## Evaluation signals

- Training job completes without GPU out-of-memory errors or CUDA kernel launch failures.
- Training logs show monotonic decrease in loss over epochs (or at least no divergence to NaN/Inf) and validation metrics improve or plateau rather than degrade catastrophically.
- Model checkpoint file size and shape are consistent with architecture definition (e.g., parameter count matches expected layer sizes); no truncated or corrupted checkpoint on disk.
- Fold-level results are reproducible: re-running the same fold with identical random seed produces identical loss trajectory and final weights.
- Input data shape and dtype match model expectations (e.g., fingerprint vectors are 4096-bit, batch size divides training set evenly, no shape mismatches logged).

## Limitations

- The mist branch work on adapting MSNovelist to Morgan 4096-bit fingerprints remains incomplete; fingerprint input layer modifications may still require debugging.
- Singularity build fails on login nodes due to system restrictions; must be built on job nodes, adding a preliminary setup step.
- Original MSNovelist relied on SIRIUS backend no longer running; model is now retrained on SIRIUS 6 data, so training with alternate fingerprint sources requires careful re-validation.
- Single-GPU training per job may be I/O bound if data is not cached locally; distributed multi-GPU training not documented in provided materials.

## Evidence

- [other] Build the MSNovelist Singularity image (stravsm/msnovelist6) on a job node and store at SIF_LOC.: "Build the MSNovelist Singularity image (stravsm/msnovelist6) on a job node and store at SIF_LOC."
- [other] Run training on a single cross-validation fold using sbatch with run_singularity.sh and run_train.sh, which invokes train.py to train one fold with GPU support.: "Run training on a single cross-validation fold using sbatch with run_singularity.sh and run_train.sh, which invokes train.py to train one fold with GPU support."
- [readme] Build singularity image on job node. Freaks out on login node: "Build singularity image on job node. Freaks out on login node"
- [readme] For usage with SLURM, sets up one GPU. Use with `sbatch --array=0-9`: "For usage with SLURM, sets up one GPU. Use with `sbatch --array=0-9`"
- [readme] train.py: train one fold of the model: "train.py: train one fold of the model"
- [other] Inspect training logs and evaluation metrics to confirm the model accepts Morgan fingerprint input without crashes or shape mismatches.: "Inspect training logs and evaluation metrics to confirm the model accepts Morgan fingerprint input without crashes or shape mismatches."
