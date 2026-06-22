---
name: database-schema-design-and-implementation
description: Use when when you have an mzML file that you want to store persistently in a queryable format for repeated access, or when memory constraints prevent loading entire mzML files into memory;
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - sqlite3
  - xml.etree.ElementTree
  - pymzML
  - Black
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
---

# database-schema-design-and-implementation

## Summary

Design and implement a SQLite database schema to store mass spectrometry spectrum data indexed by spectrum ID, then integrate it with pymzML's FileInterface to enable random-access and sequential retrieval of Spectrum objects. This skill bridges in-memory mzML parsing with persistent, queryable storage for large MS datasets.

## When to use

When you have an mzML file that you want to store persistently in a queryable format for repeated access, or when memory constraints prevent loading entire mzML files into memory; when you need both random access (by spectrum ID) and sequential iteration over spectra without re-parsing the source file each time.

## When NOT to use

- If the mzML file is small enough to fit in memory and will only be read once or twice (in-memory parsing with pymzML.run.Reader is simpler and faster).
- If you need to modify spectrum data and persist changes (the read-only design of this schema does not support updates or deletions).
- If you require full-text search, complex joins, or queries across multiple spectrum attributes beyond ID-based lookup (a relational schema with normalized CVs and metadata tables would be required).

## Inputs

- mzML file (uncompressed or gzip-compressed with .gz extension)
- target database path (string ending in .db)
- spectrum ID values (integers or string identifiers matching the mzML index)

## Outputs

- SQLite database file (.db) with Spectra table (ID, xml columns)
- SQLiteDatabase instance supporting __getitem__, read(), and get_spectrum_count() methods
- Spectrum or Chromatogram objects retrieved by ID or iteration

## How to apply

First, create a SQLite database with a Spectra table (columns: ID INT, xml TEXT) by iterating through an mzML file using pymzML.run.Reader, converting each spectrum to an XML string, and inserting (spectrum_id, xml_string) tuples. Then implement a SQLiteDatabase class that inherits the FileInterface contract: __init__ establishes a sqlite3 connection; __getitem__(key) executes SELECT queries by spectrum ID and parses the XML string back into a Spectrum or Chromatogram object using xml.etree.ElementTree.XML(); get_spectrum_count() returns SELECT COUNT(*) from the Spectra table; read() sequentially yields XML elements for iteration. Finally, register the class in pymzML's FileInterface._open() by adding an elif statement that detects .db file extensions and instantiates SQLiteDatabase(path, encoding). Verify correctness by confirming db[unique_id] returns a Spectrum object (random access) and iter() yields consistent results (sequential access).

## Related tools

- **pymzML** (Parse mzML files, iterate spectra, and provide FileInterface contract for custom file handlers) — https://github.com/pymzML/pymzML
- **sqlite3** (Python standard library for creating, querying, and managing the SQLite database)
- **xml.etree.ElementTree** (Parse XML element strings from database records back into Python objects)
- **Black** (Code formatter for maintaining consistency in the SQLiteDatabase implementation) — https://github.com/psf/black

## Examples

```
import sqlite3; import pymzml; conn = sqlite3.connect('spectra.db'); cursor = conn.cursor(); cursor.execute('CREATE TABLE spectra (id INT, xml TEXT)'); run = pymzml.run.Reader('input.mzML'); [cursor.execute('INSERT INTO spectra VALUES (?, ?)', (spec.ID, str(spec))) for spec in run]; conn.commit(); db = SQLiteDatabase('spectra.db'); spec_5 = db[5]; print(spec_5['m/z array'])
```

## Evaluation signals

- Verify database file exists and contains a Spectra table with row count matching the number of spectra in the source mzML file (SELECT COUNT(*) = expected count).
- Confirm db[unique_id] for a known spectrum ID returns a Spectrum object (type check) with correct attributes (e.g., ID, m/z array, intensity array).
- Verify random access is O(1) by querying non-sequential spectrum IDs and confirming correctness.
- Iterate through all spectra using iter(db) and confirm the count and order of returned Spectrum objects matches sequential mzML parsing.
- Test that pymzML.run.Reader can transparently instantiate and use SQLiteDatabase by passing a .db file path and verifying reader[id] and for loop iteration both work without raising FileInterface errors.

## Limitations

- The schema stores only spectrum ID and raw XML; querying by metadata attributes (precursor m/z, retention time, MS level) requires either additional columns or re-parsing the XML each time.
- Random access speed depends on SQLite index performance; very large databases (>10 GB) may require careful tuning of connection parameters and PRAGMA settings.
- Spectrum compression (e.g., mzML with base64-encoded m/z/intensity arrays) is preserved in the XML string, so decompression happens at retrieval time, not at database creation time.
- The implementation assumes immutable spectrum data; if source mzML files are updated, the database must be regenerated from scratch.

## Evidence

- [other] Create a SQLite database from an mzML file by parsing each spectrum using pymzML.run.Reader and storing the spectrum ID and XML string representation in a Spectra table with two columns (ID INT, xml TEXT).: "Create a SQLite database from an mzML file by parsing each spectrum using pymzML.run.Reader and storing the spectrum ID and XML string representation in a Spectra table with two columns (ID INT, xml"
- [other] __getitem__ to execute SELECT queries on the Spectra table and return parsed Spectrum or Chromatogram objects using xml.etree.ElementTree.XML parsing: "__getitem__ to execute SELECT queries on the Spectra table and return parsed Spectrum or Chromatogram objects using xml.etree.ElementTree.XML parsing"
- [other] get_spectrum_count to return the total row count from the Spectra table via SELECT COUNT(*): "get_spectrum_count to return the total row count from the Spectra table via SELECT COUNT(*)"
- [other] Modify FileInterface._open to add an elif statement checking for .db file endings and instantiate SQLiteDatabase(path, encoding) as the file_handler.: "Modify FileInterface._open to add an elif statement checking for .db file endings and instantiate SQLiteDatabase(path, encoding) as the file_handler."
- [readme] pymzML is an extension to Python that offers a) easy access to mass spectrometry (MS) data that allows the rapid development of tools: "pymzML is an extension to Python that offers a) easy access to mass spectrometry (MS) data that allows the rapid development of tools"
- [other] In order to make pymzML accept other kinds of mzML data (e.g databases), one can implement an own wrapper: "In order to make pymzML accept other kinds of mzML data (e.g databases), one can implement an own wrapper"
