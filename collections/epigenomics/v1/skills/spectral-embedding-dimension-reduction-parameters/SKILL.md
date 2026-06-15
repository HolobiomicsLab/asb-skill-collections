---
name: spectral-embedding-dimension-reduction-parameters
description: Use when after generating a tile matrix or feature count matrix from single-cell ATAC-seq, RNA-seq, Hi-C, or methylation data, before clustering or UMAP visualization, when you need unsupervised dimension reduction that scales to millions of cells and is agnostic to the underlying data modality.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0622
  - http://edamontology.org/topic_3673
  tools:
  - SnapATAC2
  - Python
  - tl.spectral
  - tl.macs3
  - tl.merge_peaks
  - Leiden
  - UMAP
  - Scanpy
derived_from:
- doi: 10.1038/s41592-023-02139-9
  title: snapatac2
evidence_spans:
- 'SnapATAC2: A Python/Rust package for single-cell epigenomics analysis'
- A Python/Rust package for single-cell epigenomics analysis
- tl.spectral
- tl.macs3
- tl.merge_peaks
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/epigenomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_snapatac2
    doi: 10.1038/s41592-023-02139-9
    title: snapatac2
  dedup_kept_from: coll_snapatac2
schema_version: 0.2.0
---

# Spectral-embedding dimension reduction parameters

## Summary

Configure and apply matrix-free spectral embedding for dimension reduction on single-cell ATAC-seq and multi-omics data, selecting appropriate similarity metrics and embedding parameters to preserve cell-state structure prior to clustering and visualization.

## When to use

After generating a tile matrix or feature count matrix from single-cell ATAC-seq, RNA-seq, Hi-C, or methylation data, before clustering or UMAP visualization, when you need unsupervised dimension reduction that scales to millions of cells and is agnostic to the underlying data modality. Apply this step when the raw feature matrix is too high-dimensional for downstream clustering or when you need to integrate multi-modal single-cell data.

## When NOT to use

- Input data is already a low-dimensional embedding (e.g., pre-computed PCA or UMAP coordinates); apply clustering directly instead.
- Single-cell ATAC-seq data has not been preprocessed (e.g., barcodes not yet assigned, fragments not imported); run pp.import_fragments and pp.add_tile_matrix first.
- You require a linear embedding for interpretability of feature contributions; PCA or factor analysis may be more appropriate than spectral methods.

## Inputs

- AnnData object with tile matrix (pp.add_tile_matrix) or count matrix (pp.make_peak_matrix, pp.make_gene_matrix)
- Paired-end ATAC-seq fragment counts or equivalent feature counts for other modalities
- Optional: multiple aligned count matrices for co-embedding

## Outputs

- Spectral eigenvectors stored in adata.obsm (typically 'X_spectral')
- UMAP coordinates derived from spectral embedding (adata.obsm['X_umap'])
- Leiden cluster assignments using spectral eigenvectors as input

## How to apply

Call tl.spectral on the tile matrix or count matrix, specifying the similarity metric (e.g., cosine similarity for ATAC-seq) and the number of dimensions to retain. The matrix-free algorithm avoids materializing the full feature matrix, making it suitable for large datasets. The resulting eigenvectors become the input to UMAP visualization or clustering algorithms (e.g., Leiden). For multi-omics integration, use tl.multi_spectral with aligned modality matrices to produce a joint embedding. Verify that the spectral eigenvectors capture expected biological structure by checking that subsequent UMAP coordinates and Leiden cluster assignments match reference cell-type annotations.

## Related tools

- **SnapATAC2** (Python/Rust package implementing matrix-free spectral embedding (tl.spectral, tl.multi_spectral) and downstream clustering and visualization) — https://github.com/scverse/SnapATAC2
- **Leiden** (Clustering algorithm applied to spectral eigenvectors via tl.leiden for community detection)
- **UMAP** (Visualization algorithm applied to spectral eigenvectors via tl.umap to generate 2D scatter plots)
- **Scanpy** (Seamless integration for downstream single-cell analysis workflows)

## Examples

```
import snapatac2 as snap; adata = snap.datasets.pbmc10k_multiome(); snap.pp.import_fragments(adata); snap.pp.add_tile_matrix(adata); snap.tl.spectral(adata, metric='cosine'); snap.tl.umap(adata); snap.tl.leiden(adata)
```

## Evaluation signals

- Spectral eigenvectors show clear separation by known cell type in subsequent UMAP coordinates (visual inspection of adata.obs annotations overlaid on X_umap).
- Leiden cluster assignments derived from spectral eigenvectors match reference single-cell type labels from the pbmc10k_multiome dataset (e.g., expected T cells, B cells, monocytes segregate in distinct clusters).
- Cosine similarity metric produces non-degenerate spectrum of eigenvalues (no collapsed or near-identical eigenvalues indicating rank deficiency in the tile matrix).
- Eigenvectors are reproducible across independent runs with the same random seed; standard deviation of cluster centroids in spectral space is <0.5 for stable clusters.
- Peak calling (tl.macs3) on Leiden clusters derived from spectral embedding identifies known open chromatin regions and transcription factor binding sites consistent with cell-type identity.

## Limitations

- Matrix-free spectral embedding is sensitive to the choice of similarity metric; cosine similarity is recommended for ATAC-seq but may not be optimal for sparse count data with extreme sparsity (>99% zeros).
- Spectral embedding does not account for batch effects or technical confounders; pre-filtering with pp.filter_cells and pp.select_features is necessary to remove low-quality cells and reduce noise.
- Multi-spectral co-embedding (tl.multi_spectral) requires that input modalities are measured on the same set of cells with aligned cell indices; missing modality data or unbalanced sequencing depth can bias the joint embedding.
- Parameter selection (number of spectral dimensions, resolution of Leiden clustering) is not data-adaptive; tuning may be required for datasets with unusual cell-type compositions or technical properties.

## Evidence

- [intro] Matrix-free spectral embedding algorithm applicable to single-cell ATAC-seq, RNA-seq, Hi-C, and methylation data: "Matrix-free spectral embedding algorithm that is applicable to a wide range of single-cell omics data, including single-cell ATAC-seq, single-cell RNA-seq, single-cell Hi-C, and single-cell"
- [methods] Spectral embedding is applied via tl.spectral and tl.multi_spectral with dimension reduction and co-embedding: "tl.spectral, tl.multi_spectral, tl.umap for embeddings"
- [intro] End-to-end analysis pipeline includes dimension reduction as a core step before clustering and peak calling: "End-to-end analysis pipeline for single-cell ATAC-seq data, including preprocessing, dimension reduction, clustering, data integration, peak calling"
- [methods] Spectral embedding is followed by Leiden clustering and UMAP visualization in the documented workflow: "tl.leiden, tl.kmeans, tl.dbscan, tl.hdbscan for clustering"
- [intro] Scalability of spectral embedding to millions of cells is a key feature: "Scale to more than 10 million cells."
