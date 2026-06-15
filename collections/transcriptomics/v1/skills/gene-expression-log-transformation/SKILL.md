---
name: gene-expression-log-transformation
description: Use when after normalizing total UMI counts per cell using normalize_total, and before PCA or feature selection. Use this when working with raw or depth-normalized count matrices where gene expression values span multiple orders of magnitude and variance is not homogeneous across expression levels.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3170
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

# gene-expression-log-transformation

## Summary

Apply log1p transformation to single-cell gene expression matrices after normalization to stabilize variance and compress the dynamic range of count data. This step is essential in the preprocessing pipeline before downstream analysis like PCA and clustering.

## When to use

After normalizing total UMI counts per cell using normalize_total, and before PCA or feature selection. Use this when working with raw or depth-normalized count matrices where gene expression values span multiple orders of magnitude and variance is not homogeneous across expression levels.

## When NOT to use

- Input is already log-transformed or VST-normalized (e.g., from a prior analysis step or external preprocessing)
- Working with already-transformed data (e.g., TPM, FPKM, or other log-scale units)
- Analyzing data where variance homogeneity across expression levels is not a concern or where linear methods are not planned

## Inputs

- AnnData object with normalized gene expression matrix (.X)
- Normalized count matrix (output from normalize_total)

## Outputs

- AnnData object with log1p-transformed gene expression in .X
- Log-transformed count matrix suitable for PCA and clustering

## How to apply

Apply the log1p (natural logarithm of 1 + x) transformation to the normalized expression matrix. This transformation stabilizes variance across genes with different expression levels, compresses the dynamic range of the data, and makes the distribution more suitable for linear methods like PCA. The addition of 1 prevents log(0) errors and ensures zeros remain zero. Perform this step after normalize_total but before identifying highly variable genes or computing PCA, as downstream methods assume log-transformed or comparable variance-stabilized input.

## Related tools

- **Scanpy** (Provides pp.log1p() function to apply log transformation to normalized expression matrices) — https://github.com/scverse/scanpy
- **anndata** (Data container (AnnData object) that stores gene expression matrix and transformation metadata) — https://github.com/scverse/anndata

## Examples

```
import scanpy as sc; adata = sc.datasets.pbmc3k(); sc.pp.normalize_total(adata); sc.pp.log1p(adata); sc.pp.highly_variable_genes(adata)
```

## Evaluation signals

- Verify that all zero values in the original matrix remain zero after log1p (log1p(0) = log(1) = 0)
- Check that the transformed values are non-negative and bounded by log1p(max_count)
- Confirm that the output AnnData object contains the transformed matrix in .X with same dimensions as input
- Verify downstream analysis (e.g., PCA) runs without errors and produces meaningful principal components
- Compare variance distribution across genes before and after transformation; variance should be more homogeneous in log scale

## Limitations

- Log1p transformation assumes the input is a count matrix; applying it to already log-transformed data will produce incorrect results
- The transformation does not perform true variance stabilization for all expression ranges—highly expressed genes may still dominate variance
- Log transformation can inflate noise in lowly expressed genes; highly variable gene selection after log transformation helps mitigate this
- The choice of log1p over other transformations (e.g., VST, Anscombe) is not discussed; log1p is conventional but not necessarily optimal for all datasets

## Evidence

- [other] Apply log1p transformation to stabilize variance: "Apply log1p transformation to stabilize variance."
- [other] Normalize-then-transform preprocessing workflow: "Apply normalize_total normalization to account for sequencing depth differences. 3. Apply log1p transformation to stabilize variance."
- [intro] Log transformation in the standard Scanpy preprocessing pipeline: "It includes preprocessing, visualization, clustering, trajectory inference and differential expression testing"
