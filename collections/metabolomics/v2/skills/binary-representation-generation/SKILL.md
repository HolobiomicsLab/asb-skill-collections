---
name: binary-representation-generation
description: Use when you have raw mass spectra data (MGF format with m/z/intensity pairs) that need to be clustered rapidly, especially on large-scale proteomics datasets (millions of spectra).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python 3.8+
  - HyperSpec
  - Python
  - CUDA
  - Docker
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
---

# binary-representation-generation

## Summary

Encode mass spectra into binary hyperdimensional vectors using brain-inspired hyperdimensional computing and level-id encoding, enabling ultrafast clustering through lightweight Hamming distance computation. This skill transforms raw m/z-intensity peak data into ultra-high-dimensional (>1000) binary representations that preserve spectral similarity while accelerating downstream clustering.

## When to use

You have raw mass spectra data (MGF format with m/z/intensity pairs) that need to be clustered rapidly, especially on large-scale proteomics datasets (millions of spectra). Use this skill when conventional feature-based clustering is too slow and you need to exploit GPU acceleration for Hamming distance computation over dense, high-dimensional vector spaces.

## When NOT to use

- Input spectra are already encoded in a feature space (e.g., cosine-normalized peak vectors or ML embeddings); re-encoding may degrade information.
- Target downstream analysis does not use Hamming distance or DBSCAN; other clustering metrics (Euclidean, cosine) may be more appropriate.
- GPU memory is unavailable or insufficient for batch processing; CPU-only environments will experience significant slowdown relative to the claimed performance gains.

## Inputs

- MGF file(s) containing raw mass spectra (m/z/intensity peak pairs)
- Preprocessing parameters (min_peaks, min_intensity, max_peaks_used, scaling method)
- HD encoding parameters (hd_dim, hd_Q, id_flip_factor, batch_size)

## Outputs

- Binary hyperdimensional vectors (one per spectrum, dimensionality > 1000)
- Encoded spectra checkpoint file (optional, for serialization)
- Metadata table with bucket assignments, precursor m/z, charge, and encoded vector indices

## How to apply

Load raw mass spectra from MGF files containing m/z and intensity pairs. Apply preprocessing filters (e.g., min_peaks, min_intensity, max_peaks_used thresholds, and intensity scaling via root/log/rank methods). Encode each preprocessed spectrum using level-id encoding with configurable HD dimensionality (default 2048) and quantization level (default Q=16). The encoding projects each spectrum into a binary hypervector on GPU in batches (default batch_size=5000), then validate that all encoded vectors are strictly binary format and match the target dimensionality. The rationale is that HD computing's lightweight representation allows pairwise Hamming distance matrices to be computed efficiently on GPU, circumventing the O(n²) bottleneck of traditional distance metrics.

## Related tools

- **HyperSpec** (Primary implementation framework for brain-inspired hyperdimensional computing, level-id encoding, GPU-accelerated batch vectorization, and Hamming distance computation) — https://github.com/wh-xu/Hyper-Spec
- **Python** (Programming language required (3.8+) for HyperSpec execution and preprocessing scripting)
- **CUDA** (GPU compute backend for batch HD encoding and Hamming distance matrix computation)
- **Docker** (Containerized environment for reproducible HyperSpec deployment with pre-configured CUDA and dependencies) — https://github.com/wh-xu/Hyper-Spec/blob/main/docker/Dockerfile

## Examples

```
python src/main.py ~/dataset/ ./output.csv --cpu_core_preprocess=4 --batch_size=5000 --hd_dim=2048 --hd_Q=16 --scaling=root --max_peaks_used=200 --min_intensity=10 --use_gpu_cluster
```

## Evaluation signals

