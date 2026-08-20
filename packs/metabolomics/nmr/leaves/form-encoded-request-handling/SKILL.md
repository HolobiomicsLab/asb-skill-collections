---
name: form-encoded-request-handling
description: Use when when a web service must accept spectroscopic measurements (NMR peaks, IR/MS metadata) submitted as form-encoded POST parameters from a client, and those parameters need to be validated, reformatted into an external API query format, or passed to a downstream predictor service.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - Flask
  - Python 3
  - curl
  - gunicorn
  - nmrshiftdb
  techniques:
  - NMR
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-020-00481-0
  all_source_dois:
  - 10.1186/s13321-020-00481-0
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# form-encoded-request-handling

## Summary

A skill for receiving, parsing, and validating form-encoded spectral data in HTTP POST requests to a web service backend, then transforming those parameters into structured queries for downstream processing or external APIs. Essential for integrating spectroscopic data workflows where clients submit NMR peak information (chemical shifts, multiplicities, integration values) via form parameters.

## When to use

When a web service must accept spectroscopic measurements (NMR peaks, IR/MS metadata) submitted as form-encoded POST parameters from a client, and those parameters need to be validated, reformatted into an external API query format, or passed to a downstream predictor service. Specifically applicable when the input arrives as chemical shift values, peak multiplicities, and integration data that must be reconciled with a reference database schema.

## When NOT to use

- Input is already parsed and validated in memory (e.g., from a database query or prior API call); skip form parsing and validation.
- Spectral data arrives in binary or jcamp/RAW/mzML file format rather than form-encoded parameters; use file conversion and spectral parsing workflows instead.
- The external service does not support HTTP POST queries or uses a fundamentally different API contract (e.g., gRPC, GraphQL); adapt the request formatting layer.

## Inputs

- HTTP POST request with form-encoded parameters (chemical shift values, multiplicities, integration counts)
- Configuration pointing to external prediction service URL (nmrshiftdb or equivalent)
- Validation schema for peak data (acceptable ranges, data types)

## Outputs

- Parsed and validated peaks data structure
- HTTP request payload formatted for external prediction service
- JSON response containing predicted NMR signals or molecular structure matches
- Client-facing JSON result with prediction outcomes

## How to apply

Implement a Flask endpoint (e.g., /predict/by_peaks_form or /api/v1/chemspectra/predict/nmr_peaks_form) that receives POST requests with form-encoded peak data. Parse the form parameters to extract chemical shift values, multiplicities, and integration counts using Flask's request.form interface. Validate each parsed parameter against expected ranges and data types (e.g., chemical shift ∈ [0, 14] ppm for ¹H NMR, multiplicity ∈ {s, d, t, q, m}, integration ≥ 0). Format the validated peaks into the query schema expected by the target service (e.g., nmrshiftdb HTTP API). Send an HTTP POST request to the external service with the formatted query. Parse the response, extract matching NMR signals, and return the result as JSON to the client. Use gunicorn to serve the Flask application with appropriate worker threads for concurrent request handling.

## Related tools

- **Flask** (Framework for implementing HTTP POST endpoints that receive, parse, and route form-encoded spectroscopic parameters to validation and formatting logic)
- **Python 3** (Language for implementing request parsing, data validation, and HTTP client operations in the ChemSpectra backend) — https://github.com/ComPlat/chem-spectra-app
- **gunicorn** (WSGI server for deploying Flask endpoints and handling concurrent form-encoded POST requests with multiple worker processes) — https://github.com/ComPlat/chem-spectra-app
- **curl** (Command-line utility for testing form-encoded POST requests and verifying endpoint behavior during development) — https://github.com/ComPlat/chem-spectra-app
- **nmrshiftdb** (External service that receives formatted peak queries and returns NMR signal predictions and molecular structure matches)

## Examples

```
curl -X POST http://localhost:3007/api/v1/chemspectra/predict/nmr_peaks_form -d 'peaks_data=[{"shift": 7.2, "multiplicity": "d", "integration": 2.0}, {"shift": 3.8, "multiplicity": "s", "integration": 3.0}]'
```

## Evaluation signals

- Form parameters are successfully extracted and assigned to the correct variables (peaks data contains expected keys: chemical shift, multiplicity, integration).
- Validation rejects out-of-range values (e.g., chemical shift > 14 ppm for ¹H, negative integration) and returns a 400 Bad Request with descriptive error messages.
- Formatted query payload matches the external service's documented schema; HTTP POST to nmrshiftdb succeeds (HTTP 200–299 response).
- Returned JSON response contains predicted NMR signals with matching structure identifiers or chemical annotations; response can be deserialized without parsing errors.
- Endpoint handles concurrent requests without race conditions or dropped form parameters when served with multiple gunicorn workers.

## Limitations

- Form-encoded parameters are limited in size by server configuration (typically 1–10 MB); very large peak lists (>10,000 peaks) may require pagination or switching to multipart/form-data or JSON.
- External service (nmrshiftdb) availability and query latency are not controlled by the backend; timeouts or service outages will propagate to clients.
- Validation logic must be kept in sync with both the client submission format and the external service's query schema; mismatches can silently produce incorrect predictions.
- No explicit changelog is provided in the repository; changes to form parameter naming or validation rules across releases may break existing client integrations.

## Evidence

- [other] Receive POST request at endpoint /predict/by_peaks_form or /api/v1/chemspectra/predict/nmr_peaks_form with peaks data as form parameters.: "Receive POST request at endpoint /predict/by_peaks_form or /api/v1/chemspectra/predict/nmr_peaks_form with peaks data as form parameters."
- [other] Parse and validate the peaks data (chemical shift values, multiplicities, integration).: "Parse and validate the peaks data (chemical shift values, multiplicities, integration)."
- [other] Format the peaks data into a query compatible with nmrshiftdb HTTP API.: "Format the peaks data into a query compatible with nmrshiftdb HTTP API."
- [other] Send HTTP POST request to the external nmrshiftdb service at URL_NSHIFTDB (configured in config.py) with formatted query.: "Send HTTP POST request to the external nmrshiftdb service at URL_NSHIFTDB (configured in config.py) with formatted query."
- [other] gunicorn -w 4 -b 0.0.0.0:3007 server:app --daemon: "gunicorn -w 4 -b 0.0.0.0:3007 server:app --daemon"
