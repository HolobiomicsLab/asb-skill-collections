---
name: test-driven-database-development
description: Use when when you have an existing tool or library with file-based storage (JSON, CSV, binary formats) that needs to support efficient querying across large datasets, and you want to migrate to a relational database without breaking existing functionality or performance expectations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3050
  tools:
  - MS2Query
  - GitHub
  - Python sqlite3 module
  techniques:
  - mass-spectrometry
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

# test-driven-database-development

## Summary

A systematic approach to migrating file-based data storage into a relational database by designing schemas, implementing data loaders, and validating correctness through unit tests and backward-compatibility checks. This skill ensures database-backed libraries maintain query performance and data integrity during refactoring.

## When to use

When you have an existing tool or library with file-based storage (JSON, CSV, binary formats) that needs to support efficient querying across large datasets, and you want to migrate to a relational database without breaking existing functionality or performance expectations.

## When NOT to use

- Input data is already in a relational database or has strict real-time requirements incompatible with SQLite.
- The tool or library has no existing test suite, making backward-compatibility verification impossible.
- Query patterns are purely ad-hoc or the domain does not have well-defined metadata or filtering requirements suitable for schema design.

## Inputs

- File-based library data (JSON, CSV, or binary formats)
- Existing test suite for the tool
- Documentation of metadata and data structure
- Domain-specific query patterns and performance benchmarks

## Outputs

- SQLite database schema with normalized tables
- Python migration script(s) to populate database from file sources
- Query interface module (SELECT, JOIN, filtering operations)
- Unit test suite for database operations and performance
- Updated documentation with connection examples
- Updated CHANGELOG.md entry
- Feature branch and pull request with schema documentation

## How to apply

Begin by designing a normalized SQLite schema with separate tables for spectral metadata and peak data, joined by foreign keys. Implement Python data-migration code using the sqlite3 module to load existing file formats and populate tables. Create query interfaces (SELECT/JOIN operations) to retrieve records by metadata filters and compute domain-specific scores (e.g., similarity scores for spectra). Run the existing test suite (`python setup.py test`) to verify backward compatibility and correctness. Add unit tests for database insertion, schema validation, and query performance thresholds. Document SQLite connection patterns and migration instructions, update CHANGELOG.md, and submit changes via pull request with schema documentation.

## Related tools

- **MS2Query** (Spectral library matching tool that supports custom libraries and provides framework for database-backed storage) — https://github.com/iomega/ms2query
- **Python sqlite3 module** (Standard library for creating and querying SQLite databases during data migration)
- **GitHub** (Version control and pull-request workflow for submitting database schema changes and feature documentation) — https://github.com/iomega/ms2query

## Examples

```
# Design schema, create migration script, and validate
python -c "import sqlite3; conn = sqlite3.connect('ms2query_lib.db'); cursor = conn.cursor(); cursor.execute('CREATE TABLE spectra (id INTEGER PRIMARY KEY, spectrum_data BLOB)'); cursor.execute('CREATE TABLE metadata (id INTEGER PRIMARY KEY, spectrum_id INTEGER, key TEXT, value TEXT, FOREIGN KEY(spectrum_id) REFERENCES spectra(id))'); conn.commit()" && python setup.py test && python -m pytest tests/test_database_insertion.py -v
```

## Evaluation signals

- Existing test suite (`python setup.py test`) passes without modification, confirming backward compatibility.
- Unit tests for database insertion verify that all rows are correctly inserted and queryable by foreign key.
- Query performance thresholds (e.g., response time for similarity score computation) meet or exceed file-based baseline.
- Schema validation tests confirm all metadata fields are preserved and nullable columns match the original data distribution.
- Integration test: a query spectrum returns the same ranked top-N library matches as the file-based implementation.

## Limitations

- SQLite is not suitable for concurrent writes or real-time streaming; for production systems handling high write concurrency, consider PostgreSQL or a more robust RDBMS.
- Migration performance depends on the size of the existing library and the I/O overhead of parsing heterogeneous file formats; large libraries (>10 GB) may require batching or incremental loading.
- Schema design decisions must account for the specific metadata and query patterns of the domain; poor normalization or missing indexes can negate performance gains over file-based storage.

## Evidence

- [other] Design SQLite schema to represent spectral library metadata and peak data (spectra, metadata tables with foreign keys): "Design SQLite schema to represent spectral library metadata and peak data (spectra, metadata tables with foreign keys)."
- [other] Implement Python data-migration code using sqlite3 module to load existing library formats (JSON/CSV/binary) and populate the database tables: "Implement Python data-migration code using sqlite3 module to load existing library formats (JSON/CSV/binary) and populate the database tables."
- [other] Run existing test suite with `python setup.py test` to verify backward compatibility and correctness of database queries: "Run existing test suite with `python setup.py test` to verify backward compatibility and correctness of database queries."
- [other] MS2Query supports creating custom libraries and provides documentation for building MS2Query into other tools, establishing the framework for implementing database-backed library storage: "MS2Query supports creating custom libraries and provides documentation for building MS2Query into other tools, establishing the framework for implementing database-backed library storage."
- [other] make sure the existing tests still work by running ``python setup.py test``: "make sure the existing tests still work by running ``python setup.py test``"
