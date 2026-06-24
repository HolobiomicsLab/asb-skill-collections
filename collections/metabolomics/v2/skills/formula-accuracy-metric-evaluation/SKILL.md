---
name: formula-accuracy-metric-evaluation
description: Use when when training or validating a deep learning model for molecular
  formula prediction from tandem MS/MS spectra, use this metric to track whether the
  model's predicted formula (including hydrogen atoms) exactly matches the annotated
  ground-truth formula.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3382
  tools:
  - msfiddle
  - FIDDLE
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1038/s41467-025-66060-9
  title: fiddle
evidence_spans:
- 'CLI and Python API: [msfiddle](https://github.com/josiehong/msfiddle)'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_fiddle
    doi: 10.1038/s41467-025-66060-9
    title: fiddle
  dedup_kept_from: coll_fiddle
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-025-66060-9
  all_source_dois:
  - 10.1038/s41467-025-66060-9
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# formula-accuracy-metric-evaluation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Evaluate molecular formula prediction models using formula_acc (with H) — a metric that measures the fraction of MS/MS spectra for which the predicted molecular formula exactly matches the ground-truth formula, including hydrogen count. This metric is central to monitoring rescore model training convergence and selecting best checkpoints in FIDDLE.

## When to use

When training or validating a deep learning model for molecular formula prediction from tandem MS/MS spectra, use this metric to track whether the model's predicted formula (including hydrogen atoms) exactly matches the annotated ground-truth formula. Apply it after each training epoch on a held-out validation set to identify overfitting and to decide when to save model checkpoints.

## When NOT to use

- Input does not include ground-truth molecular formulas — use alternative metrics like ranking-based recall or candidate-set accuracy instead.
- Evaluating models that do not output formula strings or hydrogen counts — use loss-based or embedding-space metrics.
- Datasets where hydrogen count is not relevant or not annotated — use formula_acc without hydrogen or a simplified atomic composition match.

## Inputs

- Validation dataset with MS/MS spectra (m/z, intensity pairs) and annotated ground-truth molecular formulas
- Trained FormulaEncoder and RescoreHead model outputs (predicted formula strings with hydrogen counts)
- Previous best validation formula_acc (with H) score for comparison

## Outputs

- formula_acc (with H) metric value (0–1 range, higher is better)
- Boolean decision: whether to save checkpoint (True if metric improved)
- Model checkpoint file (only if metric improved)
- Training log entry with epoch number, formula_acc (with H), and improvement flag

## How to apply

After each training epoch, run the trained FormulaEncoder and RescoreHead components on the validation dataset containing annotated MS/MS spectra with ground-truth molecular formulas. For each spectrum, compare the top-ranked predicted formula (output by the rescore head after binary cross-entropy loss training) to the ground-truth formula string, counting an exact match only if both the atomic composition and hydrogen count agree. Compute formula_acc (with H) as the fraction of spectra with exact matches. Save the model checkpoint only when this metric improves over the previous best validation score. Track this metric across all epochs to detect convergence and prevent overfitting.

## Related tools

- **msfiddle** (CLI and Python API for running FIDDLE inference and model evaluation on MS/MS data) — https://github.com/josiehong/msfiddle
- **FIDDLE** (Research codebase containing train_rescore.py and validation logic that computes formula_acc (with H) during training) — https://github.com/JosieHong/FIDDLE

## Evaluation signals

- formula_acc (with H) should be non-negative and ≤ 1.0 after each validation epoch.
- If formula_acc (with H) is 0 for multiple consecutive epochs, check that ground-truth annotations are present and that the model is receiving gradient updates.
- formula_acc (with H) should generally increase (or plateau) over training epochs; sharp drops may indicate overfitting or data leakage.
- Compare formula_acc (with H) to baseline or published results on the same dataset; the rescore model (v2.0.0 Siamese architecture) should exceed single-encoder baselines.
- Checkpoint save frequency should correlate with formula_acc (with H) improvements; if no checkpoints are saved after many epochs, the validation metric is not improving and training may need adjustment (learning rate, regularization, data).

## Limitations

- This metric requires exact string match of the formula including hydrogen count; near-misses (e.g., correct atoms but off-by-one hydrogen) are counted as failures and may mask models that are close to correct.
- formula_acc (with H) does not distinguish between different types of errors (e.g., wrong atom vs. wrong hydrogen count); use confusion matrices or per-element accuracy to diagnose failure modes.
- The metric assumes ground-truth formulas are correctly annotated; errors or ambiguities in the training set annotations will artificially depress or inflate the metric.
- The v2.0.0 Siamese architecture redesign may affect checkpoint compatibility; models trained on v1.x may not be directly comparable using this metric on v2.0.0 validation data.

## Evidence

- [other] monitoring formula_acc (with H) on validation set after each epoch: "Train FormulaEncoder and RescoreHead using binary cross-entropy loss, monitoring formula_acc (with H) on validation set after each epoch."
- [other] Save model checkpoint only when formula_acc (with H) improves: "Save model checkpoint only when formula_acc (with H) improves over previous best validation metric."
- [readme] The rescore model has been redesigned with a Siamese architecture in version 2.0.0: "The rescore model has been redesigned (Siamese architecture), see details in [CHANGELOG.md](./CHANGELOG.md)."
- [readme] FIDDLE is a deep learning method for predicting molecular formulas from MS/MS spectra: "FIDDLE is a deep learning method for predicting molecular formulas from MS/MS spectra."
