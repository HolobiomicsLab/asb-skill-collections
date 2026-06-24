---
name: polymorphic-class-dispatch-in-python
description: Use when when you have multiple file format variants (compressed indexed
  gzip, standard gzip, SQLite database, uncompressed mzML) that all need to be read
  via a unified interface, and you want to avoid a long chain of conditional logic
  in client code.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - sqlite3
  - xml.etree.ElementTree
  - pymzML
  license_tier: open
derived_from:
- doi: 10.1093/bioinformatics/bty046
  title: pymzml
evidence_spans:
- import sqlite3 import os from pymzml import spec
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

# polymorphic-class-dispatch-in-python

## Summary

Implement conditional branching logic in a factory method to instantiate the correct file handler class based on file extension and format detection (e.g., .gz with indexed gzip vs. standard gzip, .db for SQLite, or default .mzML). This skill enables a single entry point (FileInterface._open) to transparently route different mzML file formats to their appropriate handler implementations without exposing dispatch logic to callers.

## When to use

When you have multiple file format variants (compressed indexed gzip, standard gzip, SQLite database, uncompressed mzML) that all need to be read via a unified interface, and you want to avoid a long chain of conditional logic in client code. Use this skill when the handler classes share a common interface (e.g., __getitem__ and read methods) but differ in their I/O strategies.

## When NOT to use

- When handler selection is determined by runtime configuration or user choice independent of file content — use a strategy registry or explicit factory parameter instead.
- When file format detection is unreliable or ambiguous (e.g., multiple formats share the same extension) — implement a more robust detection layer before dispatching.
- When handler classes do not share a common interface — refactor the handlers first to ensure polymorphic compatibility.

## Inputs

- file path (string)
- file encoding parameter (string)
- file object or file-like stream (depending on handler)

## Outputs

- file handler instance (IndexedGzip, StandardGzip, SQLiteDatabase, or StandardMzml)
- handler object with __getitem__ and read methods for random and sequential access

## How to apply

Define a factory method (e.g., FileInterface._open) that accepts a file path parameter and sequentially tests file characteristics: first check if the path ends with '.gz', and if so, inspect whether it is an indexed gzip file using format-specific detection (e.g., checking for index metadata); instantiate IndexedGzip or StandardGzip accordingly. Then check for '.db' extension and instantiate SQLiteDatabase. Otherwise, default to StandardMzml for all other paths. Each conditional branch passes the path and encoding parameters to the handler class constructor. This approach isolates format-detection logic in one place, ensures each handler is responsible only for its own I/O semantics, and allows new formats to be added by extending the conditional chain without modifying client code.

## Related tools

- **pymzML** (Provides mzML file parsing and handler classes (IndexedGzip, StandardGzip, StandardMzml, SQLiteDatabase) that are dispatched by the polymorphic factory method) — https://github.com/pymzml/pymzML
- **Python** (Language in which the conditional dispatch logic and handler classes are implemented)
- **sqlite3** (Database module used by SQLiteDatabase handler class for reading spectrum data from .db files)
- **xml.etree.ElementTree** (XML parsing library used by StandardMzml and compressed gzip handlers to parse mzML structure)

## Examples

```
from pymzml.run import Reader
run = Reader('tests/data/BSA1.mzML.gz')
spectrum = run[2540]
```

## Evaluation signals

- Unit test each dispatch branch: call _open with mock files of each type (.mzML, .mzML.gz with index, .mzML.gz without index, .db) and verify the returned object is an instance of the expected handler class.
- Verify that IndexedGzip handler is instantiated only for gzip files with indexed metadata, and StandardGzip for gzip files without indices.
- Integration test: pass dispatched handlers to downstream Reader operations (e.g., spectrum access via __getitem__ or iteration via read) and confirm that spectra are retrieved correctly and consistently regardless of handler type.
- Inspect that the conditional dispatch logic does not leak format-detection details into client code — callers should only invoke FileInterface._open(path) and receive a working handler without knowing which class was instantiated.
- Verify that adding a new file format (e.g., a new .hdf5-based handler) requires only adding one new elif clause in _open without modifying handler interfaces or client code.

## Limitations

- File format detection relies on file extension and metadata inspection; formats with identical extensions or missing/ambiguous metadata may be misclassified.
- The dispatch chain is linear and evaluated sequentially; performance degrades if many format checks are required or if each check is computationally expensive (e.g., reading file headers).
- All handler classes must implement the same interface (__getitem__ for random access, read for sequential access) or callers must handle per-class API differences.
- No changelog or versioning signal available in the source material to document when dispatch rules were added or changed, making long-term maintenance of the dispatch logic potentially fragile.

## Evidence

- [other] The _open method implements conditional dispatch by first checking if the path ends with '.gz' and then inspecting whether it is an indexed gzip file; if indexed it instantiates IndexedGzip, otherwise StandardGzip; for '.db' extensions it instantiates SQLiteDatabase; for all other paths it defaults to StandardMzml.: "if path ends with '.gz', check indexed gzip status and dispatch to `IndexedGzip` or `StandardGzip` accordingly; if path ends with '.db', instantiate `SQLiteDatabase`; otherwise, instantiate"
- [other] Handler classes must implement random-access and sequential-access patterns to support polymorphic use.: "we need to implement a class, which needs to implement the __getitem__ function for random access, and a read function used to sequentiallly read in data"
- [other] File handler registration in FileInterface is achieved by adding conditional elif statements.: "In order to allow pymzML to use this new file class, the filehandler needs to be able to detect when to use this class. The easiest way is, to add another elif statement"
- [intro] The pymzML library provides indexed gzip support for efficient mzML file access.: "One of the features of pymzML is the ability to (create) and read indexed gzip which allows mzML file sizes to reach the levels of the original RAW format"
- [intro] Client code uses a unified Reader interface to access spectra from dispatched handlers.: "spectrum_with_id_2540 = run[ 2540 ]"
