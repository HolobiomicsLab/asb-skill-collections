---
name: neural-network-weight-extraction
description: Use when you have trained MLPNN models on paired microbiome-metabolome data (via 10-fold cross-validation repeated across multiple iterations) and need to derive interpretable microbe-metabolite interaction scores rather than treating the network as a black box.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3445
  edam_topics:
  - http://edamontology.org/topic_3174
  - http://edamontology.org/topic_3697
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3360
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3673
  tools:
  - neural networks
  - WGCNA
  - Seaborn clustermap
  - Cytoscape
  - Python scikit-learn
  - TensorFlow
  - scikit-learn
  - MiMeNet
  - NumPy
  - TensorFlow or PyTorch
  - PyTorch
derived_from:
- doi: 10.1371/journal.pcbi.1009021
  title: MiMeNet
evidence_spans:
- An MLPNN model is composed of multiple fully connected hidden layers
- we present MiMeNet, a neural network framework for modeling microbe-metabolite relationships
- Weighted correlation network analysis (WGCNA) of microbial features was performed using the WGCNA library in R
- compared the microbial modules in the IBD (PRISM) dataset identified by MiMeNet to those identified by the Weighted Correlation Network Analysis (WGCNA)
- using Seaborn's clustermap function in Python
- using Cytoscape
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mimenet
    doi: 10.1371/journal.pcbi.1009021
    title: MiMeNet
  - build: coll_mimenet_cq
    doi: 10.1371/journal.pcbi.1009021
    title: MiMeNet
  dedup_kept_from: coll_mimenet
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

# neural-network-weight-extraction

## Summary

Extract weight matrices from trained multilayer perceptron neural networks across multiple cross-validation folds to compute microbe-metabolite feature attribution scores via Olden's method. This enables downstream biclustering and module discovery by quantifying how individual network weights contribute to metabolite abundance predictions.

## When to use

You have trained MLPNN models on paired microbiome-metabolome data (via 10-fold cross-validation repeated across multiple iterations) and need to derive interpretable microbe-metabolite interaction scores rather than treating the network as a black box. Use this when your goal is to construct functional modules or interaction networks that group microbes and metabolites by their learned predictive relationships.

## When NOT to use

- You have only a single trained neural network model; Olden's method requires an ensemble to compute a meaningful consensus attribution matrix.
- Your network output is a classification task or categorical prediction rather than regression of metabolite abundances; Olden's method is designed for continuous feature attribution in regression contexts.
- You lack a background distribution from shuffled-data cross-validation; the 97.5 percentile threshold depends on empirically estimated background statistics.

## Inputs

- Trained MLPNN weight matrices (W_l) from all hidden layers
- Ensemble of trained neural network models (≥10 models from cross-validation)
- Background distribution of attribution scores (from shuffled-data cross-validation)
- List of well-predicted metabolites (filtered by correlation threshold)

## Outputs

- Normalized microbe-metabolite attribution score matrix (values in [−1, 1])
- Mean attribution matrix S* (averaged across all trained models)
- List of significant microbes (those with ≥1 score above 97.5 percentile threshold)
- Module membership assignments (if biclustering is applied downstream)

## How to apply

Load all trained MLPNN weight matrices W_l from hidden layers across the ensemble of models (e.g., 100 models from 10 iterations × 10-fold cross-validation). Apply Olden's method by multiplying weight matrices across all layers sequentially (S = ∏ W_l for l ∈ L) to produce one attribution score matrix per trained model. Average all score matrices to generate a consensus matrix S*, then flatten and apply a 97.5 percentile threshold (computed from the background distribution of shuffled-data models) to identify significant scores. Normalize all significant scores to the range [−1, 1] by dividing by the 97.5 percentile threshold, filter out microbes with no attribution scores above threshold across any well-predicted metabolite, and output the normalized score matrix for subsequent clustering or network analysis.

## Related tools

- **TensorFlow** (Framework for loading and manipulating trained neural network weight matrices)
- **scikit-learn** (Hierarchical clustering and consensus clustering on normalized attribution scores)
- **Seaborn clustermap** (Visualization of normalized attribution score matrices)
- **Cytoscape** (Visualization of module-based interaction networks derived from attribution scores)

