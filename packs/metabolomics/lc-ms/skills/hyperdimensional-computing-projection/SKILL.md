---
name: hyperdimensional-computing-projection
description: Use when when clustering large-scale mass spectrometry datasets (millions of MS/MS spectra in MGF format) where runtime is a bottleneck and you have access to NVIDIA GPU resources (GTX 3090 for large datasets like PXD000561, or GTX 1080Ti for smaller datasets).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python 3.8+
  - HyperSpec
  - CUDA
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.jproteome.2c00612
  title: HyperSpec
evidence_spans:
- HyperSpec requires `Python 3.8+` with `CUDA` environment
- HyperSpec requires `Python 3.8+` with `CUDA` environment.
- github.com__wh-xu__Hyper-Spec
- github.com/wh-xu/Hyper-Spec
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_hyperspec_cq
    doi: 10.1021/acs.jproteome.2c00612
    title: HyperSpec
  dedup_kept_from: coll_hyperspec_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.2c00612
  all_source_dois:
  - 10.1021/acs.jproteome.2c00612
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Hyperdimensional Computing Projection

## Summary

Project mass spectra into binary hyperdimensional space using level-id encoding to enable ultrafast clustering. This brain-inspired approach converts high-dimensional spectra data into compact hypervectors (>1000 dimensions) suitable for efficient distance computation and DBSCAN clustering on GPU.

## When to use

When clustering large-scale mass spectrometry datasets (millions of MS/MS spectra in MGF format) where runtime is a bottleneck and you have access to NVIDIA GPU resources (GTX 3090 for large datasets like PXD000561, or GTX 1080Ti for smaller datasets). Use this skill when you need to reduce clustering runtime from hours to minutes while maintaining or improving clustering quality.

## When NOT to use

- When working with already-encoded feature vectors or pre-computed distance matrices (hyperdimensional projection is only appropriate for raw spectra data).
- When GPU resources are unavailable; CPU-only preprocessing is supported but HD encoding and Hamming distance computation are GPU-optimized and will be substantially slower.
- When spectra require fine-grained intensity resolution below the quantization level Q=16; hyperdimensional encoding is lossy in the intensity dimension.

## Inputs

- MGF files containing MS/MS spectra (peak m/z and intensity pairs)
- Preprocessed spectra with m/z range filtering and peak intensity thresholding applied

## Outputs

- Binary hypervector representations (Hamming distance matrices per bucket)
- Parquet file with cluster assignments per spectrum, including precursor_charge, precursor_mz, scan, retention_time, cluster ID, and is_representative flag

## How to apply

After preprocessing spectra (peak filtering, intensity normalization), encode each spectrum into a binary hypervector using level-id encoding with configurable HD dimension (default 2048) and quantization level (default Q=16). Process spectra in GPU-optimized batches (default batch_size=5000) to compute Hamming distance matrices for small spectrum buckets. The lightweight Hamming distance computation replaces expensive Euclidean distance calculations, enabling fast pairwise similarity assessment. Select scaling method (root, log, rank, or off) based on intensity distribution. Choose HD dimension and Q parameters based on dataset size and desired precision; larger dimensions capture more spectrum detail but increase computation. Proceed to DBSCAN or hierarchical clustering on the resulting hypervector similarity matrices.

## Related tools

- **HyperSpec** (Implements hyperdimensional encoding, GPU-accelerated Hamming distance computation, and bucketing pipeline for spectra projection and clustering) — https://github.com/wh-xu/Hyper-Spec
- **Python 3.8+** (Runtime environment for HyperSpec library)
- **CUDA** (GPU compute framework enabling fast HD encoding and Hamming distance kernels on NVIDIA GPUs)

## Examples

```
python src/main.py ~/dataset/ ./output.csv --cpu_core_preprocess=4 --cluster_alg dbscan --use_gpu_cluster --cluster_charges 2 3 --hd_dim=2048 --hd_Q=16 --eps=0.2 --refine
```

## Evaluation signals

- Verify output hypervectors are binary and have dimensionality matching the --hd_dim parameter (default 2048 bits per spectrum).
- Confirm Hamming distance matrices are symmetric, with diagonal values = 0 and off-diagonal values in range [0, hd_dim].
- Validate that clustering runtime is substantially reduced (target <15 minutes for 25 million spectra on GTX 3090) compared to non-HD baseline.
- Check that output parquet contains all required metadata columns (bucket, precursor_charge, precursor_mz, cluster, is_representative) with no null cluster assignments for non-filtered spectra.
- Verify that clustering quality (as measured by spectral similarity within clusters) is maintained or improved relative to non-HD clustering on the same dataset.

## Limitations

- Clustering for large datasets (e.g. PXD000561) requires GTX 3090 with larger VRAM; GTX 1080Ti is restricted to smaller-scale datasets.
- Hyperdimensional encoding is lossy in the intensity dimension due to quantization level Q; fine-grained intensity distinctions are not preserved.
- GPU memory constraints limit batch_size parameter; excessively large batches may cause out-of-memory errors during HD encoding.
- Other NVIDIA GPU types may work but have not been officially tested; performance is not guaranteed outside GTX 1080Ti and GTX 3090.
- Hamming distance is less sensitive to small peak intensity variations than Euclidean metrics; this may affect clustering of spectra with subtle intensity patterns.

## Evidence

- [intro] brain-inspired hyperdimensional computing to project spectra data into binary hyperdimensional space: "_HyperSpec_ adopts the brain-inspired hyperdimensional (HD) computing to project the spectra data into binary hyperdimensional space to obtain better clustering quality and faster clustering speed."
- [intro] shortens the runtime on the draft human proteome dataset with 25 million spectra from a few hours to <15 minutes: "_HyperSpec_ shortens the runtime on the draft human proteome dataset with 25 million spectra from a few hours to <15 minutes."
- [readme] level-id encoding method with HD dimension and quantization parameters: "_HyperSpec_ first encodes the processed spectra into binary hypervector (HV) with ultra-high dimension (>1000) based on level-id encoding method."
- [readme] GPU requirements for different dataset scales: "Clustering for PXD000561 dataset requires GTX 3090 with larger memory; Clustering for other dataset with smaller scale requires GTX 1080Ti"
- [readme] Hamming distance computation for efficient clustering: "The pairwise Hamming distance matrix for each bucket is computed. _HyperSpec_ implements very efficient Hamming distance computation kernels on GPU."
- [readme] HD dimension and quantization level parameters with defaults: "--hd_dim HD_DIM The HD dimension. (default: 2048); --hd_Q HD_Q The HD quantization level. (default: 16)"
