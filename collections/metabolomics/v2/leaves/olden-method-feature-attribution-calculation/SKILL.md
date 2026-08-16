---
name: olden-method-feature-attribution-calculation
description: Use when after training multiple MLPNN models (via cross-validation)
  on paired microbiome and metabolome data when you need to extract interpretable
  feature importance scores from network weights to identify which microbes drive
  metabolite predictions and group them into co-functional modules.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3174
  - http://edamontology.org/topic_0622
  - http://edamontology.org/topic_3175
  tools:
  - WGCNA
  - Seaborn clustermap
  - Cytoscape
  - Python scikit-learn
  - TensorFlow
  - scikit-learn
  - MiMeNet
  license_tier: open
derived_from:
- doi: 10.1371/journal.pcbi.1009021
  title: MiMeNet
evidence_spans:
- Weighted correlation network analysis (WGCNA) of microbial features was performed
  using the WGCNA library in R
- compared the microbial modules in the IBD (PRISM) dataset identified by MiMeNet
  to those identified by the Weighted Correlation Network Analysis (WGCNA)
- using Seaborn's clustermap function in Python
- using Cytoscape
- using Python's sci-kit-learn package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mimenet
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

# Olden's Method Feature Attribution Calculation

## Summary

Olden's method derives microbe-metabolite feature attribution scores from trained multilayer perceptron neural network weights by multiplying weight matrices across all hidden layers, producing signed scores that quantify how strongly each microbe contributes to predicting metabolite abundance. These scores are subsequently normalized and thresholded to identify significant microbe-metabolite relationships for downstream functional module construction.

## When to use

Apply this skill after training multiple MLPNN models (via cross-validation) on paired microbiome and metabolome data when you need to extract interpretable feature importance scores from network weights to identify which microbes drive metabolite predictions and group them into co-functional modules. Use it specifically when you have 100+ trained models (e.g., from 10 iterations of 10-fold cross-validation) and want to aggregate their learned relationships into a consensus attribution matrix.

## When NOT to use

- Input is a linear model (e.g., Elastic Net, linear regression) rather than a trained neural network — Olden's method requires weight matrices from multiple hidden layers and is not applicable to single-layer or non-neural models.
- Microbiome or metabolome data has not undergone prior quality filtering (e.g., features present in <10% of samples should be removed first) — attribution scores will be computed on noise-prone features.
- You have fewer than 10–20 trained models; the mean attribution matrix S* requires sufficient models to robustly estimate consensus feature importance and avoid overfitting artifacts from individual model idiosyncrasies.

## Inputs

- Trained MLPNN weight matrices W_l from all hidden layers (100 models × number of layers)
- Well-predicted metabolites list (metabolites with Spearman correlation > 95th percentile of background)
- Background distribution of attribution scores (from shuffled/permuted data cross-validation)

## Outputs

- Mean attribution matrix S* (microbes × metabolites, normalized to [−1, 1])
- Filtered microbe-metabolite attribution score pairs (significant pairs above 97.5 percentile)
- Normalized attribution scores for downstream biclustering (feature vectors per microbe and metabolite)

## How to apply

Load all trained MLPNN weight matrices W_l from every hidden layer of each of the 100 trained models. For each model, compute the microbe-metabolite feature attribution score matrix S by multiplying weight matrices across layers (S = ∏ W_l for l ∈ L). Generate a mean attribution matrix S* by averaging all 100 individual S_i matrices, then apply a 97.5 percentile threshold on the absolute values computed from a background distribution (shuffled data) to identify significant attribution scores. Normalize all significant scores to the range [−1, 1] by dividing by the 97.5 percentile threshold value. Filter out microbes that have no attribution scores above threshold with any well-predicted metabolite. Positive attribution scores indicate microbes that contribute positively to metabolite abundance prediction; negative scores indicate negative contributions.

## Related tools

