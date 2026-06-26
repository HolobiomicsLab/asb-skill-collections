---
name: hierarchical-clustering-dendrogram-interpretation
description: Use when you have a pre-computed hierarchical dendrogram from correlation-based
  clustering of LC-MS features (with fixed linkage criterion and distance metric)
  and need to decide whether a single constant-threshold cut or data-driven silhouette
  optimization better resolves the underlying cluster.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - pandas
  - numpy
  - scipy
  - scikit-learn
  - matplotlib
  - MamsiStructSearch
  - MamsiStructSearch.get_correlation_clusters()
  - scikit-learn.metrics.adjusted_rand_score
  - scikit-learn.metrics.normalized_mutual_info_score
  - scipy.cluster.hierarchy (linkage, dendrogram, fcluster)
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
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
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mamsi
    doi: 10.1021/acs.analchem.5c01327
    title: mamsi
  dedup_kept_from: coll_mamsi
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c01327
  all_source_dois:
  - 10.1021/acs.analchem.5c01327
  - 10.1371/journal.pcbi.1011814
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Hierarchical-Clustering Dendrogram Interpretation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Compare and evaluate alternative dendrogram flattening strategies (constant-threshold versus silhouette-score optimization) to determine structural cluster assignments for LC-MS features, assessing agreement between methods to validate cluster stability.

## When to use

You have a pre-computed hierarchical dendrogram from correlation-based clustering of LC-MS features (with fixed linkage criterion and distance metric) and need to decide whether a single constant-threshold cut or data-driven silhouette optimization better resolves the underlying cluster structure. Use this skill when the choice of flattening method could materially affect downstream interpretation of structural relationships (e.g., isotopologue grouping, adduct annotation) or when comparing results across different analysis parameters.

## When NOT to use

- Input is not a pre-computed dendrogram or linkage matrix; if hierarchical clustering has not yet been performed, run clustering first.
- Features have not yet been selected for statistical significance (e.g., p > 0.05 not yet filtered); dendrogram interpretation is most meaningful on curated feature sets.
- Flattening method choice is dictated by downstream tools or consortia standards (e.g., a published protocol specifies constant threshold=X); comparing methods is unnecessary.

## Inputs

- Pre-computed scipy.cluster.hierarchy dendrogram object (or linkage matrix and feature distance matrix)
- Feature metadata table (feature IDs, m/z, retention time, assay name)
- Constant-threshold flattening parameters (cut_threshold value, e.g., 0.7)
- Silhouette flattening parameters (max_clusters value, e.g., 11)

## Outputs

- Cluster assignment vector from constant-threshold method (feature ID → cluster label)
- Cluster assignment vector from silhouette-score method (feature ID → cluster label)
- Agreement metrics table (adjusted Rand index, normalized mutual information, contingency matrix)
- Side-by-side comparison DataFrame (feature ID, constant-threshold cluster, silhouette cluster, agreement boolean/score)

## How to apply

Load a pre-computed correlation matrix and dendrogram from a prior MamsiStructSearch run using a fixed linkage method (e.g., complete linkage) and constant threshold (e.g., cut_threshold=0.7). Re-flatten the same dendrogram using silhouette-score optimization via get_correlation_clusters(flat_method='silhouette', max_clusters=11) to generate an alternative clustering solution. Extract cluster assignment labels for all features from both methods and compute agreement metrics—adjusted Rand index and normalized mutual information—using scikit-learn to quantify concordance. Generate a side-by-side comparison table annotating feature IDs, constant-threshold cluster labels, silhouette-optimized cluster labels, and agreement status. High agreement (ARI > 0.7, NMI > 0.7) suggests robust clustering; lower agreement indicates sensitivity to flattening strategy and warrants investigation of which method's partitioning better aligns with domain expectations (e.g., retention-time cohesion, adduct consistency).

## Related tools

- **MamsiStructSearch.get_correlation_clusters()** (Flattens pre-computed dendrogram using specified method (constant threshold or silhouette); returns cluster assignments for all features) — https://github.com/kopeckylukas/py-mamsi
- **scikit-learn.metrics.adjusted_rand_score** (Computes adjusted Rand index to quantify agreement between two clustering solutions)
- **scikit-learn.metrics.normalized_mutual_info_score** (Computes normalized mutual information to measure shared information between two partitions)
- **scipy.cluster.hierarchy (linkage, dendrogram, fcluster)** (Underlying hierarchical clustering and dendrogram manipulation; used by MamsiStructSearch)
- **pandas** (Tabulation and comparison of cluster labels; construction of feature-to-cluster mapping tables)
- **matplotlib** (Visualization of dendrograms and agreement metrics)

