---
name: sqlite-database-design-and-schema-creation
description: Use when you have an mzML file and need to enable random-access spectrum
  retrieval by integer or string identifiers without holding the entire mzML in memory
  or decompressing indexed gzip files.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3703
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - sqlite3
  - ElementTree
  - pymzML
  - ElementTree (xml.etree.ElementTree)
  - psf/black
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
  - build: coll_pymzml_cq
    doi: 10.1093/bioinformatics/bty046
    title: pymzml
  dedup_kept_from: coll_pymzml_cq
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

# sqlite-database-design-and-schema-creation

## Summary

Design and populate a SQLite database schema to store mass spectrometry spectra as indexed key-value pairs (spectrum ID and XML element), enabling random-access parsing of mzML data without full file decompression. This skill bridges file format abstraction by materializing spectral metadata into a queryable relational structure compatible with pymzML's FileInterface.

## When to use

You have an mzML file and need to enable random-access spectrum retrieval by integer or string identifiers without holding the entire mzML in memory or decompressing indexed gzip files. This is most useful when the mzML file is large, access patterns are sparse, or you need to integrate with custom data pipelines that expect key-value semantics.

## When NOT to use

- Input mzML file is already indexed gzip format (.mzML.gz with random-access support) — use GSGR class instead for direct access without materialization.
- Spectrum access pattern is fully sequential and memory is not constrained — parse mzML directly with pymzML.Reader to avoid database I/O overhead.
- Database file size would exceed available disk space or schema normalization is required for complex metadata queries beyond ID-based lookup.

## Inputs

- mzML file path (uncompressed or gzip-compressed)
- Output SQLite database file path (.db)

## Outputs

- SQLite database file (.db) with 'Spectra' table
- Table schema: (id TEXT/INTEGER PRIMARY KEY, xml_element TEXT)

## How to apply

First, parse the mzML file and extract each spectrum's ID and XML element using pymzML or ElementTree, then create a SQLite database with a 'Spectra' table containing two columns: one for the identifier (string or integer) and one for the serialized XML element string. Design the schema to support O(1) lookup by primary key (spectrum ID). Populate the table by iterating through spectra in the mzML file and INSERT each record. Verify schema integrity by executing a test query: SELECT COUNT(*) should match the total spectrum count, and SELECT xml_element WHERE id=? should return valid XML that can be re-parsed into a Spectrum or Chromatogram object by pymzML's spec module.

## Related tools

- **sqlite3** (SQL database engine for persistent storage and indexed retrieval of spectrum records)
- **pymzML** (Parser and interface layer for mzML data; provides Spectrum/Chromatogram spec module and FileInterface dispatch mechanism) — https://github.com/pymzml/pymzML
- **ElementTree (xml.etree.ElementTree)** (XML parsing and serialization for extracting and reconstructing spectrum elements from strings)
- **psf/black** (Code style enforcement for connector class implementation) — https://github.com/psf/black

## Examples

```
import sqlite3; from pymzml import spec; import xml.etree.ElementTree as et; conn = sqlite3.connect('spectra.db'); conn.execute('CREATE TABLE Spectra (id TEXT PRIMARY KEY, xml_element TEXT)'); spectra_xml = [('<spectrum id="scan=1">...</spectrum>', 'scan=1')]; conn.executemany('INSERT INTO Spectra VALUES (?, ?)', [(xml, idx) for xml, idx in spectra_xml]); conn.commit(); result = conn.execute('SELECT xml_element FROM Spectra WHERE id=?', ('scan=1',)).fetchone(); print(et.fromstring(result[0]))
```

## Evaluation signals

- Database file is created at the specified path and is a valid SQLite file (verified via `sqlite3 <path> "SELECT sqlite_version();"`).
- SELECT COUNT(*) FROM Spectra returns a count equal to the total number of spectra in the source mzML file.
- SELECT xml_element FROM Spectra WHERE id=<test_id> returns a non-empty string that can be parsed by ElementTree.fromstring() without error.
- Instantiating a SQLiteDatabase connector class and calling __getitem__(<test_id>) returns a valid Spectrum or Chromatogram object with populated attributes (m/z, intensity, scan metadata).
- Schema has a PRIMARY KEY constraint on the id column; duplicate inserts are rejected or handled deterministically.

## Limitations

- Database creation is a one-time materialization; updates to the original mzML file are not automatically reflected in the database.
- Storage footprint is larger than the original gzip-compressed mzML because XML elements are stored as TEXT without compression; consider enabling SQLite page compression or VACUUM for large databases.
- Sequential read performance may be slower than streaming mzML parsing because each spectrum requires a separate SQL query; batch queries or indexed scans may be necessary for high-throughput workflows.
- Text storage of XML elements can lead to encoding issues if the original mzML contains non-UTF-8 characters; explicit encoding handling is required during INSERT and SELECT.

## Evidence

- [other] At first, a database with a specific layout needs to be created. Here, we use a single mzML file and store each spectrum in a table with 2 columns, one for the identifier and one for the xml element: "At first, a database with a specific layout needs to be created. Here, we use a single mzML file and store each spectrum in a table with 2 columns, one for the identifier and one for the xml element"
- [other] The SQLiteDatabase connector class implements __getitem__(key) to execute SQL queries and return Spectrum or Chromatogram objects parsed from XML elements: "SQLiteDatabase connector class implements __getitem__(key) to execute SQL queries and return Spectrum or Chromatogram objects parsed from XML elements"
- [other] we need to implement a class, which needs to implement the __getitem__ function for random access, and a read function used to sequentiallly read in data for iterating the database.: "we need to implement a class, which needs to implement the __getitem__ function for random access, and a read function used to sequentiallly read in data for iterating the database"
- [other] In order to make pymzML accept other kinds of mzML data (e.g databases), one can implement an own wrapper: "In order to make pymzML accept other kinds of mzML data (e.g databases), one can implement an own wrapper"
- [intro] a new class needs to be written, which implements a `read` and a `__getitem__` function: "a new class needs to be written, which implements a `read` and a `__getitem__` function"
