---
name: python-random-access-implementation
description: Use when when you have an indexed gzip file (mzML.gz with internal index structure) and need to retrieve individual spectra or chromatograms by integer index without decompressing the entire file.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - ElementTree
  - pymzML
  techniques:
  - mass-spectrometry
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# python-random-access-implementation

## Summary

Implement bracket-notation random access to indexed gzip-compressed mass spectrometry data by building a custom class with __getitem__ and read methods that translate integer indices to byte offsets and retrieve decompressed XML data blocks. This skill enables efficient, non-sequential queries of large mzML files compressed to RAW-comparable sizes.

## When to use

When you have an indexed gzip file (mzML.gz with internal index structure) and need to retrieve individual spectra or chromatograms by integer index without decompressing the entire file. Use this when sequential iteration is not feasible due to file size or when random-access latency matters more than batch processing.

## When NOT to use

- Input file is unindexed gzip or standard mzML; use sequential parsing instead.
- Need to access all spectra in order; sequential iteration with read() is more efficient.
- mzML data is stored in a database or custom wrapper; implement __getitem__ on the database abstraction layer instead.

## Inputs

- indexed gzip file path (mzML.gz with internal index)
- integer index (0-based chapter number)
- file handle or path string

## Outputs

- Spectrum object (parsed from XML element)
- Chromatogram object (parsed from XML element)
- decompressed XML data block (string)

## How to apply

Define a custom class that accepts an indexed gzip file path and implements __getitem__(index) to accept integer indices. Load the index mapping from the gzip file's internal index structure to translate the integer key to byte offsets. Seek to the appropriate byte offset in the gzip file, extract and decompress the indexed data block, then parse the resulting XML using ElementTree. Instantiate either a Spectrum or Chromatogram object based on the XML element tag and return it. Implement a separate read() method for sequential iteration if the FileInterface requires both random and sequential access patterns.

## Related tools

- **pymzML** (Provides Spectrum and Chromatogram classes, FileInterface abstraction, and indexed gzip file support via GSGR/GSGW; integrates custom __getitem__ implementations) — https://github.com/pymzml/pymzML
- **ElementTree** (Parses extracted XML data blocks into Python objects after decompression)
- **Python** (Core language for implementing class, file I/O, and gzip seek operations)

## Examples

```
from pymzml import GSGR; reader = GSGR('data.mzML.gz'); spectrum = reader[42]; print(spectrum.mz, spectrum.intensity)
```

## Evaluation signals

- Bracket notation call (e.g., reader[42]) returns a valid Spectrum or Chromatogram object without raising IndexError or decompression error.
- Returned object's properties (m/z, intensity, retention time) match the expected values for that index from sequential parsing of the same file.
- Byte offset lookup correctly maps integer index to gzip file position; verify by comparing seek position before and after __getitem__ call.
- Performance of random access queries is significantly faster than sequential decompression up to the target index.
- Index structure is correctly loaded from the gzip file's metadata; verify by comparing index length to expected spectrum count.

## Limitations

- Requires a properly indexed gzip file with internal index structure (mzML.gz format); will fail silently or raise exceptions on unindexed gzip.
- Integer indexing assumes contiguous, 0-based spectrum numbering; gaps in index or non-integer identifiers require adapter layer.
- XML parsing with ElementTree may be slow for very large spectra; consider streaming or lazy evaluation for high-dimensional data.
- Custom class must detect and integrate into pymzML's FileInterface; requires elif statement in file handler detection logic as noted in the article.

## Evidence

- [other] Chapters are accessed by passing an integer index to the reader object, which then locates and returns the corresponding decompressed data block from the indexed gzip file.: "Chapters are accessed by passing an integer index to the reader object, which then locates and returns the corresponding decompressed data block from the indexed gzip file."
- [other] Implement the __getitem__ method to accept an integer index and retrieve the corresponding chapter/spectrum from the indexed gzip file.: "Implement the __getitem__ method to accept an integer index and retrieve the corresponding chapter/spectrum from the indexed gzip file."
- [other] Load the index mapping from the gzip file's internal index structure to translate the integer key to byte offsets.: "Load the index mapping from the gzip file's internal index structure to translate the integer key to byte offsets."
- [other] Parse the extracted XML data using ElementTree and instantiate either a Spectrum or Chromatogram object based on the element tag.: "Parse the extracted XML data using ElementTree and instantiate either a Spectrum or Chromatogram object based on the element tag."
- [intro] a new class needs to be written, which implements a `read` and a `__getitem__` function: "a new class needs to be written, which implements a `read` and a `__getitem__` function"
- [intro] access the chapters conveniently by the python bracket notation ([]): "access the chapters conveniently by the python bracket notation ([])"
- [readme] pymzML is an extension to Python that offers... random access in compressed files: "pymzML is an extension to Python that offers... random access in compressed files"
