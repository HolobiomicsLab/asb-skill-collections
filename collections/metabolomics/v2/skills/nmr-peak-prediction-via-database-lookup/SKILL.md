---
name: nmr-peak-prediction-via-database-lookup
description: Use when you have extracted peak data (chemical shift values in ppm, multiplicities, integration) from a processed NMR spectrum (JCAMP, RAW, or mzML format) and need to match these peaks against known NMR signals to propose or confirm structural assignments.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0154
  tools:
  - Flask
  - Python 3
  - curl
  - gunicorn
  - nmrshiftdb
  - chem-spectra-app
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

# nmr-peak-prediction-via-database-lookup

## Summary

Predict NMR chemical shifts and multiplicities by querying an external spectral database (nmrshiftdb) with observed peak parameters. This skill bridges experimental NMR data to literature/computed reference signals to assign or validate molecular structure.

## When to use

You have extracted peak data (chemical shift values in ppm, multiplicities, integration) from a processed NMR spectrum (JCAMP, RAW, or mzML format) and need to match these peaks against known NMR signals to propose or confirm structural assignments. Use this skill when manual peak interpretation is time-consuming or when you want automated literature-backed validation of peak identities.

## When NOT to use

- Input peaks have not been validated or extracted from a raw spectrum—use spectrum preprocessing and peak-picking skills first.
- You require real-time prediction with <100 ms latency—nmrshiftdb is an external HTTP service with network latency.
- The target molecule or functional group is not represented in the nmrshiftdb database (e.g., rare synthetic intermediates, isotopically labeled compounds).

## Inputs

- NMR peaks data (chemical shift values in ppm, multiplicities, integration values)
- JCAMP, RAW, or mzML spectral file
- nmrshiftdb service endpoint URL and credentials (from config.py)

## Outputs

- JSON-formatted NMR signal predictions with matched chemical shifts, multiplicities, and metadata from nmrshiftdb
- Ranked list of candidate molecular signals or substructures
- HTTP response from nmrshiftdb containing matching spectral library entries

## How to apply

Parse validated peak parameters (chemical shift, multiplicity, integration) from the spectral data. Format the peaks into a query string compatible with the nmrshiftdb HTTP API. Send a POST request to the external nmrshiftdb service (URL configured in config.py) with the formatted peaks payload. Parse the nmrshiftdb JSON response to extract matching NMR signals and their metadata. Return the ranked matches to the user as a structured JSON prediction, with confidence or match quality ranking if provided by nmrshiftdb. Validate that the returned signals are chemically plausible for your target structure and solvent/field strength.

## Related tools

- **Flask** (HTTP web framework that routes /predict/by_peaks_form and /api/v1/chemspectra/predict/nmr_peaks_form POST endpoints to parse and dispatch peaks data)
- **Python 3** (Primary language for HTTP client code, peak parsing, and response formatting)
- **curl** (CLI tool for manual testing and debugging of prediction requests to the endpoint)
- **gunicorn** (WSGI application server to run the Flask endpoint in production (e.g., gunicorn -w 4 -b 0.0.0.0:3007 server:app))
- **nmrshiftdb** (External spectral database and HTTP API service that receives formatted peaks and returns matching NMR signals)
- **chem-spectra-app** (Backend web service that provides NMR/IR/MS processing and hosts the prediction endpoint) — https://github.com/ComPlat/chem-spectra-app

## Examples

```
curl -X POST http://localhost:3007/api/v1/chemspectra/predict/nmr_peaks_form -d 'peaks=[{"shift": 7.2, "multiplicity": "d", "integration": 2}, {"shift": 3.8, "multiplicity": "s", "integration": 3}]'
```

## Evaluation signals

- HTTP response status is 200 and JSON response conforms to nmrshiftdb schema (contains signal matches with chemical shift and multiplicity fields).
- Returned chemical shifts are within ±0.5 ppm of input peak positions (or domain-specific tolerance configured for the solvent/instrument).
- Returned multiplicities (singlet, doublet, triplet, multiplet) match the observed multiplicities from the input peaks (allowing for minor splitting overlaps).
- Number of matched signals is non-zero and chemically consistent (e.g., peak count and integration ratios are plausible for the query molecule).
- nmrshiftdb rank or confidence score (if returned) is above a configured threshold (e.g., top 5 matches).

## Limitations

- Accuracy depends entirely on nmrshiftdb database coverage; rare or novel molecules may return no matches or false positives.
- External network dependency: service unavailability or latency issues will block prediction; no offline fallback is provided in the current design.
- Peak input must be accurate and well-separated; overlapping or poorly resolved multiplets may produce ambiguous or incorrect matches.
- nmrshiftdb is optimized for common organic solvents and field strengths; predictions in unusual solvents (e.g., DMSO-d6, CD3OD) or at atypical fields (>800 MHz) may be less reliable.
- Integration values are accepted but may not be fully utilized by nmrshiftdb; matching is primarily on chemical shift and multiplicity.

## Evidence

- [other] Parse and validate the peaks data (chemical shift values, multiplicities, integration).: "Parse and validate the peaks data (chemical shift values, multiplicities, integration)."
- [other] Format the peaks data into a query compatible with nmrshiftdb HTTP API.: "Format the peaks data into a query compatible with nmrshiftdb HTTP API."
- [other] Send HTTP POST request to the external nmrshiftdb service at URL_NSHIFTDB (configured in config.py) with formatted query.: "Send HTTP POST request to the external nmrshiftdb service at URL_NSHIFTDB (configured in config.py) with formatted query."
- [other] Parse the nmrshiftdb response containing matching NMR signals.: "Parse the nmrshiftdb response containing matching NMR signals."
- [readme] This backend web service provides NMR/IR/MS processing for jcamp/RAW/mzML files.: "This backend web service provides NMR/IR/MS processing for jcamp/RAW/mzML files."
