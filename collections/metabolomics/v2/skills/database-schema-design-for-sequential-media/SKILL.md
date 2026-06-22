---
name: database-schema-design-for-sequential-media
description: Use when when you have large sequential media files (mzML spectra, text chapters, or similar) and need to enable both random access by ID and sequential iteration without loading the entire file into memory.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3750
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - sqlite3
  - xml.etree.ElementTree
  - Python
  - pymzML
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# database-schema-design-for-sequential-media

## Summary

Design and implement a relational database schema to store sequential media (spectra, chapters, or other indexed records) with ID and content columns, enabling efficient random access and iteration. This skill is essential when converting large sequential files into queryable databases for indexed, seekable access.

## When to use

When you have large sequential media files (mzML spectra, text chapters, or similar) and need to enable both random access by ID and sequential iteration without loading the entire file into memory. Apply this skill before implementing custom file wrappers or indexed compression formats that depend on database-backed storage.

## When NOT to use

- Input is already a structured relational database or query-ready format — use direct queries instead.
- Sequential media is small enough to fit in memory — direct in-memory iteration is simpler.
- Random access is not required and only sequential reading is needed — skip the database layer.

## Inputs

- Sequential media file (mzML, text, or similar)
- File parsing logic or parser module
- Target database file path

## Outputs

- sqlite3 database file with indexed columns
- Populated schema with ID and content fields
- Database connection object for querying

## How to apply

Create a two-column relational schema using sqlite3 with an ID column (for unique identifiers like spectrum number or chapter index) and a content column (TEXT or BLOB for the actual data payload). Parse the source sequential file and INSERT each record into the database. The schema design should support fast lookups by ID via indexed queries and efficient sequential scans via cursor iteration. Validate by confirming that direct ID access (e.g., `SELECT * FROM table WHERE ID = X`) and full-table iteration both complete without errors and return expected record counts.

## Related tools

- **sqlite3** (Create and manage the relational database schema with ID and content columns; execute INSERT and SELECT queries for record storage and retrieval) — https://www.python.org/dev/peps/pep-0249/
- **Python** (Write parsing logic to load sequential media file, extract records, and insert into database via sqlite3 connection)
- **xml.etree.ElementTree** (Parse XML-based sequential formats (e.g., mzML) to extract record IDs and content before database insertion) — https://docs.python.org/3/library/xml.etree.elementtree.html
- **pymzML** (Reference example for wrapping database-backed sequential access; enables custom file classes to retrieve records from sqlite3 via __getitem__ and read() methods) — https://github.com/pymzml/pymzML

## Examples

```
import sqlite3; conn = sqlite3.connect('spectra.db'); cursor = conn.cursor(); cursor.execute('CREATE TABLE spectra (ID INTEGER PRIMARY KEY, xml TEXT)'); cursor.execute('INSERT INTO spectra (ID, xml) VALUES (?, ?)', (1, spectrum_xml_string)); conn.commit(); my_spectrum = cursor.execute('SELECT xml FROM spectra WHERE ID=?', (5,)).fetchone()
```

## Evaluation signals

- Database file exists and contains expected number of records — run `SELECT COUNT(*) FROM table_name`.
- Random access by ID succeeds and returns correct record — e.g., `db[5]` returns spectrum/chapter with ID=5 without iteration.
- Sequential iteration completes without errors and visits all records in order — iterate via cursor or for-loop wrapper.
- Schema columns (ID, content) are indexed and queries complete in sub-second time for 10k+ records.
- No duplicate IDs exist — confirm via `SELECT ID, COUNT(*) FROM table_name GROUP BY ID HAVING COUNT(*) > 1`.

## Limitations

- sqlite3 has concurrent write limitations — suitable for read-heavy workflows but not for high-frequency concurrent inserts.
- Large content fields (e.g., full spectrum arrays as TEXT) can bloat database file size; consider BLOB or external file references for very large payloads.
- No built-in support for nested or hierarchical records — schema is flat; complex multi-level structures require normalization or serialization.
- Sequential parsing of the source file is I/O-bound; initial database population may be slow for very large source files (>1 GB).

## Evidence

- [other] Create a database schema with two columns (ID for chapter number, xml TEXT for chapter content as string) using sqlite3.: "Create a database schema with two columns (ID for chapter number, xml TEXT for chapter content as string) using sqlite3"
- [other] Load Moby Dick text file and parse into chapters, storing each chapter's text and ID into the database using INSERT statements.: "Load Moby Dick text file and parse into chapters, storing each chapter's text and ID into the database using INSERT statements"
- [other] In order to make pymzML accept other kinds of mzML data (e.g databases), one can implement an own wrapper: "In order to make pymzML accept other kinds of mzML data (e.g databases), one can implement an own wrapper"
- [other] At first, a database with a specific layout needs to be created. Here, we use a single mzML file and store each spectrum in a table with 2 columns: "At first, a database with a specific layout needs to be created. Here, we use a single mzML file and store each spectrum in a table with 2 columns"
- [other] Retrieve a specific spectrum from your database db = SQLiteDatabase('test.db') unique_id = 5 my_spec = db[unique_id]: "Retrieve a specific spectrum from your database db = SQLiteDatabase('test.db') unique_id = 5 my_spec = db[unique_id]"
