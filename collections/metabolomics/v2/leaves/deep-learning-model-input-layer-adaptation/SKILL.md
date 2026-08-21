---
name: deep-learning-model-input-layer-adaptation
description: Use when you have a trained deep-learning model (e.g., MSNovelist) that
  depends on a specific fingerprint format (e.g., SIRIUS 6 fingerprints) as input,
  but you want to substitute an alternative fingerprint prediction system (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3474
  - http://edamontology.org/topic_0091
  tools:
  - MSNovelist
  - Python
  - AWS CLI
  - Singularity
  - SLURM
  - SIRIUS 6
  license_tier: open
  provenance_tier: literature
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

# deep-learning-model-input-layer-adaptation

## Summary

Modify a trained deep-learning model's input layer to accept alternative feature representations (e.g., Morgan fingerprints instead of SIRIUS-derived fingerprints) without retraining the full architecture. This skill enables reuse of model weights and downstream layers when upstream fingerprint sources change.

## When to use

You have a trained deep-learning model (e.g., MSNovelist) that depends on a specific fingerprint format (e.g., SIRIUS 6 fingerprints) as input, but you want to substitute an alternative fingerprint prediction system (e.g., Morgan 4096-bit fingerprints) while preserving the trained model backbone. This is useful when the original fingerprint backend becomes unavailable, licensing constraints apply, or you want to benchmark model robustness across different feature sources.

## When NOT to use

- The original fingerprint input layer dimension is unknown or cannot be inspected from the model checkpoint—adaptation requires explicit shape matching.
- You need to preserve exact reproducibility of the original model's predictions on SIRIUS fingerprints; input layer modification will alter downstream behavior.
- The alternative fingerprint source (Morgan) has fundamentally different semantic meaning or coverage than SIRIUS fingerprints (e.g., missing molecular substructures critical to the model's decision boundary)—the adapted model may lose predictive power.

## Inputs

- Trained MSNovelist model checkpoint with SIRIUS 6 fingerprint input layer
- Morgan 4096-bit fingerprints (predicted from alternate system)
- Training dataset (cross-validation fold) with Morgan fingerprints and ground-truth molecular structures
- Validation dataset for the same fold

## Outputs

- Adapted MSNovelist model with Morgan 4096-bit fingerprint input layer
- Training logs (GPU-based) with loss curves and validation metrics
- Evaluation metrics (e.g., structure prediction accuracy, ranking scores) for the adapted fold
- Model checkpoint(s) with updated input layer weights

## How to apply

First, identify the input layer tensor shape and feature specification in the trained model (e.g., SIRIUS fingerprint dimensionality). Then modify the input layer to accept the new fingerprint format—for Morgan 4096-bit fingerprints, ensure the input tensor shape matches 4096 dimensions. Retrain or fine-tune only the adapted input layer and immediately downstream layers on held-out validation folds while freezing the deeper model weights, using the same training framework (e.g., train.py with GPU support). Validate by running training and evaluation on a single cross-validation fold first to detect shape mismatches or numerical instabilities in the logs before scaling to the full model. Monitor for convergence issues and compare evaluation metrics (e.g., structure prediction accuracy) against baseline performance on original fingerprint inputs.

## Related tools

- **MSNovelist** (Deep-learning model for de novo structure generation; source of input layer to be adapted) — https://github.com/meowcat/MSNovelist
- **Singularity** (Container runtime for reproducible model training and evaluation; must be built on job node, not login node)
- **Python** (Host language for train.py and evaluation.py scripts that execute the adaptation workflow)
- **SLURM** (Job scheduler for submitting training (GPU) and evaluation (CPU) tasks via sbatch)
- **SIRIUS 6** (Original fingerprint source; architecture and dimensionality serve as reference for input layer design) — https://bio.informatik.uni-jena.de/software/sirius/

## Examples

```
sbatch run_singularity.sh  # Invokes run_train.sh → train.sh → train.py to train one adapted fold with Morgan fingerprints on GPU
```

## Evaluation signals

- Training logs show no tensor shape mismatch errors; loss decreases over epochs without NaN or Inf values.
- Evaluation metrics (structure prediction accuracy, cosine similarity scores) on the adapted fold are within ≤10% of baseline performance on SIRIUS fingerprints, indicating the model has successfully learned the new input representation.
- No crashes or out-of-memory errors during both training (GPU) and evaluation (CPU) phases; Singularity container runs to completion.
- Cross-validation fold evaluation.py completes without assertion failures on fingerprint input dimensions (4096-bit matched to model's expected input shape).
- Output CSV (e.g., `decode-RUNID.csv`) contains valid structure predictions with score_mod_platt and rank_score_lim_mod_platt columns populated for all input spectra.

## Limitations

- The *mist* branch work on Morgan 4096-bit fingerprint adaptation in MSNovelist remains incomplete; substantial engineering effort may be required to fully integrate the alternative fingerprint layer.
- SIRIUS 6 backend is now the recommended deployment path; retraining MSNovelist with non-SIRIUS fingerprints diverges from the supported production pipeline and may suffer from stale dependencies or unsupported PyTorch/TensorFlow versions.
- Input layer adaptation assumes downstream model architecture and learned weights remain compatible with the new fingerprint feature space; if Morgan fingerprints encode orthogonal chemical patterns, the model may require deeper retraining to recover predictive power.
- Preliminary work suggests the adaptation is feasible but not yet validated at scale; full multi-fold cross-validation and external test set evaluation are needed to confirm generalization.

## Evidence

- [other] Preliminary work on the mist branch attempted to enable MSNovelist to run with predicted Morgan 4096-bit fingerprints, but the effort remained incomplete.: "Preliminary work on the mist branch attempted to enable MSNovelist to run with predicted Morgan 4096-bit fingerprints, but the effort remained incomplete."
- [other] Switch to the mist branch and modify the fingerprint input layer to accept Morgan 4096-bit fingerprints in place of SIRIUS 6 fingerprint format.: "Switch to the mist branch and modify the fingerprint input layer to accept Morgan 4096-bit fingerprints in place of SIRIUS 6 fingerprint format."
- [other] Run training on a single cross-validation fold using sbatch with run_singularity.sh and run_train.sh, which invokes train.py to train one fold with GPU support.: "Run training on a single cross-validation fold using sbatch with run_singularity.sh and run_train.sh, which invokes train.py to train one fold with GPU support."
- [other] Inspect training logs and evaluation metrics to confirm the model accepts Morgan fingerprint input without crashes or shape mismatches.: "Inspect training logs and evaluation metrics to confirm the model accepts Morgan fingerprint input without crashes or shape mismatches."
- [readme] The *mist* branch (also merged here) contains some work on getting MSNovelist to run with predicted Morgan 4096-bit fingerprints, but we didn't get terribly far with it yet.: "The *mist* branch (also merged here) contains some work on getting MSNovelist to run with predicted Morgan 4096-bit fingerprints, but we didn't get terribly far with it yet."
