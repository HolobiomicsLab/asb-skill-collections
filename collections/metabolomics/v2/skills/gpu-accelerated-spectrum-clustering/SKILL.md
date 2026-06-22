---
name: gpu-accelerated-spectrum-clustering
description: Use when you have a large collection of tandem mass spectra (≥100k spectra) in MGF format and need to group spectra by similarity (precursor m/z, charge, and fragment ion patterns) for spectral library construction, peptide identification, or quality control.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3676
  tools:
  - Python 3.8+
  - HyperSpec
  - Python
  - CUDA
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

# GPU-accelerated spectrum clustering

## Summary

Use GPU-accelerated hyperdimensional computing to cluster mass spectra from MGF files into groups of similar fragmentation patterns at scale. This skill applies brain-inspired binary encoding and Hamming distance computation on NVIDIA GPUs to achieve clustering runtimes of <15 minutes on 25 million spectra.

## When to use

You have a large collection of tandem mass spectra (≥100k spectra) in MGF format and need to group spectra by similarity (precursor m/z, charge, and fragment ion patterns) for spectral library construction, peptide identification, or quality control. GPU clustering is especially valuable when clustering datasets exceed GTX 1080Ti memory limits (use GTX 3090 for PXD000561-scale datasets with >1M spectra).

## When NOT to use

- Input spectra are already pre-clustered or belong to a known spectral library and no new clustering is needed.
- Available GPU memory is insufficient for the dataset size (e.g., attempting PXD000561-scale clustering on GTX 1080Ti without available GTX 3090).
- Spectra lack required metadata fields (precursor m/z, charge state, or scan identifiers) or are in unsupported formats (e.g., mzML, mzXML without prior MGF conversion).

## Inputs

- MGF file(s) containing MS/MS spectra with m/z, intensity, precursor m/z, precursor charge, scan identifiers, and retention time
- CUDA-compatible GPU device (NVIDIA GTX 1080Ti or GTX 3090, tested on Linux)
- Python 3.8+ environment with CUDA bindings

## Outputs

- Parquet or CSV file with cluster labels, bucket IDs, precursor charge, precursor m/z, identifiers, scan numbers, retention time, cluster group IDs, and is_representative flags
- Optional MGF file(s) of representative spectra per cluster

## How to apply

Preprocess spectra by filtering for target charge states (default: 2, 3) and applying intensity scaling (root, log, rank, or off). Encode filtered spectra into binary hypervectors using level-id encoding with configurable hyperdimension (default: 2048) and quantization levels (default: 16). Partition the encoded dataset into small buckets and compute pairwise Hamming distance matrices per bucket on GPU. Apply hierarchical clustering (default: complete linkage, eps=0.25) or DBSCAN (default: eps=0.4) per bucket, optionally with post-clustering refinement. Output cluster assignments and representative spectra (if requested) as parquet or CSV.

## Related tools

- **HyperSpec** (GPU-based clustering engine implementing hyperdimensional encoding, Hamming distance computation, and DBSCAN/hierarchical clustering) — https://github.com/wh-xu/Hyper-Spec
- **Python** (Runtime environment (3.8+) for HyperSpec execution)
- **CUDA** (GPU compute platform enabling GPU-accelerated HD encoding and distance matrix computation)

## Examples

```
python src/main.py ~/dataset/ ./output.csv --cpu_core_preprocess=4 --cluster_alg hc_complete --cluster_charges 2 3 --eps=0.25 --refine --hd_dim=2048 --hd_Q=16
```

## Evaluation signals

- Output parquet file contains all expected columns (bucket, precursor_charge, precursor_mz, identifier, scan, retention_time, cluster, is_representative) with no null values in cluster or precursor_charge fields for included spectra.
- Cluster assignments are deterministic across repeated runs with identical parameters and random seeds.
- Representative spectra per cluster have high intra-cluster Hamming similarity (reflected in DBSCAN/hierarchical clustering threshold) and low inter-cluster similarity.
- Runtime on 25 million spectra is <15 minutes on GTX 3090, or proportionally shorter on smaller datasets; GPU memory utilization stays within device limits.
- Post-clustering refinement (when enabled) merges small singleton clusters into nearby larger clusters, reducing total cluster count without losing significant spectral information.

