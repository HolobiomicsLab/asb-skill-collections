---
name: leiden-clustering-resolution-optimization
description: Use when you have performed spectral dimension reduction on single-cell omics count matrices and wish to partition cells into discrete populations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3673
  - http://edamontology.org/topic_0654
  tools:
  - SnapATAC2
  - Python
  - tl.leiden
  - tl.macs3
  - tl.merge_peaks
  - Leiden
  - Scanpy
  - UMAP
derived_from:
- doi: 10.1038/s41592-023-02139-9
  title: snapatac2
evidence_spans:
- 'SnapATAC2: A Python/Rust package for single-cell epigenomics analysis'
- A Python/Rust package for single-cell epigenomics analysis
- tl.leiden
- tl.macs3
- tl.merge_peaks
- tl.leiden for clustering
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

# leiden-clustering-resolution-optimization

## Summary

Apply Leiden clustering to single-cell omics data (ATAC-seq, RNA-seq, Hi-C, methylation) with parameter tuning to identify optimal resolution values that yield biologically meaningful cluster assignments. This skill involves running the tl.leiden method on spectral embeddings and validating cluster quality through comparison with reference assignments or biological interpretation.

## When to use

You have performed spectral dimension reduction on single-cell omics count matrices and wish to partition cells into discrete populations. Use this skill when you need to discover cell types or states and want to systematically evaluate whether the chosen resolution produces clusters that align with known cell annotations, downstream peak calling results, or biological markers.

## When NOT to use

- Input is already annotated with ground-truth cell types and downstream biological validation is unnecessary.
- The analysis goal is to identify rare cell populations where you require soft clustering probabilities rather than hard assignments.
- Data has been pre-processed with a different clustering method (e.g., k-means or hierarchical clustering) and you are not re-optimizing.

## Inputs

- spectral eigenvector matrix (output from tl.spectral or tl.multi_spectral) embedded in AnnData .obsm
- AnnData object containing the embedding

## Outputs

- cluster assignment vector (integer categorical in AnnData .obs)
- UMAP coordinates for visualization (in .obsm)

## How to apply

Run tl.leiden on the spectral eigenvectors or other embedding matrix with the default resolution parameter as a starting point. The Leiden algorithm optimizes community detection by repeatedly merging and splitting partitions to maximize modularity. Compare the resulting cluster assignments and UMAP/embedding coordinates against reference annotations or expected cell type markers. If clusters appear over-fragmented or merged incorrectly, iterate resolution upward (finer granularity) or downward (coarser granularity). Validate by checking whether downstream analyses—such as peak calling grouped by cluster, or differential feature analysis—produce biologically coherent results. The article demonstrates this workflow on the pbmc10k_multiome dataset, where Leiden clustering on spectral embeddings successfully recovers documented PBMC subpopulations.

## Related tools

- **SnapATAC2** (unified framework providing tl.leiden clustering method, spectral embedding, and AnnData integration for single-cell omics) — https://github.com/scverse/SnapATAC2
- **Leiden** (underlying community detection algorithm optimized for modularity in cluster partitioning)
- **Scanpy** (compatible downstream analysis package for cell annotation, differential expression, and biological validation)
- **UMAP** (visualization method (tl.umap) for examining cluster separation and quality in 2D space)

## Examples

```
import snapatac2 as snap
adata = snap.pp.import_fragments(fragment_file='fragments.tsv.gz', chrom_sizes=chrom_sizes)
snap.pp.add_tile_matrix(adata)
snap.tl.spectral(adata, n_comps=30)
snap.tl.umap(adata)
snap.tl.leiden(adata, resolution=1.0)
print(adata.obs['leiden'].value_counts())
```

## Evaluation signals

- Cluster assignments match or closely approximate reference cell type annotations when available (e.g., documented PBMC subpopulations in the pbmc10k_multiome dataset).
- UMAP coordinates show clear visual separation between clusters with minimal overlap or scattered singleton points.
- Downstream peak calling (tl.macs3 in pseudo-bulk mode grouped by cluster) yields distinct peak sets per cluster that are concordant with known cell-type-specific chromatin accessibility.
- Silhouette coefficient or modularity score is stable across the chosen resolution, indicating robust partitioning.
- Differential feature analysis (marker_regions or diff_test) identifies biologically plausible cell-type-specific features with consistent effect sizes.

## Limitations

- Leiden clustering sensitivity to resolution parameter requires iterative tuning; no single 'universal' optimal resolution exists across all datasets.
- Spectral embedding and Leiden are deterministic given fixed random seeds, but parameter sweeps can be computationally expensive for >10 million cells.
- Cluster quality depends heavily on upstream preprocessing (fragment filtering, tile matrix generation, doublet removal); poor input matrices yield uninformative partitions regardless of resolution.
- The method assumes that cell populations correspond to distinct connected components in the spectral embedding space; overlapping or hierarchical populations may be misrepresented.

## Evidence

- [methods] tl.leiden for clustering: "tl.leiden for clustering"
- [intro] End-to-end analysis pipeline for single-cell ATAC-seq data, including preprocessing, dimension reduction, clustering, data integration, peak calling: "End-to-end analysis pipeline for single-cell ATAC-seq data, including preprocessing, dimension reduction, clustering, data integration, peak calling"
- [intro] Matrix-free spectral embedding algorithm that is applicable to a wide range of single-cell omics data, including single-cell ATAC-seq, single-cell RNA-seq, single-cell Hi-C, and single-cell: "Matrix-free spectral embedding algorithm that is applicable to a wide range of single-cell omics data, including single-cell ATAC-seq, single-cell RNA-seq, single-cell Hi-C"
- [other] Perform clustering using tl.leiden with default resolution parameter. Call peaks using tl.macs3 in pseudo-bulk mode grouped by cluster assignment.: "Perform clustering using tl.leiden with default resolution parameter. Call peaks using tl.macs3 in pseudo-bulk mode grouped by cluster assignment."
- [other] compare cluster assignments and UMAP coordinates to tutorial reference: "compare cluster assignments and UMAP coordinates to tutorial reference"
