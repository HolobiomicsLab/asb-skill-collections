---
name: python-sqlite-migration-and-etl
description: Use when you have MS/MS spectral library data currently stored in multiple file formats (JSON, CSV, or binary) and need to enable fast, filtered queries by metadata (e.g., precursor m/z, retention time, molecular class) without loading entire libraries into memory.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - MS2Query
  - Python
  - GitHub
  - Python sqlite3 module
  - pytest
derived_from:
- doi: 10.1038/s41467-023-37446-4
  title: ms2query
evidence_spans:
- you want to make some kind of change to the code base
- MS2Query - Reliable and fast MS/MS spectral-based analogue search
- make sure the existing tests still work by running ``python setup.py test``
- fork the repository to your own Github profile and create your own feature branch off of the latest master commit
- use the search functionality [here](https://github.com/iomega/ms2query/issues)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2query_cq
    doi: 10.1038/s41467-023-37446-4
    title: ms2query
  dedup_kept_from: coll_ms2query_cq
schema_version: 0.2.0
---

# Python SQLite Migration and ETL

## Summary

Design and implement Python-based ETL pipelines to migrate spectral library data from file-based formats (JSON, CSV, binary) into normalized SQLite schemas with foreign key relationships, enabling efficient querying and metadata filtering. This skill is essential when scaling from file-based storage to database-backed library access patterns.

## When to use

Apply this skill when you have MS/MS spectral library data currently stored in multiple file formats (JSON, CSV, or binary) and need to enable fast, filtered queries by metadata (e.g., precursor m/z, retention time, molecular class) without loading entire libraries into memory. Specifically useful in MS2Query workflows where pre-computed embeddings and library spectra must support rapid similarity re-ranking on subsets of 2000+ candidate spectra.

## When NOT to use

- Input is a single, small spectral file (<10k spectra) that fits comfortably in memory — file-based access or in-memory data structures may be simpler.
- Query patterns are ad-hoc and non-repetitive — the overhead of schema design and migration may not justify the benefit.
- Spectral data lacks consistent metadata annotations (SMILES, InChIKey) — database normalization requires structured, reliable metadata to enforce foreign key constraints.

## Inputs

- MS/MS spectral library files in JSON, CSV, or binary formats
- Library metadata annotations (precursor m/z, retention time, SMILES, InChI, InChIKey)
- Peak list data (m/z–intensity pairs per spectrum)
- Pre-computed MS2Deepscore embeddings (optional, for re-ranking)
- Existing unit test suite and expected query result sets

## Outputs

- SQLite database file (.db) with normalized schema (spectra, metadata, peaks tables)
- Python query interface module with SELECT/JOIN functions and similarity scoring
- Unit test results confirming backward compatibility and performance thresholds
- Migration and connection documentation with example code snippets
- CHANGELOG.md entry summarizing database feature addition

## How to apply

First, design a normalized SQLite schema with separate tables for spectral metadata (precursor m/z, retention time, molecular structure annotations) and peak data (m/z–intensity pairs), linked by foreign keys to library spectrum IDs. Second, write Python data-migration code using the sqlite3 module to parse existing library formats and bulk-insert records into the schema. Third, implement query functions using SELECT and JOIN operations to retrieve spectra filtered by metadata criteria and compute similarity scores (e.g., cosine or MS2Deepscore) against query spectra. Fourth, validate backward compatibility by running the existing test suite (`python setup.py test`) to confirm query results match the original file-based access patterns. Fifth, add unit tests for database insertion correctness, schema constraint validation, and query performance thresholds (e.g., sub-second retrieval for top-K matches). Finally, measure query latency and memory usage before and after migration to confirm efficiency gains.

## Related tools

- **MS2Query** (Spectral library matching tool that benefits from SQLite-backed library storage for fast re-ranking of top-K candidate spectra using MS2Deepscore embeddings and random forest scoring) — https://github.com/iomega/ms2query
- **Python sqlite3 module** (Core database connectivity and schema definition for creating normalized tables, enforcing constraints, and executing parameterized queries)
- **pytest** (Test framework for unit and integration tests validating database insertion, schema correctness, and query performance thresholds)
- **GitHub** (Version control and CI/CD platform for feature branch management, pull request review, and continuous integration testing (CI_build.yml)) — https://github.com/iomega/ms2query

## Examples

```
from ms2query.ms2library import create_library_object_from_one_dir; import sqlite3; conn = sqlite3.connect('ms2query_library.db'); cursor = conn.cursor(); cursor.execute('SELECT spectrum_id, precursor_mz FROM spectra WHERE precursor_mz BETWEEN ? AND ?', (500.0, 600.0)); results = cursor.fetchall()
```

## Evaluation signals

- All existing tests pass (`python setup.py test`), confirming backward compatibility between file-based and database query results.
- Database schema validation: Foreign key constraints enforced, primary keys unique, no orphaned records after migration.
- Query latency benchmark: Top-K spectrum retrieval (k=2000) completes in <1 second per query spectrum, with sub-linear scaling in library size.
- Memory usage reduction: Peak memory during query execution is constant (not proportional to total library size).
- Unit test coverage: Database insertion, metadata filtering (by m/z tolerance, retention time range), and similarity score computation each have passing tests.

## Limitations

- MS2Query does not perform peak picking or clustering of similar MS2 spectra — pre-processing tools like MZMine should be used upstream to reduce spectral redundancy before database ingestion, or the resulting database will be unnecessarily large.
- Spectral data lacking consistent metadata annotations (SMILES, InChI, InChIKey) cannot be reliably stored in a normalized schema with enforced foreign keys, limiting query flexibility.
- The random forest re-ranking model requires pre-computed MS2Deepscore embeddings for all library spectra; if embeddings are missing or outdated, database query performance and result quality degrade.

## Evidence

- [other] Design SQLite schema to represent spectral library metadata and peak data (spectra, metadata tables with foreign keys): "Design SQLite schema to represent spectral library metadata and peak data (spectra, metadata tables with foreign keys)."
- [other] Implement Python data-migration code using sqlite3 module to load existing library formats (JSON/CSV/binary) and populate database tables: "Implement Python data-migration code using sqlite3 module to load existing library formats (JSON/CSV/binary) and populate the database tables."
- [other] Create query interface with SELECT/JOIN operations to retrieve spectra by metadata filters and compute similarity scores: "Create query interface (SELECT/JOIN operations) to retrieve spectra by metadata filters and compute similarity scores against query spectra."
- [intro] MS2Query provides reliable and fast MS/MS spectral-based analogue search: "MS2Query - Reliable and fast MS/MS spectral-based analogue search"
- [readme] MS2Query is scalable to large numbers of MS2 spectra: "MS2Query is easy to install (see below) and is scalable to large numbers of MS2 spectra."
- [readme] MS2Query does not do any peak picking or clustering of similar MS2 spectra: "MS2Query does not do any peak picking or clustering of similar MS2 spectra. If your files contain many MS2 spectra per feature it is advised to first reduce the number of MS2 spectra by clustering or"
- [other] Run existing test suite with python setup.py test to verify backward compatibility: "Run existing test suite with `python setup.py test` to verify backward compatibility and correctness of database queries."
