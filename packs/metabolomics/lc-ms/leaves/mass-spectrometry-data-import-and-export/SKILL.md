---
name: mass-spectrometry-data-import-and-export
description: Use when use this skill at the start of any mass spectrometry analysis pipeline when you have raw spectral data in mzML, mzXML, msp, MGF, JSON, or metabolomics-USI format and need to load it into a Python environment for preprocessing, cleaning, filtering, or similarity comparison.
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
  - bioconda
  techniques:
  - LC-MS
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

# mass-spectrometry-data-import-and-export

## Summary

Import raw mass spectrometry spectral data from multiple standard file formats (mzML, mzXML, msp, MGF, JSON) into a unified Python object model, and export pre- or post-processed spectral data back to the original or compatible format. This skill underpins reproducible MS/MS analysis workflows by enabling seamless format conversion and data integrity preservation.

## When to use

Use this skill at the start of any mass spectrometry analysis pipeline when you have raw spectral data in mzML, mzXML, msp, MGF, JSON, or metabolomics-USI format and need to load it into a Python environment for preprocessing, cleaning, filtering, or similarity comparison. Also use it when you have processed spectra and need to export results back to a standard format for sharing, archival, or downstream integration with other tools.

## When NOT to use

- You have already loaded spectral data into memory and do not need to parse a file on disk.
- Your spectral data is in a proprietary vendor format not supported by matchms (use vendor-provided converters first).
- You are working with already-preprocessed spectral feature matrices or pre-computed similarity scores; import/export applies to raw or lightly processed spectra, not derived quantitative features.

## Inputs

- mzML mass spectrometry data files
- mzXML mass spectrometry data files
- msp mass spectrometry data files
- MGF mass spectrometry data files
- JSON mass spectrometry data files
- metabolomics-USI spectral data references

## Outputs

- Spectrum objects (unified matchms data structure)
- Peak lists with m/z and intensity pairs
- Metadata annotations (precursor m/z, retention time, compound name, etc.)
- Exported spectral data in mzML, mzXML, msp, MGF, or JSON format

## How to apply

Load raw mass spectrometry spectral data using matchms import functionality, which automatically detects and parses the input format (mzML, mzXML, msp, MGF, JSON). The loaded spectra are unified into matchms Spectrum objects, preserving both peak lists and metadata. After applying any preprocessing (e.g., basic peak filtering, metadata cleaning, or validation), export the processed spectra in the original or a compatible format using matchms export methods. This preserves data integrity and enables integration with other analysis pipelines. Validate that metadata and peak counts are consistent before and after round-trip import/export to ensure no data loss.

## Related tools

- **matchms** (Core Python library providing import/export functionality and unified Spectrum object model for mass spectrometry data across multiple formats) — https://github.com/matchms/matchms
- **pytest** (Test framework used to validate that imported/exported data maintains integrity and passes format compliance checks)
- **bioconda** (Package distribution channel enabling easy installation of matchms and dependencies across Linux and macOS platforms) — https://github.com/bioconda/bioconda-recipes

## Examples

```
from matchms.importing_utils import load_from_msp; spectra = load_from_msp('raw_spectra.msp'); from matchms.exporting_utils import save_to_mgf; save_to_mgf(spectra, 'processed_spectra.mgf')
```

## Evaluation signals

- Imported Spectrum objects contain expected number of peaks with valid m/z and intensity values (no NaNs or negative intensities)
- Metadata fields (precursor_mz, retention_time, compound_name, etc.) are correctly parsed and non-empty where present in source file
- Round-trip test: export imported spectra and re-import; verify peak counts and metadata match original import within numerical tolerance
- File format is correctly detected from file extension or magic bytes; no format mismatch errors occur
- Exported file passes format-specific validation tools or can be re-imported without errors by the same or downstream tools

## Limitations

- matchms supports only the listed formats (mzML, mzXML, msp, MGF, JSON, metabolomics-USI); proprietary vendor formats require prior conversion.
- Metadata field coverage varies by source file format; some formats may lack retention time, instrument type, or collision energy annotations.
- Large files (hundreds of thousands of spectra) may require streaming or chunked import to avoid memory exhaustion; standard import loads entire dataset.
- Format-specific validation rules (e.g., required vs. optional fields in msp headers) may reject or truncate non-compliant input files.

## Evidence

- [readme] The software supports a range of popular spectral data formats, including mzML, mzXML, msp, metabolomics-USI, MGF, and JSON: "The software supports a range of popular spectral data formats, including mzML, mzXML, msp, metabolomics-USI, MGF, and JSON"
- [other] Load raw mass spectrometry spectral data in supported formats (mzML, mzXML, msp, MGF, JSON) using matchms import functionality: "Load raw mass spectrometry spectral data in supported formats (mzML, mzXML, msp, MGF, JSON) using matchms import functionality"
- [readme] Matchms is a versatile open-source Python package developed for importing, processing, cleaning, and comparing mass spectrometry data (MS/MS): "Matchms is a versatile open-source Python package developed for importing, processing, cleaning, and comparing mass spectrometry data (MS/MS)"
- [readme] It facilitates the implementation of straightforward, reproducible workflows, transforming raw data from common mass spectra file formats into pre- and post-processed spectral data: "It facilitates the implementation of straightforward, reproducible workflows, transforming raw data from common mass spectra file formats into pre- and post-processed spectral data"
- [readme] Matchms offers an array of tools for metadata cleaning and validation, alongside basic peak filtering, to ensure data accuracy and integrity: "Matchms offers an array of tools for metadata cleaning and validation, alongside basic peak filtering, to ensure data accuracy and integrity"
