---
name: silhouette-analysis-threshold-optimization
description: Use when when you have a pre-computed hierarchical dendrogram from structural
  clustering (e.g., of LC-MS features based on m/z and retention time) and want to
  compare or validate the cluster assignments produced by a fixed constant-threshold
  method.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0621
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - pandas
  - numpy
  - scipy
  - scikit-learn
  - matplotlib
  - MAMSI (Multi-Assay Mass Spectrometry Integration)
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

# silhouette-analysis-threshold-optimization

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Replace fixed dendrogram-flattening thresholds with silhouette-score optimization to derive data-driven cluster assignments. This skill evaluates hierarchical clustering solutions by maximizing silhouette coefficients, yielding structural cluster assignments that adapt to the intrinsic cohesion and separation of LC-MS feature groups rather than relying on arbitrary cutoff values.

## When to use

When you have a pre-computed hierarchical dendrogram from structural clustering (e.g., of LC-MS features based on m/z and retention time) and want to compare or validate the cluster assignments produced by a fixed constant-threshold method. Use this skill to assess whether silhouette-optimized flattening yields meaningfully different or more robust cluster solutions, especially when the constant-threshold choice (e.g., cut_threshold=0.7) is arbitrary or domain-specific.

## When NOT to use

- Input dendrogram was not pre-computed from a complete run; silhouette optimization requires a stable dendrogram to re-flatten.
- You do not have a prior constant-threshold clustering result for comparison; silhouette optimization alone without a baseline makes agreement assessment impossible.
- Feature dataset is very small (< 20 features) or highly imbalanced in cluster sizes; silhouette scores may be unstable and max_clusters may exceed meaningful granularity.

## Inputs

- pre-computed correlation matrix (from hierarchical clustering run)
- hierarchical dendrogram object (from prior MamsiStructSearch run with constant threshold)
- LC-MS feature dataset with feature IDs, m/z, and retention time values
- constant-threshold cluster assignments (from prior flattening)

## Outputs

- silhouette-optimized cluster assignment labels for all features
- adjusted Rand index and normalized mutual information agreement metrics
- side-by-side comparison table (feature ID, constant-threshold cluster ID, silhouette cluster ID, agreement status)
- silhouette coefficient scores for each cluster (quality metric)

## How to apply

Load the pre-computed correlation matrix and dendrogram from a prior hierarchical clustering run (e.g., using linkage_method='complete'). Re-flatten the same dendrogram using silhouette-score optimization by calling the get_correlation_clusters() method with flat_method='silhouette' and specify a maximum number of clusters (e.g., max_clusters=11) to constrain the search space. Extract cluster assignment labels for all features from both the constant-threshold and silhouette-optimized solutions. Compute agreement metrics between the two clustering solutions using adjusted Rand index (ARI) and normalized mutual information (NMI) to quantify concordance. Generate a side-by-side comparison table showing feature IDs, constant-threshold cluster ID, silhouette-optimized cluster ID, and agreement status to identify features whose cluster membership differs and interpret the impact on downstream structural interpretation.

## Related tools

- **MAMSI (Multi-Assay Mass Spectrometry Integration)** (Python framework housing the MamsiStructSearch.get_correlation_clusters() method with flat_method='silhouette' parameter for silhouette-optimized dendrogram flattening) — https://github.com/kopeckylukas/py-mamsi
- **scikit-learn** (Provides silhouette_score() and related clustering metrics (adjusted_rand_score, normalized_mutual_info_score) for agreement and cluster quality evaluation)
- **scipy** (Supplies hierarchical clustering (linkage, dendrogram) and distance computations for dendrogram structure)
- **pandas** (Data frame manipulation for tabulating and comparing cluster assignments across methods)
- **numpy** (Numerical array operations for extracting and masking cluster labels)

## Examples

```
struct.get_correlation_clusters(flat_method='silhouette', max_clusters=11)
```

## Evaluation signals

- Silhouette scores for each cluster in the optimized solution are all non-negative and ideally > 0.5, indicating well-separated and cohesive clusters.
- Adjusted Rand index between constant-threshold and silhouette-optimized solutions is quantified (ranges 0–1, with 1 = perfect agreement); significant disagreement (ARI < 0.7) warrants investigation of which features switched clusters.
- Normalized mutual information score confirms the degree of information overlap between the two solutions; values closer to 1 indicate higher agreement.
- The comparison table shows no singleton clusters (clusters with only 1 feature) in the silhouette solution, or if they exist, they have negative silhouette scores, indicating potential misclassification.
- Maximum silhouette score across cluster ranges (2 to max_clusters) shows a clear peak, indicating the optimized number of clusters balances granularity and stability.

## Limitations

- Silhouette optimization is sensitive to the choice of max_clusters parameter; setting it too high increases computational cost and may yield spurious fine-grained clusters, while setting it too low may miss meaningful structure.
- The method assumes the dendrogram and correlation matrix remain valid and consistent; re-flattening the same dendrogram does not re-compute correlations, so changes in feature selection or preprocessing require a fresh dendrogram run.
- Silhouette scores favor well-separated, spherical clusters; elongated, chain-like structural clusters (e.g., adduct networks) may receive lower scores despite being scientifically meaningful in LC-MS structural interpretation.
- No changelog is documented for the MAMSI package, making it difficult to track whether the flat_method='silhouette' implementation has been updated or refined across versions.

## Evidence

- [other] Load pre-computed correlation matrix and hierarchical dendrogram from a prior MamsiStructSearch run using constant threshold (cut_threshold=0.7, linkage_method='complete'). Re-flatten the same dendrogram using silhouette-score optimization with max_clusters=11 via the get_correlation_clusters() method with flat_method='silhouette'.: "Load pre-computed correlation matrix and hierarchical dendrogram from a prior MamsiStructSearch run using constant threshold (cut_threshold=0.7, linkage_method='complete'). Re-flatten the same"
- [other] Extract and tabulate cluster assignment labels for all features from both flattening methods. Compute agreement metrics (adjusted Rand index, normalized mutual information) between the two clustering solutions.: "Extract and tabulate cluster assignment labels for all features from both flattening methods. Compute agreement metrics (adjusted Rand index, normalized mutual information) between the two clustering"
- [other] Generate a side-by-side comparison table showing feature IDs, constant-threshold cluster ID, silhouette-optimized cluster ID, and agreement status.: "Generate a side-by-side comparison table showing feature IDs, constant-threshold cluster ID, silhouette-optimized cluster ID, and agreement status."
- [other] MAMSI integrates multi-assay mass spectrometry datasets and clusters statistically significant LC-MS features based on structural properties defined by m/z and retention time.: "MAMSI integrates multi-assay mass spectrometry datasets and clusters statistically significant LC-MS features based on structural properties defined by m/z and retention time."
- [readme] from sklearn.model_selection import train_test_split: "Further, you can use the `MamsiStrustSearch.get_correlation_clusters()` method to find correlation clusters. struct.get_correlation_clusters(flat_method='silhouette', max_clusters=11)"
