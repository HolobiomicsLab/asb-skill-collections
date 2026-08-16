---
name: deep-learning-model-weight-persistence
description: Use when you are training a deep learning model using k-fold cross-validation
  on an HPC cluster with SLURM job arrays, where each fold runs as a separate independent
  job with its own GPU allocation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3474
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - MSNovelist
  - SLURM
  - Singularity
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

# deep-learning-model-weight-persistence

## Summary

Persist trained deep learning model weights across SLURM job-array folds to enable distributed cross-validation training where each GPU-bound array job trains one fold independently and saves checkpoints to shared storage. This skill is essential for orchestrating multi-fold model training workflows on HPC clusters where individual array jobs may time out or fail, requiring checkpointed model state to be recovered and aggregated.

## When to use

You are training a deep learning model using k-fold cross-validation on an HPC cluster with SLURM job arrays, where each fold runs as a separate independent job with its own GPU allocation. You need to ensure that partial training progress is not lost if individual jobs timeout, fail, or are preempted, and that trained fold weights can be collected and ensemble'd after all array jobs complete.

## When NOT to use

- The model training fits within a single GPU allocation and does not require cross-validation partitioning — use single-job training instead.
- Model weights must be synchronized or averaged in real-time during training (e.g., federated averaging) — this skill assumes independent fold training.
- The RESULTS_LOC directory is not on shared/networked storage accessible to all compute nodes — fold checkpoints cannot be reliably persisted or retrieved.

## Inputs

- MSNovelist source code repository (GitHub checkout on login node)
- Training dataset (SIRIUS 6 dataset, downloaded via AWS S3 to DATA_LOC)
- Environment configuration file (.env with DATA_LOC, SIF_LOC, CODE_LOC, RESULTS_LOC paths)
- SLURM batch script (run_singularity.sh) with --array=0-9 specification
- Singularity container image (msnovelist.sif built from stravsm/msnovelist6 Docker registry)

## Outputs

- Per-fold model checkpoint files (e.g., fold_0_weights.pt through fold_9_weights.pt) written to RESULTS_LOC on shared scratch storage
- Training logs or metrics per fold (optional, for convergence diagnostics)
- Aggregated or ensemble model weights (post-processing step after all folds complete)

## How to apply

Configure the training script (train.py) running inside the Singularity container to save model checkpoint files to a shared results directory (RESULTS_LOC) after each epoch or training milestone. Each SLURM array job is assigned a unique fold index (via the $SLURM_ARRAY_TASK_ID environment variable passed through run_train.sh and run_singularity.sh), and train.py uses this index to name the output checkpoint file uniquely (e.g., fold_0_weights.pt, fold_1_weights.pt). After all 10 array jobs complete, aggregate or evaluate the fold-specific weights. This approach avoids model synchronization between jobs and ensures fault tolerance: if one fold's job fails partway through, only that fold's training must be restarted, not the entire cross-validation.

## Related tools

- **SLURM** (Job scheduler and array controller; distributes each cross-validation fold as a separate array job with unique $SLURM_ARRAY_TASK_ID, enabling parallel independent fold training)
- **Singularity** (Container runtime; encapsulates the training environment and ensures that train.py and all dependencies run identically across all compute nodes)
- **Python** (Language for train.py script; implements the core model training loop and checkpoint saving logic using fold-specific naming)
- **MSNovelist** (The deep learning model being trained; train.py is the entry point that loads, trains, and saves model weights for one fold) — https://github.com/meowcat/MSNovelist

## Examples

```
sbatch --array=0-9 run_singularity.sh
```

## Evaluation signals

- Verify that each SLURM array job successfully wrote a unique fold-specific checkpoint file to RESULTS_LOC (e.g., ls -la $RESULTS_LOC/fold_*.pt shows 10 files, one per job).
- Check the SLURM job log for each array element to confirm that train.py ran to completion and reported checkpoint save operations without errors.
- Confirm that checkpoint file sizes are consistent with model complexity and that file modification times span the training duration (indicating progressive checkpointing, not single writes).
- Load and inspect fold-specific weights in post-processing to verify they are distinct (not copies) and encode different model states trained on different training subsets.
- If a single fold job is manually restarted, verify that its output checkpoint overwrites the previous version and reflects retraining from scratch or from a previously saved intermediate state.

## Limitations

- Requires that RESULTS_LOC be on shared/networked storage (e.g., /cluster/scratch) accessible and writable from all compute nodes; local node storage cannot be used for persistent checkpoints.
- SLURM job array failures are not automatically retried; if an individual array job fails, the user must manually resubmit or use external job control tools (e.g., Nextflow, Snakemake) for retry logic.
- No built-in mechanism to resume training from a checkpoint within a single fold if a job times out mid-epoch; the entire fold must be restarted unless train.py explicitly implements mid-epoch resumption.
- Docker image build (stravsm/msnovelist6 registry) must be converted to Singularity on the compute node (not login node, per the README warning), which adds build time overhead but cannot be parallelized across array jobs.

## Evidence

- [methods] SLURM job array enables parallel fold training: "Submit the job array to SLURM using sbatch --array=0-9 run_singularity.sh, launching ten parallel training jobs."
- [methods] Each array job assigned a unique fold via environment variable: "each array index runs train.py to train one fold of the cross-validation model"
- [methods] Results directory configuration for checkpoint persistence: "Set environment variables in run_train.sh pointing to DATA_LOC, SIF_LOC, CODE_LOC, and RESULTS_LOC directories configured in .env."
- [methods] Singularity container ensures consistent environment across nodes: "Build singularity image on job node. Freaks out on login node: SCRATCH_PATH=/cluster/scratch/$(id -un)"
- [methods] train.py is the model training entry point: "train.py: train one fold of the model"
