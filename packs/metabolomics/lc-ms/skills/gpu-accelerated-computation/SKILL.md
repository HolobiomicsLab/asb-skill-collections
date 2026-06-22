---
name: gpu-accelerated-computation
description: 'Use when when processing large-scale mass spectrometry datasets (>1 million spectra) where CPU-based clustering runtime would exceed minutes to hours, and when the analysis pipeline includes: (1) encoding raw spectra into high-dimensional binary vectors, (2) computing pairwise distance matrices.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python 3.8+
  - HyperSpec
  - CUDA
  - DBSCAN
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.jproteome.2c00612
  title: HyperSpec
evidence_spans:
- HyperSpec requires `Python 3.8+` with `CUDA` environment
- HyperSpec requires `Python 3.8+` with `CUDA` environment.
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

# gpu-accelerated-computation

## Summary

Offload compute-intensive steps of mass spectra analysis (encoding, distance matrix computation, clustering) to NVIDIA GPUs to achieve sub-minute runtimes on datasets with millions of spectra. This skill applies brain-inspired hyperdimensional computing kernels and Hamming distance operations optimized for GPU execution.

## When to use

When processing large-scale mass spectrometry datasets (>1 million spectra) where CPU-based clustering runtime would exceed minutes to hours, and when the analysis pipeline includes: (1) encoding raw spectra into high-dimensional binary vectors, (2) computing pairwise distance matrices across buckets, or (3) running DBSCAN or hierarchical clustering. GPU acceleration is particularly effective for level-id encoding and Hamming distance computation, which are highly parallelizable.

## When NOT to use

- Input spectra dataset is <100,000 spectra; CPU-based clustering will be faster than GPU setup and data transfer overhead.
- No NVIDIA GPU is available or CUDA environment cannot be configured; fall back to CPU clustering algorithms.
- Spectra are already encoded into feature vectors or distance matrices; this skill targets raw MGF input only.

## Inputs

- MGF (Mascot Generic Format) files containing raw mass spectra with m/z and intensity peak pairs
- Spectra metadata: precursor m/z, charge state, retention time, scan identifiers

## Outputs

- Parquet file with clustering results: bucket, precursor_charge, precursor_mz, identifier, scan, retention_time, cluster label, is_representative flag
- CSV file (alternative format) with one spectrum per line and assigned cluster label
- Checkpoint file (optional): encoded binary hypervectors (HVs) for all spectra, reusable for downstream analysis

## How to apply

First, ensure an NVIDIA GPU (GTX 1080Ti or GTX 3090 recommended) and CUDA environment are available. Preprocess input MGF files (peak normalization, charge filtering, m/z range clipping) on CPU using specified core count (default: 6). Encode each spectrum into a binary hyperdimensional vector (default dimension: 2048, quantization level: 16) on GPU via level-id encoding method, batching spectra for memory efficiency (default batch size: 5000). Partition the entire dataset into buckets and compute pairwise Hamming distance matrices for each bucket using optimized GPU kernels. Finally, apply DBSCAN (eps threshold, typically 0.2–0.4) or hierarchical clustering on GPU (if `--use_gpu_cluster` flag is set) to cluster each bucket. Post-processing refinement can be enabled to improve cluster coherence. Monitor GPU memory usage; datasets like PXD000561 (25 million spectra) require GTX 3090 with larger memory capacity.

## Related tools

- **HyperSpec** (GPU-accelerated mass spectra clustering framework implementing level-id HD encoding, Hamming distance kernels, and DBSCAN/hierarchical clustering on NVIDIA GPUs) — https://github.com/wh-xu/Hyper-Spec
- **CUDA** (Parallel compute platform and API enabling GPU kernel execution for HD encoding and distance matrix computation)
- **Python 3.8+** (High-level host language for spectra I/O, preprocessing orchestration, and GPU kernel invocation via CUDA bindings)
- **DBSCAN** (Density-based clustering algorithm executed on GPU to partition spectra buckets (alternative to hierarchical clustering))

## Examples

```
python src/main.py ~/dataset/ ./output.csv --cpu_core_preprocess=4 --cluster_alg dbscan --use_gpu_cluster --cluster_charges 2 3 --eps=0.2 --refine
```

## Evaluation signals

- Encoding runtime on benchmark dataset (PXD000561, 25 million spectra) is <15 minutes on GTX 3090, confirming GPU acceleration achieved documented speedup from hours to sub-15-minute range.
- All spectra are encoded to binary hyperdimensional vectors with correct dimensionality (default 2048) and confirmed binary format (only 0/1 values).
- Hamming distance matrices per bucket have dimensions [bucket_size, bucket_size] with integer values in range [0, hd_dim], validating distance computation correctness.
- Clustering output parquet file contains all expected fields (bucket, precursor_charge, cluster label, is_representative) with no null cluster assignments for non-filtered spectra.
- GPU memory utilization stays within device limit; if memory overflow occurs, reduce batch_size or dataset size and re-run.

## Limitations

- GPU memory is the primary bottleneck: clustering large datasets like PXD000561 (25M spectra) requires GTX 3090 with larger memory; GTX 1080Ti suitable only for smaller-scale datasets.
- CUDA environment must be correctly installed and compatible with the target NVIDIA GPU; no CPU-only fallback is implemented for encoding or clustering steps.
- Hyperparameter tuning (hd_dim, hd_Q, eps threshold) is required for optimal clustering quality; default values may not generalize across all MS/MS datasets or instrumentation types.
- No changelog is available in the repository, limiting traceability of algorithm updates or bug fixes.

## Evidence

- [intro] HyperSpec shortens the runtime on the draft human proteome dataset with 25 million spectra from a few hours to <15 minutes.: "_HyperSpec_ shortens the runtime on the draft human proteome dataset with 25 million spectra from a few hours to <15 minutes."
- [intro] HyperSpec adopts brain-inspired hyperdimensional computing to project spectra data into binary hyperdimensional space for better clustering quality and faster clustering speed.: "_HyperSpec_ adopts the brain-inspired hyperdimensional (HD) computing to project the spectra data into binary hyperdimensional space to obtain better clustering quality and faster clustering speed."
- [readme] Requires Python 3.8+ with CUDA environment and NVIDIA GPU (GTX 1080Ti or GTX 3090).: "_HyperSpec_ requires `Python 3.8+` with `CUDA` environment. A GPU should be installed properly. _HyperSpec_ has been tested on two types of NVIDIA GPUs on a Linux platform, including GTX 1080Ti and"
- [readme] Clustering for PXD000561 dataset requires GTX 3090 with larger memory.: "Clustering for PXD000561 dataset requires GTX 3090 with larger memory"
- [readme] HyperSpec encodes spectra into binary hypervectors using level-id encoding, computes pairwise Hamming distance matrices, and clusters using DBSCAN.: "_HyperSpec_ first encodes the processed spectra into binary hypervector (HV) with ultra-high dimension (>1000) based on level-id encoding method. The encoding module is implemented and optimized for"
- [readme] Default HD dimension is 2048 with quantization level 16 and batch size 5000 for GPU encoding.: "--hd_dim                    The HD dimension. (default: 2048)
    --hd_Q                      The HD quantization level. (default: 16)
    --batch_size                The batch size for HD encoding"
