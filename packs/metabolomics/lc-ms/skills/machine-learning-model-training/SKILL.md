---
name: machine-learning-model-training
description: Use when you have a labeled dataset of DIA raw files (.raw, .d, .wiff) with known quality annotations and have extracted the 15 iDIA-QC metrics (raw file characteristics from timsTOF, TripleTOF, or Orbitrap instruments).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3673
  tools:
  - Python
  - DIA-NN
  - msConvert
  - Python (scikit-learn, pandas, numpy)
  techniques:
  - LC-MS
  - ion-mobility-MS
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

# machine-learning-model-training

## Summary

Train a supervised machine learning classifier to predict DIA file quality from 15 extracted mass spectrometry metrics (e.g., precursor intensity, MS/MS count, dynamic range) across timsTOF, TripleTOF, and Orbitrap instruments. This skill produces a deployable quality-prediction model that enables automated monitoring and flagging of instrument performance issues.

## When to use

You have a labeled dataset of DIA raw files (.raw, .d, .wiff) with known quality annotations and have extracted the 15 iDIA-QC metrics (raw file characteristics from timsTOF, TripleTOF, or Orbitrap instruments). Apply this skill when you need to build a generalizable predictor to automatically classify new incoming DIA files as pass/fail or quality-tier without manual inspection.

## When NOT to use

- The input DIA files have not yet been processed through metric extraction (15 metrics are not yet computed); extract metrics first using the iDIA-QC workflow.
- Quality labels are missing or highly imbalanced (<<5% minority class) without rebalancing strategies; model training requires sufficient labeled examples.
- New DIA files originate from instrument types (e.g., newer Bruker timsTOF models) not represented in the training data; retraining or domain adaptation may be needed.

## Inputs

- Feature matrix: 15 extracted DIA metrics per file (timsTOF, TripleTOF, or Orbitrap origin)
- Target vector: quality labels for training files (binary or multiclass)
- Training dataset: labeled DIA files (.raw, .d, .wiff formats or pre-extracted metric tables)

## Outputs

- Trained machine learning model (serialized, e.g., pickle/joblib in Python)
- Quality predictions for new DIA files (file ID, predicted label, confidence scores)
- Model performance report (accuracy, precision, recall, F1, ROC-AUC on validation/test set)
- Longitudinal quality summary and visualizations for administrator notification

## How to apply

Load the 15 extracted DIA metrics and corresponding quality labels from your training dataset. Prepare a feature matrix (rows = files, columns = 15 metrics) and target vector (quality labels); handle missing values and outliers (e.g., log-scaling or winsorization of extreme metric values). Partition data into training (e.g., 70–80%) and validation/test sets using stratified splitting to preserve class balance. Train a supervised classifier (algorithm and hyperparameters should match the iDIA-QC paper's reported approach) on the training set using the 15 metrics as input features. Evaluate performance on held-out validation/test data using classification metrics (accuracy, precision, recall, F1-score, ROC-AUC). Once validated, apply the trained model to new DIA files to generate quality predictions; output results with file identifiers, predicted labels, and optional confidence scores to enable longitudinal quality monitoring and admin notification.

## Related tools

- **DIA-NN** (Provides protein qualitative and quantitative algorithms that inform the 15 DIA metrics used as model input features)
- **msConvert** (Converts raw DIA files to extracted precursor ion chromatogram (PIC) format, upstream of metric extraction)
- **Python (scikit-learn, pandas, numpy)** (Primary environment for data preparation, model training, evaluation, and prediction in iDIA-QC) — https://github.com/guomics-lab/iDIA-QC

## Evaluation signals

- Model achieves >85% accuracy (or project-specified threshold) on held-out test set; F1-score reflects balance between precision and recall for the quality-prediction task.
- Feature importance or coefficients confirm that the 15 extracted metrics have non-zero, interpretable influence on predictions (e.g., precursor intensity, MS/MS count, dynamic range are top predictors).
- Predictions on new DIA files align with manual quality inspection or longitudinal instrument performance trends (e.g., predicted 'fail' files later show instrument degradation).
- Output predictions include file identifiers and confidence scores; results are shareable via email/WeChat to administrators without requiring post-processing.
- Model generalizes across timsTOF, TripleTOF, and Orbitrap instruments without retraining (if pooled in training) or degradation in cross-instrument validation.

## Limitations

- Model performance may degrade on DIA files from instrument types or configurations not represented in the training data; periodic retraining recommended as instrument settings evolve.
- The 15 metrics assume standard DIA experimental protocols and file formats (.raw, .d, .wiff); non-standard DIA modes or preprocessing may yield unreliable predictions.
- Quality label definition (pass/fail or multiclass tier) is not detailed in the article; mismatch between training labels and operational quality criteria will reduce practical utility.
- Analysis time per file is under 5 minutes (reported in README), but model training time on large datasets is not specified; scalability to thousands of files not quantified.

## Evidence

- [other] Load the 15 extracted DIA metrics and corresponding quality labels from the training dataset; prepare feature matrix and target labels, handling missing values or outliers.: "Load the 15 extracted DIA metrics and corresponding quality labels from the training dataset. 2. Prepare feature matrix and target labels, handling any missing values or outliers."
- [readme] Based on 15 metrics extracted from the DIA files, which characterize raw files from timsTOF, TripleTOF, and Orbitrap instruments.: "Based on 15 metrics extracted from the DIA files, which describe the characteristics of the raw files from timsTOF serial instruments, TripleTOF instruments, and Orbitrap serial instruments"
- [other] Train a machine learning model on the training set using the 15 metrics as features; evaluate model performance on held-out data using appropriate classification metrics.: "Train a machine learning model (algorithm and hyperparameters derived from paper's reported approach) on the training set using the 15 metrics as features. 5. Evaluate model performance on held-out"
- [other] Apply the trained model to new DIA files to generate quality predictions and save results with file identifiers and predicted labels.: "Apply the trained model to new DIA files to generate quality predictions and save results with file identifiers and predicted labels."
- [readme] iDIA-QC promptly shares prediction results and visualization with administrators via email and WeChat.: "it promptly shares the prediction results and visualization with administrators via email and WeChat"
- [readme] Machine learning outputs feature results and status information of the original file, along with potential instrument issues.: "Machine learning outputs feature results and status information of the original file, along with potential instrument issues."
