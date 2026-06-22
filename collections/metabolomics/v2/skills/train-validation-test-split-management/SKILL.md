---
name: train-validation-test-split-management
description: Use when when you have a complete dataset of labeled examples (e.g., 100,000 augmented spectra, chromatograms, or synthetic samples) and need to train a supervised model (such as a Transformer) while preserving a held-out test set to measure generalization performance without bias.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3437
  edam_topics:
  - http://edamontology.org/topic_3373
  - http://edamontology.org/topic_0091
  tools:
  - PyTorch
  - Python 3
  - conda
  - gen_datasets function (da.py)
  - PyTorch DataLoader / torch.utils.data
  - train_model function (GCMSformer.py)
derived_from:
- doi: 10.1021/acs.analchem.3c05772
  title: GCMSFormer
evidence_spans:
- '[pytorch](https://pytorch.org/)'
- '[python3](https://www.python.org/)'
- We recommend to use [conda](https://conda.io/docs/user-guide/install/download.html)
- We recommend to use [conda](https://conda.io/docs/user-guide/install/download.html).
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_gcmsformer_cq
    doi: 10.1021/acs.analchem.3c05772
    title: GCMSFormer
  dedup_kept_from: coll_gcmsformer_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.3c05772
  all_source_dois:
  - 10.1021/acs.analchem.3c05772
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# train-validation-test-split-management

## Summary

Partition a dataset into training, validation, and test subsets according to a specified ratio (e.g., 8:1:1) to enable independent model training, hyperparameter tuning, and unbiased performance evaluation. This skill ensures reproducible, non-leaking data splits for machine learning workflows.

## When to use

When you have a complete dataset of labeled examples (e.g., 100,000 augmented spectra, chromatograms, or synthetic samples) and need to train a supervised model (such as a Transformer) while preserving a held-out test set to measure generalization performance without bias. Apply this skill before model initialization and training.

## When NOT to use

- Input is already pre-split into separate files or train/val/test directories with no further partitioning needed.
- Dataset is too small to support a 8:1:1 or similar ratio without test set underpowering (e.g., fewer than 100 samples total).
- Data exhibits temporal or hierarchical dependencies (e.g., time-series chromatography runs from the same sample) where naive random splitting would cause leakage between sets.

## Inputs

- Complete labeled dataset (e.g., 100,000 augmented simulated overlapped peaks with input spectra and target annotations)
- Target split ratio (e.g., 8:1:1 for train:validation:test)
- Random seed (optional, for reproducibility)

## Outputs

- Training set (e.g., 80,000 samples)
- Validation set (e.g., 10,000 samples)
- Test set (e.g., 10,000 samples)
- Split metadata (indices, ratio, seed used)

## How to apply

Load the full dataset into memory or a data structure accessible to your training pipeline. Calculate split boundaries based on the target ratio (e.g., for 8:1:1 on 100,000 samples: train=80,000, validation=10,000, test=10,000). Partition the dataset sequentially or via random sampling (with a fixed seed for reproducibility) to create three disjoint subsets. Assign the training set to the model training loop, the validation set to early stopping or checkpoint selection during training, and reserve the test set for final evaluation only. Document the random seed and split indices to enable reproducibility.

## Related tools

- **gen_datasets function (da.py)** (Generates or loads the complete augmented dataset and applies data augmentation parameters before splitting) — https://github.com/zxguocsu/GCMSFormer/blob/master/GCMSFormer/da.py#L240
- **PyTorch DataLoader / torch.utils.data** (Wraps split datasets to enable batching, shuffling, and iteration during training and validation) — https://pytorch.org/
- **train_model function (GCMSformer.py)** (Accepts the partitioned TRAIN and VALID sets to perform model training with validation-based early stopping) — https://github.com/zxguocsu/GCMSFormer/blob/master/GCMSFormer/GCMSformer.py#L410

## Examples

```
TRAIN, VALID, TEST, tgt_vacob = gen_datasets(para); model, Loss = train_model(para, TRAIN, VALID, tgt_vacob)
```

## Evaluation signals

- Split size verification: train + validation + test == total dataset size, and each subset respects the target ratio (e.g., 80:10:10 ± rounding).
- Disjointness check: no sample ID or index appears in more than one subset; three sets are mutually exclusive.
- Reproducibility: using the same random seed on the same dataset produces identical splits across runs.
- Test set isolation: the test set is used only for final evaluation (after train_model completes), never during training or hyperparameter search.
- BLEU score benchmark: when test set is used to evaluate a trained model, the reported BLEU score on the held-out test set matches or exceeds the baseline (0.9988 in this article).

## Limitations

- Simple random splitting does not account for class imbalance, temporal order, or hierarchical structure in the data; stratified or grouped splitting may be required for real chromatography or spectroscopy workflows.
- Fixed ratio (8:1:1) may not be optimal for small datasets or highly imbalanced classes; cross-validation or adaptive splitting may be preferable.
- Data augmentation (e.g., synthetic peak overlapping) must be applied to the full dataset before splitting to ensure fair representation across sets; augmenting only the training set can bias validation/test performance.
- No guidance in the article on handling overlapping peaks or instrumental artifacts that may correlate across splits, potentially causing leakage.

## Evidence

- [intro] The GCMSFormer model was trained, validated, and tested with 100,000 augmented simulated overlapped peaks in a ratio of 8:1:1: "The GCMSFormer model was trained, validated, and tested with 100,000 augmented simulated overlapped peaks in a ratio of 8:1:1"
- [other] Load the 100,000 augmented simulated overlapped peaks dataset and partition into train (80,000), validation (10,000), and test (10,000) sets according to the 8:1:1 ratio.: "partition into train (80,000), validation (10,000), and test (10,000) sets according to the 8:1:1 ratio"
- [other] Validate model performance on the validation set during training and apply early stopping or checkpoint selection.: "Validate model performance on the validation set during training and apply early stopping or checkpoint selection"
- [other] Evaluate the trained model on the held-out test set and compute BLEU score metric.: "Evaluate the trained model on the held-out test set and compute BLEU score metric"
- [readme] The overlapped peak dataset for training, validating and testing the GCMSFormer model is obtained using the gen_datasets functions.: "The overlapped peak dataset for training, validating and testing the GCMSFormer model is obtained using the gen_datasets functions"
