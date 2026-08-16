---
name: binary-data-base64-encoding
description: Use when when converting simulated or real LC/GC-MS spectral data (m/z–retention-time
  intensity matrices) into mzML format for archival, sharing, or downstream processing.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0335
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0092
  tools:
  - R
  - base64enc
  - mzrtsim
  techniques:
  - GC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.5c01213
  title: mzrtsim
evidence_spans:
- if (!requireNamespace("BiocManager", quietly = TRUE)) install.packages("BiocManager")
  BiocManager::install("mzrtsim")
- The underlying engine handles binary data encoding via the `base64enc` package
- github.com__yufree__mzrtsim
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mzrtsim_cq
    doi: 10.1021/acs.analchem.5c01213
    title: mzrtsim
  dedup_kept_from: coll_mzrtsim_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c01213
  all_source_dois:
  - 10.1021/acs.analchem.5c01213
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# binary-data-base64-encoding

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Encode mass spectrometry spectral data matrices as Base64-formatted binary strings for embedding in mzML XML file structures. This skill bridges raw numerical MS intensity arrays with the mzML standard's requirement for compact, XML-compatible binary representation.

## When to use

When converting simulated or real LC/GC-MS spectral data (m/z–retention-time intensity matrices) into mzML format for archival, sharing, or downstream processing. Specifically, after synthesizing chromatographic peak shapes and noise in a numerical matrix, and before writing XML scan headers and precursor metadata.

## When NOT to use

- Input is already a feature table (aggregated m/z × sample matrix); use binary encoding only for raw spectral data matrices.
- Output format is NetCDF or other non-XML MS format; Base64 encoding is mzML-specific.
- Data is intended for human inspection or statistical reporting; Base64 is opaque and requires decoding.

## Inputs

- numeric matrix: m/z–retention-time intensity array (rows = m/z bins, columns = retention-time scans)
- mzML XML template or skeleton with pre-defined scan structure
- metadata: scan number, MS level, precursor m/z (if MS2), collision energy, ionization mode

## Outputs

- Base64-encoded binary string suitable for mzML <binary> element
- mzML XML file with embedded Base64-encoded spectral data
- accompanying CSV ground-truth file (m/z, retention_time, database_intensity, sim_ins, compound_name)

## How to apply

After generating a mass spectrometry intensity matrix (either from real spectral database records or synthetic simulation), serialize the numerical array to binary format, then encode it as Base64 using the base64enc package. The encoded string is then inserted into the mzML XML structure as the content of a binary data array element (e.g., within a <binary> tag). The mzML writer handles this encoding internally without requiring external MS data libraries like mzR. Ensure the byte order and bit depth match the mzML schema declaration (typically 32-bit or 64-bit float).

## Related tools

- **base64enc** (Encodes numerical spectral matrices to Base64 strings for mzML XML embedding)
- **mzrtsim** (Generates simulated LC/GC-MS raw data and handles mzML file writing with Base64 encoding) — https://github.com/yufree/mzrtsim
- **R** (Host language for base64enc and mzML I/O operations)

## Examples

```
library(mzrtsim); data('monams1'); simmzml(db=monams1, name='test')
```

## Evaluation signals

- Encoded string is valid Base64 (regex: ^[A-Za-z0-9+/]*={0,2}$) and decodes to original byte length without error.
- Decoded binary array matches original m/z–retention-time intensity matrix in shape and data type (float precision).
- mzML file parses without XML schema validation errors and binary elements can be read by standard mzML parsers.
- File size reduction: Base64-encoded mzML is typically 33% larger than raw binary but much smaller than unencoded text representation.
- Round-trip test: decode Base64 string from generated mzML, compare intensity values to ground-truth CSV sim_ins column for exact match (or within floating-point precision).

## Limitations

- Base64 encoding increases file size by ~33% compared to raw binary; trade-off is XML compatibility and human-readability of non-binary metadata.
- Floating-point precision may be lost during serialization depending on bit depth (32 vs 64 bit); must match mzML schema declaration.
- Base64 encoding is computationally inexpensive but requires full matrix to be held in memory; very large high-resolution MS datasets may require chunking or streaming.
- mzML standard requires specific byte order (little-endian) and compression options (zlib, none); encoding must respect these constraints or downstream parsers may fail.

## Evidence

- [intro] The underlying engine handles binary data encoding via the `base64enc` package: "The underlying engine handles binary data encoding via the `base64enc` package"
- [other] Encode the resulting mass spectrometry matrix in base64 format and write to .mzML file structure: "Encode the resulting mass spectrometry matrix in base64 format and write to .mzML file structure using base64enc package."
- [readme] The native mzML writer handles the binary encoding (Base64) internally without requiring external MS data libraries: "The native mzML writer handles the binary encoding (Base64) internally without requiring external MS data libraries."
- [other] Encode the combined spectral data (noise + optional matrix) as base64-encoded binary using the base64enc package: "Encode the combined spectral data (noise + optional matrix) as base64-encoded binary using the base64enc package."
