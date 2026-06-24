---
name: deep-learning-architecture-design-for-sequence-data
description: Use when when you have raw co-fractionation/mass-spectrometry elution
  profiles (normalized intensity vectors across fractions) paired with labeled protein
  interaction ground truth, and you want to avoid hand-crafted features (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0337
  edam_topics:
  - http://edamontology.org/topic_0128
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3474
  tools:
  - SPIFFED
  - EPIC
  - TensorFlow 1.13.1 / Keras 2.2.4
  - scikit-learn
  license_tier: restricted
derived_from:
- doi: 10.1093/bib/bbad229/7199559
  title: SPIFFED
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_spiffed_cq
    doi: 10.1093/bib/bbad229/7199559
    title: SPIFFED
  dedup_kept_from: coll_spiffed_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bib/bbad229/7199559
  all_source_dois:
  - 10.1093/bib/bbad229/7199559
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# deep-learning-architecture-design-for-sequence-data

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Design and implement a balanced end-to-end deep neural network architecture that processes raw sequential elution intensity data without manual feature extraction to predict protein–protein interactions from co-fractionation/mass-spectrometry profiles. This skill is essential when raw co-elution data must be directly fed into a learner with class imbalance handling.

## When to use

When you have raw co-fractionation/mass-spectrometry elution profiles (normalized intensity vectors across fractions) paired with labeled protein interaction ground truth, and you want to avoid hand-crafted features (e.g., correlation scores, distance metrics) in favor of learning representations end-to-end. Specifically, use this skill when elution data is available as raw intensity profiles (not pre-computed similarity scores) and you need to handle imbalanced positive/negative PPI labels.

## When NOT to use

- Input elution data has already been pre-computed into correlation scores or engineered features (use Random Forest or classical classifiers instead, e.g., --feature_selection 11101001 with RF).
- You have only small numbers of labeled PPI examples (<100) and cannot generate sufficient negative samples without severe class imbalance.
- Elution profiles are sparse, high-dimensional, or contain extreme outliers that cannot be normalized effectively, as CNN performance degrades without stable numeric input.

## Inputs

- raw co-fractionation/mass-spectrometry elution profiles (normalized intensity vectors, e.g., 2 profiles × 27 fractions per protein pair)
- gold standard PPI labels file (tab-separated: protein_A, protein_B, interaction_label)
- elution profile directory containing input data files

## Outputs

- trained CNN model weights
- predicted interaction scores for all protein pairs
- evaluation metrics (precision, recall, AUC, confusion matrix)
- cross-validation fold results (if k-fold enabled)

## How to apply

First, preprocess raw elution profiles by normalizing intensity values and handling missing data points to standardize input dimensions (e.g., 27 fractions per profile). Design a convolutional neural network (CNN) that accepts raw, stacked elution intensity arrays without prior feature extraction—SPIFFED uses this approach to eliminate manual feature engineering. Implement class-balancing during training via a weighted loss function (e.g., weighted cross-entropy or focal loss) or by controlling the negative-to-positive PPI ratio (e.g., --POS_NEG_RATIO 5 means 5× negative samples per positive). Train with supervised learning on labeled pairs, optionally using k-fold cross-validation to assess generalization (--K_D_TRAIN k --FOLD_NUM 5). Evaluate on held-out test data (default 30% split) by computing binary classification metrics (precision, recall, AUC) and interaction scores for each protein pair. Save trained model weights and predicted interaction scores to disk.

## Related tools

- **SPIFFED** (Reference implementation of balanced end-to-end CNN for CF-MS interactome prediction; provides CNN, Label Spreading, and Random Forest classifiers with class-balancing strategies and raw elution profile input handling.) — https://github.com/bio-it-station/SPIFFED
- **EPIC** (Parent tool from which SPIFFED was derived; uses manual feature engineering rather than end-to-end learning.) — https://github.com/BaderLab/EPIC
- **TensorFlow 1.13.1 / Keras 2.2.4** (Deep learning framework used by SPIFFED to define and train CNN layers.)
- **scikit-learn** (Provides preprocessing (normalization), cross-validation splitting, and evaluation metrics (AUC, precision, recall).)

## Examples

```
python ./main.py -s 000000001 /path/to/elution/profiles -c /path/to/gold_standard.tsv /path/to/output -o out -M CNN -n 10 --LEARNING_SELECTION sl --K_D_TRAIN k --FOLD_NUM 5 --TRAIN_TEST_RATIO 0.3 --POS_NEG_RATIO 5 --NUM_FRC 27
```

## Evaluation signals

- Input elution profiles are successfully loaded, have consistent dimensionality (e.g., all pairs have 2 profiles × 27 fractions), and pass normalization without NaN or Inf values.
- CNN model trains without divergence (loss decreases monotonically or via early stopping) and converges within expected epoch count; validation loss plateaus or improves on held-out fold data.
- Class balance is achieved during training: positive and negative samples are weighted or resampled so that the model does not collapse to trivial predictions (e.g., accuracy > 60%, AUC > 0.6 on test set for a balanced binary problem).
- Predicted interaction scores are in a bounded range (e.g., [0, 1] for sigmoid output) and show ranking power (AUC ≥ 0.65 or higher on test set, depending on signal-to-noise in the CF-MS data).
- Cross-validation fold results are consistent across folds (mean test AUC ± std < 0.1), indicating the model generalizes and is not overfitting to one fold.

## Limitations

- SPIFFED requires Python 2.7 and older dependencies (TensorFlow 1.13.1, Keras 2.2.4); modern environments may face compatibility issues.
- Performance depends critically on gold standard label quality and completeness; sparse or noisy ground truth will degrade training signal.
- CNN architecture details (layer depth, filter counts, activation functions) are not fully exposed in the README, limiting reproducibility and hyperparameter tuning.
- Imbalanced negative PPI ratios (e.g., --POS_NEG_RATIO 5) artificially inflate negative samples, increasing training time and memory; very high ratios may harm generalization.
- Raw elution profiles must be normalized and aligned by fraction number; missing fractions or inconsistent preprocessing can cause shape mismatches and training failures.

## Evidence

- [readme] SPIFFED differs from EPIC in that it uses a convolutional neural network to analyze raw co-elution data, thereby eliminating the need for manual feature engineering.: "SPIFFED differs from EPIC in that it uses a convolutional neural network to analyze raw co-elution data, thereby eliminating the need for manual feature engineering."
- [intro] A balanced end-to-end deep learning model for interactome prediction from co-fractionation/mass-spectrometry (CF-MS) data: "A balanced end-to-end deep learning model for interactome prediction from co-fractionation/mass-spectrometry (CF-MS) data"
- [readme] If you want to run Convolutional Neural Network (CNN) or Label Spreading (LS), you must set this parameter to "-s 000000001": "If you want to run Convolutional Neural Network (CNN) or Label Spreading (LS), you must set this parameter to "-s 000000001""
- [readme] This parameter stores the ratio of negative PPIs to positive PPIs. (default: 1): "This parameter stores the ratio of negative PPIs to positive PPIs. (default: 1)"
- [other] Preprocess elution data by normalizing intensity values and handling missing data points. Design a balanced deep neural network architecture with feature-extraction-free layers to accept raw elution profiles. Implement class-balancing strategy during training to handle imbalanced positive/negative PPI labels.: "Preprocess elution data by normalizing intensity values and handling missing data points. Design a balanced deep neural network architecture with feature-extraction-free layers to accept raw elution"
