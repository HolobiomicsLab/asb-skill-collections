---
name: sql-query-optimization-for-similarity-search
description: Use when when migrating spectral library data from file-based formats (JSON, CSV, binary) into a persistent store and need to support fast filtered queries on metadata and similarity computations against query spectra.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3365
  tools:
  - MS2Query
  - GitHub
  - Python sqlite3 module
  - matchms
derived_from:
- doi: 10.1038/s41467-023-37446-4
  title: ms2query
evidence_spans:
- you want to make some kind of change to the code base
- MS2Query - Reliable and fast MS/MS spectral-based analogue search
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-023-37446-4
  all_source_dois:
  - 10.1038/s41467-023-37446-4
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# sql-query-optimization-for-similarity-search

## Summary

Design and implement SQLite schemas and query interfaces to enable efficient retrieval and similarity scoring of spectral library data. This skill optimizes database-backed storage of MS/MS spectra and metadata for fast analogue and exact-match searching without full-library linear scans.

## When to use

When migrating spectral library data from file-based formats (JSON, CSV, binary) into a persistent store and need to support fast filtered queries on metadata and similarity computations against query spectra. Use this skill when file I/O becomes a bottleneck for repeated library searches or when you want to enable programmatic queries on large spectral datasets (>tens of thousands of spectra).

## When NOT to use

- Library size is small (<1000 spectra) or queries are one-time; file-based search suffices and adds no I/O overhead.
- Spectral library is already stored in a production database system (PostgreSQL, MongoDB); re-migration to SQLite may lose transactional guarantees or concurrent write safety.
- Application requires real-time model retraining on new library spectra; SQLite schema is append-only and does not natively support online learning.

## Inputs

- Spectral library in file-based format (JSON, CSV, binary, mzML, MGF, msp, or pickled matchms object)
- Query spectra (mzML, JSON, MGF, msp, mzxml, USI, or pickled matchms object)
- Library metadata (precursor m/z, retention time, SMILES/InChI/InChIKey, molecular class annotations)

## Outputs

- SQLite database file with normalized schema (spectra, metadata, peaks tables with foreign keys)
- Query result CSV with library matches ranked by MS2Query model prediction score (0–1 range)
- Performance metrics (query latency, index overhead, throughput)

## How to apply

First, design a normalized SQLite schema with separate tables for spectra metadata (precursor m/z, retention time, molecular identifiers) and peak data, connected via foreign keys to enable efficient JOINs. Second, implement Python data-migration code using the sqlite3 module to parse existing library formats and bulk-insert records into the normalized schema. Third, construct query interfaces using SELECT and JOIN operations to retrieve spectra by metadata filters (e.g., precursor m/z tolerance, ion mode) and compute pairwise similarity scores (e.g., MS2Deepscore cosine or MS2Query model predictions) against query spectra. Fourth, establish performance thresholds for query latency and indexing strategies (e.g., B-tree indexes on precursor m/z to avoid full-table scans). Run the existing test suite with `python setup.py test` to verify backward compatibility, then add unit tests for database insertion correctness, schema validation, and query execution time to ensure no performance regression.

## Related tools

- **MS2Query** (Source library data and query spectra; provides pre-trained MS2Deepscore embeddings and random-forest model for ranking analogue/exact-match candidates by similarity score.) — https://github.com/iomega/ms2query
- **Python sqlite3 module** (Core database API for schema creation, bulk data insertion, and SQL query execution.)
- **matchms** (Library object representation and spectrum I/O (format parsing and serialization).)
- **GitHub** (Version control and pull-request workflow for documenting schema design and migration code.) — https://github.com/iomega/ms2query

## Examples

```
from ms2query.ms2library import create_library_object_from_one_dir; import sqlite3; ms2library = create_library_object_from_one_dir('./ms2query_library_files'); conn = sqlite3.connect('spectra.db'); conn.execute('CREATE TABLE spectra (spectrum_id INTEGER PRIMARY KEY, precursor_mz REAL, ionmode TEXT, FOREIGN KEY(spectrum_id) REFERENCES metadata(spectrum_id))'); conn.executemany('INSERT INTO spectra VALUES (?,?,?)', [(s.spectrum_id, s.precursor_mz, s.ionmode) for s in ms2library.spectra]); conn.commit(); results = conn.execute('SELECT * FROM spectra WHERE precursor_mz BETWEEN ? AND ?', (mz - 0.1, mz + 0.1)).fetchall()
```

## Evaluation signals

- Schema passes FOREIGN KEY constraint validation and all spectra in the input library are successfully inserted without data loss.
- Query latency for filtered spectrum retrieval (e.g., precursor m/z ± 0.1 Da) is <100 ms for libraries with >50,000 spectra; compare against baseline file-based lookup time.
- Similarity scores (e.g., MS2Query model prediction) computed via database queries match bit-for-bit with scores computed in-memory from the original library format.
- Existing test suite (`python setup.py test`) passes with zero failures; new unit tests for database insertion and schema validation achieve ≥90% code coverage.
- Results CSV matches expected output schema (columns for query spectrum ID, library match ID, precursor m/z difference, ms2query_model_prediction, molecular class) with reproducible row order.

## Limitations

- SQLite has no built-in vector similarity operators; cosine distance and MS2Deepscore embeddings must be computed in Python loops, not pushed down to the SQL engine (may be slower than specialized vector databases for very large libraries or high-frequency queries).
- MS2Query does not perform peak picking or spectrum clustering; if input files contain many redundant MS2 spectra per feature, preprocessing with MZMine or similar is required before database insertion to avoid storage bloat.
- Backward compatibility with older file-based library formats depends on explicit migration code; any undocumented binary format changes in upstream MS2Query may require schema revision.
- SQLite is single-threaded for writes; concurrent library updates from multiple processes may cause lock contention or schema conflicts.

## Evidence

- [other] Design SQLite schema to represent spectral library metadata and peak data (spectra, metadata tables with foreign keys).: "Design SQLite schema to represent spectral library metadata and peak data (spectra, metadata tables with foreign keys)."
- [other] Implement Python data-migration code using sqlite3 module to load existing library formats (JSON/CSV/binary) and populate the database tables.: "Implement Python data-migration code using sqlite3 module to load existing library formats (JSON/CSV/binary) and populate the database tables."
- [other] Create query interface (SELECT/JOIN operations) to retrieve spectra by metadata filters and compute similarity scores against query spectra.: "Create query interface (SELECT/JOIN operations) to retrieve spectra by metadata filters and compute similarity scores against query spectra."
- [readme] MS2Query is easy to install (see below) and is scalable to large numbers of MS2 spectra.: "MS2Query is easy to install (see below) and is scalable to large numbers of MS2 spectra."
- [readme] By using pre-computed MS2Deepscore embeddings for library spectra, this full-library comparison can be computed very quickly.: "By using pre-computed MS2Deepscore embeddings for library spectra, this full-library comparison can be computed very quickly."
- [other] Run existing test suite with `python setup.py test` to verify backward compatibility and correctness of database queries.: "Run existing test suite with `python setup.py test` to verify backward compatibility and correctness of database queries."
- [other] Add unit tests for database insertion, schema validation, and query performance thresholds.: "Add unit tests for database insertion, schema validation, and query performance thresholds."
- [readme] MS2Query does not do any peak picking or clustering of similar MS2 spectra. If your files contain many MS2 spectra per feature it is advised to first reduce the number of MS2 spectra by clustering or feature selection.: "MS2Query does not do any peak picking or clustering of similar MS2 spectra. If your files contain many MS2 spectra per feature it is advised to first reduce the number of MS2 spectra by clustering or"
