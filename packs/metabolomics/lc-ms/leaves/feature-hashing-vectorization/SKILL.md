---
name: feature-hashing-vectorization
description: Use when when you have high-resolution tandem MS/MS spectra in mzML, mzXML, or MGF format and need to cluster or search millions of spectra efficiently.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - falcon
  - spectrum-utils
  techniques:
  - LC-MS
derived_from:
- doi: 10.1002/rcm.9153
  title: falcon
evidence_spans:
- The _falcon_ spectrum clustering tool uses advanced algorithmic techniques for highly efficient processing of millions of MS/MS spectra.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_falcon
    doi: 10.1002/rcm.9153
    title: falcon
  dedup_kept_from: coll_falcon
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1002/rcm.9153
  all_source_dois:
  - 10.1002/rcm.9153
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# feature-hashing-vectorization

## Summary

Converts high-resolution MS/MS spectra into fixed-size, low-dimensional dense vectors by binning m/z ranges and applying non-cryptographic hash functions, enabling efficient nearest-neighbor indexing and similarity searching at scale.

## When to use

When you have high-resolution tandem MS/MS spectra in mzML, mzXML, or MGF format and need to cluster or search millions of spectra efficiently. This skill is essential when exhaustive pairwise spectrum comparison is computationally prohibitive and you require a compact, hashable representation that preserves cosine similarity.

## When NOT to use

- Spectra are already in a pre-computed feature vector format or embedded representation
- Analysis requires exact fragment mass preservation and cannot tolerate hash collisions
- Low-dimensional approximation is inadequate for your similarity metric (e.g., if you require fragment-level annotation rather than cosine similarity)

## Inputs

- High-resolution MS/MS spectra in mzML, mzXML, or MGF format
- Spectrum metadata (precursor m/z, retention time)
- Fragment mass tolerance (in Dalton) and peak intensity values

## Outputs

- Fixed-size low-dimensional feature vectors (dense NumPy arrays or sparse matrices)
- Hashed feature matrix in numerical format (e.g., NumPy array, SciPy sparse matrix, or CSV)
- Vector dimensionality and hash function parameters for reproducibility

## How to apply

First, bin high-resolution spectra across the m/z range using small mass bins (typically a few Daltons each) to create sparse, high-dimensional vectors that tightly capture fragment masses. Then apply a non-cryptographic hash function (the falcon pipeline uses MurmurHash3) to map individual mass bins to a smaller number of hash bins, producing a fixed-size low-dimensional vector. The hashing process conserves cosine similarity between original spectra, allowing the hashed vectors to approximate true spectral similarity. Normalize peak intensities during binning and tune the final vector dimensionality (controlled by the `low_dim` parameter) to balance memory efficiency against approximation accuracy—larger vectors more accurately reflect true cosine distances but increase memory and query time. This vectorization step must precede nearest neighbor index construction.

## Related tools

- **falcon** (Implements spectrum binning, feature hashing, and end-to-end spectrum clustering pipeline; coordinates vectorization with nearest-neighbor indexing and density-based clustering) — https://github.com/bittremieux/falcon
- **spectrum-utils** (Provides spectrum I/O and basic preprocessing utilities (loading mzML/mzXML, filtering, normalization) upstream of feature hashing)

## Examples

```
falcon peak/*.mzml --export_representatives --precursor_tol 20 ppm --fragment_tol 0.05 --eps 0.10
```

## Evaluation signals

- Output vector has expected fixed dimensionality (controlled by `low_dim` parameter); all spectra produce vectors of identical length
- Vector sparsity and memory footprint are consistent with input spectrum count and hash parameters; no NaN or infinite values
- Cosine similarity between hashed vectors correlates strongly with cosine similarity computed on original (unhashed) spectra, validated on a small ground-truth subset
- Downstream nearest-neighbor search retrieves plausible candidates (same precursor m/z ± tolerance, similar retention time or fragmentation pattern) as top matches
- Hash collisions do not artificially inflate similarity; sensitivity analysis shows result stability across different `low_dim` and hash seed values

## Limitations

- Hash collisions can artificially inflate similarity between unrelated spectra; collision rate increases as `low_dim` decreases
- Feature hashing is lossy; spectral information is approximated, not preserved exactly; unsuitable if fragment-level annotation or peak reconstruction is required
- Binning granularity and hash function parameters must be tuned empirically for each data type (proteomics, metabolomics, top-down); default settings are optimized for bottom-up proteomics data
- Precursor m/z bucketing (splitting vectors into separate buckets per precursor mass) can create artificial boundaries; spectra near bucket boundaries may not find true neighbors if tolerance is tight
- Performance depends critically on `low_dim` choice; README notes that 'larger vectors will more accurately approximate the true cosine distance, at the expense of longer nearest neighbor searching and memory requirements'

## Evidence

- [intro] High-resolution spectra are binned and converted to low-dimensional vectors using feature hashing: "First, high-resolution spectra are binned and converted to low-dimensional vectors using feature hashing."
- [readme] Hashing conserves cosine similarity and approximates original spectrum similarity: "the sparse, high-dimensional, vectors are hashed to lower-dimensional vectors by using a hash function (the non-cryptographic MurmurHash3 algorithm) to map the mass bins separately to a small number"
- [readme] Binning process captures fragment masses in small m/z bins: "First, spectra are converted to sparse vectors using small mass bins to tightly capture their fragment masses."
- [readme] Low-dimensional vector size trades off accuracy and computational cost: "low_dim: The length of the low-dimensional vectors used for nearest neighbor searching. Larger vectors will more accurately approximate the true cosine distance, at the expense of longer nearest"
- [readme] Input file formats supported for vectorization: "falcon takes peak files (in the mzML, mzXML, or MGF format) as input"
