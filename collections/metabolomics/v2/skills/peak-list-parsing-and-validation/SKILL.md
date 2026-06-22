---
name: peak-list-parsing-and-validation
description: Use when when importing raw mass spectrometry data from vendor or open formats (mzML, mzXML, msp, MGF, JSON, metabolomics-USI) and you need to extract peak m/z and intensity pairs into a standardized representation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
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

# peak-list-parsing-and-validation

## Summary

Parse and validate peak lists extracted from mass spectrometry spectral data files (mzML, mzXML, msp, MGF, JSON, metabolomics-USI) into structured Spectrum objects with verified metadata and peak intensity arrays. This skill ensures data integrity by constructing machine-readable spectrum representations suitable for downstream similarity comparisons and spectral processing pipelines.

## When to use

When importing raw mass spectrometry data from vendor or open formats (mzML, mzXML, msp, MGF, JSON, metabolomics-USI) and you need to extract peak m/z and intensity pairs into a standardized representation. Use this skill as the first step in a reproducible MS/MS workflow, before any metadata cleaning or spectral similarity comparisons.

## When NOT to use

- Input spectra are already in matchms Spectrum object format; use direct loading instead.
- File format is not among the six supported formats (mzML, mzXML, msp, MGF, JSON, metabolomics-USI); custom parser development is required.
- Peak list validation is not required (e.g., you only need metadata); use a lightweight metadata-only extractor.

## Inputs

- mzML files (XML-formatted mass spectrometry data)
- mzXML files (compressed XML mass spectrometry data)
- msp files (NIST MS library text format)
- MGF files (Mascot Generic Format peak lists)
- JSON files (JSON-serialized spectrum data)
- metabolomics-USI identifiers (Universal Spectrum Identifiers)

## Outputs

- matchms Spectrum objects with parsed metadata and peak lists
- Validated peak m/z–intensity arrays
- Structured metadata fields (precursor m/z, compound name, ionization mode, etc.)

## How to apply

Design a Spectrum object schema that captures both metadata (e.g., precursor m/z, compound name, ionization mode) and peak lists (m/z–intensity pairs). Implement dedicated parser functions for each supported file format that read raw format-specific records, extract peak coordinates and metadata, and construct matchms Spectrum objects. Validate each parsed spectrum against the schema (e.g., peak arrays must be numeric and non-empty; metadata fields must match expected types). Write unit tests in pytest that parse representative samples in each format and verify that Spectrum objects are correctly constructed. Run the full test suite with `pytest` to ensure parsing does not break existing functionality. Commit the parser module and tests to a feature branch and create a pull request for community review.

## Related tools

- **matchms** (Core library providing Spectrum object schema, parser framework, and validation utilities for importing and constructing spectra from multiple file formats) — https://github.com/matchms/matchms
- **pytest** (Test framework used to validate parser functions against representative sample files in each supported format and verify Spectrum object construction correctness)
- **Python** (Programming language in which parser functions and Spectrum schema are implemented)

## Examples

```
# Parse an mzML file and validate spectrum construction
from matchms.importing import load_from_mzml
import pytest

spectra = load_from_mzml('sample.mzML')
assert all(hasattr(s, 'peaks') and len(s.peaks) > 0 for s in spectra)
assert all(s.get('precursor_mz') is not None for s in spectra)
pytest tests/test_parsers.py -v
```

## Evaluation signals

- All parsed Spectrum objects contain non-null peak arrays with numeric m/z and intensity values
- Metadata fields (precursor m/z, compound name, etc.) are correctly extracted and match expected schema types
- pytest test suite passes for representative samples in each of the six file formats without breaking existing tests
- Round-trip validation: re-serializing parsed Spectrum objects to the original format produces equivalent peak lists and metadata
- No missing or truncated peak entries when comparing input file peak count to Spectrum object peak array length

## Limitations

- Only six file formats are supported (mzML, mzXML, msp, MGF, JSON, metabolomics-USI); vendor-specific or custom formats require additional parser development.
- Parser assumes well-formed input files; malformed or corrupted spectral data may cause parsing errors or produce incomplete Spectrum objects.
- Metadata field interpretation varies across file formats; standardization and cleaning of heterogeneous metadata is a separate downstream step.
- Large-scale file imports may have memory constraints when loading many spectra into Spectrum objects simultaneously.

## Evidence

- [other] Matchms supports loading mass spectrometry spectra from six file formats: mzML, mzXML, msp, metabolomics-USI, MGF, and JSON.: "Matchms supports loading mass spectrometry spectra from six file formats: mzML, mzXML, msp, metabolomics-USI, MGF, and JSON."
- [other] Design and implement parser modules that extract metadata and peak lists from each format: "1. Design Spectrum object schema and file format parsers for mzML, mzXML, msp, MGF, JSON, and metabolomics-USI using Python. 2. Implement individual parser functions that extract metadata and peak"
- [other] Validate parsing with unit tests and ensure existing tests remain unbroken: "3. Write unit tests using pytest to validate correct parsing and Spectrum object construction for representative samples in each format. 4. Run pytest to ensure all parsing tests pass and existing"
- [readme] The software supports a range of popular spectral data formats: "The software supports a range of popular spectral data formats, including mzML, mzXML, msp, metabolomics-USI, MGF, and JSON."
- [readme] Make sure the existing tests still work by running pytest: "make sure the existing tests still work by running ``pytest``"
