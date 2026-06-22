---
name: file-integrity-validation
description: Use when you have a raw NV (NMRViewJ) binary file and need to confirm it is well-formed before parsing or processing.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0336
  edam_topics:
  - http://edamontology.org/topic_3314
  tools:
  - NMRFx
  techniques:
  - NMR
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# file-integrity-validation

## Summary

Validate binary NV/NMRViewJ file format integrity by reading the fixed 2048-byte header, verifying magic integers, and confirming structural consistency across declared and actual dimensions. This ensures the file is uncorrupted and parseable before downstream NMR spectroscopy processing.

## When to use

You have a raw NV (NMRViewJ) binary file and need to confirm it is well-formed before parsing or processing. Specifically, when the file size is at least 2048 bytes, when you need to detect endianness, or when you suspect header corruption due to incomplete transfer, truncation, or format mismatch.

## When NOT to use

- Input file is not in NV binary format (e.g., mzML, FASTQ, NetCDF, or text-based formats); use format-specific validators instead.
- File size is less than 2048 bytes; header cannot be complete and validation will fail.
- You only need to check file existence or overall byte count, not structural correctness; this skill is overkill for simple presence checks.

## Inputs

- binary NV file (raw bytes, ≥2048 bytes)
- target byte-order assumption (default: native; fallback: little-endian)

## Outputs

- validated header metadata object (JSON)
- endianness flag (big-endian or little-endian)
- structured dimension array (nDim entries, each with size, blockSize, nBlocks, sf, sw, refpt, refval, refunits, label, complex, freqdomain, ph0, ph1, vsize)

## How to apply

Read the first 2048 bytes from the input NV file using a binary reader (e.g., RandomAccessFile or equivalent). Extract bytes 0–3 as the magic integer and compare against the expected value 874032077 in native byte order; if mismatch, test little-endian encoding and record the detected endianness flag. Parse file-level header fields (bytes 4–28): version, fileHeaderSize, blockHeaderSize, blockElements, and nDim as integers in the detected byte order. For each of the nDim declared dimensions (0 to 7), read the 128-byte dimension section starting at offset 1024 + dim*128, extracting size, blockSize, nBlocks, and metadata fields. Validate consistency by confirming fileHeaderSize matches the declared size and by checking that blockElements aligns with the product of per-dimension blockSizes. If all checks pass, serialize the header metadata (magic, version, nDim, dimension details, detected endianness) to a JSON output file for logging and downstream verification.

## Related tools

- **NMRFx** (NMR spectroscopy data processing and analysis platform; provides file format specifications and header parsing routines for NV files.) — https://github.com/nanalysis/nmrfx

## Evaluation signals

- Magic integer (bytes 0–3) matches expected value 874032077 after endianness correction.
- fileHeaderSize field matches the declared header size (2048 bytes or specified value).
- blockElements equals the product of blockSize values across all nDim dimensions.
- nDim is in valid range (0–7) and all nDim dimension sections are readable without offset overflow.
- Endianness flag is consistently applied across all header field reads; re-parsing with detected byte order yields identical metadata on second pass.
- JSON serialization of header is valid and contains all required fields without null or NaN values outside expected ranges.

## Limitations

- Magic integer check assumes little-endian fallback; files with other byte orders not representable in the 874032077 constant will be misclassified unless explicit byte-order flags are present in the file or metadata.
- Validation confirms structural consistency but does not verify actual spectroscopy data integrity or content; a valid header does not guarantee valid FID or spectrum blocks downstream.
- Dimension parsing is hardcoded to a maximum of 8 dimensions (indices 0–7); files declaring nDim > 8 will be rejected or truncated.
- The 128-byte per-dimension offset is fixed; if a file variant uses a different dimension section size, this validator will misalign and produce garbage metadata.

## Evidence

- [other] Extract and validate the magic integer (bytes 0–3) against the expected value 874032077; if mismatch, test little-endian encoding and set endianness flag accordingly.: "Extract and validate the magic integer (bytes 0–3) against the expected value 874032077; if mismatch, test little-endian encoding and set endianness flag accordingly."
- [other] Read the first 2048 bytes from the input NV file using RandomAccessFile or equivalent binary reader.: "Read the first 2048 bytes from the input NV file using RandomAccessFile or equivalent binary reader."
- [other] Validate consistency: confirm fileHeaderSize matches declared size and blockElements aligns with product of per-dimension blockSizes.: "Validate consistency: confirm fileHeaderSize matches declared size and blockElements aligns with product of per-dimension blockSizes."
- [other] Parse file-level header fields (bytes 4–28): version, fileHeaderSize, blockHeaderSize, blockElements, nDim, returning each as an integer.: "Parse file-level header fields (bytes 4–28): version, fileHeaderSize, blockHeaderSize, blockElements, nDim, returning each as an integer."
