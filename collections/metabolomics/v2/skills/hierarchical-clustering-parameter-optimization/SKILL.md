---
name: hierarchical-clustering-parameter-optimization
description: Use when after peak detection in GC-IMS preprocessing, when you need
  to group peaks across multiple samples and must decide whether euclidean distance
  is appropriate for your drift time and retention time coordinate space, and when
  you need to validate that your chosen dt_cluster_spread_ms and.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - R
  - GCIMS
  techniques:
  - GC-MS
  - ion-mobility-MS
  license_tier: restricted
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# hierarchical-clustering-parameter-optimization

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Optimize hierarchical clustering parameters (euclidean distance metric, drift time and retention time spread thresholds) to assign detected GC-IMS peaks to reproducible clusters across samples. This skill determines the correct distance metric and spread tolerances needed to group peaks with similar chromatographic and ion mobility properties.

## When to use

After peak detection in GC-IMS preprocessing, when you need to group peaks across multiple samples and must decide whether euclidean distance is appropriate for your drift time and retention time coordinate space, and when you need to validate that your chosen dt_cluster_spread_ms and rt_cluster_spread_s thresholds produce reproducible, biologically meaningful cluster assignments that can be compared across replicate samples.

## When NOT to use

- Input peaks are already pre-clustered or annotated with compound identity — re-clustering may destroy valid prior assignments.
- Drift time or retention time data have not been aligned across samples — misalignments will confound cluster assignments.
- Sample mixtures contain compounds with overlapping or identical retention and drift times; euclidean distance alone may not resolve them without additional chemical information.

## Inputs

- peak detection results (peaks with drift time and retention time coordinates)
- peak list with drift_time and retention_time attributes

## Outputs

- peak_clustering result object
- peak_list_clustered with cluster IDs assigned to each peak
- cluster_stats with median cluster positions and cluster membership counts

## How to apply

Load peak detection results containing drift time and retention time coordinates for each detected peak. Apply the clusterPeaks function from GCIMS with distance_method='euclidean', setting dt_cluster_spread_ms=0.1 (drift time tolerance in milliseconds) and rt_cluster_spread_s=20 (retention time tolerance in seconds) as initial parameters, and specify hclust as the linkage method. The euclidean distance metric combines drift time and retention time differences into a single dissimilarity measure; the spread thresholds define the maximum within-cluster variance allowed in each dimension. Extract the resulting cluster IDs from peak_list_clustered and inspect cluster_stats (median cluster positions) to verify that clusters are compact and separated. Adjust spread thresholds downward if clusters are too loose (merging distinct compounds) or upward if valid peaks are over-fragmented across clusters.

## Related tools

- **GCIMS** (Provides the clusterPeaks function and peak_clustering data structures for hierarchical clustering with euclidean distance and hclust linkage.) — https://github.com/sipss/GCIMS
- **R** (Execution environment for GCIMS and hierarchical clustering operations.)

## Examples

```
peak_clustering <- clusterPeaks(peaks, distance_method='euclidean', dt_cluster_spread_ms=0.1, rt_cluster_spread_s=20, linkage_method='hclust')
```

## Evaluation signals

- Cluster IDs are assigned consistently to all peaks in peak_list_clustered without missing or invalid values.
- Median cluster positions in cluster_stats fall within the specified spread thresholds (euclidean distance ≤ threshold defined by dt_cluster_spread_ms and rt_cluster_spread_s).
- Cluster assignments are reproducible when re-run on the same peak set and parameters.
- Visual inspection of 2D scatter plots (drift time vs. retention time, colored by cluster ID) shows compact, well-separated clusters without obvious over-merging or fragmentation.
- Cluster sizes are stable across replicate samples; biologically expected compounds appear in the same clusters in replicate injections.

## Limitations

- Euclidean distance assumes drift time and retention time are on commensurate scales; if they differ by orders of magnitude, the metric may be dominated by one dimension and require data normalization.
- Fixed spread thresholds (dt_cluster_spread_ms=0.1, rt_cluster_spread_s=20) may not be optimal for all sample types or chromatographic methods; validation on your specific instrument and column is essential.
- Hierarchical clustering is sensitive to linkage method; the article specifies hclust but does not justify why it is superior to other linkage methods (e.g., complete, average, or Ward) for this application.
- No guidance is provided for tuning spread thresholds a priori; the article shows one successful case (three ketones dataset) but does not describe how to choose thresholds for novel compound mixtures.

## Evidence

- [other] clusterPeaks with euclidean distance, dt_cluster_spread_ms=0.1, rt_cluster_spread_s=20, and hclust method produces peak_clustering output containing peak_list_clustered with cluster IDs and cluster_stats with median cluster positions.: "clusterPeaks with euclidean distance, dt_cluster_spread_ms=0.1, rt_cluster_spread_s=20, and hclust method produces peak_clustering output containing peak_list_clustered with cluster IDs and"
- [other] What are the cluster assignments for detected peaks when using hierarchical clustering with euclidean distance and specified drift time and retention time spread thresholds?: "cluster assignments for detected peaks when using hierarchical clustering with euclidean distance and specified drift time and retention time spread thresholds"
- [other] Load the peak detection results (peaks with drift time and retention time coordinates). 2. Apply clusterPeaks function from GCIMS with distance_method='euclidean', dt_cluster_spread_ms=0.1, rt_cluster_spread_s=20, and hclust linkage method.: "Load the peak detection results (peaks with drift time and retention time coordinates). Apply clusterPeaks function from GCIMS with distance_method='euclidean', dt_cluster_spread_ms=0.1,"
- [readme] GCIMS is an R package implementing a preprocessing pipeline for Gas Chromatography – Ion Mobility Spectrometry samples.: "GCIMS is an R package implementing a preprocessing pipeline for Gas Chromatography – Ion Mobility Spectrometry samples."
- [intro] Pressure and temperature fluctuations as well as degradation of the chromatographic column are some of the causes of misalignments in the data, both in retention and drift time.: "Pressure and temperature fluctuations as well as degradation of the chromatographic column are some of the causes of misalignments in the data, both in retention and drift time."
