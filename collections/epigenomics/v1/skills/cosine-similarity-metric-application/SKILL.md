---
name: cosine-similarity-metric-application
description: Use when you are performing dimensionality reduction on a sparse single-cell count matrix (in CSR format) and need to compute pairwise cell similarities before spectral decomposition.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_3308
  - http://edamontology.org/topic_0654
  tools:
  - SnapATAC2
  - Python
  - Rust
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

# cosine-similarity-metric-application

## Summary

Apply cosine similarity as the distance metric in matrix-free spectral embedding to compute cell-to-cell similarities in high-dimensional single-cell omics data. This metric is the default choice in SnapATAC2's spectral embedding algorithm and is suitable for sparse count matrices across ATAC-seq, RNA-seq, Hi-C, and methylation modalities.

## When to use

You are performing dimensionality reduction on a sparse single-cell count matrix (in CSR format) and need to compute pairwise cell similarities before spectral decomposition. Cosine similarity is the appropriate choice when your input is an unscaled or log-normalized count matrix and you want metric-agnostic behavior that treats zero entries uniformly. Choose this metric if you are working with SnapATAC2 Release 2.3.0 or later, where it is the default similarity metric.

## When NOT to use

- Input is a dense matrix or already a distance/similarity matrix (cosine similarity should be computed on raw counts, not post-hoc on existing similarities)
- You require a custom distance metric that is not cosine (e.g., Euclidean, Manhattan, Pearson) — use tl.spectral with explicit metric parameter instead
- Your matrix is already heavily preprocessed into a different coordinate space where cosine distance semantics do not apply

## Inputs

- sparse count matrix in CSR (compressed sparse row) format
- single-cell omics data (ATAC-seq, RNA-seq, Hi-C, or methylation)
- cell-by-feature or cell-by-tile matrix (≥10 million cells supported)

## Outputs

- low-dimensional cell embedding (weighted eigenvectors from spectral decomposition)
- eigenvalues associated with computed eigenvectors
- runtime and peak memory metrics for scalability verification

## How to apply

Initialize your single-cell count matrix in compressed sparse row (CSR) format compatible with SnapATAC2's backend. Call tl.spectral() without explicitly specifying the similarity metric argument, relying on the default cosine similarity metric (Release 2.3.0+), or explicitly pass metric='cosine' to ensure reproducibility. The spectral embedding algorithm will compute pairwise cosine similarities among all cells, then perform eigendecomposition on the resulting similarity matrix to extract the dominant eigenvectors. The returned eigenvectors are weighted by their corresponding eigenvalues by default, producing a low-dimensional embedding suitable for downstream clustering and visualization. Monitor both runtime and peak memory usage during execution to verify linear complexity scaling; cosine similarity computation is matrix-free, so memory overhead should be proportional to the number of cells and features, not their product.

## Related tools

- **SnapATAC2** (implements matrix-free spectral embedding with cosine similarity metric as default for single-cell omics dimensionality reduction) — https://github.com/scverse/SnapATAC2
- **Python** (runtime environment and primary scripting language for SnapATAC2)
- **Rust** (backend implementation language for efficient matrix-free spectral embedding computations)
- **Scanpy** (seamless integration for downstream analysis and visualization of spectral embeddings)

## Examples

```
import snapatac2 as snap; snap.tl.spectral(adata, n_comps=50)  # uses default cosine similarity metric in Release 2.3.0+
```

## Evaluation signals

- Verify that runtime scales linearly with cell count when processing datasets from 1M to 10M+ cells
- Confirm peak memory usage remains proportional to the number of cells and features (not their product), indicating matrix-free behavior
- Check that returned eigenvectors are weighted by their eigenvalues (verify non-zero weighting in output embedding matrix)
- Validate embedding dimensionality matches the number of requested eigenvectors (default behavior as of Release 2.3.0)
- Ensure cosine similarity metric produces non-negative similarities bounded in [0, 1] for sparse count data

## Limitations

- Matrix-free spectral embedding with cosine similarity assumes sparse input; dense matrices may not benefit from the claimed linear memory complexity
- Cosine similarity may not capture biologically meaningful distances in heavily zero-inflated regions of sparse matrices common in single-cell epigenomics
- Spectral embedding quality depends on the underlying count matrix preprocessing (normalization, feature selection); cosine similarity alone does not mitigate poor input quality
- The algorithm is optimized for Release 2.3.0 and later; earlier versions may use different default similarity metrics or complexity characteristics

## Evidence

- [other] Execute tl.spectral with cosine similarity metric (the default similarity metric as of Release 2.3.0) and capture wall-clock runtime using Python's time module or system profiler.: "Execute tl.spectral with cosine similarity metric (the default similarity metric as of Release 2.3.0)"
- [intro] Matrix-free spectral embedding algorithm that is applicable to a wide range of single-cell omics data, including single-cell ATAC-seq, single-cell RNA-seq, single-cell Hi-C, and single-cell methylation.: "Matrix-free spectral embedding algorithm that is applicable to a wide range of single-cell omics data, including single-cell ATAC-seq, single-cell RNA-seq, single-cell Hi-C, and single-cell"
- [other] Document the number of eigenvectors returned and verify they are weighted by eigenvalues (default behavior in Release 2.3.0) to confirm the expected output structure.: "verify they are weighted by eigenvalues (default behavior in Release 2.3.0) to confirm the expected output structure"
- [other] SnapATAC2 is capable of scaling to more than 10 million cells, demonstrating its capacity to handle very large single-cell datasets.: "SnapATAC2 is capable of scaling to more than 10 million cells, demonstrating its capacity to handle very large single-cell datasets"
- [other] Initialize the matrix in compressed sparse row (CSR) format compatible with SnapATAC2's backend.: "Initialize the matrix in compressed sparse row (CSR) format compatible with SnapATAC2's backend"
