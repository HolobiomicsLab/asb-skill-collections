---
name: environment-variable-configuration-for-distributed-jobs
description: Use when you have a multi-fold cross-validation training workflow that
  must run as parallel SLURM array jobs, each with its own GPU, and you need to ensure
  that all jobs can locate the same training data, code repository, container image,
  and results directory without hardcoded absolute paths or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3050
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - MSNovelist
  - SLURM
  - Singularity
  - Python (train.py)
  license_tier: open
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

# environment-variable-configuration-for-distributed-jobs

## Summary

Configure environment variables across login and compute nodes to enable portable, reproducible execution of containerized machine learning workflows in SLURM job arrays. This skill ensures that data paths, container images, code repositories, and results directories are correctly mounted and accessible within Singularity containers across distributed GPU-bound training jobs.

## When to use

You have a multi-fold cross-validation training workflow that must run as parallel SLURM array jobs, each with its own GPU, and you need to ensure that all jobs can locate the same training data, code repository, container image, and results directory without hardcoded absolute paths or per-node configuration drift.

## When NOT to use

- Input data is already mounted globally on all compute nodes (NFS or similar); hardcoded paths may suffice.
- Training runs on a single node without job arrays; simpler environment setup suffices.
- Container is not Singularity or does not support explicit --bind mounts for path remapping.

## Inputs

- SLURM batch script template (run_singularity.sh)
- .env configuration file with DATA_LOC, SIF_LOC, CODE_LOC, RESULTS_LOC placeholders
- Train entrypoint scripts (run_train.sh, train.sh)
- Pre-built Singularity container image (SIF file)
- Training dataset (e.g., SIRIUS 6 dataset downloaded to DATA_LOC)
- Checked-out code repository (e.g., MSNovelist GitHub repo)

## Outputs

- Environment variable assignments propagated to all SLURM array jobs
- Validated mount points within running Singularity containers
- Per-fold training logs and model checkpoints written to RESULTS_LOC
- Cross-validation fold assignments indexed by SLURM_ARRAY_TASK_ID

## How to apply

Create a `.env` configuration file that defines four path variables: DATA_LOC (location of training datasets), SIF_LOC (path to the built Singularity image), CODE_LOC (checkout directory of the training code repository), and RESULTS_LOC (output directory for model checkpoints and fold results). Source this `.env` in the SLURM batch script (run_singularity.sh) and in the container entrypoint (run_train.sh and train.sh), ensuring that SCRATCH_PATH is set on the compute node before building the Singularity image to avoid freaks-out on the login node. Pass environment variables explicitly to the container via the train.py invocation so that each fold index receives the correct array element index and GPU assignment. Verify that all four paths are accessible from within the running container by checking file listings at container startup.

## Related tools

- **SLURM** (Job scheduling and resource allocation; submits job arrays with --array=0-9 to spawn 10 parallel training jobs, each with one GPU and access to configuration from .env)
- **Singularity** (Container runtime; executes train.sh and train.py with environment variables sourced from .env, binding DATA_LOC, CODE_LOC, and RESULTS_LOC into the container filesystem)
- **MSNovelist** (Training code repository; checked out on login node, paths referenced via CODE_LOC in .env and mounted into Singularity container for each fold) — https://github.com/meowcat/MSNovelist
- **Python (train.py)** (Cross-validation training script; reads DATA_LOC, receives fold index from SLURM_ARRAY_TASK_ID and GPU assignment via environment variables, writes results to RESULTS_LOC)

## Examples

```
sbatch --array=0-9 run_singularity.sh
```

## Evaluation signals

- All four environment variables (DATA_LOC, SIF_LOC, CODE_LOC, RESULTS_LOC) are defined and non-empty in the sourced .env file.
- Each SLURM array job logs confirm that the container successfully mounted all four paths at startup (e.g., 'ls -la $DATA_LOC' produces file listings).
- Each fold's training logs and model checkpoints appear in RESULTS_LOC with correct fold numbering matching SLURM_ARRAY_TASK_ID (0–9).
- No 'file not found' or 'permission denied' errors appear in job logs related to DATA_LOC, CODE_LOC, or RESULTS_LOC during training startup.
- SCRATCH_PATH is set before Singularity image build on compute node; build does not fail with 'cannot write to $SCRATCH_PATH' errors.

## Limitations

- Singularity container build fails on login node if SCRATCH_PATH is not set; must be executed on a compute node with sufficient local scratch storage.
- Git repository checkout must use core.autocrlf=false on Windows to avoid line-ending corruption; does not work reliably on job nodes.
- Paths in .env must be absolute or resolvable from the compute node environment; relative paths or $HOME variables may fail across heterogeneous login/compute node configurations.
- Each fold runs independently; no shared state or inter-fold communication is possible, limiting distributed optimization strategies that require fold-to-fold synchronization.

## Evidence

- [methods] Set up `.env` configuration with DATA_LOC, SIF_LOC, CODE_LOC, RESULTS_LOC paths: "Set up `.env` such that it looks more or less like this: DATA_LOC, SIF_LOC, CODE_LOC, RESULTS_LOC"
- [methods] SCRATCH_PATH must be set before Singularity build to avoid failures on login node: "Build singularity image on job node. Freaks out on login node: SCRATCH_PATH=/cluster/scratch/$(id -un)"
- [methods] run_train.sh sources environment variables and runs MSNovelist container with training entrypoint: "run_train.sh: run MSNovelist Singularity container and start `train.sh` in the container"
- [methods] train.sh sets environment variables and executes train.py for one cross-validation fold: "train.sh: set environment variables and run `train.py`"
- [methods] SLURM job-array submission with one GPU per fold, indexed by array element: "For usage with SLURM, sets up one GPU. Use with `sbatch --array=0-9`"
- [readme] Docker image contains all dependencies; no external configuration required: "the Docker container packages all required software and data"
