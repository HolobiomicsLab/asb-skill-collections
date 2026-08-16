---
name: model-metadata-extraction
description: Use when when you need to programmatically interface with a TensorFlow
  Serving model instance and must discover or validate the expected input names (e.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - tensorflow serving
  - TensorFlow Serving
  techniques:
  - NMR
  license_tier: restricted
derived_from:
- doi: 10.1186/s13321-023-00738-4
  title: DeepSAT
evidence_spans:
- We pass through tensorflow serving at this url
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_deepsat
    doi: 10.1186/s13321-023-00738-4
    title: DeepSAT
  dedup_kept_from: coll_deepsat
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-023-00738-4
  all_source_dois:
  - 10.1186/s13321-023-00738-4
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# model-metadata-extraction

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Extract and validate model input/output names and API contracts from a TensorFlow Serving instance via the /model/metadata endpoint. This skill is essential when integrating with deployed ML models where input field names must be verified before constructing prediction requests.

## When to use

When you need to programmatically interface with a TensorFlow Serving model instance and must discover or validate the expected input names (e.g., '1H', '13C' spectroscopy headers) before submitting data for inference, especially when model definitions may change and code must remain synchronized.

## When NOT to use

- The model is not served via TensorFlow Serving (use the appropriate metadata endpoint for other serving frameworks)
- You already have hardcoded knowledge of input names and do not need dynamic validation

## Inputs

- TensorFlow Serving instance URL and model name
- Expected input field names (e.g., list of required header names)

## Outputs

- JSON object containing extracted model input names
- JSON object containing extracted model output names
- Validation status (pass/fail) of API contract match

## How to apply

Construct an HTTP GET request to the TensorFlow Serving /model/metadata endpoint for the target model instance (e.g., http://<host>/model/metadata). Execute the request and parse the returned JSON response to extract the model's input names, output names, and signature definition. Validate that the response contains the required top-level fields (signature, inputs, outputs) and that the extracted input names match the expected schema for your data (e.g., presence of '1H' and '13C' headers for NMR spectroscopy). Write both the extracted metadata and validation status to an output JSON file for downstream validation and code generation. If input names differ from expectations, flag this as requiring code updates.

## Related tools

- **TensorFlow Serving** (HTTP service exposing /model/metadata endpoint for querying model schema and input/output contracts)

## Evaluation signals

- HTTP response status code is 200 and response is valid JSON
- Extracted input names match the expected schema (e.g., presence of '1H' and '13C' headers)
- Response contains all required fields: signature, inputs, outputs
- Validation status correctly reflects whether extracted names match expectations
- Output JSON is well-formed and contains both metadata and validation results

## Limitations

- Requires network access to the TensorFlow Serving instance; network failures will prevent metadata retrieval
- Changes to model input names require corresponding code updates, creating a coupling between model definition and application code
- No changelog or version history available to track metadata changes over time

## Evidence

- [intro] The SMART 3 system queries model metadata via the /model/metadata endpoint: "We pass through tensorflow serving at this url: /model/metadata"
- [intro] Input names must be extracted and may require code updates if they change: "If the model input names change, then we need to change it in the code"
- [intro] Expected input names for the SMART 3 model are '1H' and '13C' headers: "You can put in your peaks as a json list of dicts, with 1H,13C as headers"
