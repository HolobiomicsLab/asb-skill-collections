---
name: hpc-job-array-orchestration
description: Use when you have a machine learning training workflow (e.g., k-fold cross-validation) where each fold is independent, GPU-accelerated, and can run in parallel.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3372
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - MSNovelist
  - SLURM
  - Singularity
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# hpc-job-array-orchestration

## Summary

Configure and submit SLURM job arrays to parallelize multi-fold cross-validation training across compute nodes, with each array index assigned a dedicated GPU and containerized execution environment. This orchestration pattern scales embarrassingly-parallel training tasks without manual job submission overhead.

## When to use

You have a machine learning training workflow (e.g., k-fold cross-validation) where each fold is independent, GPU-accelerated, and can run in parallel. You are running on an HPC cluster with SLURM workload management and want to avoid manual per-fold job submission while ensuring reproducible, containerized execution across heterogeneous compute nodes.

## When NOT to use

- Training tasks have inter-fold dependencies (e.g., ensemble aggregation during training rather than post-hoc)—use a DAG scheduler (Snakemake, Nextflow) instead.
- The cluster does not support SLURM or GPU allocation is not available—use single-machine multi-processing (multiprocessing, Ray) or a different scheduler.
- You need dynamic task allocation based on runtime performance—job arrays are static; consider task queues or adaptive schedulers.

## Inputs

- SLURM batch script template (run_singularity.sh)
- Singularity container image (.sif) or Docker image URI (e.g., docker://stravsm/msnovelist6)
- .env configuration file with DATA_LOC, SIF_LOC, CODE_LOC, RESULTS_LOC paths
- Training code and data (e.g., train.py, SIRIUS 6 dataset)
- Optional: pre-built Singularity image cache in $SCRATCH_PATH

## Outputs

- 10 (or N) completed training logs per fold
- Per-fold model checkpoints and validation metrics
- Aggregated cross-validation results (mean fold scores, confidence intervals)
- SLURM job metadata (job IDs, runtimes, GPU utilization)

## How to apply

First, define the total number of folds (or parallel tasks) as your array range—e.g., `--array=0-9` for 10-fold CV. Create a SLURM batch script (e.g., `run_singularity.sh`) that allocates one GPU per array job and invokes a secondary wrapper script (e.g., `run_train.sh`) parameterized by the SLURM array task ID (`$SLURM_ARRAY_TASK_ID`). The wrapper script sets environment variables pointing to data, code, Singularity image, and results directories (typically managed via a `.env` file), then launches the containerized training entry point (e.g., `train.sh`) inside the Singularity image. Submit the entire job array with a single `sbatch` command; SLURM automatically distributes array tasks across available nodes and manages GPU allocation. Monitor progress via `squeue` or post-job logs to confirm all folds completed and training loss curves converged per fold.

## Related tools

- **SLURM** (Workload manager for job array submission, GPU allocation, and compute node scheduling)
- **Singularity** (Container runtime for reproducible, isolated execution of training code across heterogeneous compute nodes; built from Docker images)
- **MSNovelist** (Example training application (de novo structure prediction from mass spectra) executed per cross-validation fold) — https://github.com/meowcat/MSNovelist
- **Python** (Training script runtime (train.py executes one fold per array task))

## Examples

```
sbatch --array=0-9 run_singularity.sh
```

## Evaluation signals

- All 10 (or N) array tasks complete with exit code 0 and appear in SLURM accounting (sacct output shows COMPLETED state).
- Each fold produces expected output files (e.g., fold_0_model.pkl, fold_0_metrics.csv) in RESULTS_LOC, with timestamps matching job runtime.
- Training loss per fold shows convergence within typical ranges; no fold is an obvious outlier (e.g., one fold with NaN loss while others are finite).
- GPU memory utilization per job is consistent with the container and batch size; no OOM (out-of-memory) errors in job logs.
- Cross-validation scores (mean ± std across folds) are within expected ranges for the dataset; standard deviation is non-zero, indicating genuine fold-to-fold variation.

## Limitations

- Singularity image must be built on a compute node (not login node); building on login nodes causes environment conflicts (e.g., SCRATCH_PATH not available).
- Job arrays are static; all N folds must be specified at submission time. If a fold fails mid-training, the user must manually resubmit that fold or the entire array.
- Git repository checkout must occur on the login node before array submission; checking out on job nodes is unreliable, likely due to network isolation.
- The Docker image used for Singularization (e.g., stravsm/msnovelist6) must be compatible with the host container runtime and CUDA/GPU drivers on compute nodes; version mismatches cause runtime failures.
- Data download and caching (e.g., AWS S3 to $SCRATCH_PATH) must complete before training begins; if datasets are large, this adds non-parallelizable overhead and may exceed wall-clock limits.

## Evidence

- [other] Each array index runs train.py to train one fold of the cross-validation model.: "each array index runs train.py to train one fold of the cross-validation model"
- [other] SLURM job-array submission with sbatch --array=0-9 launches 10 parallel jobs, each assigned a single GPU.: "SLURM job-array submission with `sbatch --array=0-9` to launch 10 parallel jobs, each assigned a single GPU"
- [other] Singularity image is built on the compute node from the docker://stravsm/msnovelist6 registry.: "The Singularity image is built on the compute node from the docker://stravsm/msnovelist6 registry"
- [methods] Build singularity image on job node. Freaks out on login node: set SCRATCH_PATH first.: "Build singularity image on job node. Freaks out on login node: SCRATCH_PATH=/cluster/scratch/$(id -un)"
- [methods] Checkout git repo on login node. Seemingly doesn't work on job node.: "Checkout git repo on login node. Seemingly doesn't work on job node"
- [other] Set environment variables in run_train.sh pointing to DATA_LOC, SIF_LOC, CODE_LOC, and RESULTS_LOC directories configured in .env.: "Set environment variables in run_train.sh pointing to DATA_LOC, SIF_LOC, CODE_LOC, and RESULTS_LOC directories configured in .env"
- [methods] To train, run: sbatch run_singularity.sh: "To train, run: sbatch run_singularity.sh"
- [methods] train.sh: set environment variables and run `train.py`: "train.sh: set environment variables and run `train.py`"
