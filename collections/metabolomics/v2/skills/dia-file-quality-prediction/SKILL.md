---
name: dia-file-quality-prediction
description: Use when you have a batch of DIA mass spectrometry raw files (.raw, .d,
  or .wiff formats) from known instrument types (timsTOF, TripleTOF, or Orbitrap)
  and need to classify each file as pass/fail or assign a quality label.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - DIA-NN
  - msConvert
  - iDIA-QC
  techniques:
  - LC-MS
  - ion-mobility-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1038/s41467-024-54871-1
  title: iDIA-QC
evidence_spans:
- iDIA-QC is a Python Graphical User Interface (GUI)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_idia_qc_cq
    doi: 10.1038/s41467-024-54871-1
    title: iDIA-QC
  dedup_kept_from: coll_idia_qc_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-024-54871-1
  all_source_dois:
  - 10.1038/s41467-024-54871-1
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# dia-file-quality-prediction

## Summary

Train and apply machine learning models to predict mass spectrometry DIA file quality from 15 extracted metrics (e.g., MS1/MS2 signal intensity, precursor selectivity, fragment ion detection) characterizing raw files from timsTOF, TripleTOF, and Orbitrap instruments. This skill enables automated quality monitoring and early detection of instrument performance issues in high-throughput proteomics workflows.

## When to use

Apply this skill when you have a batch of DIA mass spectrometry raw files (.raw, .d, or .wiff formats) from known instrument types (timsTOF, TripleTOF, or Orbitrap) and need to classify each file as pass/fail or assign a quality label. Use it in longitudinal monitoring scenarios where you want to track instrument performance over time and flag degraded files before downstream analysis, or when establishing a quality control baseline for a new instrument or lab protocol.

## When NOT to use

- DIA files from instrument types not in the training set (timsTOF, TripleTOF, Orbitrap). Model may not generalize to novel instrument platforms.
- When raw 15 metrics have not yet been extracted. This skill assumes pre-computed metric features; it does not perform metric extraction from raw spectra.
- If you need to understand *which* individual metrics drive poor quality. This skill predicts an overall quality label but does not provide per-metric interpretability or diagnostic guidance for instrument troubleshooting.

## Inputs

- DIA mass spectrometry raw files in .raw, .d, or .wiff format
- 15 extracted quality metrics per DIA file (numeric feature matrix)
- Instrument type label for each file (timsTOF, TripleTOF, or Orbitrap)
- Training dataset with labeled quality annotations (if training new model)

## Outputs

- Quality class predictions per DIA file (e.g., pass/fail or quality score)
- Prediction confidence scores or probability estimates
- Longitudinal summary visualizations of DIA file quality over time
- HTML report with quality metrics and potential instrument issue flags
- Administrator notifications (email or WeChat) with prediction results

## How to apply

First, extract or load the 15 quality metrics from each DIA file (performed upstream via DIA-NN integration or external metric extraction). Prepare a feature matrix with these 15 metrics as columns and handle missing values or outliers according to the training dataset's data cleaning protocol. Partition labeled historical data into training and validation/test sets (e.g., 70/30 split). Train a machine learning classifier (e.g., random forest, gradient boosting, or SVM—algorithm and hyperparameters should be derived from the iDIA-QC paper's reported approach) on the training set using the 15 metrics as input features. Evaluate model performance on held-out test data using appropriate classification metrics (accuracy, precision, recall, F1-score, or ROC-AUC depending on class balance). Apply the trained model to new DIA files to generate quality predictions, then save results with file identifiers and predicted quality labels for longitudinal tracking and administrator notification.

## Related tools

- **DIA-NN** (Provides protein qualitative and quantitative algorithms; integrated into iDIA-QC for metric extraction and model training)
- **msConvert** (Converts DIA raw files to extracted precursor ion chromatogram (PIC) format for downstream processing)
- **iDIA-QC** (Reference Python GUI implementation that orchestrates DIA file quality prediction, metric extraction, and longitudinal visualization) — https://github.com/guomics-lab/iDIA-QC

## Evaluation signals

- Model achieves target classification metrics (e.g., ≥0.90 accuracy or ≥0.85 F1-score) on held-out test data from the training instrument types
- Predictions are consistent across multiple runs on the same input DIA file (deterministic predictions, allowing for stochastic model variance)
- Quality labels correctly identify known poor-quality files (e.g., files with known instrument artifacts or acquisition errors)
- Analysis time per file is under 5 minutes, consistent with the stated scalability target
- All 15 input metrics are non-null and within expected ranges for the corresponding instrument type; missing or out-of-range metrics trigger a warning or are imputed using a documented strategy

## Limitations

- Model is specific to three instrument types (timsTOF, TripleTOF, Orbitrap). Generalization to other instruments or significant hardware/software updates to these platforms is not validated.
- Quality prediction depends on the 15 extracted metrics; if metric extraction itself is biased or incomplete, downstream predictions will inherit that limitation.
- Longitudinal monitoring assumes consistent instrument maintenance and calibration protocols. Systematic instrument degradation or major recalibration events may require model retraining.
- The skill outputs a single quality label or score per file but does not provide granular per-metric diagnostics; users cannot easily identify which specific metrics caused a 'fail' prediction.

## Evidence

- [intro] Based on 15 metrics extracted from DIA files characterizing raw files from timsTOF, TripleTOF, and Orbitrap instruments: "Based on 15 metrics extracted from the DIA files, which describe the characteristics of the raw files from timsTOF serial instruments, TripleTOF instruments, and Orbitrap serial instruments, we"
- [other] ML model training and feature preparation workflow: "Load the 15 extracted DIA metrics and corresponding quality labels from the training dataset. Prepare feature matrix and target labels, handling any missing values or outliers. Partition data into"
- [readme] Longitudinal monitoring and notification outputs: "The outputs of iDIA-QC in a longitudinal summary, visually display the quality of the DIA files. Additionally, it promptly shares the prediction results and visualization with administrators via"
- [readme] Supported input file formats and instrument assignment: "This software supports the .raw, .d, and .wiff raw data formats. Choose the type of instrument that generated the file."
- [readme] Scalability and performance targets: "Analysis time per file is under 5 minutes."