- **TensorFlow** (Framework for training and loading MLPNN models and extracting weight matrices W_l)
- **scikit-learn** (Computing hierarchical clustering on normalized attribution scores and consensus clustering for module identification)
- **Seaborn clustermap** (Visualization of the mean attribution matrix S* and heatmap display of microbe-metabolite relationships)
- **Cytoscape** (Construction and visualization of module-based interaction network from attribution edge list)
- **MiMeNet** (End-to-end pipeline implementing Olden's method on paired microbiome-metabolome data) — https://github.com/YDaiLab/MiMeNet

## Examples

```
python MiMeNet_train.py -micro microbiome.csv -metab metabolome.csv -micro_norm CLR -metab_norm CLR -num_run_cv 10 -num_cv 10 -output results/
```

## Evaluation signals

- Mean attribution matrix S* has shape (n_microbes, n_metabolites) matching the number of well-predicted metabolites and filtered microbes; all values fall in [−1, 1] after normalization.
- Number of microbes retained after filtering is consistent with the study's findings (e.g., MiMeNet identified 163 microbes with at least one significant attribution score with a well-predicted metabolite in the IBD dataset).
- Distribution of normalized scores is symmetric around zero (positive and negative contributions both present); histogram of absolute values shows expected decay after 97.5 percentile threshold.
- Validation: consensus clustering k-selection (based on Δk > 0.025 threshold) produces stable module assignments across resampling iterations; re-running on held-out test data yields similar module structure.
- Microbe-metabolite pairs with high absolute attribution scores can be cross-validated against literature or mechanistic expectation (e.g., known short-chain fatty acid producers paired with butyrate/propionate metabolites).

## Limitations

- Olden's method is data-driven and does not incorporate mechanistic knowledge; attribution scores reflect learned patterns in training data but do not prove causal relationships between microbes and metabolites.
- Not all metabolites may be associated with microbes; those with weak or no microbe-metabolite associations will have low or zero attribution scores, reducing the overall mean correlation and module coherence.
- The choice of 97.5 percentile threshold for significant scores is empirically derived and may vary across datasets (e.g., soil datasets with longitudinal structure may require higher thresholds); threshold generalizability across different microbiomes or metabolomes is not fully explored.
- Results depend on the quality of prior model training (hyperparameter tuning, cross-validation scheme, feature filtering); poorly trained networks or inappropriate normalization (RA vs. CLR) will yield unreliable attribution matrices.
- Averaging across 100 models assumes equal weight and independence; models from the same cross-validation fold share training data, which may inflate consensus attribution for features that overfit in that fold.

## Evidence

- [other] MiMeNet computes feature attribution scores for all microbe-metabolite pairs from trained MLPNN network weights, then applies biclustering to group microbes and metabolites into modules where members share similar attribution patterns.: "MiMeNet computes feature attribution scores for all microbe-metabolite pairs from trained MLPNN network weights, then applies biclustering to group microbes and metabolites into modules where members"
- [other] Calculate microbe-metabolite feature attribution scores S using Olden's method by multiplying weight matrices across layers (S = ∏ W_l for l ∈ L), producing one score matrix per trained model.: "Calculate microbe-metabolite feature attribution scores S using Olden's method by multiplying weight matrices across layers (S = ∏ W_l for l ∈ L), producing one score matrix per trained model."
- [other] Positive attribution scores indicate microbes that contribute positively to metabolite abundance prediction, while negative scores indicate negative contributions.: "Positive attribution scores indicate microbes that contribute positively to metabolite abundance prediction, while negative scores indicate negative contributions."
- [other] Generate mean attribution matrix S* by averaging all 100 S_i matrices, then flatten into a feature vector and apply 97.5 percentile threshold to identify significant attribution scores (absolute value above threshold).: "Generate mean attribution matrix S* by averaging all 100 S_i matrices, then flatten into a feature vector and apply 97.5 percentile threshold to identify significant attribution scores (absolute"
- [other] Normalize all significant scores to range [-1, 1] by dividing by the 97.5 percentile threshold from background distribution.: "Normalize all significant scores to range [-1, 1] by dividing by the 97.5 percentile threshold from background distribution."
- [other] Filter out non-significant microbes (those with no attribution scores above threshold with any well-predicted metabolite): "Filter out non-significant microbes (those with no attribution scores above threshold with any well-predicted metabolite)"
- [results] MiMeNet constructs a score matrix of microbe-metabolite feature attributions between the microbes and well-predicted metabolites: "MiMeNet constructs a score matrix of microbe-metabolite feature attributions between the microbes and well-predicted metabolites"
- [results] We identified 163 microbes that had at least one significant attribution score with a well-predicted metabolite: "We identified 163 microbes that had at least one significant attribution score with a well-predicted metabolite"
- [methods] Any feature attribution score in the observed dataset with an absolute value above the threshold was considered significant: "Any feature attribution score in the observed dataset with an absolute value above the threshold was considered significant"
- [other] Load trained MLPNN models (100 models from 10 iterations of 10-fold cross-validation) and extract weight matrices W_l from all hidden layers.: "Load trained MLPNN models (100 models from 10 iterations of 10-fold cross-validation) and extract weight matrices W_l from all hidden layers."
