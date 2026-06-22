---
name: spectral-library-data-modeling
description: Use when when migrating an existing file-based spectral library (stored as JSON, CSV, or binary formats) into a production system that requires frequent subset queries by metadata filters, similarity scoring across large spectral collections, or integration into downstream tools like MS2Query that.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - MS2Query
  - GitHub
  - Python sqlite3 module
  - matchms
  techniques:
  - LC-MS
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

# spectral-library-data-modeling

## Summary

Design and implement a normalized database schema (e.g. SQLite) to represent MS/MS spectral library metadata and peak data, replacing file-based storage (JSON/CSV/binary) to enable efficient querying and analogue search operations at scale.

## When to use

When migrating an existing file-based spectral library (stored as JSON, CSV, or binary formats) into a production system that requires frequent subset queries by metadata filters, similarity scoring across large spectral collections, or integration into downstream tools like MS2Query that perform full-library MS2 comparisons. This is essential when scaling from small custom libraries to large GNPS-scale repositories or when building MS2Query into other analytical platforms.

## When NOT to use

- Input is a small custom library (< 1000 spectra) used only for offline analysis or single batch queries—file-based storage with in-memory filtering is sufficient.
- Library spectra lack standardized metadata (smiles, inchi, inchikey)—database schema design depends on annotated records; unannotated spectra cannot be properly indexed.
- Application requires real-time writes from multiple concurrent processes—SQLite is not optimized for high-concurrency write workloads; consider PostgreSQL or similar for production multi-user systems.

## Inputs

- file-based spectral library (JSON, CSV, binary format, or pickled matchms objects)
- library metadata table (precursor m/z, retention time, smiles/inchi/inchikey, molecular class annotations)
- peak data (m/z-intensity pairs per spectrum)
- existing unit test suite

## Outputs

- SQLite database file (.db) with normalized schema (spectra, metadata, peaks tables)
- Python query interface module for retrieving spectra by metadata filters and computing similarity scores
- updated unit test suite with database-specific tests (schema validation, insertion, performance)
- migration documentation and code examples for integrating database-backed library into other tools

## How to apply

First, design a normalized SQLite schema with separate tables for spectral metadata (precursor m/z, retention time, molecular annotations) and peak data (m/z-intensity pairs), linked by foreign keys to enable join operations. Second, implement a Python data-migration pipeline using the sqlite3 module to parse existing library formats and bulk-insert records into the schema. Third, create a query interface that supports SELECT/JOIN operations to retrieve spectra filtered by metadata ranges (e.g. precursor m/z ± tolerance) and compute MS2Deepscore similarity or cosine scores against query spectra. Fourth, verify backward compatibility by running the existing test suite (`python setup.py test`) and add unit tests for schema validation, database insertion correctness, and query performance thresholds. Finally, document the SQLite connection API and provide migration instructions so other tools can consume the database-backed library.

## Related tools

- **MS2Query** (spectral library matching and analogue search tool that consumes SQLite-backed library for fast MS2Deepscore embedding lookup and random forest re-ranking) — https://github.com/iomega/ms2query
- **Python sqlite3 module** (library for designing schema, executing DDL (CREATE TABLE), and bulk-loading spectral data via INSERT statements)
- **matchms** (spectral data format for loading and converting library spectra; MS2Query supports pickled matchms objects as input)

## Examples

```
import sqlite3; conn = sqlite3.connect('ms2query_library.db'); conn.execute('CREATE TABLE spectra (id INTEGER PRIMARY KEY, precursor_mz REAL, retention_time REAL, smiles TEXT)'); conn.execute('CREATE TABLE peaks (spectrum_id INTEGER, mz REAL, intensity REAL, FOREIGN KEY(spectrum_id) REFERENCES spectra(id))'); conn.commit(); conn.close()
```

## Evaluation signals

- Database schema validation: verify foreign key constraints are enforced and all tables have appropriate indexes on frequently queried columns (precursor_mz, retention_time, molecular_class).
- Data integrity: compare row counts and peak intensity distributions between source file formats and SQLite tables to confirm no spectra or peaks were dropped or corrupted during migration.
- Query performance: confirm that metadata-filtered subset queries (e.g. precursor m/z ± 0.05 Da) return results in < 100 ms for 100k-spectrum libraries, and similarity scoring against top 2000 candidates completes in < 30 seconds.
- Backward compatibility: run existing test suite (`python setup.py test`) and confirm all tests pass; new unit tests for database insertion and schema validation should achieve ≥ 95% code coverage.
- MS2Query integration: verify that MS2Query can load the SQLite library, perform library search and analogue search on dummy spectra, and produce output CSV with expected columns (library match, ms2query_model_prediction, precursor_mz_difference) matching expected_results_dummy_data.csv.

## Limitations

- SQLite is not optimized for concurrent write workloads; if the library must be updated frequently by multiple processes, consider migration to PostgreSQL or similar.
- Library spectra must be annotated with smiles, inchi, or inchikey metadata—unannotated spectra will not be included in the database and cannot be queried by molecular class.
- MS2Query does not perform peak picking or clustering of similar MS2 spectra; preprocessing with tools like MZMine is recommended to reduce duplicate spectra per feature before database loading.
- Query performance depends on index design; poorly chosen indexes or excessive table joins can degrade performance on very large libraries (> 1M spectra).

## Evidence

- [other] Design SQLite schema to represent spectral library metadata and peak data (spectra, metadata tables with foreign keys): "Design SQLite schema to represent spectral library metadata and peak data (spectra, metadata tables with foreign keys)"
- [other] Implement Python data-migration code using sqlite3 module to load existing library formats (JSON/CSV/binary) and populate the database tables: "Implement Python data-migration code using sqlite3 module to load existing library formats (JSON/CSV/binary) and populate the database tables"
- [other] Create query interface (SELECT/JOIN operations) to retrieve spectra by metadata filters and compute similarity scores against query spectra: "Create query interface (SELECT/JOIN operations) to retrieve spectra by metadata filters and compute similarity scores against query spectra"
- [readme] It is important that the library spectra are annotated with smiles, inchi's or inchikeys in the metadata otherwise they are not included in the library: "It is important that the library spectra are annotated with smiles, inchi's or inchikeys in the metadata otherwise they are not included in the library"
- [readme] MS2Query does not do any peak picking or clustering of similar MS2 spectra. If your files contain many MS2 spectra per feature it is advised to first reduce the number of MS2 spectra by clustering or feature selection: "MS2Query does not do any peak picking or clustering of similar MS2 spectra. If your files contain many MS2 spectra per feature it is advised to first reduce the number of MS2 spectra by clustering or"
- [other] make sure the existing tests still work by running ``python setup.py test``: "make sure the existing tests still work by running ``python setup.py test``"
- [other] Run existing test suite with `python setup.py test` to verify backward compatibility and correctness of database queries: "Run existing test suite with `python setup.py test` to verify backward compatibility and correctness of database queries"
- [other] MS2Query supports creating custom libraries and provides documentation for building MS2Query into other tools, establishing the framework for implementing database-backed library storage: "MS2Query supports creating custom libraries and provides documentation for building MS2Query into other tools, establishing the framework for implementing database-backed library storage"
