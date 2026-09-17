---
name: sqlite-query-execution-and-cursor-management
description: Use when you have mass spectrometry data stored in a SQLite database
  indexed by spectrum ID and need to retrieve specific spectra by ID (random access
  via __getitem__) or iterate through all spectra sequentially (via read method).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - sqlite3
  - xml.etree.ElementTree
  - pymzML
  - Python
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1093/bioinformatics/bty046
  title: pymzml
evidence_spans:
- import sqlite3
- import xml.etree.ElementTree as et
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pymzml
    doi: 10.1093/bioinformatics/bty046
    title: pymzml
  dedup_kept_from: coll_pymzml
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/bty046
  all_source_dois:
  - 10.1093/bioinformatics/bty046
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# sqlite-query-execution-and-cursor-management

## Summary

Execute SQL queries against a SQLite database using cursor objects to retrieve spectrum metadata and XML payloads, then parse results into structured Spectrum or Chromatogram objects for downstream analysis. This skill enables random-access and sequential retrieval patterns required for integrating mass spectrometry databases with pymzML's FileInterface.

## When to use

You have mass spectrometry data stored in a SQLite database indexed by spectrum ID and need to retrieve specific spectra by ID (random access via __getitem__) or iterate through all spectra sequentially (via read method). The database contains a Spectra table with columns ID (INT) and xml (TEXT), and you are implementing a custom file-handler class to expose this data through pymzML.run.Reader.

## When NOT to use

- Your data is stored in uncompressed mzML files: pymzML already handles mzML with rapid seeking and indexed gzip support; wrapping it in SQLite adds unnecessary overhead.
- You need write-access to the database or need to update spectra after initial import: this skill assumes read-only cursor queries and does not address transaction handling or schema mutations.
- The spectrum ID field is non-integer or contains custom delimiters like 'scan=1': the implementation assumes integer primary keys; non-standard identifiers require custom regex parsing upstream.

## Inputs

- SQLite database file (.db) containing a Spectra table with columns: ID (INT), xml (TEXT)
- spectrum ID (integer key) for random-access lookups
- pymzML FileInterface class for registration

## Outputs

- Spectrum or Chromatogram object (parsed from XML string)
- Integer count of total spectra in database
- Sequential XML element strings for iteration

## How to apply

Establish a sqlite3 connection and cursor in __init__. For random-access retrieval, execute a SELECT query in __getitem__ that fetches the XML string matching the requested spectrum ID, then parse it using xml.etree.ElementTree.XML() and return a Spectrum or Chromatogram object. For sequential iteration, implement a read method that maintains internal state (current_spectrum_id) and returns XML element strings one at a time. For metadata queries like spectrum count, execute a SELECT COUNT(*) query and return the integer result. Register the resulting SQLiteDatabase class in FileInterface._open by adding an elif statement that detects .db file extensions and instantiates SQLiteDatabase(path, encoding).

## Related tools

- **sqlite3** (Execute SQL queries (SELECT COUNT, SELECT with WHERE clause) and manage cursor lifecycle against the Spectra table)
- **xml.etree.ElementTree** (Parse XML string representations of spectra retrieved from database into DOM trees for instantiation as Spectrum or Chromatogram objects)
- **pymzML** (Provide FileInterface base class for registration, and Spectrum/Chromatogram object constructors) — https://github.com/pymzml/pymzML
- **Python** (Language for implementing SQLiteDatabase class and cursor management)

## Examples

```
db = SQLiteDatabase('test.db'); my_spec = db[5]; print(my_spec['ms level']); count = db.get_spectrum_count()
```

## Evaluation signals

- Verify random access: call db[unique_id] and confirm a Spectrum or Chromatogram object is returned with matching ID
- Verify sequential iteration: call iter(SQLiteDatabase('test.db')) and confirm all spectra are yielded in order without errors
- Verify spectrum count: call db.get_spectrum_count() and compare against SELECT COUNT(*) result from raw sqlite3 cursor
- Verify XML parsing: inspect returned Spectrum object attributes (e.g., spectrum['ms level'], spectrum.ID) match values in original mzML
- Verify FileInterface registration: instantiate pymzml.run.Reader('test.db') and confirm it uses SQLiteDatabase without errors

## Limitations

- Requires a pre-populated SQLite database with exact schema (Spectra table, ID INT, xml TEXT); no schema auto-migration or validation
- Read-only cursor operations: no support for INSERT, UPDATE, or DELETE; the database must be created and indexed offline
- Spectrum XML parsing assumes well-formed XML and standard mzML element names; malformed or non-standard mzML stored in the database will cause xml.etree.ElementTree.XML() to raise ParseError
- Sequential read() method maintains in-memory state and does not support concurrent iteration or restart from mid-stream without reimplementation

## Evidence

- [other] Implement the SQLiteDatabase class with __init__ to establish a sqlite3 connection and cursor, __getitem__ to execute SELECT queries on the Spectra table and return parsed Spectrum or Chromatogram objects using xml.etree.ElementTree.XML parsing, get_spectrum_count to return the total row count from the Spectra table via SELECT COUNT(*), and read to sequentially return XML element strings by current_spectrum_id.: "Implement the SQLiteDatabase class with __init__ to establish a sqlite3 connection and cursor, __getitem__ to execute SELECT queries on the Spectra table and return parsed Spectrum or Chromatogram"
- [other] Create a SQLite database from an mzML file by parsing each spectrum using pymzML.run.Reader and storing the spectrum ID and XML string representation in a Spectra table with two columns (ID INT, xml TEXT).: "Create a SQLite database from an mzML file by parsing each spectrum using pymzML.run.Reader and storing the spectrum ID and XML string representation in a Spectra table with two columns (ID INT, xml"
- [other] Modify FileInterface._open to add an elif statement checking for .db file endings and instantiate SQLiteDatabase(path, encoding) as the file_handler.: "Modify FileInterface._open to add an elif statement checking for .db file endings and instantiate SQLiteDatabase(path, encoding) as the file_handler."
- [abstract] pymzML is an extension to Python that offers: "pymzML is an extension to Python that offers"
