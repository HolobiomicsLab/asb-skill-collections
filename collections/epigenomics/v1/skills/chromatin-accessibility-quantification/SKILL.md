---
name: chromatin-accessibility-quantification
description: Use when you have a backed AnnData object populated with fragment coordinates (stored in .obsm['fragment_paired'] or .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3565
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_0102
  - http://edamontology.org/topic_0749
  tools:
  - SnapATAC2
  - Python
  - Rust
  - TOBIAS
  - TOBIAS ATACorrect
  - TOBIAS ScoreBigwig
  - TOBIAS PlotAggregate / PlotTracks
  - TOBIAS BINDetect
derived_from:
- doi: 10.1038/s41592-023-02139-9
  title: snapatac2
- doi: 10.1038/s41467-020-18035-1
  title: ''
evidence_spans:
- 'SnapATAC2: A Python/Rust package for single-cell epigenomics analysis'
- A Python/Rust package for single-cell epigenomics analysis
- '**TOBIAS** is a collection of command-line bioinformatics tools for performing footprinting analysis on ATAC-seq data'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/epigenomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_snapatac2
    doi: 10.1038/s41592-023-02139-9
    title: snapatac2
  - build: coll_tobias
    doi: 10.1038/s41467-020-18035-1
    title: tobias
  dedup_kept_from: coll_snapatac2
schema_version: 0.2.0
---

# chromatin-accessibility-quantification

## Summary

Quantify chromatin accessibility across the genome at fixed genomic intervals (tiles) from single-cell ATAC-seq fragment data using SnapATAC2's paired-insertion counting strategy. This skill converts aligned fragment coordinates and cell barcodes into a sparse count matrix suitable for downstream analysis.

## When to use

You have a backed AnnData object populated with fragment coordinates (stored in .obsm['fragment_paired'] or .obsm['fragment_single']) from aligned single-cell ATAC-seq data and need to generate a tile-based count matrix to quantify chromatin accessibility for clustering, embedding, or peak discovery.

## When NOT to use

- Fragment data has not yet been loaded or parsed into the AnnData object—use pp.import_fragments or pp.make_fragment_file first.
- You require peak-level counts instead of fixed-interval tiles—use pp.make_peak_matrix instead.
- Input is already a pre-computed feature matrix; tiling and counting would be redundant.

## Inputs

- Backed AnnData object with fragment data in .obsm['fragment_paired'] or .obsm['fragment_single']
- Cell barcodes (stored in .obs)
- Fragment coordinates (chromosome, start, end) and quality metrics

## Outputs

- Tile-based count matrix (n_obs × n_vars, sparse format)
- Tile coordinate metadata (genomic positions of each bin)
- QC metrics (fragment counts per cell, sparsity)

## How to apply

Load your backed AnnData object containing pre-parsed fragment data. Invoke pp.add_tile_matrix with counting_strategy='paired_insertion' to assign each fragment pair to fixed genomic tiles (default tile size is typically 5 kb) and count the number of fragments per tile per cell. The function scans all fragments, maps their coordinates to tile bins, and aggregates counts by cell barcode and tile ID. Verify that the resulting count matrix has shape (n_obs × n_vars) matching the number of cells and tiles, and confirm non-zero entries are distributed across both cells and genomic regions, indicating successful quantification.

## Related tools

- **SnapATAC2** (Core preprocessing and matrix generation framework; provides pp.add_tile_matrix function for paired-insertion counting and tile-based quantification.) — https://github.com/scverse/SnapATAC2
- **Python** (Scripting language for invoking SnapATAC2 functions and manipulating AnnData objects.)
- **Rust** (Backend performance-critical implementation of tile binning and fragment counting logic in SnapATAC2.)

## Examples

```
import snapatac2 as sa; adata = sa.read('fragments.h5ad'); sa.pp.add_tile_matrix(adata, counting_strategy='paired_insertion'); print(adata.X.shape, adata.X.nnz)
```

## Evaluation signals

- Output count matrix shape matches expected dimensions: n_obs = number of cells, n_vars = number of genomic tiles.
- Count matrix contains non-zero entries; sparsity is >90% but distribution is non-uniform across cells and regions (not all zeros or all ones).
- Tile coordinates are correctly positioned and non-overlapping; genomic ranges follow chromosome order.
- Fragment counts per cell (sum over all tiles) are consistent with raw fragment file; no data loss during binning.
- QC metrics (duplication rate, read counts per cell) remain accessible and match pre-quantification fragment-level QC.

## Limitations

- Tile size is fixed and predetermined; the method does not adapt tile width to local chromatin structure or peak density.
- Paired-insertion counting assumes that fragment pairs are correctly linked by cell barcode; miscoded or ambiguous barcodes will lead to count inflation or loss.
- The approach does not account for fragment length bias or GC content; normalization may be needed in downstream analysis.
- Memory usage scales with the number of tiles and cells; very large genomes or very high resolution tiling can exceed available RAM even with backed AnnData.

## Evidence

- [other] Load backed AnnData object containing fragment data (stored in .obsm['fragment_paired'] or .obsm['fragment_single']). Invoke pp.add_tile_matrix with counting_strategy='paired_insertion' to quantify chromatin accessibility at fixed genomic intervals.: "Load backed AnnData object containing fragment data (stored in .obsm['fragment_paired'] or .obsm['fragment_single']). Invoke pp.add_tile_matrix with counting_strategy='paired_insertion' to quantify"
- [other] Extract the resulting count matrix and verify matrix shape (n_obs × n_vars) matches tile coordinates. Validate that count matrix contains non-zero entries and that paired-insertion counts are distributed across cells and genomic tiles as expected.: "Extract the resulting count matrix and verify matrix shape (n_obs × n_vars) matches tile coordinates. Validate that count matrix contains non-zero entries and that paired-insertion counts are"
- [methods] Matrix operation including pp.add_tile_matrix, pp.make_peak_matrix, pp.make_gene_matrix: "Matrix operation including pp.add_tile_matrix, pp.make_peak_matrix, pp.make_gene_matrix"
- [intro] Blazingly fast preprocessing tools for BAM to fragment files conversion and count matrix generation.: "Blazingly fast preprocessing tools for BAM to fragment files conversion and count matrix generation."