## Examples

```
# Load 100 trained models and extract weight matrices; compute Olden attribution scores
import numpy as np
for model_i in range(100):
    W_layers = [model_weights[l] for l in range(num_layers)]
    S_i = np.ones(shape=(n_microbes, n_metabolites))
    for W_l in W_layers:
        S_i = S_i @ W_l.T
    S_matrices.append(S_i)
S_star = np.mean(S_matrices, axis=0)
thresh_95 = np.percentile(np.abs(S_background.flatten()), 97.5)
S_norm = S_star / thresh_95
S_norm = np.clip(S_norm, -1, 1)
```

## Evaluation signals

- Mean attribution matrix S* is symmetric in structure and centered near zero (positive and negative contributions are both present).
- Normalized scores are bounded to [−1, 1]; any value outside this range indicates an error in the normalization step.
- Number of significant microbes (with ≥1 score above 97.5 percentile) is substantially smaller than total number of microbes in input data (e.g., 163 out of thousands), confirming that filtering is selective.
- Positive attribution scores correlate with microbes known to increase metabolite abundance; negative scores correlate with inhibitory microbes (validate against prior knowledge or external data).
- Downstream biclustering produces ≥2 and ≤20 consensus clusters (k* and k**), with silhouette coefficient or cumulative distribution function area indicating stable partitions.

## Limitations

- Olden's method assumes multiplicative interactions across layers; complex non-linear pathways through skip connections or residual networks may not be fully captured.
- Attribution scores are relative, not absolute; interpretation depends on the magnitude of the background threshold, which can vary across datasets (e.g., higher threshold observed in longitudinal soil data).
- MiMeNet analysis is data-driven without incorporating mechanistic knowledge; high attribution scores do not prove causal relationships, only learned predictive correlations.
- Not all metabolites may be associated with microbes, resulting in lower prediction correlations for some metabolites and potentially unstable or uninformative attribution scores.
- Weight extraction and attribution computation are sensitive to network hyperparameter choices (number of layers, layer size, L2 penalty, dropout rate); results may differ substantially if architecture is changed.

## Evidence

- [other] Calculate microbe-metabolite feature attribution scores S using Olden's method by multiplying weight matrices across layers (S = ∏ W_l for l ∈ L), producing one score matrix per trained model.: "Calculate microbe-metabolite feature attribution scores S using Olden's method by multiplying weight matrices across layers (S = ∏ W_l for l ∈ L)"
- [other] Generate mean attribution matrix S* by averaging all 100 S_i matrices, then flatten into a feature vector and apply 97.5 percentile threshold to identify significant attribution scores.: "Generate mean attribution matrix S* by averaging all 100 S_i matrices, then flatten into a feature vector and apply 97.5 percentile threshold to identify significant attribution scores"
- [other] Normalize all significant scores to range [-1, 1] by dividing by the 97.5 percentile threshold from background distribution.: "normalize all significant scores to range [-1, 1] by dividing by the 97.5 percentile threshold from background distribution"
- [other] Filter out non-significant microbes (those with no attribution scores above threshold with any well-predicted metabolite): "Filter out non-significant microbes (those with no attribution scores above threshold with any well-predicted metabolite)"
- [other] Load trained MLPNN models (100 models from 10 iterations of 10-fold cross-validation) and extract weight matrices W_l from all hidden layers.: "Load trained MLPNN models (100 models from 10 iterations of 10-fold cross-validation) and extract weight matrices W_l from all hidden layers"
- [other] Positive attribution scores indicate microbes that contribute positively to metabolite abundance prediction, while negative scores indicate negative contributions.: "Positive attribution scores indicate microbes that contribute positively to metabolite abundance prediction, while negative scores indicate negative contributions"
- [methods] Any feature attribution score in the observed dataset with an absolute value above the threshold was considered significant: "Any feature attribution score in the observed dataset with an absolute value above the threshold was considered significant"
- [results] We identified 163 microbes that had at least one significant attribution score with a well-predicted metabolite: "We identified 163 microbes that had at least one significant attribution score with a well-predicted metabolite"
