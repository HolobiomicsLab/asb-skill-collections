---
name: matrix-multiplication-pipeline
description: Use when after completing 10-fold cross-validated training of MiMeNet neural networks on paired microbiome-metabolome datasets and identifying well-predicted metabolites (those with Spearman correlation coefficient above the 95th percentile of background distribution).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3174
  - http://edamontology.org/topic_3697
  - http://edamontology.org/topic_0621
  tools:
  - MiMeNet
  - Python scikit-learn
  - NumPy
  - TensorFlow or PyTorch
  - Pandas
derived_from:
- doi: 10.1371/journal.pcbi.1009021
  title: MiMeNet
evidence_spans:
- MiMeNet (Microbiome-Metabolome Network), a multi-layer perceptron (MLPNN)
- MiMeNet uses paired microbiome and metabolome data for model training. Microbiome abundance features (green) are used to train a neural network to predict metabolite abundance features (blue).
- models can predict the entire set of metabolites at once, and all models were evaluated using 10 iterations of 10-fold cross-validation. Random Forest models were implemented using
- CLR transformation applied to all data except IBD PRISM microbes
- where W is the weight matrix connecting layer l−1 and layer l. Each element in S represents a microbe-metabolite feature attribution score
- MiMeNet was trained using the ADAM optimizer and the mean squared error (MSE) loss function
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mimenet_cq
    doi: 10.1371/journal.pcbi.1009021
    title: MiMeNet
  dedup_kept_from: coll_mimenet_cq
schema_version: 0.2.0
---

# Reconstruct the Olden's-method feature attribution score matrix from trained MiMeNet networks

## Summary

Extract weight matrices from trained neural network models and compute microbe-metabolite feature attribution scores using Olden's method (successive layer-wise weight matrix multiplication). This skill produces normalized, clipped interaction score matrices that identify which microbial features drive predictions of specific metabolomic features.

## When to use

After completing 10-fold cross-validated training of MiMeNet neural networks on paired microbiome-metabolome datasets and identifying well-predicted metabolites (those with Spearman correlation coefficient above the 95th percentile of background distribution). Use this skill when you need interpretable microbe-metabolite interaction patterns to seed downstream biclustering and module discovery.

## When NOT to use

- Single trained model or <10 cross-validated model instances (insufficient sampling of weight-space variability)
- When metabolite predictions have not yet been filtered by Spearman correlation threshold (attribution scores would include noise from poorly-predicted metabolites)
- When input features have been filtered to <10% sample prevalence but feature names/indices have not been synchronized across training and attribution extraction

## Inputs

- Trained neural network models (100 total from 10 iterations of 10-fold cross-validation)
- Weight matrices W_l extracted from all hidden layers of each model
- Background distribution of attribution scores from shuffled-data cross-validation
- 97.5th percentile threshold value for significance determination
- List of well-predicted metabolites (SCC > 95th percentile)

## Outputs

- 100 per-model microbe-metabolite attribution score matrices (one per trained network)
- Normalized and clipped attribution matrices with values in [-1, +1]
- Filtered attribution matrices containing only microbes with ≥1 significant score
- Structured output format (NumPy arrays or CSV tables indexed by microbe and metabolite feature names)

## How to apply

Load all trained neural network weight matrices W_l from hidden layers l across all 100 models (10 iterations × 10 folds). For each trained model, compute the product of successive layer weights: S = ∏(W_l) where rows represent microbe input features and columns represent metabolite output features. Positive scores indicate increased microbe abundance predicts increased metabolite abundance; negative scores indicate inverse relationship. Normalize each attribution matrix S_i by dividing by the 97.5th percentile threshold identified from the background shuffled-data distribution, then clip all values to the range [-1, +1]. Retain only rows (microbes) with at least one significant attribution score (absolute value > 97.5th percentile threshold) for downstream use.

## Related tools

- **MiMeNet** (Neural network framework that trains multilayer perceptron models on microbiome-metabolome data and provides trained weight matrices for attribution extraction) — https://github.com/YDaiLab/MiMeNet
- **TensorFlow or PyTorch** (Deep learning backend for loading trained model weights and performing matrix operations)
- **NumPy** (Matrix multiplication (np.prod or np.matmul) and element-wise normalization/clipping operations)
- **Pandas** (DataFrame-based I/O and feature name indexing for attributed score matrices)

