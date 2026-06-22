---
name: hyperdimensional-vector-encoding
description: Use when you have preprocessed mass spectra (mz/intensity pairs in MGF format) and need to convert them into a compact, fixed-dimensional representation suitable for fast similarity computation and clustering.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Python 3.8+
  - HyperSpec
  - CUDA
  techniques:
  - mass-spectrometry
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

# hyperdimensional-vector-encoding

## Summary

Encodes mass spectra into binary hypervectors of ultra-high dimensionality (>1000) using level-id encoding, enabling lightweight yet powerful data representation for downstream clustering. This brain-inspired approach projects m/z–intensity pairs into hyperdimensional space to improve clustering quality and speed.

## When to use

Apply this skill when you have preprocessed mass spectra (mz/intensity pairs in MGF format) and need to convert them into a compact, fixed-dimensional representation suitable for fast similarity computation and clustering. The technique is especially valuable when clustering large-scale datasets (millions of spectra) where traditional distance metrics become computationally expensive.

## When NOT to use

- Input spectra are already in feature vector form (e.g., fingerprints, already-embedded representations) — encoding is redundant.
- You require interpretability of individual dimensions or direct correlation to m/z bins — hyperdimensional encoding obscures peak-level attribution.
- GPU memory is unavailable and CPU-only encoding is mandatory — the method is optimized for GPU and slower on CPU alone.

## Inputs

- MGF files containing raw mass spectra (mz/intensity peak pairs)
- Preprocessed spectra with filtering applied (peak count, intensity thresholds, m/z range)
- Configuration parameters: HD dimensionality, quantization level, batch size

## Outputs

- Binary hypervectors (high-dimensional, typically 2048–8192 dimensions)
- Encoded spectra checkpoint file (optional parquet or binary format)
- Metadata linking each hypervector to original spectrum identifiers and precursor properties

## How to apply

Load raw mass spectra from MGF input files containing mz/intensity peak pairs. Apply level-id encoding to project each spectrum into a binary hypervector of configurable dimensionality (default: 2048) with quantization level (default: 16). The encoding is GPU-accelerated and batched for efficiency (default batch size: 5000). Each spectrum is transformed into a high-dimensional binary representation that preserves spectral similarity relationships while enabling Hamming distance computation. Validate that output hypervectors are binary format and match the specified HD dimensionality before export.

## Related tools

- **HyperSpec** (Python library providing GPU-accelerated level-id encoding and HD projection for mass spectra) — https://github.com/wh-xu/Hyper-Spec
- **Python 3.8+** (Language runtime for encoding pipeline and CUDA integration)
- **CUDA** (GPU compute platform enabling parallel hypervector encoding and Hamming distance computation)

## Examples

```
python src/main.py ~/dataset/ ./output.csv --cpu_core_preprocess=4 --hd_dim=2048 --hd_Q=16 --batch_size=5000 --use_gpu_cluster --cluster_alg dbscan
```

## Evaluation signals

- Output hypervectors are binary (all values 0 or 1) and match the configured HD dimensionality exactly.
- Hamming distances between encoded spectra are computable in O(n/64) time per pair (bitwise operations), confirming binary format.
- Spectra with high cosine similarity in original m/z space produce low Hamming distance in HD space (inverse relationship validation).
- Encoding batch throughput meets expected GPU performance (e.g., >5000 spectra/second on GTX 3090) indicating correct GPU utilization.
- Clustering results on encoded vectors show comparable or improved silhouette score and purity compared to baseline clustering on raw spectra.

## Limitations

- Encoding quality depends on careful tuning of quantization level (HD_Q) and dimensionality (HD_DIM); suboptimal settings reduce clustering coherence.
- Large-scale datasets (>25M spectra) require high-memory GPU (GTX 3090 recommended; GTX 1080Ti sufficient for smaller datasets per README).
- Brain-inspired level-id encoding is a lossy projection; original m/z values cannot be recovered from hypervectors.
- GPU availability is mandatory for production performance; CPU fallback is orders of magnitude slower.

## Evidence

- [readme] HyperSpec first encodes the processed spectra into binary hypervector (HV) with ultra-high dimension (>1000) based on level-id encoding method.: "_HyperSpec_ first encodes the processed spectra into binary hypervector (HV) with ultra-high dimension (>1000) based on level-id encoding method."
- [intro] HyperSpec adopts brain-inspired hyperdimensional computing to project spectra data into binary hyperdimensional space for better clustering quality and faster clustering speed.: "_HyperSpec_ adopts the brain-inspired hyperdimensional (HD) computing to project the spectra data into binary hyperdimensional space to obtain better clustering quality and faster clustering speed."
- [other] Apply brain-inspired HD computing projection to encode each spectrum into a binary hyperdimensional vector representation; validate encoding dimensionality and binary format compliance.: "Apply brain-inspired hyperdimensional (HD) computing projection to encode each spectrum into a binary hyperdimensional vector representation. 3. Validate encoding dimensionality and binary format"
- [readme] The HD dimension defaults to 2048 and quantization level defaults to 16.: "--hd_dim                    The HD dimension. (default: 2048)"
- [intro] HyperSpec shortens runtime on 25 million spectra from hours to <15 minutes using HD encoding and GPU acceleration.: "_HyperSpec_ shortens the runtime on the draft human proteome dataset with 25 million spectra from a few hours to <15 minutes."
- [readme] The encoding module is implemented and optimized for GPU for shorter runtime.: "The encoding module is implemented and optimized for GPU for shorter runtime."
