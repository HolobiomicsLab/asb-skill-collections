---
name: feature-correlation-graph-construction
description: Use when after imputing missing values and before assigning Cluster_IDs
  in the notame preprocessing pipeline.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - notame
  - R
  - Biobase
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.3390/metabo10040135
  title: notame
- doi: 10.1093/bioinformatics/btr597
  title: ''
evidence_spans:
- This package can be used to analyze preprocessed LC-MS data in non-targeted metabolomics
- library(notame)
- reads them to R, conducts additional preprocessing and statistical analyses
- '```MetaboSet``` is built upon the ```ExpressionSet``` class from the Biobase package
  by Bioconductor'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_notame_cq
    doi: 10.3390/metabo10040135
    title: notame
  dedup_kept_from: coll_notame_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3390/metabo10040135
  all_source_dois:
  - 10.3390/metabo10040135
  - 10.1093/bioinformatics/btr597
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Reconstruct the feature clustering algorithm producing Cluster_ID assignments

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Build a graph of correlated LC-MS metabolic features by identifying feature pairs with high correlation and similar retention times, then decompose the graph into connected components to group related features for subsequent cluster assignment. This is a prerequisite step for feature clustering and metabolite identification in non-targeted metabolomics workflows.

## When to use

Apply this skill after imputing missing values and before assigning Cluster_IDs in the notame preprocessing pipeline. Use it when you have a MetaboSet object with abundance data and feature metadata (Feature_ID, mass-to-charge ratio, retention time) and need to group isotopes, adducts, and fragments originating from the same parent compound before statistical analysis or metabolite identification.

## When NOT to use

- Input is already a curated peak table with pre-assigned compound classes; feature clustering is redundant if metabolites are already identified.
- Retention time metadata is missing, unreliable, or significantly drifts across samples; clustering will fail or produce false positives.
- Correlation threshold 0.9 is too stringent for your instrument/method; adjust only after verifying it does not conflate distinct isomers or isobars in your mass range.

## Inputs

- MetaboSet object (Biobase ExpressionSet subclass) with abundance matrix and feature metadata
- Feature metadata columns: Feature_ID, Mass (m/z), RetentionTime
- Preprocessed abundance data (post-imputation, post-drift correction)

## Outputs

- Graph of feature connections (edges represent correlation ≥ 0.9 + RT co-elution within ±1 s)
- Connected components (clusters of related features)
- Feature cluster assignments (input to assign_cluster_id())

## How to apply

Extract sample abundances and feature metadata (Feature_ID, Mass, RetentionTime) from the MetaboSet object using combined_data() and fData(). Execute find_connections() with a correlation threshold of 0.9 and retention time window of ±1 s, specifying column names (name_col='Feature_ID', mz_col='Mass', rt_col='RetentionTime') to identify all correlated feature pairs within the RT window. This produces a graph where nodes are features and edges represent correlation + co-elution relationships. Run find_clusters() with a degree threshold of 0.8 on the connections output to decompose the graph into connected components, pruning nodes iteratively until each remaining node meets the minimum degree criterion. This ensures that within each cluster, features are sufficiently connected, removing isolated or weakly connected outliers. The output is a set of feature clusters ready for Cluster_ID assignment.

## Related tools

- **notame** (Provides find_connections(), find_clusters(), and assign_cluster_id() functions to construct and decompose feature correlation graphs for LC-MS metabolomics data) — https://github.com/hanhineva-lab/notame
- **Biobase** (Supplies ExpressionSet class underlying MetaboSet; enables extraction of feature metadata via fData() and abundance data via combined_data())
- **R** (Runtime environment for executing notame functions and correlation-based graph construction)

## Examples

```
# R code: construct feature correlation graph and clusters
data <- combined_data(metaboset_object)
fdata <- fData(metaboset_object)
connections <- find_connections(data, fdata, correlation_threshold = 0.9, rt_window = 1, name_col = 'Feature_ID', mz_col = 'Mass', rt_col = 'RetentionTime')
clusters <- find_clusters(connections, degree_threshold = 0.8)
```

## Evaluation signals

- Verify that find_connections() output contains only feature pairs with Pearson/Spearman correlation ≥ 0.9 and retention time difference ≤ ±1 s.
- Confirm that find_clusters() output is a set of disjoint connected components with no isolated nodes below the degree threshold of 0.8.
- Check that cluster sizes are biologically plausible (e.g., 1–10 features per cluster for typical LC-MS runs); very large clusters (>20 features) may indicate overly permissive thresholds or batch effects.
- Verify that each feature appears in exactly one cluster and all features from the input MetaboSet are represented in the cluster assignments.
- Inspect a sample cluster manually: confirm that features within a cluster co-elute (RT differences < ±1 s) and have high pairwise correlations across samples, consistent with isotopes, adducts, or in-source fragments.

## Limitations

- Correlation threshold (0.9) and retention time window (±1 s) are fixed hyperparameters; they may require tuning for different instruments, chromatographic methods, or mass ranges, and notame documentation offers limited guidance on this.
- The method assumes that high correlation and co-elution reliably indicate shared identity; false positives can occur with coeluting contaminants or unrelated features with correlated abundance patterns across samples.
- Degree threshold (0.8) for cluster pruning may remove valid low-abundance features (e.g., rare isotopologues or minor adducts) that have few correlated neighbors but are biologically significant.
- Retention time stability is assumed; significant RT drift across the analysis window or between batches can fragment true clusters or conflate unrelated features.
- The algorithm does not account for mass difference constraints (e.g., known isotope or adduct mass shifts); it relies purely on correlation and RT proximity, potentially missing chemically informed relationships.

## Evidence

- [other] Extract sample abundances and feature metadata (Feature_ID, Mass, RetentionTime) from the toy MetaboSet object using combined_data() and fData().: "Extract sample abundances and feature metadata (Feature_ID, Mass, RetentionTime) from the toy MetaboSet object using combined_data() and fData()"
- [other] Execute find_connections() with correlation threshold 0.9, retention time window ±1 s, and column names (name_col='Feature_ID', mz_col='Mass', rt_col='RetentionTime') to identify all correlated feature pairs within the RT window.: "Execute find_connections() with correlation threshold 0.9, retention time window ±1 s, and column names (name_col='Feature_ID', mz_col='Mass', rt_col='RetentionTime') to identify all correlated"
- [other] Run find_clusters() with degree threshold 0.8 on the connections output to decompose the graph into connected components and prune nodes iteratively until each node meets the minimum degree criterion.: "Run find_clusters() with degree threshold 0.8 on the connections output to decompose the graph into connected components and prune nodes iteratively until each node meets the minimum degree criterion."
- [other] MetaboSet is built upon the ExpressionSet class from the Biobase package by Bioconductor: "```MetaboSet``` is built upon the ```ExpressionSet``` class from the Biobase package by Bioconductor"
- [readme] A novel method for clustering similar molecular features: "A novel method for clustering similar molecular features"
- [readme] The algorithm for clustering molecular features originating from the same compound is based on MATLAB code written by David Broadhurst: "The algorithm for clustering molecular features originating from the same compound is based on MATLAB code written by David Broadhurst"
