---
name: http-api-integration-with-external-services
description: Use when when your application needs to enrich or predict spectral properties (NMR peaks, molecular structure) by querying external databases, and you have peak data (chemical shift, multiplicity, integration) that must be transformed into a remote service's query format, validated, and the.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_3520
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# http-api-integration-with-external-services

## Summary

This skill integrates a local HTTP API endpoint with external web services (e.g., nmrshiftdb) by formatting spectral data into compatible query payloads, dispatching POST requests, and parsing responses. It enables chemical spectral prediction workflows where internal processing delegates specialized tasks to remote databases.

## When to use

When your application needs to enrich or predict spectral properties (NMR peaks, molecular structure) by querying external databases, and you have peak data (chemical shift, multiplicity, integration) that must be transformed into a remote service's query format, validated, and the response parsed back into your local data model.

## When NOT to use

- The external service is unavailable or has a high failure rate; implement caching or fallback strategies first.
- Peak data is malformed, incomplete, or fails validation; reject the request before dispatching to the external service.
- The external service query format changes frequently without version compatibility; version the API endpoint and document breaking changes.

## Inputs

- Peaks data as HTTP form parameters (chemical shift values, multiplicities, integration)
- External service configuration URL from config.py
- Spectral metadata (if required by external service)

## Outputs

- Prediction result as JSON response (matching NMR signals from external database)
- Formatted spectral predictions ready for client consumption

## How to apply

Receive spectral peak data (chemical shifts, multiplicities, integration values) at a Flask endpoint (e.g., /predict/by_peaks_form or /api/v1/chemspectra/predict/nmr_peaks_form) as form parameters. Parse and validate the peaks data for completeness and type correctness. Format the validated peaks into a query structure compatible with the external service's HTTP API (e.g., nmrshiftdb query format). Send a POST request to the external service URL (stored in config.py as URL_NSHIFTDB) with the formatted query. Parse the JSON or structured response from the external service to extract matching NMR signals or prediction results. Format the enriched results as JSON and return to the client, ensuring the response schema matches the client's expectations.

## Related tools

- **Flask** (HTTP server framework for defining API endpoints that receive peaks data and return predictions)
- **Python 3** (Language for implementing request parsing, validation, formatting, and response handling logic)
- **curl** (Command-line tool for testing HTTP API integration and verifying endpoint connectivity)
- **gunicorn** (WSGI application server for deploying the Flask API in production environments)
- **nmrshiftdb** (External HTTP API service that receives formatted NMR peak queries and returns spectral predictions)

## Examples

```
curl -X POST http://localhost:3007/api/v1/chemspectra/predict/nmr_peaks_form -d 'peaks=[{"shift":7.2,"multiplicity":"d","integration":2}]'
```

## Evaluation signals

- HTTP POST request to the endpoint returns a 200 status code with valid JSON containing predicted NMR signals.
- Parsed response from the external service contains non-empty matching signals field with chemical shift and multiplicity data.
- Validated peaks data conforms to the external service's expected query schema (correct field names, value ranges, data types).
- Round-trip test: submit known peaks to nmrshiftdb via the endpoint and verify that returned predictions match previously cached or manually verified results.
- Error handling: malformed peaks, missing config URL, or external service timeout returns appropriate HTTP error code (400, 500, 503) with descriptive error message.

## Limitations

- External service (nmrshiftdb) must be reachable and responsive; network failures or service downtime will cause prediction requests to fail.
- Query format compatibility depends on exact alignment between the local formatter and the external service's API specification; schema drift breaks integration.
- No retry logic or request timeout specified in the workflow; long-running external requests may block the Flask endpoint and timeout at the client.
- The article does not describe authentication mechanisms (API keys, OAuth) required by some external services; implementation may require additional security configuration.

## Evidence

- [other] Receive POST request at endpoint /predict/by_peaks_form or /api/v1/chemspectra/predict/nmr_peaks_form with peaks data as form parameters.: "Receive POST request at endpoint /predict/by_peaks_form or /api/v1/chemspectra/predict/nmr_peaks_form with peaks data as form parameters."
- [other] Parse and validate the peaks data (chemical shift values, multiplicities, integration).: "Parse and validate the peaks data (chemical shift values, multiplicities, integration)."
- [other] Format the peaks data into a query compatible with nmrshiftdb HTTP API.: "Format the peaks data into a query compatible with nmrshiftdb HTTP API."
- [other] Send HTTP POST request to the external nmrshiftdb service at URL_NSHIFTDB (configured in config.py) with formatted query.: "Send HTTP POST request to the external nmrshiftdb service at URL_NSHIFTDB (configured in config.py) with formatted query."
- [other] Parse the nmrshiftdb response containing matching NMR signals. Format and return the prediction result to the client as JSON.: "Parse the nmrshiftdb response containing matching NMR signals. Format and return the prediction result to the client as JSON."
