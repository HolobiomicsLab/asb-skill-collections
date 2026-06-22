---
name: blockwise-data-parsing-and-indexing
description: Use when when you need random access into a large text or XML file that you want to keep compressed, where the file has natural logical divisions (chapters, spectra, records) that can be written independently.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0080
  tools:
  - ElementTree
  - pymzML
  - Python ElementTree
  - GSGW (Generalized Seekable Gzip Writer)
  - Black
  techniques:
  - mass-spectrometry
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# blockwise-data-parsing-and-indexing

## Summary

Parse and index large structured data files (e.g., mzML, text documents) by logical blocks—each block written as a single unit with an integer or string identifier—using the Generalized Seekable Gzip Writer (GSGW) pattern to enable random access in compressed archives without decompressing the entire file.

## When to use

When you need random access into a large text or XML file that you want to keep compressed, where the file has natural logical divisions (chapters, spectra, records) that can be written independently. This skill is especially valuable for mass spectrometry data (mzML) or narrative text where you want to retrieve specific blocks by key without loading all preceding data.

## When NOT to use

- Input data is unstructured or does not have well-defined logical blocks; use general-purpose compression instead.
- You require edit-in-place or frequent insertion/deletion within the compressed file; GSGW is write-once.
- File is already stored in a seekable indexed format (e.g., SQLite database); re-indexing adds redundant overhead.
- Random access latency is not a concern and the file fits in memory; simpler compression suffices.

## Inputs

- Source file with logical block structure (mzML, text file with chapters, XML-based records)
- Block identifiers (integer or string keys)
- File path or file handle

## Outputs

- Indexed gzip archive with byte-offset index
- Custom file handler object supporting bracket notation access and sequential read()
- Compressed file at reduced size comparable to original binary format

## How to apply

1. Identify and parse the source file blockwise, treating each logical unit (e.g., chapter, spectrum) as a discrete block. 2. Create a custom handler class that implements __getitem__(key) for random access by integer or string identifier and read() for sequential iteration. 3. Use GSGW to write each parsed block in a single operation via add_data(key, block_data), then finalize with write_index() to record byte offsets for each key. 4. Integrate the handler into the file interface (e.g., pymzML's FileInterface._open()) by adding detection logic to instantiate the wrapper when the compressed indexed file is encountered. 5. Validate random access by retrieving specific keys and sequential reads by iterating through all blocks to confirm data completeness and absence of corruption.

## Related tools

- **pymzML** (File interface framework for mzML parsing; accepts custom handlers via FileInterface._open() to support indexed gzip access) — https://github.com/pymzml/pymzML
- **Python ElementTree** (XML parsing library used to parse blockwise structured mzML or XML data before writing blocks to indexed gzip)
- **GSGW (Generalized Seekable Gzip Writer)** (Core compression and indexing mechanism; writes blocks with add_data() and builds index via write_index())
- **Black** (Code formatter for ensuring style compliance in implementation) — https://github.com/psf/black

## Examples

```
from pymzml import spec; handler = spec.MzML(filename='moby_dick_indexed.mzML.gz'); chapter_3 = handler['chapter_3']; for block_key, block_data in handler: process(block_data)
```

## Evaluation signals

- Random access via bracket notation (e.g., handler[key]) returns the correct decompressed block for each key without decompressing other blocks.
- Sequential iteration via read() returns all blocks in order with no data loss, corruption, or gaps.
- Byte offsets recorded in the index correspond to actual block positions in the compressed file.
- Compressed file size is comparable to the original binary format (e.g., mzML.gz ≈ RAW format size).
- Handler integration into FileInterface._open() successfully detects indexed gzip files and instantiates the wrapper without breaking existing file type detection.

## Limitations

- The index is built once during write and cannot be updated; all data must be available upfront.
- Each block must fit in memory during writing, limiting applicability to very large individual records.
- Key collision or reuse will overwrite previous entries; users must ensure key uniqueness.
- No built-in transaction or rollback mechanism; file I/O errors during write_index() may leave the archive in an incomplete state.

## Evidence

- [other] GSGW accepts data parsed blockwise from a source file, with each logical block (e.g., chapter) written in a single operation using add_data() and indexed by either integer or string identifiers, then finalized with write_index() to create an indexed gzip file.: "each logical block (e.g., chapter) written in a single operation using add_data() and indexed by either integer or string identifiers, then finalized with write_index()"
- [other] Implement custom API class with read() and __getitem__() functions for different mzML file formats: "a new class needs to be written, which implements a `read` and a `__getitem__` function"
- [intro] Indexed gzip files allow mzML file sizes to reach levels comparable to the original RAW format: "indexed gzip which allows mzML file sizes to reach the levels of the original RAW format"
- [intro] pymzML enables parsing of mzML data and supports multiple file formats including mzML, mzML.gz, and indexed gzip files with random access capability: "Module to parse mzML data in Python... ability to write and read indexed gzip files"
- [other] In order to allow pymzML to use this new file class, the filehandler needs to be able to detect when to use this class. The easiest way is, to add another elif statement which decides which handler: "the filehandler needs to be able to detect when to use this class. The easiest way is, to add another elif statement"
- [readme] pymzML is an extension to Python that offers a) easy access to mass spectrometry (MS) data that allows the rapid development of tools b) a very fast parser for mzML data, the standard mass spectrometry data format c) a set of functions to compare and/or handle spectra d) random access in compressed files: "pymzML is an extension to Python that offers...d) random access in compressed files"
