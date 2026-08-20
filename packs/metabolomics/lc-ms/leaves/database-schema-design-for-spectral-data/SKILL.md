---
name: database-schema-design-for-spectral-data
description: Use when you have MS/MS spectral library data currently stored in file-based formats (JSON, CSV, binary, MGF, MSP) and need to migrate to database-backed storage to support fast queries by metadata filters (precursor m/z, ion mode, retention time) and computed similarity scores against query.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3372
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# database-schema-design-for-spectral-data

## Summary

Design and implement a SQLite schema to represent MS/MS spectral library data (spectra, metadata, peak information) with relational structure (foreign keys, normalized tables) to enable efficient similarity-based querying and filtering of library spectra by metadata and computed scores.

## When to use

You have MS/MS spectral library data currently stored in file-based formats (JSON, CSV, binary, MGF, MSP) and need to migrate to database-backed storage to support fast queries by metadata filters (precursor m/z, ion mode, retention time) and computed similarity scores against query spectra, especially when scaling to large numbers of library spectra or supporting repeated analogue/exact-match searches.

## When NOT to use

- Your spectral library is small (<1000 spectra) and access patterns are infrequent; file-based storage with in-memory loading may suffice and adds simpler deployment.
- You require real-time streaming ingestion of new spectra and your schema is highly volatile; a document store (MongoDB) or append-only log may be more appropriate than SQLite.
- Library spectra lack essential metadata (precursor m/z, ion mode, or compound annotations); the relational schema cannot enforce data quality and queries will return incomplete results.

## Inputs

- Spectral library files in JSON, CSV, binary, MGF, MSP, or mzML format
- Spectral metadata: precursor m/z, ion mode, compound name, SMILES, InChI, retention time, scan number
- Peak data: m/z and intensity pairs for each spectrum
- Query spectra in same formats (for validation and test cases)
- Optional: pre-computed MS2Deepscore embeddings for library spectra

## Outputs

- SQLite database file (.db or .sqlite) with normalized schema
- Populated spectra and peaks tables with foreign key integrity
- Query result sets: DataFrames or lists of library spectra ranked by similarity score
- Database connection object and query interface (Python class/module)
- Unit test suite covering schema, insertion, and query correctness
- Updated documentation with schema diagram and migration instructions
- Migration logs or summary (counts of spectra/peaks inserted, validation errors)

## How to apply

First, design normalized SQLite tables to represent spectral library structure: a primary spectra table with metadata columns (precursor_mz, ion_mode, compound_name, inchi/smiles), a peaks table with foreign key references to spectra (storing m/z and intensity pairs), and optional tables for embeddings (e.g., MS2Deepscore pre-computed vectors) and compound annotations. Second, implement Python migration code using the sqlite3 module to parse existing library formats and populate tables with atomic transactions and schema validation. Third, create query interfaces using SELECT/JOIN operations to retrieve spectra by metadata filters (e.g., precursor m/z window, ion mode) and compute similarity metrics (e.g., cosine score, MS2Query model prediction) by joining query spectra against library peaks. Fourth, run the existing test suite (`python setup.py test`) to verify backward compatibility and correctness of database queries against expected results (e.g., dummy_spectra.mgf → expected_results_dummy_data.csv). Fifth, add unit tests covering database insertion idempotence, schema constraint enforcement, and query performance thresholds (e.g., sub-second retrieval for top-K spectral matches). Finally, document connection strings, migration examples, and schema ER diagrams in the project README.

## Related tools

- **MS2Query** (Spectral library matching and analogue/exact-match search engine that consumes the database-backed library; supports custom library creation and query via Python API) — https://github.com/iomega/ms2query
- **Python sqlite3 module** (Standard library module for creating, populating, and querying SQLite databases; used to implement schema creation and data migration)
- **matchms** (Library for parsing and manipulating MS/MS spectra in multiple formats (mzML, JSON, MGF, MSP); used to deserialize input spectral data before migration)
- **GitHub** (Version control and collaborative development platform for managing feature branches, pull requests, and schema documentation) — https://github.com/iomega/ms2query

## Examples

