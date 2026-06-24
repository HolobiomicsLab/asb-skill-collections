---
name: file-format-dispatch-and-handler-routing
description: Use when you have a parser library that must support multiple file formats
  (e.g., mzML, SQLite, compressed gzip) and want to avoid conditional logic scattered
  throughout the parsing code.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
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

# file-format-dispatch-and-handler-routing

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Route file I/O operations to format-specific handler classes by detecting file extension or metadata in a central FileInterface dispatcher. This skill enables a parser library to support multiple data formats (mzML, .db, indexed gzip) without duplicating parsing logic, by instantiating the appropriate connector class at open time.

## When to use

You have a parser library that must support multiple file formats (e.g., mzML, SQLite, compressed gzip) and want to avoid conditional logic scattered throughout the parsing code. Use this skill when you need to detect file type at I/O time and route to a custom handler class that implements a standard interface (__getitem__, read, get_count methods).

## When NOT to use

- File format is already determined and a single handler is sufficient — skip dispatch overhead and instantiate directly.
- Parser receives a file handle (already open) rather than a path — dispatch typically occurs at the path/filename stage.
- All supported formats share identical binary structure — use a single polymorphic handler with format-aware logic instead of routing.

## Inputs

- file path or URI (string)
- file extension or metadata indicating storage format
- optional: file size or header bytes for format detection

## Outputs

- file handler instance (custom class inheriting FileInterface or implementing __getitem__ and read)
- Spectrum or Chromatogram objects (via handler's __getitem__ and read methods)

## How to apply

In the central FileInterface._open() method, add a chain of elif statements that detect file extension or path properties (e.g., path.endswith('.db'), path.endswith('.mzML.gz')). For each format, instantiate the appropriate custom handler class (e.g., SQLiteDatabase, IndexedGzipReader) that implements the required read() and __getitem__() methods. Assign the instantiated handler to file_handler and return it to the caller. Each handler class must parse its format into the same output type (Spectrum or Chromatogram objects) so the downstream Reader sees a unified interface regardless of the storage format.

## Related tools

- **pymzML** (Parser library providing FileInterface base class and Reader; route file handlers through FileInterface._open() to enable format-agnostic spectrum access) — https://github.com/pymzml/pymzML
- **sqlite3** (Query and retrieve spectrum XML elements from .db files in the SQLiteDatabase handler's __getitem__ implementation)
- **ElementTree** (Parse XML string elements retrieved from database or gzip into Spectrum objects via pymzML's spec module)
- **black** (Code formatter applied to handler implementations to ensure consistent style across format-specific classes) — https://github.com/psf/black

## Examples

```
from pymzml import Reader; reader = Reader('spectra.db'); spectrum = reader[0]; print(spectrum.mz, spectrum.intensity)
```

## Evaluation signals

- FileInterface._open() correctly detects file extension and instantiates the appropriate handler class without raising KeyError or AttributeError.
- Handler.__getitem__(key) returns valid Spectrum or Chromatogram objects for integer or string keys; verify object type and that required fields (mz, intensity, ID) are populated.
- Handler.read() yields sequential spectrum XML strings or parsed objects; verify iteration count matches get_spectrum_count().
- Round-trip test: open a .db file via FileInterface, iterate over spectra via Reader, and confirm spectrum IDs and m/z arrays match the original mzML source.
- No performance regression: dispatch overhead (extension check, handler instantiation) is <1% of total parse time for typical mzML files.

## Limitations

- File extension detection is brittle if files lack standard extensions (e.g., renamed .mzML.gz to .gz); consider adding magic-byte detection as a fallback.
- Each new format requires a custom handler class implementing __getitem__ and read; no automatic schema inference — handler logic is format-specific and must be written by hand.
- Handler must produce identical output types (Spectrum, Chromatogram) to maintain Reader compatibility; if a format stores fundamentally different metadata (e.g., only precursor m/z, no fragments), mapping to standard Spectrum may lose information.
- Sequential read() via iteration does not support random-access seeking in all formats; indexed gzip and SQLite support __getitem__ random access, but naive text parsers may need refactoring to enable both access patterns.

## Evidence

- [other] dispatch_via_extension: "Add an elif clause to FileInterface._open() that detects '.db' file extensions and instantiates SQLiteDatabase, routing the file_handler assignment to the new connector class."
- [other] handler_interface_contract: "Implement a class, which needs to implement the __getitem__ function for random access, and a read function used to sequentially read in data for iterating the database."
- [other] unified_output_type: "__getitem__(key) to execute SQL queries and return Spectrum or Chromatogram objects parsed from XML elements"
- [intro] extensibility_rationale: "In order to make pymzML accept other kinds of mzML data (e.g databases), one can implement an own wrapper"
- [intro] multiple_format_support: "Module to parse mzML data in Python based on cElementTree... ability to write and read indexed gzip files"
