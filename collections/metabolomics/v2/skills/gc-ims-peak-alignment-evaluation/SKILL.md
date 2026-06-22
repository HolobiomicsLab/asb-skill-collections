---
name: gc-ims-peak-alignment-evaluation
description: Use when after peak detection in GC-IMS preprocessing, when you need to assess whether detected peaks from multiple samples align to the same chemical entities (clusters) using hierarchical clustering.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
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

# GC-IMS Peak Alignment Evaluation

## Summary

Hierarchical clustering of detected peaks in Gas Chromatography–Ion Mobility Spectrometry data using Euclidean distance with specified drift time and retention time thresholds to assign peak cluster memberships and extract cluster statistics. This skill evaluates peak alignment reproducibility across samples by grouping peaks with similar drift time and retention time coordinates.

## When to use

After peak detection in GC-IMS preprocessing, when you need to assess whether detected peaks from multiple samples align to the same chemical entities (clusters) using hierarchical clustering. Apply this skill when you want to reproduce ROI (region of interest) clustering across samples and need cluster assignments with quantified median cluster positions for downstream analysis or validation.

## When NOT to use

- Peak detection has not yet been performed on the GC-IMS dataset; alignment requires detected peak coordinates as input.
- You only have a single sample; clustering is most meaningful for cross-sample reproducibility assessment.
- Input peaks lack both drift time and retention time dimensions; the Euclidean distance metric requires both coordinates.

## Inputs

- peak_detection_results (list containing peaks with drift_time and retention_time coordinates)
- dt_cluster_spread_ms (numeric: drift time spread threshold, e.g., 0.1 ms)
- rt_cluster_spread_s (numeric: retention time spread threshold, e.g., 20 s)

## Outputs

- peak_clustering (list object)
- peak_list_clustered (data frame with peaks annotated by cluster ID)
- cluster_stats (data frame with cluster-level statistics including median drift time and retention time positions)

## How to apply

Load peak detection results containing drift time and retention time coordinates for all detected peaks. Apply the clusterPeaks function from the GCIMS R package with distance_method='euclidean', dt_cluster_spread_ms=0.1 (drift time spread threshold in milliseconds), rt_cluster_spread_s=20 (retention time spread threshold in seconds), and hclust linkage method. The function performs hierarchical clustering and produces peak_clustering output containing peak_list_clustered (peaks annotated with cluster IDs) and cluster_stats (median cluster positions). Verify cluster assignments are consistent by checking that within-cluster peak coordinates do not exceed the specified spread thresholds in either dimension.

## Related tools

- **GCIMS** (R package implementing clusterPeaks function for hierarchical clustering of GC-IMS peaks using Euclidean distance and specified drift/retention time spread thresholds) — https://github.com/sipss/GCIMS
- **R** (Statistical computing environment required to execute GCIMS package and clusterPeaks function)

## Examples

```
peak_clustering <- clusterPeaks(peaks, distance_method='euclidean', dt_cluster_spread_ms=0.1, rt_cluster_spread_s=20, hclust_method='complete')
```

## Evaluation signals

- All peaks in peak_list_clustered have assigned cluster IDs (no missing values).
- Cluster_stats contains median drift time and retention time positions for each cluster; these medians fall within the observed peak coordinate ranges.
- Within-cluster pairwise Euclidean distances (computed from drift time and retention time) do not exceed the specified thresholds (dt_cluster_spread_ms=0.1, rt_cluster_spread_s=20) after accounting for coordinate scaling.
- Cluster membership is reproducible: re-running clusterPeaks with identical parameters on the same input peaks produces identical cluster assignments.
- Number of clusters is reasonable relative to total number of detected peaks (suggests meaningful grouping, not over-fragmentation).

## Limitations

- Euclidean distance assumes drift time and retention time are commensurable after scaling; the fixed thresholds may need adjustment if instrumentation or experimental conditions change.
- Hierarchical clustering with hclust linkage method depends on the choice of linkage criterion (e.g., complete, average); the article specifies hclust but does not detail which linkage method is used by default.
- Pressure and temperature fluctuations as well as chromatographic column degradation can cause drift time and retention time misalignments that precede peak detection; clustering cannot correct pre-detection misalignments.
- The skill requires well-separated peaks; overlapping or co-eluting peaks may be incorrectly clustered if they fall within the spread thresholds.

## Evidence

- [other] What are the cluster assignments for detected peaks when using hierarchical clustering with euclidean distance and specified drift time and retention time spread thresholds?: "research_question: What are the cluster assignments for detected peaks when using hierarchical clustering with euclidean distance and specified drift time and retention time spread thresholds?"
- [other] clusterPeaks with euclidean distance, dt_cluster_spread_ms=0.1, rt_cluster_spread_s=20, and hclust method produces peak_clustering output containing peak_list_clustered with cluster IDs and cluster_stats with median cluster positions.: "clusterPeaks with euclidean distance, dt_cluster_spread_ms=0.1, rt_cluster_spread_s=20, and hclust method produces peak_clustering output containing peak_list_clustered with cluster IDs and"
- [other] Apply clusterPeaks function from GCIMS with distance_method='euclidean', dt_cluster_spread_ms=0.1, rt_cluster_spread_s=20, and hclust linkage method. Extract and assign cluster IDs to each peak.: "Apply clusterPeaks function from GCIMS with distance_method='euclidean', dt_cluster_spread_ms=0.1, rt_cluster_spread_s=20, and hclust linkage method. 3. Extract and assign cluster IDs to each peak."
- [intro] Pressure and temperature fluctuations as well as degradation of the chromatographic column are some of the causes of misalignments in the data, both in retention and drift time.: "Pressure and temperature fluctuations as well as degradation of the chromatographic column are some of the causes of misalignments in the data, both in retention and drift time."
- [readme] GCIMS is an R package implementing a preprocessing pipeline for Gas Chromatography – Ion Mobility Spectrometry samples.: "GCIMS is an R package implementing a preprocessing pipeline for Gas Chromatography – Ion Mobility Spectrometry samples."
