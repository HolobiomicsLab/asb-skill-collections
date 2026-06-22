---
name: spectral-peak-data-validation-and-parsing
description: Use when when you have received POST requests containing peaks data as form parameters (chemical shift, multiplicity, integration values) and need to accept, validate, and normalize those values before formatting them into a query compatible with an external NMR prediction service such as.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0593
  tools:
  - Flask
  - Python 3
  - curl
  - gunicorn
  - nmrshiftdb
derived_from:
- doi: 10.1186/s13321-020-00481-0
  title: ChemSpectra
evidence_spans:
- export FLASK_APP=chem_spectra && export FLASK_DEBUG=true && flask run
- export FLASK_APP=chem_spectra && export FLASK_DEBUG=true && flask run --host=0.0.0.0 --port=3007
- Use the file pyproject.toml to determine the version of Python required.
- curl xxx.xxx.xxx.xxx:3007/ping
- gunicorn -w 4 -b 0.0.0.0:3007 server:app --daemon
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_chemspectra_cq
    doi: 10.1186/s13321-020-00481-0
    title: ChemSpectra
  dedup_kept_from: coll_chemspectra_cq
schema_version: 0.2.0
---

# spectral-peak-data-validation-and-parsing

## Summary

Parse and validate NMR spectral peak data (chemical shift values, multiplicities, integration) extracted from jcamp/RAW/mzML files into a normalized form suitable for external prediction APIs. This skill ensures data integrity before downstream query construction and inference.

## When to use

When you have received POST requests containing peaks data as form parameters (chemical shift, multiplicity, integration values) and need to accept, validate, and normalize those values before formatting them into a query compatible with an external NMR prediction service such as nmrshiftdb.

## When NOT to use

- Peak data is already validated and formatted into an nmrshiftdb API query—skip directly to HTTP submission.
- Input is raw spectral image or binary spectrum data (jcamp/RAW/mzML file)—use spectral file conversion and peak extraction first.
- Peaks have already been matched against a reference database—this skill is for upstream validation, not post-prediction processing.

## Inputs

- POST request with form parameters containing NMR peak data
- Chemical shift values (float, ppm)
- Multiplicity labels (string: singlet, doublet, triplet, etc.)
- Integration values (float, relative intensity)

## Outputs

- Validated and normalized peak data structure (JSON or dict)
- Validation error report (if data fails checks)
- Formatted query ready for nmrshiftdb API submission

## How to apply

Receive the peaks data payload at the endpoint (e.g., /predict/by_peaks_form or /api/v1/chemspectra/predict/nmr_peaks_form). Parse the form parameters to extract chemical shift values, multiplicities (e.g., singlet, doublet), and integration values. Validate each field: check that chemical shift values are within expected NMR range (typically 0–12 ppm for ¹H NMR), that multiplicities match known types, and that integration values are positive and reasonable. Reject or flag malformed entries and return detailed error messages. Once validated, normalize the parsed data into a structured format (typically JSON or dictionary) ready for formatting into the external API query. This validation step prevents downstream failures and ensures the prediction request is well-formed.

## Related tools

- **Flask** (Web framework for receiving and handling POST requests at /predict/by_peaks_form endpoint) — https://github.com/ComPlat/chem-spectra-app
- **Python 3** (Language for implementing parse, validate, and normalize logic) — https://github.com/ComPlat/chem-spectra-app
- **gunicorn** (WSGI application server for deploying Flask application at production scale) — https://github.com/ComPlat/chem-spectra-app
- **nmrshiftdb** (External HTTP API that receives formatted peak query and returns matching NMR signals)

## Examples

```
curl -X POST http://localhost:3007/api/v1/chemspectra/predict/nmr_peaks_form -d 'shift=7.3&multiplicity=doublet&integration=2.0&shift=3.5&multiplicity=singlet&integration=3.0'
```

## Evaluation signals

- All required form parameters (chemical shift, multiplicity, integration) are present and parsed without exceptions.
- Chemical shift values fall within expected NMR range (0–12 ppm for ¹H); out-of-range values are flagged.
- Multiplicity labels match known NMR coupling patterns (singlet, doublet, triplet, etc.); unknown labels are rejected.
- Integration values are positive, non-zero, and have consistent scale across the peak list.
- Normalized output structure matches the schema expected by the nmrshiftdb HTTP API (verified by successful downstream submission).

## Limitations

- Validation scope is limited to structural and range checks; does not verify chemical plausibility (e.g., whether a peak multiplicity is physically consistent with molecular structure).
- No handling of overlapping peaks or peak clusters—assumes each peak is discrete and independently reported.
- Integration normalization assumes form parameters use a consistent scale; mixed or undeclared scales may cause silent errors.
- No version management or schema evolution for nmrshiftdb API changes—validation rules must be manually updated if external API format changes.

## Evidence

- [other] Parse and validate the peaks data (chemical shift values, multiplicities, integration).: "Parse and validate the peaks data (chemical shift values, multiplicities, integration)."
- [other] Receive POST request at endpoint /predict/by_peaks_form or /api/v1/chemspectra/predict/nmr_peaks_form with peaks data as form parameters.: "Receive POST request at endpoint /predict/by_peaks_form or /api/v1/chemspectra/predict/nmr_peaks_form with peaks data as form parameters."
- [readme] This backend web service provides NMR/IR/MS processing for jcamp/RAW/mzML files.: "This backend web service provides NMR/IR/MS processing for jcamp/RAW/mzML files."
- [other] Format the peaks data into a query compatible with nmrshiftdb HTTP API.: "Format the peaks data into a query compatible with nmrshiftdb HTTP API."
