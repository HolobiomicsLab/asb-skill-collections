---
name: mass-spectra-clustering-hyperdimensional-space
description: Use when you have large-scale MS/MS spectra datasets (hundreds of thousands
  to millions of spectra) in MGF format that need to be grouped by similarity, and
  you have access to NVIDIA GPU hardware (GTX 1080Ti or GTX 3090).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python 3.8+
  - HyperSpec
  - CUDA
  - DBSCAN / Hierarchical Clustering
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
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

# Mass spectra clustering in hyperdimensional space

## Summary

Cluster MS/MS spectra by encoding them into binary hypervectors of ultra-high dimension (>1000) and computing pairwise Hamming distances, then applying DBSCAN or hierarchical clustering. This brain-inspired hyperdimensional computing approach achieves sub-15-minute runtimes on 25M-spectra datasets on GPU.

## When to use

You have large-scale MS/MS spectra datasets (hundreds of thousands to millions of spectra) in MGF format that need to be grouped by similarity, and you have access to NVIDIA GPU hardware (GTX 1080Ti or GTX 3090). Use this when runtime must be minimized (target <15 min for 25M spectra) and you need both high clustering quality and speed.

## When NOT to use

- You lack GPU hardware (CUDA environment with NVIDIA GPU); CPU-only clustering will be orders of magnitude slower.
- Your spectra are already pre-clustered or belong to a single, already-annotated family; re-clustering adds no value.
- You require sub-spectra-level feature engineering or de novo MS/MS interpretation; HyperSpec clusters whole spectra, not fragments.

## Inputs

- MGF files containing MS/MS spectra
- Precursor m/z and retention time metadata
- Precursor charge state annotations
- Peak intensity and m/z arrays

## Outputs

- CSV or parquet file with cluster assignments per spectrum
- Cluster labels with representative spectra flagged
- Metadata: bucket, precursor_charge, precursor_mz, identifier, scan, retention_time, cluster, is_representative

## How to apply

First, preprocess spectra using CPU cores (default 6) to filter by charge state (typically charge 2–3), min/max m/z ranges, precursor tolerance, and peak intensity thresholds. Then encode the filtered spectra into binary hypervectors using GPU-optimized level-id encoding with configurable HD dimension (default 2048) and quantization level (default 16). Divide the encoded dataset into buckets and compute pairwise Hamming distance matrices for each bucket on GPU. Finally, apply DBSCAN (eps default 0.4) or hierarchical clustering (complete, single, or average linkage) to cluster each bucket. Enable post-clustering refinement to improve result quality. Record total end-to-end runtime and verify it meets the <15 minute threshold on comparable hardware.

## Related tools

- **HyperSpec** (Core clustering library implementing hyperdimensional encoding, GPU-accelerated Hamming distance computation, and DBSCAN/hierarchical clustering.) — https://github.com/wh-xu/Hyper-Spec
- **Python 3.8+** (Programming language runtime required to execute HyperSpec.)
- **CUDA** (GPU compute framework required for GPU-accelerated encoding and distance computation.)
- **DBSCAN / Hierarchical Clustering** (Clustering algorithms applied to Hamming distance matrices; selectable via --cluster_alg parameter.)

## Examples

```
python src/main.py ~/dataset/ ./output.csv --cpu_core_preprocess=4 --cluster_alg dbscan --use_gpu_cluster --cluster_charges 2 3 --eps=0.2 --refine
```

## Evaluation signals

- End-to-end runtime on 25M-spectra dataset is <15 minutes on GTX 3090 or equivalent GPU hardware.
- Output parquet/CSV file contains one row per input spectrum with valid cluster labels (non-negative integers) and is_representative boolean flag.
- Cluster assignment is deterministic: re-running with identical parameters produces identical cluster IDs.
- Pairwise Hamming distances between spectra in the same cluster are below the eps threshold; distances between clusters exceed eps.
- Representative spectra are correctly flagged (typically highest intensity or closest to cluster centroid in HD space).

## Limitations

- Requires NVIDIA GPU with sufficient VRAM; PXD000561 (25M spectra) requires GTX 3090 with larger memory; smaller datasets can use GTX 1080Ti.
- Performance depends on SSD speed; high-performance SSD storage is recommended for best throughput during I/O-heavy preprocessing.
- HD dimension and quantization level (hd_dim, hd_Q) are fixed hyperparameters; no dynamic adaptation to dataset characteristics.
- Clustering quality and runtime vary with charge state filtering, m/z range, and other preprocessing thresholds; parameter tuning required for novel datasets.
- No built-in support for spectra with missing or very sparse peak lists; minimum peak count filtering required.

## Evidence

- [readme] HyperSpec adopts the brain-inspired hyperdimensional (HD) computing to project the spectra data into binary hyperdimensional space to obtain better clustering quality and faster clustering speed.: "HyperSpec adopts the brain-inspired hyperdimensional (HD) computing to project the spectra data into binary hyperdimensional space to obtain better clustering quality and faster clustering speed."
- [readme] HyperSpec shortens the runtime on the draft human proteome dataset with 25 million spectra from a few hours to <15 minutes.: "HyperSpec shortens the runtime on the draft human proteome dataset with 25 million spectra from a few hours to <15 minutes."
- [readme] HyperSpec first encodes the processed spectra into binary hypervector (HV) with ultra-high dimension (>1000) based on level-id encoding method.: "HyperSpec first encodes the processed spectra into binary hypervector (HV) with ultra-high dimension (>1000) based on level-id encoding method."
- [readme] The entire dataset is divided into small buckets and the pairwise Hamming distance matrix for each bucket is computed.: "The entire dataset is divided into small buckets and the pairwise Hamming distance matrix for each bucket is computed."
- [readme] HyperSpec finally clusters each spectra bucket using DBSCAN algorithm.: "HyperSpec finally clusters each spectra bucket using DBSCAN algorithm."
- [readme] HyperSpec requires `Python 3.8+` with `CUDA` environment. A GPU should be installed properly.: "HyperSpec requires `Python 3.8+` with `CUDA` environment. A GPU should be installed properly."
- [readme] Clustering for PXD000561 dataset requires GTX 3090 with larger memory: "Clustering for PXD000561 dataset requires GTX 3090 with larger memory"
- [readme] We recommend using high-performance SSD as the storage device for the best performance.: "We recommend using high-performance SSD as the storage device for the best performance."
- [readme] The exported meta data for clustering results are compressed and stored in `parquet` file, which records `bucket`, `precursor_charge`, `precursor_mz`, `identifier`, `scan`, `retention_time`, `cluster`, and `is_representative` information.: "The exported meta data for clustering results are compressed and stored in `parquet` file, which records `bucket`, `precursor_charge`, `precursor_mz`, `identifier`, `scan`, `retention_time`,"
