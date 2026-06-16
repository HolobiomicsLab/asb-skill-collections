---
name: random-access-index-implementation
description: Use when you have a large compressed scientific data file (e.g., indexed gzip mzML) where you need to retrieve specific spectra, chapters, or records by integer ID without loading the entire file into memory.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - xml.etree.ElementTree
  - pymzML
  - Python
derived_from:
- doi: 10.1093/bioinformatics/bty046
  title: pymzml
evidence_spans:
- import xml.etree.ElementTree as et
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pymzml
    doi: 10.1093/bioinformatics/bty046
    title: pymzml
  dedup_kept_from: coll_pymzml
schema_version: 0.2.0
---

# random-access-index-implementation

## Summary

Implement a custom file handler class that parses embedded index metadata from a compressed file header and provides bracket-notation access to retrieve specific data blocks by integer key without decompressing the entire file. This skill enables rapid, seek-based access to large compressed scientific data files (e.g., mzML.gz) by storing an index-to-offset mapping in the gzip header comment field.

## When to use

You have a large compressed scientific data file (e.g., indexed gzip mzML) where you need to retrieve specific spectra, chapters, or records by integer ID without loading the entire file into memory. The file must contain an embedded index structure (ID bytes, VERSION, IDXLEN, OFFSETLEN, followed by index/offset pairs) in the gzip header comment field to enable direct byte-offset lookup.

## When NOT to use

- Input file is uncompressed or compressed without an embedded index structure—use sequential parsing instead.
- Data file does not conform to the GSGR header format (missing ID bytes, VERSION, or IDXLEN/OFFSETLEN fields)—validate file structure before attempting index extraction.
- Entire file must be accessed sequentially in order; random access overhead is not justified—use streaming decompression.

## Inputs

- indexed gzip file (.igz or .mzML.gz) with GSGR index metadata in header comment field
- integer key (spectrum/block ID)
- file path string to compressed data source

## Outputs

- decompressed data block (e.g., spectrum object, chapter text)
- dictionary mapping integer indices to byte offsets
- iterator over sequential blocks

## How to apply

Parse the gzip file header to extract and decode the embedded index metadata into a dictionary mapping integer indices to byte offsets. Implement a `__getitem__` method that accepts an integer key, queries the index dictionary for the corresponding byte offset, seeks to that position in the compressed stream, and decompresses only the requested block. Optionally implement a `read()` method for sequential iteration by tracking the current item ID and incrementing it on each call. Validate that the file format matches the expected GSGR structure (ID bytes, VERSION field, IDXLEN and OFFSETLEN bytes, then index/offset pairs terminated with a zero byte). Test random access by instantiating the handler with the compressed file path and retrieving a specific item using bracket notation (e.g., `handler[5]`).

## Related tools

- **pymzML** (Reader class that implements indexed gzip random access for mzML files via __getitem__ method and supports custom regex patterns for non-standard index identifiers) — https://github.com/pymzml/pymzML
- **Python** (Language and runtime for implementing the custom file handler class, index parsing logic, and bracket-notation access)
- **xml.etree.ElementTree** (XML parsing library used within pymzML to parse mzML file structure and spectrum metadata after byte-offset seek)

## Examples

```
run = pymzml.run.Reader('tests/data/BSA1.mzML.gz'); spectrum_with_id_2540 = run[2540]
```

## Evaluation signals

- Successfully parse the gzip header comment field and extract all index/offset pairs without corruption (verify against file size and offset monotonicity).
- Bracket-notation access returns the correct decompressed block for each integer key (validate by comparing checksums or content hashes with reference decompressed data).
- Sequential read() calls return blocks in order and terminate cleanly; iterator does not skip or duplicate items.
- Seek-based random access is significantly faster than full-file decompression for retrieving single blocks (benchmark wall-clock time for handler[N] vs. sequential parse to item N).
- No index mismatch errors; verify that offset dictionary keys match the actual block IDs present in the file header.

## Limitations

- Index metadata must be present and correctly formatted in the gzip header comment field; corrupted or missing index will cause KeyError or silent return of wrong block.
- File structure must conform strictly to GSGR format (ID bytes, VERSION, IDXLEN, OFFSETLEN, index/offset pairs, zero-byte terminator); non-standard variants require custom regex or header parsing logic.
- Requires index-aware file creation at compression time; cannot retroactively add indices to existing non-indexed gzip files.
- Performance gain is most significant for sparse random access; sequential iteration through all blocks may be slower than standard streaming due to repeated seeks and decompress overhead per block.

## Evidence

- [other] the index-to-offset mapping stored in the gzip header comment field as: ID bytes (2), VERSION (1), IDXLEN (1), OFFSETLEN (1), followed by index/offset pairs terminated with a zero byte: "ID bytes (2), VERSION (1), IDXLEN (1), OFFSETLEN (1), followed by index/offset pairs terminated with a zero byte"
- [other] Implement a __getitem__ method that accepts an integer key, queries the index dictionary for the corresponding offset, seeks to that position in the compressed stream, and decompresses only the requested item.: "Implement a __getitem__ method that accepts an integer key, queries the index dictionary for the corresponding offset, seeks to that position in the compressed stream, and decompresses only the"
- [intro] One of the features of pymzML is the ability to (create) and read indexed gzip which allows mzML file sizes to reach the levels of the original RAW format: "the ability to (create) and read indexed gzip which allows mzML file sizes to reach the levels of the original RAW format"
- [other] my_Reader.read_block(chap_num) to retrieve blocks by integer index: "supports bracket notation access (e.g., my_Reader.read_block(chap_num)) to retrieve blocks by integer index"
- [other] After this, we need to implement a class, which needs to implement the __getitem__ function for random access, and a read function used to sequentiallly read in data: "implement a class, which needs to implement the __getitem__ function for random access, and a read function used to sequentiallly read in data"
