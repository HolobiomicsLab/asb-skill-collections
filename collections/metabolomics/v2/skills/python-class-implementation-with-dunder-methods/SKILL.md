---
name: python-class-implementation-with-dunder-methods
description: Use when you have mzML spectral data stored in a non-standard format (SQLite database, custom binary store, or indexed archive) and need pymzML's Reader to parse and iterate over spectra as if they were in native mzML files. Specifically, when FileInterface.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0335
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - sqlite3
  - Python
  - ElementTree
  - pymzML
  - black
derived_from:
- doi: 10.1093/bioinformatics/bty046
  title: pymzml
evidence_spans:
- import sqlite3
- import sqlite3 import os from pymzml import spec
- Module to parse mzML data in Python
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# python-class-implementation-with-dunder-methods

## Summary

Implement custom Python classes with dunder methods (__getitem__, __init__, read) to enable random and sequential access to mzML spectral data stored in alternative formats (SQLite databases, compressed files). This skill bridges data storage backends with pymzML's Reader interface by defining the protocol through which the library retrieves spectra on demand.

## When to use

You have mzML spectral data stored in a non-standard format (SQLite database, custom binary store, or indexed archive) and need pymzML's Reader to parse and iterate over spectra as if they were in native mzML files. Specifically, when FileInterface._open() must dispatch file paths to a custom handler that implements both random access (by spectrum ID) and sequential iteration.

## When NOT to use

- Input is already a native .mzML or .mzML.gz file — use pymzML's built-in parser instead
- You do not need random access — streaming a single pass through sequential data may not justify the implementation overhead
- The storage backend does not support indexed or keyed retrieval — the class requires both __getitem__ and read methods

## Inputs

- SQLite database file (.db) containing spectrum IDs and XML element strings in a 'Spectra' table
- File path string (detected by extension)
- Integer or string spectrum identifiers (keys)

## Outputs

- Spectrum or Chromatogram objects (from pymzML spec module)
- XML element strings (from read() method for sequential access)
- File handler object integrated into pymzML's FileInterface

## How to apply

Define a custom class (e.g., SQLiteDatabase) that implements three dunder methods: (1) __init__(filepath) to open and cache the underlying storage connection; (2) __getitem__(key) to retrieve individual Spectrum or Chromatogram objects by integer index or string spectrum ID, parsing XML elements from storage and constructing spec module objects; (3) read() to yield sequential XML strings for iteration during normal file traversal. Parse XML strings using ElementTree to convert database-stored elements into pymzML spectrum objects. Finally, modify FileInterface._open() to detect the file format (e.g., check path.endswith('.db')) and instantiate your custom class instead of the default mzML handler, routing the file_handler assignment accordingly.

## Related tools

- **pymzML** (Provides Reader, spec module, and FileInterface dispatcher that the custom class integrates with) — https://github.com/pymzml/pymzML
- **sqlite3** (Built-in Python library to query and retrieve spectral XML from the database backend)
- **ElementTree** (Parses XML strings retrieved from storage into XML elements for spectrum construction)
- **black** (Code formatting standard used in pymzML project for style consistency) — https://github.com/psf/black

## Examples

```
from pymzml import Reader; import sqlite3; r = Reader('spectra.db'); spectra = [spec for spec in r]; print(f'Loaded {len(spectra)} spectra from database')
```

## Evaluation signals

- Instantiate the custom class with a test .db file and verify __getitem__(0) returns a valid Spectrum or Chromatogram object with correct ID and m/z–intensity pairs
- Call read() sequentially and confirm it yields all spectrum XML strings in the database without duplication
- Confirm FileInterface._open() correctly detects the .db extension and routes to the custom class (trace via isinstance checks or file_handler type)
- Iterate over pymzML.Reader(db_path) and verify spectrum count matches the database table row count
- Check that spectrum metadata (scan time, mass range, precursor m/z) parsed from XML matches the original mzML file

## Limitations

- Performance depends on database query efficiency and storage I/O; random access is only as fast as the underlying database index
- XML parsing adds memory overhead for large spectra; very large XML elements may exceed available RAM during element construction
- The class must implement both __getitem__ and read methods — incomplete implementations will fail pymzML iteration or indexing workflows
- File format detection in FileInterface._open() is extension-based; databases with non-.db extensions will not be routed to the custom handler

## Evidence

- [intro] a new class needs to be written, which implements a `read` and a `__getitem__` function: "a new class needs to be written, which implements a `read` and a `__getitem__` function"
- [other] __getitem__ should parse XML and return Spectrum or Chromatogram objects via pymzML's spec module: "__getitem__ should parse XML and return Spectrum or Chromatogram objects"
- [other] Add an elif clause to FileInterface._open() that detects '.db' file extensions and instantiates SQLiteDatabase: "Add an elif clause to FileInterface._open() that detects '.db' file extensions and instantiates SQLiteDatabase"
- [other] In order to make pymzML accept other kinds of mzML data (e.g databases), one can implement an own wrapper: "In order to make pymzML accept other kinds of mzML data (e.g databases), one can implement an own wrapper"
- [readme] pymzML is an extension to Python that offers a very fast parser for mzML data, the standard mass spectrometry data format: "pymzML is an extension to Python that offers a very fast parser for mzML data, the standard mass spectrometry data format"
