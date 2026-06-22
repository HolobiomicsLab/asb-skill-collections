---
name: compressed-file-header-parsing
description: Use when you have a large indexed gzip file (igz format) with metadata encoded in the gzip header comment field, and you need to retrieve specific blocks or spectra by integer index without decompressing the entire file.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3546
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - xml.etree.ElementTree
  - pymzML
  - Python
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# compressed-file-header-parsing

## Summary

Parse binary metadata embedded in gzip file headers to construct an index-to-offset mapping that enables random-access retrieval of compressed data blocks without full decompression. This skill is essential for handling large indexed gzip files (igz format) where seek-by-index performance is critical.

## When to use

You have a large indexed gzip file (igz format) with metadata encoded in the gzip header comment field, and you need to retrieve specific blocks or spectra by integer index without decompressing the entire file. This is common in mass spectrometry workflows where mzML files are stored as indexed gzip to save space while maintaining rapid random access to individual spectra.

## When NOT to use

- Input is an uncompressed or standard gzip file without embedded index metadata in the header comment field; use sequential parsing instead.
- You need to retrieve all blocks or iterate through the entire file; sequential decompression may be more efficient.
- The file format does not support the igz header structure (ID, VERSION, IDXLEN, OFFSETLEN, index/offset pairs); use a different index format or build your own external index.

## Inputs

- indexed gzip file (.igz or .mzML.gz with embedded index metadata)
- integer block or spectrum index (key)
- file path to indexed gzip archive

## Outputs

- parsed index-to-offset dictionary mapping integer indices to byte positions
- decompressed data block for a single requested index
- spectrum object or structured record retrieved by integer key

## How to apply

Extract and decode the gzip header comment field to recover the embedded index metadata: read the ID bytes (2 bytes), VERSION (1 byte), IDXLEN (1 byte), OFFSETLEN (1 byte), followed by variable-length index/offset pairs terminated with a zero byte. Store the parsed pairs in a dictionary mapping integer indices to byte offsets. Implement a __getitem__ method that accepts an integer key, looks up the corresponding offset in the dictionary, seeks to that position in the compressed stream, and decompresses only the requested block. For sequential iteration, implement a read method that tracks the current item ID and increments it on each call. Test the implementation by instantiating the handler with a compressed file path and retrieving a specific block using bracket notation.

## Related tools

- **pymzML** (Python module that reads indexed gzip mzML files and implements random access via header-embedded index parsing) — https://github.com/pymzml/pymzML
- **Python** (Host language for implementing gzip header parsing and __getitem__ methods)
- **xml.etree.ElementTree** (Parse mzML XML structure after decompression to access spectrum metadata)

## Examples

```
run = pymzml.run.Reader('tests/data/BSA1.mzML.gz'); spectrum_with_id_2540 = run[2540]
```

## Evaluation signals

- The parsed dictionary contains all expected integer keys matching the gzip header comment structure, with offsets that are valid byte positions within the file.
- Random access retrieval using bracket notation (e.g., handler[5]) returns correctly decompressed data for the requested index without full file decompression.
- Offset values in the dictionary are monotonically increasing and point to valid gzip block boundaries, allowing the stream to seek and decompress without corruption.
- Sequential iteration via the read method increments the item ID correctly and returns data in the same order as indexed retrieval.
- Spectrum IDs or metadata parsed from the decompressed blocks match the index keys, confirming index-to-data alignment.

## Limitations

- Requires the gzip file to have been created with embedded index metadata in the header comment field (ID, VERSION, IDXLEN, OFFSETLEN format); files lacking this structure cannot be parsed.
- The index must use consistent OFFSETLEN encoding; mismatched or corrupted offset length declarations will cause seek failures.
- Performance gains apply only to random access; if the entire file must be read sequentially, overhead of index parsing may not justify use.
- Index parsing assumes zero-byte termination and proper byte alignment; malformed header comments will silently produce incorrect offset mappings.

## Evidence

- [other] The GSGR class is initialized with a path to an indexed gzip file and supports bracket notation access (e.g., my_Reader.read_block(chap_num)) to retrieve blocks by integer index, with the index-to-offset mapping stored in the gzip header comment field as: ID bytes (2), VERSION (1), IDXLEN (1), OFFSETLEN (1), followed by index/offset pairs terminated with a zero byte.: "the index-to-offset mapping stored in the gzip header comment field as: ID bytes (2), VERSION (1), IDXLEN (1), OFFSETLEN (1), followed by index/offset pairs terminated with a zero byte"
- [intro] One of the features of pymzML is the ability to (create) and read indexed gzip which allows mzML file sizes to reach the levels of the original RAW format: "One of the features of pymzML is the ability to (create) and read indexed gzip which allows mzML file sizes to reach the levels of the original RAW format"
- [intro] pymzML can also rapidly seek into any uncompressed mzML file, no matter if an index was included into the file or not: "pymzML can also rapidly seek into any uncompressed mzML file, no matter if an index was included into the file or not"
- [other] After this, we need to implement a class, which needs to implement the __getitem__ function for random access, and a read function used to sequentiallly read in data: "implement a class, which needs to implement the __getitem__ function for random access, and a read function used to sequentiallly read in data"
- [readme] pymzML is an extension to Python that offers a) easy access to mass spectrometry (MS) data that allows the rapid development of tools b) a very fast parser for mzML data, the standard mass spectrometry data format c) a set of functions to compare and/or handle spectra d) random access in compressed files: "pymzML is an extension to Python that offers a) easy access to mass spectrometry (MS) data that allows the rapid development of tools b) a very fast parser for mzML data, the standard mass"