## Examples

```
from mamsi.mamsi_struct_search import MamsiStructSearch
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score
import pandas as pd

struct = MamsiStructSearch()
struct.load_lcms(selected_features)
const_clusters = struct.get_correlation_clusters(flat_method='constant', cut_threshold=0.7)
silh_clusters = struct.get_correlation_clusters(flat_method='silhouette', max_clusters=11)
ari = adjusted_rand_score(const_clusters, silh_clusters)
nmi = normalized_mutual_info_score(const_clusters, silh_clusters)
comparison = pd.DataFrame({'feature_id': selected_features.index, 'const_cluster': const_clusters, 'silhouette_cluster': silh_clusters, 'ari': ari, 'nmi': nmi})
```

## Evaluation signals

- Adjusted Rand index (ARI) and normalized mutual information (NMI) are both > 0.7, indicating high agreement and suggesting either method is robust; ARI/NMI < 0.5 indicates substantial divergence warranting manual inspection of conflicting assignments.
- Contingency matrix between the two clusterings shows block-diagonal structure (high diagonal counts, low off-diagonal), reflecting strong label concordance.
- Cluster size distributions are similar between methods (Kolmogorov–Smirnov test on cluster cardinalities); large discrepancies suggest one method produces singleton clusters or imbalanced partitions.
- Structural properties are preserved within clusters: features assigned to the same cluster by both methods show consistent retention-time proximity (< 5 seconds window) and/or matching neutral masses after adduct correction (within 15 ppm).
- Features with discordant assignments (assigned to different clusters by the two methods) are manually reviewed; if they form plausible structural links (e.g., same adduct, same RT window, nearby m/z), dendrogram flattening choice is reconsidered.

## Limitations

- Comparison is restricted to dendrograms produced by the same linkage criterion and distance metric; different linkage methods (complete, average, ward) will produce structurally different trees and comparing flattening of two trees is not meaningful.
- Silhouette-score optimization is sensitive to the choice of max_clusters hyperparameter; different values may yield different optimal partitions. The skill assumes max_clusters is fixed a priori (e.g., 11) based on domain knowledge or prior exploration.
- Agreement metrics (ARI, NMI) are symmetric and do not distinguish which method's cluster assignments are more biologically/chemically meaningful; high disagreement does not automatically imply poor clustering, only that the methods partition differently. Manual validation against known structural relationships (isotopologues, adducts) is necessary.
- Dendrogram interpretation assumes features are already filtered to statistically significant features; unfiltered noisy features may inflate cluster numbers and obscure structural signal.
- Method is specific to correlation-based clustering of LC-MS features; applicability to other distance metrics, clustering algorithms, or data types (genomics, proteomics, etc.) requires re-validation of parameter ranges and agreement thresholds.

## Evidence

- [other] Load pre-computed correlation matrix and hierarchical dendrogram from a prior MamsiStructSearch run using constant threshold (cut_threshold=0.7, linkage_method='complete'). Re-flatten the same dendrogram using silhouette-score optimization with max_clusters=11 via the get_correlation_clusters() method with flat_method='silhouette'.: "Load pre-computed correlation matrix and hierarchical dendrogram from a prior MamsiStructSearch run using constant threshold (cut_threshold=0.7, linkage_method='complete'). Re-flatten the same"
- [other] Extract and tabulate cluster assignment labels for all features from both flattening methods. Compute agreement metrics (adjusted Rand index, normalized mutual information) between the two clustering solutions.: "Extract and tabulate cluster assignment labels for all features from both flattening methods. Compute agreement metrics (adjusted Rand index, normalized mutual information) between the two clustering"
- [other] Generate a side-by-side comparison table showing feature IDs, constant-threshold cluster ID, silhouette-optimized cluster ID, and agreement status.: "Generate a side-by-side comparison table showing feature IDs, constant-threshold cluster ID, silhouette-optimized cluster ID, and agreement status."
- [other] Does the silhouette flattening method produce different structural cluster assignments compared to the default constant-threshold method in the MAMSI structural clustering pipeline?: "Does the silhouette flattening method produce different structural cluster assignments compared to the default constant-threshold method in the MAMSI structural clustering pipeline?"
- [readme] Further, you can use the `MamsiStrustSearch.get_correlation_clusters()` method to find correlation clusters.: "Further, you can use the `MamsiStrustSearch.get_correlation_clusters()` method to find correlation clusters."
