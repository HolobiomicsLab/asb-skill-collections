---
name: nv-header-structure-interpretation
description: Use when you have a raw NV file from NMRViewJ or compatible NMR acquisition software and need to extract header metadata before processing spectroscopic data.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0593
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

# nv-header-structure-interpretation

## Summary

Parse and validate the binary header structure of NV (NMRViewJ) format files, extracting magic number, version, dimensionality, and per-dimension metadata (size, blockSize, frequency, phase, labels). This skill is essential for correctly reading NMR spectroscopy data files and detecting endianness mismatches early in the pipeline.

## When to use

You have a raw NV file from NMRViewJ or compatible NMR acquisition software and need to extract header metadata before processing spectroscopic data. Specifically: the file is binary (not text), you do not yet know the endianness or dimensionality, or you need to validate file integrity before attempting block-level data extraction.

## When NOT to use

- Input is already a text-based format (e.g., ASCII NMR data, CSV export) — use direct text parsing instead.
- Header has already been extracted and validated in a prior pipeline stage — reuse the cached JSON header.
- File is corrupted or truncated below 2048 bytes — early failure is appropriate; do not attempt recovery here.

## Inputs

- binary NV file (first 2048 bytes minimum)
- file path or file handle to NV-format spectroscopy data

## Outputs

- parsed header object (JSON-serializable dictionary or file)
- endianness flag (big-endian or little-endian)
- dimension metadata array (size, blockSize, nBlocks, frequency, phase, labels per dimension)
- validation status (pass/fail with diagnostic message)

## How to apply

Read the first 2048 bytes of the input NV file using a binary reader (RandomAccessFile or equivalent). Extract bytes 0–3 and validate the magic integer against the expected value 874032077; if validation fails, test little-endian encoding and set an endianness flag. Parse file-level header fields (bytes 4–28) as integers: version, fileHeaderSize, blockHeaderSize, blockElements, and nDim. For each dimension (0 to nDim−1), read the 128-byte dimension section starting at offset 1024 + dim×128, extracting size, blockSize, nBlocks, spectrometer frequency (sf), sweep width (sw), reference point (refpt), reference value (refval), reference units (refunits), a 16-character label string, and phase and domain flags (complex, freqdomain, ph0, ph1, vsize). Validate consistency: confirm that fileHeaderSize matches the declared header size and that blockElements aligns with the product of per-dimension blockSizes. Serialize the complete parsed header object (magic, version, nDim, all dimension metadata, detected endianness) to a JSON output file for downstream stages.

## Related tools

- **NMRFx** (NMR data processing suite that defines and uses the NV file format; provides reference implementation for header parsing and block-level data I/O) — https://github.com/nanalysis/nmrfx

## Evaluation signals

- Magic integer matches 874032077 (or correct byte-swapped value after endianness detection)
- fileHeaderSize field equals 2048 (or stated alternative); blockHeaderSize and blockElements are positive integers consistent with dimension declarations
- All nDim dimension sections (0 to nDim−1) parse without out-of-bounds reads; each label is ≤16 characters; size, blockSize, nBlocks are positive
- Consistency check passes: product of per-dimension blockSizes equals declared blockElements
- JSON output is schema-valid and round-trips (re-parsing the JSON yields identical field values)
- Endianness detection is unambiguous: either big-endian OR little-endian yields a valid magic number; conflicts indicate corruption

## Limitations

- Magic integer validation assumes the file conforms to NMRViewJ spec; non-standard or corrupted headers will fail early with no recovery path.
- Endianness is detected heuristically via magic-number byte-swap; ambiguous endianness (neither order yields a recognized magic) will cause parsing to halt.
- Dimension metadata is assumed to fit exactly in 128-byte sections at offset 1024 + dim×128; files with non-standard padding or layout will misparse.
- No support for NV format extensions or vendor-specific variants; only the documented fixed-size 2048-byte header and standard dimension fields are parsed.

## Evidence

- [other] Extract and validate the magic integer (bytes 0–3) against the expected value 874032077; if mismatch, test little-endian encoding and set endianness flag accordingly.: "Extract and validate the magic integer (bytes 0–3) against the expected value 874032077; if mismatch, test little-endian encoding"
- [other] Read the first 2048 bytes from the input NV file using RandomAccessFile or equivalent binary reader.: "Read the first 2048 bytes from the input NV file using RandomAccessFile or equivalent binary reader"
- [other] For each of nDim dimensions (0 to 7), read the 128-byte dimension section starting at offset 1024 + dim*128, extracting: size, blockSize, nBlocks, spectrometer frequency (sf), sweep width (sw), reference point (refpt), reference value (refval), reference units (refunits), label (16-char string), complex flag, freqdomain flag, zero-order phase (ph0), first-order phase (ph1), and vsize.: "For each of nDim dimensions (0 to 7), read the 128-byte dimension section starting at offset 1024 + dim*128"
- [other] Validate consistency: confirm fileHeaderSize matches declared size and blockElements aligns with product of per-dimension blockSizes.: "Validate consistency: confirm fileHeaderSize matches declared size and blockElements aligns with product of per-dimension blockSizes"
- [abstract] NMRFx is referenced as the tool for NMR processing and NV file format handling.: "github.com/nanalysis/nmrfx"
