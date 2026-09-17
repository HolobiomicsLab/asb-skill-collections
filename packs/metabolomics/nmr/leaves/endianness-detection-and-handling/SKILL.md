---
name: endianness-detection-and-handling
description: Use when when reading a binary file format with a magic integer or fixed
  checksum field at a known offset, and endianness is not explicitly declared in file
  metadata or header comments.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3307
  - http://edamontology.org/topic_2269
  tools:
  - NMRFx
  techniques:
  - NMR
  license_tier: restricted
  provenance_tier: literature
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

# endianness-detection-and-handling

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Detect and handle byte-order encoding (big-endian vs. little-endian) in binary file formats by validating magic integers and adjusting parsing logic accordingly. This skill is essential when parsing NMR data files (e.g., NV format) where endianness is not declared in metadata and must be inferred from known fixed-value fields.

## When to use

When reading a binary file format with a magic integer or fixed checksum field at a known offset, and endianness is not explicitly declared in file metadata or header comments. Specifically applicable to NMR file formats like NV/NMRViewJ where the magic integer (874032077 in native byte order) serves as both a format identifier and endianness probe.

## When NOT to use

- If the file format explicitly declares endianness in a text header, XML preamble, or separate metadata file—use the declared value instead of inferring.
- If the magic integer is not known or not reliably fixed (e.g., varies by file version or content)—endianness detection via magic will fail or be unreliable.
- If the binary file is already guaranteed to be in native endianness (e.g., pre-converted or platform-specific archive)—skip detection and proceed with native parsing.

## Inputs

- binary file (NV/NMRViewJ format or equivalent with magic integer)
- expected magic integer value (int32, e.g., 874032077)
- byte offset of magic integer (typically 0)

## Outputs

- endianness flag (boolean or string: 'big-endian' / 'little-endian')
- parsed binary header object with byte-swapped fields (if needed)
- JSON-serialized metadata including detected endianness

## How to apply

Read the first 2048 bytes of the input binary file using a random-access binary reader (e.g., RandomAccessFile in Java or buffered I/O in Python). Extract the magic integer from bytes 0–3 and compare it directly against the expected value 874032077. If the comparison succeeds, the file uses native endianness; if it fails, interpret bytes 0–3 as little-endian and re-compare. Set an endianness flag based on the successful match. Use this flag to guide byte-swap operations when parsing all subsequent multi-byte integers and floating-point fields in the header and dimension metadata. Validate consistency by confirming that the declared fileHeaderSize and blockElements align with the parsed structure under the detected endianness.

## Related tools

- **NMRFx** (NMR data processing suite that implements NV file parsing with endianness detection for multi-platform support) — https://github.com/nanalysis/nmrfx

## Evaluation signals

- Magic integer matches expected value (874032077) after detecting endianness.
- Parsed header field values (fileHeaderSize, blockElements, nDim) are consistent with declared structure and reasonable ranges (e.g., 0 ≤ nDim ≤ 8, fileHeaderSize ≈ 2048).
- Dimension metadata offsets (1024 + dim*128 for dim in 0..7) yield valid dimension size, blockSize, and frequency values (e.g., spectrometer frequency > 0, blockElements aligns with product of per-dimension blockSizes).
- JSON serialization of parsed header object round-trips without data loss or NaN values.
- Test file round-trip: write endianness-flagged data back to binary, re-read, and confirm magic integer and header fields match original.

## Limitations

- Magic integer detection is reliable only if the value is truly fixed and unambiguous across file versions; collision with data content is possible but unlikely for a 32-bit value.
- If both big-endian and little-endian interpretations yield valid-looking (but incorrect) metadata, additional validation (e.g., sanity checks on frequency or block count) may be needed to disambiguate.
- Endianness detection via magic integer does not handle platform-specific floating-point encoding (IEEE 754 is assumed); non-standard FP formats require separate treatment.
- The approach assumes the magic integer is positioned at a known fixed offset; formats with variable-length or encrypted headers may require alternative detection strategies.

## Evidence

- [other] Extract and validate the magic integer (bytes 0–3) against the expected value 874032077; if mismatch, test little-endian encoding and set endianness flag accordingly.: "Extract and validate the magic integer (bytes 0–3) against the expected value 874032077; if mismatch, test little-endian encoding and set endianness flag accordingly."
- [other] Read the first 2048 bytes from the input NV file using RandomAccessFile or equivalent binary reader.: "Read the first 2048 bytes from the input NV file using RandomAccessFile or equivalent binary reader."
- [other] Serialize the parsed header object (magic, version, nDim, all dimension metadata, endianness detected) to JSON output file.: "Serialize the parsed header object (magic, version, nDim, all dimension metadata, endianness detected) to JSON output file."
