---
name: compound-query-formatting
description: Use when you have a set of chemical compounds (identified by name, SMILES,
  InChI, or other standard identifier) that you need to classify using ClassyFire,
  and you must prepare them as a single batch query body for the submit_query POST
  request.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3778
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3371
  tools:
  - Ruby
  - rest-client
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

# compound-query-formatting

## Summary

Format chemical compound identifiers and structural representations into tab-separated newline-delimited input for submission to the ClassyFire API POST endpoint. This skill ensures compounds are correctly serialized for batch classification queries.

## When to use

You have a set of chemical compounds (identified by name, SMILES, InChI, or other standard identifier) that you need to classify using ClassyFire, and you must prepare them as a single batch query body for the submit_query POST request.

## When NOT to use

- Compounds are already stored in a ClassyFire query and you only need to retrieve results (use result polling instead).
- You are submitting a single compound query with immediate result retrieval (consider alternative endpoints if available).
- Your compounds lack valid structural representation or identifiers that ClassyFire recognizes.

## Inputs

- List of compound identifiers (strings)
- List of chemical structure representations (SMILES, InChI, or IUPAC names)
- Query label (string)

## Outputs

- Tab-separated newline-delimited compound query string (formatted request body)
- HTTP POST request to ClassyFire submit_query endpoint
- JSON response containing query ID and status

## How to apply

Construct a query body by creating one line per compound, where each line contains a unique compound identifier (or label), followed by a tab character, followed by the chemical structure representation in SMILES, InChI, or IUPAC name format. Separate lines with newlines. Assign a descriptive query label to the entire batch. Pass this formatted string as the request body to the ClassyFire API submit_query POST endpoint using rest-client or equivalent HTTP client. The server will respond with a JSON object containing a query ID and initial status; parse this response to retrieve the query ID for downstream polling.

## Related tools

- **rest-client** (HTTP client library for constructing and executing the POST request to ClassyFire API)
- **ClassyFire API** (Target API endpoint for receiving formatted compound queries and returning classification results) — bitbucket.org/wishartlab/classyfire_api
- **Ruby** (Programming environment for loading rest-client gem and executing the formatted query submission)

## Examples

```
require 'rest-client'; body = "aspirin\tCC(=O)Oc1ccccc1C(=O)O\nibuprofen\tCC(C)Cc1ccc(cc1)C(C)C(=O)O"; response = RestClient.post('http://classyfire.wishartlab.com/queries', body, {params: {label: 'my_compounds'}}); puts response
```

## Evaluation signals

- Each line in the query body contains exactly one tab character separating identifier and structure.
- Lines are separated by newlines with no extra whitespace or blank lines between compounds.
- All structure representations conform to SMILES, InChI, or IUPAC name syntax (validated by ClassyFire accept/reject response).
- HTTP response status is 200 or 201 and contains a valid JSON object with 'query_id' and 'status' fields.
- Query ID returned can be used in subsequent polling requests to retrieve classification results without error.

## Limitations

- ClassyFire API may reject queries with invalid or unrecognized structure formats; ensure SMILES/InChI are well-formed.
- Batch size limits are not documented in the provided source; very large compound sets may need to be split into multiple queries.
- Tab-separated format is rigid; any embedded tabs in identifiers or structures will break line parsing.

## Evidence

- [other] The submit_query method accepts a query label and tab-separated compound inputs (identifier and structural representation) separated by newlines: "The submit_query method accepts a query label and tab-separated compound inputs (identifier and structural representation) separated by newlines, formatted as individual lines where each line"
- [other] Construct a POST request with query label and tab-separated compound inputs: "Construct a POST request to the ClassyFire API submit_query endpoint with a query label and tab-separated compound inputs separated by newlines as the request body."
- [other] Execute the HTTP POST call and capture the JSON response containing the query ID and status: "Execute the HTTP POST call and capture the JSON response containing the query ID and status."
- [intro] ClassyFire is a resource that allows you to automatically classify any chemical compound based on its structure: "ClassyFire is a resource that allows you to automatically classify any chemical compound based on its structure"
- [intro] A query can be submitted using the POST method: "A query can be submitted using the POST method"