## Examples

```
# Load 100 trained MiMeNet models and compute Olden's attributions
for model_idx in range(100):
    model = load_trained_model(f'models/cv_fold_{model_idx}.h5')
    weights = [model.layers[i].get_weights()[0] for i in range(model.n_hidden_layers)]
    S = np.linalg.multi_dot(weights)  # Olden's method: successive matrix product
    S_norm = S / background_threshold_97p5
    S_clipped = np.clip(S_norm, -1, 1)
    S_filtered = S_clipped[microbe_indices_with_significant_scores, :]
    attribution_matrices.append(S_filtered)
```

## Evaluation signals

- All 100 attribution matrices have shape (n_microbes, n_metabolites) matching training data dimensions
- After normalization and clipping, 100% of values fall within [-1.0, +1.0] range
- Distribution of attribution score absolute values in each matrix exhibits expected bimodal pattern: background noise near zero and signal tail above 97.5th percentile threshold
- Number of retained microbes (rows with ≥1 significant score) matches the count reported in cross-validation results (e.g., '163 microbes with at least one significant attribution score')
- Symmetry check: sign of attribution score is consistent with direction of microbe–metabolite correlation in the original trained model predictions

## Limitations

- Attribution scores reflect learned network weights but do not incorporate mechanistic or biochemical knowledge; high scores do not prove causal relationships
- Olden's method assumes multiplicative composition of layer-wise effects; non-linear layer interactions (e.g., from ReLU activation functions) are not explicitly captured in the product
- Attribution matrices are data-driven and may reflect confounding or indirect associations rather than direct microbe-metabolite interactions
- Performance depends on quality of upstream training; if metabolite predictions are poor (low Spearman correlation), resulting attribution scores are unreliable noise
- Threshold choice (97.5th percentile for significance) is empirically determined from background distribution but may require adjustment for datasets with different sample sizes or feature richness

## Evidence

- [other] Load trained neural network models from 10 iterations of 10-fold cross-validation (100 total models). For each trained model, extract weight matrices W_l from all hidden layers l in the network.: "Load trained neural network models from 10 iterations of 10-fold cross-validation (100 total models). For each trained model, extract weight matrices W_l from all hidden layers l in the network."
- [other] Apply Olden's method by computing the product of weight matrices across all layers: S = ∏(W_l) for l ∈ L, where each row represents a microbe input feature and each column represents a metabolite output feature.: "Apply Olden's method by computing the product of weight matrices across all layers: S = ∏(W_l) for l ∈ L, where each row represents a microbe input feature and each column represents a metabolite"
- [other] positive scores indicate increased microbe abundance leads to increased metabolite abundance, and negative scores indicate increased microbe abundance leads to decreased metabolite abundance: "positive scores indicate increased microbe abundance leads to increased metabolite abundance, and negative scores indicate increased microbe abundance leads to decreased metabolite abundance"
- [results] MiMeNet constructs a score matrix of microbe-metabolite feature attributions between the microbes and well-predicted metabolites using the learned network weights obtained from cross-validation training: "constructs a score matrix of microbe-metabolite feature attributions between the microbes and well-predicted metabolites using the learned network weights obtained from cross-validation training"
- [methods] We normalized the values in each feature attribution score matrix Si by dividing the significant threshold score identified from the background and clipped values to be between -1 and 1: "We normalized the values in each feature attribution score matrix Si by dividing the significant threshold score identified from the background and clipped values to be between -1 and 1"
- [methods] a threshold was set at the 97.5 percentile. Any feature attribution score in the observed dataset with an absolute value above the threshold was considered significant: "a threshold was set at the 97.5 percentile. Any feature attribution score in the observed dataset with an absolute value above the threshold was considered significant"
- [results] We identified 163 microbes that had at least one significant attribution score with a well-predicted metabolite: "We identified 163 microbes that had at least one significant attribution score with a well-predicted metabolite"
- [methods] the rows representing non-significant microbes were filtered out from S* as well as from all feature attribution score matrices S used in subsequent analyses: "the rows representing non-significant microbes were filtered out from S* as well as from all feature attribution score matrices S used in subsequent analyses"
