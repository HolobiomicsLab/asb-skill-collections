---
name: sparse-vs-dense-vector-format-selection
description: Use when when converting high-resolution tandem mass spectra to vectors for clustering or similarity searching, you must decide whether to output sparse or dense vectors. Use this decision point after binning spectra into mass bins but before constructing nearest-neighbor indexes.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3645
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
  - build: coll_falcon_cq
    doi: 10.1002/rcm.9153
    title: falcon
  dedup_kept_from: coll_falcon_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1002/rcm.9153
  all_source_dois:
  - 10.1002/rcm.9153
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# sparse-vs-dense-vector-format-selection

## Summary

Choose between sparse and dense vector representations when converting binned MS/MS spectra to low-dimensional feature-hashed vectors. Dense vectors are compact and enable fast nearest-neighbor searching; sparse vectors preserve high-dimensional detail but require more memory and slower comparison.

## When to use

When converting high-resolution tandem mass spectra to vectors for clustering or similarity searching, you must decide whether to output sparse or dense vectors. Use this decision point after binning spectra into mass bins but before constructing nearest-neighbor indexes. The choice affects memory consumption, query speed, and the fidelity of cosine similarity approximation in downstream nearest-neighbor searching.

## When NOT to use

- Input spectra have not yet been binned—perform binning to small mass bins before deciding on vector format.
- You require exact peak m/z positions in downstream analysis—sparse vectors may be needed instead of dense hashed vectors.
- The number of spectra is small (<1000) and memory is not a constraint—the overhead of format selection is negligible and clustering accuracy dominates.

## Inputs

- High-resolution MS/MS spectra (mzML, mzXML, or MGF format)
- Binned spectrum representation (sparse vectors with mass bin indices and intensities)

## Outputs

- Dense low-dimensional hashed spectrum vectors (fixed-size arrays)
- Sparse low-dimensional hashed spectrum vectors (sparse matrix or coordinate list format)

## How to apply

After binning high-resolution spectra into small mass bins to capture fragment masses, apply feature hashing using a hash function (such as MurmurHash3) to map mass bins to a fixed number of hash bins, producing either dense or sparse vectors. Dense vectors are preferred for nearest-neighbor indexing when memory and query speed are critical, since they allow compact storage and fast dot-product computation; sparse vectors preserve the original sparsity of the binned spectra but require sparse matrix operations and more storage. Select dense format when constructing inverted indexes for querying; select sparse when memory is unconstrained and you need to preserve explicit bin positions for downstream interpretation. The hashing process itself conserves cosine similarity between vectors, so the format choice primarily impacts computational efficiency rather than clustering accuracy.

## Related tools

- **falcon** (Spectrum clustering tool that applies feature hashing to convert binned spectra into low-dimensional vectors (dense or sparse) for nearest-neighbor indexing) — https://github.com/bittremieux/falcon
- **spectrum-utils** (Utility library for loading and preprocessing raw high-resolution MS/MS spectra prior to binning and hashing)

## Examples

```
falcon peak/*.mzml falcon --export_representatives --precursor_tol 20 ppm --fragment_tol 0.05 --eps 0.10
```

## Evaluation signals

- Dense vectors have fixed dimensionality (controlled by the `low_dim` parameter) and uniform memory footprint across all spectra.
- Sparse vectors preserve the non-zero mass bins from the original binned spectra and have variable density depending on peak count.
- Cosine similarity between hashed vectors (dense or sparse) approximates the true cosine distance between original spectra; verify by comparing hashed similarities to reference un-hashed similarities on a held-out test set.
- Nearest-neighbor query latency and memory consumption differ: dense vectors typically support faster queries on CPUs or GPUs; sparse vectors reduce memory footprint when peak density is low.
- Cluster purity (fraction of spectra in each cluster corresponding to a single peptide) should be comparable between sparse and dense choices for the same `eps` parameter, since both preserve cosine similarity.

## Limitations

- Dense vectors approximate the true cosine distance between original high-resolution spectra; the approximation error depends on the `low_dim` parameter (longer vectors are more accurate but require more memory and slower nearest-neighbor searching).
- Sparse vectors require specialized matrix libraries and operations, increasing code complexity compared to dense arrays.
- The choice of hash function (MurmurHash3 in falcon) and hash bin count are fixed at pipeline configuration; tuning these hyperparameters requires re-running the binning and hashing steps.
- Feature hashing is not invertible: the original mass bin positions cannot be exactly recovered from hashed vectors, limiting post-hoc spectral interpretation.

## Evidence

- [intro] High-resolution spectra are binned and converted to low-dimensional vectors using feature hashing as the first step: "First, high-resolution spectra are binned and converted to low-dimensional vectors using feature hashing."
- [readme] Sparse vectors use small mass bins; dense vectors are hashed using MurmurHash3 algorithm: "First, spectra are converted to sparse vectors using small mass bins to tightly capture their fragment masses. Next, the sparse, high-dimensional, vectors are hashed to lower-dimensional vectors by"
- [readme] Feature hashing conserves cosine similarity between hashed vectors: "This feature hashing conserves the cosine similarity between hashed vectors and can be used to approximate the similarity between the original spectra."
- [readme] Low-dimensional vector length is tunable and affects nearest-neighbor accuracy and speed: "Larger vectors will more accurately approximate the true cosine distance, at the expense of longer nearest neighbor searching and memory requirements."
- [intro] Dense and sparse vectors are used in nearest-neighbor indexing: "Next, the spectrum vectors are used to construct nearest neighbor indexes for fast similarity searching."
