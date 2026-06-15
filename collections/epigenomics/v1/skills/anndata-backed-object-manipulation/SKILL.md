---
name: anndata-backed-object-manipulation
description: Use when when working with large single-cell ATAC-seq or multi-omics datasets where in-memory storage is infeasible (>1M cells), and you need to iteratively add or modify count matrices (tile-based, peak-based, or gene-based) while preserving fragment-level data for reproducibility and re-analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3565
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_3673
  tools:
  - SnapATAC2
  - Python
  - precellar
  - Scanpy
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

# anndata-backed-object-manipulation

## Summary

Manipulate fully backed AnnData objects to store and access single-cell omics fragment data and count matrices without loading entire datasets into memory. This skill enables scalable preprocessing and matrix operations on datasets exceeding 10 million cells by leveraging on-disk storage.

## When to use

When working with large single-cell ATAC-seq or multi-omics datasets where in-memory storage is infeasible (>1M cells), and you need to iteratively add or modify count matrices (tile-based, peak-based, or gene-based) while preserving fragment-level data for reproducibility and re-analysis.

## When NOT to use

- Input data is already a dense in-memory count matrix; use backed AnnData only to avoid reprocessing raw fragments.
- Workflow requires frequent random access to all cells × features values (backed mode has I/O latency); consider in-memory AnnData for small datasets (<1M cells).
- Fragment data is unavailable or lost; count matrices cannot be regenerated with alternative binning strategies without raw sequencing alignments.

## Inputs

- backed AnnData object (.h5ad file on disk)
- fragment coordinate data stored in .obsm slots (paired-end or single-end fragment tuples)
- genomic interval definitions (tile coordinates, peak BED file, or gene GTF annotations)

## Outputs

- count matrix (stored in .X or .obsm of the same backed AnnData object)
- updated backed AnnData object with added matrix layer
- metadata about matrix binning (tile size, peak list, gene annotations)

## How to apply

Load or create a backed AnnData object using SnapATAC2's I/O functions, which stores dense arrays and sparse matrices on disk rather than in RAM. Store raw fragment coordinates in .obsm['fragment_paired'] or .obsm['fragment_single'] slots. Apply matrix operations (pp.add_tile_matrix, pp.make_peak_matrix, pp.make_gene_matrix) to generate count matrices from fragments; each operation reads from and writes to disk without materializing the full dataset. Verify matrix shape (n_obs × n_vars) and sparsity after each operation to confirm the count matrix reflects the intended genomic binning or feature selection.

## Related tools

- **SnapATAC2** (Provides pp.add_tile_matrix, pp.make_peak_matrix, pp.make_gene_matrix functions for matrix operations on backed AnnData; handles fragment data I/O and count aggregation) — https://github.com/scverse/SnapATAC2
- **precellar** (Upstream preprocessing: converts raw FASTQ files to fragment files (.tsv.zst) and count matrices that are input to backed AnnData workflows) — https://github.com/regulatory-genomics/precellar
- **Scanpy** (Companion library for seamless integration with backed AnnData objects; provides embedding and clustering on top of SnapATAC2 matrices)

## Examples

```
import snapatac2 as snap; adata = snap.read('data.h5ad', backed='r+'); snap.pp.add_tile_matrix(adata, counting_strategy='paired_insertion'); adata.write()
```

## Evaluation signals

- Verify that the backed AnnData object file size on disk grows incrementally with each matrix operation; no explosion to in-memory size.
- Check that .X (or intended .obsm key) contains the expected count matrix shape: n_obs = number of cells, n_vars = number of tiles/peaks/genes.
- Confirm matrix is sparse (majority zeros) and contains non-zero entries distributed across cells and genomic coordinates; spot-check a few cell × feature pairs for plausible counts.
- Run pp.filter_cells or pp.select_features on the matrix output to verify that downstream filtering operations read and write correctly to the backed object.
- Profile disk I/O latency: operations should complete in reasonable time (seconds to minutes per matrix depending on dataset size); significant slowdown may indicate backing strategy issues.

## Limitations

- Backed AnnData objects require consistent on-disk storage; file system failures or accidental deletion of .h5ad file causes data loss.
- Matrix operations are sequential and I/O-bound; random-access patterns (e.g., selecting arbitrary subsets of cells repeatedly) may be slower than in-memory alternatives.
- Fragment storage in .obsm as tuples or coordinate arrays can itself consume significant disk space for large datasets; compression (e.g., via precellar's .tsv.zst) is recommended upstream.
- Compatibility with older AnnData or SnapATAC2 versions may break if the backing format or .obsm schema changes.

## Evidence

- [readme] Implementation of fully backed AnnData.: "Implementation of fully backed AnnData."
- [other] Matrix operation including pp.add_tile_matrix, pp.make_peak_matrix, pp.make_gene_matrix: "Matrix operation including pp.add_tile_matrix, pp.make_peak_matrix, pp.make_gene_matrix"
- [other] Load backed AnnData object containing fragment data (stored in .obsm['fragment_paired'] or .obsm['fragment_single']). Invoke pp.add_tile_matrix with counting_strategy='paired_insertion': "Load backed AnnData object containing fragment data (stored in .obsm['fragment_paired'] or .obsm['fragment_single']). Invoke pp.add_tile_matrix with counting_strategy='paired_insertion'"
- [readme] Scale to more than 10 million cells.: "Scale to more than 10 million cells."
- [readme] Blazingly fast preprocessing tools for BAM to fragment files conversion and count matrix generation.: "Blazingly fast preprocessing tools for BAM to fragment files conversion and count matrix generation."
