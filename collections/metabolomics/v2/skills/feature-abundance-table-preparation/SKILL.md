---
name: feature-abundance-table-preparation
description: Use when you have raw omics data (microbiome OTU/ASV tables, metabolomic
  or transcriptomic abundance matrices) that needs to be reformatted or validated
  before correlation analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3697
  - http://edamontology.org/topic_0092
  tools:
  - MetaNet
  - R
  - pcutils
  - igraph
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1101/2025.06.26.661636v1
  title: MetaNet
evidence_spans:
- MetaNet, a high-performance R package that unifies network construction, visualization,
  and analysis across diverse omics layers.
- MetaNet, a high-performance R package that unifies network construction, visualization,
  and analysis across diverse omics layers
- MetaNet, a high-performance R package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metanet_cq
    doi: 10.1101/2025.06.26.661636v1
    title: MetaNet
  dedup_kept_from: coll_metanet_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2025.06.26.661636v1
  all_source_dois:
  - 10.1101/2025.06.26.661636v1
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# feature-abundance-table-preparation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Prepare and format feature abundance tables (rows = features, columns = samples) for correlation-based network construction. This skill ensures data is in the correct orientation and structure for high-dimensional omics datasets containing thousands of features, enabling downstream correlation computation and network building.

## When to use

You have raw omics data (microbiome OTU/ASV tables, metabolomic or transcriptomic abundance matrices) that needs to be reformatted or validated before correlation analysis. Use this skill when your input table has features as rows and samples as columns, or when you need to subset, transpose, or verify the integrity of your feature abundance matrix prior to network construction.

## When NOT to use

- Input is already a correlation matrix or distance matrix — proceed directly to network construction.
- Features are already in columns and samples in rows in the orientation required by your correlation engine — skip transpose step.
- You are working with pre-computed network edges or adjacency matrices, not raw abundances.

## Inputs

- Raw feature abundance table (CSV, TSV, or R data frame; rows = features, columns = samples)
- Optional: metadata or annotation table for sample-level or feature-level filtering
- Optional: multiple omics tables for multi-omics integration (microbiome, metabolome, transcriptome)

## Outputs

- Validated, transposed feature abundance matrix ready for correlation calculation (samples as rows, features as columns, or features as rows × samples as columns depending on correlation function input)
- Aligned multi-omics datasets with matched sample identifiers across layers (if applicable)

## How to apply

Load the feature abundance table into R with rows representing features (>10,000 in high-dimensional datasets) and columns representing samples. Transpose the matrix if necessary so that pairwise correlations are computed between features. Verify table dimensions, check for missing values or zero-variance features, and ensure sample identifiers and feature names are correctly preserved. If working with multi-omics data, align samples across layers. The table structure must support vectorized correlation computation in MetaNet's optimized correlation engine, which uses matrix algorithms to minimize memory and runtime overhead.

## Related tools

- **MetaNet** (Performs correlation calculation and network construction on prepared feature abundance tables; requires correctly formatted input matrix for c_net_calculate() function) — https://github.com/Asa12138/MetaNet
- **pcutils** (Provides utility functions for data manipulation and transformation, including transposition (t2() function) used in MetaNet workflows) — https://github.com/Asa12138/pcutils
- **R** (Core computing environment for loading, validating, and manipulating feature abundance tables)
- **igraph** (Underlying graph structure that MetaNet builds upon; requires proper node and edge specification from prepared abundance data)

## Examples

```
library(pcutils); library(MetaNet); data('otutab', package = 'pcutils'); totu <- t2(otutab[1:70, ]); cor <- c_net_calculate(totu)
```

## Evaluation signals

- Table dimensions are correct: number of rows matches feature count, number of columns matches sample count (or vice versa after transpose).
- No missing values (NA/NaN) in the numeric abundance matrix, or missing values are handled explicitly (e.g., imputed or removed).
- Feature names and sample identifiers are preserved and unique; no duplicates in row or column names.
- For multi-omics tables: sample identifiers are identical and ordered consistently across all omics layers; c_net_build() reports 'All samples matched' and 'All features are OK'.
- Correlation computation completes without memory overflow or runtime errors when passed to c_net_calculate(); output correlation matrix dimensions are (n_features × n_features).

## Limitations

- High-dimensional datasets (>10,000 features) require substantial memory even with MetaNet's optimized vectorized algorithms; transposition and validation should be done on subsets if RAM is limited.
- Zero-variance features (identical values across all samples) will produce undefined or NaN correlations; should be filtered before or after loading.
- Multi-omics alignment assumes samples are identifiable and consistently named across tables; mismatched or partial sample overlap will cause c_net_build() to reject the dataset.
- Large numbers of features with many zero-abundance values may inflate spurious correlations; quantile filtering or abundance thresholding is often recommended prior to network construction.

## Evidence

- [other] Load the feature abundance table (rows = features, columns = samples) into R. Compute pairwise correlations between all features using MetaNet's correlation engine, which is optimized for datasets exceeding 10,000 features.: "Load the feature abundance table (rows = features, columns = samples) into R. Compute pairwise correlations between all features using MetaNet's correlation engine, which is optimized for datasets"
- [intro] MetaNet enables fast and scalable correlation-based network construction for datasets with more than 10,000 features: "MetaNet enables fast and scalable correlation-based network construction for datasets with more than 10,000 features"
- [readme] Inter-species correlation coefficients were calculated after transposition: "Inter-species correlation coefficients were calculated after transposition"
- [readme] All samples matched. All features are OK. Calculating 18 samples and 150 features of 3 groups.: "All samples matched. All features are OK. Calculating 18 samples and 150 features of 3 groups."
- [readme] Pairwise correlation computation is central to most network-based omics tools, but the growing scale of omics datasets imposes substantial computational demands. MetaNet addresses this through optimized vectorized matrix algorithms for calculating correlation coefficients and corresponding p-values, greatly reducing memory use and runtime: "MetaNet addresses this through optimized vectorized matrix algorithms for calculating correlation coefficients and corresponding p-values, greatly reducing memory use and runtime"