```
import sqlite3
from matchms.importing import load_from_mgf

conn = sqlite3.connect('spectral_library.db')
cursor = conn.cursor()
cursor.execute('CREATE TABLE spectra (id INTEGER PRIMARY KEY, precursor_mz REAL, ion_mode TEXT, compound_name TEXT, inchi TEXT)')
cursor.execute('CREATE TABLE peaks (id INTEGER PRIMARY KEY, spectrum_id INTEGER, mz REAL, intensity REAL, FOREIGN KEY(spectrum_id) REFERENCES spectra(id))')

for spectrum in load_from_mgf('library.mgf'):
    cursor.execute('INSERT INTO spectra (precursor_mz, ion_mode, compound_name, inchi) VALUES (?, ?, ?, ?)', 
                   (spectrum.precursor_mz, spectrum.metadata.get('ionmode'), spectrum.metadata.get('compound_name'), spectrum.metadata.get('inchi')))
    spectrum_id = cursor.lastrowid
    for mz, intensity in zip(spectrum.mz, spectrum.intensities):
        cursor.execute('INSERT INTO peaks (spectrum_id, mz, intensity) VALUES (?, ?, ?)', (spectrum_id, mz, intensity))

conn.commit()
conn.close()
```

## Evaluation signals

- Database schema creation succeeds without errors; all tables exist with correct column types, primary/foreign keys, and constraints enforced by SQLite
- Existing test suite (`python setup.py test`) passes 100%; no regression in query correctness or backward compatibility with file-based library format
- Migration code populates all spectra and peaks rows from input library without data loss; row counts match source file records and no NULL values in non-nullable columns
- Query performance meets thresholds: metadata-filtered queries (e.g., precursor m/z ± 0.1 Da) return results in <1 second for libraries with >100k spectra; SELECT with JOINs to peaks table execute efficiently
- Unit tests verify schema validation (reject invalid precursor m/z, ion mode enum constraints), insertion atomicity (rollback on constraint violation), and similarity score correctness (e.g., cosine ≥ 0 and ≤ 1, MS2Query prediction in [0,1])

## Limitations

- SQLite is single-writer and may not be suitable for high-concurrency scenarios with many simultaneous insertion/update processes; production deployments with concurrent writes should consider PostgreSQL or MySQL.
- Pre-computed MS2Deepscore embeddings must be stored separately or as BLOB columns; managing embedding size and format adds complexity. Schema design must balance query speed against storage footprint.
- Library spectra lacking SMILES, InChI, or InChIKey metadata cannot be reliably annotated with molecular class or structure; such spectra should be flagged during migration validation and excluded or handled with NULL placeholders.
- Migration from legacy file formats requires custom parsing logic for each input type (JSON vs. CSV vs. binary); validation and error recovery (e.g., malformed records) must be implemented per format to avoid partial/corrupted database state.

## Evidence

- [other] Design SQLite schema to represent spectral library metadata and peak data (spectra, metadata tables with foreign keys).: "Design SQLite schema to represent spectral library metadata and peak data (spectra, metadata tables with foreign keys)."
- [other] Implement Python data-migration code using sqlite3 module to load existing library formats (JSON/CSV/binary) and populate the database tables.: "Implement Python data-migration code using sqlite3 module to load existing library formats (JSON/CSV/binary) and populate the database tables."
- [other] Create query interface (SELECT/JOIN operations) to retrieve spectra by metadata filters and compute similarity scores against query spectra.: "Create query interface (SELECT/JOIN operations) to retrieve spectra by metadata filters and compute similarity scores against query spectra."
- [other] Run existing test suite with `python setup.py test` to verify backward compatibility and correctness of database queries.: "Run existing test suite with `python setup.py test` to verify backward compatibility and correctness of database queries."
- [other] MS2Query supports creating custom libraries and provides documentation for building MS2Query into other tools, establishing the framework for implementing database-backed library storage.: "MS2Query supports creating custom libraries and provides documentation for building MS2Query into other tools, establishing the framework for implementing database-backed library storage."
- [readme] It is important that the library spectra are annotated with smiles, inchi's or inchikeys in the metadata otherwise they are not included in the library.: "It is important that the library spectra are annotated with smiles, inchi's or inchikeys in the metadata otherwise they are not included in the library."
- [other] make sure the existing tests still work by running ``python setup.py test``: "make sure the existing tests still work by running ``python setup.py test``"
