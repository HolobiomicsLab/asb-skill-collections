---
name: fingerprint-feature-format-conversion
description: Use when you have a pretrained deep learning model (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3359
  edam_topics:
  - http://edamontology.org/topic_3174
  - http://edamontology.org/topic_0154
  tools:
  - MSNovelist
  - Python
  - AWS CLI
  - Singularity
  - SLURM
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

# fingerprint-feature-format-conversion

## Summary

Adapt a trained molecular structure prediction model to accept fingerprints from an alternate prediction system by modifying the input layer to convert between fingerprint formats. This skill is necessary when transitioning from bundled fingerprint data (e.g., SIRIUS 6 fingerprints) to external predicted fingerprints (e.g., Morgan 4096-bit) without retraining the entire model.

## When to use

You have a pretrained deep learning model (e.g., MSNovelist) that expects fingerprints in one format (SIRIUS 6) but want to feed it predicted Morgan 4096-bit fingerprints from an alternate prediction system, and you need to verify that the model can accept the new format without shape mismatches or numerical instability during training and inference.

## When NOT to use

- Input fingerprints are already in the target model's native format (e.g., already SIRIUS 6 fingerprints for MSNovelist) — no conversion is needed.
- You need to retrain the entire model from scratch on new data rather than adapt an existing frozen or partially frozen model.
- The fingerprint dimensionality mismatch cannot be resolved by simple input layer modification (e.g., Morgan fingerprints are fundamentally incompatible with the downstream architecture).

## Inputs

- Pretrained model weights and architecture (e.g., MSNovelist repository on mist branch)
- Predicted Morgan 4096-bit fingerprints (numeric matrix or feature file)
- Configuration file (.env) specifying data, code, and Singularity image paths
- Cross-validation fold indices or data split definition
- Training dataset with labels (e.g., molecular structures paired with spectra)

## Outputs

- Modified model input layer accepting Morgan 4096-bit fingerprints
- Training logs confirming successful epoch iterations without shape errors
- Evaluation metrics (e.g., loss, accuracy) on the validation fold
- Model checkpoint/weights from the single-fold training run

## How to apply

Checkout the model repository and switch to a development branch containing fingerprint adapter code (e.g., mist branch in MSNovelist). Modify the fingerprint input layer to accept the target format (Morgan 4096-bit) in place of the original format, ensuring tensor shape compatibility. Configure environment variables (.env file) to point to the data location, model container path, code location, and results directory. Build the model container (Singularity image) on a compute node, then run training on a single cross-validation fold using the sbatch/SLURM scheduler with GPU support to validate that the model accepts the new fingerprint input without crashes. Run evaluation on the same fold without GPU and inspect training logs and evaluation metrics to confirm shape consistency and numerical stability.

## Related tools

- **MSNovelist** (Target model whose input layer is adapted to accept alternate fingerprint formats) — https://github.com/meowcat/MSNovelist
- **Singularity** (Container system for building and running the adapted model on HPC infrastructure)
- **SLURM** (Job scheduler for submitting training and evaluation tasks to GPU-enabled compute nodes)
- **Python** (Language for train.py and evaluation.py scripts that orchestrate training and validation of the converted fingerprint input layer)

## Examples

```
sbatch run_singularity.sh
```

## Evaluation signals

- Training completes at least one epoch without tensor shape mismatch errors or dimension misalignment exceptions
- Model checkpoint file is created and contains trained weights with no NaN or Inf values
- Evaluation metrics (loss, accuracy) are computed and logged for the validation fold without numerical instability or divergence
- Input fingerprint tensor shape matches the expected 4096-bit dimensionality throughout the forward pass
- Training and evaluation logs show consistent batch processing without crashes or out-of-memory errors when using Morgan fingerprints

## Limitations

- Preliminary work on the mist branch remained incomplete; full production readiness of Morgan fingerprint adaptation in MSNovelist is not guaranteed.
- Conversion requires modifying only the input layer — if downstream layers have architecture assumptions tied to the original fingerprint format, deeper model surgery may be necessary.
- Single-fold validation is necessary but insufficient for full model assessment; production deployment requires evaluation across all cross-validation folds and on held-out test sets.
- Morgan 4096-bit fingerprints may encode different chemical information than SIRIUS 6 fingerprints, potentially degrading downstream prediction quality even if the format conversion succeeds technically.

## Evidence

- [other] research_question: "Can MSNovelist be adapted to accept predicted Morgan 4096-bit fingerprints as input instead of relying on bundled SIRIUS 6 fingerprint data?"
- [other] workflow_incomplete: "Preliminary work on the mist branch attempted to enable MSNovelist to run with predicted Morgan 4096-bit fingerprints, but the effort remained incomplete."
- [other] input_layer_modification: "Switch to the mist branch and modify the fingerprint input layer to accept Morgan 4096-bit fingerprints in place of SIRIUS 6 fingerprint format."
- [other] training_validation: "Run training on a single cross-validation fold using sbatch with run_singularity.sh and run_train.sh, which invokes train.py to train one fold with GPU support."
- [other] evaluation_logs: "Inspect training logs and evaluation metrics to confirm the model accepts Morgan fingerprint input without crashes or shape mismatches."
- [readme] readme_mist_branch: "The *mist* branch (also merged here) contains some work on getting MSNovelist to run with predicted Morgan 4096-bit fingerprints, but we didn't get terribly far with it yet."
