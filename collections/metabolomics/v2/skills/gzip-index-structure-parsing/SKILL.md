---
name: gzip-index-structure-parsing
description: Use when when you have an indexed gzip-compressed mzML file (mzML.gz with an internal index) and need to retrieve specific spectra or chromatogram data blocks by integer index without decompressing the entire archive.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - ElementTree
  - pymzML
  - Python
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

# gzip-index-structure-parsing

## Summary

Parse and navigate indexed gzip file structures to enable random access retrieval of compressed mzML data blocks using Python bracket notation. This skill allows mass spectrometry data to be stored in highly compressed indexed gzip format while maintaining O(1) seek-time access to individual spectra or chromatograms without decompressing the entire file.

## When to use

When you have an indexed gzip-compressed mzML file (mzML.gz with an internal index) and need to retrieve specific spectra or chromatogram data blocks by integer index without decompressing the entire archive. This is particularly valuable for large mass spectrometry datasets where file size approaches the original RAW format and sequential iteration is inefficient.

## When NOT to use

- Input is a non-indexed gzip file (no internal index structure); use sequential parsing instead.
- Input is an uncompressed mzML file; direct XML parsing is more efficient.
- You need to read all spectra sequentially; use the `read()` function for iteration rather than repeated bracket notation calls.

## Inputs

- indexed gzip file path (mzML.gz with internal index structure)
- integer index (0-based chapter/spectrum identifier)

## Outputs

- Spectrum object (parsed from indexed XML data block)
- Chromatogram object (parsed from indexed XML data block)

## How to apply

Instantiate a Generalized Seekable Gzip Reader (GSGR) class with the path to an indexed gzip file. Load the internal index structure that maps integer indices to byte offsets within the compressed file. Implement the `__getitem__` method to accept an integer index, use the index mapping to locate the corresponding byte offset, seek to that position in the gzip file, extract and decompress the indexed data block, parse the XML content using ElementTree, and instantiate either a Spectrum or Chromatogram object based on the element tag. Access data blocks via Python bracket notation (e.g., `reader[chapter_index]`), which invokes `__getitem__` and returns the decompressed spectrum or chromatogram object.

## Related tools

- **pymzML** (Provides GSGR class implementation and Spectrum/Chromatogram object models for parsing indexed gzip mzML files) — https://github.com/pymzml/pymzML
- **ElementTree** (Parses decompressed XML data blocks extracted from indexed gzip to instantiate Spectrum and Chromatogram objects)
- **Python** (Provides gzip file I/O, bracket notation via `__getitem__` protocol, and byte-offset seek operations)

## Examples

```
from pymzml.oset import IndexedGzip; reader = IndexedGzip('/path/to/file.mzML.gz'); spectrum = reader[42]; print(spectrum.mz, spectrum.i)
```

## Evaluation signals

- Bracket notation `reader[N]` returns a valid Spectrum or Chromatogram object without raising IndexError or seek errors
- Retrieved object contains expected XML attributes and child elements corresponding to the requested index
- Multiple calls with different indices retrieve distinct, non-overlapping data blocks from the same indexed gzip file
- Seek time to retrieve any indexed block is independent of file size and block position (O(1) access pattern verified)
- Index structure is correctly parsed and byte offsets map to valid gzip frame boundaries

## Limitations

- Indexed gzip format requires an internal index structure created during file generation (via GSGW class); non-indexed gzip files cannot be read with GSGR.
- Performance depends on the accuracy and integrity of the internal index mapping; corrupted or missing index entries will cause seek failures.
- The index must be compatible with the pymzML implementation; third-party indexed gzip tools may produce incompatible structures.
- Random access performance assumes the gzip file is stored on a filesystem supporting efficient seek operations; network or tape storage may negate the speed advantage.

## Evidence

- [intro] access the chapters conveniently by the python bracket notation ([]): "access the chapters conveniently by the python bracket notation ([])"
- [other] Chapters are accessed by passing an integer index to the reader object, which then locates and returns the corresponding decompressed data block from the indexed gzip file.: "Chapters are accessed by passing an integer index to the reader object, which then locates and returns the corresponding decompressed data block"
- [other] The GSGR class accepts an indexed gzip file path during initialization and implements bracket notation access to retrieve data blocks.: "The GSGR class accepts an indexed gzip file path during initialization and implements bracket notation access to retrieve data blocks"
- [other] Seek to the appropriate byte offset in the gzip file and extract the indexed data block. Parse the extracted XML data using ElementTree and instantiate either a Spectrum or Chromatogram object based on the element tag.: "Seek to the appropriate byte offset in the gzip file and extract the indexed data block. Parse the extracted XML data using ElementTree and instantiate either a Spectrum or Chromatogram object"
- [intro] indexed gzip which allows mzML file sizes to reach the levels of the original RAW format: "indexed gzip which allows mzML file sizes to reach the levels of the original RAW format"
- [readme] random access in compressed files: "random access in compressed files"
