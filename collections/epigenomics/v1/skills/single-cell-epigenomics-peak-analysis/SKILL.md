---
name: single-cell-epigenomics-peak-analysis
description: Use when you have preprocessed single-cell ATAC-seq fragment files or count matrices and need to identify open chromatin regions (peaks) to support downstream differential accessibility analysis, motif discovery, or regulatory network inference.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3680
  edam_topics:
  - http://edamontology.org/topic_3674
  - http://edamontology.org/topic_0749
  tools:
  - SnapATAC2
  - tl.diff_test
  - datasets.cis_bp
  - Python
  - pp.make_tile_matrix
  - pp.make_peak_matrix
  - tl.spectral
  - tl.macs3
  - tl.merge_peaks
  - Scanpy
derived_from:
- doi: 10.1038/s41592-023-02139-9
  title: snapatac2
evidence_spans:
- 'SnapATAC2: A Python/Rust package for single-cell epigenomics analysis'
- tl.marker_regions, tl.diff_test for differential analysis
- datasets.cis_bp
- A Python/Rust package for single-cell epigenomics analysis
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

# single-cell-epigenomics-peak-analysis

## Summary

Identifies and characterizes chromatin accessibility peaks in single-cell ATAC-seq data using spectral embedding and peak-calling algorithms. This skill enables discovery of cell-type-specific regulatory regions and their enrichment for transcription factor motifs.

## When to use

Apply this skill when you have preprocessed single-cell ATAC-seq fragment files or count matrices and need to identify open chromatin regions (peaks) to support downstream differential accessibility analysis, motif discovery, or regulatory network inference. Use it after BAM-to-fragment conversion and cell filtering but before comparing accessibility between cell populations.

## When NOT to use

- Input is already a curated set of consensus peaks from bulk ATAC-seq or ChIP-seq; skip to motif enrichment or annotation.
- Single-cell data lacks sufficient sequencing depth (~5,000 fragments per cell minimum); peak calling will be unreliable.
- Analyzing bulk ATAC-seq or RNA-seq data; use bulk peak callers (MACS2, ENCODE pipeline) instead.

## Inputs

- BAM or fragment files (TSV or gzipped format)
- Cell barcodes and metadata (cell-type annotations or cluster assignments)
- Reference genome (optional; for peak annotation)

## Outputs

- Peak count matrix (.h5ad AnnData object with peaks × cells)
- Peak coordinates (BED format or interval table)
- Spectral embedding coordinates (low-dimensional representation)
- Differential accessibility results (peak IDs, log2-fold-change, p-values)

## How to apply

Begin by constructing a tile matrix or peak matrix from fragment files using pp.make_tile_matrix or pp.make_peak_matrix. Apply dimension reduction via matrix-free spectral embedding (tl.spectral) to embed cells in a low-dimensional space, which enables clustering and visualization without materializing the full count matrix. Perform peak calling using tl.macs3 (or merge peaks across cell types with tl.merge_peaks) to define consensus peak sets. For peaks identified as differentially accessible via tl.diff_test, validate peak quality by checking for non-zero counts and reasonable distribution of peak widths. The spectral embedding is scalable to >10 million cells and supports integration with downstream tools (Scanpy, peak annotation) via AnnData format.

## Related tools

- **SnapATAC2** (Python/Rust framework for spectral embedding, peak calling, and differential analysis of single-cell ATAC-seq data) — https://github.com/scverse/SnapATAC2
- **pp.make_tile_matrix** (Generate fixed-width tile matrix from fragment files for spectral embedding) — https://github.com/scverse/SnapATAC2
- **pp.make_peak_matrix** (Generate peak count matrix from fragment files using predefined peak coordinates) — https://github.com/scverse/SnapATAC2
- **tl.spectral** (Matrix-free spectral embedding for dimension reduction without materializing full count matrix) — https://github.com/scverse/SnapATAC2
- **tl.macs3** (Peak calling to identify chromatin accessibility regions within single-cell ATAC-seq data) — https://github.com/scverse/SnapATAC2
- **tl.merge_peaks** (Merge and consolidate peaks across cell types or clusters to define consensus peak set) — https://github.com/scverse/SnapATAC2
- **tl.diff_test** (Differential accessibility testing to identify peaks enriched in specific cell populations) — https://github.com/scverse/SnapATAC2
- **Scanpy** (Integration framework for downstream single-cell analysis (clustering, annotation) with SnapATAC2 outputs)

## Examples

```
import snapatac2 as snap; adata = snap.pp.make_tile_matrix(snap.io.read_h5ad('fragments.h5ad')); snap.tl.spectral(adata, random_state=0); snap.tl.macs3(adata); snap.tl.diff_test(adata, groupby='cell_type')
```

## Evaluation signals

- Peak count matrix is non-empty and sparse (median non-zero entries per cell >100 and <0.5% density), consistent with ATAC-seq sparsity.
- Spectral embedding coordinates have low reconstruction error and embed cells such that k-nearest neighbors within a cluster have higher accessibility correlation than cross-cluster pairs.
- Peak width distribution is reasonable (median 300–500 bp for mammalian data); peaks should not be extremely narrow (<50 bp) or broad (>10 kb).
- Differentially accessible peaks (tl.diff_test output) show expected p-value distribution with enrichment at small p-values and minimal bias toward specific regions or cell types.
- AnnData .h5ad file contains all required slots (X, obs, var) with no null values in peak ID, chromosome, start, and end columns.

## Limitations

- Peak calling accuracy depends on sequencing depth; low-coverage cells (<5,000 fragments) may fail or produce spurious peaks.
- Spectral embedding scales well to >10 million cells but requires tuning of neighborhood parameters (n_neighbors, n_components) for optimal results.
- SnapATAC2 outputs are in AnnData format; integration with non-scverse tools (e.g., Seurat, Cell Ranger) requires format conversion.
- Motif enrichment analysis (tl.motif_enrichment) is performed post-hoc on differential peaks; it does not directly inform peak calling and may miss rare TF binding sites.

## Evidence

- [readme] End-to-end analysis pipeline for single-cell ATAC-seq data, including preprocessing, dimension reduction, clustering, data integration, peak calling, differential analysis, motif analysis, regulatory network analysis.: "End-to-end analysis pipeline for single-cell ATAC-seq data, including preprocessing, dimension reduction, clustering, data integration, peak calling, differential analysis, motif analysis, regulatory"
- [methods] Matrix-free spectral embedding algorithm that is applicable to a wide range of single-cell omics data, including single-cell ATAC-seq, single-cell RNA-seq, single-cell Hi-C, and single-cell methylation.: "Matrix-free spectral embedding algorithm that is applicable to a wide range of single-cell omics data, including single-cell ATAC-seq, single-cell RNA-seq, single-cell Hi-C, and single-cell"
- [intro] Scale to more than 10 million cells.: "Scale to more than 10 million cells."
- [methods] tl.macs3, tl.merge_peaks for peak calling: "tl.macs3, tl.merge_peaks for peak calling"
- [methods] tl.marker_regions, tl.diff_test for differential analysis: "tl.marker_regions, tl.diff_test for differential analysis"
- [readme] Blazingly fast preprocessing tools for BAM to fragment files conversion and count matrix generation.: "Blazingly fast preprocessing tools for BAM to fragment files conversion and count matrix generation."
