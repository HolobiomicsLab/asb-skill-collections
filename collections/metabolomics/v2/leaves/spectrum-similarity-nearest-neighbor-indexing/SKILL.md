---
name: spectrum-similarity-nearest-neighbor-indexing
description: Use when when you have thousands to millions of high-resolution tandem
  MS/MS spectra (in mzML, mzXML, or MGF format) that need to be clustered or compared,
  and exhaustive pairwise distance computation is computationally prohibitive.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - falcon
  - spectrum-utils==0.3.5
  - spectrum-utils
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1002/rcm.9153
  title: falcon
evidence_spans:
- The _falcon_ spectrum clustering tool uses advanced algorithmic techniques for highly
  efficient processing of millions of MS/MS spectra.
- pip install falcon-ms spectrum-utils==0.3.5
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

# spectrum-similarity-nearest-neighbor-indexing

## Summary

Construct nearest neighbor indexes on low-dimensional spectrum vectors to enable fast, sparse pairwise similarity searching without exhaustive comparisons. This skill accelerates large-scale MS/MS spectrum clustering by trading full pairwise distance computation for efficient approximate nearest neighbor retrieval.

## When to use

When you have thousands to millions of high-resolution tandem MS/MS spectra (in mzML, mzXML, or MGF format) that need to be clustered or compared, and exhaustive pairwise distance computation is computationally prohibitive. Particularly useful for bottom-up proteomics datasets where you want to group spectra with similar precursor mass and fragment patterns.

## When NOT to use

- When you require exhaustive all-against-all spectrum comparisons for validation or when downstream analysis depends on complete pairwise distance information.
- For small datasets (< ~1000 spectra) where brute-force pairwise comparison is already fast enough.
- When input spectra are already aggregated or pre-clustered; the skill assumes individual spectrum records as input.

## Inputs

- peak files in mzML, mzXML, or MGF format containing tandem MS/MS spectra
- precursor mass tolerance (ppm or Dalton)
- fragment mass tolerance (Dalton)
- spectrum preprocessing parameters (min_peaks, min_mz_range, min_mz, max_mz, scaling method)

## Outputs

- sparse pairwise distance matrix (cosine similarities between neighboring spectra pairs)
- nearest neighbor index structures (inverted index partitioned by precursor m/z bucket)
- input data for downstream density-based clustering

## How to apply

First, convert high-resolution spectra to low-dimensional vectors using feature hashing (binning spectra into sparse high-dimensional vectors, then hashing via MurmurHash3 to a smaller number of hash bins). Next, partition spectrum vectors into buckets by precursor m/z and construct a Voronoi diagram–based inverted index within each bucket, assigning vectors to nearest representative vectors. During querying, retrieve similarities to neighboring spectra by inspecting a configurable number of inverted index lists (n_probe parameter). This produces a sparse pairwise distance matrix that preserves cosine similarity between original spectra while dramatically reducing the number of comparisons. Tune n_probe, n_neighbors, and low_dim parameters to balance clustering speed versus accuracy; default settings are suitable for most proteomics datasets.

## Related tools

- **falcon** (command-line tool that implements spectrum vector hashing, nearest neighbor indexing, and sparse distance matrix computation via its core clustering pipeline) — https://github.com/bittremieux/falcon
- **spectrum-utils** (utility library for spectrum preprocessing, binning, and normalization prior to hashing and indexing)

## Examples

```
falcon peak/*.mzml falcon --export_representatives --precursor_tol 20 ppm --fragment_tol 0.05 --eps 0.10
```

## Evaluation signals

- The sparse pairwise distance matrix is non-empty and contains only valid cosine similarity values (0.0 to 1.0 or distance equivalents) for neighbor pairs.
- The number of pairwise comparisons in the sparse matrix is substantially smaller than the theoretical maximum (N choose 2), confirming sparsity.
- Downstream density-based clustering (DBSCAN) on the sparse distance matrix produces clusters with sensible cluster purity and spectrum groupings matching known peptide standards or repeated injections.
- Nearest neighbor search time scales sub-linearly with dataset size, demonstrating efficiency gains over brute-force comparison.
- Cosine similarity values between indexed neighbor pairs closely approximate the true cosine similarities computed on the original (unhashed) spectrum vectors, confirming fidelity of the feature hashing step.

## Limitations

- The feature hashing step reduces spectral information from high-dimensional binned vectors to low_dim hash bins (default or user-specified); collision and information loss increase if low_dim is too small, reducing clustering accuracy.
- The n_probe parameter (number of inverted index lists inspected) directly trades clustering accuracy for speed; inspecting fewer lists may miss true nearest neighbors in high-dimensional space.
- Precursor m/z bucketing assumes spectra with similar precursor masses are more likely to be similar; spectra with the same peptide sequence but different charge states or post-translational modifications may be assigned to different buckets.
- The method assumes input spectra have undergone appropriate preprocessing (e.g., removal of low-intensity noise, normalization). Badly preprocessed spectra will produce poor indexing and weak neighbor relationships.
- Performance and clustering quality are sensitive to the eps parameter (maximum cosine distance for neighbors); values between 0.05 and 0.15 are recommended for pure clustering, but optimal values depend on spectral preprocessing choices and data type (bottom-up proteomics, metabolomics, top-down require different tuning).

## Evidence

- [intro] The nearest neighbor indexes are used to efficiently compute a sparse pairwise distance matrix without having to exhaustively compare all spectra to each other.: "The nearest neighbor indexes are used to efficiently compute a sparse pairwise distance matrix without having to exhaustively compare all spectra to each other."
- [intro] High-resolution spectra are binned and converted to low-dimensional vectors using feature hashing.: "First, high-resolution spectra are binned and converted to low-dimensional vectors using feature hashing."
- [intro] Next, the spectrum vectors are used to construct nearest neighbor indexes for fast similarity searching.: "Next, the spectrum vectors are used to construct nearest neighbor indexes for fast similarity searching."
- [readme] falcon takes peak files (in the mzML, mzXML, or MGF format) as input and exports the clustering result as a comma-separated file with each MS/MS spectrum and its cluster label on a single line.: "falcon takes peak files (in the mzML, mzXML, or MGF format) as input and exports the clustering result as a comma-separated file"
- [readme] Vectors are split into buckets based on the precursor m/z of the corresponding spectra to construct nearest neighbor indexes for highly efficient spectrum comparison.: "Vectors are split into buckets based on the precursor m/z of the corresponding spectra to construct nearest neighbor indexes"
- [readme] The accuracy and speed of similarity searching is governed by the number of neighboring cells to explore during searching: exploring more cells during searching decreases the chance of missing a nearest neighbor in the high-dimensional space, at the expense of a longer searching time.: "The accuracy and speed of similarity searching is governed by the number of neighboring cells to explore during searching"
- [readme] n_probe: The maximum number of lists in the inverted index to inspect during querying. Inspecting fewer lists will run faster but will give slightly less accurate clustering results.: "n_probe: The maximum number of lists in the inverted index to inspect during querying. Inspecting fewer lists will run faster but will give slightly less accurate clustering results."
- [readme] low_dim: The length of the low-dimensional vectors used for nearest neighbor searching. Larger vectors will more accurately approximate the true cosine distance, at the expense of longer nearest neighbor searching and memory requirements.: "low_dim: The length of the low-dimensional vectors used for nearest neighbor searching. Larger vectors will more accurately approximate the true cosine distance"
