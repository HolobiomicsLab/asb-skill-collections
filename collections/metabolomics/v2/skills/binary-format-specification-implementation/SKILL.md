---
name: binary-format-specification-implementation
description: Use when you have a compressed file format (e.g., igzip) with a custom binary header structure that encodes metadata (index-to-offset mappings) in a fixed layout, and you need to parse or generate compliant files.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3359
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3173
  tools:
  - pymzML
  - Python
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

# binary-format-specification-implementation

## Summary

Implement a binary file format specification by defining header structure constants, encoding index-to-offset pairs as fixed-width tuples, and verifying byte-for-byte correctness against reference hex dumps. This skill is essential for enabling random access in compressed scientific data files like indexed gzip (igzip) used in mass spectrometry data.

## When to use

You have a compressed file format (e.g., igzip) with a custom binary header structure that encodes metadata (index-to-offset mappings) in a fixed layout, and you need to parse or generate compliant files. Specifically, when you need to enable rapid random-access seeking into compressed scientific data without decompressing the entire file.

## When NOT to use

- Your file format uses variable-length encoding (e.g., varint, UTF-8) without fixed-width fields — this skill assumes fixed-width tuples.
- You are parsing a text-based format (JSON, XML, CSV) — binary format implementation is specific to binary protocols.
- The header structure is undocumented or changes per file — this skill requires a stable, reproducible specification.

## Inputs

- Binary file format specification document (with magic bytes, field sizes, encoding rules)
- Reference hex dump or binary file example (e.g., igzip header from Moby Dick example)
- Index-to-offset mapping data (list of tuples: index values and their byte offsets)

## Outputs

- Binary-encoded header bytes conforming to the specification
- Validated byte-for-byte comparison result (match/mismatch with reference)
- Encoded index-to-offset pairs in fixed-width format

## How to apply

First, define binary structure constants for magic bytes, version fields, and variable-length fields (index length, offset length). Implement binary packing functions that encode index-to-offset pairs as tuples with fixed widths matching the OFFSETLEN specification (e.g., 6 bytes for offsets). Construct the complete header by concatenating magic bytes (ID1, ID2), version byte, length fields, all index-to-offset pairs in sequence, and a zero-byte terminator. Parse a reference hex dump or known-good file to extract expected byte sequences. Finally, compare generated binary output byte-for-byte against the reference to verify correctness; any mismatch indicates errors in field widths, byte order, or packing logic.

## Related tools

- **pymzML** (Implements igzip parsing and random-access seeking for compressed mzML files; demonstrates the binary header encoding and decoding for indexed gzip format) — https://github.com/pymzml/pymzML
- **Python** (Language for implementing binary packing/unpacking via struct module and byte manipulation; used to construct and validate igzip headers)

## Examples

```
import struct; header = b'FU' + b'\x01' + struct.pack('>Q', 9) + struct.pack('>Q', 6) + b''.join(struct.pack('>QB', idx, offset) for idx, offset in [(0, 0), (100, 512)]) + b'\x00'; assert header[:10] == b'FU\x01\x00\x00\x00\x00\x00\x00\x09'
```

## Evaluation signals

- Generated binary header matches the reference hex dump byte-for-byte (e.g., magic bytes F and U, version 1, correct length fields)
- Index-to-offset pairs are encoded with the correct fixed width (e.g., 9-byte indices, 6-byte offsets in the igzip example)
- Header is correctly terminated with a null byte (\x00)
- Random-access seeking using the encoded offsets successfully retrieves the correct data chunks from the compressed file
- Round-trip test: encode a header, then parse it back and verify all fields and pairs match the original input

## Limitations

- Requires an explicit, frozen specification of field sizes and byte order; undocumented formats cannot be reliably implemented.
- Fixed-width encoding can waste space for variable-sized indices or offsets; no compression of the metadata itself.
- Byte-order (endianness) must be consistent; mixing big-endian and little-endian in a single header will cause mismatch failures.
- Verification depends on access to a reference hex dump; without one, correctness cannot be validated empirically.

## Evidence

- [other] The igzip format encodes a custom header in the gzip comment field containing ID bytes (F and U), version byte (1), index length (9 bytes in the example), offset length (6 bytes in the example), followed by index-to-offset mapping pairs, all terminated with a zero byte (\x00).: "The igzip format encodes a custom header in the gzip comment field containing ID bytes (F and U), version byte (1), index length (9 bytes in the example), offset length (6 bytes in the example),"
- [intro] One of the features of pymzML is the ability to (create) and read indexed gzip which allows mzML file sizes to reach the levels of the original RAW format: "One of the features of pymzML is the ability to (create) and read indexed gzip which allows mzML file sizes to reach the levels of the original RAW format"
- [other] Implement binary packing functions to encode index-to-offset pairs as fixed-width tuples according to OFFSETLEN specification.: "Implement binary packing functions to encode index-to-offset pairs as fixed-width tuples according to OFFSETLEN specification"
- [other] Compare generated binary output byte-for-byte against the hex dump reference to verify correctness of header encoding.: "Compare generated binary output byte-for-byte against the hex dump reference to verify correctness of header encoding"
