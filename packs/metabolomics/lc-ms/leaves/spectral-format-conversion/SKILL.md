---
name: spectral-format-conversion
description: Use when when raw spectral data exists in one mass spectrometry file
  format but downstream analysis requires a different format; when integrating spectra
  from multiple sources or instruments that produce heterogeneous file formats;
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - pytest
  - matchms
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1186/s13321-024-00878-1
  title: matchms
evidence_spans:
- Matchms is a versatile open-source Python package developed for importing, processing,
  cleaning, and comparing mass spectrometry data
- matchms is a versatile open-source Python package
- make sure the existing tests still work by running ``pytest``
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_matchms_cq
    doi: 10.1186/s13321-024-00878-1
    title: matchms
  dedup_kept_from: coll_matchms_cq
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

# spectral-format-conversion

## Summary

Convert mass spectrometry spectral data between standardized formats (mzML, mzXML, msp, MGF, JSON) to enable interoperability across analysis pipelines and ensure compatibility with downstream similarity scoring and comparison workflows.

## When to use

When raw spectral data exists in one mass spectrometry file format but downstream analysis requires a different format; when integrating spectra from multiple sources or instruments that produce heterogeneous file formats; or when preparing spectral libraries for large-scale similarity comparisons that require consistent input encoding.

## When NOT to use

- Input spectra are already in the target format — apply format conversion only when format mismatch is confirmed.
- Spectral data is already parsed into in-memory spectrum objects — conversion applies to file-level formats, not intermediate representations.
- Proprietary or unsupported file formats are encountered — matchms supports only mzML, mzXML, msp, metabolomics-USI, MGF, and JSON.

## Inputs

- Raw spectral data in mzML format
- Raw spectral data in mzXML format
- Raw spectral data in msp format
- Raw spectral data in MGF format
- Raw spectral data in JSON format

## Outputs

- Converted spectral dataset in target format (mzML, mzXML, msp, MGF, or JSON)
- Spectrum objects with normalized metadata fields
- Conversion log documenting format-specific transformations applied

## How to apply

Load raw spectral data from the source format (mzML, mzXML, msp, MGF, or JSON) using matchms import utilities; apply format-specific parsers to extract peak lists and metadata fields; normalize metadata field names and structures to a common schema; validate that all required fields conform to the target format's specification; then export the converted spectrum dataset to the desired output format. Coordinate format conversion with metadata cleaning and validation (step 2–3 in the reconstruction workflow) to ensure data integrity is preserved across the conversion boundary.

## Related tools

- **matchms** (Provides import utilities and format-specific parsers for reading and writing mzML, mzXML, msp, MGF, and JSON spectral formats) — https://github.com/matchms/matchms
- **Python** (Programming language for invoking matchms import and export functions within conversion workflows)
- **pytest** (Test framework for validating that format conversion preserves metadata integrity and peak accuracy across converted spectra)

## Examples

```
from matchms.importing_utils import load_from_msp, save_as_json; spectra = load_from_msp('input.msp'); [spectrum.set("spectrum_type", "MS2") for spectrum in spectra]; save_as_json(spectra, 'output.json')
```

## Evaluation signals

- Output spectrum count matches input spectrum count (no spectra lost or duplicated during conversion).
- All mandatory metadata fields in the target format are populated for each converted spectrum; no required fields are null or malformed.
- Peak lists (m/z and intensity arrays) are numerically identical before and after conversion, within floating-point precision tolerances.
- Metadata field names conform to the target format's naming conventions and schema; no deprecated or format-incompatible field names remain.
- File-level validation passes when output file is re-parsed by matchms import utilities and compared against source spectrum objects.

## Limitations

- Conversion between formats may result in loss of format-specific metadata fields not supported by the target format; document such losses in a conversion report.
- Proprietary or vendor-specific extensions in source formats (e.g., instrument-specific annotations in mzML) may not be preserved during export to simpler formats.
- Large-scale batch conversions may introduce I/O bottlenecks if file formats require sequential record processing; consider chunking or parallelization strategies for multi-thousand spectrum datasets.

## Evidence

- [readme] The software supports a range of popular spectral data formats, including mzML, mzXML, msp, metabolomics-USI, MGF, and JSON: "The software supports a range of popular spectral data formats, including mzML, mzXML, msp, metabolomics-USI, MGF, and JSON"
- [other] Load imported spectra from matchms-compatible format (mzML, mzXML, msp, MGF, or JSON) using Python and matchms import utilities: "Load imported spectra from matchms-compatible format (mzML, mzXML, msp, MGF, or JSON) using Python and matchms import utilities"
- [readme] It facilitates the implementation of straightforward, reproducible workflows, transforming raw data from common mass spectra file formats into pre- and post-processed spectral data: "It facilitates the implementation of straightforward, reproducible workflows, transforming raw data from common mass spectra file formats into pre- and post-processed spectral data"
- [other] Output cleaned spectrum dataset with validated metadata in the original or preferred matchms format: "Output cleaned spectrum dataset with validated metadata in the original or preferred matchms format"
