---
name: harmonized-metadata-schema-mapping
description: Use when you have imported mass spectrometry spectra from multiple file formats (mzML, mzXML, msp, metabolomics-USI, MGF, JSON) and need to standardize their metadata fields before performing spectral comparisons, similarity scoring, or library construction.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - pytest
  - matchms
  techniques:
  - mass-spectrometry
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# harmonized-metadata-schema-mapping

## Summary

Normalize and validate spectral metadata fields across heterogeneous mass spectrometry data formats (mzML, mzXML, msp, MGF, JSON) into a common schema to ensure data accuracy and enable downstream processing. This skill is essential when importing spectra from multiple sources or formats that use inconsistent metadata field naming and structure.

## When to use

Apply this skill when you have imported mass spectrometry spectra from multiple file formats (mzML, mzXML, msp, metabolomics-USI, MGF, JSON) and need to standardize their metadata fields before performing spectral comparisons, similarity scoring, or library construction. Use it particularly when metadata field names, data types, or validation rules differ across input sources.

## When NOT to use

- Input spectra are already from a single, homogeneous source with uniform metadata schema and do not require normalization.
- Spectra have already been preprocessed and validated by another pipeline; re-harmonizing may introduce redundant operations.
- Metadata fields are not critical for your downstream analysis (e.g., if you only need peak m/z and intensity values for similarity scoring).

## Inputs

- Raw mass spectra in supported formats: mzML, mzXML, msp, metabolomics-USI, MGF, JSON
- Spectrum metadata records with heterogeneous field names and structures
- Target metadata schema or field mapping specification

## Outputs

- Harmonized spectrum objects with normalized metadata fields
- Cleaned and validated spectral dataset with consistent schema
- Test results confirming metadata validation passed

## How to apply

Load raw spectra data using matchms import functions for your target format(s). Identify the set of metadata fields present in each spectrum record and map them to a unified schema with consistent field names and types. Apply matchms metadata cleaning operations to normalize values (e.g., string case, numeric precision, date formats) and validate that required fields are present and conform to expected constraints. Run pytest on the imported and cleaned spectra to verify that validation tests pass and that no data integrity issues were introduced. Output cleaned spectral records with harmonized metadata fields ready for downstream operations like peak filtering, scoring, or comparison.

## Related tools

- **matchms** (Provides metadata cleaning operations, validation functions, and import/export for supported spectral formats; orchestrates harmonization workflow.) — https://github.com/matchms/matchms
- **pytest** (Runs validation test suite to verify that metadata cleaning and harmonization operations pass all integrity checks.)
- **Python** (Core language for implementing matchms-based metadata cleaning and validation scripts.)

## Examples

```
from matchms.importing_utils import load_from_msp, load_from_mgf; from matchms.data_processing import add_losses, normalize_intensities; spectra_msp = list(load_from_msp('file.msp')); spectra_mgf = list(load_from_mgf('file.mgf')); cleaned = [normalize_intensities(add_losses(s)) for s in spectra_msp + spectra_mgf]
```

## Evaluation signals

- All spectrum objects have the same set of metadata field names and no undefined/inconsistent keys.
- Metadata values conform to expected data types (e.g., numeric fields are numeric, date fields are ISO-formatted strings).
- pytest validation tests pass with no errors or warnings related to metadata schema violations.
- Manual inspection or diffing of pre- and post-harmonization metadata shows consistent normalization (e.g., whitespace trimmed, case normalized, field names standardized).
- Downstream operations (similarity scoring, spectral comparisons) execute without metadata-related errors and produce expected output dimensions.

## Limitations

- Matchms metadata cleaning handles common cases but may not capture domain-specific or non-standard metadata fields; custom validators may be needed for specialized schemas.
- File format support is limited to mzML, mzXML, msp, metabolomics-USI, MGF, and JSON; other formats require conversion or custom parsers.
- Harmonization assumes a target schema is known or can be inferred; ambiguous or conflicting metadata interpretations across formats may require manual curation.
- Large-scale batch harmonization may have memory or I/O performance constraints when processing hundreds of thousands of spectra; sparse data handling and batch processing strategies are recommended.

## Evidence

- [intro] Matchms provides an array of tools for metadata cleaning and validation, alongside basic peak filtering, to ensure data accuracy and integrity of imported spectra.: "Matchms offers an array of tools for metadata cleaning and validation, alongside basic peak filtering, to ensure data accuracy and integrity"
- [readme] The software supports a range of popular spectral data formats, including mzML, mzXML, msp, metabolomics-USI, MGF, and JSON.: "The software supports a range of popular spectral data formats, including mzML, mzXML, msp, metabolomics-USI, MGF, and JSON"
- [other] Apply metadata cleaning operations to normalize and validate spectral metadata fields during the import workflow.: "Apply metadata cleaning operations to normalize and validate spectral metadata fields"
- [readme] Matchms facilitates the implementation of straightforward, reproducible workflows, transforming raw data from common mass spectra file formats into pre- and post-processed spectral data.: "It facilitates the implementation of straightforward, reproducible workflows, transforming raw data from common mass spectra file formats into pre- and post-processed spectral data"
- [other] Run pytest to verify that existing validation tests pass after applying metadata cleaning operations.: "make sure the existing tests still work by running ``pytest``"
