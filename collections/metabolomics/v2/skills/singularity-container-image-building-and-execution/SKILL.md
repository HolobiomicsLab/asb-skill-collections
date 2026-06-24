---
name: singularity-container-image-building-and-execution
description: Use when you have a Docker image published to a registry (e.g., docker://stravsm/msnovelist6),
  need to run it on an HPC cluster with SLURM scheduling, and must allocate specific
  hardware resources (GPUs, RAM) per job.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3552
  edam_topics:
  - http://edamontology.org/topic_3316
  - http://edamontology.org/topic_0769
  tools:
  - Singularity
  - Python
  - MSNovelist
  - SLURM
  license_tier: open
derived_from:
- doi: 10.1038/s41592-022-01486-3
  title: MSNovelist
evidence_spans:
- 'Build singularity image on job node. Freaks out on login node: ``` SCRATCH_PATH=/cluster/scratch/$(id'
- Build singularity image on job node
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

# singularity-container-image-building-and-execution

## Summary

Build a Singularity container image from a Docker registry on a compute node and execute containerized workflows with resource constraints (GPU binding, environment variable injection). This skill is essential for deploying complex scientific pipelines on HPC systems where login nodes cannot perform image construction but job nodes can.

## When to use

You have a Docker image published to a registry (e.g., docker://stravsm/msnovelist6), need to run it on an HPC cluster with SLURM scheduling, and must allocate specific hardware resources (GPUs, RAM) per job. Use this when your workflow requires isolation of dependencies and reproducible execution across compute nodes.

## When NOT to use

- Input Docker image is already available as a pre-built .sif file on the cluster; skip to execution.
- Your HPC system has Singularity image caching already managed by administrators; building locally may duplicate effort.
- The containerized task requires interactive I/O or real-time monitoring; SLURM batch submission is not appropriate.

## Inputs

- Docker image URI (e.g., docker://stravsm/msnovelist6)
- SLURM batch script template (run_singularity.sh)
- Environment configuration file (.env with DATA_LOC, SIF_LOC, CODE_LOC, RESULTS_LOC)
- Local data directories to be mounted into container
- Source code repository (cloned on login node)

## Outputs

- Singularity image file (.sif) cached at $SCRATCH_PATH
- Containerized job output logs and results
- Per-fold training checkpoints or prediction artifacts (stored in RESULTS_LOC)
- SLURM job array submission confirmation and task IDs

## How to apply

First, on the login node, checkout the source repository from GitHub. Second, on a compute node (via sbatch or interactive job), set SCRATCH_PATH to a writable cluster scratch directory and build the Singularity image from the Docker registry using `singularity build $SCRATCH_PATH/image.sif docker://registry/image:tag`, caching to $SCRATCH_PATH/singularity_cache to avoid repeated pulls. Third, create a SLURM batch script that invokes the containerized entrypoint (e.g., train.sh) for each array element, binding local directories (DATA_LOC, CODE_LOC, RESULTS_LOC) via `--bind` flags. Fourth, inject environment variables into the container via `singularity exec` or `singularity run` with explicit `--env` or shell exports. Finally, submit the batch script to SLURM using `sbatch --array=0-9` to launch parallel jobs, each assigned one GPU per array index. Verify image integrity by checking the .sif file size and running a test invocation before full submission.

## Related tools

- **Singularity** (Container runtime and image builder; orchestrates Docker image pull, layer merging, and .sif file creation on compute node)
- **SLURM** (Job scheduler and resource allocator; submits batch script with --array and --gpus flags to distribute array jobs across compute nodes)
- **MSNovelist** (Example containerized scientific application; provides train.py and train.sh entrypoint scripts executed inside the container per fold) — https://github.com/meowcat/MSNovelist
- **Python** (Training and inference script language; train.py runs inside container to train one cross-validation fold)

## Examples

```
singularity build $SCRATCH_PATH/msnovelist.sif docker://stravsm/msnovelist6 && sbatch --array=0-9 run_singularity.sh
```

## Evaluation signals

- Singularity image file exists at $SCRATCH_PATH and has non-zero size (>1 GB for typical scientific images)
- SLURM job array submission succeeds with confirmation of job IDs (e.g., 'Submitted batch job 12345_[0-9]')
- Each array job logs show container invocation and no sandbox/permission errors (grep 'Singularity' or 'train.py' in job output)
- Environment variables (DATA_LOC, RESULTS_LOC) are correctly bound and accessible inside container (verify with `ls` or output file presence)
- GPU assignments match array index mapping (one GPU per fold); check SLURM accounting with `sacct --format=JobID,GRES`

## Limitations

- Image building must occur on a compute node with sufficient scratch space; login nodes often lack permissions or temporary storage.
- Docker image registry must be accessible from compute nodes; no support for private registries without pre-configured credentials.
- Singularity caching to $SCRATCH_PATH can fail if the cluster scratch filesystem is full or has per-user quotas; monitor with `df` and `quota`.
- Port forwarding and interactive shells are limited in batch mode; web UIs or real-time monitoring require separate interactive job submission.

## Evidence

- [methods] Build singularity image on job node. Freaks out on login node: SCRATCH_PATH=/cluster/scratch/$(id -un): "Build singularity image on job node. Freaks out on login node: SCRATCH_PATH=/cluster/scratch/$(id -un)"
- [methods] For usage with SLURM, sets up one GPU. Use with `sbatch --array=0-9`: "For usage with SLURM, sets up one GPU. Use with `sbatch --array=0-9`"
- [methods] singularity build $SCRATCH_PATH/MSNovelist-image/msnovelist.sif docker://stravsm/msnovelist6: "singularity build $SCRATCH_PATH/MSNovelist-image/msnovelist.sif docker://stravsm/msnovelist6"
- [other] The training workflow uses SLURM job-array submission with `sbatch --array=0-9` to launch 10 parallel jobs, each assigned a single GPU.: "The training workflow uses SLURM job-array submission with `sbatch --array=0-9` to launch 10 parallel jobs, each assigned a single GPU."
- [other] Set environment variables in run_train.sh pointing to DATA_LOC, SIF_LOC, CODE_LOC, and RESULTS_LOC directories configured in .env.: "Set environment variables in run_train.sh pointing to DATA_LOC, SIF_LOC, CODE_LOC, and RESULTS_LOC directories configured in .env."
- [other] Each job invokes train.sh inside the Singularity container, which runs train.py to train one cross-validation fold of the model: "Each job invokes train.sh inside the Singularity container, which runs train.py to train one cross-validation fold of the model"
