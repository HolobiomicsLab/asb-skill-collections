---
name: metabolite-cluster-identification-from-correlated-features
description: Use when after preprocessing, imputation, and batch correction of LC-MS
  peak tables when you need to group redundant or related feature measurements (e.g.,
  [M+H]+ and [M+Na]+ adducts, or isotope peaks) into metabolite-level clusters before
  statistical testing or identification.
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
  - igraph
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

# metabolite-cluster-identification-from-correlated-features

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Groups correlated metabolic features into clusters based on mass-to-charge ratio proximity, retention time co-elution, and abundance correlation, then assigns each cluster a representative Cluster_ID derived from the feature with highest median peak area. This skill identifies putative metabolites that may represent the same compound across different ionization modes or adducts in non-targeted LC-MS data.

## When to use

After preprocessing, imputation, and batch correction of LC-MS peak tables when you need to group redundant or related feature measurements (e.g., [M+H]+ and [M+Na]+ adducts, or isotope peaks) into metabolite-level clusters before statistical testing or identification. Apply this when you have extracted feature metadata (Feature_ID, m/z, retention time) and sample abundance data stored in a MetaboSet object and suspect multiple features represent the same underlying metabolite.

## When NOT to use

- Input data is already clustered or aggregated to the metabolite level (Cluster_IDs already exist).
- Features have not been imputed or preprocessed; missing values or extreme drift will inflate false correlations.
- Retention time metadata is unavailable or unreliable; the RT window criterion cannot be applied.

## Inputs

- MetaboSet object (Biobase ExpressionSet subclass containing feature abundance matrix and feature metadata)
- Feature metadata table with columns: Feature_ID, Mass (m/z), RetentionTime
- Feature abundance matrix (samples × features)

## Outputs

- Cluster_ID assignments for all features (character vector or column added to feature data)
- Feature-to-cluster membership mapping (data.frame or list)
- Connections graph (igraph object showing correlated feature pairs)

## How to apply

First, extract sample abundances and feature metadata (Feature_ID, Mass, RetentionTime) from the MetaboSet object using combined_data() and fData(). Second, execute find_connections() with a correlation threshold (e.g., 0.9 Pearson r) and a retention time window (e.g., ±1 s) to identify all feature pairs that co-elute and show strong abundance correlation, specifying column names for feature ID, m/z, and RT. Third, run find_clusters() with a degree threshold (e.g., 0.8) on the connections output to decompose the graph into connected components and iteratively prune nodes until each remaining node meets the minimum degree criterion, removing weakly connected peripheral features. Finally, execute assign_cluster_id() to label all features with a Cluster_ID named after the feature with the highest median peak area within each cluster, then verify that the Cluster_ID column has been added to feature data and inspect cluster assignments for biological plausibility.

## Related tools

- **notame** (Orchestrates the complete LC-MS preprocessing and clustering workflow; provides find_connections(), find_clusters(), and assign_cluster_id() functions for feature correlation, graph decomposition, and cluster labeling.) — https://github.com/hanhineva-lab/notame
- **R** (Runtime environment and language for executing notame functions and manipulating MetaboSet objects.)
- **Biobase** (Provides the ExpressionSet class on which MetaboSet is built; enables storage and manipulation of feature metadata and abundance matrices.)
- **igraph** (Underlying graph library used by find_connections() and find_clusters() for network decomposition and connected component detection.)

## Examples

```
# Extract feature data and abundances from MetaboSet
fdata <- fData(metaboset_obj)
abund <- combined_data(metaboset_obj)
# Identify correlated feature pairs
connections <- find_connections(fdata, abund, name_col='Feature_ID', mz_col='Mass', rt_col='RetentionTime', correlation_threshold=0.9, rt_window=1)
# Decompose into connected components
clusters <- find_clusters(connections, degree_threshold=0.8)
# Assign cluster IDs
fdata <- assign_cluster_id(fdata, clusters, abund)
```

## Evaluation signals

- Cluster_ID column exists in feature metadata (fData) and contains no missing values for non-flagged features.
- Each cluster contains ≥2 features (singletons indicate weak connectivity or algorithm misconfiguration).
- Features within a cluster show Pearson correlation ≥ correlation threshold (e.g., r ≥ 0.9) when abundance vectors are compared.
- Feature pairs within a cluster have retention time differences ≤ the specified RT window (e.g., ±1 s for LC-MS).
- Cluster naming is consistent: verify that the Cluster_ID label matches the Feature_ID with the highest median peak area in that cluster.
- Cluster composition is biologically plausible: spot-check large clusters (>5 features) for known adduct mass differences (e.g., +1 for H+, +23 for Na+, -1 for deprotonation) or isotope patterns (+1.003 for 13C).

## Limitations

- Clustering results depend critically on correlation threshold and RT window parameters; suboptimal thresholds can produce fragmented or over-merged clusters.
- The algorithm assumes that correlated, co-eluting features are related; true biological co-regulation can produce false positive clusters.
- Retention time variability across samples (drift) can inflate within-cluster RT differences; drift correction must precede clustering.
- Missing values remaining after imputation reduce correlation estimates; cluster quality is sensitive to imputation method (notame recommends random forest imputation via missForest).
- Degree threshold (minimum node connectivity) is dataset-dependent and requires empirical tuning; insufficient threshold retains spurious features, excessive threshold fragments true clusters.
- The method is sensitive to peak picking software output quality; systematic biases in feature detection or m/z calibration will propagate to cluster assignments.

## Evidence

- [other] find_connections, find_clusters, and assign_cluster_id functions operate together to group related metabolic features: "Execute find_connections() with correlation threshold 0.9, retention time window ±1 s, and column names (name_col='Feature_ID', mz_col='Mass', rt_col='RetentionTime') to identify all correlated"
- [readme] Clustering algorithm for grouping similar features: "A novel method for clustering similar molecular features"
- [other] MetaboSet object structure for notame: "MetaboSet objects are the primary data structure of this package. MetaboSet is built upon the ExpressionSet class from the Biobase package by Bioconductor"
- [readme] Rationale for feature clustering in LC-MS: "The algorithm for clustering molecular features originating from the same compound is based on MATLAB code written by David Broadhurst"
- [intro] notame bundles preprocessing and visualization methods: "This package can be used to analyze preprocessed LC-MS data in non-targeted metabolomics. Notame was developed at the [research group of nutritional metabolomics at University of Eastern Finland]"
