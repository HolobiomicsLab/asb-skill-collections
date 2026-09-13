---
name: machine-learning-cross-validation-training
description: Use when you have a labeled dataset (e.g., mass spectra with molecular
  structures, SIRIUS 6 fingerprint annotations) that you wish to train a supervised
  deep learning model on, and you need to estimate generalization performance and
  reduce variance from a single train–test split.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
  edam_topics:
  - http://edamontology.org/topic_3474
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - MSNovelist
  - SLURM
  - Singularity
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1038/s41592-022-01486-3
  title: MSNovelist
evidence_spans:
- 'train.py: train one fold of the model'
- singularity build $SCRATCH_PATH/MSNovelist-image/msnovelist.sif docker://stravsm/msnovelist6
- 'run_train.sh: run MSNovelist Singularity container and start `train.sh`'
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

# machine-learning-cross-validation-training

## Summary

Orchestrate k-fold cross-validation model training across parallel GPU-bound compute nodes using SLURM job arrays and containerized environments. This skill ensures reproducible, distributed training of deep learning models on large datasets by partitioning data into k disjoint folds, training k independent model instances in parallel, and aggregating fold-level predictions.

## When to use

You have a labeled dataset (e.g., mass spectra with molecular structures, SIRIUS 6 fingerprint annotations) that you wish to train a supervised deep learning model on, and you need to estimate generalization performance and reduce variance from a single train–test split. The dataset is large enough (e.g., SIRIUS 6 dataset with thousands of spectra) that serial k-fold training would be prohibitively slow, and you have access to a SLURM-managed HPC cluster with per-node GPUs.

## When NOT to use

- Your dataset is very small (n < 100 samples) such that 10-fold stratification produces folds too small to train a deep model reliably; consider fewer folds or a single train–test split.
- You already have a pre-trained model and wish only to evaluate it on held-out test data; this skill is for model training, not inference.
- Your training script does not support or has not been refactored to accept a fold index as input; serial re-runs of the full script on different data subsets are needed first.
- You do not have access to a SLURM cluster or multiple GPUs; single-machine k-fold training is simpler and does not require this orchestration skill.

## Inputs

