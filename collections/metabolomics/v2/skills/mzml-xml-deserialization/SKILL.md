---
name: mzml-xml-deserialization
description: Use when your input is an mzML file (XML-based mass spectrometry data
  format) and you need to expose spectral metadata, scan information, and ion data
  in a structured, programmatic form for alignment, clustering, drift correction,
  or quantification within the BMXP pipeline.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - bmxp
  - Chroma
  - Eclipse
  - Gravity
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mzml-xml-deserialization

## Summary

Deserialize mzML XML-formatted mass spectrometry files into structured spectral and chromatographic data objects for downstream metabolomics processing. This is the format-specific parsing step within the Chroma module that extracts scan metadata, retention times, m/z values, and ion intensities from the mzML standard.

## When to use

Use this skill when your input is an mzML file (XML-based mass spectrometry data format) and you need to expose spectral metadata, scan information, and ion data in a structured, programmatic form for alignment, clustering, drift correction, or quantification within the BMXP pipeline. mzML is preferred when data originates from instruments with native XML output or when cross-platform portability is required.

## When NOT to use

- Input is already in a structured format (HDF5, Parquet, or BMXP-native schema); use Chroma only for raw mzML or .raw files.
- Instrument output is .raw format (Thermo RAW); use the Chroma .raw parser instead of mzML deserializer.
- Data has already been processed through Chroma and exists as a feature table; deserialization is not idempotent.

## Inputs

- .mzml files (XML-serialized mass spectrometry data)
- mzML schema reference or validation rules
- expected retention time and m/z ranges

## Outputs

- Structured spectral data object (scan number, retention time, m/z array, intensity array, precursor info)
- Chromatographic data representation compatible with shared BMXP schema
- Feature metadata conforming to bmxp.FMDATA (RT, MZ, Intensity columns)

## How to apply

Implement an XML parser (using Python libraries such as ElementTree or lxml) that deserializes the mzML document structure and reconstructs spectral and chromatographic data into a unified internal schema. Extract key fields: scan number, retention time, m/z arrays, intensity arrays, and precursor information (for tandem MS). Map these parsed fields into the shared BMXP schema (RT, MZ, Intensity) to ensure downstream modules (Eclipse, Gravity, Blueshift) can consume the output without format-specific logic. Validate the parsed output against reference mzML files to confirm fidelity of reconstructed data, paying attention to data type precision (float64 for m/z and intensity), array alignment, and metadata completeness.

## Related tools

- **Chroma** (Parent module that routes and orchestrates format-specific parsers (mzML and .raw); Chroma exposes a unified interface that calls this deserialization skill as part of its workflow.) — https://github.com/broadinstitute/bmxp/blob/main/bmxp/chroma/readme.md
- **Python** (Implementation language for XML parsing and data structure construction; used to write the mzML deserializer.)
- **Eclipse** (Downstream consumer of deserialized mzML data; requires structured spectral metadata for alignment of same-method nontargeted LCMS datasets.) — https://github.com/broadinstitute/bmxp/blob/main/bmxp/eclipse/readme.md
- **Gravity** (Downstream consumer of parsed RT and m/z data for clustering redundant LCMS features.) — https://github.com/broadinstitute/bmxp/blob/main/bmxp/gravity/readme.md

## Examples

```
from bmxp.chroma import Chroma; chroma = Chroma(); spec_data = chroma.parse('sample.mzml'); print(spec_data['RT'], spec_data['MZ'], spec_data['Intensity'])
```

## Evaluation signals

- Parsed scan numbers, retention times, and m/z arrays match reference values from a validated mzML file (bit-perfect or within instrument calibration tolerance).
- All required columns in the shared BMXP schema (RT, MZ, Intensity) are populated with correct data types and non-null values.
- Intensity arrays align with m/z arrays (same length, no off-by-one errors); chromatographic profile is monotonic or physically plausible.
- Precursor m/z and charge state (if present) are correctly extracted and available for downstream tandem-MS processing.
- Malformed or truncated mzML files are caught and raise informative errors; parsing does not silently produce corrupted output.

## Limitations

- Parsing performance depends on mzML file size; very large datasets (>1 GB) may require streaming or chunked parsing rather than full in-memory deserialization.
- mzML schema compliance varies by instrument vendor and acquisition software version; non-standard extensions or missing fields may cause parsing failures.
- Data loss or rounding may occur during XML serialization/deserialization of floating-point m/z and intensity values, especially if precision is not explicitly declared.
- Precursor information and fragmentation spectra (MS/MS) require additional parsing logic beyond basic scan metadata; tandem-MS support must be explicitly implemented.

## Evidence

- [other] Implement a parser for .mzml files that deserializes the XML-based format and reconstructs spectral and chromatographic data.: "Implement a parser for .mzml files that deserializes the XML-based format and reconstructs spectral and chromatographic data."
- [other] Define a unified data structure (class or dictionary schema) that abstracts both formats and exposes common properties (scan number, retention time, m/z values, intensities, precursor information).: "Define a unified data structure (class or dictionary schema) that abstracts both formats and exposes common properties (scan number, retention time, m/z values, intensities, precursor information)."
- [intro] Chroma - Read .raw and .mzml files: "Chroma - Read .raw and .mzml files"
- [other] Validate the structured output against known reference .raw and .mzml files to confirm fidelity of parsed data.: "Validate the structured output against known reference .raw and .mzml files to confirm fidelity of parsed data."
- [readme] Each tool is meant to be a standalone module that performs a step in our processing pipeline.: "Each tool is meant to be a standalone module that performs a step in our processing pipeline."
