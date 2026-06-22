---
name: model-evaluation-metrics-interpretation
description: Use when you have retrained or modified a neural network model (e.g., MSNovelist) to accept a different input fingerprint representation (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3379
  - http://edamontology.org/topic_3314
  tools:
  - MSNovelist
  - Python
  - AWS CLI
  - train.py
  - evaluation.py
  - MSNovelist (Singularity container)
  - SLURM (sbatch)
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# model-evaluation-metrics-interpretation

## Summary

Interpret training and evaluation metrics from de novo structure prediction models to assess whether architectural changes (e.g., fingerprint input format substitution) have been successfully integrated without breaking model behavior. This skill involves inspecting log outputs and comparing metric distributions across cross-validation folds to confirm model convergence and input compatibility.

## When to use

You have retrained or modified a neural network model (e.g., MSNovelist) to accept a different input fingerprint representation (e.g., Morgan 4096-bit instead of SIRIUS 6 fingerprints), and you need to verify that the model learns meaningfully and does not crash due to shape mismatches or incompatible tensor dimensions during training and evaluation.

## When NOT to use

- Input fingerprint format has not been changed and you are simply running standard training; use this skill only when verifying that a new input modality (e.g., alternate fingerprint system) integrates without crashes.
- You are evaluating prediction accuracy on external test data for a production model; this skill is for debugging architectural changes, not for reporting final model performance.
- Metrics have already been statistically compared across multiple folds with significance testing; this skill covers single-fold inspection, not formal cross-validation analysis.

## Inputs

- training log file (text or structured format from train.py)
- evaluation metrics output (CSV or pickle from evaluation.py)
- baseline or reference metrics from prior training runs
- single cross-validation fold checkpoint (PyTorch model state)

## Outputs

- interpretation of metric trends (e.g., 'loss converged smoothly', 'no shape mismatches detected')
- pass/fail verdict on model compatibility with new fingerprint input
- identified anomalies (NaN, zero metrics, loss spikes) flagging input layer bugs

## How to apply

After running train.py on a single cross-validation fold with GPU support, inspect the training logs to confirm the model converged without shape mismatches or NaN losses. Then run evaluation.py on the same fold (without GPU) to compute held-out metrics. Compare the training loss trajectory and evaluation metrics (e.g., loss, accuracy, ranking metrics) against baseline runs or expected ranges to detect anomalies. If losses remain finite, decrease monotonically during training, and evaluation metrics are non-zero and in a plausible range, the fingerprint input layer likely accepted the new format correctly. If losses spike or become NaN, or evaluation produces zero values, investigate tensor shape mismatches in the input preprocessing layer.

## Related tools

- **train.py** (Executes single-fold training; emits loss and training metrics to logs) — https://github.com/meowcat/MSNovelist
- **evaluation.py** (Runs inference and computes held-out evaluation metrics on one fold without GPU) — https://github.com/meowcat/MSNovelist
- **MSNovelist (Singularity container)** (Containerized environment bundling PyTorch, SIRIUS 6, and MSNovelist training/eval scripts) — https://github.com/meowcat/MSNovelist
- **SLURM (sbatch)** (Job scheduler to allocate GPU/CPU resources for training and non-GPU evaluation runs)

## Examples

```
sbatch run_singularity.sh && sbatch run_evaluation.sh; tail -f training.log | grep -E '(loss|epoch|shape)' && cat evaluation_metrics.csv | head -20
```

## Evaluation signals

- Training loss remains finite (no NaN or Inf) throughout the epoch and decreases monotonically or plateaus, indicating stable backpropagation.
- No shape mismatch errors or tensor dimension warnings appear in training logs, confirming the modified fingerprint input layer accepted the new Morgan 4096-bit format.
- Evaluation metrics (e.g., ranking loss, accuracy) are non-zero and fall within a plausible range relative to prior baseline runs (not zero or catastrophically large).
- Evaluation step completes without crashes or out-of-memory errors, confirming forward pass inference is compatible with the new input representation.
- Cross-entropy or ranking loss on the validation fold is comparable to the training fold (within ~10–20% relative difference), suggesting no severe overfitting introduced by the architectural change.

## Limitations

- Single-fold evaluation may not reveal generalization failures; metrics should be aggregated across multiple folds and compared statistically for robust conclusions.
- Logs from train.py and evaluation.py must be captured and accessible; if stderr/stdout is not redirected or if the container environment suppresses logging, metric inspection becomes infeasible.
- This skill detects *whether* the new fingerprint format was accepted, but does not assess *whether* the model's predictions are chemically or biologically meaningful; external validation against known compounds or empirical structure data is required for that.
- Metric interpretation requires domain knowledge (e.g., what loss range is 'normal' for de novo structure prediction); comparison to baseline runs is strongly recommended to establish context.
- Changes to downstream loss functions, model architecture depth, or regularization simultaneously with fingerprint format changes may confound metric interpretation; isolate the fingerprint input change for clearest diagnosis.

## Evidence

- [other] Run training on a single cross-validation fold using sbatch with run_singularity.sh and run_train.sh, which invokes train.py to train one fold with GPU support.: "Run training on a single cross-validation fold using sbatch with run_singularity.sh and run_train.sh, which invokes train.py to train one fold with GPU support."
- [other] Run evaluation on the same fold using sbatch with run_evaluation.sh and evaluation.sh, which invokes evaluation.py to evaluate one fold without GPU.: "Run evaluation on the same fold using sbatch with run_evaluation.sh and evaluation.sh, which invokes evaluation.py to evaluate one fold without GPU."
- [other] Inspect training logs and evaluation metrics to confirm the model accepts Morgan fingerprint input without crashes or shape mismatches.: "Inspect training logs and evaluation metrics to confirm the model accepts Morgan fingerprint input without crashes or shape mismatches."
- [readme] The *mist* branch contains some work on getting MSNovelist to run with predicted Morgan 4096-bit fingerprints, but we didn't get terribly far with it yet.: "The *mist* branch contains some work on getting MSNovelist to run with predicted Morgan 4096-bit fingerprints, but we didn't get terribly far with it yet."
- [other] train.py: train one fold of the model: "train.py: train one fold of the model"
