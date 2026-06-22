---
name: cluster-validation-cdf-threshold-selection
description: Use when when you have generated multiple biclusters or clusterings from ensemble models (e.g., 100 trained neural network models via cross-validation) and need to select an objective cluster number k without manual inspection.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3474
  - http://edamontology.org/topic_0091
  tools:
  - Seaborn clustermap
  - Python
  - Cytoscape
  - Hierarchical clustering (Euclidean distance, complete linkage)
  - Consensus clustering
  - Python (NumPy, SciPy, Pandas)
derived_from:
- doi: 10.1371/journal.pcbi.1009021
  title: MiMeNet
evidence_spans:
- linkage using Seaborn’s clustermap function in
- using Python's sci-kit-learn package
- Networks showing microbe and metabolite modules and the interactions between them were constructed using Cytoscape
- Networks showing the modules and the interactions between them were constructed using Cytoscape
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# cluster-validation-cdf-threshold-selection

## Summary

Determine the optimal number of clusters in a dataset by computing consensus matrices across multiple trained models, calculating cumulative distribution functions (CDFs), and selecting the largest cluster number where the proportional change in area under the CDF exceeds a predefined threshold (e.g., Δk > 0.025). This approach validates clustering stability and prevents over-clustering.

## When to use

When you have generated multiple biclusters or clusterings from ensemble models (e.g., 100 trained neural network models via cross-validation) and need to select an objective cluster number k without manual inspection. Particularly useful when clustering rows and columns of a matrix independently (e.g., microbes and metabolites from a bipartite feature attribution matrix) and seeking consensus across model runs.

## When NOT to use

- Input is a single clustering result, not an ensemble of models — consensus methods require multiple independent runs to detect stable structure.
- You have prior domain knowledge strongly favoring a specific cluster number — this method is data-driven and may override expert judgment.
- The dataset has clear, well-separated clusters visible by visual inspection — simpler elbow methods or silhouette analysis may suffice.

## Inputs

- Multiple trained clustering models or ensemble model weights (e.g., 100 neural networks trained via 10-fold cross-validation)
- Normalized feature matrix or attribution score matrix (e.g., S_i normalized by dividing by significant threshold and clipped to [-1, 1])
- Candidate range for cluster numbers k (e.g., k ∈ [2, 20])

## Outputs

- Optimal cluster numbers k₁* (for rows) and k₂* (for columns)
- Consensus matrices for each k (average connectivity across ensemble models)
- CDF values and area-under-curve (AUC) for each k
- Elbow plot or area-change plot (Δk vs. k) for visual validation
- Final cluster assignments using k₁* and k₂*

## How to apply

For each candidate cluster number k ranging from 2 to a maximum (e.g., 20), generate k-clusterings across all trained models (e.g., 100 models). Build a consensus matrix by averaging the connectivity matrices (binary adjacency indicating co-clustering) from all models. Calculate the cumulative distribution function (CDF) of each consensus matrix and compute the area under the CDF curve. Plot the area values against k and identify the largest k where the proportional change Δk = (area_k - area_k-1) / area_k-1 exceeds the threshold (e.g., 0.025). This peak-detection strategy identifies the elbow point where additional clusters add diminishing information gain. Apply this procedure separately to rows (e.g., microbes) and columns (e.g., metabolites) to obtain k₁* and k₂*.

## Related tools

- **Hierarchical clustering (Euclidean distance, complete linkage)** (Initial clustering of rows and columns for each k value; used within the consensus clustering loop)
- **Seaborn clustermap** (Visualization tool for displaying hierarchical clusters and heatmaps during exploratory analysis)
- **Consensus clustering** (Core method that generates connectivity matrices across ensemble models and averages them to compute consensus)
- **Python (NumPy, SciPy, Pandas)** (Implementation language for computing CDFs, areas under curves, and proportional change calculations) — https://github.com/YDaiLab/MiMeNet

## Evaluation signals

- Verify that the area-under-CDF plot shows a clear elbow or inflection point; a monotonically increasing or flat curve indicates poor cluster structure or inappropriate threshold.
- Confirm that selected k values (k₁* and k₂*) produce biologically or functionally meaningful clusters (e.g., metabolite modules enriched for disease state in statistical tests: Wilcoxon rank-sum, p < 0.05).
- Check that consensus matrices have high diagonal values (indicating strong within-cluster co-clustering) and low off-diagonal values for non-consensus assignments.
- Validate that the proportional change Δk transitions from above threshold to below threshold at k*, not scattered erratically across the range.
- Examine that cluster assignments remain stable across cross-validation folds — members should not shuffle dramatically between folds.

## Limitations

- Method assumes ensemble models are sufficiently diverse; if all models converge to identical solutions, consensus matrices will be binary and CDF-based selection loses discriminative power.
- Threshold selection (e.g., Δk = 0.025) is somewhat arbitrary; sensitivity to this parameter is not formally analyzed in the article, and different datasets may require empirical tuning.
- Computational cost scales with the number of candidate k values and ensemble size; evaluating k ∈ [2, 20] across 100 models requires ~100 hierarchical clusterings per k.
- Method requires rows and columns to be clustered independently; it does not optimize a joint objective for both dimensions simultaneously, potentially missing biclusters that are tightly coupled.
- CDF-based area calculation is sensitive to the range and distribution of consensus values; heavily skewed or truncated distributions may produce misleading AUC comparisons.

## Evidence

- [other] perform hierarchical clustering separately on microbe rows and metabolite columns using Euclidean distance and complete linkage with Seaborn's clustermap. 3. For each fixed cluster number k ranging from 2 to 20, generate a k-clustering and compute a consensus matrix by averaging connectivity matrices across all 100 trained models: "For each fixed cluster number k ranging from 2 to 20, generate a k-clustering and compute a consensus matrix by averaging connectivity matrices across all 100 trained models."
- [other] Calculate the cumulative distribution function (CDF) of each consensus matrix and compute the area under the CDF. 5. Determine optimal cluster numbers k₁* (microbes) and k₂* (metabolites) by selecting the largest k where the proportional change in area (Δk) exceeds 0.025 threshold: "Calculate the cumulative distribution function (CDF) of each consensus matrix and compute the area under the CDF. 5. Determine optimal cluster numbers k₁* (microbes) and k₂* (metabolites) by"
- [other] Bicluster the normalized score matrix S* using k₁* and k₂* to assign microbes and metabolites to their final module memberships.: "Bicluster the normalized score matrix S* using k₁* and k₂* to assign microbes and metabolites to their final module memberships."
- [other] Normalize the feature attribution score matrix S_i by dividing by the significant threshold score from background distribution and clip values to range [-1, 1].: "Normalize the feature attribution score matrix S_i by dividing by the significant threshold score from background distribution and clip values to range [-1, 1]."
- [other] identifying 8 modules of microbes and 8 modules of metabolites, with module feature values calculated as the average normalized abundance of members within each module.: "identifying 8 modules of microbes and 8 modules of metabolites, with module feature values calculated as the average normalized abundance of members within each module."
