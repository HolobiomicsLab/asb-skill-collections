---
name: mass-spectrometry-data-object-instantiation
description: Use when when you have mass spectrometry data stored in non-standard
  formats (SQLite, HDF5, custom binary) that pymzML does not natively support, and
  you want to enable random-access and sequential parsing of spectra without converting
  to mzML first.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - sqlite3
  - ElementTree
  - pymzML
  - black
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

# mass-spectrometry-data-object-instantiation

## Summary

Implement a custom file handler class that wraps mass spectrometry data stored in alternative formats (e.g., SQLite databases) by implementing the `__getitem__()` and `read()` interface methods, then register it with pymzML's FileInterface to enable transparent spectrum/chromatogram object construction during parsing.

## When to use

When you have mass spectrometry data stored in non-standard formats (SQLite, HDF5, custom binary) that pymzML does not natively support, and you want to enable random-access and sequential parsing of spectra without converting to mzML first. Triggers include: file extension not recognized by FileInterface, need for database-backed storage to reduce file size, or requirement for indexed access patterns incompatible with direct mzML parsing.

## When NOT to use

- Input data is already in standard mzML or mzML.gz format — use pymzML's built-in parser directly.
- Data store does not have stable, queryable spectrum indexing — the handler requires predictable key-to-record mapping.
- Performance-critical application requiring sub-millisecond spectrum access — database queries may introduce latency compared to indexed gzip seeking.

## Inputs

- SQLite database file (.db) or alternative data store with indexed spectrum records
- File path string pointing to the data store
- Spectrum ID (integer or string key) for random access

## Outputs

- Spectrum object (pymzML.spec.Spectrum) or Chromatogram object (pymzML.spec.Chromatogram)
- XML string representation of spectrum metadata and data
- Integer count of spectra in the data store

## How to apply

First, create or populate a data store (e.g., SQLite database with a 'Spectra' table containing spectrum ID and XML element columns) from an existing mzML file using sqlite3. Second, implement a connector class with `__init__` (accepting file path), `__getitem__(key)` (executing queries and parsing XML strings into Spectrum or Chromatogram objects via pymzML.spec), `get_spectrum_count()` returning the total number of entries, and `read()` returning XML strings sequentially. Import ElementTree to parse XML retrieved from the store into Element objects. Third, modify FileInterface._open() to add an elif clause that detects the target file extension (e.g., `path.endswith('.db')`) and instantiates your connector class, assigning the instance to the file_handler variable. Finally, instantiate pymzML.Reader with a path to the new format; it will dispatch to your handler transparently.

## Related tools

- **pymzML** (Parsing framework; provides spec module for Spectrum/Chromatogram object construction and FileInterface dispatch logic) — https://github.com/pymzml/pymzML
- **sqlite3** (Creating and querying the spectrum data store; retrieving indexed XML elements)
- **ElementTree** (Parsing XML strings retrieved from the database into Element objects for spectrum construction)
- **black** (Code style enforcement for maintaining consistent formatting in the connector class implementation) — https://github.com/psf/black

## Examples

```
from pymzml import run; import sqlite3; conn = sqlite3.connect('spectra.db'); conn.execute('CREATE TABLE Spectra (id TEXT, xml TEXT)'); run(Reader('spectra.db'))
```

## Evaluation signals

- FileInterface._open() successfully routes .db file paths to the new handler class without raising KeyError or AttributeError.
- Calling `handler[0]` and `handler[1]` returns valid pymzML Spectrum or Chromatogram objects with populated m/z and intensity arrays.
- Sequential iteration via repeated `read()` calls returns non-empty XML strings in order, covering all spectra in the store.
- `get_spectrum_count()` matches the row count of the underlying data store (SELECT COUNT(*) FROM Spectra).
- pymzML.Reader instantiated with the .db file path successfully iterates spectra and produces identical m/z values compared to parsing the source mzML file directly.

## Limitations

- Database query latency may degrade performance for interactive visualization or real-time processing compared to native indexed gzip access.
- The handler assumes a fixed schema (spectrum ID and XML element columns); custom data stores with different layouts require rewriting __getitem__ and read() logic.
- No built-in support for partial spectrum loading or streaming; __getitem__ must reconstruct the entire Spectrum object on each access.
- XML parsing via ElementTree requires the full XML string to be in memory; very large spectra or chromatograms may cause memory overhead.

## Evidence

- [other] The SQLiteDatabase connector class implements __getitem__(key) to execute SQL queries and return Spectrum or Chromatogram objects parsed from XML elements: "The SQLiteDatabase connector class implements __getitem__(key) to execute SQL queries and return Spectrum or Chromatogram objects"
- [other] FileInterface._open() function dispatches .db file paths via an elif condition checking path.endswith('.db'): "FileInterface._open() function dispatches .db file paths to this handler via an elif condition checking path.endswith('.db')"
- [intro] a new class needs to be written, which implements a `read` and a `__getitem__` function: "a new class needs to be written, which implements a `read` and a `__getitem__` function"
- [other] In order to make pymzML accept other kinds of mzML data (e.g databases), one can implement an own wrapper: "In order to make pymzML accept other kinds of mzML data (e.g databases), one can implement an own wrapper"
- [other] a read function used to sequentially read in data for iterating the database. In this simple approach, the read function always returns a whole spectra xml string: "a read function used to sequentially read in data for iterating the database. In this simple approach, the read function always returns a whole spectra xml string"
- [other] Create a SQLite database from an mzML file using sqlite3, storing spectrum ID and XML element pairs in a 'Spectra' table with two columns: "Create a SQLite database from an mzML file using sqlite3, storing spectrum ID and XML element pairs in a 'Spectra' table with two columns"
