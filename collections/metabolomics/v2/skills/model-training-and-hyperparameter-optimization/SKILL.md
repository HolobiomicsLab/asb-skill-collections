---
name: model-training-and-hyperparameter-optimization
description: Use when you have raw co-elution profiles (27 fractions × 2+ proteins per pair) and a gold-standard PPI reference set, want to avoid manual feature engineering, and need to handle severe class imbalance (negative PPIs >> positive PPIs).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0128
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3373
  tools:
  - SPIFFED
  - EPIC
  - TensorFlow
  - Keras
  - scikit-learn
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
---

# model-training-and-hyperparameter-optimization

## Summary

Train a balanced end-to-end deep learning model (CNN or Label Spreading) on co-fractionation/mass-spectrometry elution profiles with class-balancing strategies and systematic hyperparameter tuning to predict protein–protein interactions without manual feature engineering.

## When to use

You have raw co-elution profiles (27 fractions × 2+ proteins per pair) and a gold-standard PPI reference set, want to avoid manual feature engineering, and need to handle severe class imbalance (negative PPIs >> positive PPIs). Use this skill when direct training or k-fold cross-validation is required to find optimal negative-to-positive PPI ratios, test/train splits, and CNN architecture settings.

## When NOT to use

- Input elution profiles have already been manually feature-engineered (e.g., Pearson correlation, Euclidean distance pre-computed)—use RF with those engineered features instead.
- You lack a curated gold standard PPI reference set; semi-supervised learning (LS) may still work but supervised learning (CNN with SL) will degrade without labeled training pairs.
- Elution profiles are in a non-standard format or missing fractions; preprocessing must normalize and handle missingness before passing to the model.

## Inputs

- co-fractionation/mass-spectrometry elution profile files (intensity values across 27 fractions, 2 proteins per pair)
- gold standard PPI reference file (tab-separated protein pairs with binary labels)
- input directory path (absolute)

## Outputs

- trained model weights
- predicted interaction scores for all protein pairs
- per-fold or direct-training performance metrics (precision, recall, ROC-AUC)
- output directory with specified prefix-named result files

## How to apply

Preprocess elution profiles by normalizing intensity values and handling missing data, then set the feature-selection flag to raw elution profile mode (`-s 000000001`). Choose a training method (CNN or LS for raw profiles; RF for engineered features) and specify supervised or semi-supervised learning via `--LEARNING_SELECTION`. Configure class balancing by adjusting `--POS_NEG_RATIO` (default 1:1, often increased to 1:5 or 1:10 to match biological prevalence of negative PPIs). Select either direct training (`--K_D_TRAIN d`) or k-fold validation (`--K_D_TRAIN k --FOLD_NUM 5`). Set `--TRAIN_TEST_RATIO` (default 0.3) to control validation/test splits. For CNN ensemble models, set `--CNN_ENSEMBLE 1` and provide multiple elution profiles (`--NUM_EP 2`). Train using weighted loss (cross-entropy or focal loss implied by class-balancing strategy) and evaluate on held-out test set.

## Related tools

- **SPIFFED** (end-to-end implementation of CNN and Label Spreading training pipelines with class-balancing and k-fold cross-validation for PPI prediction from raw CF-MS elution profiles) — https://github.com/bio-it-station/SPIFFED
- **EPIC** (predecessor tool providing RF-based PPI prediction with manually engineered correlation scores; SPIFFED improves upon it by eliminating feature engineering) — https://github.com/BaderLab/EPIC
- **TensorFlow** (deep learning backend for CNN model training)
- **Keras** (high-level API for constructing and training neural network architectures)
- **scikit-learn** (provides Random Forest classifier and preprocessing/evaluation utilities)

## Examples

```
python ./main.py -s 000000001 /path/to/input/elution_profiles -c /path/to/gold_standard.tsv /path/to/output -o results -M CNN -n 10 -m EXP -f STRING --LEARNING_SELECTION sl --K_D_TRAIN k --FOLD_NUM 5 --TRAIN_TEST_RATIO 0.3 --POS_NEG_RATIO 5 --NUM_EP 2 --NUM_FRC 27 --CNN_ENSEMBLE 1
```

## Evaluation signals

- Verify that class balance ratio matches the specified `--POS_NEG_RATIO` parameter in the training set (e.g., if `--POS_NEG_RATIO 5`, check that #negatives ≈ 5 × #positives).
- For k-fold training, confirm that each fold achieves convergence (loss decreases monotonically or stabilizes) and that per-fold AUC/precision/recall metrics are reported for all k folds.
- Check that output files are created with the specified prefix and that predicted interaction scores are saved and span a sensible range (e.g., 0–1 for probability or –1 to +1 for confidence).
- Validate that test-set performance (ROC-AUC, precision-recall) is reported separately from training performance; CNN should outperform RF baseline on unseen raw elution profiles.
- Confirm that the model handles the specified number of fractions (`--NUM_FRC 27`) and elution profiles per pair (`--NUM_EP 2`) without shape mismatches or NaN outputs.

## Limitations

- Python 2.7 requirement (deprecated); modern deployments may face dependency conflicts with TensorFlow 1.13.1 and Keras 2.2.4.
- CNN architecture details (layers, units, activation functions, dropout rates) are not fully exposed in the README; reproducibility and ablation studies require access to source code.
- Class-balancing strategy via `--POS_NEG_RATIO` is a simple undersampling or oversampling approach; more advanced techniques (focal loss, weighted cross-entropy) are mentioned but not explicitly configurable.
- Scalability and runtime are not characterized; performance on large interactomes or with high-dimensional elution profiles (many fractions or many replicates) is unknown.
- Semi-supervised learning (LS) requires unlabeled data; the README does not specify how unlabeled PPIs are selected or weighted during training.

## Evidence

- [readme] SPIFFED uses a convolutional neural network to analyze raw co-elution data, thereby eliminating the need for manual feature engineering.: "it uses a convolutional neural network to analyze raw co-elution data, thereby eliminating the need for manual feature engineering"
- [readme] A balanced end-to-end deep learning model for interactome prediction from co-fractionation/mass-spectrometry (CF-MS) data: "A balanced end-to-end deep learning model for interactome prediction from co-fractionation/mass-spectrometry (CF-MS) data"
- [other] Implement class-balancing strategy during training to handle imbalanced positive/negative PPI labels.: "Implement class-balancing strategy during training to handle imbalanced positive/negative PPI labels"
- [other] Train the model on labeled protein pairs using an appropriate loss function (e.g., weighted cross-entropy or focal loss) and optimization algorithm.: "Train the model on labeled protein pairs using an appropriate loss function (e.g., weighted cross-entropy or focal loss)"
- [readme] If you want to run with semi-supervised learning, then set `--LEARNING_SELECTION ssl` (Your training_method can be CNN or LS).: "If you want to run with semi-supervised learning, then set `--LEARNING_SELECTION ssl` (Your training_method can be CNN or LS)"
- [readme] Set `--K_D_TRAIN` d to directly train the model; set `--K_D_TRAIN` k to run with k-fold training.: "Set `--K_D_TRAIN` d to directly train the model; set `--K_D_TRAIN` k to run with k-fold training"
- [readme] `--POS_NEG_RATIO` negative_PPIs_ratio: This parameter stores the ratio of negative PPIs to positive PPIs. (default: 1): "`--POS_NEG_RATIO` negative_PPIs_ratio: This parameter stores the ratio of negative PPIs to positive PPIs"
