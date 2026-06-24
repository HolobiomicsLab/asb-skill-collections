---
name: mass-spectrometry-spectrum-vectorization
description: Use when you have high-resolution MS/MS spectra in mzML, mzXML, or MGF
  format and need to cluster or search across millions of spectra. The vectorization
  step is necessary before constructing nearest-neighbor indexes or computing pairwise
  distance matrices for spectrum clustering.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - falcon
  - spectrum-utils
  - Python 3.8+
  - mzBucket
  - pyproteolizard-data
  - pyproteolizard-algorithm
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1002/rcm.9153
  title: falcon
- doi: 10.1186/s12859-022-04833-5
  title: ''
evidence_spans:
- The _falcon_ spectrum clustering tool uses advanced algorithmic techniques for highly
  efficient processing of millions of MS/MS spectra.
- pip install falcon-ms spectrum-utils==0.3.5
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_falcon_cq
    doi: 10.1002/rcm.9153
    title: falcon
  - build: coll_mzbucket_cq
    doi: 10.1186/s12859-022-04833-5
    title: mzBucket
  dedup_kept_from: coll_falcon_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1002/rcm.9153
  all_source_dois:
  - 10.1002/rcm.9153
  - 10.1186/s12859-022-04833-5
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-spectrum-vectorization

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Convert high-resolution MS/MS spectra into low-dimensional dense or sparse vectors using binning and feature hashing, enabling efficient similarity searching and clustering of millions of spectra. This is the critical first step in the falcon spectrum clustering pipeline.

## When to use

You have high-resolution MS/MS spectra in mzML, mzXML, or MGF format and need to cluster or search across millions of spectra. The vectorization step is necessary before constructing nearest-neighbor indexes or computing pairwise distance matrices for spectrum clustering.

## When NOT to use

- Spectra are already pre-processed into a feature table or hashed vector format
- You are working with low-resolution or centroided spectra where the binning and hashing steps would be inappropriate
- Your analysis does not require similarity searching or clustering; downstream use case does not benefit from vectorization

## Inputs

- Peak files in mzML, mzXML, or MGF format containing high-resolution MS/MS spectra
- Raw MS/MS spectra with m/z and intensity peak values

## Outputs

- Low-dimensional hashed spectrum vectors (dense or sparse format)
- Vector file compatible with nearest-neighbor index construction

## How to apply

Load raw high-resolution MS/MS spectra using spectrum-utils. First, bin the m/z and intensity dimensions of each spectrum into small mass bins to capture fragment masses as a sparse vector. Then apply feature hashing (using the MurmurHash3 non-cryptographic hash function) to map the mass bins to a lower-dimensional vector space. The hashing conserves cosine similarity between the original spectra, allowing the hashed vectors to approximate the similarity of original spectra while reducing dimensionality for fast nearest-neighbor searching. Configure the `low_dim` parameter (length of hashed vectors) to balance accuracy against memory and query speed; larger vectors more accurately preserve cosine distance but increase memory and computation time.

## Related tools

- **falcon** (Spectrum clustering tool that orchestrates the vectorization step as the first stage of the clustering pipeline) — https://github.com/bittremieux/falcon
- **spectrum-utils** (Utility library for loading and manipulating raw MS/MS spectra from standard peak file formats)
- **Python 3.8+** (Runtime environment required to execute falcon and spectrum-utils)

## Examples

```
falcon peak/*.mzml falcon --export_representatives --precursor_tol 20 ppm --fragment_tol 0.05 --eps 0.10
```

## Evaluation signals

- Vectorized spectra retain cosine similarity relationships of original spectra (cosine distance between hashed vectors approximates the true distance)
- Output vectors have the expected dimensionality as specified by the `low_dim` parameter
- Vectors are stored in a format compatible with nearest-neighbor index construction (indexed by spectrum ID and precursor m/z)
- Spectral preprocessing filters (min_peaks, min_mz_range, m/z range bounds) have been applied correctly; verify by checking the number of peaks and m/z ranges in vectorized output
- No NaN or infinite values in the hashed vectors; all vectors have consistent length

## Limitations

- Feature hashing trades off dimensionality reduction against approximation error; collision artifacts may introduce noise into the hashed vectors, affecting subsequent clustering accuracy
- The `low_dim` parameter requires tuning based on spectral characteristics and dataset; values that are too small may lose critical information, while large values increase memory requirements
- Binning and hashing are optimized for bottom-up proteomics spectra; metabolomics or top-down proteomics data may require adjusted preprocessing parameters (min_peaks, min_mz_range, m/z bounds) for appropriate vectorization
- The default m/z range (101–500 m/z) may exclude relevant peaks in non-proteomics applications and should be reconfigured accordingly

## Evidence

- [readme] Binning and feature hashing method: "High-resolution MS/MS spectra are converted to low-dimensional vectors using feature hashing. First, spectra are converted to sparse vectors using small mass bins to tightly capture their fragment"
- [readme] Hashing algorithm and similarity preservation: "the sparse, high-dimensional, vectors are hashed to lower-dimensional vectors by using a hash function (the non-cryptographic MurmurHash3 algorithm) to map the mass bins separately to a small number"
- [intro] Workflow step in falcon pipeline: "First, high-resolution spectra are binned and converted to low-dimensional vectors using feature hashing."
- [readme] Input file formats supported: "_falcon_ takes peak files (in the mzML, mzXML, or MGF format) as input and exports the clustering result"
- [readme] Low_dim parameter tuning: "`low_dim`: The length of the low-dimensional vectors used for nearest neighbor searching. Larger vectors will more accurately approximate the true cosine distance, at the expense of longer nearest"
- [readme] Preprocessing defaults and adjustments: "The default settings are intended for clustering bottom-up proteomics data. When analyzing metabolomics or top-down data, these settings likely need to be adjusted accordingly."
