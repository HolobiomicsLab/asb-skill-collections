---
name: xml-structured-metadata-construction
description: Use when when you have synthesized or assembled mass spectrometry spectral
  data (m/z values, intensities, retention times) and need to encode it as a portable,
  standard mzML file format rather than a proprietary binary or text representation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3932
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  tools:
  - R
  - base64enc
  - mzrtsim
  - mzR
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
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

# xml-structured-metadata-construction

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Construct properly-formatted mzML XML structures with nested scan headers, precursor metadata, and base64-encoded binary product ion arrays for mass spectrometry data files. This skill is essential for generating standards-compliant MS data files that can be read by downstream analysis software.

## When to use

When you have synthesized or assembled mass spectrometry spectral data (m/z values, intensities, retention times) and need to encode it as a portable, standard mzML file format rather than a proprietary binary or text representation. Specifically required after generating background noise and optional matrix peaks, or after simulating chromatographic peak shapes with realistic isotope and fragment ion distributions.

## When NOT to use

- Input spectral data is already in mzML, NetCDF, or other standard MS format — use file conversion tools instead.
- You only need a feature table (peak list with m/z, RT, intensity) — use peak list simulation (simmzml or mzrtsim) which outputs CSV directly.
- Binary MS data is already encoded and you need only to read it — use mzR or other MS file readers instead of constructing XML.

## Inputs

- synthetic m/z array (numeric vector or matrix)
- intensity array (numeric vector or matrix, same dimensions as m/z)
- retention time values (numeric vector, one per scan)
- MS level (integer: 1 for full scan, 2+ for fragmentation)
- optional precursor m/z and collision energy (for MS2+)
- optional polarity string ('positive' or 'negative')

## Outputs

- .mzML file (XML with base64-encoded binary spectral data)
- mzML-compliant structured metadata (scan headers, precursor info, array descriptors)

## How to apply

After generating or collecting spectral arrays (m/z, intensity, retention time), encode the binary intensity data using base64 encoding via the base64enc package. Construct the XML document tree with root <indexedmzML> element, then nest <mzML> with appropriate scan-level metadata (scan number, retention time, MS level, polarity). For each scan, create a <scan> block containing precursor information (if MS2+), product ion m/z and intensity arrays as base64-encoded binary, and array descriptors specifying precision (32-bit vs 64-bit) and compression method. Write the complete XML tree to a .mzML file. Validate that the XML is well-formed and the base64 encoding is byte-accurate; downstream tools (mzR, xcms, etc.) will fail silently on malformed XML or encoding errors.

## Related tools

- **base64enc** (Encodes binary spectral intensity arrays to base64 strings for embedding in XML)
- **mzR** (Reads and validates mzML files; used to verify that constructed XML is parseable)
- **R** (Primary language for XML tree construction and base64 encoding in mzrtsim workflow)

## Examples

```
# After generating m/z and intensity arrays:
simmzml(db=monams1, name='test')
# This produces test.mzML with internal XML structure and base64-encoded spectral data
```

## Evaluation signals

- Output .mzML file is valid XML (parses without namespace or schema errors)
- base64-encoded binary data decodes back to original m/z and intensity arrays with no precision loss or byte misalignment
- mzR or other MS tools can successfully read the .mzML file and extract all scan metadata (RT, MS level, precursor m/z) without warnings
- Scan count, array lengths, and retention time ordering match the input spectral data dimensions
- XML structure includes all required elements: <indexedmzML>, <mzML>, <run>, <spectrumList>, <scan>, <precursorList> (if MS2+), and <binaryDataArrayList>

## Limitations

- Base64 encoding increases file size by ~33% compared to raw binary; large datasets (1000+ scans) may produce multi-MB .mzML files.
- XML construction must maintain strict element nesting and namespace declarations; typos in tag names or attribute keys will cause silent failures in downstream readers.
- Precision loss can occur if floating-point m/z or intensity values are not rounded consistently before encoding; verify numeric precision (32-bit vs 64-bit) matches instrument specifications.
- The mzML standard is complex; custom metadata (collision energy, cone voltage, custom tags) may not round-trip correctly through all readers.
- No automatic validation of spectral chemistry (e.g., isotope patterns, mass accuracy relative to formula); construction is purely structural.

## Evidence

- [other] Encode the combined spectral data (noise + optional matrix) as base64-encoded binary using the base64enc package.: "Encode the combined spectral data (noise + optional matrix) as base64-encoded binary using the base64enc package."
- [other] Construct mzML XML structure with appropriate scan headers, precursor metadata, and product ion arrays, then write to the output .mzML file.: "Construct mzML XML structure with appropriate scan headers, precursor metadata, and product ion arrays, then write to the output .mzML file."
- [intro] The underlying engine handles binary data encoding via the `base64enc` package: "The underlying engine handles binary data encoding via the `base64enc` package"
- [readme] The native mzML writer handles the binary encoding (Base64) internally without requiring external MS data libraries.: "The native mzML writer handles the binary encoding (Base64) internally without requiring external MS data libraries."
