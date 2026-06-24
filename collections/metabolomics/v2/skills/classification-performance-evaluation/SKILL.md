---
name: classification-performance-evaluation
description: Use when after running inference on test mass spectrometry spectra with
  a trained deep learning model (e.g., PS2MS) to verify that class label predictions
  and confidence scores match expected reference outputs.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - PS2MS
  - scikit-learn metrics module
  techniques:
  - mass-spectrometry
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.3c05019
  title: ps2ms
evidence_spans:
- jhhung/PS2MS
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_idia_qc_cq
    doi: 10.1038/s41467-024-54871-1
    title: iDIA-QC
  - build: coll_ps2ms_cq
    doi: 10.1021/acs.analchem.3c05019
    title: ps2ms
  dedup_kept_from: coll_ps2ms_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.3c05019
  all_source_dois:
  - 10.1021/acs.analchem.3c05019
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# classification-performance-evaluation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Quantitatively assess the predictive accuracy of a classification model by computing standard metrics (accuracy, precision, recall, F1-score) on held-out test data and comparing predictions against reference outputs. This skill validates that a trained classifier generalizes correctly to unseen examples.

## When to use

Apply this skill after running inference on test mass spectrometry spectra with a trained deep learning model (e.g., PS2MS) to verify that class label predictions and confidence scores match expected reference outputs. Use it when you have both model predictions and ground-truth labels for a test set and need quantitative evidence that the model was correctly implemented and performs within acceptable tolerances.

## When NOT to use

- Input data has not been normalized or formatted to match model requirements; validation will fail or be misleading.
- Ground-truth labels are unavailable or unreliable; metrics cannot be computed or will be meaningless.
- The model has not yet been trained or the pre-trained weights have not been loaded; inference will fail.

## Inputs

- Test mass spectrometry spectral data (in model-expected format: normalized spectra with structure as specified in repository)
- Ground-truth class labels for test examples (novel psychoactive substance identities)
- Model predictions on test data (class labels and confidence scores from inference)
- Reference outputs (published or repository-provided predictions and/or metrics for comparison)

## Outputs

- Classification metrics: accuracy, precision, recall, F1-score (per class and macro/micro averages)
- Confusion matrix or per-class breakdown of true positives, false positives, true negatives, false negatives
- Comparison report showing predicted labels vs. reference labels with alignment status
- Validation summary indicating whether predictions match expected outputs within tolerance

## How to apply

First, prepare test mass spectrometry spectral data in the format expected by the model (structure and normalization as specified in the repository). Run inference on the test spectra using the trained classifier to generate class predictions and confidence scores. Collect predictions and align them with ground-truth reference labels from the paper or repository. Compute classification metrics—accuracy (fraction of correct predictions), precision (true positives / predicted positives), recall (true positives / actual positives), and F1-score (harmonic mean of precision and recall)—for each novel psychoactive substance class. Compare computed metrics against expected outputs reported in the publication; small numerical differences due to floating-point rounding are acceptable, but predictions should match reference outputs within a pre-defined tolerance (e.g., ≤ 1–2% absolute difference for metrics).

## Related tools

- **PS2MS** (Deep learning classifier that generates predictions (class labels and confidence scores) on test mass spectrometry spectra for novel psychoactive substance identification) — https://github.com/jhhung/PS2MS
- **scikit-learn metrics module** (Computes classification metrics (accuracy, precision, recall, F1-score, confusion matrix) from predicted and ground-truth labels)

## Evaluation signals

- Computed accuracy, precision, recall, and F1-score values fall within the range reported in the paper (or within ≤ 1–2% absolute difference if reproducing a published result).
- Confusion matrix diagonal values (true positives per class) are non-zero for all represented NPS classes; off-diagonal values are minimized.
- Per-class metrics are balanced across novel psychoactive substance categories; no single class shows substantially higher or lower performance without justification.
- Model predictions on test spectra can be mapped 1:1 to reference labels; no misalignment or shape mismatch between predicted and ground-truth arrays.
- Computed metrics are reproducible across independent runs with the same test data, model weights, and random seed.

## Limitations

- Metrics are meaningful only if test data is representative of the distribution of novel psychoactive substances the model will encounter in practice; class imbalance or distribution shift can inflate reported performance.
- Classification metrics do not capture model uncertainty or the confidence/calibration of predictions; high accuracy can coexist with poorly calibrated confidence scores.
- Comparison to reference outputs is sensitive to numerical precision, floating-point rounding, and differences in metric computation implementations across tools.

## Evidence

- [other] Run inference on the test spectra using the PS2MS model to generate NPS class predictions. Collect predictions (class labels and confidence scores) and compare against the reference outputs reported in the paper or repository.: "Run inference on the test spectra using the PS2MS model to generate NPS class predictions. Collect predictions (class labels and confidence scores) and compare against the reference outputs reported"
- [other] Compute classification metrics (accuracy, precision, recall, F1-score) and validate that predictions match expected outputs within tolerance.: "Compute classification metrics (accuracy, precision, recall, F1-score) and validate that predictions match expected outputs within tolerance."
- [readme] PS<sup>2</sup>MS builds a synthetic NPS database by enumerating possible derivatives based on the core structure of a preselected illicit drug. The system leverages two deep learning tools, NEIMS and DeepEI, to generate mass spectra and chemical fingerprints, respectively.: "The system leverages two deep learning tools, NEIMS and DeepEI, to generate mass spectra and chemical fingerprints, respectively."
- [readme] The final step of PS<sup>2</sup>MS is to compare the analyte and the synthetic database. The system will compare the spectrum and chemical fingerprint between compounds and generate a list of the hundred most similar compounds which are ranked by similarity score.: "The system will compare the spectrum and chemical fingerprint between compounds and generate a list of the hundred most similar compounds which are ranked by similarity score."
