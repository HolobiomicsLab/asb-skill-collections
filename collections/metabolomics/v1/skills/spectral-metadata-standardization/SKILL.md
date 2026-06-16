---
name: spectral-metadata-standardization
description: Use when when importing mass spectrometry spectral data from public repositories or multi-source MGF/MSP files where metadata fields are inconsistent, missing, or non-standard;
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - matchms
  - pytest
  - Python
derived_from:
- doi: 10.21105/joss.02411
  title: matchms
evidence_spans:
- Matchms offers an array of tools for metadata cleaning and validation
- Matchms is a versatile open-source Python package developed for importing, processing, cleaning, and comparing mass spectrometry data
- make sure the existing tests still work by running ``pytest``
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_matchms
    doi: 10.21105/joss.02411
    title: matchms
  dedup_kept_from: coll_matchms
schema_version: 0.2.0
---

# spectral-metadata-standardization

## Summary

Standardize and validate mass spectrometry spectral metadata fields (instrument type, precursor m/z, retention time, etc.) using matchms cleaning filters to ensure consistent, machine-readable metadata across heterogeneous spectral collections before similarity comparisons or library integration.

## When to use

When importing mass spectrometry spectral data from public repositories or multi-source MGF/MSP files where metadata fields are inconsistent, missing, or non-standard; before running large-scale spectral similarity comparisons or library deposition, where metadata quality directly impacts downstream match reliability and reproducibility.

## When NOT to use

- Spectral data is already in a single, internally consistent repository with validated metadata — standardization has already occurred.
- The analysis goal requires retaining raw, unmodified metadata as-is for provenance or audit purposes.
- Metadata fields are domain-specific or proprietary and cannot be mapped to matchms' standard schema without information loss.

## Inputs

- MGF (Mascot Generic Format) spectral files
- MSP (NIST MS Search) spectral files
- Raw spectral data with heterogeneous or incomplete metadata

## Outputs

- Cleaned spectral collection with standardized metadata fields
- MGF or JSON export of cleaned spectra
- Test report from pytest validating filter logic

## How to apply

Load spectral data from MGF or MSP files using matchms' import functions. Apply matchms metadata cleaning filters to standardize critical fields such as instrument type, precursor m/z values, retention time, and compound identifiers to a uniform schema. Then apply matchms validation filters to flag or remove spectra with missing or invalid metadata in those fields. Export the cleaned spectrum collection to MGF or JSON format. Verify filter logic and data integrity constraints by running pytest on the cleaning workflow to ensure no data was lost and all metadata now conforms to the standardized schema.

## Related tools

- **matchms** (Python package providing metadata cleaning and validation filters for standardizing spectral metadata fields) — https://github.com/matchms/matchms
- **Python** (Language for scripting matchms import, filter application, and data export workflows)
- **pytest** (Test framework for validating that cleaning filters preserve data integrity and enforce metadata constraints)

## Examples

```
from matchms import Spectrum, importing; from matchms.filtering import normalize_compound_name, add_parent_mass; spectra = list(importing.load_from_mgf('raw_spectra.mgf')); cleaned = [normalize_compound_name(add_parent_mass(s)) for s in spectra]; [s.export_to_mgf() for s in cleaned]
```

## Evaluation signals

- All spectra in the output collection have non-null values for critical metadata fields (precursor m/z, instrument type) — no incomplete records remain.
- Metadata values conform to expected formats and ranges (e.g., m/z values are numeric and positive; retention time is numeric and within instrument hardware limits).
- pytest test suite passes without errors, confirming filter logic is deterministic and reproducible across multiple runs.
- Spot-check comparison of input vs. output metadata shows consistent standardization (e.g., instrument name variants are unified to a single canonical form).
- Export file (MGF or JSON) parses without schema errors and can be ingested by downstream similarity-comparison tools.

## Limitations

- Matchms cleaning filters may remove or discard spectra with too much missing metadata, reducing dataset size; the trade-off between coverage and quality must be chosen deliberately.
- Standardization is schema-dependent — if the target metadata schema does not match the fields present in the raw data, important domain-specific information may be discarded or unmapped.
- Metadata cleaning cannot infer or recover values that are genuinely absent from the source file (e.g., if instrument type is never recorded); it can only standardize and validate what is present.

## Evidence

- [other] Apply matchms metadata cleaning filters to standardize and validate spectrum metadata fields: "Apply matchms metadata cleaning filters to standardize and validate spectrum metadata fields (e.g., instrument type, precursor m/z, retention time)."
- [readme] Metadata cleaning and validation alongside peak filtering to ensure data accuracy and integrity: "Matchms offers an array of tools for metadata cleaning and validation, alongside basic peak filtering, to ensure data accuracy and integrity."
- [readme] Straightforward, reproducible workflows transforming raw mass spectra file formats into pre- and post-processed spectral data: "It facilitates the implementation of straightforward, reproducible workflows, transforming raw data from common mass spectra file formats into pre- and post-processed spectral data"
- [readme] Multiple spectral data formats including mzML, mzXML, msp, metabolomics-USI, MGF, and JSON: "The software supports a range of popular spectral data formats, including mzML, mzXML, msp, metabolomics-USI, MGF, and JSON."
