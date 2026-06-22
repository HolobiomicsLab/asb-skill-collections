---
name: slurm-gpu-resource-allocation
description: Use when you have a machine learning training workflow (e.g., k-fold cross-validation) where each fold is independent, can run in parallel, and requires exactly one GPU per fold.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3372
  tools:
  - SLURM
  - Python
  - MSNovelist
  - Singularity
  - Python (train.py)
derived_from:
- doi: 10.1038/s41592-022-01486-3
  title: MSNovelist
evidence_spans:
- For usage with SLURM, sets up one GPU. Use with `sbatch --array=0-9`
- For usage with SLURM, sets up one GPU
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
---

# slurm-gpu-resource-allocation

## Summary

Configure SLURM job-array submission to allocate one GPU per array index and parallelize multi-fold cross-validation training. This skill ensures reproducible, scalable distributed training on HPC clusters where GPU resources are managed by a scheduling layer.

## When to use

You have a machine learning training workflow (e.g., k-fold cross-validation) where each fold is independent, can run in parallel, and requires exactly one GPU per fold. Your HPC cluster uses SLURM for resource management and you want to launch N identical training jobs (one per fold) in a single batch submission without manual job submission overhead.

## When NOT to use

- Your training workflow has inter-fold dependencies (e.g., fold N+1 requires output from fold N); job arrays assume independence.
- You require fine-grained dynamic GPU allocation per task (e.g., some folds need 2 GPUs, others 1); SLURM arrays use static per-job allocations.
- Your HPC cluster does not support job arrays or does not have GPU resources managed through SLURM (e.g., uses a different scheduler like PBS or HTCondor).

## Inputs

- SLURM batch script template (e.g., run_singularity.sh)
- Training entry point (Python script or containerized shell script, e.g., train.py or train.sh)
- Environment configuration file (.env with DATA_LOC, SIF_LOC, CODE_LOC, RESULTS_LOC)
- Cross-validation dataset partitioned into K folds (e.g., SIRIUS 6 dataset in sirius-novelist/dataset-s6-202311)

## Outputs

- N parallel training job submissions to SLURM queue (one per fold)
- Per-fold model checkpoints and training logs written to RESULTS_LOC
- SLURM job IDs and array task IDs for monitoring and debugging

## How to apply

Write a SLURM batch script (e.g., run_singularity.sh) that uses `sbatch --array=0-9` to define an array job spanning folds 0–9. In the script body, use the SLURM environment variable `$SLURM_ARRAY_TASK_ID` to map each array index to one fold identifier, passed as a parameter to your training entry point (e.g., train.py). Set `#SBATCH --gpus=1` or equivalent to allocate exactly one GPU per job. Each job invokes the training script independently; SLURM schedules these jobs across available GPUs, queuing as needed. Use environment variables (e.g., in a .env file) to configure DATA_LOC, SIF_LOC, CODE_LOC, and RESULTS_LOC so that the training code can locate input data and write results deterministically per fold.

## Related tools

- **SLURM** (Job scheduler and resource manager; submits array jobs and allocates one GPU per array task)
- **Singularity** (Container runtime; encapsulates training environment (Python, dependencies, SIRIUS 6); built on job node and invoked per array task) — https://github.com/apptainer/apptainer
- **Python (train.py)** (Training script; executed inside container per fold, receives fold ID via environment variable or command-line argument) — https://github.com/meowcat/MSNovelist
- **MSNovelist** (Deep learning model for de novo molecular structure generation; trained on cross-validation folds using SIRIUS 6 fingerprints) — https://github.com/meowcat/MSNovelist

## Examples

```
sbatch --array=0-9 run_singularity.sh
```

## Evaluation signals

- SLURM queue submission succeeds: `sbatch --array=0-9 run_singularity.sh` returns a job ID without errors.
- All 10 array tasks are listed by `squeue -j <JOB_ID>` with distinct SLURM_ARRAY_TASK_ID values (0–9).
- Each fold produces its own output directory under RESULTS_LOC (e.g., results/fold_0, results/fold_1, ..., results/fold_9) with non-empty training logs and model artifacts.
- GPU utilization per task is confirmed via `nvidia-smi` on compute nodes during execution (one GPU busy per job).
- Total training time is approximately 1/10 of sequential single-GPU training (allowing for queue wait times and I/O).

## Limitations

- Job arrays require strict independence between folds; any cross-fold synchronization (e.g., averaging) must happen in a post-processing step after all jobs complete.
- SLURM array job failure handling is not automatic; a single failed fold does not automatically trigger retry or rollback of other folds.
- GPU allocation is static per job; if one fold finishes early and another is queued, the freed GPU cannot be dynamically reassigned without manual job management.
- The MSNovelist repository README notes the original codebase is obsolete and recommends using SIRIUS 6 instead; retraining custom variants requires fingerprint data from the target SIRIUS version.

## Evidence

- [other] Use SLURM job-array submission with `sbatch --array=0-9` to launch 10 parallel jobs, each assigned a single GPU.: "The training workflow uses SLURM job-array submission with `sbatch --array=0-9` to launch 10 parallel jobs, each assigned a single GPU."
- [other] Submit jobs using sbatch --array and one GPU per job, with each array index running train.py to train one fold.: "Submit the job array to SLURM using sbatch --array=0-9 run_singularity.sh, launching ten parallel training jobs. Each job invokes train.sh inside the Singularity container, which runs train.py to"
- [other] Set environment variables in .env file pointing to DATA_LOC, SIF_LOC, CODE_LOC, and RESULTS_LOC directories.: "Set environment variables in run_train.sh pointing to DATA_LOC, SIF_LOC, CODE_LOC, and RESULTS_LOC directories configured in .env."
- [methods] For usage with SLURM, sets up one GPU. Use with `sbatch --array=0-9`: "For usage with SLURM, sets up one GPU. Use with `sbatch --array=0-9`"
- [methods] Build singularity image on job node before launching training jobs.: "Build singularity image on job node. Freaks out on login node: SCRATCH_PATH=/cluster/scratch/$(id -un)"
