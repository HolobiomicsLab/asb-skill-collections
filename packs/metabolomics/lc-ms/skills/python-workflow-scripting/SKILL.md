---
name: python-workflow-scripting
description: Use when you have raw mass spectrometry spectral data in common formats (MGF, MSP, mzML, mzXML, JSON) that requires standardized metadata cleaning, validation, and peak filtering before comparative analysis. Use this skill when you need to encode data quality constraints (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - matchms
  - Python
  - pytest
  - poetry
  techniques:
  - LC-MS
derived_from:
- doi: 10.1186/s13321-024-00878-1
  title: matchms
evidence_spans:
- Matchms offers an array of tools for metadata cleaning and validation
- Matchms is a versatile open-source Python package developed for importing, processing, cleaning, and comparing mass spectrometry data
- Matchms is a versatile open-source Python package
- make sure the existing tests still work by running ``pytest``
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_matchms
    doi: 10.1186/s13321-024-00878-1
    title: matchms
  dedup_kept_from: coll_matchms
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

# python-workflow-scripting

## Summary

Implement reproducible, multi-step mass spectrometry data processing pipelines using Python scripts that import, clean, validate, and compare spectral data across standardized file formats (MGF, MSP, mzML, mzXML, JSON). This skill enables systematic transformation of raw MS/MS data into analysis-ready spectral collections with documented provenance and testable logic.

## When to use

You have raw mass spectrometry spectral data in common formats (MGF, MSP, mzML, mzXML, JSON) that requires standardized metadata cleaning, validation, and peak filtering before comparative analysis. Use this skill when you need to encode data quality constraints (e.g., removing spectra with missing instrument type or invalid precursor m/z), ensure reproducibility across batches, and make the pipeline auditable via automated tests.

## When NOT to use

- Input spectra are already pre-processed and validated by the data provider, and no re-standardization is needed.
- The analysis goal is exploratory and does not require reproducibility or audit trails.
- Raw MS/MS data is in a proprietary binary format not supported by matchms loaders.

## Inputs

- Mass spectrometry spectral data in MGF, MSP, mzML, or mzXML format
- Metadata field specifications (required fields, valid ranges, standardization rules)
- Peak intensity and m/z filtering thresholds (if applicable)

## Outputs

- Cleaned spectrum collection exported to MGF or JSON format
- Test report from pytest verifying filter logic and data integrity
- Log or summary report of removed spectra and reasons (missing/invalid metadata)

## How to apply

Structure the workflow in Python using the matchms package to (1) import spectral data from MGF or MSP files; (2) apply matchms metadata cleaning filters to standardize spectrum metadata fields (instrument type, precursor m/z, retention time); (3) chain validation filters to remove spectra with missing or invalid critical metadata; (4) optionally apply basic peak filtering for intensity/m/z constraints; (5) export the cleaned spectrum collection to MGF or JSON format; (6) run pytest on the cleaning workflow to verify filter logic and validate that data integrity constraints are met. Document each filter's purpose and thresholds in comments, and parameterize cutoffs at the script head to enable reuse across projects.

## Related tools

- **matchms** (Primary Python package for importing, cleaning, validating, and exporting mass spectrometry spectral data; provides metadata cleaning filters, validation filters, and peak filtering tools.) — https://github.com/matchms/matchms
- **pytest** (Automated testing framework for verifying filter logic, data integrity constraints, and ensuring cleaned spectral data meets quality thresholds.)
- **Python** (Scripting language for authoring reproducible workflow pipelines that chain matchms operations and custom validation logic.)
- **poetry** (Dependency and version management tool for matchms project; used to bump package versions during releases.)

## Examples

```
from matchms.importing_utils import load_from_mgf
from matchms.filtering import default_filters, normalize_precursor_mz
spectra = [s for s in load_from_mgf('raw_spectra.mgf')]
spectra = [default_filters(s) for s in spectra]
spectra = [normalize_precursor_mz(s) for s in spectra if s.get('precursor_mz') is not None]
with open('cleaned_spectra.mgf', 'w') as f:
    for s in spectra:
        f.write(s.to_mgf())
```

## Evaluation signals

- All output spectra contain no missing values in critical metadata fields (instrument type, precursor m/z, retention time) as specified in the validation schema.
- pytest suite passes with 100% of test cases covering filter logic, data integrity constraints, and edge cases (malformed metadata, out-of-range m/z, negative intensities).
- Cleaned spectrum file (MGF or JSON) contains fewer spectra than input, with a removal report documenting which spectra were excluded and why.
- Metadata field values are standardized (e.g., instrument names normalized to canonical forms, precursor m/z within expected range, retention time > 0).
- Script is version-controlled, parameterized, and includes inline comments explaining each filter's purpose and threshold rationale.

## Limitations

- Matchms loaders support only common spectral formats (mzML, mzXML, MSP, MGF, JSON, metabolomics-USI); proprietary or custom binary formats require external conversion first.
- Metadata cleaning rules are domain- and dataset-specific; filters tuned for one instrument or ionization method may not be appropriate for another, requiring manual rule adjustment per project.
- Peak filtering and metadata validation do not correct or impute missing values; they only flag or remove defective spectra, which can result in loss of otherwise usable data if validation thresholds are too strict.
- Large-scale workflows (hundreds of thousands of spectra) require careful management of sparse data structures and memory; dense matrix approaches may cause out-of-memory errors.

## Evidence

- [readme] importing, processing, cleaning, and comparing mass spectrometry data: "Matchms is a versatile open-source Python package developed for importing, processing, cleaning, and comparing mass spectrometry data"
- [readme] metadata cleaning and validation tools: "Matchms offers an array of tools for metadata cleaning and validation, alongside basic peak filtering, to ensure data accuracy and integrity"
- [other] standardize and validate spectrum metadata fields: "Apply matchms metadata cleaning filters to standardize and validate spectrum metadata fields (e.g., instrument type, precursor m/z, retention time)"
- [other] remove spectra with missing or invalid critical metadata: "Apply matchms validation filters to remove spectra with missing or invalid critical metadata"
- [readme] straightforward, reproducible workflows: "It facilitates the implementation of straightforward, reproducible workflows, transforming raw data from common mass spectra file formats into pre- and post-processed spectral data"
- [other] Run pytest on the cleaning workflow: "Run pytest on the cleaning workflow to verify filter logic and data integrity constraints are met"
- [readme] supported data formats: "The software supports a range of popular spectral data formats, including mzML, mzXML, msp, metabolomics-USI, MGF, and JSON"
- [other] ensure tests still work by running pytest: "make sure the existing tests still work by running ``pytest``"
