---
name: spectrum-vector-serialization
description: Use when after successfully constructing a nearest neighbor index from hashed spectrum feature vectors and before performing density-based clustering or similarity searches.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0335
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

# Serialize and Persist Nearest Neighbor Index to File

## Summary

This skill persists constructed nearest neighbor indexes built from low-dimensional spectrum vectors to disk in a format optimized for fast retrieval and subsequent similarity search operations. It is essential for enabling reusable, efficient clustering workflows where indexes do not need to be reconstructed for each analysis run.

## When to use

Apply this skill after successfully constructing a nearest neighbor index from hashed spectrum feature vectors and before performing density-based clustering or similarity searches. Use it when you need to store indexes for large-scale MS/MS datasets (millions of spectra) to avoid costly recomputation across multiple clustering runs or when sharing preprocessed data across analysis pipelines.

## When NOT to use

- Index has not yet been constructed from spectrum vectors; first build the index, then serialize.
- Spectrum dataset is very small (<10,000 spectra); recomputing the index on-the-fly may be faster than I/O overhead.
- Index will only be used once in a single session; persistence is unnecessary overhead.

## Inputs

- Constructed nearest neighbor index object (from spectrum vectors)
- Low-dimensional spectrum feature vectors (hashed, dimensionality typically 10–1000)
- Index metadata (algorithm type, parameters: n_neighbors, n_probe, precursor_tol, fragment_tol)

## Outputs

- Serialized index file (binary or text format optimized for I/O)
- Index metadata file (JSON or INI config with parameters and version info)
- Optional: manifest or checksum file for integrity verification

## How to apply

After building nearest neighbor indexes from low-dimensional spectrum vectors (produced by feature hashing of binned spectra), serialize the index object to a persistent file format suitable for rapid deserialization and lookup. The choice of format and storage location should prioritize fast I/O performance, since the index will be queried repeatedly during similarity searching. The serialized index must preserve the exact structure and parameters (e.g., n_neighbors, n_probe settings, hash dimensionality) so that subsequent nearest neighbor queries return identical results. Verify that the persisted index can be successfully loaded and queried without recomputation, and confirm that file size is reasonable relative to the input spectrum count and vector dimensionality.

## Related tools

- **falcon** (Performs nearest neighbor index construction and handles serialization as part of the spectrum clustering pipeline) — https://github.com/bittremieux/falcon
- **spectrum-utils** (Provides spectrum I/O and preprocessing utilities; used alongside falcon for spectral data handling)

## Evaluation signals

- Serialized index file exists at the specified output path with non-zero file size appropriate for the spectrum count and vector dimensionality.
- Index can be deserialized and loaded into memory without errors.
- Nearest neighbor queries on the loaded index return identical results to queries on the in-memory index before serialization.
- Index metadata (parameters like n_neighbors, n_probe, vector dimensionality, precursor_tol, fragment_tol) are preserved and retrievable from the persisted file.
- File integrity can be verified via checksum or manifest if available; confirm reproducibility across platforms/machines.

## Limitations

- Serialization format and backward compatibility are tool-specific; falcon may not maintain compatibility across major version upgrades.
- Storage requirements scale with spectrum dataset size and vector dimensionality; very large indexes (>10 GB) may require specialized filesystems or cloud storage.
- Serialized indexes are optimized for specific nearest neighbor algorithm and parameters (n_probe, n_neighbors); changing these parameters after serialization requires index recomputation.
- Index does not store the original raw MS/MS spectra, only the hashed vector representations; original spectrum files must be retained separately for downstream analysis.

## Evidence

- [other] Build nearest neighbor indexes using the vector input, selecting an appropriate nearest neighbor algorithm and index structure. 3. Serialize and persist the index to a file format suitable for fast retrieval and similarity search operations.: "Serialize and persist the index to a file format suitable for fast retrieval and similarity search operations."
- [readme] the spectrum vectors are used to construct nearest neighbor indexes for fast similarity searching: "the spectrum vectors are used to construct nearest neighbor indexes for fast similarity searching"
- [readme] The nearest neighbor indexes are used to efficiently compute a sparse pairwise distance matrix without having to exhaustively compare all spectra to each other.: "The nearest neighbor indexes are used to efficiently compute a sparse pairwise distance matrix without having to exhaustively compare all spectra to each other."
- [other] Spectrum vectors are used to construct nearest neighbor indexes that enable efficient computation of sparse pairwise distance matrices without exhaustively comparing all spectra to each other.: "Spectrum vectors are used to construct nearest neighbor indexes that enable efficient computation of sparse pairwise distance matrices"
- [readme] high-resolution spectra are binned and converted to low-dimensional vectors using feature hashing: "high-resolution spectra are binned and converted to low-dimensional vectors using feature hashing"
