---
name: json-response-serialization
description: Use when when a backend service receives structured prediction results
  from an external API (e.g., nmrshiftdb peak predictions) and must return them to
  a client application via HTTP POST response.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0602
  tools:
  - Flask
  - Python 3
  - curl
  - gunicorn
  techniques:
  - NMR
  license_tier: open
derived_from:
- doi: 10.1186/s13321-020-00481-0
  title: ChemSpectra
evidence_spans:
- export FLASK_APP=chem_spectra && export FLASK_DEBUG=true && flask run
- export FLASK_APP=chem_spectra && export FLASK_DEBUG=true && flask run --host=0.0.0.0
  --port=3007
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

# json-response-serialization

## Summary

Serialize spectroscopic prediction results (NMR peak matches from external inference services) into JSON format for HTTP response delivery to client applications. This skill ensures consistent, machine-readable output from backend web services handling chemical spectrum analysis.

## When to use

When a backend service receives structured prediction results from an external API (e.g., nmrshiftdb peak predictions) and must return them to a client application via HTTP POST response. Specifically applies after parsing and validating external service responses containing NMR signal matches, multiplicities, or chemical shift assignments.

## When NOT to use

- Input is already a valid JSON string or stream—serialize only once
- Response format is specified as XML, Protocol Buffers, or other non-JSON serialization by the client API contract
- Prediction results must be streamed or chunked (use streaming JSON or NDJSON instead of single JSON object)

## Inputs

- Parsed nmrshiftdb HTTP response containing matching NMR signals and peak metadata
- Python dict or object representation of spectrum prediction results
- Peak data with fields: chemical shift values, multiplicities, integration

## Outputs

- JSON-serialized HTTP response body containing NMR peak predictions
- JSON object with prediction metadata and matched signal records

## How to apply

After the backend service receives and parses the nmrshiftdb HTTP response containing matching NMR signals, format the prediction result into a JSON object structure suitable for HTTP transmission. The serialization must preserve the hierarchical nature of spectrum metadata (chemical shifts, multiplicities, integration values) while conforming to the client's expected schema. Use Flask's built-in JSON serialization or Python's json module to convert the parsed response objects into valid JSON. Return the serialized JSON via Flask's response object (e.g., jsonify() or direct JSON dumps) with appropriate Content-Type headers. Validation occurs implicitly through JSON schema conformance—malformed or incomplete data will either fail serialization or be flagged by client-side schema validation.

## Related tools

- **Flask** (HTTP framework providing jsonify() and response handlers for JSON serialization and delivery) — https://github.com/ComPlat/chem-spectra-app
- **Python 3** (Host language for json module and dict-to-JSON conversion logic) — https://github.com/ComPlat/chem-spectra-app
- **gunicorn** (WSGI server that receives and transmits JSON-serialized responses over HTTP) — https://github.com/ComPlat/chem-spectra-app

## Examples

```
curl -X POST http://localhost:3007/api/v1/chemspectra/predict/nmr_peaks_form -d 'peaks_data={...}' -H 'Content-Type: application/x-www-form-urlencoded'
```

## Evaluation signals

- JSON response is valid according to RFC 7158 (parseable by json.loads() or equivalent)
- Response Content-Type header is 'application/json' or 'application/json; charset=utf-8'
- HTTP POST response body contains all expected prediction fields: chemical shifts, multiplicities, and integration values from the nmrshiftdb result
- Client-side JavaScript or Python JSON parser successfully deserializes the response without error
- Serialized JSON preserves numeric precision and data types (e.g., float vs. string for chemical shift values)

## Limitations

- JSON serialization requires all field values be JSON-serializable (Datetime objects, NumPy arrays, or custom classes may need explicit encoder or pre-conversion)
- Large nmrshiftdb result sets may produce unwieldy JSON payloads; no implicit pagination or truncation is mentioned in the workflow
- The external nmrshiftdb service response format must be known and validated before serialization to avoid inclusion of malformed or unexpected fields

## Evidence

- [other] Parse the nmrshiftdb response containing matching NMR signals: "Parse the nmrshiftdb response containing matching NMR signals."
- [other] Format and return the prediction result to the client as JSON: "Format and return the prediction result to the client as JSON."
- [other] Parse and validate the peaks data (chemical shift values, multiplicities, integration): "Parse and validate the peaks data (chemical shift values, multiplicities, integration)."
- [readme] export FLASK_APP=chem_spectra && export FLASK_DEBUG=true && flask run: "export FLASK_APP=chem_spectra && export FLASK_DEBUG=true && flask run"
