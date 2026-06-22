---
name: python-bracket-notation-protocol-implementation
description: Use when you have a blockwise-indexed compressed file (e.g., indexed gzip with chapter or spectrum identifiers) and need to retrieve individual logical blocks by key using Python bracket notation (e.g., `handler['chapter_1']` or `handler[0]`) rather than sequential iteration.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3216
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - ElementTree
  - pymzML
derived_from:
- doi: 10.1093/bioinformatics/bty046
  title: pymzml
evidence_spans:
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Python Bracket Notation Protocol Implementation

## Summary

Implement the `__getitem__()` protocol in a custom Python class to enable random access to indexed data blocks (e.g., chapters in a compressed mzML file) using bracket notation. This allows seekable access to blockwise-indexed content without decompressing the entire file.

## When to use

You have a blockwise-indexed compressed file (e.g., indexed gzip with chapter or spectrum identifiers) and need to retrieve individual logical blocks by key using Python bracket notation (e.g., `handler['chapter_1']` or `handler[0]`) rather than sequential iteration. The data must already be partitioned into discrete, addressable units with corresponding index entries.

## When NOT to use

- Data is stored in a sequential (non-indexed) format — use sequential read() instead.
- The index is not available or malformed — implement index reconstruction or fall back to linear scan.
- Access patterns are purely sequential — overhead of bracket-notation lookup may not justify the implementation.

## Inputs

- indexed gzip file (.gz with internal or sidecar index)
- blockwise-indexed data (e.g., mzML with chapter or spectrum identifiers)
- integer or string key mapping (e.g., chapter names, spectrum IDs)

## Outputs

- custom wrapper class implementing __getitem__() protocol
- retrieved data block (e.g., XML element string or binary chunk)
- random-access handler suitable for integration into FileInterface

## How to apply

Define a custom wrapper class that implements the `__getitem__(self, key)` method to accept either integer or string identifiers and return the corresponding data block from the indexed file. The class must maintain an internal index mapping keys to byte offsets within the compressed file, using a GSGR (Generalized Seekable Gzip Reader) or similar seek-capable reader to retrieve the block at the correct file position. Populate the index during initialization by parsing the index structure embedded in or accompanying the compressed file. Test random access by calling the handler with bracket notation and verify that each key returns the correct block without iterating through preceding blocks.

## Related tools

- **pymzML** (FileInterface host for custom handler; provides GSGR/GSGW classes and Spectrum/Run parsing infrastructure) — https://github.com/pymzml/pymzML
- **Python** (Language for implementing __getitem__() protocol and wrapper class)
- **ElementTree** (XML parsing of mzML spectrum and run elements retrieved via bracket notation)

## Examples

```
class MzMLHandler:
    def __init__(self, filename):
        self.reader = gzip.open(filename)
        self.index = self._load_index()
    def __getitem__(self, key):
        offset = self.index[key]
        self.reader.seek(offset)
        return self.reader.read()

handler = MzMLHandler('file.mzML.gz')
spectrum = handler['scan=1234']
```

## Evaluation signals

- Random access via bracket notation returns correct block for each key without sequential iteration (time complexity ≤ O(1) per access after index load).
- Sequential iteration via read() function traverses all blocks without data loss or corruption.
- Index mapping is consistent: all keys present in the compressed file are correctly addressable; no orphaned or duplicate entries.
- Retrieved XML or binary data matches expected schema (e.g., valid mzML spectrum elements with correct scan number or chapter boundary).
- Handler integrates into pymzML FileInterface via elif statement in _open() and transparently replaces native file access for detected file types.

## Limitations

- Requires pre-existing index embedded in or alongside the compressed file; no dynamic re-indexing of non-indexed gzip files.
- Performance depends on index lookup speed and seek latency; large indices may cause initial overhead.
- String keys require case-sensitive or normalized matching; inconsistent key format may lead to KeyError.
- Handler must be registered in FileInterface._open() for automatic detection; manual instantiation required otherwise.

## Evidence

- [intro] access the chapters conveniently by the python bracket notation ([]): "access the chapters conveniently by the python bracket notation ([])"
- [intro] a new class needs to be written, which implements a `read` and a `__getitem__` function: "a new class needs to be written, which implements a `read` and a `__getitem__` function"
- [other] we need to implement a class, which needs to implement the __getitem__ function for random access: "we need to implement a class, which needs to implement the __getitem__ function for random access"
- [intro] parse the data blockwise, so every piece of data, which should be accessible by indexing is written in one go: "parse the data blockwise, so every piece of data, which should be accessible by indexing is written in one go"
- [other] the filehandler needs to be able to detect when to use this class. The easiest way is, to add another elif statement: "the filehandler needs to be able to detect when to use this class. The easiest way is, to add another elif statement"
