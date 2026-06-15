---
name: cluster-umap-layout-reproducibility-benchmarking
description: Use when you have executed an end-to-end SnapATAC2 pipeline on the pbmc10k_multiome dataset (or a similar single-cell ATAC-seq dataset with a published reference) and need to validate that spectral embedding, Leiden clustering, and UMAP layout have converged to expected cluster identities and.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3643
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_3674
  - http://edamontology.org/topic_3391
  tools:
  - SnapATAC2
  - Python
  - tl.umap
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
- tl.umap
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

# cluster-umap-layout-reproducibility-benchmarking

## Summary

Verify that a single-cell ATAC-seq analysis pipeline produces reproducible cluster assignments and UMAP coordinates by comparing observed outputs against a documented reference implementation. This skill ensures that dimension reduction, clustering, and visualization steps have been correctly applied and yield consistent results.

## When to use

Apply this skill when you have executed an end-to-end SnapATAC2 pipeline on the pbmc10k_multiome dataset (or a similar single-cell ATAC-seq dataset with a published reference) and need to validate that spectral embedding, Leiden clustering, and UMAP layout have converged to expected cluster identities and coordinate distributions. Use it after calling tl.spectral, tl.leiden, and tl.umap to confirm the pipeline has not diverged from the documented workflow.

## When NOT to use

- Data has not yet been processed through pp.import_fragments and pp.add_tile_matrix—comparison requires fully preprocessed tile matrices.
- No reference implementation or published cluster assignments are available for the dataset—reproducibility benchmarking requires a ground truth to compare against.
- The dataset is substantially different from the reference (e.g., different cell type composition, different species, or very different sequencing depth)—reproducibility metrics may be uninformative if the underlying biology differs.

## Inputs

- AnnData object with tile matrix generated via pp.add_tile_matrix (rows: cells, columns: genomic tiles; values: paired-insertion counts)
- Spectral eigenvectors computed by tl.spectral (shape: n_cells × n_components)
- Leiden cluster assignments (categorical, one per cell)
- UMAP coordinates (shape: n_cells × 2)
- Reference cluster assignments and UMAP layouts from published tutorial or prior validated run

## Outputs

- Comparison metrics: adjusted Rand index (ARI), purity, or homogeneity between observed and reference cluster assignments
- Correlation coefficient (Pearson r) between observed and reference cluster-averaged UMAP coordinates
- Paired UMAP visualizations (observed vs. reference) for visual assessment of layout consistency
- Cluster composition table (number of cells per cluster, cell type annotations if available)
- Report indicating pass/fail status against reproducibility thresholds

## How to apply

After completing spectral embedding dimension reduction using tl.spectral with cosine similarity metric, perform Leiden clustering with default resolution parameter on the resulting eigenvectors. Generate UMAP visualization using tl.umap applied to the spectral coordinates. Extract cluster assignments and UMAP coordinates from the resulting AnnData object and compare them quantitatively to reference values from the published tutorial or a validated previous run: check that cluster identities match (using adjusted Rand index or purity metrics), and verify that UMAP coordinates fall within expected ranges or show expected spatial segregation of cell types. Visualize both observed and reference UMAP layouts side-by-side to identify gross deviations. Minor coordinate shifts are expected due to stochastic initialization in UMAP and Leiden; use reproducibility thresholds (e.g., Pearson correlation >0.95 for cluster-averaged coordinates) rather than exact matching.

## Related tools

- **SnapATAC2** (Execute spectral embedding, Leiden clustering, and UMAP layout; provide AnnData container for cluster assignments and coordinates) — https://github.com/scverse/SnapATAC2
- **Leiden** (Community detection algorithm used by tl.leiden for cluster assignment)
- **UMAP** (Dimensionality reduction and visualization algorithm used by tl.umap for 2D layout)
- **Scanpy** (Used for downstream analysis and interoperability with SnapATAC2 via AnnData format)

## Examples

```
import snapatac2 as snap; import numpy as np; adata = snap.datasets.pbmc10k_multiome(); snap.pp.import_fragments(adata); snap.pp.add_tile_matrix(adata); snap.tl.spectral(adata, cosine=True); snap.tl.umap(adata); observed_ari = adjusted_rand_score(reference_clusters, adata.obs['leiden']); observed_corr = np.corrcoef(adata.obsm['X_umap'].mean(axis=0), ref_umap.mean(axis=0)); print(f'ARI={observed_ari:.3f}, UMAP correlation={observed_corr[0,1]:.3f}')
```

## Evaluation signals

- Adjusted Rand Index (ARI) between observed and reference cluster assignments ≥ 0.90, indicating strong agreement in cell-to-cluster mappings.
- Pearson correlation of cluster-averaged UMAP coordinates (observed vs. reference) ≥ 0.95 in both X and Y dimensions.
- Cluster sizes (cell counts per cluster) within 10–15% of reference values, accounting for stochastic sampling in clustering.
- Visual inspection: reference and observed UMAP layouts show identical cluster segregation patterns and cell-type spatial organization.
- Leiden clustering with identical parameters (default resolution) and same spectral eigenvectors reproducibly recovers the same number of clusters and cell-type labels across independent runs.

## Limitations

- UMAP and Leiden both contain stochastic elements (random initialization, tie-breaking); perfect coordinate reproducibility is not expected or achievable without fixing random seeds.
- Spectral embedding is deterministic given cosine-normalized tile matrix input, but minor numerical differences in linear algebra backends (e.g., NumPy vs. different BLAS implementations) can propagate to downstream coordinates.
- Reproducibility benchmarking is only meaningful for datasets and parameters that match the reference; changing cell-type composition, sequencing depth, or clustering resolution will shift results.
- The article does not specify quantitative thresholds for 'acceptable' divergence; practitioners must define their own pass/fail criteria based on domain knowledge and prior runs.

## Evidence

- [methods] Perform spectral embedding dimension reduction using tl.spectral with cosine similarity metric on tile matrix.: "Perform spectral embedding dimension reduction using tl.spectral with cosine similarity metric."
- [methods] Generate UMAP visualization using tl.umap applied to spectral eigenvectors.: "Generate UMAP visualization using tl.umap on spectral eigenvectors."
- [methods] Perform clustering using tl.leiden with default resolution parameter.: "Perform clustering using tl.leiden with default resolution parameter."
- [other] SnapATAC2 provides an end-to-end analysis pipeline for single-cell ATAC-seq data that includes preprocessing, dimension reduction, clustering, data integration, and peak calling steps.: "SnapATAC2 provides an end-to-end analysis pipeline for single-cell ATAC-seq data that includes preprocessing, dimension reduction, clustering, data integration, and peak calling steps."
- [methods] Compare cluster assignments and UMAP coordinates to tutorial reference.: "compare cluster assignments and UMAP coordinates to tutorial reference."
- [intro] Matrix-free spectral embedding algorithm that is applicable to a wide range of single-cell omics data, including single-cell ATAC-seq: "Matrix-free spectral embedding algorithm that is applicable to a wide range of single-cell omics data, including single-cell ATAC-seq"
- [readme] Seamless integration with other single-cell analysis packages such as Scanpy.: "Seamless integration with other single-cell analysis packages such as Scanpy."
