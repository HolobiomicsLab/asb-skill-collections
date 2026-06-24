---
name: feature-interpretation-neural-networks
description: Use when you have trained multiple neural network models (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3474
  - http://edamontology.org/topic_3373
  - http://edamontology.org/topic_0625
  tools:
  - MiMeNet
  - Python scikit-learn
  - NumPy
  - TensorFlow or PyTorch
  - Scikit-learn
  license_tier: open
derived_from:
- doi: 10.1371/journal.pcbi.1009021
  title: MiMeNet
evidence_spans:
- MiMeNet (Microbiome-Metabolome Network), a multi-layer perceptron (MLPNN)
- MiMeNet uses paired microbiome and metabolome data for model training. Microbiome
  abundance features (green) are used to train a neural network to predict metabolite
  abundance features (blue).
- models can predict the entire set of metabolites at once, and all models were evaluated
  using 10 iterations of 10-fold cross-validation. Random Forest models were implemented
  using
- CLR transformation applied to all data except IBD PRISM microbes
- where W is the weight matrix connecting layer l−1 and layer l. Each element in S
  represents a microbe-metabolite feature attribution score
- MiMeNet was trained using the ADAM optimizer and the mean squared error (MSE) loss
  function
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pcbi.1009021
  all_source_dois:
  - 10.1371/journal.pcbi.1009021
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Reconstruct feature attribution score matrix from trained neural networks using Olden's method

## Summary

Extract and interpret learned feature relationships from trained multilayer perceptron networks by computing element-wise products of weight matrices across all hidden layers, producing a normalized microbe-metabolite interaction score matrix where positive and negative values indicate predicted directional effects on metabolite abundance.

## When to use

You have trained multiple neural network models (e.g., from cross-validation) and need to understand which input features (microbes) drive predictions of output features (metabolites), especially when you want to group microbes and metabolites with similar interaction patterns into functional modules and identify significant directional associations.

## When NOT to use

- Linear regression models (e.g., Elastic Net, MelonnPan): Olden's method is specific to neural networks with stacked weight matrices; linear models do not have layered weight matrices to multiply.
- Single-layer networks or models without hidden layers: The method relies on composing weights across multiple layers; it loses interpretability with insufficient depth.
- When you only need global feature importance (e.g., permutation importance or SHAP): Olden's method produces directional pairwise interactions, not univariate feature ranks.

## Inputs

- Trained TensorFlow or PyTorch multilayer perceptron neural network models (100 total from 10 iterations of 10-fold cross-validation)
- Background distribution of attribution scores from shuffled cross-validation
- List of well-predicted metabolites (identified via Spearman correlation coefficient threshold)
- Feature names (microbe and metabolite identifiers)

## Outputs

- Per-model microbe-metabolite feature attribution score matrices (NumPy arrays or CSV tables, indexed by microbe and metabolite names)
- Normalized and clipped attribution scores in range [-1, 1]
- Filtered set of microbes with significant metabolite associations
- Significance threshold value (97.5th percentile) for identifying important interactions

## How to apply

For each of the trained neural network models, extract all weight matrices W_l from every hidden layer l. Apply Olden's method by computing the element-wise product S = ∏(W_l) across all layers, where each row corresponds to a microbe input feature and each column to a metabolite output feature. Normalize each attribution matrix by dividing by the significant threshold derived from a shuffled background distribution (typically the 97.5th percentile of background attribution scores). Clip all normalized values to the range [-1, 1] to bound the interpretation. Record attribution scores where positive values indicate increased microbe abundance predicts increased metabolite abundance, and negative scores indicate inverse relationships. Select only microbes with at least one significant (absolute value above the threshold) attribution score to well-predicted metabolites for downstream analysis.

## Related tools

- **MiMeNet** (Trains multilayer perceptron networks on microbiome-metabolome data and orchestrates Olden's method computation on learned weights) — https://github.com/YDaiLab/MiMeNet
- **TensorFlow or PyTorch** (Underlying deep learning framework that provides trained model objects and weight matrix access for attribution extraction)
- **NumPy** (Element-wise matrix multiplication and normalization operations during score computation and clipping)
- **Scikit-learn** (Cross-validation splitting and model evaluation metrics (Spearman correlation) to identify well-predicted metabolites)

## Examples

```
# Extract attribution matrices from 100 trained MiMeNet models and apply Olden's method (pseudocode):
for model_i in trained_models:
    weights = [model_i.layers[l].get_weights()[0] for l in range(num_layers)]
    S = np.eye(weights[0].shape[0])  # Initialize identity for first multiplication
    for W_l in weights:
        S = S @ W_l  # Cumulative matrix product
    S_normalized = S / background_threshold_97p5
    S_clipped = np.clip(S_normalized, -1, 1)
    attribution_matrices.append(S_clipped)
```

## Evaluation signals

- All 100 per-model attribution matrices are produced and have shape (num_microbes, num_metabolites) with no NaN or Inf values.
- Normalized scores lie strictly within [-1, 1] after clipping; no values exceed these bounds.
- The number of microbes retained (with ≥1 significant interaction) is substantially smaller than the input microbe count, confirming filtering has occurred.
- Absolute attribution values above the 97.5th percentile threshold are distributed similarly across positive and negative directions (consistent with expected biological interactions).
- Module biclustering on the filtered and normalized score matrix yields discrete clusters with coherent functional or taxonomic membership, suggesting interpretable patterns were recovered.

## Limitations

- Olden's method assumes that multiplying weight matrices in a feedforward network captures the cumulative effect of all hidden layers; this assumes additive or multiplicative signal flow and may not hold for networks with skip connections, attention mechanisms, or complex activation landscapes.
- The method is data-driven without incorporating mechanistic knowledge of microbe-metabolite biochemistry, so high attribution scores do not necessarily imply causal mechanisms.
- Significant threshold determination (97.5th percentile from background distribution) is empirical and may be sensitive to the shuffling scheme and number of background iterations; lower thresholds risk false positives, higher thresholds risk false negatives.
- Attribution scores reflect learned patterns specific to the training data; they may not generalize to external cohorts or environmental conditions not well-represented in the training set.
- Not all metabolites may be genuinely associated with microbes; some well-predicted metabolites may be statistical artifacts, resulting in spurious or weak attributions.

## Evidence

- [other] Apply Olden's method by computing the product of weight matrices across all layers: S = ∏(W_l) for l ∈ L, where each row represents a microbe input feature and each column represents a metabolite output feature.: "Apply Olden's method by computing the product of weight matrices across all layers: S = ∏(W_l) for l ∈ L, where each row represents a microbe input feature and each column represents a metabolite"
- [methods] We normalized the values in each feature attribution score matrix Si by dividing the significant threshold score identified from the background and clipped values to be between -1 and 1: "We normalized the values in each feature attribution score matrix Si by dividing the significant threshold score identified from the background and clipped values to be between -1 and 1"
- [methods] a threshold was set at the 97.5 percentile. Any feature attribution score in the observed dataset with an absolute value above the threshold was considered significant: "a threshold was set at the 97.5 percentile. Any feature attribution score in the observed dataset with an absolute value above the threshold was considered significant"
- [other] positive scores indicate increased microbe abundance leads to increased metabolite abundance, and negative scores indicate increased microbe abundance leads to decreased metabolite abundance.: "positive scores indicate increased microbe abundance leads to increased metabolite abundance, and negative scores indicate increased microbe abundance leads to decreased metabolite abundance."
- [results] using the learned network weights obtained from cross-validation training, MiMeNet constructs a score matrix of microbe-metabolite feature attributions between the microbes and well-predicted: "using the learned network weights obtained from cross-validation training, MiMeNet constructs a score matrix of microbe-metabolite feature attributions between the microbes and well-predicted"
- [results] We identified 163 microbes that had at least one significant attribution score with a well-predicted metabolite: "We identified 163 microbes that had at least one significant attribution score with a well-predicted metabolite"
- [discussion] Although the MiMeNet analysis is data-driven without incorporating mechanistic knowledge, these types of evidence obtained from the integrative analysis of metagenomes and metabolomes could be used: "Although the MiMeNet analysis is data-driven without incorporating mechanistic knowledge, these types of evidence obtained from the integrative analysis of metagenomes and metabolomes could be used"
