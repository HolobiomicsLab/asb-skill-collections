---
name: igzip-header-structure-encoding
description: Use when when implementing an igzip parser, decoder, or validator that must interpret the custom header format; when debugging igzip file corruption or encoding errors; or when extending pymzML's igzip support to handle new index schemes.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - pymzML
  - Python struct module
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1093/bioinformatics/bty046
  title: pymzml
evidence_spans: []
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

# igzip-header-structure-encoding

## Summary

Reconstruct and validate the binary header structure of indexed gzip (igzip) files, which encode custom metadata (version, index-offset mappings) in the gzip comment field to enable random-access seeking in compressed mass spectrometry data. This skill is essential for implementing or extending igzip parsers that need to read or write seekable gzip-compressed mzML files.

## When to use

When implementing an igzip parser, decoder, or validator that must interpret the custom header format; when debugging igzip file corruption or encoding errors; or when extending pymzML's igzip support to handle new index schemes. Triggered by the need to map byte offsets in a compressed mzML file back to logical spectrum indices without decompressing the entire file.

## When NOT to use

- Input is an uncompressed mzML file; igzip structure is only relevant to compressed, indexed gzip archives.
- Goal is to read spectrum data directly; header parsing is a prerequisite step only, not sufficient for spectrum retrieval.
- File uses a different random-access compression scheme (e.g., bgzip for genomics) with incompatible header layout.

## Inputs

- igzip-compressed mzML file (binary)
- gzip comment field bytes (extracted from file header)
- hex dump or reference binary sequence of known igzip header

## Outputs

- parsed header dictionary with version, index_length, offset_length fields
- list of (index, offset) tuples decoded from header
- reconstructed binary header bytes (for validation)

## How to apply

Define binary header structure constants matching the igzip specification: magic bytes (ID1=0x1f, ID2=0x8b), a VERSION field (1), and two variable-length fields (IDXLEN and OFFSETLEN) that specify the width in bytes of index and offset values respectively. Parse the gzip comment field sequentially: extract the version byte, read IDXLEN and OFFSETLEN as fixed integers, then iterate through fixed-width (IDXLEN + OFFSETLEN)-byte tuples until encountering a null terminator (\x00). Use Python's struct module to unpack each index-offset pair according to the declared widths. Validate the parsed header by comparing reconstructed binary output byte-for-byte against the original hex dump or known reference (e.g., the Moby Dick igzip example cited in pymzML documentation) to confirm correct interpretation of header encoding.

## Related tools

- **pymzML** (Reference implementation and primary consumer of igzip header parsing; provides Reader class for indexed gzip mzML files and defines igzip file format specification) — https://github.com/pymzml/pymzML
- **Python struct module** (Binary packing/unpacking of fixed-width index-offset tuples according to OFFSETLEN and IDXLEN specifications)

## Examples

```
import struct
header_bytes = b'FU\x01\t\x06'  # F, U, version=1, idxlen=9, offsetlen=6
idx, offsetlen = struct.unpack('B B B B B', header_bytes[:5])
index_offset_pairs = struct.iter_unpack(f'>{idx}sQ', comment_field[5:-1])  # unpack until null byte
```

## Evaluation signals

- Parsed IDXLEN and OFFSETLEN values match the declared lengths in the header (e.g., 9 bytes for index, 6 bytes for offset in the Moby Dick example).
- All index-offset tuples unpack without struct errors and yield sensible integer values (indices ≥ 0, offsets increasing monotonically).
- Reconstructed binary header (magic bytes + version + IDXLEN + OFFSETLEN + all tuples + null terminator) matches the original gzip comment field byte-for-byte.
- Header terminates with exactly one null byte (\x00) with no trailing garbage.
- Index values are unique and monotonically increasing; offset values are positive and increasing.

## Limitations

- Header format is specific to pymzML's igzip variant; other gzip-based indexed formats (bgzip, zran) use different header layouts and are not compatible.
- IDXLEN and OFFSETLEN are fixed at file creation time; changing them requires re-encoding the entire index.
- No cryptographic integrity check (e.g., CRC32 of header); corruption in the comment field cannot be detected without comparing against a known reference.

## Evidence

- [other] The igzip format encodes a custom header in the gzip comment field containing ID bytes (F and U), version byte (1), index length (9 bytes in the example), offset length (6 bytes in the example), followed by index-to-offset mapping pairs, all terminated with a zero byte (\x00).: "The igzip format encodes a custom header in the gzip comment field containing ID bytes (F and U), version byte (1), index length (9 bytes in the example), offset length (6 bytes in the example),"
- [intro] One of the features of pymzML is the ability to (create) and read indexed gzip which allows mzML file sizes to reach the levels of the original RAW format: "One of the features of pymzML is the ability to (create) and read indexed gzip which allows mzML file sizes to reach the levels of the original RAW format"
- [other] Parse the Moby Dick example hex dump provided in the reference documentation to extract expected byte sequences. Compare generated binary output byte-for-byte against the hex dump reference to verify correctness of header encoding.: "Parse the Moby Dick example hex dump provided in the reference documentation to extract expected byte sequences. Compare generated binary output byte-for-byte against the hex dump reference to verify"
