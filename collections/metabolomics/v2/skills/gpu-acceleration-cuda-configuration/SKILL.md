---
name: gpu-acceleration-cuda-configuration
description: Use when when clustering or encoding large MS/MS spectra datasets (>1
  million spectra) where CPU-only runtime exceeds practical thresholds (hours to days).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3791
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python 3.8+
  - CUDA
  - HyperSpec
  techniques:
  - LC-MS
  license_tier: open
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# GPU Acceleration via CUDA Configuration

## Summary

Configure and deploy CUDA-accelerated GPU computing to enable sub-15-minute clustering of large-scale mass spectrometry datasets (e.g., 25 million spectra) using hyperdimensional encoding and Hamming distance computation on NVIDIA GPUs. This skill trades GPU memory requirements for dramatic runtime reduction in compute-intensive proteomics workflows.

## When to use

When clustering or encoding large MS/MS spectra datasets (>1 million spectra) where CPU-only runtime exceeds practical thresholds (hours to days). Specifically applicable when hyperdimensional computing or distance-matrix operations dominate the computational load and NVIDIA GPU hardware (GTX 1080Ti or RTX 3090) is available with sufficient VRAM.

## When NOT to use

- Input dataset is <100k spectra: CPU clustering may be faster due to GPU initialization overhead.
- GPU with <6GB VRAM and dataset >10 million spectra: memory pressure will force excessive batch-size reduction or fail.
- Non-NVIDIA GPU or missing CUDA toolkit: HyperSpec requires CUDA-capable hardware and has been tested only on GTX 1080Ti and RTX 3090.

## Inputs

- MGF (mass spectrometry peak) files containing raw MS/MS spectra
- Dataset path containing one or more MGF files
- Spectra metadata (precursor m/z, charge state, retention time, scan number)

## Outputs

- Parquet file with clustered spectra metadata (bucket, precursor_charge, precursor_mz, identifier, scan, retention_time, cluster, is_representative)
- CSV file with cluster assignments (one spectrum and cluster label per line)
- Checkpoint file containing encoded hypervectors (optional, for resumption)

## How to apply

Install Python 3.8+ with CUDA environment and configure the GPU cluster task using the `--use_gpu_cluster` flag. Set batch size (default 5000 spectra per batch) to balance GPU memory usage against throughput; for large datasets like PXD000561 (25M spectra), use GTX 3090 or higher-memory GPU. Enable GPU-optimized Hamming distance kernels and HD encoding modules during spectra preprocessing. Verify CUDA device availability and monitor memory utilization during batch processing to prevent out-of-memory failures. The HD encoding module runs on GPU with batch_size parameter to trade memory for speed; lower batch_size if GPU memory is exhausted, higher batch_size if memory permits and latency is critical.

## Related tools

- **HyperSpec** (GPU-accelerated spectra clustering framework with CUDA kernels for HD encoding and Hamming distance computation) — https://github.com/wh-xu/Hyper-Spec
- **CUDA** (GPU compute platform required for parallel HD encoding, Hamming distance matrix computation, and optional DBSCAN clustering on GPU)
- **Python 3.8+** (Runtime environment and interface for HyperSpec command-line invocation and batch parameter configuration)

## Examples

```
python src/main.py ~/dataset/ ./output.csv --cpu_core_preprocess=4 --cluster_alg dbscan --use_gpu_cluster --cluster_charges 2 3 --eps=0.2 --batch_size=5000 --refine
```

## Evaluation signals

- End-to-end runtime on 25M-spectra dataset is <15 minutes on GTX 3090 (vs. hours on CPU baseline).
- GPU memory usage (monitored via nvidia-smi) remains below device capacity throughout batch processing; no OOM errors occur.
- Output parquet/CSV file contains cluster IDs for all input spectra with no missing or null cluster assignments.
- Hamming distance matrices computed on GPU yield identical clustering results (cluster labels, representative spectra) compared to CPU reference implementation.
- Batch processing completes without CUDA synchronization errors or kernel launch failures.

## Limitations

- Clustering PXD000561 (25M spectra) requires GTX 3090 with large VRAM; smaller GPUs (e.g., GTX 1080Ti) support smaller datasets only.
- Performance gains are specific to hyperdimensional encoding and Hamming distance; standard DBSCAN on CPU may not show proportional speedup.
- CUDA environment setup and GPU driver installation are prerequisites; not portable to CPU-only or non-NVIDIA platforms.
- Batch size tuning is dataset- and hardware-dependent; no automatic heuristic provided for optimal batch_size selection.

## Evidence

- [intro] _HyperSpec_ shortens the runtime on the draft human proteome dataset with 25 million spectra from a few hours to <15 minutes.: "_HyperSpec_ shortens the runtime on the draft human proteome dataset with 25 million spectra from a few hours to <15 minutes."
- [readme] _HyperSpec_ requires `Python 3.8+` with `CUDA` environment. A GPU should be installed properly.: "_HyperSpec_ requires `Python 3.8+` with `CUDA` environment. A GPU should be installed properly."
- [readme] Clustering for PXD000561 dataset requires GTX 3090 with larger memory: "Clustering for PXD000561 dataset requires GTX 3090 with larger memory"
- [readme] The encoding module is implemented and optimized for GPU for shorter runtime.: "The encoding module is implemented and optimized for GPU for shorter runtime."
- [readme] _HyperSpec_ implements very efficient Hamming distance computation kernels on GPU.: "_HyperSpec_ implements very efficient Hamming distance computation kernels on GPU."
- [readme] --batch_size                The batch size for HD encoding on GPU. (default: 5000): "--batch_size                The batch size for HD encoding on GPU. (default: 5000)"
- [readme] --use_gpu_cluster           Flag that determines whether to use DBSCAN on GPU. (default: True): "--use_gpu_cluster           Flag that determines whether to use DBSCAN on GPU. (default: True)"
