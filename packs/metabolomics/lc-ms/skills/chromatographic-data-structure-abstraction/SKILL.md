---
name: chromatographic-data-structure-abstraction
description: Use when when ingesting raw mass spectrometry data from multiple instrument vendors or file formats into a metabolomics processing pipeline, and you need to expose spectral and chromatographic metadata through a single, consistent interface regardless of the source format's internal structure.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - Python
  - bmxp
  - bmxp (Chroma module)
  techniques:
  - LC-MS
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

# chromatographic-data-structure-abstraction

## Summary

Design and implement a unified data structure that abstracts heterogeneous mass spectrometry file formats (.raw, .mzml) into a common schema, exposing normalized properties (scan number, retention time, m/z values, intensities, precursor information) for downstream processing in metabolomics pipelines.

## When to use

When ingesting raw mass spectrometry data from multiple instrument vendors or file formats into a metabolomics processing pipeline, and you need to expose spectral and chromatographic metadata through a single, consistent interface regardless of the source format's internal structure.

## When NOT to use

- Input is already in a downstream processed format (feature table, aligned feature matrix, or annotated metabolite list) — abstraction of raw file formats is not needed.
- Your pipeline only ingests a single, homogeneous file format from one instrument vendor — overhead of abstraction is unnecessary.
- You require vendor-specific metadata or instrument-tuning parameters not present in the standard schema — direct format-specific parsing may be more appropriate.

## Inputs

- Thermo .raw files (binary mass spectrometry data format)
- mzml files (XML-serialized mass spectrometry data)
- File path or file handle (string or file object)

## Outputs

- Unified chromatographic data structure (Python object or dictionary) with normalized fields: scan_number, retention_time, mz_values, intensities, precursor_mz
- Structured spectral and chromatographic metadata accessible via common property interface

## How to apply

First, analyze the structure and metadata fields of both .raw (Thermo RAW binary format) and .mzml (XML-based standard) files to identify common and format-specific properties. Define a unified data structure (Python class or dictionary schema) that captures the intersection of essential chromatographic and spectral data: scan number, retention time, m/z array, intensity array, and precursor m/z for MS/MS events. Implement format-specific parsers for each file type that deserialize their native structures and map extracted fields into the unified schema. Route incoming files based on extension to the appropriate parser. Implement defensive I/O and error handling to gracefully handle malformed or truncated files. Validate the abstracted output against reference files from each format to confirm fidelity of parsed metadata and peak data.

## Related tools

- **bmxp (Chroma module)** (Standalone module that reads .raw and .mzml files and exposes their contents through a unified interface for the BMXP metabolomics processing pipeline) — https://github.com/broadinstitute/bmxp/blob/main/bmxp/chroma/readme.md
- **Python** (Language for implementing file format handlers, parsers, and data structure definitions)

## Examples

```
from bmxp.chroma import ChromaReader; chroma = ChromaReader(); data = chroma.read('sample.raw'); print(data.scan_number, data.retention_time, data.mz_values, data.intensities)
```

## Evaluation signals

- Parsed output conforms to the unified schema — all common properties (scan number, retention time, m/z, intensity) are present and correctly mapped for both .raw and .mzml inputs.
- Validation against known reference files: spectral metadata and peak intensities match the original file's content within expected tolerance (e.g., no data loss or truncation).
- File I/O error handling succeeds on malformed or truncated test files without crashing the parser.
- Round-trip consistency: multiple ingestions of the same file produce identical output structures.
- Format-agnostic downstream tools (e.g., clustering, alignment) receive identical results from .raw and .mzml encodings of the same experiment.

## Limitations

- Abstraction necessarily loses vendor-specific metadata and extended instrument parameters not expressible in the common schema.
- Parsing performance depends on file size and I/O characteristics; large .raw or .mzml files may incur significant latency during deserialization.
- Thermo .raw binary format parsing requires access to proprietary libraries or reverse-engineered specification; mzml parsing is standardized but XML parsing overhead may be a bottleneck.
- Truncated or corrupted files may fail silently or produce incomplete structures if error handling is insufficient.

## Evidence

- [other] Define a unified data structure (class or dictionary schema) that abstracts both formats and exposes common properties (scan number, retention time, m/z values, intensities, precursor information).: "Define a unified data structure (class or dictionary schema) that abstracts both formats and exposes common properties (scan number, retention time, m/z values, intensities, precursor information)."
- [other] Chroma is a standalone module designed to read .raw and .mzml files, serving as the data input step that exposes mass spectrometry file contents for downstream processing in the BMXP pipeline.: "Chroma is a standalone module designed to read .raw and .mzml files, serving as the data input step that exposes mass spectrometry file contents for downstream processing in the BMXP pipeline."
- [other] Implement a parser for .raw files (Thermo RAW format) that extracts spectral metadata, scan information, and ion data into a structured object.: "Implement a parser for .raw files (Thermo RAW format) that extracts spectral metadata, scan information, and ion data into a structured object."
- [other] Implement file I/O and error handling to ensure robust reading of malformed or truncated files.: "Implement file I/O and error handling to ensure robust reading of malformed or truncated files."
- [readme] Each tool is meant to be a standalone module that performs a step in our processing pipeline.: "Each tool is meant to be a standalone module that performs a step in our processing pipeline."
