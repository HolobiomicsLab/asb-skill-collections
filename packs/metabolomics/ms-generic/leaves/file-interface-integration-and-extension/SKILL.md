---
name: file-interface-integration-and-extension
description: Use when when you need to parse mzML data stored in a format beyond the
  built-in mzML, mzML.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - ElementTree
  - pymzML
  - sqlite3
  - black
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1093/bioinformatics/bty046
  title: pymzml
evidence_spans:
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

# file-interface-integration-and-extension

## Summary

Extend pymzML's FileInterface to support custom file formats (e.g., indexed gzip, databases) by implementing wrapper classes with __getitem__() for random access and read() for sequential iteration, then integrating them via conditional detection in FileInterface._open(). This skill enables rapid parser development for non-standard mzML storage backends.

## When to use

When you need to parse mzML data stored in a format beyond the built-in mzML, mzML.gz, and indexed gzip support—such as from databases, custom compression schemes, or blockwise-indexed archives—and you want to leverage pymzML's existing spectrum parsing and comparison utilities without reimplementing the entire pipeline.

## When NOT to use

- Your mzML data is already in standard mzML or mzML.gz format—use pymzML's native handlers instead.
- You require streaming-only access to extremely large files and cannot afford the overhead of maintaining an index or wrapper class.
- Your custom format lacks a natural logical block structure (e.g., contiguous byte stream with no boundaries)—restructure the format first or consider alternative storage.

## Inputs

- Source file in custom format (indexed gzip, SQLite database, or custom archive)
- File type identifier or path suffix
- Optional schema mapping logical blocks to keys (chapter boundaries, spectrum IDs, database table layout)

## Outputs

- Custom file handler class implementing __getitem__() and read()
- Integrated FileInterface that recognizes and instantiates the handler
- Seekable, random-accessible mzML spectrum data via pymzML API

## How to apply

First, analyze your source file format to identify how data is logically partitioned (e.g., by chapter, spectrum ID, or database record). Create a custom wrapper class that implements two methods: __getitem__(key) to support random access by integer or string identifier, and read() to yield sequential blocks for iteration. If using blockwise indexing (e.g., indexed gzip), write each logical block in a single operation using a GSGW-like pattern and maintain a key-to-byte-offset index. Finally, integrate the wrapper into pymzML by adding an elif statement in FileInterface._open() to detect your file type and instantiate the wrapper class. Test both access patterns: bracket notation for random access and iteration for sequential reads, verifying that all blocks are retrievable without corruption.

## Related tools

- **pymzML** (Host framework for file handler integration; provides FileInterface._open() extension point and spectrum parsing utilities after handler retrieval) — https://github.com/pymzml/pymzML
- **ElementTree** (XML parsing backend used by pymzML to deserialize mzML spectrum elements returned by custom handlers)
- **sqlite3** (Example backend for implementing database-backed handlers that retrieve spectrum XML from relational tables)
- **black** (Code formatter for ensuring consistent Python style in wrapper and integration code) — https://github.com/psf/black

## Examples

```
from pymzml import FileInterface; handler = MyIndexedGzipWrapper('moby_dick.igz'); spectrum_data = handler['chapter_5']; for block in handler: process(block)
```

## Evaluation signals

- Random access via bracket notation (e.g., handler['chapter_5']) returns the correct logical block without seeking errors or data loss.
- Sequential iteration via read() yields all blocks in order with no skipped or duplicate records.
- pymzML's FileInterface detects the custom file type and instantiates the handler without manual path construction or type casting.
- Spectrum comparison and querying functions (e.g., spec.ID, m/z filtering) work on spectra retrieved via the handler, confirming XML deserialization correctness.
- Indexed byte offsets map consistently to logical blocks: verify no off-by-one errors or corruption when jumping to non-sequential keys.

## Limitations

- Implementation of __getitem__() and read() must match the exact logical block structure of your format; misalignment causes silent data loss or duplication.
- Maintaining an in-memory or on-disk index (key-to-offset map) adds storage and initialization overhead; very large archives may require lazy index construction.
- FileInterface._open() detection relies on file extension or path pattern matching; ambiguous file types may require additional metadata or MIME type hints.
- The wrapper class is specific to each custom format; no single implementation generalizes to arbitrary blockwise or database schemas.

## Evidence

- [other] In order to make pymzML accept other kinds of mzML data (e.g databases), one can implement an own wrapper: "In order to make pymzML accept other kinds of mzML data (e.g databases), one can implement an own wrapper"
- [other] a new class needs to be written, which implements a `read` and a `__getitem__` function: "a new class needs to be written, which implements a `read` and a `__getitem__` function"
- [intro] parse the data blockwise, so every piece of data, which should be accessible by indexing is written in one go. The index used can be either an integer or a string: "parse the data blockwise, so every piece of data, which should be accessible by indexing is written in one go. The index used can be either an integer or a string"
- [other] In order to allow pymzML to use this new file class, the filehandler needs to be able to detect when to use this class. The easiest way is, to add another elif statement which decides which handler: "In order to allow pymzML to use this new file class, the filehandler needs to be able to detect when to use this class. The easiest way is, to add another elif statement which decides which handler"
- [readme] random access in compressed files: "random access in compressed files"
