---
name: retention-time-co-elution-detection
description: Use when after matching mass-to-charge ratios to a compound database (e.g., KEGG) and assigning adduct/fragment types, when you have an annotated feature table with retention times, m/z values, and intensity profiles across samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - mWISE
  - R
  - CAMERA
derived_from:
- doi: 10.1021/acs.analchem.1c00238
  title: mWISE
evidence_spans:
- mWISE (metabolomics Wise Inference of Speck Entities) is an R package that provides tools for context-based annotation of untargeted LC-MS data.
- mWISE (metabolomics Wise Inference of Speck Entities) is an R package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mwise_cq
    doi: 10.1021/acs.analchem.1c00238
    title: mWISE
  dedup_kept_from: coll_mwise_cq
schema_version: 0.2.0
---

# retention-time-co-elution-detection

## Summary

Group co-eluting LC-MS features by retention time proximity and intensity correlation to identify candidate ions arising from the same metabolite. This clustering step precedes candidate filtering and reduces false positive annotations by consolidating fragments and adducts into quasi-molecular ion clusters.

## When to use

After matching mass-to-charge ratios to a compound database (e.g., KEGG) and assigning adduct/fragment types, when you have an annotated feature table with retention times, m/z values, and intensity profiles across samples. Apply this skill before filtering to coarse-grained candidate sets and to enable cluster-aware prioritization of quasi-molecular ions over in-source fragments.

## When NOT to use

- Input features are already known to be from distinct metabolites with no expected co-elution.
- Retention time data are missing, unreliable, or severely variable across analytical runs.
- Sample set is too small (< 3 samples) to establish meaningful intensity correlation patterns.
- Features have been pre-filtered to only quasi-molecular ions; clustering is redundant if no fragment/adduct diversity remains.

## Inputs

- Annotated feature table with KEGG candidate assignments and adduct type labels
- Feature table columns: m/z, retention time, intensity across samples
- KEGG database matches with adduct/fragment classifications

## Outputs

- Feature table with pcgroup (cluster group identifier) column added
- Cluster membership assignments linking co-eluting features to putative metabolite groups

## How to apply

Use the mWISE featuresClustering function to group features based on retention time proximity and intensity correlation across the sample set. The function clusters co-eluting features and assigns each to a cluster group identifier (pcgroup). Merge the resulting pcgroup column back into the annotated feature table. The rationale is that true metabolite ions—parent, adducts, and fragments—co-elute and show correlated intensity patterns, whereas noise and unrelated features do not. This creates a structural context for the downstream cluster-based filtering step, which retains only quasi-molecular adducts (MH, MNa, MK, etc.) within each cluster and removes low-frequency adducts (observed frequency ≤ 0.1) and in-source fragments.

## Related tools

- **mWISE** (Provides featuresClustering function to group co-eluting features by retention time and intensity correlation; outputs pcgroup cluster identifiers) — https://dev.b2s.club/b2slab/mWISE
- **R** (Runtime environment for mWISE and cluster analysis workflows)
- **CAMERA** (Source of default adduct and fragment classification table used to label features before clustering)

## Examples

```
featuresClustering(annotated_table, rt_window = 0.5, intensity_cor_threshold = 0.6) %>% left_join(annotated_table, by = 'feature_id')
```

## Evaluation signals

- Each output pcgroup contains 2+ features with similar retention times (within expected chromatographic peak width).
- Features within the same cluster show correlated intensity patterns across the sample set (visual inspection or rank correlation > 0.6).
- Cluster membership is consistent across replicate analytical runs (if available).
- Downstream cluster-based filtering step successfully retains quasi-molecular ions and removes in-source fragments, as confirmed by pcgroup composition inspection.
- No pcgroup is assigned to isolated features with no co-eluting neighbors (singleton clusters may indicate true singletons or failed clustering).

## Limitations

- Clustering quality depends on the number and diversity of samples; small sample sets or homogeneous intensity profiles reduce correlation signal.
- Retention time drift or non-linear shifts between runs can cause true co-eluting features to be split into separate clusters or falsely grouped.
- Shared adducts or neutral loss patterns across unrelated metabolites with similar retention times may cause false co-clustering.
- The featuresClustering function uses fixed or user-specified thresholds for retention time proximity and intensity correlation; parameter tuning is required for different instrumental platforms and chromatographic methods.
- Very high feature density (hundreds of features in a narrow retention time window) can lead to over-clustering or ambiguous cluster assignments.

## Evidence

- [intro] The featuresClustering function groups co-eluting features based on intensity correlation and retention time proximity: "the features that may come from the same metabolite are clustered using the `featuresClustering` function"
- [intro] Cluster group identifiers (pcgroup) are merged into the annotated table as a new column: "Apply mWISE featuresClustering function to group co-eluting features based on intensity correlation and retention time proximity. 3. Merge the resulting cluster group (pcgroup) identifiers into the"
- [intro] Clustering precedes cluster-based filtering to enable retention of only quasi-molecular adducts: "clustering and filtering the potential KEGG candidates"
- [intro] The rationale: true metabolite ions co-elute and show correlated behavior: "the features that may come from the same metabolite are clustered using the `featuresClustering` function"
