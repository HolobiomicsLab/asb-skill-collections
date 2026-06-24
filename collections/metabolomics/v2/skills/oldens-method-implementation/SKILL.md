---
name: oldens-method-implementation
description: Use when you have trained multi-layer perceptron neural networks on paired
  microbiome-metabolome data and need to extract interpretable feature attribution
  scores from the learned weights to identify microbe-metabolite interaction relationships.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3625
  edam_topics:
  - http://edamontology.org/topic_3174
  - http://edamontology.org/topic_3697
  - http://edamontology.org/topic_0625
  tools:
  - MiMeNet
  - Python scikit-learn
  - NumPy
  - TensorFlow or PyTorch
  - TensorFlow / PyTorch
  - scikit-learn
  license_tier: restricted
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

# Olden's Method Implementation for Neural Network Feature Attribution

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Olden's method computes microbe-metabolite feature attribution scores by multiplying weight matrices across all hidden layers of a trained neural network, producing a single attribution matrix per model where rows represent microbial input features and columns represent metabolite output features. This method enables identification of which microbes contribute to predicting each metabolite by quantifying the product-of-weights pathway through the network.

## When to use

Apply this skill when you have trained multi-layer perceptron neural networks on paired microbiome-metabolome data and need to extract interpretable feature attribution scores from the learned weights to identify microbe-metabolite interaction relationships. Use it specifically after cross-validated model training is complete and you want to move from predictive accuracy to mechanistic interpretation of which microbes drive metabolite predictions.

## When NOT to use

