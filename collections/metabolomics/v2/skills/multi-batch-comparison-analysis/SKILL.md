---
name: multi-batch-comparison-analysis
description: Use when you have a SummarizedExperiment object containing both a raw/imputed assay (e.g., rawImpute) and a normalized assay (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3935
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - hRUV
  - R
  - dplyr
  - SummarizedExperiment
derived_from:
- doi: 10.1101/2020.12.21.423723
  title: hRUV
evidence_spans:
- '`hRUV` is a package for normalisation of multiple batches of metabolomics data'
- '`hRUV` is a package for normalisation of multiple batches of metabolomics data in a hierarchical strategy'
- Install the R package from GitHub using the `devtools` package
- we will load the hRUV package and other packages required for the demonstration... library(dplyr)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_hruv_cq
    doi: 10.1101/2020.12.21.423723
    title: hRUV
  dedup_kept_from: coll_hruv_cq
schema_version: 0.2.0
---

# multi-batch-comparison-analysis

## Summary

Generate paired before/after PCA visualizations to assess batch-effect removal in multi-batch metabolomics studies. This skill validates whether a hierarchical normalization strategy (such as hRUV) has successfully eliminated batch clustering by comparing raw and normalized assays across the same samples colored by batch identity.

## When to use

Apply this skill when you have a SummarizedExperiment object containing both a raw/imputed assay (e.g., rawImpute) and a normalized assay (e.g., loessShort_concatenate) from a multi-batch metabolomics experiment, and you need to visually confirm that batch effects present in the raw data have been removed by the normalization pipeline. This is especially critical after applying hierarchical normalization to metabolomics data with intra-batch and inter-batch replicates.

## When NOT to use

- Data has not yet undergone cleaning and imputation—apply data cleaning with threshold filtering and k-nearest neighbour imputation first.
- SummarizedExperiment object lacks batch_info metadata in colData; batch identity must be explicitly tracked.
- Only a single batch is present in the dataset; multi-batch comparison is meaningless for single-batch data.

## Inputs

- SummarizedExperiment object with rawImpute assay
- SummarizedExperiment object with loessShort_concatenate (or equivalent normalized) assay
- batch_info metadata column in colData

## Outputs

- PCA plot (pre-normalization) colored by batch_info
- PCA plot (post-normalization) colored by batch_info
- visual comparison report confirming presence/absence of batch clustering

## How to apply

Load the SummarizedExperiment object and extract both the raw imputed assay and the normalized assay. Generate two PCA plots using hRUV::plotPCA, coloring samples by batch_info in both plots. The first plot visualizes the pre-normalization batch structure using the rawImpute assay; the second visualizes post-normalization using the loessShort_concatenate assay. Compare the spatial distribution of batch-colored clusters: if normalization was successful, the normalized plot should show no batch-driven clustering (i.e., samples from different batches should intermix in the PCA space rather than segregate by batch). Document any residual batch structure that persists after normalization.

## Related tools

- **hRUV** (provides plotPCA function to generate PCA visualizations with batch coloring; implements hierarchical normalization strategy (loess smoothing + RUV-III) that produces the normalized assay for comparison) — https://github.com/SydneyBioX/hRUV
- **SummarizedExperiment** (container object for storing multiple assays (rawImpute, loessShort_concatenate) and associated metadata (batch_info); accessed via assay() and colData())
- **dplyr** (optional; used for filtering or organizing batch metadata prior to visualization)
- **R** (execution environment for hRUV and SummarizedExperiment operations)

## Examples

```
# Load normalized SE object
library(hRUV)
library(SummarizedExperiment)
p1 <- hRUV::plotPCA(dat, assay = "rawImpute", colour_by = "batch_info")
p2 <- hRUV::plotPCA(dat, assay = "loessShort_concatenate", colour_by = "batch_info")
# Visual comparison: p1 should show batch clustering; p2 should show batch mixing
```

## Evaluation signals

- Pre-normalization PCA plot shows clear spatial clustering by batch (samples from the same batch occupy nearby regions despite belonging to different biological groups).
- Post-normalization PCA plot shows no batch-driven clustering (batch-colored groups are randomly interspersed across the plot; PC1/PC2 variance is no longer dominated by batch).
- Batch-driven principal components (if any remain post-normalization) contribute <10% of total variance, indicating successful batch correction.
- Biological signal (if available in metadata, e.g., disease status) becomes visible or strengthens in the post-normalization plot, confirming that batch removal has not obscured true biological structure.
- Statistical test (e.g., PERMANOVA on batch vs. PC scores) shows non-significant batch effect post-normalization but significant batch effect pre-normalization.

## Limitations

- PCA is a dimensionality-reduction technique and may not capture all batch effects; residual batch structure in higher-dimensional space may persist despite visual absence in PC1/PC2.
- Visualization effectiveness depends on batch effect magnitude relative to biological signal—weak batch effects may be difficult to discern visually even in raw data.
- hRUV normalization strategy is optimized for hierarchical study designs with embedded intra-batch and inter-batch replicates; may not perform equally well on datasets lacking such replicate structure.
- Comparison is qualitative; formal statistical batch-effect assessment (e.g., silhouette index, batch entropy) should accompany visual inspection for rigorous validation.

## Evidence

- [intro] batch effect validation via PCA before and after normalization: "PCA visualisation of rawImpute assay shows strong batch effect, whereas PCA of the loessShort_concatenate normalised assay no longer displays batch effect when coloured by batch_info."
- [readme] hRUV hierarchical normalization approach: "hRUV is a package for normalisation of multiple batches of metabolomics data in a hierarchical strategy with use of samples replicates in large-scale studies."
- [intro] intra-batch and inter-batch normalization workflow steps: "For intra batch normalisation, we perform loess smoothing on samples and RUV-III using short replicates with parameter k set to 5. For inter batch normalisation, we perform concatenating hierarchical"
- [intro] use of plotPCA function for batch effect visualization: "Generate a PCA plot using hRUV::plotPCA with rawImpute assay colored by batch_info to visualize the pre-normalization batch effect."
- [intro] data input format and preprocessing: "The data is already formatted in to a SummarizedExperiment object. we provide a first 5 batches of BioHEART-CT metabolomics data."
