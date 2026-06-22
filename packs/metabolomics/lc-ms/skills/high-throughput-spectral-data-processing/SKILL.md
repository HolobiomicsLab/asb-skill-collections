---
name: high-throughput-spectral-data-processing
description: Use when when you have MGF-formatted mass spectrometry peak files (typically from proteomics experiments) numbering in the millions of spectra that require grouping into similar MS/MS clusters, and runtime must be kept under 15 minutes rather than hours.
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

# high-throughput-spectral-data-processing

## Summary

Process and cluster millions of mass spectra using GPU-accelerated hyperdimensional computing to project spectra into binary hypervector space, enabling sub-15-minute runtimes on datasets that would otherwise require hours. This skill is essential when proteomics workflows must handle draft human proteome scales (25M+ spectra) with speed and clustering quality constraints.

## When to use

When you have MGF-formatted mass spectrometry peak files (typically from proteomics experiments) numbering in the millions of spectra that require grouping into similar MS/MS clusters, and runtime must be kept under 15 minutes rather than hours. Specifically triggered by need to cluster large proteome datasets (e.g., PXD000561 or equivalent 25M-spectra draft human proteome) on GPU-equipped infrastructure.

## When NOT to use

- Input spectra are already in a pre-computed distance matrix or feature table format; use direct clustering instead.
- Dataset is small (<1M spectra) or runtime is not a constraint; simpler CPU-based clustering may suffice.
- GPU hardware (NVIDIA with CUDA support) is unavailable; HyperSpec requires GPU for its speed advantage.

## Inputs

- MGF peak files (mass spectrometry data in text format with m/z and intensity pairs)
- Directory path containing one or more MGF files
- Spectrum metadata (precursor m/z, charge state, retention time, scan identifier)

## Outputs

- CSV or parquet file with one spectrum per row and assigned cluster label
- Parquet metadata table with columns: bucket, precursor_charge, precursor_mz, identifier, scan, retention_time, cluster, is_representative
- Optional: representative spectra MGF file (if --representative_mgf flag enabled)
- Optional: checkpoint file with encoded hypervectors for checkpointing

## How to apply

Load MGF files from your input directory into HyperSpec with CUDA GPU acceleration enabled. Apply level-id encoding to project each preprocessed spectrum into a binary hypervector of ultra-high dimension (default 2048 dimensions, adjustable via --hd_dim). Configure preprocessing CPU cores (--cpu_core_preprocess, default 6) to handle spectrum intensity filtering, m/z range clipping (--min_mz, --max_mz), and peak count filtering (--min_peaks). Divide the encoded dataset into small spatial buckets and compute pairwise Hamming distance matrices on GPU. Finally, apply DBSCAN or hierarchical clustering (--cluster_alg, default hc_complete) with a distance threshold (--eps, typically 0.2–0.4) and optional post-clustering refinement (--refine flag). Monitor that end-to-end runtime remains <15 minutes and verify cluster labels are assigned to each spectrum in the output parquet file.

## Related tools

- **HyperSpec** (GPU-accelerated hyperdimensional encoding and DBSCAN/hierarchical clustering engine for mass spectra) — https://github.com/wh-xu/Hyper-Spec
- **Python 3.8+** (Runtime environment for HyperSpec)
- **CUDA** (GPU compute framework required for HyperSpec acceleration)

## Examples

```
python src/main.py ~/dataset/ ./output.csv --cpu_core_preprocess=4 --cluster_alg dbscan --use_gpu_cluster --cluster_charges 2 3 --eps=0.2 --refine
```

## Evaluation signals

- End-to-end runtime on 25M spectra dataset completes in <15 minutes (vs. baseline hours without GPU acceleration).
- Output parquet file contains one row per spectrum with valid cluster label (integer ≥ 0) and is_representative boolean flag.
- Clustering quality preserved: within-cluster Hamming distances should be lower than between-cluster distances; representative spectra should be marked correctly.
- Spectrum count in output matches input spectrum count; no spectra dropped or duplicated during encoding or clustering.
- Metadata columns (precursor_charge, precursor_mz, retention_time, scan identifier) are preserved and non-null in output.

## Limitations

- Clustering for the largest datasets (PXD000561, 25M spectra) requires GTX 3090 or equivalent high-memory GPU; smaller GPUs (e.g., GTX 1080Ti) only support smaller datasets.
- Hypervector dimension (--hd_dim) and quantization level (--hd_Q) are fixed at encode time; altering them requires re-encoding, not reuse of cached hypervectors.
- DBSCAN threshold (--eps) and hierarchical clustering linkage method are user-tunable but lack automated parameter selection; suboptimal choices may yield poor clusters or over-fragmentation.
- Performance gains are heavily dependent on SSD storage speed; the README recommends high-performance SSDs for best I/O throughput.

## Evidence

- [intro] HyperSpec shortens the runtime on the draft human proteome dataset with 25 million spectra from a few hours to <15 minutes.: "HyperSpec shortens the runtime on the draft human proteome dataset with 25 million spectra from a few hours to <15 minutes."
- [intro] HyperSpec adopts brain-inspired hyperdimensional computing to project spectra data into binary hyperdimensional space.: "HyperSpec adopts the brain-inspired hyperdimensional (HD) computing to project the spectra data into binary hyperdimensional space to obtain better clustering quality and faster clustering speed."
- [readme] HyperSpec requires Python 3.8+ with CUDA environment and GPU support.: "HyperSpec requires `Python 3.8+` with `CUDA` environment. A GPU should be installed properly."
- [readme] Clustering for PXD000561 dataset requires GTX 3090 with larger memory.: "Clustering for PXD000561 dataset requires GTX 3090 with larger memory"
- [readme] HyperSpec takes MGF peak files as input and exports clustering result as CSV with spectrum and cluster label.: "HyperSpec supports running using the command line and takes `MGF` peak files as input and exports the clustering result as a CSV file with each MS/MS spectrum and its cluster label on a single line."
- [readme] HyperSpec encodes spectra into binary hypervectors, computes Hamming distance matrices per bucket, then clusters with DBSCAN.: "HyperSpec first encodes the processed spectra into binary hypervector (HV) with ultra-high dimension (>1000) based on level-id encoding method. The entire dataset is divided into small buckets and"
- [readme] Output format is compressed parquet with spectrum metadata and cluster assignment.: "The exported meta data for clustering results are compressed and stored in `parquet` file, which records `bucket`, `precursor_charge`, `precursor_mz`, `identifier`, `scan`, `retention_time`,"
- [readme] High-performance SSD is recommended for best performance.: "We recommend using high-performance SSD as the storage device for the best performance."
