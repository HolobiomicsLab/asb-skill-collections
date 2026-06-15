---
name: correlation-matrix-heatmap-visualization
description: Use when after computing a correlation matrix (e.g., Pearson correlation across samples) on statistically significant LC-MS features, particularly when you need to inspect hierarchical dendrogram structure, validate cluster assignments from different flattening methods (constant-threshold vs..
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - Python
  - pandas
  - numpy
  - scipy
  - scikit-learn
  - matplotlib
  - scipy.cluster.hierarchy
  - scipy.spatial.distance.pdist / squareform
  - scikit-learn (metrics.adjusted_rand_score, metrics.normalized_mutual_info_score)
  - MamsiStructSearch.get_correlation_clusters()
derived_from:
- doi: 10.1021/acs.analchem.5c01327
  title: mamsi
- doi: 10.1371/journal.pcbi.1011814
  title: ''
evidence_spans:
- MAMSI is a Python framework
- import pandas as pd
- import numpy as np
- scipy
- 'Dependencies: scipy'
- from sklearn.model_selection import train_test_split
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mamsi
    doi: 10.1021/acs.analchem.5c01327
    title: mamsi
  dedup_kept_from: coll_mamsi
schema_version: 0.2.0
---

# correlation-matrix-heatmap-visualization

## Summary

Visualize pairwise correlations among LC-MS features or metabolites as a hierarchical heatmap to identify structural and functional relationships in mass spectrometry datasets. This skill enables rapid detection of feature co-clustering patterns and supports downstream cluster assignment validation.

## When to use

Apply this skill after computing a correlation matrix (e.g., Pearson correlation across samples) on statistically significant LC-MS features, particularly when you need to inspect hierarchical dendrogram structure, validate cluster assignments from different flattening methods (constant-threshold vs. silhouette-optimized), or compare clustering solutions side-by-side before extracting final feature groupings.

## When NOT to use

- Input is a raw, non-normalized feature abundance table (not a correlation matrix): compute correlations first.
- Number of features exceeds ~500–1000 and hierarchical dendrogram becomes visually uninterpretable; consider feature selection or sub-sampling.
- Goal is to identify outlier samples or detect batch effects: use principal component analysis (PCA) or quality-control heatmaps instead.
- Correlation matrix is sparse or contains many missing values; imputation or robust correlation methods should precede visualization.

## Inputs

- Pre-computed correlation matrix (pandas DataFrame or numpy array; typically Pearson correlation of shape n_features × n_features)
- Hierarchical dendrogram object from scipy.cluster.hierarchy or pre-computed linkage matrix
- Cluster assignment labels (pandas Series or numpy array; one label per feature for each flattening method)

## Outputs

- Correlation heatmap with dendrogram (matplotlib Figure or image file, e.g. PNG/PDF)
- Side-by-side comparison figure (if two methods are compared) showing feature IDs, correlation values, and cluster assignments by color
- Agreement metrics table (e.g. adjusted Rand index, normalized mutual information scores between two clustering solutions)

## How to apply

Load a pre-computed correlation matrix and corresponding hierarchical dendrogram from a prior clustering run (e.g., using complete linkage and a fixed threshold such as 0.7). Use matplotlib to render the correlation matrix as a heatmap, overlaying the dendrogram axes to show feature relationships. If comparing two flattening methods (e.g., constant-threshold vs. silhouette optimization), generate side-by-side heatmaps with cluster assignment labels annotated by color or row order. The heatmap serves as a visual validation tool: high-correlation blocks within the same cluster and low-correlation blocks between clusters indicate successful separation. Use agreement metrics (adjusted Rand index, normalized mutual information) computed from cluster labels to quantify dendrogram quality.

## Related tools

- **scipy.cluster.hierarchy** (Compute and manipulate hierarchical dendrograms; used to generate linkage matrices and perform dendrogram flattening with methods='complete')
- **scipy.spatial.distance.pdist / squareform** (Convert correlation matrices to distance matrices and vice versa for dendrogram computation)
- **matplotlib** (Render correlation heatmaps and dendrogram visualizations with customizable color maps and annotations)
- **scikit-learn (metrics.adjusted_rand_score, metrics.normalized_mutual_info_score)** (Compute agreement metrics (adjusted Rand index, normalized mutual information) between two cluster label sets to quantify dendrogram quality)
- **pandas** (Manage and tabulate feature metadata, cluster assignments, and agreement metrics for side-by-side comparison)
- **MamsiStructSearch.get_correlation_clusters()** (Load pre-computed correlation matrix and dendrogram from MAMSI; re-flatten using alternative methods ('silhouette' vs. constant threshold); extract cluster labels for visualization) — https://github.com/kopeckylukas/py-mamsi

## Examples

```
struct.get_correlation_clusters(flat_method='silhouette', max_clusters=11); import matplotlib.pyplot as plt; plt.figure(figsize=(12, 8)); dendrogram_plot = struct.dendrogram; plt.imshow(struct.correlation_matrix, cmap='RdBu_r', aspect='auto'); plt.colorbar(); plt.title('LC-MS Feature Correlation Heatmap'); plt.show()
```

## Evaluation signals

- Heatmap reveals block-diagonal structure: high correlations (warm colors) concentrate within cluster boundaries, low correlations (cool colors) between clusters, indicating successful feature grouping.
- Dendrogram cut line (threshold) visually aligns with data structure: when cut at the chosen height (e.g., 0.7 for constant-threshold method), resulting cluster assignments match the expected feature groupings.
- Agreement metrics (adjusted Rand index ≥ 0.8 and normalized mutual information ≥ 0.8) indicate high consistency between two flattening methods; values < 0.5 suggest substantial differences requiring investigation.
- Feature ID labels and cluster colors on heatmap rows are consistent across replicates: same features are always assigned to the same cluster in both methods.
- Dendrogram structure is stable: minor changes to correlation cutoff threshold produce only small changes in cluster membership, indicating robust clustering.

## Limitations

- Heatmap visualization becomes difficult to interpret when the number of features exceeds ~500 due to crowded row/column labels and small cell sizes; consider hierarchical sub-sampling or feature importance filtering.
- Pearson correlation assumes linear relationships; non-linear associations (e.g. sigmoid-shaped relationships between m/z and retention time) may be missed, potentially misrepresenting structural cluster boundaries.
- Dendrogram flattening is sensitive to the choice of linkage method (complete, average, single, ward) and distance metric; the same correlation matrix can produce different dendrograms, affecting cluster interpretation.
- Missing values in the correlation matrix (e.g. features with zero variance) are not explicitly handled by standard correlation functions; pre-processing should remove or impute such features before visualization.
- Heatmap colors can be misleading if the correlation range is narrow (e.g. all correlations between 0.5–0.7); choose color map scales carefully to avoid false visual clustering.

## Evidence

- [other] Load pre-computed correlation matrix and hierarchical dendrogram from a prior MamsiStructSearch run using constant threshold (cut_threshold=0.7, linkage_method='complete'). Re-flatten the same dendrogram using silhouette-score optimization with max_clusters=11 via the get_correlation_clusters() method with flat_method='silhouette'.: "Load pre-computed correlation matrix and hierarchical dendrogram from a prior MamsiStructSearch run using constant threshold (cut_threshold=0.7, linkage_method='complete'). Re-flatten the same"
- [other] Extract and tabulate cluster assignment labels for all features from both flattening methods. Compute agreement metrics (adjusted Rand index, normalized mutual information) between the two clustering solutions.: "Extract and tabulate cluster assignment labels for all features from both flattening methods. Compute agreement metrics (adjusted Rand index, normalized mutual information) between the two clustering"
- [other] Generate a side-by-side comparison table showing feature IDs, constant-threshold cluster ID, silhouette-optimized cluster ID, and agreement status.: "Generate a side-by-side comparison table showing feature IDs, constant-threshold cluster ID, silhouette-optimized cluster ID, and agreement status."
- [readme] the MAMSI framework provides a platform for linking statistically significant features of untargeted multi-assay liquid chromatography – mass spectrometry (LC-MS) metabolomics datasets into clusters defined by their structural properties based on mass-to-charge ratio (m/z) and retention time (RT).: "the MAMSI framework provides a platform for linking statistically significant features of untargeted multi-assay LC-MS metabolomics datasets into clusters defined by structural properties based on"
- [readme] You can find all MAMSI tutorials by visiting our MAMSI Tutorials repository. To import and instantiate the package objects, you can follow this quickstart guide: "You can find all MAMSI tutorials by visiting our MAMSI Tutorials repository"
