---
name: file-format-detection-by-extension
description: Use when when building a file I/O abstraction layer that must support
  multiple serialization formats (e.g., uncompressed mzML, gzip-compressed mzML, indexed
  gzip mzML, or SQLite-backed mzML) and route each to its correct handler class without
  exposing format logic to downstream consumers.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - sqlite3
  - xml.etree.ElementTree
  - pymzML
  techniques:
  - mass-spectrometry
  license_tier: restricted
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

# file-format-detection-by-extension

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Conditionally dispatch file handlers to appropriate parser classes based on file extension and format-specific metadata (e.g., indexed gzip status). This skill enables polymorphic file handling in mass spectrometry data pipelines, allowing a single Reader interface to transparently support mzML, compressed gzip, indexed gzip, and SQLite database backends.

## When to use

When building a file I/O abstraction layer that must support multiple serialization formats (e.g., uncompressed mzML, gzip-compressed mzML, indexed gzip mzML, or SQLite-backed mzML) and route each to its correct handler class without exposing format logic to downstream consumers. Specifically apply this skill when you have polymorphic file sources with different file extensions (.mzML, .mzML.gz, .db) and need to instantiate the correct handler transparently.

## When NOT to use

- The input file format is already known and fixed at design time; use direct instantiation instead of dispatch.
- File extension is unreliable or absent (e.g., extensionless pipes or streams); use content-based format detection (magic bytes) instead.
- The handler classes have incompatible APIs; ensure all handlers implement the same interface (__getitem__, read, get_spectrum_count) before applying this skill.

## Inputs

- file path (str)
- file extension (.mzML, .mzML.gz, .db)
- file header bytes (for indexed gzip detection)

## Outputs

- file handler instance (IndexedGzip | StandardGzip | SQLiteDatabase | StandardMzml)

## How to apply

Implement a dispatcher method (e.g., FileInterface._open) that inspects the file path extension and optional file-specific metadata to determine the handler class to instantiate. First check if the path ends with '.gz'; if so, read the file header or opening bytes to distinguish between indexed gzip (instantiate IndexedGzip) and standard gzip (instantiate StandardGzip). If the path ends with '.db', instantiate SQLiteDatabase. Otherwise, default to StandardMzml. Pass the file path and any encoding parameters to the selected handler constructor. This avoids conditional branching in downstream code and centralizes format detection logic, making it easy to register new formats by adding additional elif branches.

## Related tools

- **pymzML** (Provides Reader interface and file handler classes (IndexedGzip, StandardGzip, SQLiteDatabase, StandardMzml); dispatching logic registers handlers in FileInterface._open method.) — https://github.com/pymzml/pymzML
- **sqlite3** (Database backend for SQLiteDatabase handler; enables spectrum storage and retrieval by ID from .db files.)
- **xml.etree.ElementTree** (XML parsing for mzML file structure inspection; used by StandardMzml handler to parse spectrum metadata.)

## Examples

```
from pymzml.file_interface import FileInterface; handler = FileInterface._open('sample.mzML.gz'); spectrum = handler[0]
```

## Evaluation signals

- Instantiate _open with mock files of each supported type (.mzML, .mzML.gz indexed, .mzML.gz standard, .db) and verify the returned handler is an instance of the expected class via isinstance().
- Call the returned handler's __getitem__ method (random access) and read() method (sequential iteration) and verify they return valid Spectrum objects with non-empty m/z and intensity arrays.
- For .db files, confirm that get_spectrum_count() returns the correct number of spectra and that db[spectrum_id] retrieves the same spectrum independently multiple times.
- Pass dispatched handlers to downstream Reader operations (e.g., iteration, filtering) and verify spectrum retrieval correctness by comparing m/z values or retention times against known reference data.
- Verify that dispatch logic correctly detects indexed gzip by reading the file header (ID bytes, version, index length fields) and does not misclassify standard gzip as indexed.

## Limitations

- Extension-based detection fails for files without standard extensions or for data in non-standard containers; content-based detection (magic bytes) is more robust but slower.
- Indexed gzip detection requires reading and parsing the file header, adding I/O overhead at dispatch time; cache the detected format if the same file is opened multiple times.
- The dispatcher assumes handler classes share a common interface (__getitem__, read, get_spectrum_count); if a new handler has a different API, the dispatcher must be updated and downstream code may break.
- SQLiteDatabase handler is specific to spectrum data stored in a single table with (ID, xml TEXT) columns; schema changes or multi-table designs require custom wrapper implementations.

## Evidence

- [other] if path ends with '.gz', check indexed gzip status and dispatch to IndexedGzip or StandardGzip accordingly; if path ends with '.db', instantiate SQLiteDatabase; otherwise, instantiate StandardMzml: "if path ends with '.gz', check indexed gzip status and dispatch to `IndexedGzip` or `StandardGzip` accordingly; if path ends with '.db', instantiate `SQLiteDatabase`; otherwise, instantiate"
- [other] In order to allow pymzML to use this new file class, the filehandler needs to be able to detect when to use this class. The easiest way is, to add another elif statement: "In order to allow pymzML to use this new file class, the filehandler needs to be able to detect when to use this class. The easiest way is, to add another elif statement"
- [other] The _open method implements conditional dispatch by first checking if the path ends with '.gz' and then inspecting whether it is an indexed gzip file: "The _open method implements conditional dispatch by first checking if the path ends with '.gz' and then inspecting whether it is an indexed gzip file"
- [readme] pymzML is an extension to Python that offers a) easy access to mass spectrometry (MS) data that allows the rapid development of tools b) a very fast parser for mzML data, the standard mass spectrometry data format: "pymzML is an extension to Python that offers a) easy access to mass spectrometry (MS) data that allows the rapid development of tools b) a very fast parser for mzML data"
- [other] In order to make pymzML accept other kinds of mzML data (e.g databases), one can implement an own wrapper: "In order to make pymzML accept other kinds of mzML data (e.g databases), one can implement an own wrapper"
