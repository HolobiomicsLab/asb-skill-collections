---
name: mzml-data-access-abstraction
description: Use when when building or extending a mass spectrometry data parser that must support multiple mzML storage formats (plain .mzML, indexed .mzML.gz, standard-compressed .mzML.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - sqlite3
  - xml.etree.ElementTree
  - pymzML
  - Python (standard library)
derived_from:
- doi: 10.1093/bioinformatics/bty046
  title: pymzml
evidence_spans:
- import sqlite3
- import xml.etree.ElementTree as et
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pymzml
    doi: 10.1093/bioinformatics/bty046
    title: pymzml
  dedup_kept_from: coll_pymzml
schema_version: 0.2.0
---

# mzML Data Access Abstraction

## Summary

Implement a polymorphic file handler interface (FileInterface) that dispatches mzML file reads to specialized handler classes based on file extension and compression format, enabling unified random-access parsing across uncompressed, indexed-gzip, standard-gzip, and SQLite-backed mzML data sources. This abstraction decouples Reader logic from storage format, permitting extensible support for new backends without modifying core parsing code.

## When to use

When building or extending a mass spectrometry data parser that must support multiple mzML storage formats (plain .mzML, indexed .mzML.gz, standard-compressed .mzML.gz, and database-backed variants) and you need to route file open calls to the correct handler class without duplicating spectrum retrieval logic or embedding format detection throughout the codebase.

## When NOT to use

- Input is already parsed into an in-memory spectrum list or Spectrum object tree — use data access directly instead of re-opening the file.
- The mzML file format and its variants are not the data source (e.g., raw Bruker .d or Thermo .RAW files) — use vendor-specific readers.
- Random access is not required and sequential streaming is sufficient — the overhead of detecting and instantiating a handler may not be justified.

## Inputs

- file_path (str): filesystem path to an mzML file or database
- encoding (str, optional): character encoding for XML parsing (default typically 'utf-8')
- file_object (file-like, optional): for in-memory or remote data sources

## Outputs

- handler_instance: one of {IndexedGzip, StandardGzip, SQLiteDatabase, StandardMzml} — any class implementing __getitem__ and read()
- spectrum_data: dict or Spectrum object retrieved via handler[spectrum_id] or sequential iteration

## How to apply

Define a FileInterface._open(path, encoding) method that inspects the file path extension and internal format markers to conditionally instantiate the appropriate handler. Check path.endswith('.gz'), then inspect whether the gzip stream contains an index (indexed gzip signature); if so, instantiate IndexedGzip, else StandardGzip. For path.endswith('.db'), instantiate SQLiteDatabase. For all other paths, default to StandardMzml. Each handler class must implement __getitem__(spectrum_id) for random access and read() for sequential iteration. The Reader class then calls FileInterface._open() once during initialization and delegates all spectrum access to the returned handler, remaining agnostic to the underlying storage format. This pattern allows future handlers (e.g., HDF5, network-streamed mzML) to be added by implementing the handler interface and adding a new elif branch.

## Related tools

- **pymzML** (provides the Reader and mzML parsing infrastructure that calls FileInterface._open() to obtain a handler; implements StandardMzml, IndexedGzip, StandardGzip handlers) — https://github.com/pymzml/pymzML
- **sqlite3** (backend for SQLiteDatabase handler to store and retrieve spectra from a relational database)
- **xml.etree.ElementTree** (parses XML structure within mzML files to extract spectrum metadata and peak data)
- **Python (standard library)** (file I/O, gzip module for indexed gzip detection and decompression) — https://www.python.org

## Examples

```
run = pymzml.run.Reader('tests/data/BSA1.mzML.gz'); spectrum_2540 = run[2540]
```

## Evaluation signals

- Unit test: call FileInterface._open() with a .mzML file and confirm returned handler is instance of StandardMzml; repeat for .mzML.gz (indexed), .mzML.gz (non-indexed), and .db files, verifying correct handler type in each case.
- Integration test: call Reader(path) for each file type and confirm spectrum retrieval (e.g., spectrum = run[2540]) returns consistent Spectrum objects regardless of backend.
- Verify random access: instantiate handler and call handler[spectrum_id] for non-sequential IDs (e.g., [2540, 100, 5000]) and confirm results match sequential iteration in the same file.
- Mock test: replace actual file with a mock path that triggers each conditional branch (_open inspects path.endswith('.gz'), gzip index check, .db check, default) and assert the correct handler class was instantiated in each branch.
- Extension test: implement a custom handler class (e.g., HDF5File), add elif branch to _open, and verify Reader can use it without changes to downstream spectrum access code.

## Limitations

- Handler dispatch is based purely on filename extension and internal format detection (gzip index signature); if file extensions are non-standard or misnamed, dispatch will fail or route to the wrong handler.
- IndexedGzip requires an explicit index appended to the .gz file; mzML files compressed with standard gzip tools without the indexed-gzip format will be handled as StandardGzip (slower random access).
- SQLiteDatabase handler requires manual database creation and population from mzML before Reader can use it; there is no automatic .mzML → .db conversion in FileInterface.
- No built-in fallback or retry logic if a handler fails to open a file; errors (e.g., corrupted index, missing database) propagate directly to the caller.
- Custom regex patterns for non-standard index identifiers (scan=1 vs. scan=01) must be set on Reader initialization, not at FileInterface level, limiting flexibility for mixed-format batches.

## Evidence

- [other] The _open method implements conditional dispatch by first checking if the path ends with '.gz' and then inspecting whether it is an indexed gzip file; if indexed it instantiates IndexedGzip, otherwise StandardGzip; for '.db' extensions it instantiates SQLiteDatabase; for all other paths it defaults to StandardMzml.: "the _open method implements conditional dispatch by first checking if the path ends with '.gz' and then inspecting whether it is an indexed gzip file; if indexed it instantiates IndexedGzip,"
- [intro] One of the features of pymzML is the ability to (create) and read indexed gzip which allows mzML file sizes to reach the levels of the original RAW format: "One of the features of pymzML is the ability to (create) and read indexed gzip which allows mzML file sizes to reach the levels of the original RAW format"
- [intro] pymzML can also rapidly seek into any uncompressed mzML file, no matter if an index was included into the file or not: "pymzML can also rapidly seek into any uncompressed mzML file, no matter if an index was included into the file or not"
- [other] In order to allow pymzML to use this new file class, the filehandler needs to be able to detect when to use this class. The easiest way is, to add another elif statement: "In order to allow pymzML to use this new file class, the filehandler needs to be able to detect when to use this class. The easiest way is, to add another elif statement"
- [other] After this, we need to implement a class, which needs to implement the __getitem__ function for random access, and a read function used to sequentiallly read in data: "After this, we need to implement a class, which needs to implement the __getitem__ function for random access, and a read function used to sequentiallly read in data"
