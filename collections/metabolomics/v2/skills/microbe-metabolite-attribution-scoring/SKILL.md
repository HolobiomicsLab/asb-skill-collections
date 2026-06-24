---
name: microbe-metabolite-attribution-scoring
description: Use when after training multi-layer perceptron neural networks via cross-validation
  to predict metabolite abundances from microbiome composition, when you need to interpret
  which microbes drive predictions of specific metabolites and to identify groups
  of microbes with coherent metabolite.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3174
  - http://edamontology.org/topic_0621
  - http://edamontology.org/topic_3673
  tools:
  - MiMeNet
  - Python scikit-learn
  - NumPy
  - TensorFlow or PyTorch
  - Seaborn clustermap
  - Python
  - Cytoscape
  - SciPy
  - Pandas
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

# microbe-metabolite-attribution-scoring

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Compute feature attribution scores linking individual microbes to predicted metabolites using Olden's method applied to trained neural network weights. This quantifies the directional and magnitude contribution of each microbe to each metabolite prediction, enabling downstream functional module discovery.

## When to use

After training multi-layer perceptron neural networks via cross-validation to predict metabolite abundances from microbiome composition, when you need to interpret which microbes drive predictions of specific metabolites and to identify groups of microbes with coherent metabolite interaction patterns.

## When NOT to use

- Linear regression models (e.g., Elastic Net, MelonnPan): Olden's method is designed for multi-layer networks and does not apply to single-layer linear models without modification.
- When microbes and metabolites have not yet been filtered for quality: apply feature presence filtering (features in <10% of samples removed) and well-predicted metabolite selection before attribution scoring.
- Input is a pre-computed interaction or correlation matrix rather than trained neural network weights: this skill specifically requires learned weight matrices from trained networks.

## Inputs

- Trained neural network models from 10 iterations of 10-fold cross-validation (100 total models)
- Learned weight matrices W_l from all hidden layers of each trained model
- Background distribution of correlation coefficients from shuffled cross-validated data
- Significant correlation threshold from 95th percentile of background distribution
- List of well-predicted metabolites (those exceeding the 95th percentile threshold)

## Outputs

- Per-model microbe-metabolite feature attribution score matrices (100 matrices, one per trained network)
- Normalized and clipped attribution score matrix S* (values in [−1, 1])
- Binary significance mask indicating microbe-metabolite pairs above 97.5th percentile threshold
- Filtered microbe list containing only those with ≥1 significant metabolite association
- Normalized attribution matrices indexed by microbe and metabolite feature names (NumPy arrays or CSV format)

## How to apply

Extract weight matrices W_l from all hidden layers of each trained network model, then apply Olden's method by computing the element-wise product across layers: S = ∏(W_l) for l ∈ L, where each row represents a microbe input feature and each column a metabolite output feature. Normalize each attribution matrix S_i by dividing by the significant threshold score identified from a background distribution (generated by shuffling and cross-validating on permuted data). Clip normalized values to the range [−1, 1]. Flag microbe-metabolite pairs with absolute attribution scores above the 97.5th percentile of the background distribution as significant interactions. Positive scores indicate increased microbe abundance associates with increased metabolite abundance; negative scores indicate inverse associations. Retain only microbes with at least one significant attribution to well-predicted metabolites; filter out non-significant microbes from all downstream analyses.

## Related tools

