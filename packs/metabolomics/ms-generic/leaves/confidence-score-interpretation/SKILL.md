---
name: confidence-score-interpretation
description: Use when after executing forward inference on preprocessed mass spectrometry spectra with a deep learning model (e.g., PS²MS), when you have per-spectrum predictions with associated confidence scores or per-class probabilities.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0769
  tools:
  - PS2MS
  - PS²MS
  - NEIMS
  - DeepEI
  techniques:
  - mass-spectrometry
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
  - build: coll_ps2ms
    doi: 10.1021/acs.analchem.3c05019
    title: ps2ms
  dedup_kept_from: coll_ps2ms
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

# confidence-score-interpretation

## Summary

Interpret and apply confidence thresholds to deep learning model predictions for NPS classification from mass spectrometry data. This skill filters predictions by model confidence to assign reliable NPS class labels and exclude low-confidence matches.

## When to use

After executing forward inference on preprocessed mass spectrometry spectra with a deep learning model (e.g., PS²MS), when you have per-spectrum predictions with associated confidence scores or per-class probabilities. Use this skill to convert raw model outputs into actionable NPS identifications by filtering out predictions below a minimum confidence threshold.

## When NOT to use

- Input is already a curated NPS reference library or training set—confidence filtering applies to novel unknowns, not ground-truth labels.
- Model has not been trained or validated on your specific mass spectrometry instrument, ionization method, or drug class—apply model validation and calibration before confidence thresholding.
- Threshold parameters have not been established via receiver operating characteristic (ROC) analysis or precision-recall trade-off study on a held-out validation set.

## Inputs

- Raw model predictions with confidence scores (from forward inference pass)
- Per-class probability vectors or logit outputs
- Spectrum identifiers or metadata
- Confidence threshold parameter (user-defined or derived from validation set)

## Outputs

- Structured prediction table with spectrum identifiers, predicted NPS classes, and per-class probabilities
- Filtered prediction set (high-confidence predictions only)
- Confidence score distribution or summary statistics
- Unclassified or ambiguous spectrum set (confidence below threshold)

## How to apply

Retrieve the confidence scores or probability vectors output by the deep learning inference step for each spectrum. Define a confidence threshold appropriate to your analytical tolerance—in NPS detection workflows, this typically balances sensitivity (detecting true novel drugs) against false-positive rate. For each spectrum, retain only the predicted NPS class(es) whose confidence score exceeds the threshold. Discard predictions below the threshold and mark them as unclassified or ambiguous. Post-process the filtered predictions to produce a final prediction table that maps each spectrum identifier to its assigned NPS class label, per-class probabilities, and confidence metrics. This filtering reduces false identifications in forensic or regulatory screening contexts where incorrect NPS assignment carries high cost.

## Related tools

- **PS²MS** (Deep learning model that outputs NPS classification predictions and confidence scores from preprocessed mass spectrometry spectra) — https://github.com/jhhung/PS2MS
- **NEIMS** (Generates predicted mass spectra for synthetic NPS database compounds; integrated into PS²MS similarity scoring)
- **DeepEI** (Predicts chemical fingerprints of unknown analytes and database compounds; used in integrated similarity score (SMSF) calculation for ranking NPS candidates)

## Evaluation signals

- Confidence scores are within valid range (0–1 or 0–100% depending on model output format) with no null or inf values for any prediction.
- Number of high-confidence predictions (above threshold) is reasonable relative to total spectra—extreme retention (>95%) or rejection (<5%) suggests threshold miscalibration.
- Prediction table schema includes spectrum identifiers, assigned NPS class labels, and per-class probabilities; no missing values in required columns.
- Confidence threshold is documented and justified (e.g., derived from validation set ROC analysis, precision-recall curve, or prior domain knowledge of acceptable false-positive rate).
- Ambiguous predictions (below threshold) are segregated and tracked; total predictions (high-confidence + ambiguous) equals input spectra count.

## Limitations

- Confidence scores reflect model calibration on training data; if test spectra or NPS classes differ significantly from training distribution, confidence may not be reliable without recalibration.
- The choice of confidence threshold is problem-dependent and must be validated empirically; no universal threshold is recommended across all NPS detection scenarios.
- Per-class probabilities may be skewed if the synthetic NPS database is incomplete or biased toward certain drug cores or functional group substitutions.
- Low confidence does not imply the unknown is not an NPS—it may indicate a truly novel compound not well-represented in the training or synthetic database.

## Evidence

- [other] Execute forward inference pass on preprocessed spectra to generate NPS classification predictions and confidence scores.: "Execute forward inference pass on preprocessed spectra to generate NPS classification predictions and confidence scores."
- [other] Post-process predictions to assign NPS class labels and filter by model confidence threshold.: "Post-process predictions to assign NPS class labels and filter by model confidence threshold."
- [other] Export results as a structured prediction table with spectrum identifiers, predicted NPS classes, and per-class probabilities.: "Export results as a structured prediction table with spectrum identifiers, predicted NPS classes, and per-class probabilities."
- [readme] PS²MS calculates the integrated similarity scores(SMSF) between the unknown analyte and the derivatives from synthetic database and yields a list of potential NPS identities for the analyte.: "PS²MS calculates the integrated similarity scores(SMSF) between the unknown analyte and the derivatives from synthetic database and yields a list of potential NPS identities for the analyte."
