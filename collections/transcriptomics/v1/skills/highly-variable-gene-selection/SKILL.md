---
name: highly-variable-gene-selection
description: Use when after normalization (normalize_total, log1p transformation) and before PCA or other dimensionality reduction on raw or near-raw single-cell gene expression matrices.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3173
  - http://edamontology.org/topic_0203
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

# highly-variable-gene-selection

## Summary

Identify and retain genes with high variance across single cells to reduce dimensionality while preserving biological signal. This preprocessing step filters a typically genome-scale gene set (e.g., ~20,000 genes in human) down to a smaller, more informative subset (typically hundreds to thousands) before downstream analysis.

## When to use

Apply this skill after normalization (normalize_total, log1p transformation) and before PCA or other dimensionality reduction on raw or near-raw single-cell gene expression matrices. Use it when working with whole-genome expression data and you need to reduce computational burden while retaining genes most likely to distinguish cell types or biological states.

## When NOT to use

- Input is already a pre-filtered feature table (e.g., from a prior study); redundant filtering may lose known markers.
- Analysis requires discovery of rare or lowly-expressed genes (e.g., transcription factors, cell-type-specific markers with low absolute expression); variance-based selection may exclude them.
- Working with targeted or amplicon sequencing data pre-selected for specific genes of interest; apply only if you intend to expand the feature set.

## Inputs

- AnnData object with normalized, log-transformed gene expression matrix (n_obs × n_vars)
- Cell-level metadata (obs) and gene-level metadata (var)

## Outputs

- AnnData object with highly_variable boolean column in .var
- Subset AnnData object containing only highly variable genes
- Variance metrics and thresholds stored in .var annotations

## How to apply

Use Scanpy's pp.highly_variable_genes() function to identify genes with high variance across the cell population. The function computes variance metrics (typically within-batch or across-batch) and ranks genes; genes above a specified variance threshold are retained. This step is applied to a normalized, log-transformed AnnData object (obs × genes matrix). The selected genes are then used for all subsequent analysis (PCA, neighbor graph, clustering, embedding); genes failing to meet the variance threshold are excluded to reduce noise and improve computational efficiency without sacrificing biological interpretability.

## Related tools

- **Scanpy** (Primary library providing pp.highly_variable_genes() function for variance-based gene filtering) — https://github.com/scverse/scanpy
- **anndata** (Data structure (AnnData) for storing and manipulating gene expression matrices with metadata) — https://github.com/scverse/anndata
- **Python** (Programming language and runtime for executing Scanpy preprocessing functions)

## Examples

```
import scanpy as sc
adata = sc.read_h5ad('pbmc3k_normalized.h5ad')
sc.pp.highly_variable_genes(adata, min_mean=0.0125, max_mean=3, min_disp=0.5)
adata_hvg = adata[:, adata.var.highly_variable]
sc.pp.pca(adata_hvg)
```

## Evaluation signals

- AnnData.var contains a 'highly_variable' boolean column with True/False for each gene
- Number of retained genes is substantially smaller than input (typically <20% of original gene count) but sufficient for downstream analysis
- Retained genes show high variance across the cell population (inspect .var['dispersions'] or equivalent metric)
- PCA and clustering on highly variable genes produce interpretable, biologically meaningful cell clusters consistent with known biology
- Highly variable genes include known marker genes for the expected cell types in the dataset

## Limitations

- Variance-based selection assumes noise is uniformly distributed and that high-variance genes are biologically informative; this may fail if batch effects dominate variance structure.
- Rare cell types or transient cell states with low variance within-type but high between-type variance may be missed.
- Genes with uniform or bimodal expression (e.g., on/off markers) may have moderate variance and pass filtering; additional filtering (e.g., by mean expression) may be needed.
- The method is sensitive to normalization choice; improper normalization before variance calculation will bias gene selection.

## Evidence

- [other] Identify highly variable genes using pp.highly_variable_genes to reduce dimensionality.: "Identify highly variable genes using pp.highly_variable_genes to reduce dimensionality."
- [intro] Scanpy is a scalable toolkit for analyzing single-cell gene expression data built jointly with anndata.: "Scanpy is a scalable toolkit for analyzing single-cell gene expression data built jointly with anndata."
- [intro] Scanpy includes preprocessing, visualization, clustering, trajectory inference and differential expression testing capabilities: "It includes preprocessing, visualization, clustering, trajectory inference and differential expression testing"
