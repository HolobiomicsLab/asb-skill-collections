---
name: sequential-and-random-access-dual-mode-support
description: Use when when parsing mzML or other blockwise-structured scientific data
  files where analysis requires both sequential scanning (e.g., iterating all spectra)
  and random direct access by identifier (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3520
  tools:
  - ElementTree
  - pymzML
  - Python
  - Black
  techniques:
  - mass-spectrometry
  license_tier: open
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

# sequential-and-random-access-dual-mode-support

## Summary

Implement dual-mode file access (sequential iteration and random indexing) for compressed mass spectrometry data formats by creating a wrapper class that bridges pymzML's FileInterface with custom storage backends, enabling both blockwise iteration and key-based random access to indexed gzip archives.

## When to use

When parsing mzML or other blockwise-structured scientific data files where analysis requires both sequential scanning (e.g., iterating all spectra) and random direct access by identifier (e.g., retrieving a specific chapter or spectrum by name/ID), and file compression is necessary to reduce storage from RAW format sizes while maintaining seek capability.

## When NOT to use

- Input is already a compressed indexed gzip file (use GSGR reader directly rather than reconstructing)
- Analysis requires only sequential access with no random lookups (standard gzip or streaming decompressor is simpler and faster)
- File size is small enough that full decompression into memory is feasible (overhead of indexing not justified)

## Inputs

- uncompressed blockwise-structured text file (e.g., mzML, chapters of Moby Dick)
- logical block identifiers (integer or string keys for each block)

## Outputs

- indexed gzip file with byte-offset index mapping keys to block locations
- wrapped file handler object supporting both `read()` and `__getitem__()` interfaces

## How to apply

Create a custom wrapper class that implements both `read()` (for sequential iteration returning one logical block per call) and `__getitem__(key)` (for random access returning a block by integer or string identifier). Parse the input file blockwise using the Generalized Seekable Gzip Writer (GSGW) pattern, writing each logical unit (e.g., spectrum, chapter) with `add_data()` and finalizing with `write_index()` to map keys to byte offsets. Integrate the wrapper into pymzML's FileInterface by adding an elif clause in `_open()` to detect the file type and instantiate your handler. Validate that random access via bracket notation returns correct blocks and sequential reads iterate without data loss or corruption.

## Related tools

- **pymzML** (Provides FileInterface abstraction layer, GSGW/GSGR indexed gzip classes, and spectrum/mzML parsing; wrapper integrates into pymzML.FileInterface._open() to enable dual-mode access) — https://github.com/pymzml/pymzML
- **ElementTree** (XML parsing for mzML structure (blockwise parsing may leverage ElementTree to identify logical boundaries))
- **Python** (Core language for implementing wrapper class and integration)
- **Black** (Code formatter for maintaining style consistency in wrapper and integration code) — https://github.com/psf/black

## Examples

```
from pymzml import FileInterface; handler = FileInterface._open('moby_dick.indexed.gzip'); chapter_5 = handler['5']; all_chapters = [block for block in iter(handler.read, None)]
```

## Evaluation signals

- Random access via bracket notation (e.g., `handler[key]`) returns the exact block corresponding to that key without loading the entire file
- Sequential iteration using `read()` returns blocks in order, with each call advancing position, and stops cleanly at EOF
- Byte offsets in the index file are correct (verify by seeking to offset, decompressing, and confirming block identity)
- No data corruption or truncation detected when comparing decompressed block content to original blockwise input
- File size of indexed gzip archive is comparable to or smaller than original RAW format (per pymzML design goal)

## Limitations

- Index must be finalized with write_index() before use; dynamic updates to keys after finalization require index reconstruction
- Blockwise parsing assumes clear logical boundaries (e.g., chapter markers, spectrum delimiters); ambiguous block boundaries may cause data loss
- Random access performance depends on index lookup speed; very large indices may incur overhead
- The wrapper must be tightly coupled to pymzML's FileInterface; compatibility issues may arise if pymzML's API changes

## Evidence

- [other] GSGW accepts data parsed blockwise from a source file, with each logical block (e.g., chapter) written in a single operation using add_data() and indexed by either integer or string identifiers, then finalized with write_index() to create an indexed gzip file.: "GSGW accepts data parsed blockwise from a source file, with each logical block (e.g., chapter) written in a single operation using add_data() and indexed by either integer or string identifiers, then"
- [readme] pymzML is an extension to Python that offers a) easy access to mass spectrometry (MS) data that allows the rapid development of tools b) a very fast parser for mzML data, the standard mass spectrometry data format c) a set of functions to compare and/or handle spectra d) random access in compressed files e) interactive data visualization: "pymzML is an extension to Python that offers a) easy access to mass spectrometry (MS) data that allows the rapid development of tools b) a very fast parser for mzML data, the standard mass"
- [other] a new class needs to be written, which implements a `read` and a `__getitem__` function: "a new class needs to be written, which implements a `read` and a `__getitem__` function"
- [other] In order to allow pymzML to use this new file class, the filehandler needs to be able to detect when to use this class. The easiest way is, to add another elif statement which decides which handler: "In order to allow pymzML to use this new file class, the filehandler needs to be able to detect when to use this class. The easiest way is, to add another elif statement"
- [readme] indexed gzip which allows mzML file sizes to reach the levels of the original RAW format: "indexed gzip which allows mzML file sizes to reach the levels of the original RAW format"