## Limitations

- Tested on Linux only; Windows and macOS support not documented.
- Requires NVIDIA GPU with CUDA support; non-NVIDIA GPUs are untested.
- PXD000561-scale clustering requires GTX 3090; GTX 1080Ti memory insufficient for this dataset.
- Clustering quality depends on hyperparameter tuning (eps, hd_dim, hd_Q, scaling method); defaults may not be optimal for all datasets.
- No changelog available in repository; versioning and breaking changes not tracked.

## Evidence

- [intro] _HyperSpec_ shortens the runtime on the draft human proteome dataset with 25 million spectra from a few hours to <15 minutes.: "_HyperSpec_ shortens the runtime on the draft human proteome dataset with 25 million spectra from a few hours to <15 minutes."
- [intro] _HyperSpec_ adopts the brain-inspired hyperdimensional (HD) computing to project the spectra data into binary hyperdimensional space to obtain better clustering quality and faster clustering speed.: "_HyperSpec_ adopts the brain-inspired hyperdimensional (HD) computing to project the spectra data into binary hyperdimensional space to obtain better clustering quality and faster clustering speed."
- [readme] _HyperSpec_ requires `Python 3.8+` with `CUDA` environment. A GPU should be installed properly. _HyperSpec_ has been tested on two types of NVIDIA GPUs on a Linux platform, including GTX 1080Ti and GTX 3090.: "_HyperSpec_ requires `Python 3.8+` with `CUDA` environment. A GPU should be installed properly. _HyperSpec_ has been tested on two types of NVIDIA GPUs on a Linux platform, including GTX 1080Ti and"
- [readme] Clustering for PXD000561 dataset requires GTX 3090 with larger memory: "Clustering for PXD000561 dataset requires GTX 3090 with larger memory"
- [readme] The exported meta data for clustering results are compressed and stored in `parquet` file, which records `bucket`, `precursor_charge`, `precursor_mz`, `identifier`, `scan`, `retention_time`, `cluster`, and `is_representative` information.: "The exported meta data for clustering results are compressed and stored in `parquet` file, which records `bucket`, `precursor_charge`, `precursor_mz`, `identifier`, `scan`, `retention_time`,"
- [readme] _HyperSpec_ first encodes the processed spectra into binary hypervector (HV) with ultra-high dimension (>1000) based on level-id encoding method. The encoding module is implemented and optimized for GPU for shorter runtime.: "_HyperSpec_ first encodes the processed spectra into binary hypervector (HV) with ultra-high dimension (>1000) based on level-id encoding method. The encoding module is implemented and optimized for"
- [readme] The entire dataset is divided into small buckets and the pairwise Hamming distance matrix for each bucket is computed. _HyperSpec_ implements very efficient Hamming distance computation kernels on GPU.: "The entire dataset is divided into small buckets and the pairwise Hamming distance matrix for each bucket is computed. _HyperSpec_ implements very efficient Hamming distance computation kernels on"
- [readme] _HyperSpec_ finally clusters each spectra bucket using DBSCAN algorithm. Thanks HD computing's lightweight computation and powerful data presentation capability, _HyperSpec_ achieves significant speedup over other spectra clustering tools.: "_HyperSpec_ finally clusters each spectra bucket using DBSCAN algorithm. Thanks HD computing's lightweight computation and powerful data presentation capability, _HyperSpec_ achieves significant"
- [readme] --hd_dim HD_DIM The HD dimension. (default: 2048); --hd_Q HD_Q The HD quantization level. (default: 16); --eps EPS The threshold value `eps` for DBSCAN clustering. (default: 0.4); --cluster_alg {dbscan,hc_single,hc_complete,hc_average}: "--hd_dim HD_DIM The HD dimension. (default: 2048); --hd_Q HD_Q The HD quantization level. (default: 16); --eps EPS The threshold value `eps` for DBSCAN clustering. (default: 0.4); --cluster_alg"
