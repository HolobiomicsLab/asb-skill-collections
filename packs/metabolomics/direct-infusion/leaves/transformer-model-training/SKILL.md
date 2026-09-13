---
name: transformer-model-training
description: Use when you have a dataset of augmented simulated overlapped GC-MS peaks
  and need to train a Transformer model to automatically deconvolve them into pure
  component mass spectra.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - PyTorch
  - Python 3
  - conda
  - GCMSFormer repository
  techniques:
  - LC-MS
  - GC-MS
  - direct-infusion-MS
  license_tier: open
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# transformer-model-training

## Summary

Train a Transformer model (GCMSFormer) to resolve overlapped peaks in GC-MS data by predicting pure mass spectra and concentration distributions. This skill involves partitioning augmented simulated peak data, configuring model hyperparameters, executing the training loop with validation checkpointing, and evaluating performance on held-out test sets using BLEU score.

## When to use

Apply this skill when you have a dataset of augmented simulated overlapped GC-MS peaks and need to train a Transformer model to automatically deconvolve them into pure component mass spectra. Specifically, use this when you have 100,000+ simulated overlapped peaks that can be partitioned into training (80%), validation (10%), and test (10%) sets, and your goal is to achieve BLEU score ≥0.9988 on the test set.

## When NOT to use

- Input dataset is smaller than 10,000 samples or cannot be partitioned into the 8:1:1 train/validation/test ratio without violating data independence.
- Goal is not to predict mass spectral matrices and concentration distributions but rather to perform other GC-MS analyses (e.g., retention time prediction, compound identification from known libraries).
- Peaks are already resolved or are from a different analytical modality (e.g., LC-MS, direct infusion MS) where the overlapped peak simulation strategy is not applicable.

## Inputs

- 100,000 augmented simulated overlapped GC-MS peaks dataset
- data augmentation parameters (para object)
- hyperparameters for model training (para object)
- training set (TRAIN)
- validation set (VALID)
- target vocabulary library (tgt_vocab)

## Outputs

- trained GCMSFormer Transformer model
- training loss history
- test-set BLEU score (metric ≥0.9988)
- model checkpoint at best validation performance

## How to apply

First, generate or load 100,000 augmented simulated overlapped peaks using the `gen_datasets` function with appropriate data augmentation parameters. Partition the data into training (80,000), validation (10,000), and test (10,000) sets according to the 8:1:1 ratio. Initialize the GCMSFormer Transformer architecture with configured hyperparameters. Call the `train_model` function with the training set, validation set, and target vocabulary to execute the training loop with PyTorch backpropagation. During training, apply validation-based checkpointing or early stopping to select the model with best validation performance. After training completes, evaluate the final model on the held-out test set and compute the BLEU (bilingual evaluation understudy) score metric. Verify that the test-set BLEU score reaches or exceeds the benchmark of 0.9988.

## Related tools

- **PyTorch** (Deep learning framework for implementing Transformer architecture, backpropagation, and model training loop) — https://pytorch.org/
- **Python 3** (Programming language for model implementation and orchestration) — https://www.python.org/
- **conda** (Environment and dependency management for reproducible package installation) — https://conda.io/docs/user-guide/install/download.html
- **GCMSFormer repository** (Provides gen_datasets function for data augmentation, train_model function for training loop, and model architecture) — https://github.com/zxguocsu/GCMSFormer

## Examples

```
model, Loss = train_model(para, TRAIN, VALID, tgt_vacob)
```

## Evaluation signals

- Test-set BLEU score equals or exceeds 0.9988, demonstrating model reproducibility against benchmark.
- Validation loss decreases monotonically during training epochs before plateau, indicating model convergence and proper checkpoint selection.
- Training loss is consistently lower than validation loss, confirming absence of overfitting.
- Model predictions on test set correctly recover pure mass spectral matrix (S) such that least squares fitting to concentration distribution matrix (C) produces physically plausible component spectra.
- Data partitioning maintains 8:1:1 ratio exactly: 80,000 train / 10,000 validation / 10,000 test samples with no overlap.

## Limitations

- Model is trained and evaluated only on augmented simulated overlapped peaks; performance on real GC-MS data with experimental noise and irregular peak shapes may differ significantly.
- BLEU score alone does not capture whether predicted mass spectra are chemically meaningful or match authentic library spectra; downstream validation via orthogonal projection resolution (OPR) and least squares fitting is required.
- Training requires substantial computational resources (GPU with PyTorch support recommended) and may not converge within acceptable time on CPU-only systems.
- Benchmark BLEU score of 0.9988 is dataset-specific; generalization to other peak overlap scenarios, mass ranges, or component mixtures is not guaranteed.

## Evidence

- [other] GCMSFormer achieved a BLEU score of 0.9988 on the test set when trained, validated, and tested with 100,000 augmented simulated overlapped peaks in an 8:1:1 ratio.: "GCMSFormer achieved a BLEU score of 0.9988 on the test set when trained, validated, and tested with 100,000 augmented simulated overlapped peaks in an 8:1:1 ratio."
- [readme] The overlapped peak dataset for training, validating and testing the GCMSFormer model is obtained using the gen_datasets functions.: "The overlapped peak dataset for training, validating and testing the GCMSFormer model is obtained using the gen_datasets functions."
- [readme] Train the model based on your own training dataset with train_model function.: "Train the model based on your own training dataset with train_model function."
- [readme] GCMSFormer can predict the pure mass spectra of all components in overlapped peaks (mass spectral matrix S), and then use the least squares method to find the concentration distribution matrix C.: "GCMSFormer can predict the pure mass spectra of all components in overlapped peaks (mass spectral matrix S), and then use the least squares method to find the concentration distribution matrix C."
- [readme] We recommend to use conda. [python3, pytorch] By using the environment.yml file, it will install all the required packages.: "We recommend to use conda. - python3 - pytorch By using the environment.yml file, it will install all the required packages."
