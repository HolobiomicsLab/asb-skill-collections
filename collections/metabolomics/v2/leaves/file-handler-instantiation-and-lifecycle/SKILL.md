---
name: file-handler-instantiation-and-lifecycle
description: Use when you need to open an mzML file in pymzML and must automatically
  select the correct handler based on file extension (.mzML, .mzML.gz, .db) and—for
  gzip files—indexed vs. non-indexed compression status. Use it whenever FileInterface.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - sqlite3
  - xml.etree.ElementTree
  - pymzML
  - Python
  techniques:
  - mass-spectrometry
  license_tier: open
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

# file-handler-instantiation-and-lifecycle

## Summary

Instantiate and manage file handler objects in pymzML by conditionally dispatching to specialized classes (IndexedGzip, StandardGzip, SQLiteDatabase, StandardMzml) based on file extension and compression metadata. This skill enables transparent support for multiple mzML file formats and storage backends within a unified Reader interface.

## When to use

Apply this skill when you need to open an mzML file in pymzML and must automatically select the correct handler based on file extension (.mzML, .mzML.gz, .db) and—for gzip files—indexed vs. non-indexed compression status. Use it whenever FileInterface._open receives a file path and must route to the appropriate handler class without manual caller specification.

## When NOT to use

- File path is already an open file object or stream—pass the handler directly instead of re-instantiating.
- Input file format is not mzML (e.g., raw proprietary MS formats or non-mass-spectrometry data)—use format-specific readers instead.
- Handler lifecycle is managed externally (e.g., context manager or factory already instantiated the handler)—avoid double instantiation.

## Inputs

- File path (string) with .mzML, .mzML.gz, or .db extension
- Indexed gzip metadata (presence/absence of index structure in .gz file)
- Encoding specification (optional parameter, e.g., UTF-8)

## Outputs

- File handler instance (IndexedGzip, StandardGzip, SQLiteDatabase, or StandardMzml)
- Handler object with __getitem__, read, and get_spectrum_count methods bound to the input file

## How to apply

Implement the _open method in FileInterface to accept a file path parameter and inspect its extension and compression metadata. First check if the path ends with '.gz': if true, inspect whether the gzip is indexed (using indexed gzip detection logic) and instantiate IndexedGzip or StandardGzip accordingly; if the path ends with '.db', instantiate SQLiteDatabase; otherwise, instantiate StandardMzml as the default handler. Pass the path and encoding parameters to each handler's constructor. The dispatch logic should be deterministic and testable by calling _open with mock files of each type and verifying the returned instance type matches the expected handler class. For each successful dispatch, the handler object becomes available for downstream Reader operations (spectrum retrieval by index, sequential iteration) and should implement __getitem__ for random access and read for sequential data access.

## Related tools

- **pymzML** (Provides FileInterface class, _open dispatch method, and handler classes (IndexedGzip, StandardGzip, SQLiteDatabase, StandardMzml) for conditional file format routing) — https://github.com/pymzml/pymzML
- **Python** (Runtime environment and standard library (os.path for extension inspection, encoding parameter support))
- **sqlite3** (Database backend for SQLiteDatabase handler instantiation and spectrum table access)
- **xml.etree.ElementTree** (XML parsing used internally by StandardMzml and IndexedGzip handlers to deserialize spectrum data)

## Examples

```
from pymzml import run; handler = pymzml.FileInterface()._open('tests/data/BSA1.mzML.gz'); spectrum = handler[2540]
```

## Evaluation signals

- Unit test: call _open with a mock .mzML file and verify returned instance is StandardMzml.
- Unit test: call _open with a mock .mzML.gz file containing an index and verify returned instance is IndexedGzip.
- Unit test: call _open with a mock .mzML.gz file without an index and verify returned instance is StandardGzip.
- Unit test: call _open with a mock .db file and verify returned instance is SQLiteDatabase.
- Integration test: pass the returned handler to Reader operations (e.g., run[2540] for indexed access, iteration via for spectrum in run) and confirm spectrum retrieval succeeds without error.

## Limitations

- File extension detection is literal (checks string suffix) and will fail silently on paths with uppercase .GZ or .DB extensions unless extension checking is case-insensitive.
- Indexed gzip detection requires that the .gz file contains valid index metadata; corrupted or malformed indices may cause IndexedGzip instantiation to fail or fall back to sequential reading.
- SQLiteDatabase handler assumes the database schema and table layout match pymzML conventions (spectra table with specific columns); custom database structures will require custom wrapper implementations.
- No automatic fallback or retry: if instantiation fails (e.g., file not found, permission denied), the exception propagates directly; caller must handle error recovery.

## Evidence

- [other] The _open method implements conditional dispatch by first checking if the path ends with '.gz' and then inspecting whether it is an indexed gzip file; if indexed it instantiates IndexedGzip, otherwise StandardGzip; for '.db' extensions it instantiates SQLiteDatabase; for all other paths it defaults to StandardMzml.: "The _open method implements conditional dispatch by first checking if the path ends with '.gz' and then inspecting whether it is an indexed gzip file; if indexed it instantiates IndexedGzip,"
- [intro] One of the features of pymzML is the ability to (create) and read indexed gzip which allows mzML file sizes to reach the levels of the original RAW format: "One of the features of pymzML is the ability to (create) and read indexed gzip which allows mzML file sizes to reach the levels of the original RAW format"
- [other] In order to allow pymzML to use this new file class, the filehandler needs to be able to detect when to use this class. The easiest way is, to add another elif statement: "In order to allow pymzML to use this new file class, the filehandler needs to be able to detect when to use this class. The easiest way is, to add another elif statement"
- [other] After this, we need to implement a class, which needs to implement the __getitem__ function for random access, and a read function used to sequentiallly read in data: "After this, we need to implement a class, which needs to implement the __getitem__ function for random access, and a read function used to sequentiallly read in data"
- [readme] pymzML is an extension to Python that offers a) easy access to mass spectrometry (MS) data that allows the rapid development of tools b) a very fast parser for mzML data, the standard mass spectrometry data format: "pymzML is an extension to Python that offers a) easy access to mass spectrometry (MS) data that allows the rapid development of tools b) a very fast parser for mzML data, the standard mass"
