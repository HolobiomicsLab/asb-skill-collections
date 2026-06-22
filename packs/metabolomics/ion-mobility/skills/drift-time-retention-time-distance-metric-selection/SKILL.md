---
name: drift-time-retention-time-distance-metric-selection
description: Use when after peak detection in GCIMS when you need to group detected peaks across multiple samples into reproducible clusters.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0625
  tools:
  - R
  - GCIMS
  techniques:
  - GC-MS
  - ion-mobility-MS
derived_from:
- doi: 10.1016/j.chemolab.2023.104938
  title: GCIMS
evidence_spans:
- library(ggplot2) library(cowplot) library(GCIMS)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_gcims_cq
    doi: 10.1016/j.chemolab.2023.104938
    title: GCIMS
  dedup_kept_from: coll_gcims_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1016/j.chemolab.2023.104938
  all_source_dois:
  - 10.1016/j.chemolab.2023.104938
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# drift-time-retention-time-distance-metric-selection

## Summary

Select and apply an appropriate distance metric (Euclidean, Manhattan, etc.) for hierarchical clustering of Gas Chromatography–Ion Mobility Spectrometry peaks in two-dimensional drift time and retention time space. This choice directly affects cluster assignments and reproducibility across samples with similar chromatographic and ion-mobility profiles.

## When to use

After peak detection in GCIMS when you need to group detected peaks across multiple samples into reproducible clusters. Use this skill when peaks have drift time and retention time coordinates and you want to assign cluster IDs based on spatial proximity in the drift-time/retention-time plane, especially when validating reproducibility of peak assignments under specified drift time spread (e.g., dt_cluster_spread_ms=0.1) and retention time spread (e.g., rt_cluster_spread_s=20) thresholds.

## When NOT to use

- Peaks have not yet been detected; apply peak detection first.
- You already have pre-assigned cluster memberships or aligned peaks from external software; use a metric-selection skill only if re-clustering is required.
- Drift time and retention time coordinates are on vastly different scales and you have not normalized them; consider standardizing dimensions before metric selection.

## Inputs

- peak_list (detected peaks with drift_time and retention_time coordinates)
- drift_time coordinate values (in milliseconds)
- retention_time coordinate values (in seconds)

## Outputs

- peak_clustering (hierarchical clustering result)
- peak_list_clustered (peaks with assigned cluster IDs)
- cluster_stats (median cluster positions in drift–retention space)

## How to apply

Choose a distance metric appropriate to your peak coordinate system; Euclidean distance is standard for continuous drift-time and retention-time dimensions when both axes carry equal importance. Pass the selected distance_method parameter (e.g., 'euclidean') to the clusterPeaks function in GCIMS alongside your drift time and retention time spread thresholds and linkage method (e.g., hclust). The metric determines how distances between peaks are computed before hierarchical clustering; Euclidean distance is preferred when drift time (in milliseconds) and retention time (in seconds) coordinates should be treated as orthogonal dimensions with comparable scaling. Verify that the resulting peak_clustering output with cluster IDs and cluster_stats shows consistent median cluster positions across repeated runs or multiple samples.

## Related tools

- **GCIMS** (R package providing clusterPeaks function with distance_method parameter for hierarchical clustering of peaks in drift–retention time space) — https://github.com/sipss/GCIMS
- **R** (Statistical programming language in which GCIMS and hierarchical clustering functions are implemented)

## Examples

```
peak_clustering <- clusterPeaks(peaks, distance_method='euclidean', dt_cluster_spread_ms=0.1, rt_cluster_spread_s=20, linkage_method='hclust')
```

## Evaluation signals

- Cluster assignments are reproducible across independent runs with the same distance metric and parameters.
- peak_list_clustered contains cluster IDs for all detected peaks with no missing values.
- cluster_stats median positions fall within expected ranges given dt_cluster_spread_ms and rt_cluster_spread_s thresholds.
- Clusters show spatial coherence in the drift–retention time plane; intra-cluster variance is smaller than inter-cluster variance.
- Comparison of cluster memberships across multiple samples shows expected alignment when samples contain the same compounds.

## Limitations

- Euclidean distance assumes drift time and retention time are on compatible scales; pressure and temperature fluctuations as well as column degradation cause misalignments in both dimensions, potentially requiring alignment preprocessing before clustering.
- Distance metric choice alone does not account for missing signals (e.g., compounds absent in some samples), which may necessitate post-hoc filtering or annotation steps.
- Hierarchical clustering with a fixed distance metric may not capture multi-scale structure if drift time or retention time precision varies across the chromatogram or between instruments.

## Evidence

- [intro] Euclidean distance metric selection for peak clustering: "clusterPeaks with euclidean distance, dt_cluster_spread_ms=0.1, rt_cluster_spread_s=20, and hclust method produces peak_clustering output containing peak_list_clustered with cluster IDs and"
- [intro] Misalignment motivates careful coordinate-space design: "Pressure and temperature fluctuations as well as degradation of the chromatographic column are some of the causes of misalignments in the data, both in retention and drift time"
- [intro] clusterPeaks function applies distance metric to peak coordinates: "Apply clusterPeaks function from GCIMS with distance_method='euclidean', dt_cluster_spread_ms=0.1, rt_cluster_spread_s=20, and hclust linkage method"
