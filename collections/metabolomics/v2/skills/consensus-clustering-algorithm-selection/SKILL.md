---
name: consensus-clustering-algorithm-selection
description: Use when when you have computed hierarchical clustering dendrograms on
  your feature matrix (microbes or metabolites) using Euclidean distance and complete
  linkage, and need to determine how many clusters to cut the dendrogram into.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3307
  - http://edamontology.org/topic_0080
  tools:
  - WGCNA
  - Seaborn clustermap
  - Cytoscape
  - Python scikit-learn
  - scikit-learn
  - SciPy
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

# Consensus-clustering algorithm selection

## Summary

Selects the optimal number of clusters (k) in hierarchical consensus clustering by computing cumulative distribution function (CDF) area across a range of k values and identifying the largest k where the proportional change in area (Δk) exceeds a predefined threshold. This prevents overfitting and ensures stable, reproducible cluster assignments across multiple random initializations.

## When to use

When you have computed hierarchical clustering dendrograms on your feature matrix (microbes or metabolites) using Euclidean distance and complete linkage, and need to determine how many clusters to cut the dendrogram into. Use this skill when the optimal k is unknown a priori and you want an automated, data-driven selection criterion rather than manual visual inspection or arbitrary fixed k values.

## When NOT to use

- When you already have strong domain knowledge specifying the expected number of functional modules—use that fixed k instead.
- When the input feature matrix is very small (< 20 features)—consensus clustering gains robustness from many resamples, which is less effective on tiny inputs.
- When hierarchical clustering has not yet been performed or you are using a different distance metric (e.g., Manhattan, correlation) without validating that consensus clustering is appropriate for that metric.

## Inputs

- Hierarchical clustering dendrogram (from Euclidean distance and complete linkage)
- Normalized feature matrix (rows = features, columns = samples or vice versa; values in [-1, 1] range)
- Range of candidate k values (typically 2 to 20)

## Outputs

- Selected optimal k value (k* for microbes or k** for metabolites)
- CDF area curve across k values
- Δk curve (proportional change in CDF area)
- Cluster membership vector assigning each feature to one of k* clusters

## How to apply

After performing hierarchical clustering on normalized feature attribution scores (or any normalized matrix), apply consensus clustering with k ranging from 2 to 20 (or appropriate upper bound). For each k, compute the cumulative distribution function of the consensus matrix and calculate its area. Then compute Δk, the proportional change in area between consecutive k values. Select k* as the largest k where Δk exceeds a 0.025 threshold. This threshold balances detecting meaningful cluster structure while avoiding oversplitting; lower thresholds (e.g., 0.01) produce larger k, higher thresholds produce smaller k. The rationale is that true cluster structure produces sharp increases in CDF area at the correct k, whereas spurious clusters produce diminishing gains.

## Related tools

- **scikit-learn** (Computes hierarchical clustering (linkage, dendrogram) and performs consensus clustering via AgglomerativeClustering or custom consensus matrix construction) — https://scikit-learn.org
- **WGCNA** (Alternative hierarchical clustering and module detection method for comparison; uses dynamic tree cutting instead of fixed k)
- **SciPy** (Provides scipy.cluster.hierarchy for linkage and dendrogram visualization) — https://scipy.org

## Examples

```
from sklearn.cluster import AgglomerativeClustering; from scipy.cluster.hierarchy import linkage, dendrogram; import numpy as np; Z = linkage(normalized_scores, method='complete', metric='euclidean'); areas = []; deltas = []; [areas.append(consensus_area(normalized_scores, k)) for k in range(2, 21)]; [deltas.append((areas[i+1] - areas[i])/areas[i] if areas[i] > 0 else 0) for i in range(len(areas)-1)]; k_star = max([k for k, delta in enumerate(deltas, start=2) if delta > 0.025])
```

## Evaluation signals

- Δk curve is monotonically decreasing (proportional gains should diminish with increasing k)
- Selected k* is within the tested range [2, 20] and corresponds to the largest k satisfying Δk > threshold
- CDF area increases monotonically with k (no non-monotonic jumps in the area curve)
- Cluster membership vector contains no empty clusters and assigns each input feature to exactly one cluster
- Repeating consensus clustering on subsampled data (e.g., 80% of features) recovers similar k*, indicating stability

## Limitations

- The 0.025 threshold for Δk is heuristic and may require tuning for datasets with different sizes or distributions; the article does not provide sensitivity analysis or justification for this specific value.
- Consensus clustering is computationally expensive (requires many hierarchical clustering runs on resampled matrices); scaling to very high-dimensional inputs (> 10,000 features) may be prohibitive.
- The method assumes that true cluster structure produces a sharp 'elbow' in the CDF area curve; if biological modules have overlapping or soft boundaries, consensus clustering may force an artificial hard partition.
- Selection of k is sensitive to the hierarchical clustering linkage method (complete, average, ward) and distance metric; the article uses only Euclidean distance and complete linkage, not validated on other metrics.

## Evidence

- [methods] Δk proportional change criterion: "calculate cumulative distribution function area for each k and select k* as the largest k where Δk (proportional change in area) exceeds 0.025 threshold"
- [methods] Consensus clustering procedure: "Perform hierarchical clustering on normalized attribution scores using Euclidean distance and complete linkage, then apply consensus clustering with k ranging from 2 to 20"
- [methods] Repeat for second dimension: "Repeat consensus clustering for metabolites to identify k** using the same Δk threshold criterion"
- [methods] Biclustering output: "Bicluster the normalized score matrix using k* and k** to partition rows (microbes) and columns (metabolites) into final functional modules"
- [readme] README consensus clustering application: "Number of cross-validated folds (Recommend at least 5). The provided command will run MiMeNet on the IBD dataset and store results in the directory _results/output_dir_."
