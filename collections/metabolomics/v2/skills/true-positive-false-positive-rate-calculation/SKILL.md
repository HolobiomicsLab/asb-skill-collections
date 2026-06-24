---
name: true-positive-false-positive-rate-calculation
description: Use when you have a trained NeatMS neural network model (.h5 format)
  and need to assess its classification performance at a specific decision threshold
  (e.g., 0.01) to determine what fraction of true peaks are retained (TPR) versus
  what fraction of incorrect peaks are incorrectly accepted (FPR).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - NeatMS
  - Python
  - pandas
  - NumPy
  - scikit-learn
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1021/acs.analchem.1c02220
  title: neatms
evidence_spans:
- NeatMS provides the necessary functions to do that, all we will have to do is create
  a `Neural network handler` object
- Calling the method `get_threshold()` will compute and return the optimal threshold
- After installation, you should be able to import NeatMS
- Import the required libraries first
- import pandas as pd
- import numpy as np
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_neatms
    doi: 10.1021/acs.analchem.1c02220
    title: neatms
  dedup_kept_from: coll_neatms
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c02220
  all_source_dois:
  - 10.1021/acs.analchem.1c02220
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# true-positive-false-positive-rate-calculation

## Summary

Extract and validate True Positive Rate (TPR) and False Positive Rate (FPR) metrics from a trained NeatMS neural network model at a specified probability threshold. This skill is essential for evaluating classifier performance on untargeted LCMS peak classification and understanding the trade-off between retaining true peaks and filtering false positives.

## When to use

Use this skill when you have a trained NeatMS neural network model (.h5 format) and need to assess its classification performance at a specific decision threshold (e.g., 0.01) to determine what fraction of true peaks are retained (TPR) versus what fraction of incorrect peaks are incorrectly accepted (FPR). Apply this when validating model behavior against reference benchmarks or when tuning threshold selection for downstream LCMS peak filtering.

## When NOT to use

- The input model has not yet been trained; train the model using full model training (≥500 peaks per class) or transfer learning before applying this skill.
- The probability threshold value lies outside the supported range [0.00, 0.99]; verify threshold is within documented bounds.
- The class label does not exist in the model's training data; confirm the label matches classes used during model training and annotation.

## Inputs

- trained NeatMS neural network model (.h5 file format)
- probability threshold value (float, range 0.00–0.99)
- class label for evaluation (string, e.g., 'High_quality')

## Outputs

- threshold-dependent recall table (pandas DataFrame)
- True Positive Rate at threshold (float, typically 0.0–1.0)
- False Positive Rate at threshold (float, typically 0.0–1.0)
- False_low ratio (fraction of false positives that are Low_quality)
- False_noise ratio (fraction of false positives that are Noise)

## How to apply

Load the trained NeatMS neural network model (.h5 file) using nn_handler.create_model(model='path_to_model.h5'). Call nn_handler.get_true_vs_false_positive_df(label='High_quality') to generate a threshold-dependent recall table spanning probability thresholds from 0.00 to 0.99. Locate the row where Probability_threshold matches your target value (e.g., 0.01). Extract the True column (TPR, expected ≈1.0 or 100%), False column (FPR, the primary false positive rate metric), False_low (fraction of false positives classified as Low_quality), and False_noise (fraction classified as Noise). Compare retrieved values against expected reference metrics to confirm correct model behavior and threshold-dependent classification dynamics.

## Related tools

- **NeatMS** (Provides neural network handler object and methods to load trained models and compute threshold-dependent True/False Positive Rate tables.) — https://github.com/bihealth/NeatMS
- **Python** (Runtime environment for executing NeatMS handler methods and data frame operations.)
- **pandas** (Used to manipulate and extract rows/columns from the threshold-dependent recall DataFrame.)
- **scikit-learn** (Supports ROC analysis and metric computation for evaluating classifier performance.)

## Examples

```
from neatms import NeuralNetworkHandler
nn_handler = NeuralNetworkHandler()
nn_handler.create_model(model='path_to_trained_model.h5')
recall_df = nn_handler.get_true_vs_false_positive_df(label='High_quality')
metrics_at_0_01 = recall_df[recall_df['Probability_threshold'] == 0.01]
print(metrics_at_0_01[['True', 'False', 'False_low', 'False_noise']])
```

## Evaluation signals

- True Positive Rate (TPR) at threshold 0.01 equals 1.0 (100% of true peaks retained), confirming no true positives are filtered out at this low threshold.
- False Positive Rate (FPR) at threshold 0.01 equals 0.440 (44% of false positives accepted), matching expected reference value.
- False_low ratio at threshold 0.01 equals 0.803 (≈80% of false positives classified as Low_quality), confirming correct sub-classification of rejected peaks.
- False_noise ratio at threshold 0.01 equals 0.206 (≈20% of false positives classified as Noise), confirming complementary sub-classification.
- Row corresponding to Probability_threshold=0.01 is successfully extracted from the returned DataFrame with all four metrics (True, False, False_low, False_noise) present and non-null.

## Limitations

- The skill requires a pre-trained NeatMS neural network model; no mechanism exists to train or tune the model within this isolated calculation.
- The threshold-dependent recall table is computed only for thresholds 0.00 to 0.99 in 0.01 increments; custom intermediate thresholds are not directly supported.
- The class label must match exactly one of the classes used during model training; mismatched labels will produce no output or errors.
- The metrics reflect performance on the training/validation set used to build the model; generalization to new datasets is not assessed by this skill alone.

## Evidence

- [other] research_question: "What are the True Positive Rate and False Positive Rate values at threshold 0.01 when applying the default NeatMS model under full training conditions?"
- [other] workflow_step_1: "Load a trained NeatMS neural network model (in .h5 format) using nn_handler.create_model(model='path_to_model.h5')"
- [other] workflow_step_2: "Call nn_handler.get_true_vs_false_positive_df(label='High_quality') to compute the threshold-dependent recall table across probability thresholds from 0.00 to 0.99"
- [other] workflow_step_3: "Extract the row corresponding to Probability_threshold=0.01 and read the True, False, False_low, and False_noise column values"
- [other] reference_metrics: "Verify that True (TPR) equals 1.0 (100% retention), False (FPR) equals 0.440 (44%), False_low equals 0.803 (80% of false positives are Low_quality), and False_noise equals 0.206 (≈20% are Noise)"
- [readme] intro_finding: "NeatMS relies on neural network based classification to distinguish true from false positive peaks in untargeted LCMS data"
- [readme] readme_intro: "NeatMS enables automated filtering of false positive MS1 peaks reported by commonly used LCMS data processing pipelines"