- **MiMeNet** (Source of trained multi-layer perceptron neural network models from which weight matrices are extracted for attribution scoring) — https://github.com/YDaiLab/MiMeNet
- **TensorFlow or PyTorch** (Framework used to implement neural networks and extract layer weight matrices for Olden's method computation)
- **NumPy** (Efficient element-wise matrix multiplication and normalization operations for computing and processing attribution score matrices)
- **SciPy** (Statistical functions for percentile calculations and background distribution analysis)
- **Pandas** (Data structure for organizing and indexing attribution matrices by microbe and metabolite feature names)

## Examples

```
# Load 100 trained models and extract attribution scores
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import StandardScaler

# For each of 100 models from cross-validation
attribution_matrices = []
for model_path in model_paths:
    model = tf.keras.models.load_model(model_path)
    # Extract weights and compute Olden's method: S = product of all layer weights
    S = np.array([1.0])  # Start with identity
    for layer in model.layers:
        if len(layer.get_weights()) > 0:
            W = layer.get_weights()[0]
            S = S @ W
    # Normalize by background threshold and clip to [-1, 1]
    S_norm = np.clip(S / background_threshold, -1, 1)
    attribution_matrices.append(S_norm)

# Identify significant pairs at 97.5th percentile
attribution_matrices = np.array(attribution_matrices)
significant_mask = np.abs(attribution_matrices) > np.percentile(np.abs(attribution_matrices), 97.5)
print(f'Significant interactions: {np.sum(significant_mask) / significant_mask.size * 100:.2f}%')
```

## Evaluation signals

- All 100 per-model attribution matrices have shape (n_microbes, n_metabolites) matching input feature counts, with row and column labels preserved.
- Normalized score values are strictly within [−1, 1] after clipping; verify no values fall outside this range.
- Percentage of significant interactions (|score| > 97.5th percentile threshold) is <2.5% of all possible pairs, confirming threshold calibration against background distribution.
- Microbe rows with zero significant interactions are completely removed from S*; verify no microbes without ≥1 significant association remain in output.
- Sign consistency check: across the 100 models, a given microbe-metabolite pair should predominantly have the same sign (positive or negative) if the interaction is robust; high sign flipping suggests weak or noisy attribution.

## Limitations

- Attribution scores are data-driven without incorporating mechanistic knowledge; scores reflect learned network associations but do not prove causal metabolic relationships.
- Olden's method assumes feed-forward network architecture; application to recurrent or other non-feedforward architectures requires modification.
- Background distribution and significance thresholds are sample-size and dataset-dependent; thresholds identified on one cohort (e.g., IBD PRISM) may not transfer to external cohorts with different sample sizes, prevalence, or microbiota composition.
- Not all metabolites may be genuinely associated with microbes; some may have low prediction correlations independent of microbiome, leading to lower average attribution scores across all metabolites.
- Attribution scores cannot distinguish direct versus indirect interactions—a high score may reflect direct microbe-metabolite relationships or microbe A → microbe B → metabolite cascades mediated through the latent layer representations.

## Evidence

- [other] For each trained model, extract weight matrices W_l from all hidden layers l in the network.: "For each trained model, extract weight matrices W_l from all hidden layers l in the network."
- [other] Apply Olden's method by computing the product of weight matrices across all layers: S = ∏(W_l) for l ∈ L: "Apply Olden's method by computing the product of weight matrices across all layers: S = ∏(W_l) for l ∈ L, where each row represents a microbe input feature and each column represents a metabolite"
- [other] Normalize these scores by dividing by the significant threshold identified from background distribution and clips values to be between -1 and 1: "MiMeNet constructs a microbe-metabolite feature attribution score matrix using learned network weights from cross-validation training, then normalizes these scores by dividing by the significant"
- [other] absolute values above the 97.5th percentile threshold considered significant interactions: "with absolute values above the 97.5th percentile threshold considered significant interactions."
- [other] positive scores indicate increased microbe abundance leads to increased metabolite abundance, and negative scores indicate increased microbe abundance leads to decreased metabolite abundance: "where positive scores indicate increased microbe abundance leads to increased metabolite abundance, and negative scores indicate increased microbe abundance leads to decreased metabolite abundance."
- [results] We identified 163 microbes that had at least one significant attribution score with a well-predicted metabolite: "We identified 163 microbes that had at least one significant attribution score with a well-predicted metabolite"
- [methods] a threshold was set at the 97.5 percentile. Any feature attribution score in the observed dataset with an absolute value above the threshold was considered significant: "a threshold was set at the 97.5 percentile. Any feature attribution score in the observed dataset with an absolute value above the threshold was considered significant"
- [methods] We normalized the values in each feature attribution score matrix Si by dividing the significant threshold score identified from the background and clipped values to be between -1 and 1: "We normalized the values in each feature attribution score matrix Si by dividing the significant threshold score identified from the background and clipped values to be between -1 and 1"
