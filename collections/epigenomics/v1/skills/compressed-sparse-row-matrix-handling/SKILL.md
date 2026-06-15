---
name: compressed-sparse-row-matrix-handling
description: Use when you have a raw or preprocessed single-cell count matrix (from BAM-to-fragment or FASTQ-to-matrix pipelines) and need to apply matrix-free algorithms like tl.spectral, tl.multi_spectral, or other scalable dimension reduction methods that require dense or sparse matrix input.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3673
  - http://edamontology.org/topic_0769
  tools:
  - SnapATAC2
  - Python
  - Rust
  - AnnData
  - scipy.sparse
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

# compressed-sparse-row-matrix-handling

## Summary

Convert and initialize single-cell count matrices into compressed sparse row (CSR) format compatible with matrix-free spectral embedding and scalable dimension reduction algorithms. CSR representation is essential for memory-efficient processing of large sparse single-cell datasets (10M+ cells) in downstream spectral and clustering workflows.

## When to use

You have a raw or preprocessed single-cell count matrix (from BAM-to-fragment or FASTQ-to-matrix pipelines) and need to apply matrix-free algorithms like tl.spectral, tl.multi_spectral, or other scalable dimension reduction methods that require dense or sparse matrix input. Use CSR format specifically when dataset size exceeds typical in-memory dense matrix limits (e.g., >1M cells) or when downstream tools (SnapATAC2, Scanpy) explicitly expect sparse backends.

## When NOT to use

- Input matrix is already in CSR or other optimized sparse format (e.g., scipy.sparse.csc_matrix) — skip conversion and proceed directly to downstream tools.
- Dataset size is <100K cells and memory is not a constraint — dense matrix storage may be simpler and faster for small-scale exploratory analysis.
- Downstream tool explicitly requires dense matrix input (rare for SnapATAC2 ecosystem, but check tool documentation).

## Inputs

- count matrix (tile-based, peak-based, or gene-based quantification)
- cell-by-feature matrix in dense array format, scipy.sparse format, or HDF5
- AnnData object with .X as dense array

## Outputs

- AnnData object with .X as CSR-backed sparse matrix
- scipy.sparse.csr_matrix
- compressed sparse row representation compatible with tl.spectral

## How to apply

Load the count matrix (tile-based, peak-based, or gene-based) from its native format (HDF5, AnnData, or text-based sparse formats) and convert to CSR format using SnapATAC2's matrix utilities or scipy.sparse. Initialize the matrix in SnapATAC2's AnnData object with `.X` as a CSR-backed array; this enables lazy evaluation and reduces peak memory footprint during subsequent operations. Verify CSR integrity by checking matrix shape, sparsity (number of nonzero elements), and data type consistency. For datasets approaching or exceeding 10 million cells, confirm that memory profiling shows sub-linear memory growth relative to cell count when CSR is used versus dense alternatives.

## Related tools

- **SnapATAC2** (primary framework for loading, initializing, and storing CSR-backed matrices; integrates scipy.sparse backend with AnnData) — https://github.com/scverse/SnapATAC2
- **AnnData** (container format for sparse matrix storage and lazy evaluation; supports CSR and other sparse formats via backed/on-disk storage)
- **scipy.sparse** (underlying library for CSR matrix construction and conversion)
- **precellar** (upstream preprocessing tool that generates count matrices (gene/fragment quantification) that become inputs to CSR conversion) — https://github.com/regulatory-genomics/precellar

## Examples

```
import snapatac2 as snap; import scipy.sparse as sp; adata = snap.pp.import_fragments('fragments.tsv.gz'); snap.pp.make_peak_matrix(adata, snap.datasets.colon()); adata.X = sp.csr_matrix(adata.X) if not sp.issparse(adata.X) else adata.X; snap.tl.spectral(adata, use_rep='X')
```

## Evaluation signals

- Matrix shape and sparsity metrics match input count matrix dimensions; verify nonzero element count is preserved after CSR conversion.
- Peak memory usage during spectral embedding is approximately linear or sub-linear with respect to cell count (measurable via memory_profiler or psutil), confirming CSR efficiency.
- Wall-clock runtime for tl.spectral on 10M+ cell datasets completes in reasonable time (reported in article as <hours on standard hardware); compare runtime against dense matrix baseline.
- CSR matrix format is confirmed via `.X.format == 'csr'` check in AnnData object or `type(matrix) == scipy.sparse.csr_matrix`.
- Downstream operations (e.g., cosine similarity in tl.spectral) produce expected eigenvalue-weighted eigenvector output without memory overflow or truncation.

## Limitations

- CSR format is optimized for row-wise operations; column-wise access may be slower than CSC (compressed sparse column) format.
- Conversion overhead is minimal but non-zero; for very small matrices (<10K cells), dense representation may be faster end-to-end.
- Not all downstream tools in the SnapATAC2 ecosystem may support sparse matrices equally; verify compatibility before committing to full CSR pipeline.
- CSR backend in AnnData can slow down random access to individual elements; use primarily for batch operations and linear algebra (matrix multiplication, decomposition).

## Evidence

- [other] Initialize the matrix in compressed sparse row (CSR) format compatible with SnapATAC2's backend.: "Initialize the matrix in compressed sparse row (CSR) format compatible with SnapATAC2's backend."
- [intro] Matrix-free spectral embedding algorithm that is applicable to a wide range of single-cell omics data, including single-cell ATAC-seq, single-cell RNA-seq, single-cell Hi-C, and single-cell methylation.: "Matrix-free spectral embedding algorithm that is applicable to a wide range of single-cell omics data, including single-cell ATAC-seq, single-cell RNA-seq, single-cell Hi-C, and single-cell"
- [intro] Scale to more than 10 million cells.: "Scale to more than 10 million cells."
- [readme] Implementation of fully backed AnnData.: "Implementation of fully backed AnnData."
- [other] Monitor and record peak memory usage throughout the spectral decomposition using a memory profiler (e.g., memory_profiler or psutil).: "Monitor and record peak memory usage throughout the spectral decomposition using a memory profiler (e.g., memory_profiler or psutil)."
