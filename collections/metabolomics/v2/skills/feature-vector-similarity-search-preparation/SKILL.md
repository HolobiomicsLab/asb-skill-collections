---
name: feature-vector-similarity-search-preparation
description: Use when you have millions of MS/MS spectra in mzML, mzXML, or MGF format and need to identify similar spectra for clustering, but exhaustive pairwise cosine-similarity computation would be prohibitively slow.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
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

# feature-vector-similarity-search-preparation

## Summary

Convert high-resolution MS/MS spectra to low-dimensional hashed vectors and construct nearest neighbor indexes to enable efficient similarity searching without exhaustive pairwise comparisons. This skill bridges spectrum preprocessing and fast clustering by creating the index structures that make large-scale spectrum analysis computationally feasible.

## When to use

Apply this skill when you have millions of MS/MS spectra in mzML, mzXML, or MGF format and need to identify similar spectra for clustering, but exhaustive pairwise cosine-similarity computation would be prohibitively slow. Use it as the intermediate step between spectrum preprocessing (binning, scaling) and density-based clustering.

## When NOT to use

- Spectra are already represented as precomputed feature vectors or distance matrices—skip directly to clustering.
- The dataset contains fewer than ~10,000 spectra—exhaustive pairwise comparison may be faster than index construction overhead.
- Spectrum format is not mzML, mzXML, or MGF; conversion to these formats is required first.
- You require exact (not approximate) cosine similarities; feature hashing introduces approximation error that depends on `low_dim` setting.

## Inputs

- High-resolution MS/MS spectra (mzML, mzXML, or MGF format)
- Precursor m/z values for each spectrum
- Preprocessed spectrum intensities (scaled if applicable)

## Outputs

- Low-dimensional hashed spectrum vectors (length controlled by `low_dim` parameter)
- Serialized nearest neighbor index structures (one per precursor m/z bucket)
- Inverted index mappings for fast neighbor retrieval

## How to apply

First, bin high-resolution spectra into sparse vectors capturing fragment mass bins, then apply feature hashing (MurmurHash3) to compress these sparse, high-dimensional vectors into low-dimensional approximations that preserve cosine similarity. Partition hashed vectors into buckets stratified by precursor m/z to create separate nearest neighbor indexes for each bucket, using Voronoi partitioning to assign vectors to nearest representatives in an inverted index structure. Tune the `low_dim` parameter (length of hashed vectors) to balance approximation accuracy against memory and search speed; larger values more accurately preserve cosine distance but increase computational cost. Tune `n_neighbors` and `n_neighbors_ann` (final and ANN-search neighbor counts) to balance clustering completeness against search time. The resulting indexes enable sparse pairwise distance matrix computation by querying only promising neighbors rather than all spectra.

## Related tools

- **falcon** (Command-line spectrum clustering tool that orchestrates feature hashing, nearest neighbor indexing, and density-based clustering; implements the full workflow from raw spectra to cluster assignments.) — https://github.com/bittremieux/falcon
- **spectrum-utils** (Python library for spectrum preprocessing (binning, scaling, filtering) prior to hashing and indexing.)

## Examples

```
falcon peak/*.mzml falcon --export_representatives --precursor_tol 20 ppm --fragment_tol 0.05 --eps 0.10
```

## Evaluation signals

- Index construction completes without memory errors and produces serialized index files for each precursor m/z bucket.
- Hashed vectors preserve relative cosine similarity: cosine(hashed_spec_A, hashed_spec_B) ≈ cosine(original_spec_A, original_spec_B) with error bounded by `low_dim` choice.
- Nearest neighbor queries retrieve true nearest neighbors within the setting of `n_probe` (number of inverted index lists inspected); verify by spot-checking against brute-force k-NN on a subset.
- Downstream density-based clustering (DBSCAN with `eps` threshold) produces clusters with >90% purity (clusters contain spectra from single peptide/compound) and >80% sensitivity (true co-fragmenting spectra are grouped together).
- Wall-clock time for clustering millions of spectra is at least 5–10× faster than would be required for exhaustive pairwise cosine computation.

## Limitations

- Feature hashing introduces approximation error in cosine similarity; the magnitude depends on `low_dim`: smaller dimensions are faster but less accurate. Values that work well for one dataset's spectral characteristics may require tuning for metabolomics vs. proteomics data.
- Inverted index tuning via `n_probe` trades accuracy for speed; exploring fewer index lists during neighbor retrieval increases the risk of missing true nearest neighbors in high-dimensional space, potentially leading to fragmented clusters.
- Index construction must stratify by precursor m/z to avoid comparing spectra with incompatible precursor masses; results are sensitive to `precursor_tol` setting (default 20 ppm or Dalton).
- The method assumes spectra have been preprocessed to remove low-quality peaks (e.g., `min_peaks` ≥5, `min_mz_range` ≥250 m/z); raw, unfiltered spectra can produce poor index quality.

## Evidence

- [readme] High-resolution spectra binned and converted to low-dimensional vectors using feature hashing: "First, high-resolution spectra are binned and converted to low-dimensional vectors using feature hashing."
- [readme] Spectrum vectors construct nearest neighbor indexes for fast similarity searching: "Next, the spectrum vectors are used to construct nearest neighbor indexes for fast similarity searching."
- [readme] Nearest neighbor indexes enable sparse pairwise distance matrix without exhaustive comparisons: "The nearest neighbor indexes are used to efficiently compute a sparse pairwise distance matrix without having to exhaustively compare all spectra to each other."
- [readme] Feature hashing uses MurmurHash3 and Voronoi partitioning in inverted index: "the sparse, high-dimensional, vectors are hashed to lower-dimensional vectors by using a hash function (the non-cryptographic MurmurHash3 algorithm) to map the mass bins separately to a small number"
- [readme] Precursor m/z buckets and tunable neighbor parameters control index accuracy/speed tradeoff: "The spectrum vectors in each bucket are partitioned into data subspaces to create a Voronoi diagram, and all vectors are assigned to their nearest representative vector in an inverted index. The"
- [readme] n_probe, n_neighbors, and low_dim are tunable parameters for nearest neighbor indexing: "n_probe: The maximum number of lists in the inverted index to inspect during querying. Inspecting fewer lists will run faster but will give slightly less accurate clustering results. n_neighbors and"