- All output binary hypervectors have exactly hd_dim bits (e.g., 2048); check vector length invariant via len(encoded_vector) == hd_dim.
- Each encoded vector is strictly binary (contains only 0 and 1 values); validate via set(encoded_vector) ⊆ {0, 1}.
- Pairwise Hamming distances between encoded spectra are computable and fall in the range [0, hd_dim]; a few spot-checks should confirm distance computation completes without NaN or overflow.
- Downstream DBSCAN/hierarchical clustering with eps threshold (e.g., 0.2–0.4) produces non-trivial cluster assignments (neither all singletons nor one giant cluster) on hold-out subsets.
- Runtime on a GPU (e.g., GTX 3090) for encoding 25M spectra is <15 min total; compare wall-clock time before/after to confirm speedup relative to baseline.

## Limitations

- Requires a GPU (tested on GTX 1080Ti and GTX 3090); clustering large datasets (e.g., PXD000561) requires higher-memory GPUs (GTX 3090 recommended).
- Level-id encoding parameters (hd_dim, hd_Q) are fixed at encoding time; downstream clustering performance is sensitive to these hyperparameters and may require tuning for new datasets.
- HD encoding assumes m/z and intensity ranges are preprocessed consistently (min_peaks, max_peaks_used, intensity scaling); inconsistent preprocessing across batches may produce spurious or non-comparable vectors.
- Binary HD vectors do not preserve absolute intensity magnitudes or fine-grained peak ordering, only aggregate spectral similarity; spectral libraries or de novo sequencing tasks requiring peak-level detail may need supplementary representations.

## Evidence

- [intro] HyperSpec adopts the brain-inspired hyperdimensional (HD) computing to project the spectra data into binary hyperdimensional space to obtain better clustering quality and faster clustering speed.: "adopts the brain-inspired hyperdimensional (HD) computing to project the spectra data into binary hyperdimensional space to obtain better clustering quality and faster clustering speed"
- [intro] HyperSpec shortens the runtime on the draft human proteome dataset with 25 million spectra from a few hours to <15 minutes.: "shortens the runtime on the draft human proteome dataset with 25 million spectra from a few hours to <15 minutes"
- [readme] _HyperSpec_ first encodes the processed spectra into binary hypervector (HV) with ultra-high dimension (>1000) based on level-id encoding method. The encoding module is implemented and optimized for GPU for shorter runtime.: "encodes the processed spectra into binary hypervector (HV) with ultra-high dimension (>1000) based on level-id encoding method. The encoding module is implemented and optimized for GPU"
- [other] Load raw mass spectra from input file (mz/intensity pairs). 2. Apply brain-inspired hyperdimensional (HD) computing projection to encode each spectrum into a binary hyperdimensional vector representation. 3. Validate encoding dimensionality and binary format compliance.: "Apply brain-inspired hyperdimensional (HD) computing projection to encode each spectrum into a binary hyperdimensional vector representation. 3. Validate encoding dimensionality and binary format"
- [readme] _HyperSpec_ requires `Python 3.8+` with `CUDA` environment. A GPU should be installed properly.: "requires `Python 3.8+` with `CUDA` environment. A GPU should be installed properly"
- [readme] --batch_size BATCH_SIZE] [--use_gpu_cluster] [--min_peaks MIN_PEAKS] [--mz_interval MZ_INTERVAL] [--min_intensity MIN_INTENSITY] [--max_peaks_used MAX_PEAKS_USED] [--scaling {off,root,log,rank}] [--hd_dim HD_DIM] [--hd_Q HD_Q]: "--batch_size BATCH_SIZE] [--use_gpu_cluster] [--min_peaks MIN_PEAKS] [--min_intensity MIN_INTENSITY] [--max_peaks_used MAX_PEAKS_USED] [--scaling {off,root,log,rank}] [--hd_dim HD_DIM] [--hd_Q HD_Q]"
- [readme] The pairwise Hamming distance matrix for each bucket is computed. _HyperSpec_ implements very efficient Hamming distance computation kernels on GPU.: "pairwise Hamming distance matrix for each bucket is computed. _HyperSpec_ implements very efficient Hamming distance computation kernels on GPU"
