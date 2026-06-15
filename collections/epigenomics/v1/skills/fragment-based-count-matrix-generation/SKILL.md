---
name: fragment-based-count-matrix-generation
description: Use when you have a backed AnnData object containing processed fragment data (stored in .obsm['fragment_paired'] or .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3216
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_0654
  tools:
  - SnapATAC2
  - Python
  - precellar
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

# fragment-based-count-matrix-generation

## Summary

Generate tile-based count matrices from single-cell ATAC-seq fragment data using paired-insertion counting strategy in SnapATAC2. This skill quantifies chromatin accessibility at fixed genomic intervals and produces dense or sparse count matrices suitable for downstream dimensionality reduction and clustering.

## When to use

You have a backed AnnData object containing processed fragment data (stored in .obsm['fragment_paired'] or .obsm['fragment_single']) from single-cell ATAC-seq and need to convert raw genomic fragments into a quantitative count matrix indexed by fixed genomic tiles for clustering, embedding, or differential analysis.

## When NOT to use

- Input data is already in the form of a peak-by-cell matrix or gene-by-cell matrix; use pp.make_peak_matrix or pp.make_gene_matrix instead.
- Fragment file has not been imported or processed; first convert BAM to fragment file using pp.make_fragment_file or pp.import_fragments.
- You need counts at peak regions rather than fixed tiles; use pp.make_peak_matrix with called or external peak coordinates.

## Inputs

- backed AnnData object with fragment data in .obsm['fragment_paired'] or .obsm['fragment_single']
- genomic fragment coordinates (chromosome, start, end, barcode)

## Outputs

- count matrix (n_obs × n_vars) indexed by genomic tiles and cell barcodes
- tile coordinate metadata (chromosome, start, end positions for each tile)
- sparse matrix with paired-insertion counts per cell per tile

## How to apply

Load the backed AnnData object containing fragment coordinates and invoke pp.add_tile_matrix with counting_strategy='paired_insertion' to aggregate fragment counts across non-overlapping genomic tiles (fixed intervals, typically 5 kb). The function processes paired-end fragments by counting insertions at each genomic position, then sums counts within each tile to generate a sparse count matrix with dimensions n_obs (cells) × n_vars (tiles). Verify the resulting matrix shape matches the number of cells and the expected number of tiles, and confirm that count values are non-zero and reasonably distributed across the tile-cell space (no unexpected sparsity or skew).

## Related tools

- **SnapATAC2** (Provides pp.add_tile_matrix function to generate tile-based count matrices from fragment data with paired-insertion counting strategy) — https://github.com/scverse/SnapATAC2
- **precellar** (Upstream preprocessing tool to convert raw fastq files and BAM alignments into fragment files compatible with SnapATAC2 count matrix generation) — https://github.com/regulatory-genomics/precellar
- **Python** (Host language for SnapATAC2 API and data manipulation)

## Examples

```
import snapatac2 as snap; adata = snap.read('fragments.h5ad', backed='r'); snap.pp.add_tile_matrix(adata, counting_strategy='paired_insertion'); print(adata.X.shape)
```

## Evaluation signals

- Count matrix shape (n_obs × n_vars) matches the number of cells and expected number of genomic tiles (e.g., ~600,000 tiles for 5 kb resolution across human genome).
- Matrix contains non-zero entries distributed across both cells and tiles; median non-zero count per cell is consistent with expected fragment complexity (typically 1,000–100,000 fragments per cell).
- No cells have zero counts across all tiles; no tiles have zero counts across all cells (or if present, they represent genuine biological absence, not data corruption).
- Sparsity (fraction of zero entries) is within expected range for ATAC-seq (typically 95–99% sparse); extremely dense or sparse matrices may indicate counting or filtering errors.
- Count distribution is right-skewed with a long tail, consistent with chromatin accessibility patterns (some tiles have high accessibility, most have low).

## Limitations

- Tile-based counting does not account for peak structure; accessibility hotspots may be smoothed across multiple tiles. For peak-aware analysis, use pp.make_peak_matrix instead.
- Fixed tile size (typically 5 kb) is a compromise between resolution and noise; smaller tiles increase sparsity, larger tiles sacrifice resolution. Choice should be motivated by downstream analysis goal and cell-type complexity.
- Paired-insertion counting assumes high-quality paired-end sequencing and correct fragment coordinate assignment; errors in fragment end prediction or barcode assignment will propagate into count matrix.
- SnapATAC2 scales to >10 million cells but matrix generation time and memory scale with both cell count and number of tiles; very large tile matrices may require disk-backed sparse formats.

## Evidence

- [other] SnapATAC2 provides a pp.add_tile_matrix function that generates count matrices from fragment data as part of its matrix operation workflow for single-cell ATAC-seq analysis.: "SnapATAC2 provides a pp.add_tile_matrix function that generates count matrices from fragment data as part of its matrix operation workflow for single-cell ATAC-seq analysis."
- [other] Invoke pp.add_tile_matrix with counting_strategy='paired_insertion' to quantify chromatin accessibility at fixed genomic intervals.: "Invoke pp.add_tile_matrix with counting_strategy='paired_insertion' to quantify chromatin accessibility at fixed genomic intervals."
- [other] Load backed AnnData object containing fragment data (stored in .obsm['fragment_paired'] or .obsm['fragment_single']).: "Load backed AnnData object containing fragment data (stored in .obsm['fragment_paired'] or .obsm['fragment_single'])."
- [readme] Blazingly fast preprocessing tools for BAM to fragment files conversion and count matrix generation.: "Blazingly fast preprocessing tools for BAM to fragment files conversion and count matrix generation."
- [methods] Matrix operation including pp.add_tile_matrix, pp.make_peak_matrix, pp.make_gene_matrix: "Matrix operation including pp.add_tile_matrix, pp.make_peak_matrix, pp.make_gene_matrix"
