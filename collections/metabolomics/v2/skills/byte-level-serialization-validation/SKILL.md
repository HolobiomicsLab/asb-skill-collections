---
name: byte-level-serialization-validation
description: Use when when you have implemented a binary file format encoder (such as igzip header construction) and need to verify that the binary output is correct before deploying it to read or write real files.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0335
  edam_topics:
  - http://edamontology.org/topic_3372
  - http://edamontology.org/topic_0091
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# byte-level-serialization-validation

## Summary

Validate binary file format encoding by reconstructing known structures, serializing them to bytes, and performing byte-for-byte comparison against reference hex dumps. This skill ensures correct implementation of custom binary protocols (e.g., indexed gzip headers) by verifying that generated output matches expected binary sequences.

## When to use

When you have implemented a binary file format encoder (such as igzip header construction) and need to verify that the binary output is correct before deploying it to read or write real files. Specifically, when you have access to a reference hex dump or known-good binary example and want to ensure round-trip serialization correctness.

## When NOT to use

- Input is a text-based format (JSON, XML, CSV) — use text-level schema or content validation instead.
- No reference binary example or hex dump is available — byte-level validation requires a ground truth to compare against.
- The file format specification is ambiguous or incomplete — clarify structure before attempting serialization.

## Inputs

- Binary format specification document (structure, field widths, magic bytes, terminator conventions)
- Reference hex dump or known-good binary file excerpt
- Index-to-offset mapping data (e.g., list of tuples to encode)

## Outputs

- Validated binary-encoded header or file section
- Byte-for-byte comparison report (pass/fail)
- Identified encoding errors (if any)

## How to apply

First, define the binary structure as fixed-width fields and constants (magic bytes, version, length fields, terminator bytes). Implement packing functions that encode index-to-offset pairs or other variable-length data according to the format specification (e.g., OFFSETLEN byte width). Construct the complete binary header by concatenating all packed components in order. Then, parse the provided reference hex dump to extract expected byte sequences. Finally, compare generated output byte-for-byte against the reference hex dump; any mismatch indicates an encoding error in field order, width, endianness, or termination.

## Related tools

- **pymzML** (Parses and validates mzML files that may use indexed gzip (igzip) format with custom binary headers; provides Reader API for random access seeking into compressed files) — https://github.com/pymzml/pymzML
- **Python** (Provides struct module for binary packing/unpacking, hexdump utilities, and byte-string comparison for serialization validation)

## Examples

```
import struct; igzip_header = b'FU' + b'\x01' + struct.pack('>I', 9) + struct.pack('>I', 6) + b'\x00'; print(igzip_header.hex())
```

## Evaluation signals

- Generated binary output matches reference hex dump byte-for-byte with no differences.
- Field offsets and byte widths (e.g., IDXLEN, OFFSETLEN) are correct according to the specification.
- Magic bytes, version byte, and terminator byte (\x00) are in the correct positions.
- Index-to-offset pairs are packed using the correct byte width and appear in the correct order within the header.
- Hex dump can be parsed back into the original index-to-offset tuples with no data loss (round-trip validation).

## Limitations

- Byte-level validation only detects structural correctness; it does not verify semantic validity (e.g., whether offsets actually point to valid data in the file).
- Requires access to a reliable reference hex dump or known-good binary example — if the reference itself is incorrect, validation will pass incorrect encodings.
- Does not account for platform-specific endianness or floating-point representation unless explicitly specified in the format.
- Validation is brittle to format changes; any modification to the specification requires updating both the encoder and the reference example.

## Evidence

- [other] The igzip format encodes a custom header in the gzip comment field containing ID bytes (F and U), version byte (1), index length (9 bytes in the example), offset length (6 bytes in the example), followed by index-to-offset mapping pairs, all terminated with a zero byte (\x00).: "The igzip format encodes a custom header in the gzip comment field containing ID bytes (F and U), version byte (1), index length (9 bytes in the example), offset length (6 bytes in the example),"
- [other] Compare generated binary output byte-for-byte against the hex dump reference to verify correctness of header encoding.: "Compare generated binary output byte-for-byte against the hex dump reference to verify correctness of header encoding."
- [intro] One of the features of pymzML is the ability to (create) and read indexed gzip which allows mzML file sizes to reach the levels of the original RAW format: "One of the features of pymzML is the ability to (create) and read indexed gzip which allows mzML file sizes to reach the levels of the original RAW format"
- [other] Implement binary packing functions to encode index-to-offset pairs as fixed-width tuples according to OFFSETLEN specification.: "Implement binary packing functions to encode index-to-offset pairs as fixed-width tuples according to OFFSETLEN specification."
