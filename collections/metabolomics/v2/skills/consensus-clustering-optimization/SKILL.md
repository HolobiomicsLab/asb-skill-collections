---
name: consensus-clustering-optimization
description: Use when when you have a feature attribution matrix (e.g., microbe-metabolite interaction scores) from ensemble neural network training and need to group rows and columns into functionally coherent modules without pre-specifying cluster numbers.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3697
  - http://edamontology.org/topic_3174
  - http://edamontology.org/topic_0769
  tools:
  - Seaborn clustermap
  - Hierarchical clustering (Euclidean distance, complete linkage)
  - Consensus clustering
  - Python
  - Cytoscape
  - scikit-learn hierarchical clustering
  - scipy spatial
  - Python numpy/pandas
derived_from:
- doi: 10.1371/journal.pcbi.1009021
  title: MiMeNet
evidence_spans:
- linkage using Seaborn’s clustermap function in
- cluster microbes (rows) and metabolites (columns) separately based on the Euclidean distance and complete linkage
- for each fixed k, ranged from 2 to 20, a k-clustering of the rows using each normalized S was generated. Then a consensus matrix M(k) was calculated as the mean connectivity matrix across all
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

# Consensus Clustering Optimization

## Summary

Determine optimal cluster numbers for hierarchical clustering by computing consensus matrices across multiple trained models and selecting the cluster count where the proportional change in area under the cumulative distribution function (CDF) exceeds a stability threshold. This stabilizes cluster assignments and reduces model-specific artifacts in microbe-metabolite functional module discovery.

## When to use

When you have a feature attribution matrix (e.g., microbe-metabolite interaction scores) from ensemble neural network training and need to group rows and columns into functionally coherent modules without pre-specifying cluster numbers. Use this when you want robustness against single-model clustering instability and seek data-driven determination of the number of biological modules.

## When NOT to use

- Input data is already manually assigned to pre-defined biological categories or functional hierarchies; use consensus clustering for de novo discovery, not validation of known partitions.
- You have only one trained model; consensus clustering requires aggregation across multiple models to distinguish signal from model-specific noise.
- The feature attribution matrix is sparse or highly imbalanced; clustering stability may be compromised and Δk thresholds may need dataset-specific tuning.

## Inputs

- Feature attribution score matrices S_i (one per trained model) with shape [num_microbes × num_metabolites]
- Set of trained neural network models (≥10 recommended for stable consensus)

## Outputs

- Optimal cluster number k₁* for microbes
- Optimal cluster number k₂* for metabolites
- Consensus clustering matrix averaged across all models
- CDF curve and area plot for k = 2 to 20
- Final microbe module assignments (microbes × module_id)
- Final metabolite module assignments (metabolites × module_id)

## How to apply

Train multiple models (e.g., 100 neural networks via cross-validation) and extract the feature attribution score matrix from each. For each candidate cluster number k from 2 to 20, perform hierarchical clustering (Euclidean distance, complete linkage) on rows and columns separately, and record the connectivity matrix (which samples cluster together). Average the connectivity matrices across all trained models to create a consensus matrix. Calculate the cumulative distribution function (CDF) of each consensus matrix and compute the area under the curve. Plot the area as a function of k and identify the largest k where the proportional change in area (Δk) exceeds the stability threshold (typically 0.025). Use these optimal k values to perform final biclustering on the normalized and clipped attribution score matrix, assigning microbes and metabolites to their definitive module memberships.

## Related tools

- **Seaborn clustermap** (Perform hierarchical clustering on attribution matrix rows and columns and visualize consensus dendrograms) — https://seaborn.pydata.org/
- **scikit-learn hierarchical clustering** (Compute hierarchical clustering linkage using Euclidean distance and complete linkage strategy) — https://scikit-learn.org/stable/modules/generated/sklearn.cluster.AgglomerativeClustering.html
- **scipy spatial** (Calculate pairwise distances and manage connectivity matrices for consensus computation) — https://docs.scipy.org/doc/scipy/reference/spatial.html
- **Python numpy/pandas** (Perform matrix arithmetic (averaging connectivity matrices, CDF calculation, area under curve computation))
- **Cytoscape** (Visualize the final module-based interaction network derived from optimal cluster assignments) — https://cytoscape.org/

## Examples