- labeled training dataset (e.g., MGF file with spectra and SIRIUS 6 annotations, stored in DATA_LOC)
- modular training script accepting fold index (e.g., train.py with --fold argument)
- SLURM batch script template (e.g., run_singularity.sh with job-array directives)
- Singularity container image or Docker registry URI (e.g., docker://stravsm/msnovelist6)
- configuration file (.env) specifying DATA_LOC, CODE_LOC, SIF_LOC, RESULTS_LOC paths

## Outputs

- k fold-specific trained model checkpoints (stored in RESULTS_LOC/fold_0, ..., fold_9)
- per-fold validation metrics and predictions (e.g., CSV files with scores, CSV/pickle with structure predictions)
- aggregated cross-validation performance report (mean and variance of fold-level metrics)
- SLURM job logs (stdout/stderr from each array task, useful for debugging convergence or GPU allocation)

## How to apply

Structure your training codebase into a modular script (e.g., train.py) that accepts a fold index as a command-line argument and trains one model on 9/10 of your data while holding out the corresponding 1/10 fold for validation. Create a SLURM batch script that submits a job array with `sbatch --array=0-9` to launch 10 parallel jobs, each assigned one GPU via SLURM resource requests (e.g., `--gres=gpu:1`). Containerize your training environment (Python, deep learning framework, dependencies) in a Singularity image built from a Docker registry (e.g., `docker://stravsm/msnovelist6`); build the image on a compute node (not the login node) and cache it to a scratch filesystem to avoid repeated rebuilds. In your job script (e.g., run_train.sh), set environment variables pointing to data, code, Singularity image, and results directories, then invoke `singularity exec` to run train.py inside the container for the fold index specified by `$SLURM_ARRAY_TASK_ID`. Each fold trains independently on GPU, writing model weights and validation metrics to a fold-specific results directory. After all 10 jobs complete, concatenate or aggregate the per-fold predictions and metrics to compute overall cross-validation performance (e.g., mean validation loss, F1 score across folds).

## Related tools

- **SLURM** (job scheduler and resource manager; submits job arrays (--array=0-9) to distribute k fold-training jobs across compute nodes, each with one GPU allocation)
- **Singularity** (container engine; encapsulates training environment (Python, PyTorch/TensorFlow, dependencies); built from Docker image on compute node and invoked via singularity exec to run train.py in isolated environment)
- **Python** (programming language for training script (train.py); accepts fold index, loads fold-specific data subset, trains model on GPU, writes results to fold-specific directory)
- **MSNovelist** (example downstream application; trains de novo molecular structure prediction model using 10-fold cross-validation on SIRIUS 6 mass spectrometry dataset) — https://github.com/meowcat/MSNovelist

## Examples

```
sbatch --array=0-9 run_singularity.sh
```

## Evaluation signals

- All k job-array tasks complete successfully (check SLURM log: `sacct -j JOBID` shows all array indices 0–9 with EXIT_CODE 0).
- Each fold produces the expected output files in its results subdirectory (fold-specific model checkpoint, validation metrics CSV, predictions pickle); verify file count and schema consistency across folds.
- Aggregated cross-validation metric (e.g., mean validation loss, mean F1 score) lies within expected range relative to single train–test baseline; significant degradation or unexpected variance may indicate data leakage or fold-stratification failure.
- Per-fold training curves (loss vs. epoch) are smooth and convergent; noisy or divergent curves in individual folds suggest GPU allocation, data loading, or container environment issues.
- Wall-clock time for all 10 folds is approximately 1/10 of serial k-fold time (assuming full GPU utilization); significant deviation suggests job queueing delays or GPU contention.

## Limitations

- Singularity image build must be run on a compute node, not the login node; building on the login node can cause environment conflicts or permission issues.
- Git repository checkout must occur on the login node before submitting jobs; checking out on compute nodes within the job may fail or introduce race conditions across parallel tasks.
- 10-fold cross-validation assumes your dataset is large enough and balanced enough that each fold contains representative samples; highly imbalanced or small datasets may require stratified k-fold or alternative splitting strategies.
- MSNovelist in this repository is retrained on SIRIUS 6 data and cannot be used with other fingerprint systems unless re-trained; the original MSNovelist relied on an old SIRIUS backend that is no longer running.
- Parallel GPU jobs share the same storage backend (scratch filesystem); writing from 10 concurrent jobs to RESULTS_LOC can cause contention or write conflicts if fold-specific subdirectories are not carefully isolated.

## Evidence

- [other] The training workflow uses SLURM job-array submission with sbatch --array=0-9 to launch 10 parallel jobs, each assigned a single GPU.: "uses SLURM job-array submission with `sbatch --array=0-9` to launch 10 parallel jobs, each assigned a single GPU"
- [other] The Singularity image is built on the compute node from the docker://stravsm/msnovelist6 registry, and each array index runs train.py to train one fold of the cross-validation model.: "Singularity image is built on the compute node from the docker://stravsm/msnovelist6 registry, and each array index runs train.py to train one fold"
- [other] On a job node, set SCRATCH_PATH environment variable and build the MSNovelist Singularity image from the stravsm/msnovelist6 Docker image, caching to $SCRATCH_PATH/singularity_cache.: "On a job node, set SCRATCH_PATH environment variable and build the MSNovelist Singularity image from the stravsm/msnovelist6 Docker image, caching to $SCRATCH_PATH"
- [other] Create a SLURM batch script (run_singularity.sh) that calls run_train.sh for each array element, with one GPU allocated per job.: "Create a SLURM batch script (run_singularity.sh) that calls run_train.sh for each array element, with one GPU allocated per job"
- [other] Each job invokes train.sh inside the Singularity container, which runs train.py to train one cross-validation fold of the model on the downloaded SIRIUS 6 dataset.: "Each job invokes train.sh inside the Singularity container, which runs train.py to train one cross-validation fold of the model"
- [methods] Build singularity image on job node. Freaks out on login node: SCRATCH_PATH=/cluster/scratch/$(id -un): "Build singularity image on job node. Freaks out on login node"
- [methods] Checkout git repo on login node. Seemingly doesn't work on job node.: "Checkout git repo on login node. Seemingly doesn't work on job node"
