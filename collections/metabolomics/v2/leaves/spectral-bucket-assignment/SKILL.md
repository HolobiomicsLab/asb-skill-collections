---
name: spectral-bucket-assignment
description: Use when you have a collection of mass spectrometry spectral data (m/z
  and intensity pairs) that must be indexed for fast neighbor retrieval or similarity
  search, and you need to trade some precision in similarity matching for substantial
  gains in query speed and memory efficiency across large.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - mzBucket
  - pyproteolizard-algorithm
  - pyproteolizard-data
  techniques:
  - mass-spectrometry
  license_tier: open
derived_from:
- doi: 10.1186/s12859-022-04833-5
  title: mzBucket
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mzbucket_cq
    doi: 10.1186/s12859-022-04833-5
    title: mzBucket
  dedup_kept_from: coll_mzbucket_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s12859-022-04833-5
  all_source_dois:
  - 10.1186/s12859-022-04833-5
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-bucket-assignment

## Summary

Assigns mass spectrometry spectra to indexed buckets using locality-sensitive hashing (LSH), enabling efficient retrieval and similarity search across large spectral databases. This skill transforms vectorized spectra into discrete bucket assignments that preserve local similarity structure.

## When to use

Apply this skill when you have a collection of mass spectrometry spectral data (m/z and intensity pairs) that must be indexed for fast neighbor retrieval or similarity search, and you need to trade some precision in similarity matching for substantial gains in query speed and memory efficiency across large repositories.

## When NOT to use

- Spectra have not been normalized or vectorized into a fixed-dimensional representation suitable for hashing
- Query speed is not a concern and exact nearest-neighbor matching is required (LSH introduces a trade-off favoring speed over precision)
- The spectral dataset is very small (< 10,000 spectra) where linear search or simpler indexing methods are more practical than LSH overhead

## Inputs

- mass spectrometry spectral data (m/z and intensity pairs)
- vectorized spectrum representations (binary or real-valued feature vectors)
- LSH parameters (number of hash tables, hash functions per table, bucket width)

## Outputs

- LSH index with bucket assignments
- spectrum-to-bucket mappings
- serialized model file containing hash function parameters and all bucket assignments

## How to apply

First, normalize or vectorize each mass spectrometry spectrum into a feature representation (e.g., binary or real-valued vector) suitable for LSH. Initialize LSH hash functions with parameters governing the number of hash tables, hash functions per table, and bucket width—these control the balance between collision probability (sensitivity) and index granularity. Compute hash values for each spectrum across all hash tables and hash functions to determine its bucket assignments. Assign each spectrum to the corresponding buckets in the LSH index structure, creating a mapping from spectrum identifiers to bucket locations. Finally, serialize the complete LSH index—including hash function parameters, bucket assignments, and spectrum-to-bucket mappings—to a model file for later retrieval and query operations.

## Related tools

- **mzBucket** (Implements locality-sensitive hashing for organizing and indexing mass spectrometry spectral data into buckets) — https://github.com/hildebrandtlab/mzBucket
- **pyproteolizard-algorithm** (Provides the LSH algorithm implementation used by mzBucket for spectral bucket assignment) — https://github.com/theGreatHerrLebert/proteolizard-algorithm
- **pyproteolizard-data** (Provides data-access layer for reading and normalizing mass spectrometry spectral data) — https://github.com/theGreatHerrLebert/proteolizard-data

## Evaluation signals

- Verify that every spectrum in the input dataset has been assigned to at least one bucket across the LSH hash tables
- Check that the serialized model file contains valid hash function parameters (bucket width, number of hash tables, number of hash functions per table) that are consistent with the assignment process
- Validate that the spectrum-to-bucket mapping is deterministic: re-hashing the same spectrum with the same LSH parameters produces identical bucket assignments
- Confirm that bucket occupancy follows expected sparsity patterns for the chosen LSH parameters (uniformly low occupancy indicates appropriate parameter tuning)
- Test retrieval: query a known spectrum and verify it is found in at least one of its assigned buckets, and that nearby neighbors in the full feature space appear in overlapping buckets

## Limitations

- LSH trades precision for speed: not all true nearest neighbors may be retrieved, especially if LSH parameters (bucket width, number of hash tables) are not tuned appropriately for the spectral data distribution
- The quality of bucket assignments depends critically on the choice of vectorization method for spectra; poor normalization or feature representation will degrade both recall and precision
- The mzBucket implementation has been deprecated in favor of the proteolizard framework components (pyproteolizard-data and pyproteolizard-algorithm); the original repository should not be used for new analyses

## Evidence

- [other] how_to_apply step 1–6: "1. Load mass spectrometry spectral data (m/z and intensity pairs). 2. Normalize or vectorize each spectrum into a representation suitable for LSH (e.g., binary or real-valued feature vector). 3."
- [readme] summary and skill purpose: "Locality-sensitive hashing for mass spectrometry data."
- [readme] tool and framework migration: "The implementation has been updated and shifted to the proteolizard framework, more precisely the components pyproteolizard-data for data-access and pyproteolizard-algorithm for the LSH."
- [intro] core finding on LSH mechanism: "mzBucket implements locality-sensitive hashing as a mechanism for organizing mass spectrometry data."