```
# Pseudocode for consensus clustering optimization on MiMeNet attribution matrices
# Input: list of 100 S_i matrices (one per trained model), each shape [163 microbes × 1000 metabolites]
from scipy.cluster.hierarchy import linkage, dendrogram
from scipy.spatial.distance import pdist, squareform
import numpy as np

k_range = range(2, 21)
connectivity_matrices = []

for k in k_range:
    consensus = np.zeros_like(S_i[0])  # Initialize consensus matrix
    for S in S_i:  # S_i: list of 100 models
        Z_rows = linkage(pdist(S, metric='euclidean'), method='complete')
        clusters = dendrogram(Z_rows, no_plot=True)['leaves']
        # Build connectivity from clustering...
        connectivity_matrices.append(consensus / len(S_i))

# Compute CDF and area for each k, select k* where Δk > 0.025
areas = [np.trapz(np.sort(np.diag(C))) for C in connectivity_matrices]
delta_areas = np.diff(areas)
k_optimal = np.where(delta_areas > 0.025)[0][-1] + 2
```

## Evaluation signals

- Δk curve exhibits a clear elbow or plateau region, indicating stability; the selected k* should correspond to the last k where Δk > 0.025 threshold is satisfied.
- Consensus matrix shows high diagonal block structure (block-diagonal connectivity) at optimal k, meaning microbes/metabolites within modules cluster consistently across models and between-module links are weak.
- Module membership assignments are deterministic and reproducible: re-running consensus with the same trained models and same k* yields identical cluster labels (up to permutation).
- Biological validation: modules identified at k* show significant enrichment for sample-level covariates (e.g., disease status) when tested via Wilcoxon rank-sum test (p < 0.05).
- Qualitative inspection: microbes and metabolites within each module share interpretable functional or metabolic relationships, evidenced by known metabolic pathways or co-occurrence patterns in literature.

## Limitations

- Consensus clustering assumes that multiple independent model trainings are available; methods requiring only a single model (e.g., gap statistic) may be more efficient but less robust to model-specific artifacts.
- The choice of Δk threshold (0.025) is empirical and may require tuning for datasets with different properties (e.g., longitudinal or sparse data may exhibit higher background noise, requiring higher threshold).
- Hierarchical clustering is sensitive to outliers and extreme feature values; normalization and clipping of attribution scores to [−1, 1] partially mitigate this but may not be sufficient for all datasets.
- Computational cost scales with number of models (M), cluster range (k_max − k_min), and matrix size; consensus over 100 models with k up to 20 and large matrices (>1000 features) may be slow.
- Not all features may have strong microbe-metabolite associations; presence of weakly associated or spurious features can inflate optimal k and reduce module interpretability.

## Evidence

- [methods] Perform hierarchical clustering separately on microbe rows and metabolite columns using Euclidean distance and complete linkage with Seaborn's clustermap.: "Perform hierarchical clustering separately on microbe rows and metabolite columns using Euclidean distance and complete linkage with Seaborn's clustermap"
- [methods] For each fixed cluster number k ranging from 2 to 20, generate a k-clustering and compute a consensus matrix by averaging connectivity matrices across all 100 trained models.: "For each fixed cluster number k ranging from 2 to 20, generate a k-clustering and compute a consensus matrix by averaging connectivity matrices across all 100 trained models"
- [methods] Calculate the cumulative distribution function (CDF) of each consensus matrix and compute the area under the CDF.: "Calculate the cumulative distribution function (CDF) of each consensus matrix and compute the area under the CDF"
- [methods] Determine optimal cluster numbers k₁* (microbes) and k₂* (metabolites) by selecting the largest k where the proportional change in area (Δk) exceeds 0.025 threshold.: "Determine optimal cluster numbers k₁* (microbes) and k₂* (metabolites) by selecting the largest k where the proportional change in area (Δk) exceeds 0.025 threshold"
- [results] MiMeNet then trains multiple network models using 10-fold cross-validation: "MiMeNet then trains multiple network models using 10-fold cross-validation"
- [abstract] identifying 8 modules of microbes and 8 modules of metabolites, with module feature values calculated as the average normalized abundance of members within each module: "identifying 8 modules of microbes and 8 modules of metabolites, with module feature values calculated as the average normalized abundance of members within each module"
