---
name: structural-representation-format-detection
description: Use when when you have a mixed-format input query that may contain a
  compound identifier and a structural representation separated by a tab delimiter,
  and you need to determine which ClassyFire API endpoint (SMILES, InChI, IUPAC, or
  FASTA) to submit the query to for chemical classification.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3314
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

# structural-representation-format-detection

## Summary

Detect and classify chemical structure input formats (SMILES, InChI, IUPAC name, or FASTA) from query strings to enable correct routing to ClassyFire API endpoints. This skill disambiguates among multiple structural representation syntaxes so that downstream classification requests are submitted to the correct endpoint.

## When to use

When you have a mixed-format input query that may contain a compound identifier and a structural representation separated by a tab delimiter, and you need to determine which ClassyFire API endpoint (SMILES, InChI, IUPAC, or FASTA) to submit the query to for chemical classification.

## When NOT to use

- Input is a pre-classified compound that has already been submitted to ClassyFire and returned a result.
- Input is a single structure format known in advance (e.g. you are certain all inputs are SMILES); direct submission without detection overhead is more efficient.
- Input lacks a structural representation component or is malformed such that tab-delimited parsing fails.

## Inputs

- query input string (tab-delimited: optional compound identifier + structural representation)
- structural representation (one of: Daylight SMILES, InChI string, IUPAC name, FASTA sequence)

## Outputs

- dispatched request object
- API response from ClassyFire endpoint
- classification result for the submitted chemical compound

## How to apply

Parse the input query string by splitting on the tab delimiter to extract an optional compound identifier and the structural representation. Apply pattern matching against format-specific syntax rules: SMILES syntax rules (Daylight format), InChI prefix conventions, FASTA format indicators (sequence headers and codes), and IUPAC nomenclature patterns. Classify the detected format and dispatch the parsed query to the corresponding ClassyFire API endpoint using the REST-client gem via POST method with the appropriate parameter key for that structure type. Return the dispatched request object or API response for downstream processing.

## Related tools

- **rest-client gem** (HTTP client library for submitting POST requests to ClassyFire API endpoints with the detected parameter key)
- **Ruby** (Programming language environment in which to parse input query strings, apply format detection logic, and orchestrate API calls)
- **ClassyFire API** (Target REST API that accepts routed queries for automatic chemical compound classification based on structure) — bitbucket.org/wishartlab/classyfire_api

## Evaluation signals

- Query string is successfully split on tab delimiter into compound identifier (if present) and structural representation.
- Pattern matching correctly classifies the structural representation into one of the four formats (SMILES, InChI, IUPAC, FASTA) with no misclassification.
- The correct ClassyFire API endpoint parameter key is selected and used in the POST request body.
- API response is received without 400/422 errors indicating malformed parameter keys or incompatible format submission.
- Returned classification result is chemically plausible for the submitted structure (e.g., compound class, chemical ontology hierarchy is populated).

## Limitations

- IUPAC nomenclature patterns are complex and context-dependent; some systematic IUPAC names may not be reliably distinguished from free-text input without additional heuristics.
- Ambiguous or malformed inputs (e.g., truncated SMILES, incomplete InChI strings) may lead to misclassification and failed API submission.
- FASTA format detection relies on header and sequence code conventions; non-standard FASTA variants may not be recognized.
- No changelog or version tracking documented for the ClassyFire API, so format changes or new accepted structures may not be immediately discoverable.

## Evidence

- [other] Parse input query string; detect structural representation type; dispatch to appropriate endpoint: "Parse the input query string to extract the optional compound identifier and structural representation, splitting on tab delimiter. Detect the structural representation type by pattern matching"
- [intro] ClassyFire API accepts tab-delimited input with multiple format types: "The ClassyFire API accepts query input consisting of an optional compound identifier and structural representation separated by a tab, with the structural representation dispatched according to its"
- [intro] POST method submission via REST-client gem: "submitting via POST method with the appropriate parameter key for the detected structure type"
- [intro] ClassyFire enables chemical classification from structure: "ClassyFire is a resource that allows you to automatically classify any chemical compound based on its structure"
