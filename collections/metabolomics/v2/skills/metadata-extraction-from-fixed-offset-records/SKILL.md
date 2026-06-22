---
name: metadata-extraction-from-fixed-offset-records
description: Use when you have a binary file (e.g., NV format) with a known fixed-size header block (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3520
  tools:
  - NMRFx
derived_from:
- doi: 10.1038/s42004-025-01812-8
  title: NMRFx
evidence_spans:
- github.com__nanalysis__nmrfx
- github.com/nanalysis/nmrfx
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_nmrfx_cq
    doi: 10.1038/s42004-025-01812-8
    title: NMRFx
  dedup_kept_from: coll_nmrfx_cq
schema_version: 0.2.0
---

# metadata-extraction-from-fixed-offset-records

## Summary

Extract and validate structured metadata from binary files with fixed-offset record layouts by reading at known byte positions, validating magic numbers and field consistency, and serializing parsed headers to structured output. Essential for reverse-engineering and parsing proprietary NMR file formats where header structure is known but parsing tools are unavailable.

## When to use

You have a binary file (e.g., NV format) with a known fixed-size header block (e.g., 2048 bytes) containing magic integers, version fields, and dimensioned metadata at fixed byte offsets, and you need to extract, validate, and serialize these fields for downstream analysis or format conversion.

## When NOT to use

- Input file has variable-length or self-describing headers (e.g., XML, HDF5, NetCDF) — use a format-specific parser instead.
- Byte offsets or record structure are unknown or undocumented — reverse engineering is required before this skill applies.
- Magic number validation is not applicable or the file format lacks a magic integer sentinel — use alternative validation (e.g., file extension, content heuristics).

## Inputs

- binary file with fixed-offset header structure (e.g., NV file)
- byte-offset map and expected magic integer value
- dimension count and per-dimension record size

## Outputs

- parsed header object (magic, version, endianness, nDim, dimension metadata)
- JSON serialization of header metadata
- endianness flag (big-endian or little-endian)

## How to apply

Read the first fixed-size header block (e.g., 2048 bytes) from the binary file using a binary reader (RandomAccessFile or equivalent). Extract the magic integer at bytes 0–3 and validate it against the expected value (e.g., 874032077 for NV files); test little-endian encoding if big-endian fails and record the detected endianness. Parse all file-level header fields (e.g., version, fileHeaderSize, blockHeaderSize, blockElements, nDim) from the designated byte ranges as integers. For each declared dimension (0 to nDim − 1), read the fixed-size dimension record (e.g., 128 bytes at offset 1024 + dim × 128) and extract all subfields (size, blockSize, nBlocks, spectrometer frequency, sweep width, reference point, reference value, reference units, label, complex flag, freqdomain flag, phase angles, vsize). Cross-validate consistency: confirm fileHeaderSize matches the declared header size and blockElements aligns with the product of per-dimension blockSizes. Serialize all parsed metadata (magic, version, nDim, all dimension records, detected endianness) to a structured JSON output file for programmatic access.

## Related tools

- **NMRFx** (NMR file format library and visualization tool supporting NV file parsing and header extraction) — https://github.com/nanalysis/nmrfx

## Evaluation signals

- Magic integer extracted at bytes 0–3 matches expected value (874032077) or valid little-endian variant.
- fileHeaderSize field matches the declared 2048-byte header block size.
- blockElements product (nBlocks₀ × nBlocks₁ × … × nBlocksₙ) matches declared blockElements.
- All dimension records parse without out-of-bounds reads; nDim ≤ 8 and each dimension offset is within the 2048-byte header.
- JSON serialization is valid and round-trips: re-reading parsed JSON reproduces original byte offsets and field values.

## Limitations

- Endianness detection relies on magic-number mismatch; files with corrupted or non-standard magic integers may be misclassified or fail validation.
- Fixed-offset parsing assumes the header structure is invariant across file versions; version changes that alter field positions or sizes will break compatibility.
- No error recovery: if any fixed-offset read fails (e.g., file is truncated), the entire parse halts; partial header recovery is not implemented.
- Dimension metadata is assumed to occupy contiguous 128-byte records starting at offset 1024; non-standard layouts or padding schemes are not detected.

## Evidence

- [other] Read the first 2048 bytes from the input NV file using RandomAccessFile or equivalent binary reader.: "Read the first 2048 bytes from the input NV file using RandomAccessFile or equivalent binary reader."
- [other] Extract and validate the magic integer (bytes 0–3) against the expected value 874032077; if mismatch, test little-endian encoding and set endianness flag accordingly.: "Extract and validate the magic integer (bytes 0–3) against the expected value 874032077; if mismatch, test little-endian encoding and set endianness flag accordingly."
- [other] Parse file-level header fields (bytes 4–28): version, fileHeaderSize, blockHeaderSize, blockElements, nDim, returning each as an integer.: "Parse file-level header fields (bytes 4–28): version, fileHeaderSize, blockHeaderSize, blockElements, nDim, returning each as an integer."
- [other] For each of nDim dimensions (0 to 7), read the 128-byte dimension section starting at offset 1024 + dim*128: "For each of nDim dimensions (0 to 7), read the 128-byte dimension section starting at offset 1024 + dim*128"
- [other] Validate consistency: confirm fileHeaderSize matches declared size and blockElements aligns with product of per-dimension blockSizes.: "Validate consistency: confirm fileHeaderSize matches declared size and blockElements aligns with product of per-dimension blockSizes."
