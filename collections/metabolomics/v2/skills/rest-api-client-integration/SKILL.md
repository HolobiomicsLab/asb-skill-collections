---
name: rest-api-client-integration
description: Use when you have a batch of chemical compounds (identifiers and structures
  in SMILES, InChI, or IUPAC format) that need to be submitted to a remote REST API
  for classification or analysis, and you require the server's response (query ID
  and status) to track or retrieve results asynchronously.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3336
  tools:
  - rest-client
  - Ruby
  - rest-client gem
  - ClassyFire API
  tool_license:
    tier: noncommercial
    requires_ack: true
    ref: Academic use free; commercial use/redistribution by permission of the authors
      (Wishart Lab).
    url: https://bitbucket.org/wishartlab/classyfire_api.git
derived_from:
- doi: 10.1186/s13321-016-0174-y
  title: ClassyFire
evidence_spans:
- gem 'rest-client', '=1.8.0'
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

# rest-api-client-integration

## Summary

Construct and execute HTTP POST requests to remote REST APIs using a Ruby client library, formatting compound data as tab-separated values and parsing JSON responses for downstream polling or result retrieval. This skill enables programmatic submission of chemical structure queries to web services like ClassyFire.

## When to use

You have a batch of chemical compounds (identifiers and structures in SMILES, InChI, or IUPAC format) that need to be submitted to a remote REST API for classification or analysis, and you require the server's response (query ID and status) to track or retrieve results asynchronously.

## When NOT to use

- The API endpoint does not accept POST requests or requires a different HTTP method (GET, PUT, DELETE).
- Compound structures are already encoded in a proprietary binary format or database blob incompatible with text-based SMILES/InChI/IUPAC representation.
- The REST API does not return a query ID or requires synchronous response with results embedded in the initial POST response, rather than asynchronous polling.

## Inputs

- compound_identifier (string)
- chemical_structure_representation (SMILES, InChI, or IUPAC name string)
- query_label (string)
- tab-separated compound input stream (newline-delimited)

## Outputs

- query_id (string, from JSON response)
- query_status (string, from JSON response)
- JSON response object

## How to apply

Load the rest-client gem (v1.8.0) in a Ruby environment. Format your compound inputs as tab-separated lines, where each line contains a compound identifier, a tab character, and the chemical structure representation (SMILES, InChI, or IUPAC name). Construct a POST request to the API's submit_query endpoint, embedding the formatted compound data and a descriptive query label in the request body. Execute the HTTP POST call using the rest-client library and capture the JSON response. Parse the response to extract the query ID and status fields for use in subsequent polling or result-retrieval workflows. Validate that the server responds with HTTP 200–299 status and valid JSON containing query metadata.

## Related tools

- **rest-client gem** (HTTP client library for constructing and executing POST requests to the ClassyFire API submit_query endpoint) — https://github.com/rest-client/rest-client
- **Ruby** (Runtime environment for executing rest-client commands and parsing JSON responses)
- **ClassyFire API** (Remote REST web service that accepts chemical compound submissions via POST and returns query tracking metadata) — https://bitbucket.org/wishartlab/classyfire_api

## Examples

```
require 'rest-client'; response = RestClient.post('http://classyfire.wishartlab.com/queries', {query_label: 'my_batch', compounds: "aspirin\t[O-]C(=O)c1ccccc1C(C)=O\ncaffeine\tCN1C=NC2=C1C(=O)N(C(=O)N2C)C"}, {content_type: :json}); puts response
```

## Evaluation signals

- HTTP response status code is 2xx (200–299), indicating successful POST submission.
- Returned JSON response contains required fields: query_id (non-empty string) and status (e.g., 'Submitted' or 'Done').
- The query_id is unique across multiple invocations and differs from previous submission IDs.
- Subsequent polling requests using the returned query_id successfully retrieve compound classification results from the same API.
- Tab-separated input format is correctly parsed by the API with no 'malformed request' or 'format error' messages in response.

## Limitations

- The skill requires network access to the remote API endpoint; offline or firewall-blocked environments cannot execute the POST request.
- API rate limiting or server throttling may cause POST submissions to be rejected or delayed if requests exceed service quotas.
- Compound structures must be representable in SMILES, InChI, or IUPAC name format; structures in proprietary or graphical formats require conversion preprocessing.
- The rest-client gem v1.8.0 is an older release; compatibility with modern Ruby versions (3.x+) or SSL/TLS configurations may require gem updates.

## Evidence

- [intro] rest-client gem v1.8.0 requirement: "Load the rest-client gem (v1.8.0) in a Ruby environment"
- [intro] POST method and tab-separated format specification: "The submit_query method accepts a query label and tab-separated compound inputs (identifier and structural representation) separated by newlines, formatted as individual lines where each line"
- [intro] POST request construction and execution workflow: "Construct a POST request to the ClassyFire API submit_query endpoint with a query label and tab-separated compound inputs separated by newlines as the request body. Execute the HTTP POST call and"
- [intro] Query submission via POST method: "A query can be submitted using the POST method"
- [intro] ClassyFire resource and automatic classification capability: "ClassyFire is a resource that allows you to automatically classify any chemical compound based on its structure"
