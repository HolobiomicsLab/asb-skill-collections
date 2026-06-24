---
name: binary-file-format-parsing
description: Use when you encounter a proprietary or undocumented binary file (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3520
  tools:
  - NMRFx
  techniques:
  - NMR
  license_tier: restricted
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s42004-025-01812-8
  all_source_dois:
  - 10.1038/s42004-025-01812-8
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# binary-file-format-parsing

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Parse and validate binary file format headers by reading fixed-size byte blocks, extracting and verifying magic integers and metadata fields, and deserializing structured header content into machine-readable output. This skill is essential for interpreting proprietary or domain-specific file formats (e.g., NMR data archives) where header structure and endianness detection are prerequisites for downstream analysis.

## When to use

Apply this skill when you encounter a proprietary or undocumented binary file (e.g., NV/NMRViewJ format) where you need to (1) verify file integrity via magic-number validation, (2) extract instrument metadata (dimensions, frequencies, block structure) from a fixed-offset header region, or (3) establish endianness and format versioning before reading spectroscopic or array data. Triggered when raw binary input lacks schema documentation and manual hex inspection reveals fixed byte offsets for header fields.

## When NOT to use

- Input is not a binary file or lacks a fixed-size header structure (e.g., streaming or variable-length format)
- File format and byte offsets are unknown and cannot be reverse-engineered or documented
- Header has already been parsed and deserialized by upstream tools; skip to downstream processing

## Inputs

- Binary file (NV/NMRViewJ format) with fixed 2048-byte header
- Magic integer reference value (874032077)
- Byte offset map (header at 0–28, dimension records at 1024 + dim × 128)

## Outputs

- Parsed header object (JSON): magic, version, fileHeaderSize, blockHeaderSize, blockElements, nDim, dimension metadata array, detected endianness flag
- Validation report: magic-number match status, endianness determination, consistency checks on blockElements and fileHeaderSize

## How to apply

Open the binary file using a RandomAccessFile or low-level binary reader and read the first 2048 bytes into memory. Extract and validate the magic integer (bytes 0–3, expected value 874032077); if the value does not match, test little-endian encoding and set an endianness flag accordingly. Parse file-level header fields from bytes 4–28 (version, fileHeaderSize, blockHeaderSize, blockElements, nDim) as integers. For each declared dimension (0 to nDim − 1), seek to offset 1024 + dim × 128 and extract the 128-byte dimension record, which contains: size, blockSize, nBlocks, spectrometer frequency (sf), sweep width (sw), reference point (refpt), reference value (refval), reference units (refunits), label (16-character string), and per-dimension flags (complex, freqdomain, zero-order phase ph0, first-order phase ph1, vsize). Validate consistency by confirming fileHeaderSize matches the declared size and blockElements aligns with the product of per-dimension blockSizes. Serialize the complete parsed header (magic, version, nDim, all dimension metadata, detected endianness) to a JSON output file for downstream tools.

## Related tools

- **NMRFx** (NMR data processing and visualization platform; uses parsed NV file headers to load and manipulate spectroscopic datasets) — https://github.com/nanalysis/nmrfx

## Evaluation signals

- Magic integer matches 874032077 (or correctly identified as little-endian; endianness flag is consistent across all subsequent reads)
- Parsed version, fileHeaderSize, blockHeaderSize, and nDim values are integers ≥ 0 and within expected ranges for the NMR instrument
- For each dimension: size, blockSize, nBlocks are positive integers; sf (frequency) and sw (sweep width) are in expected physical ranges (MHz, ppm); label is a valid 16-character string; blockElements product equals blockHeaderSize constraint
- fileHeaderSize equals the declared byte offset (typically 2048) and is consistent with the number of dimension records (nDim × 128 bytes)
- JSON output is valid, schema-complete, and round-trips without loss when re-read by downstream tools

## Limitations

- Magic-number validation is brittle if the file has been corrupted or truncated; truncation below 2048 bytes will cause read failure
- Endianness detection relies on comparing two candidate magic integers; ambiguity arises if both match by chance (rare but possible in corrupted files)
- Dimension metadata extraction assumes exactly nDim dimension records at fixed offsets; files with dynamic or variable-length dimension sections will fail
- No validation of physical plausibility for frequency or phase values; nonsensical metadata will be accepted if the byte offsets and types are correct

## Evidence

- [other] Read the first 2048 bytes from the input NV file using RandomAccessFile or equivalent binary reader.: "Read the first 2048 bytes from the input NV file using RandomAccessFile or equivalent binary reader."
- [other] Extract and validate the magic integer (bytes 0–3) against the expected value 874032077; if mismatch, test little-endian encoding and set endianness flag accordingly.: "Extract and validate the magic integer (bytes 0–3) against the expected value 874032077; if mismatch, test little-endian encoding and set endianness flag accordingly."
- [other] For each of nDim dimensions (0 to 7), read the 128-byte dimension section starting at offset 1024 + dim*128, extracting: size, blockSize, nBlocks, spectrometer frequency (sf), sweep width (sw), reference point (refpt), reference value (refval), reference units (refunits), label (16-char string), complex flag, freqdomain flag, zero-order phase (ph0), first-order phase (ph1), and vsize.: "For each of nDim dimensions (0 to 7), read the 128-byte dimension section starting at offset 1024 + dim*128, extracting: size, blockSize, nBlocks, spectrometer frequency (sf), sweep width (sw),"
- [other] Serialize the parsed header object (magic, version, nDim, all dimension metadata, endianness detected) to JSON output file.: "Serialize the parsed header object (magic, version, nDim, all dimension metadata, endianness detected) to JSON output file."
