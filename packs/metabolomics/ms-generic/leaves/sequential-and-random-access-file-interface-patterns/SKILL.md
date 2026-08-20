---
name: sequential-and-random-access-file-interface-patterns
description: Use when when you need to support custom data storage backends (e.g., SQLite, HDF5, or proprietary databases) for mzML-equivalent spectra, but the pymzML parser expects only standard file formats (mzML, mzML.gz, indexed gzip).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - sqlite3
  - ElementTree
  - pymzML
  - ElementTree (xml.etree.ElementTree)
  - black
  techniques:
  - mass-spectrometry
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

# sequential-and-random-access-file-interface-patterns

## Summary

Design and implement dual-mode file interface patterns that support both sequential iteration (via read()) and random access (via __getitem__()) for alternative mass spectrometry data storage backends. This skill enables pymzML to parse spectra from non-standard formats like SQLite databases by abstracting file handling through a polymorphic connector class pattern.

## When to use

When you need to support custom data storage backends (e.g., SQLite, HDF5, or proprietary databases) for mzML-equivalent spectra, but the pymzML parser expects only standard file formats (mzML, mzML.gz, indexed gzip). The trigger is: you have spectrum data in an alternative storage format AND you want to reuse pymzML's parsing logic without modifying the core reader.

## When NOT to use

- Input is already a standard mzML or indexed gzip (.mzML.gz) file — use pymzML's built-in handlers instead.
- You only need sequential access and have no random lookup requirement — a simpler single-method iterator suffices.
- The backend is a relational database and you need full SQL query support — this pattern is optimized for spectrum-by-ID lookups, not complex cross-spectrum filtering.

## Inputs

- Alternative data storage file (e.g., .db SQLite database containing spectrum ID and XML element pairs)
- File path string ending in a custom extension (e.g., '.db')
- Integer index or spectral identifier (for __getitem__ lookups)

## Outputs

- Spectrum or Chromatogram objects (parsed from XML via pymzML.spec)
- Sequential XML strings (returned by read() for iteration)
- Integration with pymzML.Reader and FileInterface._open()

## How to apply

Implement a custom connector class that satisfies two interface requirements: (1) a read() method that returns sequential XML strings for iterative access, and (2) a __getitem__(key) method that parses the XML at a given integer index and returns Spectrum or Chromatogram objects via pymzML's spec module. Store your backend data (e.g., spectrum ID and XML element pairs) in a normalized table structure. Then register the connector in FileInterface._open() by adding an elif clause that detects file extension patterns (e.g., path.endswith('.db')) and instantiates your connector class. The rationale is to preserve pymzML's dual-access semantics: iterating over large files sequentially without loading all spectra into memory (via read()), while also enabling direct spectral lookups by index (via __getitem__()) for tools that need random access.

## Related tools

- **pymzML** (Core parser that defines the dual interface requirement (read() and __getitem__()) and provides Spectrum/Chromatogram object models via spec module; custom connectors integrate via FileInterface._open() dispatch) — https://github.com/pymzml/pymzML
- **sqlite3** (Persistent storage backend for spectrum ID and XML element pairs; enables random access via SQL queries within __getitem__())
- **ElementTree (xml.etree.ElementTree)** (XML parser for converting stored XML strings into ElementTree elements before passing to pymzML's spec module for Spectrum/Chromatogram instantiation)
- **black** (Code formatting and style enforcement for maintained connector code) — https://github.com/psf/black

## Examples

```
from pymzml import Reader; from your_module import SQLiteDatabase; db_handler = SQLiteDatabase('spectra.db'); spectrum = db_handler[0]; for xml_str in db_handler.read(): print(xml_str[:50])
```

## Evaluation signals

- Verify that __getitem__(int_key) returns valid Spectrum or Chromatogram objects with correct m/z, intensity, and metadata fields for integer indices.
- Confirm read() returns sequential, well-formed XML strings that preserve spectrum ID and binary array elements across multiple calls.
- Check that FileInterface._open() correctly detects the custom file extension and instantiates the connector class without fallback to default handlers.
- Validate that iteration over the connector (via read()) and random lookup (via __getitem__) yield consistent spectrum data (same ID and XML content).
- Ensure no data is lost or corrupted during round-trip: store a spectrum in the backend, retrieve it via __getitem__(), and confirm parsed intensity/m/z arrays match the original.

## Limitations

- The pattern assumes spectrum data can be uniquely identified by integer index; non-integer or composite keys require wrapper logic.
- Sequential access via read() returns the entire XML string for each spectrum; for very large spectra, memory usage may spike unless read() is called in a streaming loop.
- Integration into FileInterface._open() via file extension detection is simple but fragile; if multiple backends use the same extension, a more sophisticated MIME-type or magic-byte check is needed.
- The pattern does not handle nested or multi-level data structures (e.g., spectra with multiple precursor ions stored separately); backend schema must be flat or require pre-aggregation.
- Random access performance depends on backend indexing; SQLite without a primary key on spectrum ID will degrade to O(n) lookup, defeating the purpose of __getitem__().

## Evidence

- [other] The SQLiteDatabase connector class implements __getitem__(key) to execute SQL queries and return Spectrum or Chromatogram objects parsed from XML elements: "The SQLiteDatabase connector class implements __getitem__(key) to execute SQL queries and return Spectrum or Chromatogram objects parsed from XML elements"
- [intro] a new class needs to be written, which implements a `read` and a `__getitem__` function: "a new class needs to be written, which implements a `read` and a `__getitem__` function"
- [other] the filehandler needs to be able to detect when to use this class. The easiest way is, to add another elif statement which decides which handler: "the filehandler needs to be able to detect when to use this class. The easiest way is, to add another elif statement which decides which handler"
- [other] In order to make pymzML accept other kinds of mzML data (e.g databases), one can implement an own wrapper: "In order to make pymzML accept other kinds of mzML data (e.g databases), one can implement an own wrapper"
- [intro] parse the data blockwise, so every piece of data, which should be accessible by indexing is written in one go. The index used can be either an integer or a string: "parse the data blockwise, so every piece of data, which should be accessible by indexing is written in one go. The index used can be either an integer or a string"
