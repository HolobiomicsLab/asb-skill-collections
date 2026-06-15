---
name: single-cell-atac-fragment-import-processing
description: Use when you have aligned single-cell ATAC-seq data as BAM files or fragment files (TSV format with genomic coordinates) and need to prepare it for spectral embedding, clustering, and peak calling. This is the entry point after alignment but before any dimension reduction or statistical analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_0654
  - http://edamontology.org/topic_3179
  tools:
  - SnapATAC2
  - Python
  - pp.import_fragments
  - tl.macs3
  - tl.merge_peaks
  - precellar
  - AnnData
derived_from:
- doi: 10.1038/s41592-023-02139-9
  title: snapatac2
evidence_spans:
- 'SnapATAC2: A Python/Rust package for single-cell epigenomics analysis'
- A Python/Rust package for single-cell epigenomics analysis
- pp.import_fragments
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

# single-cell-atac-fragment-import-processing

## Summary

Import aligned ATAC-seq fragment files into an AnnData object and generate a tile-based count matrix for downstream analysis. This preprocessing step converts BAM or fragment TSV inputs into a sparse, indexed matrix representation suitable for dimension reduction and clustering.

## When to use

You have aligned single-cell ATAC-seq data as BAM files or fragment files (TSV format with genomic coordinates) and need to prepare it for spectral embedding, clustering, and peak calling. This is the entry point after alignment but before any dimension reduction or statistical analysis.

## When NOT to use

- Input is already a peak-by-cell count matrix or feature table; use this only for raw fragment data.
- Fragment files are missing or corrupted; validate file integrity and coordinate format first.
- You need peak-level rather than tile-level resolution; defer peak calling until after clustering.

## Inputs

- BAM files (aligned single-cell ATAC-seq reads)
- Fragment TSV files (tab-delimited: chr, start, end, barcode, count)
- Cell barcode whitelist (optional, for filtering)

## Outputs

- AnnData object with tile matrix (.X as sparse CSR matrix)
- Cell metadata including barcode and QC metrics
- Tile feature names (genomic intervals)

## How to apply

First, import fragment files using pp.import_fragments with paired-end mode enabled, which reads fragment coordinate triplets (chromosome, start, end) and cell barcodes into an AnnData object. Then generate a tile matrix using pp.add_tile_matrix with a paired-insertion counting strategy, which bins the genome into fixed-width tiles (default 500 bp) and counts fragment insertions per tile per cell. This creates a sparse feature matrix where rows are tiles and columns are cells. The tile-based approach is matrix-free, scaling efficiently to millions of cells without materializing the full dense matrix. Verify that the resulting AnnData object has nonzero counts in the tile matrix and that cell and tile dimensions match expectations before proceeding to spectral embedding.

## Related tools

- **SnapATAC2** (Python/Rust package providing pp.import_fragments and pp.add_tile_matrix functions for ATAC-seq preprocessing) — https://github.com/scverse/SnapATAC2
- **precellar** (Upstream preprocessing package for converting raw FASTQ files to fragment TSV format via alignment) — https://github.com/regulatory-genomics/precellar
- **AnnData** (Data structure for storing the tile matrix, cell metadata, and feature annotations)

## Examples

```
import snapatac2 as snap; adata = snap.pp.import_fragments('fragments.tsv.gz', paired_end=True); snap.pp.add_tile_matrix(adata); print(adata.X.shape, adata.X.nnz)
```

## Evaluation signals

- AnnData object has a nonzero tile matrix (X attribute) with sparse CSR or CSC format and shape (n_cells, n_tiles).
- Cell metadata includes barcode identifiers; verify barcode count matches fragment file distinct barcodes.
- Tile features span the reference genome at expected intervals; spot-check a few tile names (chr:start-end format).
- Total insert counts per cell are reasonable (typically 1,000–100,000+ depending on sequencing depth); cells with <100 inserts or >outlier threshold may warrant QC filtering before downstream analysis.
- Matrix sparsity is >99% (typical for single-cell ATAC); dense or low-sparsity matrices may indicate processing errors.

## Limitations

- Tile matrix resolution is fixed by the tile size parameter (default 500 bp); peak-level resolution requires separate pp.make_peak_matrix step after peak calling.
- Fragment files must contain valid genomic coordinates; malformed or unaligned fragments are silently dropped or cause import errors.
- Large datasets (>10 million cells) require sufficient RAM for the sparse matrix and metadata; use disk-backed AnnData (h5ad format) to manage memory.
- Cell barcode filtering relies on an explicit whitelist; off-target barcodes may introduce noise if not provided.
- No built-in QC metrics for insert size distribution, mitochondrial contamination, or TSS enrichment at this step; apply pp.filter_cells or custom filters after import if needed.

## Evidence

- [methods] Import fragment files into AnnData using pp.import_fragments with paired-end mode: "Import fragment files into AnnData using pp.import_fragments with paired-end mode."
- [methods] Generate tile matrix using pp.add_tile_matrix with paired-insertion counting strategy: "Generate tile matrix using pp.add_tile_matrix with paired-insertion counting strategy."
- [intro] Blazingly fast preprocessing tools for BAM to fragment files conversion and count matrix generation: "Blazingly fast preprocessing tools for BAM to fragment files conversion and count matrix generation."
- [methods] Matrix operation including pp.add_tile_matrix, pp.make_peak_matrix, pp.make_gene_matrix: "Matrix operation including pp.add_tile_matrix, pp.make_peak_matrix, pp.make_gene_matrix"
- [intro] Matrix-free spectral embedding algorithm that is applicable to a wide range of single-cell omics data: "Matrix-free spectral embedding algorithm that is applicable to a wide range of single-cell omics data"
