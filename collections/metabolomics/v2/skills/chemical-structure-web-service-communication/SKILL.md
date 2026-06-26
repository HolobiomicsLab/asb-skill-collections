---
name: chemical-structure-web-service-communication
description: Use when you have a collection of chemical compounds (identified by name,
  SMILES, InChI, or other standard identifier) that you need to classify by structural
  features, and you want to submit them in batch to a remote web service rather than
  performing local computation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3346
  edam_topics:
  - http://edamontology.org/topic_0209
  - http://edamontology.org/topic_3343
  tools:
  - Ruby
  - rest-client gem
  - ClassyFire API
  tool_license:
    tier: noncommercial
    requires_ack: true
    ref: Academic use free; commercial use/redistribution by permission of the authors
      (Wishart Lab).
    url: https://bitbucket.org/wishartlab/classyfire_api.git
  license_tier: noncommercial
  provenance_tier: literature
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

# chemical-structure-web-service-communication

> **License: noncommercial** — confirm your use is a permitted (noncommercial) purpose before applying; commercial use requires a separate license (see `metadata.tool_license`). <!-- asb-license-banner -->
## Summary

Construct and execute HTTP POST requests to the ClassyFire API to submit batches of chemical compounds for automatic structure-based classification, receiving a query ID for downstream polling and result retrieval.

## When to use

You have a collection of chemical compounds (identified by name, SMILES, InChI, or other standard identifier) that you need to classify by structural features, and you want to submit them in batch to a remote web service rather than performing local computation.

## When NOT to use

- You only have a single compound to classify and do not need batch submission.
- You require synchronous (blocking) classification results; ClassyFire API responses are asynchronous and require polling.
- Your chemical structures are in a format not supported by ClassyFire (e.g., binary molecular formats, MOL2 without conversion to SMILES/InChI).

## Inputs

- query label (string)
- compound identifiers (list of strings)
- chemical structure representations (SMILES, InChI, or IUPAC name strings)
- tab-separated compound input (newline-delimited text)

## Outputs

- JSON response object containing query ID
- query status (from server response)
- query ID (for polling and result retrieval)

## How to apply

Load the rest-client gem (v1.8.0) in a Ruby environment and construct a POST request to the ClassyFire API submit_query endpoint. Format the request body as a query label followed by tab-separated compound inputs separated by newlines, where each line contains a compound identifier, a tab character, and a chemical structure representation (SMILES, InChI, or IUPAC name). Execute the HTTP POST call and parse the returned JSON response to extract the query ID and status. Use the query ID to poll for classification results via subsequent API calls.

## Related tools

- **rest-client gem** (HTTP client library used to construct and execute POST requests to the ClassyFire API endpoint)
- **Ruby** (Programming environment in which rest-client commands are executed and JSON responses are parsed)
- **ClassyFire API** (Remote web service that receives POST requests containing compound structures and returns query IDs for classification tracking) — bitbucket.org/wishartlab/classyfire_api

## Examples

```
RestClient.post('http://classyfire.wishartlab.com/queries', { label: 'my_batch', data: "aspirin\tCC(=O)Oc1ccccc1C(=O)O\nibuprofen\tCC(C)Cc1ccc(cc1)C(C)C(=O)O" })
```

## Evaluation signals

- HTTP response status code is 200 or 201 (POST accepted).
- Returned JSON response contains a non-null query ID field.
- Query ID can be used in subsequent GET requests to the ClassyFire API to retrieve classification results.
- All submitted compounds are parsed and accepted by the server (no validation errors in response).
- Tab-separated input format is correctly parsed by the server (confirmed by subsequent polling returning status 'Done' with classification data).

## Limitations

- ClassyFire API submission is asynchronous; results are not returned in the POST response but must be retrieved via polling using the returned query ID.
- Compound structures must be formatted as SMILES, InChI, or IUPAC names; other chemical data formats require prior conversion.
- No changelog is available for the ClassyFire API, making version compatibility and breaking changes difficult to track.

## Evidence

- [other] The submit_query method accepts a query label and tab-separated compound inputs (identifier and structural representation) separated by newlines: "The submit_query method accepts a query label and tab-separated compound inputs (identifier and structural representation) separated by newlines, formatted as individual lines where each line"
- [other] Execute the HTTP POST call and capture the JSON response containing the query ID and status: "Execute the HTTP POST call and capture the JSON response containing the query ID and status."
- [intro] ClassyFire is a resource that allows automatic classification based on structure: "ClassyFire is a resource that allows you to automatically classify any chemical compound based on its structure"
- [intro] A query can be submitted using the POST method: "A query can be submitted using the POST method"
- [intro] rest-client gem version specification: "Load the rest-client gem (v1.8.0) in a Ruby environment."
