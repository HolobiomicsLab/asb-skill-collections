---
name: clustering-solution-comparison-metrics
description: Use when you have applied two different clustering or dendrogram-flattening methods (e.g., constant-threshold vs. silhouette-score optimization) to the same feature set and need to assess whether the two solutions assign features to clusters consistently.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - pandas
  - numpy
  - scipy
  - scikit-learn
  - matplotlib
  - MAMSI (MamsiStructSearch.get_correlation_clusters())
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# clustering-solution-comparison-metrics

## Summary

Compare two hierarchical clustering solutions (e.g., from different flattening methods) using agreement metrics such as adjusted Rand index and normalized mutual information to quantify structural consistency and validate clustering robustness in LC-MS metabolomics feature grouping.

## When to use

You have applied two different clustering or dendrogram-flattening methods (e.g., constant-threshold vs. silhouette-score optimization) to the same feature set and need to assess whether the two solutions assign features to clusters consistently. This is critical when validating whether a new clustering strategy (e.g., silhouette optimization) produces materially different structural assignments compared to an existing pipeline.

## When NOT to use

- Both clustering solutions are identical or derived from the same method and parameters—no comparison is needed.
- You have only one clustering solution and no alternative method to compare against.
- The clustering labels encode different semantic meanings (e.g., one is by structural property, the other by correlation)—agreement metrics assume the same target structure.

## Inputs

- Dendrogram or correlation matrix from hierarchical clustering (from prior run)
- Two sets of cluster assignment labels (e.g., from constant-threshold and silhouette-optimized flattening)
- Feature ID list with corresponding cluster IDs for both solutions

## Outputs

- Adjusted Rand Index (ARI) score
- Normalized Mutual Information (NMI) score
- Side-by-side comparison table (feature ID, cluster A, cluster B, agreement flag)
- Summary statistics on concordance

## How to apply

First, extract cluster assignment labels for all features from both clustering solutions into tabular form (feature ID, cluster ID from method A, cluster ID from method B). Then compute pairwise agreement metrics: adjusted Rand index (ARI) quantifies concordance accounting for chance agreement (range −1 to 1, where 1 indicates perfect agreement), and normalized mutual information (NMI) measures shared information between labelings (range 0 to 1). Generate a side-by-side comparison table flagging each feature's cluster membership in both solutions and whether assignments agree. High agreement (ARI > 0.7, NMI > 0.8) indicates the two methods produce stable, robust cluster structure; low agreement suggests the new method substantially restructures feature groupings and warrants investigation of which structural relationships drive the divergence.

## Related tools

- **scikit-learn** (Provides adjusted_rand_score() and normalized_mutual_info_score() functions for computing agreement metrics between two cluster label arrays) — https://scikit-learn.org
- **pandas** (Used to tabulate and compare cluster assignments side-by-side for each feature) — https://pandas.pydata.org
- **MAMSI (MamsiStructSearch.get_correlation_clusters())** (Produces alternative cluster solutions via flat_method='silhouette' vs. default constant-threshold flattening for comparison) — https://github.com/kopeckylukas/py-mamsi
- **scipy** (Provides utility functions for cluster analysis and dendrogram manipulation) — https://scipy.org

## Examples

```
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score
ari = adjusted_rand_score(clusters_constant, clusters_silhouette)
nmi = normalized_mutual_info_score(clusters_constant, clusters_silhouette)
comparison_df = pd.DataFrame({'feature_id': feature_ids, 'cluster_const': clusters_constant, 'cluster_silhouette': clusters_silhouette, 'agree': clusters_constant == clusters_silhouette})
print(f'ARI: {ari:.3f}, NMI: {nmi:.3f}, Agreement: {comparison_df["agree"].sum() / len(comparison_df):.1%}')
```

## Evaluation signals

- Adjusted Rand Index and Normalized Mutual Information scores are both calculated and reported for the pair of solutions; ARI range −1 to 1 and NMI range 0 to 1 are respected.
- Comparison table includes all features with non-null cluster assignments in both solutions; row count matches the total number of features analyzed.
- Agreement flag is correctly computed (e.g., cluster_A == cluster_B for each feature) and summary statistics (percentage agreement, pairwise concordance) are derived.
- High-agreement scenarios (ARI > 0.7) indicate both methods converge on the same structural grouping; low-agreement scenarios (ARI < 0.3) warrant manual inspection of differing cluster compositions to understand which structural properties drive divergence.
- No missing or NaN values in cluster assignments after flattening; both solutions span the same feature set without loss.

## Limitations

- ARI and NMI assume cluster labels are discrete and comparable; if one solution has more clusters than the other by design, agreement may be artificially low despite overlapping structural relationships.
- These metrics measure label agreement only, not the biological or chemical validity of the clusters; two solutions may agree perfectly but both be incorrect with respect to true metabolite structure.
- The interpretation threshold (e.g., 'ARI > 0.7 = good agreement') is context-dependent; in exploratory studies, even moderate agreement (0.4–0.7) may signal meaningful structural divergence worth investigating.
- If the dendrogram or hierarchical tree is recomputed with different parameters (e.g., different linkage method or distance metric), the base correlation structure may change, confounding comparison of flattening methods alone.

## Evidence

- [other] Extract and tabulate cluster assignment labels for all features from both flattening methods: "Extract and tabulate cluster assignment labels for all features from both flattening methods. 4. Compute agreement metrics (adjusted Rand index, normalized mutual information)"
- [other] Re-flatten the same dendrogram using silhouette-score optimization with max_clusters=11 via the get_correlation_clusters() method: "Re-flatten the same dendrogram using silhouette-score optimization with max_clusters=11 via the get_correlation_clusters() method with flat_method='silhouette'"
- [other] Load pre-computed correlation matrix and hierarchical dendrogram from a prior MamsiStructSearch run: "Load pre-computed correlation matrix and hierarchical dendrogram from a prior MamsiStructSearch run using constant threshold (cut_threshold=0.7, linkage_method='complete')"
- [other] Generate a side-by-side comparison table showing feature IDs and cluster agreement status: "Generate a side-by-side comparison table showing feature IDs, constant-threshold cluster ID, silhouette-optimized cluster ID, and agreement status"
- [other] scikit-learn, scipy provide functions for agreement metrics and dendrogram analysis: "Tools: Python, pandas, numpy, scipy, scikit-learn, matplotlib"
