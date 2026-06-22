---
name: class-imbalance-handling-in-neural-networks
description: Use when your PPI prediction dataset has a large mismatch between positive (true interactions) and negative (non-interactions) labels—typical in CF-MS interactome prediction where true interactions are rare. When training an end-to-end neural network (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3627
  edam_topics:
  - http://edamontology.org/topic_0128
  - http://edamontology.org/topic_0821
  - http://edamontology.org/topic_3500
  tools:
  - SPIFFED
  - TensorFlow / Keras
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bib/bbad229/7199559
  all_source_dois:
  - 10.1093/bib/bbad229/7199559
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# class-imbalance-handling-in-neural-networks

## Summary

Apply class-balancing strategies during deep learning model training to handle imbalanced positive and negative protein-protein interaction (PPI) labels in co-fractionation/mass-spectrometry prediction tasks. This skill ensures the model learns meaningful representations of both classes despite severe label imbalance.

## When to use

Your PPI prediction dataset has a large mismatch between positive (true interactions) and negative (non-interactions) labels—typical in CF-MS interactome prediction where true interactions are rare. When training an end-to-end neural network (e.g., CNN) on raw elution profiles without hand-crafted features, class imbalance causes the model to bias toward the majority class, yielding poor recall on true interactions.

## When NOT to use

- Your dataset has balanced positive and negative labels (roughly equal class frequencies); standard unweighted loss functions suffice.
- You are using a non-neural-network classifier (e.g., random forest with SPIFFED hand-engineered features); those may have their own built-in class weighting.
- You have already performed manual class balancing via stratified sampling or resampling before feeding data to the model.

## Inputs

- co-fractionation/mass-spectrometry raw elution profiles (2D array: N proteins × M fractions)
- labeled protein pairs with binary PPI labels (positive/negative)
- imbalance ratio or class weights specification

## Outputs

- trained neural network model with balanced decision boundary
- per-class evaluation metrics (precision, recall, F1, ROC-AUC for each class)
- PPI prediction scores for all protein pairs

## How to apply

During training, apply class-balancing by selecting an appropriate loss function (weighted cross-entropy or focal loss) that penalizes misclassification of the minority class more heavily. Set the positive-to-negative PPI ratio parameter (e.g., --POS_NEG_RATIO) to control the relative weight of negative examples; values > 1 increase the penalty for false negatives. Alternatively, downsample the majority class or oversample the minority class to achieve desired balance. Monitor validation metrics separately for positive and negative classes (precision, recall, F1) to ensure neither class is neglected. Validate using k-fold cross-validation (--FOLD_NUM parameter) to ensure the balancing strategy generalizes across data splits.

## Related tools

- **SPIFFED** (End-to-end deep learning framework for CF-MS interactome prediction that implements class-balancing strategies during CNN training via weighted loss functions and adjustable POS_NEG_RATIO parameter) — https://github.com/bio-it-station/SPIFFED
- **TensorFlow / Keras** (Deep learning backend used by SPIFFED to implement weighted cross-entropy and focal loss functions for handling class imbalance)
- **scikit-learn** (Provides class_weight utilities and resampling functions for balancing training data before or during neural network training)

## Examples

```
python ./main.py -s 000000001 /path/to/elution/profiles -c /path/to/gold_standard.tsv /path/to/output -o result -M CNN --LEARNING_SELECTION sl --POS_NEG_RATIO 5 --FOLD_NUM 5
```

## Evaluation signals

- Per-class validation recall and precision are both >0.70 (not biased toward majority class); F1 score on minority class is competitive with majority class F1.
- ROC-AUC and PR-AUC metrics show the model separates positive and negative PPIs across the full operating range, not just at extreme thresholds.
- Cross-validation folds show consistent per-class performance (low variance across k splits), indicating the balancing strategy is stable.
- Confusion matrix shows true positive rate and true negative rate are both reasonably high; false negatives (missed interactions) are not disproportionately large.
- Model achieves better performance on the true positive class compared to an unbalanced baseline trained without class weighting.

## Limitations

- Aggressive class weighting (high POS_NEG_RATIO values) can cause overfitting to the minority class, inflating validation metrics while harming generalization; careful tuning and early stopping are required.
- Class imbalance handling does not address data quality issues (e.g., mislabeled or low-confidence PPIs in the gold standard); poor-quality labels will corrupt training regardless of weighting.
- The optimal balance ratio (--POS_NEG_RATIO) is dataset-specific and requires empirical tuning; no universal best value exists.
- Raw elution profile input (feature-extraction free) may contain noisy or uninformative co-elution patterns that no amount of class balancing can remedy; preprocessing quality matters.
- SPIFFED requires Python 2.7 (as of the README), which is obsolete; dependency versions (TensorFlow 1.13.1, Keras 2.2.4) are outdated and may not run on modern systems.

## Evidence

- [other] Implement class-balancing strategy during training to handle imbalanced positive/negative PPI labels.: "Implement class-balancing strategy during training to handle imbalanced positive/negative PPI labels"
- [other] Train the model on labeled protein pairs using an appropriate loss function (e.g., weighted cross-entropy or focal loss) and optimization algorithm.: "Train the model on labeled protein pairs using an appropriate loss function (e.g., weighted cross-entropy or focal loss)"
- [readme] This parameter stores the ratio of negative PPIs to positive PPIs. (default: 1): "This parameter stores the ratio of negative PPIs to positive PPIs. (default: 1)"
- [readme] CNN and LS must come with raw elution profile and supervised or semi-supervised learning modes handle class imbalance via loss weighting.: "CNN and LS must come with raw elution profile ("-s 000000001")"
- [readme] SPIFFED differs from EPIC in that it uses a convolutional neural network to analyze raw co-elution data, thereby eliminating the need for manual feature engineering.: "SPIFFED differs from EPIC in that it uses a convolutional neural network to analyze raw co-elution data"
