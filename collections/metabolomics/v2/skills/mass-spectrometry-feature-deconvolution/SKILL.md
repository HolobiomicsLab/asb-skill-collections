---
name: mass-spectrometry-feature-deconvolution
description: Use when you have a peak table from LC-MS peak picking software (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - notame
  - R
  - Biobase
derived_from:
- doi: 10.3390/metabo10040135
  title: notame
- doi: 10.1093/bioinformatics/btr597
  title: ''
evidence_spans:
- This package can be used to analyze preprocessed LC-MS data in non-targeted metabolomics
- library(notame)
- reads them to R, conducts additional preprocessing and statistical analyses
- '```MetaboSet``` is built upon the ```ExpressionSet``` class from the Biobase package by Bioconductor'
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Reconstruct the feature clustering algorithm producing Cluster_ID assignments

## Summary

Group correlated LC-MS metabolic features into clusters based on mass-to-charge ratio proximity, retention time co-elution, and abundance correlation, then assign cluster identifiers named after the highest-abundance feature in each cluster. This skill resolves isotopologues, adducts, and in-source fragments that represent the same underlying metabolite.

## When to use

Apply this skill when you have a peak table from LC-MS peak picking software (e.g., MS-DIAL output) with Feature_ID, Mass, RetentionTime, and abundance columns, and you need to reduce redundancy by merging features likely to originate from the same compound before statistical analysis or metabolite identification.

## When NOT to use

- Input features are already known to represent distinct metabolites (i.e., target analysis with pre-defined compound lists); clustering adds unnecessary complexity.
- Retention time information is unreliable or missing; the ±RT window filter becomes ineffective.
- Peak picking output is incomplete or lacks standardized feature identifiers, making correlation-based linkage unreliable.

## Inputs

- MetaboSet object with feature abundance matrix (exprs) and feature metadata (fData)
- Feature metadata: Feature_ID, Mass (m/z), RetentionTime columns
- Sample abundance data: feature intensities across all samples

## Outputs

- Updated MetaboSet object with Cluster_ID column added to feature data
- Cluster membership assignments (each feature labeled with its cluster)
- Cluster representatives (the feature with highest median peak area per cluster)

## How to apply

First, extract sample abundances and feature metadata (Feature_ID, Mass, RetentionTime) from the MetaboSet object using combined_data() and fData(). Execute find_connections() with a correlation threshold (e.g., 0.9), a retention time window (e.g., ±1 s), and specify column names (name_col='Feature_ID', mz_col='Mass', rt_col='RetentionTime') to build a graph where nodes are features and edges connect correlated pairs within the RT window. Run find_clusters() with a degree threshold (e.g., 0.8) to decompose the graph into connected components and iteratively prune low-degree nodes until each remaining node meets the minimum connectivity criterion. Finally, execute assign_cluster_id() to label all features with a Cluster_ID (named after the feature with highest median peak area in each cluster). Verify that the Cluster_ID column has been added to feature metadata and inspect within-cluster groupings to confirm biologically plausible associations.

## Related tools

- **notame** (Provides find_connections(), find_clusters(), and assign_cluster_id() functions; manages MetaboSet data structure holding feature metadata and abundances) — https://github.com/hanhineva-lab/notame
- **Biobase** (ExpressionSet class upon which MetaboSet is built, enabling unified access to feature metadata and abundance matrices)
- **R** (Runtime environment for executing notame functions and data manipulation)

## Examples

```
find_connections(metaboset, name_col='Feature_ID', mz_col='Mass', rt_col='RetentionTime', correlation_threshold=0.9, rt_window=1); clusters <- find_clusters(connections, degree_threshold=0.8); metaboset <- assign_cluster_id(metaboset, clusters)
```

## Evaluation signals

- Cluster_ID column is present in fData(metaboset) and contains no missing values for valid features
- Each Cluster_ID is named after a valid Feature_ID corresponding to the highest median peak area feature in that cluster
- All features within a cluster have pairwise correlation ≥ threshold AND retention times within ±RT window
- Cluster sizes are reasonable (no single cluster contains >90% of features, suggesting threshold parameters are too permissive)
- Degree distribution of cluster members shows that iterative pruning removed low-connectivity outliers as expected

## Limitations

- Clustering quality depends critically on accurate m/z and retention time measurements; calibration drift or peak picking errors propagate into spurious cluster assignments.
- Correlation threshold and retention time window are user-specified and may require optimization for different LC-MS methods, ionization modes, or metabolite classes; no universally optimal values are provided.
- Features with very low abundance across samples may have unstable correlation estimates, leading to unexpected cluster membership or isolation.
- The algorithm assumes that co-eluting, correlated features represent the same metabolite; genuine metabolites with very similar m/z and RT (isobars) may be incorrectly merged.

## Evidence

- [other] Execute find_connections() with correlation threshold 0.9, retention time window ±1 s, and column names (name_col='Feature_ID', mz_col='Mass', rt_col='RetentionTime') to identify all correlated feature pairs within the RT window.: "Execute find_connections() with correlation threshold 0.9, retention time window ±1 s, and column names (name_col='Feature_ID', mz_col='Mass', rt_col='RetentionTime') to identify all correlated"
- [other] Run find_clusters() with degree threshold 0.8 on the connections output to decompose the graph into connected components and prune nodes iteratively until each node meets the minimum degree criterion.: "Run find_clusters() with degree threshold 0.8 on the connections output to decompose the graph into connected components and prune nodes iteratively until each node meets the minimum degree criterion."
- [other] Execute assign_cluster_id() to label all features with Cluster_ID (named after the feature with highest median peak area in each cluster) and record cluster membership.: "Execute assign_cluster_id() to label all features with Cluster_ID (named after the feature with highest median peak area in each cluster) and record cluster membership."
- [readme] A novel method for clustering similar molecular features: "A novel method for clustering similar molecular features"
- [readme] The algorithm for clustering molecular features originating from the same compound is based on MATLAB code written by David Broadhurst: "The algorithm for clustering molecular features originating from the same compound is based on MATLAB code written by David Broadhurst"
