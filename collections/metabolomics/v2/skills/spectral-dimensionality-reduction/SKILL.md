---
name: spectral-dimensionality-reduction
description: Use when you have high-resolution tandem MS spectra (in mzML, mzXML, or MGF format) that need to be clustered or searched at scale (millions of spectra).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - falcon
  - spectrum-utils
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
---

# spectral-dimensionality-reduction

## Summary

Transform high-resolution MS/MS spectra into fixed-size, low-dimensional vector representations using feature hashing, enabling efficient nearest-neighbor indexing and similarity searching at scale. This transformation preserves cosine similarity while reducing memory footprint and computational cost.

## When to use

Apply this skill when you have high-resolution tandem MS spectra (in mzML, mzXML, or MGF format) that need to be clustered or searched at scale (millions of spectra). Use it specifically when you need to construct nearest-neighbor indexes for fast similarity searching without exhaustive pairwise comparisons, or when memory and speed constraints prohibit direct cosine-distance computation on full spectra.

## When NOT to use

- Spectra are already represented as low-dimensional feature vectors or embeddings from another method.
- You require exact cosine distances and cannot tolerate the approximation error introduced by hashing.
- Input spectra have very few peaks (< 5) or narrow m/z ranges (< 250 m/z), where binning loses discriminative power; in metabolomics or minimal-peak contexts, reconsider preprocessing thresholds rather than skipping this step.

## Inputs

- High-resolution MS/MS spectra in mzML, mzXML, or MGF format
- Spectrum metadata (precursor m/z, retention time, intensity values)
- Optional: intensity scaling parameters (sqrt, log, rank, or none)

## Outputs

- Fixed-size low-dimensional hashed feature vectors (dense or sparse matrix)
- Vector-to-spectrum mapping (index correspondence)
- Cosine similarity matrix or distance estimates for downstream indexing

## How to apply

First, bin high-resolution spectra across the m/z range using small mass bins to capture fragment masses as sparse vectors. Next, apply feature hashing (using the non-cryptographic MurmurHash3 algorithm) to map the mass bins to a smaller number of hash bins, producing fixed-size low-dimensional vectors. Choose the `low_dim` parameter (length of hashed vectors) based on your accuracy-speed trade-off: larger vectors more accurately approximate true cosine distance but increase memory and searching time. The hashing process conserves cosine similarity between the original spectra, allowing the low-dimensional vectors to serve as proxies for similarity searching. Normalize intensities and optionally apply scaling (square root, logarithm, or rank) before hashing, as this can improve clustering quality. Output the resulting hashed feature matrix in a dense or sparse numerical format (NumPy array or SciPy sparse matrix).

## Related tools

- **falcon** (Primary tool; implements feature hashing and nearest-neighbor indexing for spectrum clustering. Accepts mzML/mzXML/MGF input and outputs hashed vectors and cluster assignments.) — https://github.com/bittremieux/falcon
- **spectrum-utils** (Utility library (v0.3.5) used by falcon for spectrum binning, normalization, and preprocessing operations prior to feature hashing.)

## Examples

```
falcon peak/*.mzml falcon --export_representatives --precursor_tol 20 ppm --fragment_tol 0.05 --eps 0.10
```

## Evaluation signals

- Output vectors have the expected fixed dimensionality (controlled by `low_dim` parameter); verify vector shape matches `(n_spectra, low_dim)`.
- Cosine similarity between pairs of hashed vectors approximates the cosine similarity of the original binned spectra; spot-check 10–20 pairs to confirm correlation ≥ 0.95.
- Sparse matrix density is reasonable for the spectral complexity; too-dense output suggests hashing collisions or overly aggressive binning.
- Downstream nearest-neighbor index construction completes without memory errors and retrieves expected neighbors (i.e., spectra with high cosine similarity are retrieved as nearest neighbors).
- Cluster purity and fragmentation metrics (e.g., number of single-spectrum clusters, cluster size distribution) align with literature expectations for the same `eps` threshold and data type (proteomics vs. metabolomics).

## Limitations

- Feature hashing introduces approximation error; the fidelity of the low-dimensional approximation depends on `low_dim` — smaller values are faster and use less memory but lose fine-grained spectral detail.
- Hash collisions can occur when multiple mass bins map to the same hash bin, degrading similarity preservation; mitigate by increasing `low_dim` or the number of hash bins.
- Performance and clustering purity are sensitive to preprocessing parameters (`min_peaks`, `min_mz_range`, `scaling`); these must be tuned for the spectral type (proteomics vs. metabolomics vs. top-down data).
- The method assumes spectra are comparable in quality and intensity range; highly variable instrument conditions or very low-intensity spectra may require normalization or filtering before hashing.
- Binning and hashing discard exact peak positions; if downstream analyses require m/z-level precision, retain the original spectra alongside the hashed vectors.

## Evidence

- [intro] High-resolution spectra are binned and converted to low-dimensional vectors using feature hashing: "First, high-resolution spectra are binned and converted to low-dimensional vectors using feature hashing."
- [readme] Spectra are converted to sparse vectors using small mass bins, then hashed using MurmurHash3: "First, spectra are converted to sparse vectors using small mass bins to tightly capture their fragment masses. Next, the sparse, high-dimensional, vectors are hashed to lower-dimensional vectors by"
- [readme] Feature hashing conserves cosine similarity between hashed vectors: "This feature hashing conserves the cosine similarity between hashed vectors and can be used to approximate the similarity between the original spectra."
- [readme] low_dim parameter controls vector size and accuracy-speed tradeoff: "low_dim: The length of the low-dimensional vectors used for nearest neighbor searching. Larger vectors will more accurately approximate the true cosine distance, at the expense of longer nearest"
- [readme] Scaling can improve clustering quality and affects cosine threshold: "scaling: Scale the peak intensities by their square root, logarithm, rank, or no scaling. Default is no scaling, with square root scaling often giving good results as well. Note that the scaling"
- [methods] Input formats and output types for binning and hashing: "Load high-resolution MS/MS spectra in mzML or mzXML format. 2. Bin spectra across the m/z range and normalize intensities. 3. Apply feature hashing to convert binned spectra into fixed-size"
