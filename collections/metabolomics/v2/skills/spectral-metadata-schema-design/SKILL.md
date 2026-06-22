---
name: spectral-metadata-schema-design
description: Use when you are implementing a file parser or data ingestion module that must read .raw (Thermo) and .mzml files from heterogeneous LC-MS instruments and pass structured data to downstream tools (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3371
  tools:
  - Python
  - bmxp
  - bmxp.chroma
  - bmxp.eclipse
  - bmxp.gravity
  - bmxp.blueshift
derived_from:
- doi: 10.1093/bioinformatics/btaf290/8128335
  title: Eclipse
evidence_spans:
- They are written in Python and C
- pip install bmxp
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_eclipse_cq
    doi: 10.1093/bioinformatics/btaf290/8128335
    title: Eclipse
  dedup_kept_from: coll_eclipse_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btaf290/8128335
  all_source_dois:
  - 10.1093/bioinformatics/btaf290/8128335
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-metadata-schema-design

## Summary

Design and implement a unified data structure that abstracts multiple mass spectrometry file formats (.raw, .mzml) into a common schema, exposing standardized properties for downstream metabolomics processing. This skill bridges format heterogeneity at the data input stage of the BMXP pipeline, enabling consistent access to spectral metadata across diverse instrument vendors and file types.

## When to use

You are implementing a file parser or data ingestion module that must read .raw (Thermo) and .mzml files from heterogeneous LC-MS instruments and pass structured data to downstream tools (e.g., feature detection, alignment, drift correction) that expect a consistent column/property interface. Use this skill when you need to define what spectral attributes (scan number, retention time, m/z values, intensities, precursor information) will be exposed and how they will be named across all input formats.

## When NOT to use

- Input files are already in a standardized format (e.g., NetCDF, HDF5) that downstream tools natively support without translation.
- You are working with a single file format exclusively and do not need cross-format abstraction.
- The downstream workflow does not require spectral-level metadata and only consumes pre-computed feature tables (e.g., Formation output) or aligned abundances.

## Inputs

- .raw files (Thermo RAW format)
- .mzml files (mzML XML-based format)
- Mass spectrometry spectral data with metadata (scan information, retention time, precursor information)

## Outputs

- Unified structured object (class instance or dictionary) with standardized spectral properties
- Extracted spectral metadata: scan number, retention time, m/z values, intensities, precursor information
- Validation report confirming parsed data fidelity against reference files

## How to apply

First, enumerate the common spectral properties required by all downstream modules (scan number, retention time, m/z array, intensity array, precursor m/z, precursor intensity, isolation window, activation method). Second, design a class or dictionary schema that abstracts both .raw and .mzml formats, mapping vendor-specific metadata fields to canonical property names. Third, implement format-specific parsers that extract these properties from each file type—for .raw files, deserialize Thermo's binary headers and scan index; for .mzml files, parse XML elements and base64-encoded arrays. Fourth, define error handling for malformed or truncated files (e.g., missing scan metadata, invalid base64, truncated intensity arrays). Fifth, validate the output against reference .raw and .mzml files to confirm that parsed scan counts, RT ranges, m/z ranges, and intensity distributions match expected values. The schema design should prioritize properties that downstream tools (Eclipse for alignment, Gravity for clustering, Blueshift for drift correction) require as input.

## Related tools

- **bmxp.chroma** (Primary module for reading .raw and .mzml files; implements the unified spectral metadata schema to expose file contents for downstream BMXP processing steps.) — https://github.com/broadinstitute/bmxp/blob/main/bmxp/chroma/readme.md
- **bmxp.eclipse** (Downstream consumer of unified spectral metadata; aligns nontargeted LC-MS datasets using standardized feature and injection metadata structures.) — https://github.com/broadinstitute/bmxp/blob/main/bmxp/eclipse/readme.md
- **bmxp.gravity** (Downstream consumer; clusters redundant LCMS features using retention time and correlation properties standardized in the schema.) — https://github.com/broadinstitute/bmxp/blob/main/bmxp/gravity/readme.md
- **bmxp.blueshift** (Downstream consumer; applies drift correction using injection and feature metadata with standard column headers.) — https://github.com/broadinstitute/bmxp/blob/main/bmxp/blueshift/readme.md

## Examples

```
from bmxp.chroma import ChromaReader; reader = ChromaReader(); spectrum = reader.read('sample.raw'); print(spectrum.scan_number, spectrum.retention_time, spectrum.mz_values, spectrum.intensities)
```

## Evaluation signals

- Verify that all parsed scans have valid, monotonically increasing scan numbers and retention times within expected instrument ranges (e.g., 0–30 min).
- Confirm that m/z arrays and intensity arrays have matching lengths and contain valid numeric values (no NaN or infinities except where expected).
- Validate that precursor m/z values fall within the instrument's mass range and match the scan's isolation window.
- Compare output scan counts, RT distributions, m/z distributions, and intensity ranges against reference .raw and .mzml files; deviations >0.1% indicate parsing errors.
- Check that the unified data structure exposes the required properties (scan_number, retention_time, mz_values, intensities, precursor_mz) without missing fields for any input file.

## Limitations

- Thermo .raw file parsing requires access to vendor libraries or reverse-engineered parsers; proprietary format licensing or version incompatibilities may limit portability.
- mzML files may use different compression schemes (zlib, gzip) and base64 encodings (32-bit vs. 64-bit float); all variants must be supported or validation will fail on subset of files.
- Truncated or corrupted files may yield partial scans or missing metadata fields; error handling must decide whether to skip corrupted scans, raise exceptions, or fill with sentinel values.
- Different LC-MS instruments (Thermo, Agilent, Waters, Bruker) store retention time in different units (seconds vs. minutes) and precursor information differently; the schema must handle these vendor-specific conventions.
- Very large .raw or .mzml files (>1 GB) may exhaust memory if parsed entirely into a single object; streaming or chunked parsing may be required for high-throughput pipelines.

## Evidence

- [other] Design a file format handler in Python that detects and routes .raw and .mzml files to format-specific parsers.: "Design a file format handler in Python that detects and routes .raw and .mzml files to format-specific parsers."
- [other] Define a unified data structure (class or dictionary schema) that abstracts both formats and exposes common properties (scan number, retention time, m/z values, intensities, precursor information).: "Define a unified data structure (class or dictionary schema) that abstracts both formats and exposes common properties (scan number, retention time, m/z values, intensities, precursor information)."
- [other] Validate the structured output against known reference .raw and .mzml files to confirm fidelity of parsed data.: "Validate the structured output against known reference .raw and .mzml files to confirm fidelity of parsed data."
- [readme] Each tool is meant to be a standalone module that performs a step in our processing pipeline.: "Each tool is meant to be a standalone module that performs a step in our processing pipeline."
- [readme] Chroma - Read .raw and .mzml files: "Chroma - Read .raw and .mzml files"
- [other] Chroma is a standalone module designed to read .raw and .mzml files, serving as the data input step that exposes mass spectrometry file contents for downstream processing in the BMXP pipeline.: "Chroma is a standalone module designed to read .raw and .mzml files, serving as the data input step that exposes mass spectrometry file contents for downstream processing in the BMXP pipeline."
