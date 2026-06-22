---
name: spectral-peak-clustering-gc-ims
description: Use when after peak detection on individual GC-IMS samples, when you need to assign consistent cluster IDs to peaks detected across multiple samples to enable cross-sample comparison and quantification.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - R
  - GCIMS
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
---

# spectral-peak-clustering-gc-ims

## Summary

Cluster detected gas chromatography–ion mobility spectrometry (GC-IMS) peaks across samples using hierarchical clustering with Euclidean distance in drift time and retention time space. This skill groups peaks with similar spatiotemporal coordinates to produce unified peak identities across replicates.

## When to use

After peak detection on individual GC-IMS samples, when you need to assign consistent cluster IDs to peaks detected across multiple samples to enable cross-sample comparison and quantification. Apply this when peaks show drift time and retention time coordinates that should be grouped despite minor instrumental drift or sample variation.

## When NOT to use

- Peaks have not yet been detected or lack drift time and retention time coordinates.
- You require clustering in other feature spaces (e.g., m/z, intensity, shape descriptors) not in drift/retention time.
- Input peaks are from a single sample and no cross-sample alignment is needed.

## Inputs

- peak_list: detected peaks with drift_time (ms) and retention_time (s) coordinates from peak detection step
- dt_cluster_spread_ms: drift time clustering spread threshold (numeric, milliseconds)
- rt_cluster_spread_s: retention time clustering spread threshold (numeric, seconds)

## Outputs

- peak_clustering: object containing peak_list_clustered with cluster ID assignments for each peak
- cluster_stats: summary statistics including median drift time and retention time positions for each cluster

## How to apply

Load peak detection results containing drift time and retention time coordinates for all detected peaks. Apply the clusterPeaks function from GCIMS with distance_method='euclidean', setting dt_cluster_spread_ms=0.1 (drift time tolerance in milliseconds) and rt_cluster_spread_s=20 (retention time tolerance in seconds) to define the spatial threshold for merging peaks into clusters. Use hierarchical clustering (hclust linkage method) to construct dendrograms and assign cluster IDs. Extract the peak_clustering output containing peak_list_clustered (peaks with assigned cluster IDs) and cluster_stats (median cluster positions in drift and retention time). The choice of spread thresholds should reflect expected instrumental drift and peak width variation observed in your sample replicates.

## Related tools

- **GCIMS** (R package providing clusterPeaks function for hierarchical clustering of GC-IMS peaks using Euclidean distance in drift/retention time space) — https://github.com/sipss/GCIMS
- **R** (Statistical computing environment in which GCIMS package executes clustering)

## Examples

```
peak_clustering <- clusterPeaks(peaks, distance_method='euclidean', dt_cluster_spread_ms=0.1, rt_cluster_spread_s=20, linkage_method='hclust')
```

## Evaluation signals

- peak_list_clustered contains no null or NA cluster IDs for any detected peak.
- cluster_stats median drift times and retention times fall within the specified dt_cluster_spread_ms and rt_cluster_spread_s ranges of their constituent peaks.
- Peaks within the same cluster have pairwise Euclidean distances ≤ the specified spread thresholds; peaks in different clusters exceed thresholds.
- Cluster membership is reproducible when the same parameters are reapplied to the same peak input.
- Cross-sample consistency: peaks from replicate samples of the same compound are assigned to the same cluster ID.

## Limitations

- Hierarchical clustering with fixed Euclidean distance thresholds may merge distinct peaks if they fall within the spread thresholds, especially when dt_cluster_spread_ms or rt_cluster_spread_s are set too generously.
- The skill assumes peaks from different samples are already in the same drift time and retention time coordinate frame; prior alignment (drift time and retention time alignment) is required.
- Clustering performance depends heavily on the choice of dt_cluster_spread_ms and rt_cluster_spread_s; suboptimal thresholds can lead to over-clustering or under-clustering.

## Evidence

- [intro] clusterPeaks function parameters: "clusterPeaks with euclidean distance, dt_cluster_spread_ms=0.1, rt_cluster_spread_s=20, and hclust method produces peak_clustering output containing peak_list_clustered with cluster IDs and"
- [intro] Function output and structure: "Extract and assign cluster IDs to each peak. 4. Output the peak_clustering result with cluster membership."
- [intro] Workflow context: "Load the peak detection results (peaks with drift time and retention time coordinates). 2. Apply clusterPeaks function from GCIMS with distance_method='euclidean'"
- [intro] Peak clustering step in pipeline: "peak_clustering <- clusterPeaks"
