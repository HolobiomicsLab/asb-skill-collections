---
name: machine-learning-pipeline-integration-testing
description: Use when you have adapted an ML pipeline (e.g., MSNovelist) to consume a non-standard fingerprint representation (Morgan 4096-bit instead of bundled SIRIUS 6 fingerprints) and need to verify that the model's input layer correctly reshapes and processes the new fingerprint format before committing.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3474
  tools:
  - MSNovelist
  - Python
  - AWS CLI
  - Singularity
  - SLURM
  - Python (train.py, evaluation.py)
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
---

# machine-learning-pipeline-integration-testing

## Summary

Validate that a retrained machine-learning model accepts modified input fingerprint formats (e.g., Morgan 4096-bit fingerprints in place of SIRIUS 6 fingerprints) without crashes or tensor shape mismatches, by executing a single cross-validation fold through training and evaluation in a containerized environment.

## When to use

You have adapted an ML pipeline (e.g., MSNovelist) to consume a non-standard fingerprint representation (Morgan 4096-bit instead of bundled SIRIUS 6 fingerprints) and need to verify that the model's input layer correctly reshapes and processes the new fingerprint format before committing to full retraining across all folds.

## When NOT to use

- Input fingerprints are already validated to work with the model (use full multi-fold training instead)
- No GPU or SLURM infrastructure is available (this workflow requires sbatch and containerization)
- You are debugging containerization errors unrelated to fingerprint format (e.g., Docker/Singularity build failures)

## Inputs

- MSNovelist repository (mist branch or equivalent)
- Morgan 4096-bit fingerprints in numeric or binary format
- Training dataset (single cross-validation fold)
- Singularity container definition or pre-built SIF image
- .env configuration file with paths to data, code, and output

## Outputs

- Training logs from train.py (per-epoch loss, convergence metrics)
- Evaluation metrics from evaluation.py (e.g., accuracy, ranking metrics)
- Model checkpoint for the tested fold
- Decoded predictions CSV or pickle file

## How to apply

Checkout the target repository (e.g., mist branch of MSNovelist) on a login node and modify the fingerprint input layer to accept the alternate format. Configure environment variables (.env) pointing to data location, Singularity image path, code location, and results output directory. Build the Singularity container on a job node (to avoid login-node resource constraints). Submit a single cross-validation fold to SLURM using sbatch, invoking train.py with GPU support to train that fold, then run evaluation.py on the same fold without GPU. Inspect training logs and evaluation metrics for shape mismatches, NaN losses, or early crashes that indicate the fingerprint adapter is not functioning correctly.

## Related tools

- **MSNovelist** (ML pipeline being adapted to accept alternate fingerprint input format) — https://github.com/meowcat/MSNovelist
- **Singularity** (Container runtime for reproducible model training and evaluation on job nodes)
- **SLURM** (Job scheduler for GPU-accelerated training and CPU-based evaluation submission)
- **Python (train.py, evaluation.py)** (Training and evaluation scripts invoked inside the Singularity container) — https://github.com/meowcat/MSNovelist

## Examples

```
sbatch run_singularity.sh
```

## Evaluation signals

- Training log shows no tensor shape mismatch errors (e.g., 'expected size X, got size Y') when processing Morgan 4096-bit fingerprints
- Loss values remain finite (no NaN or Inf) throughout training epoch; loss curve exhibits expected downward trend
- Evaluation script completes without crashing and produces output metrics (e.g., ranking scores, accuracy)
- Model checkpoint is successfully saved and contains parameters with expected tensor shapes matching the modified input layer
- Decoded predictions CSV/pickle file is non-empty and contains valid predictions for the test fold

## Limitations

- This skill validates only a single cross-validation fold and does not guarantee performance across the full training set or generalization to held-out test data.
- The mist branch implementation remains incomplete according to the README; fingerprint adapter logic may require manual debugging or extension.
- Integration testing on one fold may not surface problems that emerge only during distributed training across multiple folds (e.g., data loading bottlenecks, stochastic initialization issues).
- Container build can take up to 20 minutes and requires ~6.5 GB of disk space; iterative debugging may be slow.

## Evidence

- [other] Preliminary work on the mist branch attempted to enable MSNovelist to run with predicted Morgan 4096-bit fingerprints, but the effort remained incomplete.: "The *mist* branch (also merged here) contains some work on getting MSNovelist to run with predicted Morgan 4096-bit fingerprints, but we didn't get terribly far with it yet."
- [other] Switch to the mist branch and modify the fingerprint input layer to accept Morgan 4096-bit fingerprints in place of SIRIUS 6 fingerprint format.: "modify the fingerprint input layer to accept Morgan 4096-bit fingerprints in place of SIRIUS 6 fingerprint format"
- [other] Build the MSNovelist Singularity image on a job node and store at SIF_LOC; run training on a single cross-validation fold using sbatch with GPU support.: "Build the MSNovelist Singularity image (stravsm/msnovelist6) on a job node and store at SIF_LOC. Run training on a single cross-validation fold using sbatch with run_singularity.sh and run_train.sh,"
- [other] Inspect training logs and evaluation metrics to confirm the model accepts Morgan fingerprint input without crashes or shape mismatches.: "Inspect training logs and evaluation metrics to confirm the model accepts Morgan fingerprint input without crashes or shape mismatches."
- [methods] Build singularity image on job node. Freaks out on login node.: "Build singularity image on job node. Freaks out on login node: SCRATCH_PATH=/cluster/scratch/$(id -un)"
