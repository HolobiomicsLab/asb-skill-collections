---
name: open-modification-spectral-search-strategy
description: Use when when searching an unknown query MS/MS spectrum against a large spectral library (>100k spectra) for both unmodified and modified peptides, and computational speed is critical without sacrificing sensitivity or FDR control.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - ANN-SoLo
  - Faiss
derived_from:
- doi: 10.1021/acs.jproteome.8b00359
  title: ANN-SoLo
evidence_spans:
- '**ANN-SoLo** (**A**pproximate **N**earest **N**eighbor **S**pectral **L**ibrary) is a spectral library search engine'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ann_solo_gpu_feature_hashing_cq
    doi: 10.1021/acs.jproteome.8b00359
    title: ANN-SoLo
  dedup_kept_from: coll_ann_solo_gpu_feature_hashing_cq
schema_version: 0.2.0
---

# open-modification-spectral-search-strategy

## Summary

A hybrid search strategy combining approximate nearest neighbor indexing with cascade scoring to accelerate open modification searching on MS/MS spectral libraries while controlling false discovery rate. ANN-SoLo reduces the library candidate set from millions of spectra to a tractable K-sized subset for detailed scoring.

## When to use

When searching an unknown query MS/MS spectrum against a large spectral library (>100k spectra) for both unmodified and modified peptides, and computational speed is critical without sacrificing sensitivity or FDR control. Particularly suited when the query may match spectra with unexpected post-translational modifications (PTMs) or chemical modifications.

## When NOT to use

- When the spectral library is small (<10k spectra) — sequential comparison without ANN indexing may be faster and simpler.
- When only unmodified peptide matching is required and open modification search is not needed — standard closed-search methods are more straightforward.
- When the query spectrum lacks sufficient spectral feature density or quality for reliable vectorization — ANN indexing requires reproducible feature representations.

## Inputs

- MS/MS spectral library (reference spectra in vectorized numerical form)
- Query MS/MS spectrum (unknown peptide spectrum to be identified)
- Spectral feature representation (intensity vectors or derived features suitable for ANN indexing)
- K parameter (number of nearest neighbors to retrieve)
- FDR threshold value(s) for cascade filtering stages

## Outputs

- Ranked list of candidate library spectra (K most similar to query)
- Cascade-filtered match scores with FDR-controlled confidence
- Peptide sequence identifications for unmodified and modified spectra
- False discovery rate estimates at each cascade stage

## How to apply

First, preprocess and vectorize both the spectral library and query spectrum into a numerical representation (e.g., intensity vectors or spectral features). Build an approximate nearest neighbor index over library spectra using a space-partitioning algorithm (e.g., Faiss). Query the ANN index with the unknown spectrum to retrieve the K most similar library spectra candidates. Combine this with a cascade search strategy: score the K candidates with a sensitive metric (e.g., shifted dot product to account for mass shifts from modifications), then apply stringent FDR thresholds at each cascade stage to maximize identifications while strictly controlling false positives. The rationale is that true matches will rank highly in both the ANN retrieval and subsequent cascade stages, whereas random matches are unlikely to survive both filters.

## Related tools

- **ANN-SoLo** (Reference implementation of the hybrid ANN + cascade search strategy for open modification spectral library searching; provides the exact algorithm, indexing backend (Faiss), and shifted dot product scoring described in the method) — https://github.com/bittremieux/ANN-SoLo
- **Faiss** (Underlying approximate nearest neighbor indexing library used by ANN-SoLo to build and query the space-partitioned index over library spectra) — https://github.com/facebookresearch/faiss

## Examples

```
pip install ann_solo; python -m ann_solo.spectrum_match --library spectral_library.mgf --query unknown_spectrum.mgf --output results.csv
```

## Evaluation signals

- Candidate set size equals K (verify retrieval returned exactly K nearest neighbors from the ANN index).
- Retrieved candidates have increasing cosine similarity or dot product scores relative to random library spectra, confirming ANN ranking is meaningful.
- Cascade-stage match scores improve monotonically through stages (e.g., unmodified → modified candidates → shifted dot product refinement) and survive FDR thresholds.
- False discovery rate of final identifications remains ≤ user-specified threshold (e.g., 1% or 5% FDR) when validated against decoy library or known negatives.
- Sensitivity (% true positives recovered) is comparable to or exceeds full library search, confirming cascade filtering does not eliminate true matches despite ANN candidate reduction.

## Limitations

- Python 3.6–3.9 only; Python 3.10+ not currently supported. GPU acceleration requires Linux with NVIDIA CUDA-enabled hardware.
- ANN indexing introduces a small recall loss — true matches may occasionally rank outside the K nearest neighbors if their vectorized representation differs substantially from the query due to extreme modifications or spectral noise.
- Cascade search strategy effectiveness depends on appropriate tuning of K, shifted dot product mass shift tolerance, and FDR thresholds; suboptimal parameters may increase false negatives or false positives.
- Vectorization quality is critical; spectra with very low precursor intensity, severe fragmentation, or extensive noise may produce unreliable feature representations and poor ANN rankings.

## Evidence

- [other] ANN-SoLo applies approximate nearest neighbor indexing to select only a limited number of the most relevant library spectra for comparison to an unknown query spectrum, thereby accelerating open modification searching.: "ANN-SoLo applies approximate nearest neighbor indexing to select only a limited number of the most relevant library spectra for comparison to an unknown query spectrum, thereby accelerating open"
- [other] Preprocess and vectorize spectra into a numerical representation suitable for ANN indexing, then build an ANN index over library spectra, query it to retrieve K candidates, and return ranked candidates for downstream scoring and cascade search.: "Preprocess and vectorize spectra into a numerical representation suitable for ANN indexing (e.g., intensity vectors or spectral features). 3. Build an approximate nearest neighbor index over the"
- [intro] Cascade search strategy is combined to maximize the number of identified unmodified and modified spectra while strictly controlling the false discovery rate: "This is combined with a cascade search strategy to maximize the number of identified unmodified and modified spectra while strictly controlling the false discovery rate"
- [readme] ANN-SoLo uses the shifted dot product score to sensitively match modified spectra to their unmodified counterpart in conjunction with ANN candidate selection.: "shifted dot product score to sensitively match modified spectra to their unmodified counterpart"
- [readme] NumPy and Faiss are required dependencies; Faiss installation depends on a specific GPU version and supports Linux with NVIDIA CUDA-enabled GPU or CPU-only on Linux and OSX.: "The GPU-powered version of ANN-SoLo can be used on Linux systems with an NVIDIA CUDA-enabled GPU device, while the CPU-only version supports both the Linux and OSX platforms"
