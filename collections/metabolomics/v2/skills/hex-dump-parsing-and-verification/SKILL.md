---
name: hex-dump-parsing-and-verification
description: Use when when implementing or reverse-engineering a custom binary file format (e.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - pymzML
  - Python struct module
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# hex-dump-parsing-and-verification

## Summary

Parse binary file format specifications from hexadecimal dumps and verify correctness of encoded structures by byte-for-byte comparison against reference documentation. This skill is essential when implementing custom binary formats (such as indexed gzip headers) where exact byte layout and field encoding must be validated.

## When to use

When implementing or reverse-engineering a custom binary file format (e.g., igzip comment field encoding) that is documented only as hexadecimal dumps or raw byte sequences, and you need to validate that your encoding implementation produces byte-for-byte identical output to the reference specification.

## When NOT to use

- Input is an already-parsed ASCII or text-based format specification—use text parsing instead.
- The binary format is fully documented in a standards document (RFC, ISO standard) rather than as hex dumps—refer to the standard directly instead of reverse-engineering from dumps.
- Your goal is to *read* an existing binary file, not to *encode* a new one—use existing libraries (e.g., `gzip`, `struct.unpack()`) to parse rather than reimplementing the format.

## Inputs

- Hexadecimal dump or raw byte sequence (reference specification)
- Binary format structure definition (field names, byte widths, order)
- Index-to-offset mapping data (pairs to be encoded)

## Outputs

- Binary-encoded file header or comment field (bytes object)
- Verification report (pass/fail on byte-for-byte comparison)

## How to apply

First, define constant values for all fixed-width binary structures (magic bytes, version fields, length fields) from the hex dump reference. Second, implement binary packing functions using Python's `struct` or `pack` modules to encode variable-length fields (such as index-to-offset pairs) according to specified byte widths (e.g., OFFSETLEN=6 bytes). Third, construct the complete binary structure by concatenating magic bytes, version, length fields, all encoded pairs, and a zero-terminator in the documented order. Fourth, parse the reference hex dump to extract the expected byte sequences. Finally, use byte-by-byte comparison (e.g., `assert generated == reference_bytes`) to verify that your output matches the reference exactly, ensuring field ordering, byte widths, and termination are correct.

## Related tools

- **pymzML** (Implements indexed gzip file header encoding/decoding for mzML data; demonstrates practical application of binary header structure constants and index-to-offset mapping) — https://github.com/pymzml/pymzML
- **Python struct module** (Provides binary packing (`struct.pack()`) and unpacking functions for fixed-width field encoding)

## Examples

```
import struct; idx_bytes = struct.pack('>Q', 2540); offset_bytes = struct.pack('>XXXXXX', 512000); header = b'FU\x01' + struct.pack('>B', 9) + struct.pack('>B', 6) + idx_bytes + offset_bytes + b'\x00'; assert header == reference_hex_dump
```

## Evaluation signals

- Generated binary output is identical (byte-for-byte) to the hex dump reference when compared with `==`
- All fixed-width fields (magic bytes, version, length fields) appear at their documented byte offsets in the output
- Index-to-offset pairs are encoded with correct byte widths (e.g., OFFSETLEN=6 bytes per offset value) and in the correct order
- Null terminator (\x00) appears at the expected position following the last index-to-offset pair
- Length fields (IDXLEN, OFFSETLEN) accurately reflect the actual byte counts of their respective data sections

## Limitations

- Hex dump reference must be complete and accurate; ambiguities or errors in the reference will propagate to the implementation.
- This skill assumes fixed-width encoding; variable-length fields or length-prefixed structures require additional parsing logic not covered by basic byte-for-byte comparison.
- Byte order (endianness) must be explicitly specified or inferred from the reference; the skill provides no automatic endianness detection.
- Reference hex dumps may be incomplete (e.g., showing only header structure without all possible index pairs); extrapolation to unseen data requires domain knowledge.

## Evidence

- [other] The igzip format encodes a custom header in the gzip comment field containing ID bytes (F and U), version byte (1), index length (9 bytes in the example), offset length (6 bytes in the example), followed by index-to-offset mapping pairs, all terminated with a zero byte (\x00).: "The igzip format encodes a custom header in the gzip comment field containing ID bytes (F and U), version byte (1), index length (9 bytes in the example), offset length (6 bytes in the example),"
- [other] Implement binary packing functions to encode index-to-offset pairs as fixed-width tuples according to OFFSETLEN specification.: "Implement binary packing functions to encode index-to-offset pairs as fixed-width tuples according to OFFSETLEN specification."
- [other] Parse the Moby Dick example hex dump provided in the reference documentation to extract expected byte sequences.: "Parse the Moby Dick example hex dump provided in the reference documentation to extract expected byte sequences."
- [other] Compare generated binary output byte-for-byte against the hex dump reference to verify correctness of header encoding.: "Compare generated binary output byte-for-byte against the hex dump reference to verify correctness of header encoding."
- [readme] One of the features of pymzML is the ability to (create) and read indexed gzip which allows mzML file sizes to reach the levels of the original RAW format: "One of the features of pymzML is the ability to (create) and read indexed gzip which allows mzML file sizes to reach the levels of the original RAW format"
