---
name: single-cell-rna-seq-normalization
description: Use when immediately after loading raw single-cell gene expression count matrices (AnnData objects) and before identifying highly variable genes or performing dimensionality reduction.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3565
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3308
  tools:
  - Python
  - Scanpy
  - anndata
derived_from:
- doi: 10.1186/s13059-017-1382-0
  title: scanpy
evidence_spans:
- Single-Cell Analysis in Python
- type annotations on function parameters
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/transcriptomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_scanpy
    doi: 10.1186/s13059-017-1382-0
    title: scanpy
  dedup_kept_from: coll_scanpy
schema_version: 0.2.0
---

# single-cell-rna-seq-normalization

## Summary

Normalize single-cell RNA-seq gene expression data to account for sequencing depth differences and stabilize variance across cells, a foundational preprocessing step required before dimensionality reduction and clustering. Scanpy implements this through library-size normalization followed by log transformation.

## When to use

Apply this skill immediately after loading raw single-cell gene expression count matrices (AnnData objects) and before identifying highly variable genes or performing dimensionality reduction. Normalization is mandatory when comparing gene expression across cells that have different total sequencing depths (UMI or read counts), which is the norm in scRNA-seq datasets.

## When NOT to use

- Input expression data is already normalized or log-transformed (e.g., from a published preprocessed dataset like pbmc3k_processed)
- Analysis requires preservation of raw count-level inference (e.g., for methods that explicitly model count distributions)
- Expression matrix contains negative or non-integer values, indicating prior transformation has already been applied

## Inputs

- AnnData object containing raw gene expression count matrix (adata.X)
- Cell-by-gene expression matrix with integer counts

## Outputs

- AnnData object with normalized, log-transformed expression values in adata.X
- Normalized matrix ready for highly variable gene selection and dimensionality reduction

## How to apply

First, apply library-size normalization using `sc.pp.normalize_total()` to divide each cell's gene expression counts by its total sequencing depth, accounting for technical variation in sequencing coverage across cells. Next, apply `sc.pp.log1p()` to stabilize variance by log-transforming the normalized counts. The rationale is that raw count data exhibit mean-variance relationships (higher-expressed genes have higher variance), and log transformation renders variance approximately homogeneous across expression levels, improving downstream statistical inference and visualization. These two operations should be applied in sequence on the raw count matrix stored in `adata.X` before feature selection or PCA.

## Related tools

- **Scanpy** (Primary toolkit providing normalize_total() and log1p() preprocessing functions for single-cell RNA-seq normalization) — https://github.com/scverse/scanpy
- **anndata** (Data structure (AnnData object) that stores the expression matrix and metadata for normalized counts) — https://github.com/scverse/anndata
- **Python** (Programming language in which Scanpy normalization pipelines are implemented and executed)

## Examples

```
import scanpy as sc; adata = sc.datasets.pbmc3k(); sc.pp.normalize_total(adata); sc.pp.log1p(adata)
```

## Evaluation signals

- Verify that adata.X contains float-type values (not raw integer counts) after normalization and log transformation
- Check that the mean expression per gene is stable across cells and no longer strongly correlated with gene variance
- Confirm that log-transformed values are non-negative (log1p output) and approximate a normal distribution within cell clusters
- Inspect that downstream highly variable gene selection (using pp.highly_variable_genes) identifies a reasonable number of genes (typically 1000–5000 for pbmc3k-scale datasets)
- Verify that PCA and UMAP visualizations post-normalization show clear, meaningful cell clusters without artificial density patterns from technical bias

## Limitations

- Library-size normalization assumes that sequencing depth differences are technical noise; it does not account for genuine biological differences in total RNA content across cell types
- Log transformation with log1p can compress expression differences at high count levels, potentially reducing sensitivity for highly expressed genes
- Normalization does not address batch effects or other non-technical sources of variation; batch correction should be applied as a separate preprocessing step if multi-sample or multi-batch data is present

## Evidence

- [other] normalization and log transformation: "Apply normalize_total normalization to account for sequencing depth differences. 3. Apply log1p transformation to stabilize variance."
- [other] highly_variable_genes after normalization: "Identify highly variable genes using pp.highly_variable_genes to reduce dimensionality. 5. Scale gene expression to unit variance using pp.scale."
- [intro] Scanpy preprocessing capabilities: "It includes preprocessing, visualization, clustering, trajectory inference and differential expression testing"
- [other] sequencing depth normalization rationale: "Apply normalize_total normalization to account for sequencing depth differences."
