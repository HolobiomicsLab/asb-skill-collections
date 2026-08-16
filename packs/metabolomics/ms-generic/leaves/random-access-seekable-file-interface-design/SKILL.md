---
name: random-access-seekable-file-interface-design
description: Use when you have a large mzML file or text corpus (e.g., Moby Dick, proteomics run) stored in compressed or database format and need to retrieve specific spectra or chapters by ID without sequential iteration or full decompression.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - sqlite3
  - xml.etree.ElementTree
  - pymzML
  - Python
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

# random-access-seekable-file-interface-design

## Summary

Design and implement a custom file wrapper class that enables random-access seeking into compressed or database-backed spectral data files by implementing indexed block structure with __getitem__, read(), and spectrum count methods. This skill is essential when standard mzML parsers must support chapter/spectrum-level random access on files too large for full decompression.

## When to use

Apply this skill when you have a large mzML file or text corpus (e.g., Moby Dick, proteomics run) stored in compressed or database format and need to retrieve specific spectra or chapters by ID without sequential iteration or full decompression. Use this specifically when the pymzML reader must support indexed gzip (.gz) files or custom storage backends that require custom file interface registration.

## When NOT to use

- Input file is already in uncompressed mzML format with native index support — use pymzML.run.Reader() directly without custom wrapper.
- Spectral data is small enough to fit in memory — wrapper adds complexity and overhead relative to simple in-memory parsing.
- Analysis requires sequential-only access to all spectra with no random seeks — standard sequential mzML parsing is simpler and faster.

## Inputs

- mzML file (raw or gzip-compressed)
- sqlite3 database with spectrum/chapter metadata (ID, xml TEXT columns)
- Spectral or textual data requiring chapter-level or spectrum-level indexing

## Outputs

- Indexed gzip file (.gz) with chapter/spectrum offsets in header
- Custom file wrapper instance registered in FileInterface
- Random-access capable mzML reader instance

## How to apply

Implement a wrapper class with three essential methods: (1) __getitem__(key) to retrieve a spectrum or chapter by ID from the underlying storage (database or compressed block) and convert to igzip-compatible block format; (2) read(size=-1) to sequentially iterate through spectra/chapters for linear access; (3) get_spectrum_count() to return the total number of spectra or chapters. Store spectrum metadata (ID, offset, content) in a sqlite3 database with two columns (ID for spectrum/chapter number, xml TEXT for content as string). Construct an indexed .gz file header containing ID bytes, version, index length, and offset length fields, followed by spectrum-to-offset mappings terminated by a zero byte. Register the wrapper class in FileInterface._open() via an elif statement that detects the underlying storage type (e.g., .db file extension) and instantiates the wrapper. Validate by retrieving specific spectra via wrapper[spectrum_id] and verifying sequential iteration via for loop over the wrapper instance.

## Related tools

- **pymzML** (Parser and random-access framework into which custom file wrappers are registered via FileInterface._open(); provides Reader class and igzip-compatible block compression/decompression infrastructure) — https://github.com/pymzml/pymzML
- **sqlite3** (Underlying storage backend for spectrum/chapter metadata; provides CREATE TABLE, INSERT, and SELECT queries for indexed lookup by spectrum ID)
- **xml.etree.ElementTree** (Parsing and serialization of spectrum XML content stored in the sqlite3 database TEXT column)
- **Python** (Language for implementing the wrapper class, database connection, and FileInterface registration logic)
- **black** (Code formatting tool for ensuring consistent style in wrapper class implementation (referenced in pymzML contribution guidelines)) — https://github.com/psf/black

## Examples

```
db = SQLiteDatabase('test.db'); my_spec = db[5]; for spectrum in db: print(spectrum['ms level']); count = db.get_spectrum_count()
```

## Evaluation signals

- Random access retrieval of a specific spectrum by ID (e.g., run[2540]) returns the correct spectrum XML without reading preceding spectra.
- Sequential iteration via for loop over wrapper instance yields spectra in order with correct ms level and metadata.
- File header contains ID bytes (0x1f, 0x8b), version, index length, and offset length fields followed by spectrum-to-offset mappings terminated by zero byte.
- get_spectrum_count() returns the total spectrum count matching the number of rows in the sqlite3 database.
- FileInterface._open() correctly detects .db file extension and instantiates the custom wrapper class without FileNotFoundError or AttributeError.

## Limitations

- Wrapper class requires manual implementation of __getitem__, read(), and get_spectrum_count() methods — no automatic code generation.
- SQLite3 lookup performance degrades with very large databases (millions of spectra); index optimization or alternative backends (e.g., HDF5) may be required.
- Custom regex patterns may be needed to parse non-standard mzML index identifiers (e.g., 'scan=1' format) when initializing the reader.
- File size must remain within gzip constraints; very large indexed gzip files may require chunked writing and index refresh strategies not covered here.

## Evidence

- [other] In order to make pymzML accept other kinds of mzML data (e.g databases), one can implement an own wrapper: "In order to make pymzML accept other kinds of mzML data (e.g databases), one can implement an own wrapper"
- [other] After this, we need to implement a class, which needs to implement the __getitem__ function for random access, and a read function used to sequentiallly read in data: "After this, we need to implement a class, which needs to implement the __getitem__ function for random access, and a read function used to sequentiallly read in data"
- [other] def get_spectrum_count(self): self.cursor.execute("SELECT COUNT(*) from spectra"): "def get_spectrum_count(self): self.cursor.execute("SELECT COUNT(*) from spectra")"
- [abstract] pymzML is an extension to Python that offers a) easy access to mass spectrometry (MS) data that allows the rapid development of tools b) a very fast parser for mzML data, the standard mass spectrometry data format c) a set of functions to compare and/or handle spectra d) random access in compressed files e) interactive data visualization: "pymzML is an extension to Python that offers ... d) random access in compressed files"
- [intro] One of the features of pymzML is the ability to (create) and read indexed gzip which allows mzML file sizes to reach the levels of the original RAW format: "One of the features of pymzML is the ability to (create) and read indexed gzip which allows mzML file sizes to reach the levels of the original RAW format"
- [intro] spectrum_with_id_2540 = run[ 2540 ]: "spectrum_with_id_2540 = run[ 2540 ]"
- [other] In order to allow pymzML to use this new file class, the filehandler needs to be able to detect when to use this class. The easiest way is, to add another elif statement: "In order to allow pymzML to use this new file class, the filehandler needs to be able to detect when to use this class. The easiest way is, to add another elif statement"
