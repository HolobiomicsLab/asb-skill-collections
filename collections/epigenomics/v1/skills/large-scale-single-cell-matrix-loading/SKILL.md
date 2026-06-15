---
name: large-scale-single-cell-matrix-loading
description: Use when you have a single-cell count matrix with 10 million or more cells that must be processed through dimension reduction, clustering, or integration pipelines. Use it specifically before executing matrix-free spectral embedding (tl.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_3179
  - http://edamontology.org/topic_3308
  - http://edamontology.org/topic_0622
  tools:
  - SnapATAC2
  - Python
  - Rust
  - psutil
  - memory_profiler
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

# large-scale-single-cell-matrix-loading

## Summary

Load and initialize single-cell count matrices with ≥10 million cells in compressed sparse row (CSR) format for scalable downstream analysis. This skill is essential when working with very large omics datasets where memory efficiency and linear-time complexity are critical.

## When to use

Apply this skill when you have a single-cell count matrix with 10 million or more cells that must be processed through dimension reduction, clustering, or integration pipelines. Use it specifically before executing matrix-free spectral embedding (tl.spectral) or other scalable SnapATAC2 tools that require efficient sparse matrix representation.

## When NOT to use

- Input is already a processed and filtered AnnData object ready for dimension reduction — use directly without re-initialization.
- Dataset contains fewer than 100,000 cells — standard dense matrix handling may be more efficient.
- Matrix is already in a non-CSR sparse format (e.g., COO, LIL) incompatible with SnapATAC2 backend — convert format explicitly first.

## Inputs

- single-cell count matrix with ≥10 million cells (dense or sparse format)
- cell-by-feature table (BAM files, fragment files, or pre-computed count matrices)
- metadata specifying matrix dimensions and cell/feature identifiers

## Outputs

- CSR-formatted sparse matrix compatible with SnapATAC2 backend
- AnnData object (.h5ad) with initialized count matrix
- memory usage profile and initialization metrics

## How to apply

Load the count matrix using SnapATAC2's dataset utilities or external data sources and initialize it in compressed sparse row (CSR) format, which is the sparse matrix representation required by SnapATAC2's backend. Verify that the matrix dimensions match the expected number of cells (rows) and features (columns), and confirm that the data type supports the downstream cosine similarity metric used in spectral decomposition. Monitor memory footprint during initialization using a profiler such as psutil or memory_profiler to ensure the sparse format achieves the expected linear space complexity. Document the initialization parameters and resulting matrix structure (sparsity percentage, number of nonzero elements) before proceeding to decomposition or embedding steps.

## Related tools

- **SnapATAC2** (Primary framework for loading, initializing, and managing large-scale single-cell matrices in CSR format; provides dataset utilities and backend handling) — https://github.com/scverse/SnapATAC2
- **Python** (Programming environment and runtime for matrix loading, initialization, and profiling operations)
- **Rust** (Backend implementation in SnapATAC2 for efficient sparse matrix operations and CSR format management) — https://github.com/scverse/SnapATAC2
- **psutil** (Memory profiling and system resource monitoring during matrix initialization)
- **memory_profiler** (Detailed memory usage tracking throughout sparse matrix initialization and loading)
- **AnnData** (Data structure for storing initialized count matrices with cell and feature annotations)

## Examples

```
import snapatac2 as snap; mat = snap.datasets.pbmc10k_multiome(); mat_csr = mat.to_csr(); print(f'Shape: {mat_csr.shape}, Sparsity: {1 - mat_csr.nnz / (mat_csr.shape[0] * mat_csr.shape[1]):.2%}')
```

## Evaluation signals

- Matrix successfully initializes in CSR format without out-of-memory errors when loading ≥10 million cells
- Peak memory usage remains proportional to the number of nonzero elements (linear space complexity) and is substantially lower than dense matrix equivalent
- Sparsity percentage and number of nonzero elements match expectations for the input data modality (ATAC-seq, RNA-seq, Hi-C, methylation)
- Subsequent spectral embedding execution (tl.spectral) with cosine similarity metric completes without format conversion errors
- Memory profiler output shows flat or sublinear memory growth during initialization relative to cell count increase

## Limitations

- CSR format initialization requires sufficient available system RAM to build the sparse representation; very sparse data with many zero values still requires in-memory intermediate structures
- SnapATAC2's backend assumes cosine similarity metric as the default similarity metric as of Release 2.3.0; other similarity metrics may require explicit specification or reformatting
- Loading from BAM or fragment files requires prior conversion to fragment file format via precellar or external tools; direct BAM loading may incur additional preprocessing overhead
- Linear complexity claim applies to the spectral embedding algorithm itself; the matrix loading and initialization step may show super-linear behavior on datasets with highly non-uniform sparsity patterns

## Evidence

- [other] Initialize the matrix in compressed sparse row (CSR) format compatible with SnapATAC2's backend.: "Initialize the matrix in compressed sparse row (CSR) format compatible with SnapATAC2's backend."
- [readme] Scale to more than 10 million cells.: "Scale to more than 10 million cells."
- [readme] SnapATAC2 is a flexible, versatile, and scalable single-cell omics analysis framework: "SnapATAC2 is a flexible, versatile, and scalable single-cell omics analysis framework"
- [intro] Matrix-free spectral embedding algorithm that is applicable to a wide range of single-cell omics data, including single-cell ATAC-seq, single-cell RNA-seq, single-cell Hi-C, and single-cell methylation: "Matrix-free spectral embedding algorithm that is applicable to a wide range of single-cell omics data, including single-cell ATAC-seq, single-cell RNA-seq, single-cell Hi-C, and single-cell"
- [other] Monitor and record peak memory usage throughout the spectral decomposition using a memory profiler (e.g., memory_profiler or psutil).: "Monitor and record peak memory usage throughout the spectral decomposition using a memory profiler (e.g., memory_profiler or psutil)."
- [other] cosine similarity metric (the default similarity metric as of Release 2.3.0): "cosine similarity metric (the default similarity metric as of Release 2.3.0)"
