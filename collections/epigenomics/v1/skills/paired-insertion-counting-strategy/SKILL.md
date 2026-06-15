---
name: paired-insertion-counting-strategy
description: Use when you have loaded fragment data from single-cell ATAC-seq experiments into a backed AnnData object (with fragments stored in .obsm['fragment_paired'] or .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3793
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_0654
  tools:
  - SnapATAC2
  - Python
  - precellar
  - AnnData
derived_from:
- doi: 10.1038/s41592-023-02139-9
  title: snapatac2
evidence_spans:
- 'SnapATAC2: A Python/Rust package for single-cell epigenomics analysis'
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

# paired-insertion-counting-strategy

## Summary

A fragment quantification method in SnapATAC2 that counts chromatin accessibility at fixed genomic tiles by processing paired-end insertion coordinates from single-cell ATAC-seq fragment data. This strategy generates a cell-by-tile count matrix suitable for downstream analysis of chromatin accessibility patterns.

## When to use

Apply this skill when you have loaded fragment data from single-cell ATAC-seq experiments into a backed AnnData object (with fragments stored in .obsm['fragment_paired'] or .obsm['fragment_single']) and need to quantify chromatin accessibility across fixed genomic intervals (tiles) rather than at predefined peaks or genes.

## When NOT to use

- Fragment data is unavailable or not loaded into the AnnData object structure
- Analysis goal requires peak-level or gene-level quantification instead of genome-wide tiles (use pp.make_peak_matrix or pp.make_gene_matrix respectively)
- Fragments have not been processed or validated for quality (remove low-quality fragments or cell barcodes first via pp.filter_cells)

## Inputs

- Backed AnnData object with fragment data in .obsm['fragment_paired'] or .obsm['fragment_single']
- Genomic interval specifications (tile width, typically 5 kb)

## Outputs

- Sparse count matrix (n_cells × n_tiles) stored in .X or designated matrix slot
- Updated AnnData object with tile-based accessibility counts

## How to apply

Invoke pp.add_tile_matrix with counting_strategy='paired_insertion' on a backed AnnData object containing fragment data. The function processes paired-end fragments by counting insertion events within fixed-width genomic tiles (typically 5 kb or user-specified width) across the entire genome. Each cell's fragment insertions are aggregated into bins, producing a sparse count matrix where rows are cells and columns are genomic tiles. After execution, verify the output matrix shape (n_obs × n_vars) matches the number of cells and expected tile coordinates, and confirm that count values are non-zero and distributed across cells and tiles with expected sparsity patterns typical of chromatin accessibility data.

## Related tools

- **SnapATAC2** (Provides pp.add_tile_matrix function for paired-insertion counting and tile-matrix generation from fragment data) — https://github.com/scverse/SnapATAC2
- **Python** (Programming language for executing SnapATAC2 functions and workflows)
- **precellar** (Upstream preprocessing tool for BAM-to-fragment conversion and quality control prior to tile-matrix generation) — https://github.com/regulatory-genomics/precellar
- **AnnData** (Data container format that stores fragment data and resulting tile-based count matrices)

## Examples

```
import snapatac2 as sa; adata = sa.read('data.h5ad', backed='r'); sa.pp.add_tile_matrix(adata, counting_strategy='paired_insertion'); print(adata.X.shape)
```

## Evaluation signals

- Output matrix shape matches expected dimensions (n_cells × n_tiles computed from genome size and tile width)
- Count matrix is non-sparse in expected regions; verify mean counts per cell are consistent with sequencing depth and typical ATAC-seq accessibility patterns
- No negative values in count matrix; all entries are non-negative integers
- Tile-based accessibility patterns are biologically coherent when visualized (e.g., accessible regions cluster with known regulatory elements or match peak-calling results)
- Row and column sums are reasonable; median counts per cell and per tile are consistent with input fragment density and genome coverage

## Limitations

- Paired-insertion counting assumes high-quality paired-end fragment data; unpaired or low-quality fragments may be excluded or misclassified
- Fixed tile size is a simplification; peaks or regulatory elements spanning multiple tiles or smaller than tile width may be diluted across bins
- Sparsity of resulting matrix increases with smaller tile widths; very fine resolution (e.g., 1 kb tiles) may require additional normalization or imputation for downstream analysis
- Method does not account for fragment length distribution or directionality; alternative counting strategies (e.g., peak-based or TSS-centered) may be more sensitive in specific regulatory contexts

## Evidence

- [other] SnapATAC2 provides a pp.add_tile_matrix function that generates count matrices from fragment data as part of its matrix operation workflow for single-cell ATAC-seq analysis.: "pp.add_tile_matrix function that generates count matrices from fragment data as part of its matrix operation workflow"
- [other] Invoke pp.add_tile_matrix with counting_strategy='paired_insertion' to quantify chromatin accessibility at fixed genomic intervals.: "Invoke pp.add_tile_matrix with counting_strategy='paired_insertion' to quantify chromatin accessibility at fixed genomic intervals"
- [methods] Matrix operation including pp.add_tile_matrix, pp.make_peak_matrix, pp.make_gene_matrix for different quantification strategies.: "Matrix operation including pp.add_tile_matrix, pp.make_peak_matrix, pp.make_gene_matrix"
- [other] Load backed AnnData object containing fragment data stored in .obsm['fragment_paired'] or .obsm['fragment_single'].: "Load backed AnnData object containing fragment data (stored in .obsm['fragment_paired'] or .obsm['fragment_single'])"
- [readme] Blazingly fast preprocessing tools for BAM to fragment files conversion and count matrix generation.: "Blazingly fast preprocessing tools for BAM to fragment files conversion and count matrix generation"
