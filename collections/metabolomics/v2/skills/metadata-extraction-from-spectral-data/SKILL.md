---
name: metadata-extraction-from-spectral-data
description: Use when you have raw mass spectrometry files in one of the supported formats (mzML, mzXML, msp, metabolomics-USI, MGF, JSON) and need to parse out metadata fields (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - pytest
  - matchms
derived_from:
- doi: 10.1186/s13321-024-00878-1
  title: matchms
evidence_spans:
- Matchms is a versatile open-source Python package developed for importing, processing, cleaning, and comparing mass spectrometry data
- make sure the existing tests still work by running ``pytest``
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_matchms_2_cq
    doi: 10.1186/s13321-024-00878-1
    title: matchms
  dedup_kept_from: coll_matchms_2_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-024-00878-1
  all_source_dois:
  - 10.1186/s13321-024-00878-1
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metadata-extraction-from-spectral-data

## Summary

Extract and validate metadata fields from mass spectrometry spectral data files in multiple formats (mzML, mzXML, msp, MGF, JSON, metabolomics-USI). This skill ensures accurate metadata preservation and cleaning during import of raw MS/MS data into matchms Spectrum objects.

## When to use

You have raw mass spectrometry files in one of the supported formats (mzML, mzXML, msp, metabolomics-USI, MGF, JSON) and need to parse out metadata fields (e.g., compound name, molecular weight, collision energy, precursor m/z) to construct standardized Spectrum objects for downstream processing or comparison workflows.

## When NOT to use

- Input spectral data is already loaded and validated as matchms Spectrum objects — use this skill only on raw, unparsed files
- File format is not one of the six supported formats (mzML, mzXML, msp, metabolomics-USI, MGF, JSON) — metadata extraction will fail or require new parser implementation
- Metadata quality is not a requirement for your analysis (e.g., you only need peak m/z and intensity values for de novo spectral comparison without compound context)

## Inputs

- mzML file
- mzXML file
- msp file
- MGF file
- JSON file
- metabolomics-USI identifier

## Outputs

- matchms Spectrum objects with extracted metadata
- metadata field mappings (format-specific to matchms schema)
- pytest test suite validating parser correctness

## How to apply

Design and implement individual parser functions for each supported file format that extract both metadata and peak lists from the file structure, then construct matchms Spectrum objects with the parsed metadata fields. Each parser must handle format-specific metadata schemas and map them to matchms Spectrum object attributes. Write unit tests using pytest to validate correct parsing of representative samples in each format, ensuring metadata accuracy and schema compliance. Run the full test suite to confirm all parsing tests pass and no existing tests are broken. This validation step is critical because metadata quality directly affects downstream similarity comparisons and spectral library cleaning pipelines.

## Related tools

- **Python** (Language for implementing parser functions and Spectrum object construction)
- **pytest** (Unit testing framework to validate parser correctness and Spectrum object construction for each file format)
- **matchms** (Target package providing Spectrum object schema and metadata validation) — https://github.com/matchms/matchms

## Examples

```
from matchms.importing_utils import load_from_msp; spectra = load_from_msp('library.msp'); print(spectra[0].metadata)
```

## Evaluation signals

- All parser unit tests pass in pytest with 100% of representative samples in each format correctly parsed
- Extracted metadata fields match expected schema defined in matchms Spectrum object (no missing or malformed attributes)
- Existing test suite remains unbroken after parser module integration (verified by full pytest run)
- Spectrum objects constructed from parsed metadata are serializable and can be passed to downstream matchms workflows (e.g., cleaning pipelines, similarity scoring)
- Metadata content accuracy spot-check: verify that extracted values (e.g., precursor m/z, compound name) match the source file content for a sample of spectra

## Limitations

- Parser implementation is format-specific; adding support for new file formats requires new parser functions and corresponding tests
- Metadata completeness depends on what fields are actually present in the source file — some formats may omit optional fields, and parsers must handle gracefully
- Large-scale file parsing performance is not explicitly addressed; bulk import of thousands of spectra may require optimization for I/O or memory efficiency
- Metadata validation occurs within matchms after extraction; this skill focuses on parsing and field mapping, not on data quality or semantic consistency checks (e.g., detecting duplicate records or chemically invalid values)

## Evidence

- [other] What file formats does matchms support for importing mass spectrometry spectral data?: "Matchms supports loading mass spectrometry spectra from six file formats: mzML, mzXML, msp, metabolomics-USI, MGF, and JSON."
- [readme] matchms supports popular spectral data formats: "The software supports a range of popular spectral data formats, including mzML, mzXML, msp, metabolomics-USI, MGF, and JSON"
- [readme] Metadata cleaning and validation tools: "Matchms offers an array of tools for metadata cleaning and validation, alongside basic peak filtering, to ensure data accuracy and integrity"
- [other] Parser implementation workflow: "Implement individual parser functions that extract metadata and peak lists from each format and construct matchms Spectrum objects."
- [other] Testing requirement for parsers: "Write unit tests using pytest to validate correct parsing and Spectrum object construction for representative samples in each format."
- [readme] pytest validation step: "make sure the existing tests still work by running ``pytest``"
