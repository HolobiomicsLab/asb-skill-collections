---
name: http-post-request-construction
description: Use when you need to submit structured chemical compound data (identifiers
  and structural representations) to a remote REST API that accepts POST requests
  and returns JSON responses, particularly when the API requires tab-separated compound
  inputs separated by newlines and a query label as the.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3760
  edam_topics:
  - http://edamontology.org/topic_0154
  tools:
  - Ruby
  - rest-client gem
  tool_license:
    tier: noncommercial
    requires_ack: true
    ref: Academic use free; commercial use/redistribution by permission of the authors
      (Wishart Lab).
    url: https://bitbucket.org/wishartlab/classyfire_api.git
  license_tier: noncommercial
derived_from:
- doi: 10.1186/s13321-016-0174-y
  title: ClassyFire
evidence_spans:
- in order to use the commands below in a Ruby console
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_classyfire_cq
    doi: 10.1186/s13321-016-0174-y
    title: ClassyFire
  dedup_kept_from: coll_classyfire_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-016-0174-y
  all_source_dois:
  - 10.1186/s13321-016-0174-y
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# http-post-request-construction

> **License: noncommercial** — confirm your use is a permitted (noncommercial) purpose before applying; commercial use requires a separate license (see `metadata.tool_license`). <!-- asb-license-banner -->
## Summary

Construct and execute HTTP POST requests to remote APIs, formatting compound data as tab-separated values with newline delimiters and capturing JSON responses for downstream processing. This skill enables programmatic submission of chemical structure queries to web services like ClassyFire for automated classification.

## When to use

Use this skill when you need to submit structured chemical compound data (identifiers and structural representations) to a remote REST API that accepts POST requests and returns JSON responses, particularly when the API requires tab-separated compound inputs separated by newlines and a query label as the request body.

## When NOT to use

- Input data is already in binary or pre-serialized format incompatible with tab-separated text encoding
- The target API does not accept POST requests or requires a different request body format (e.g., JSON object, XML, multipart form data)
- Network connectivity is unavailable or the API endpoint is unreachable

## Inputs

- Query label (string)
- Compound identifiers (list of strings)
- Chemical structure representations (list of SMILES, InChI, or IUPAC names)
- API endpoint URL (string)

## Outputs

- HTTP response body (JSON)
- Query ID (string)
- Server status message (string)

## How to apply

Load the rest-client gem (v1.8.0) in a Ruby environment and construct a POST request to the target API endpoint. Format the request body as a query label followed by tab-separated compound inputs separated by newlines, where each line contains a compound identifier, a tab character, and a chemical structure representation in SMILES, InChI, or IUPAC name format. Execute the HTTP POST call using RestClient, capture the JSON response containing the query ID and status, and parse the response for downstream polling or result retrieval. Validate that the response structure matches the expected schema before proceeding.

## Related tools

- **rest-client gem** (Constructs and executes HTTP POST requests to the ClassyFire API endpoint; handles request serialization, network I/O, and JSON response parsing)
- **Ruby** (Runtime environment for loading rest-client and executing the POST request workflow)

## Examples

```
RestClient.post('http://classyfire.wishartlab.com/queries', "query_label\ncompound1\tCC(=O)Nc1ccc(O)cc1\ncompound2\tCC(C)Cc1ccc(cc1)C(C)C(O)=O")
```

## Evaluation signals

- HTTP response status code is 2xx (success) or matches documented API success codes
- Returned JSON contains expected keys (e.g., query ID and status fields) matching the API schema
- Query ID is non-null and can be used for subsequent polling or result retrieval operations
- Request body is correctly formatted with query label, tab characters, and newline delimiters as verified by server acceptance
- No network timeouts or connection errors occur during POST execution

## Limitations

- The skill assumes the target API accepts tab-separated, newline-delimited text input; APIs requiring JSON objects or other formats require reformulation
- No built-in retry logic or error handling for transient network failures or rate limiting
- Chemical structure representations must be in one of three supported formats (SMILES, InChI, IUPAC name); other formats require preprocessing
- Large compound batches may exceed API payload size limits or server timeout thresholds

## Evidence

- [other] The submit_query method accepts a query label and tab-separated compound inputs (identifier and structural representation) separated by newlines, formatted as individual lines where each line contains a compound identifier, tab character, and chemical structure representation (SMILES, InChI, or IUPAC name format).: "accepts a query label and tab-separated compound inputs (identifier and structural representation) separated by newlines, formatted as individual lines where each line contains a compound identifier,"
- [other] Construct a POST request to the ClassyFire API submit_query endpoint with a query label and tab-separated compound inputs separated by newlines as the request body.: "Construct a POST request to the ClassyFire API submit_query endpoint with a query label and tab-separated compound inputs separated by newlines as the request body"
- [other] Execute the HTTP POST call and capture the JSON response containing the query ID and status.: "Execute the HTTP POST call and capture the JSON response containing the query ID and status"
- [other] Load the rest-client gem (v1.8.0) in a Ruby environment.: "Load the rest-client gem (v1.8.0) in a Ruby environment"
- [intro] A query can be submitted using the POST method: "A query can be submitted using the POST method"
