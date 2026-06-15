---
name: computational-complexity-validation
description: Use when when an algorithm claims linear or sublinear time/space complexity (e.g., matrix-free spectral embedding) and you need to verify that claim holds for datasets at the scale intended (10 million+ cells).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3673
  - http://edamontology.org/topic_3308
  tools:
  - SnapATAC2
  - Python
  - Rust
  - memory_profiler
  - psutil
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

# computational-complexity-validation

## Summary

Empirically validate theoretical time and space complexity claims of a scalable algorithm by executing it on progressively large datasets (10M+ cells), measuring wall-clock runtime and peak memory, and plotting observed metrics against the predicted complexity curve to confirm linear or sublinear behavior.

## When to use

When an algorithm claims linear or sublinear time/space complexity (e.g., matrix-free spectral embedding) and you need to verify that claim holds for datasets at the scale intended (10 million+ cells). Typical trigger: the algorithm's documentation or paper asserts O(n) or O(n log n) complexity, but you have access to datasets large enough to test empirically, and the scaling behavior is critical to your application's feasibility.

## When NOT to use

- Algorithm documentation does not make an explicit complexity claim to validate.
- Datasets available are too small (< 100K cells) to reliably distinguish linear from polynomial growth; noise in measurements dominates.
- Input is already preprocessed to a lower-dimensional representation (e.g., PCA scores, gene expression matrix); complexity validation requires full-rank or near-full-rank input.

## Inputs

- single-cell count matrix in CSR (compressed sparse row) format with ≥1M cells
- cell and feature annotation metadata (optional but recommended for reproducibility)

## Outputs

- wall-clock runtime measurements (seconds) for each dataset size
- peak memory usage (GB) for each dataset size
- log-log plot of runtime vs. cell count with fitted complexity slope
- log-log plot of memory vs. cell count with fitted complexity slope
- summary table: cell count, runtime, peak memory, eigenvectors returned, output structure validation status

## How to apply

Execute the algorithm on a series of datasets of increasing size (e.g., 1M, 5M, 10M+ cells), ensuring input matrices are in the same sparse format (e.g., CSR) that the algorithm expects. Measure wall-clock runtime using Python's time module or system profilers, and track peak memory consumption throughout execution using memory_profiler or psutil. Record the number of output features (e.g., eigenvectors) and verify they match expected output structure (e.g., weighted by eigenvalues). Plot runtime and memory against dataset size on log-log axes; a linear complexity algorithm should produce a slope near 1.0 when both axes are logarithmic. Analyze deviations from theory—actual overhead, constant factors, and memory alignment effects often cause a steeper slope at smaller sizes—and document whether the observed complexity is consistent with the published claim at the target scale.

## Related tools

- **SnapATAC2** (Algorithm under test; provides tl.spectral (matrix-free spectral embedding with cosine similarity metric) and dataset utilities for loading/generating large count matrices in CSR format.) — https://github.com/scverse/SnapATAC2
- **Python** (Language for orchestrating measurement workflow; time module for runtime capture, integration with memory profiling.)
- **memory_profiler** (Monitor and record peak memory usage throughout execution.)
- **psutil** (Alternative system profiler for memory consumption tracking.)

## Examples

```
import time
import snapatac2 as snap
from memory_profiler import profile

adata = snap.datasets.pbmc10k_multiome()
start = time.time()
snap.tl.spectral(adata, use_rep='X')
runtime = time.time() - start
print(f'Spectral embedding on {adata.n_obs} cells: {runtime:.2f}s')
```

## Evaluation signals

- Runtime vs. cell count plot exhibits slope ≈ 1.0 on log-log axes (confirming linear time complexity); slope significantly > 1.0 (e.g., 1.5–2.0) indicates sublinear scaling relative to claim.
- Peak memory vs. cell count plot exhibits slope ≈ 1.0 on log-log axes (confirming linear space complexity); slope significantly > 1.0 suggests memory scaling is worse than linear.
- Measured peak memory is within the theoretical CSR matrix overhead (nnz * 2 * 8 bytes for data + col_indices, plus row_pointers and auxiliary structures), not orders of magnitude higher.
- Output eigenvectors are present, correctly weighted by eigenvalues, and their count matches expected behavior (e.g., default 30 in Release 2.3.0) across all tested dataset sizes.
- Runtime and memory measurements show consistent, monotonic growth with dataset size; random fluctuations are small relative to the trend (coefficient of variation < 20% across replicates if available).

## Limitations

- Empirical validation is sensitive to hardware (CPU cache, memory architecture, I/O speed), competing processes, and data layout; results may not generalize across different compute environments.
- Constant factors and overhead dominate at small dataset sizes (< 1M cells), making it difficult to distinguish linear from polynomial complexity without very large datasets; 10M+ cell experiments are computationally expensive.
- Memory measurement captures peak usage at a point in time; some algorithms may have multiple phases with different memory footprints, and a single peak snapshot may not capture the true worst-case.
- Similarity metric choice (cosine, Euclidean, etc.) can affect both runtime and memory; the article specifies cosine as default in Release 2.3.0, but other metrics may show different scaling properties.
- Sparse matrix fill rate and feature diversity affect practical runtime independent of theoretical complexity; two 10M-cell matrices with different sparsity patterns will show different execution times even if complexity class is identical.

## Evidence

- [other] Does the matrix-free spectral embedding algorithm (tl.spectral) in SnapATAC2 achieve linear time and space complexity when applied to datasets of 10 million or more cells?: "Does the matrix-free spectral embedding algorithm (tl.spectral) in SnapATAC2 achieve linear time and space complexity when applied to datasets of 10 million or more cells?"
- [other] SnapATAC2 is capable of scaling to more than 10 million cells, demonstrating its capacity to handle very large single-cell datasets.: "SnapATAC2 is capable of scaling to more than 10 million cells, demonstrating its capacity to handle very large single-cell datasets."
- [other] Execute tl.spectral with cosine similarity metric (the default similarity metric as of Release 2.3.0) and capture wall-clock runtime using Python's time module or system profiler.: "Execute tl.spectral with cosine similarity metric (the default similarity metric as of Release 2.3.0) and capture wall-clock runtime using Python's time module or system profiler."
- [other] Monitor and record peak memory usage throughout the spectral decomposition using a memory profiler (e.g., memory_profiler or psutil).: "Monitor and record peak memory usage throughout the spectral decomposition using a memory profiler (e.g., memory_profiler or psutil)."
- [other] Analyze runtime and peak memory against the reported linear complexity claim by plotting execution metrics.: "Analyze runtime and peak memory against the reported linear complexity claim by plotting execution metrics."
- [intro] Scale to more than 10 million cells.: "Scale to more than 10 million cells."
- [intro] Matrix-free spectral embedding algorithm that is applicable to a wide range of single-cell omics data, including single-cell ATAC-seq, single-cell RNA-seq, single-cell Hi-C, and single-cell: "Matrix-free spectral embedding algorithm that is applicable to a wide range of single-cell omics data"
