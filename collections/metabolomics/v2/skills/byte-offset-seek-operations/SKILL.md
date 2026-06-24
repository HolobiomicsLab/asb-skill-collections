---
name: byte-offset-seek-operations
description: 'Use when when you have an indexed gzip-compressed mzML file and need
  to retrieve individual spectra or chromatograms by index without sequential file
  reading or full decompression. Typical scenario: you want spectrum[42] from a 10
  GB indexed mzML.gz file and need sub-second access time.'
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
  techniques:
  - mass-spectrometry
  license_tier: restricted
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

# byte-offset-seek-operations

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Enable random access retrieval of indexed data blocks from compressed gzip files by implementing bracket notation access that translates integer indices to byte offsets and extracts decompressed XML elements. This skill is essential for handling large-scale mzML mass spectrometry data in seekable gzip format without decompressing the entire file.

## When to use

When you have an indexed gzip-compressed mzML file and need to retrieve individual spectra or chromatograms by index without sequential file reading or full decompression. Typical scenario: you want spectrum[42] from a 10 GB indexed mzML.gz file and need sub-second access time.

## When NOT to use

- Input is an uncompressed mzML file—use standard sequential parsing instead
- The gzip file lacks an internal index structure—first create one using GSGW (Generalized Seekable Gzip Writer) class
- You need to iterate through all spectra sequentially; use a simpler read() method for better streaming performance

## Inputs

- indexed gzip file path (string)
- integer index (key for bracket notation)
- gzip file with internal index structure mapping indices to byte offsets

## Outputs

- Spectrum object (parsed from XML element)
- Chromatogram object (parsed from XML element)
- decompressed XML data block (string)

## How to apply

Implement a reader class (GSGR) that accepts the path to an indexed gzip file during initialization. The class must implement the `__getitem__` method to accept an integer index. Load the index mapping from the gzip file's internal index structure to translate the integer key to byte offsets. Seek to the appropriate byte offset in the gzip file using the offset table, extract the indexed data block, decompress it, and parse the resulting XML using ElementTree. Instantiate and return either a Spectrum or Chromatogram object based on the parsed element tag. The byte offset lookup and seek operation are the critical performance paths—these enable random access without iterating through preceding entries.

## Related tools

- **pymzML** (provides GSGR class, ElementTree parsing, and Spectrum/Chromatogram object model for implementing bracket notation random access on indexed gzip files) — https://github.com/pymzml/pymzML
- **ElementTree** (parses extracted XML data blocks into Python element trees for tag-based object instantiation)
- **Python** (standard library for file I/O, seek operations, and index data structure management)

## Examples

```
from pymzml.FileInterface import FileInterface
reader = FileInterface('large_file.mzML.gz')
spectrum_42 = reader[42]
print(spectrum_42.mz, spectrum_42.intensity)
```

## Evaluation signals

- Verify that `reader[n]` returns a valid Spectrum or Chromatogram object for valid indices 0 ≤ n < file_length without raising IndexError
- Check that the returned object's XML attributes (e.g. scan number, precursor m/z) match the expected values for that index
- Confirm that seek operation completes in <100 ms for random indices, demonstrating true random access (not sequential decompression)
- Validate that decompressed XML parses without ElementTree exceptions and instantiation produces correct object type (Spectrum vs Chromatogram based on tag name)
- Test boundary cases: index=0, index=last_valid, index=out_of_range (should raise IndexError); ensure no file handle leaks on repeated access

## Limitations

- The gzip file must be pre-indexed using GSGW (Generalized Seekable Gzip Writer); seek operations fail silently or raise errors if the index structure is malformed or missing
- Index size grows linearly with the number of spectrum/chromatogram blocks; very large datasets may incur overhead in loading the full index into memory
- Byte offset lookups assume the indexed gzip format is stable; changes to compression parameters or re-compression will invalidate existing indices
- ElementTree parsing assumes well-formed XML; corrupted or truncated data blocks will raise parsing exceptions

## Evidence

- [other] The GSGR class accepts an indexed gzip file path during initialization and implements bracket notation access to retrieve data blocks.: "The GSGR class accepts an indexed gzip file path during initialization and implements bracket notation access to retrieve data blocks."
- [other] Chapters are accessed by passing an integer index to the reader object, which then locates and returns the corresponding decompressed data block from the indexed gzip file.: "Chapters are accessed by passing an integer index to the reader object, which then locates and returns the corresponding decompressed data block from the indexed gzip file."
- [other] Load the index mapping from the gzip file's internal index structure to translate the integer key to byte offsets.: "Load the index mapping from the gzip file's internal index structure to translate the integer key to byte offsets."
- [other] Seek to the appropriate byte offset in the gzip file and extract the indexed data block.: "Seek to the appropriate byte offset in the gzip file and extract the indexed data block."
- [other] Parse the extracted XML data using ElementTree and instantiate either a Spectrum or Chromatogram object based on the element tag.: "Parse the extracted XML data using ElementTree and instantiate either a Spectrum or Chromatogram object based on the element tag."
- [readme] ability to write and read indexed gzip files: "ability to write and read indexed gzip files"
- [readme] access the chapters conveniently by the python bracket notation ([]): "access the chapters conveniently by the python bracket notation ([])"