- If the neural network is a single-layer network or has no hidden layers (Olden's method requires multiple layers to compute meaningful weight products).
- If you only have access to predictions without the underlying trained model weights (the method requires explicit weight matrices from all layers).
- If you need local post-hoc explanations for individual predictions rather than global feature importance across the entire training set (Olden's method produces global, model-level attributions).

## Inputs

- Trained multi-layer perceptron neural network models (100 models from 10 iterations of 10-fold cross-validation)
- Weight matrices W_l extracted from all hidden layers of each trained model
- Background distribution of significance thresholds (97.5th percentile) from shuffled cross-validation

## Outputs

- Per-model microbe-metabolite feature attribution score matrices (S_i, one per trained network)
- Normalized and clipped attribution scores (values between -1 and 1)
- Structured output tables indexed by microbe feature names (rows) and metabolite feature names (columns)

## How to apply

For each of the trained neural network models (e.g., 100 models from 10 iterations of 10-fold cross-validation), extract the weight matrices W_l from all hidden layers l. Apply Olden's method by computing the element-wise product of all weight matrices in sequence: S = ∏(W_l) for l ∈ L, where each row index corresponds to a microbe input feature and each column index corresponds to a metabolite output feature. Normalize the resulting attribution matrix S_i by dividing each element by the 97.5th percentile significance threshold derived from a background distribution (generated by shuffling), then clip values to the range [-1, 1]. Positive attribution scores indicate that increased microbe abundance leads to increased metabolite abundance prediction, while negative scores indicate inverse relationships. Output all per-model attribution matrices in a structured format (NumPy arrays or CSV tables) indexed by microbe and metabolite feature names for downstream analysis.

## Related tools

- **MiMeNet** (Neural network framework that implements Olden's method for extracting feature attributions from trained models in microbiome-metabolome prediction tasks) — https://github.com/YDaiLab/MiMeNet
- **TensorFlow / PyTorch** (Deep learning frameworks used to construct and train the multi-layer perceptron models from which weight matrices are extracted)
- **NumPy** (Matrix computation library for performing element-wise weight matrix multiplication and normalization operations)
- **scikit-learn** (Machine learning utility library for cross-validation, model evaluation, and normalization preprocessing)

## Examples

```
# Load trained models from cross-validation and extract attribution matrices
for i, model in enumerate(trained_models):
    S_i = np.ones((n_microbes, n_metabolites))
    for layer_weights in model.layers:
        S_i = S_i * layer_weights
    S_i_normalized = S_i / bg_threshold_975
    S_i_clipped = np.clip(S_i_normalized, -1, 1)
    attribution_matrices[i] = S_i_clipped
```

## Evaluation signals

- Per-model attribution matrix S_i has dimensions matching input microbe features (rows) × output metabolite features (columns); verify shape consistency across all 100 models.
- All normalized attribution scores fall within [-1, 1] range after clipping; check for any values outside this interval indicating normalization errors.
- Attribution scores above the 97.5th percentile threshold (in absolute value) are flagged as significant; verify that the threshold is correctly derived from the background shuffled distribution and consistently applied across models.
- Positive and negative attribution scores are distributed and interpretable (e.g., correlate directionally with observed microbe-metabolite relationships in the data); examine sign consistency with known biological interactions.
- Dimensions of output matrices remain consistent with input feature counts after filtering non-significant microbes; verify that row-filtered matrices exclude microbes without any significant attribution scores to well-predicted metabolites.

## Limitations

- Olden's method produces global feature importance based on the product of weights across layers; it does not capture layer-specific or pathway-specific contributions, which can obscure which hidden layers drive specific predictions.
- The significance threshold (97.5th percentile) is derived from an empirical background distribution generated by shuffling; the method's sensitivity to this threshold choice is not fully explored, and different thresholds may yield substantially different interaction predictions.
- Normalization by dividing by the background percentile threshold assumes that the shuffled background distribution is a valid null model; if the data has inherent structure (e.g., compositional effects in microbiome data), this assumption may be violated.
- The method assumes that multiplying weight matrices linearly captures the cumulative effect of microbe-metabolite relationships through the network; in practice, nonlinear interactions within hidden layers may not be fully captured by this product-of-weights approach.
- Attribution matrices derived from Olden's method are based on learned weights and do not incorporate mechanistic or functional knowledge of microbe-metabolite biology; high attribution scores may reflect correlations rather than causal mechanisms.

## Evidence

- [other] For each trained model, extract weight matrices W_l from all hidden layers l in the network. 3. Apply Olden's method by computing the product of weight matrices across all layers: S = ∏(W_l) for l ∈ L, where each row represents a microbe input feature and each column represents a metabolite output feature.: "For each trained model, extract weight matrices W_l from all hidden layers l in the network. 3. Apply Olden's method by computing the product of weight matrices across all layers: S = ∏(W_l) for l ∈"
- [other] MiMeNet constructs a microbe-metabolite feature attribution score matrix using learned network weights from cross-validation training, then normalizes these scores by dividing by the significant threshold identified from background distribution and clips values to be between -1 and 1, with absolute values above the 97.5th percentile threshold considered significant interactions.: "MiMeNet constructs a microbe-metabolite feature attribution score matrix using learned network weights from cross-validation training, then normalizes these scores by dividing by the significant"
- [other] For each attribution matrix S_i, record element-wise values where positive scores indicate increased microbe abundance leads to increased metabolite abundance, and negative scores indicate increased microbe abundance leads to decreased metabolite abundance.: "For each attribution matrix S_i, record element-wise values where positive scores indicate increased microbe abundance leads to increased metabolite abundance, and negative scores indicate increased"
- [other] Output all 100 per-model attribution matrices (one per trained network) in a structured format (e.g., NumPy arrays or CSV tables indexed by microbe and metabolite feature names).: "Output all 100 per-model attribution matrices (one per trained network) in a structured format (e.g., NumPy arrays or CSV tables indexed by microbe and metabolite feature names)."
- [results] using the learned network weights obtained from cross-validation training, MiMeNet constructs a score matrix of microbe-metabolite feature attributions between the microbes and well-predicted: "using the learned network weights obtained from cross-validation training, MiMeNet constructs a score matrix of microbe-metabolite feature attributions between the microbes and well-predicted"
- [methods] a threshold was set at the 97.5 percentile. Any feature attribution score in the observed dataset with an absolute value above the threshold was considered significant: "a threshold was set at the 97.5 percentile. Any feature attribution score in the observed dataset with an absolute value above the threshold was considered significant"
