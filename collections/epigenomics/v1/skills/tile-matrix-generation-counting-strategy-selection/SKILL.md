---
name: tile-matrix-generation-counting-strategy-selection
description: Use when after importing fragment files into AnnData using pp.import_fragments and before performing spectral embedding (tl.spectral) or other dimension reduction.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3791
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_0654
  - http://edamontology.org/topic_3957
  tools:
  - SnapATAC2
  - Python
  - pp.add_tile_matrix
  - tl.macs3
  - tl.merge_peaks
  - pp.import_fragments
  - tl.spectral
  - AnnData
derived_from:
- doi: 10.1038/s41592-023-02139-9
  title: snapatac2
evidence_spans:
- 'SnapATAC2: A Python/Rust package for single-cell epigenomics analysis'
- A Python/Rust package for single-cell epigenomics analysis
- pp.add_tile_matrix
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

# tile-matrix-generation-counting-strategy-selection

## Summary

Select and apply an appropriate counting strategy (e.g., paired-insertion counting) when generating a tile matrix from ATAC-seq fragment data in SnapATAC2. This skill bridges fragment-level preprocessing and downstream spectral embedding by converting raw alignments into a discrete feature matrix suitable for dimension reduction.

## When to use

After importing fragment files into AnnData using pp.import_fragments and before performing spectral embedding (tl.spectral) or other dimension reduction. Apply this skill when you have paired-end ATAC-seq data with properly formatted fragment coordinates and need to represent chromatin accessibility as a tile-by-cell count matrix for clustering and visualization.

## When NOT to use

- Input is already a peak-by-cell or gene-by-cell count matrix (use directly for embedding instead).
- Fragment data contains single-end reads without paired mate information (requires alternative counting strategy or realignment).
- Analysis goal is peak-level rather than genome-wide accessibility profiling (use pp.make_peak_matrix instead).

## Inputs

- AnnData object with imported fragment data (adata with obs column containing cell barcodes and var containing genomic coordinates from pp.import_fragments)
- Reference genome assembly or chrom.sizes file defining tile boundaries

## Outputs

- AnnData object with tile matrix added as a sparse count matrix (adata.X or named layer)
- Tile coordinates in adata.var indexed by genomic position (chr:start-end)

## How to apply

Use SnapATAC2's pp.add_tile_matrix function with paired-insertion counting strategy, which counts the number of Tn5 insertions falling within non-overlapping genomic tiles (typically 5 kb). The paired-insertion strategy correctly handles paired-end reads by counting each valid fragment pair once, avoiding double-counting and artificial noise from single-end artefacts. This produces a sparse, binary or count matrix indexed by tile coordinates and cell barcodes. Validate that the resulting matrix has non-zero coverage across cell populations and that tile counts correlate with expected chromatin accessibility patterns before proceeding to embedding.

## Related tools

- **SnapATAC2** (Primary framework providing pp.add_tile_matrix function and paired-insertion counting strategy implementation) — https://github.com/scverse/SnapATAC2
- **pp.import_fragments** (Upstream preprocessing function that loads raw fragment files into AnnData before tile matrix generation) — https://github.com/scverse/SnapATAC2
- **tl.spectral** (Downstream dimension reduction tool applied to the tile matrix for embedding) — https://github.com/scverse/SnapATAC2
- **AnnData** (Data container that stores tile matrix, cell metadata, and tile coordinates)

## Examples

```
import snapatac2 as snap; adata = snap.pp.add_tile_matrix(adata, n_jobs=8); print(adata.X.shape, adata.var_names[:5])
```

## Evaluation signals

- Tile matrix dimensions match expected number of tiles (e.g., ~600k tiles for 5 kb resolution on hg38) and number of cells in fragment import.
- Sparsity of tile matrix is consistent with ATAC-seq (typically 95–99% zeros); very dense or very sparse matrices suggest counting errors.
- Cell-level coverage statistics (total insertions per cell) are comparable across cell populations and match fragment import statistics.
- UMAP or spectral embedding computed on tile matrix visually separates known cell types or clusters consistent with published reference (e.g., pbmc10k_multiome tutorial).
- Tile matrix correlates with known peak regions from parallel peak-calling experiments (e.g., peaks called with tl.macs3 should overlap high-coverage tiles).

## Limitations

- Tile size (typically 5 kb) is a fixed hyperparameter that cannot be easily adjusted post-hoc; very small tiles may be too sparse, very large tiles may obscure fine-grained chromatin structure.
- Paired-insertion strategy requires high-quality fragment files with correct mate pairing; incorrectly paired or single-end-only fragments will be discarded or cause errors.
- SnapATAC2's tile matrix is memory-resident in AnnData format; scaling to >10 million cells requires sparse matrix compression and may require high-memory compute nodes.
- Tile counts are sensitive to sequencing depth and library quality; samples with vastly different coverage may require explicit normalization before downstream analysis.

## Evidence

- [other] Generate tile matrix using pp.add_tile_matrix with paired-insertion counting strategy: "Generate tile matrix using pp.add_tile_matrix with paired-insertion counting strategy."
- [methods] Fragment file processing and matrix operations are core workflow steps: "Fragment file processing with pp.make_fragment_file, pp.import_fragments; Matrix operation including pp.add_tile_matrix, pp.make_peak_matrix, pp.make_gene_matrix"
- [intro] End-to-end pipeline workflow includes preprocessing and matrix generation before dimension reduction: "End-to-end analysis pipeline for single-cell ATAC-seq data, including preprocessing, dimension reduction, clustering, data integration, peak calling"
- [intro] Blazingly fast preprocessing enables count matrix generation as part of core workflow: "Blazingly fast preprocessing tools for BAM to fragment files conversion and count matrix generation."
- [readme] SnapATAC2 scales to millions of cells with efficient preprocessing: "Scale to more than 10 million cells."
