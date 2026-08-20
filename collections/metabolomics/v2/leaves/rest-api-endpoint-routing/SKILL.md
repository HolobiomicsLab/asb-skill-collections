---
name: rest-api-endpoint-routing
description: Use when your input is a raw query string containing a chemical compound
  identifier and structural representation (e.g. tab-delimited compound ID + structure),
  and you need to submit it to the ClassyFire API for automatic structure-based classification.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3314
  tools:
  - rest-client gem
  - Ruby
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

# rest-api-endpoint-routing

> **License: noncommercial** — confirm your use is a permitted (noncommercial) purpose before applying; commercial use requires a separate license (see `metadata.tool_license`). <!-- asb-license-banner -->
## Summary

Route chemical structure query input (SMILES, InChI, IUPAC name, or FASTA) to the correct ClassyFire API endpoint by detecting the structural representation type via pattern matching and dispatching via REST POST. This skill enables correct parsing and submission of heterogeneous chemical compound formats to a unified classification API.

## When to use

Your input is a raw query string containing a chemical compound identifier and structural representation (e.g. tab-delimited compound ID + structure), and you need to submit it to the ClassyFire API for automatic structure-based classification. The structural representation format is unknown or mixed within a batch, requiring runtime detection and type-specific endpoint routing.

## When NOT to use

- Input is already a validated, classified compound record from ClassyFire (re-routing would be redundant).
- Structural representation is in a format not supported by ClassyFire (e.g., MOL/SDF block format, SMARTS patterns, proprietary vendor formats).
- Query lacks sufficient information to disambiguate structure type (e.g., ambiguous text that matches multiple format patterns).

## Inputs

- Query input string with optional compound identifier and structural representation (tab-delimited)
- Structural representation in one of: Daylight SMILES format, InChI format, IUPAC name, or FASTA format

## Outputs

- REST API request object (prepared by rest-client gem)
- API response from ClassyFire containing structure classification results
- Routed query with detected structure type and appropriate endpoint parameter

## How to apply

Parse the input query string to extract the optional compound identifier and structural representation by splitting on a tab delimiter. Detect the structural representation type by pattern matching: test for Daylight SMILES syntax rules, InChI format prefix conventions (InChI= or InChIKey=), FASTA format indicators (lines starting with > or sequence characters), or IUPAC nomenclature patterns. Route the detected structure type to the corresponding ClassyFire API endpoint parameter key (e.g., 'smiles', 'inchi', 'fasta') and submit via POST method using the rest-client gem in Ruby. Return the dispatched request object or API response for downstream processing and validation.

## Related tools

- **rest-client gem** (Ruby HTTP client library used to construct and dispatch POST requests to ClassyFire API endpoints with the detected structure type parameter)
- **ClassyFire API** (Remote API resource that receives routed structure queries and returns automatic chemical compound classification results) — bitbucket.org/wishartlab/classyfire_api

## Evaluation signals

- The detected structure type matches the true format of the input (validated by format-specific validators: SMILES parser, InChI standard, FASTA spec, IUPAC nomenclature rule).
- The REST POST request is submitted to the correct ClassyFire endpoint parameter key corresponding to the detected type (e.g., 'smiles' key for SMILES input).
- The API response HTTP status code is 2xx (success), indicating the routed query was accepted and processed.
- Round-trip consistency: re-parsing the returned classification record links back to the original structure input without loss of information.
- No format detection errors or ambiguities are logged; the detection algorithm produced exactly one matched route.

## Limitations

- Pattern-based format detection may ambiguously classify edge-case inputs (e.g., short IUPAC names that coincidentally match SMILES substrings); no formal grammar validation is applied during detection.
- The ClassyFire API documentation does not specify error handling or retry behavior for malformed structures routed to incorrect endpoints; failure modes are not fully characterized.
- FASTA format detection does not distinguish between valid peptide/nucleotide sequences and random sequence-like text; garbage input may route successfully but fail at the API.
- The skill assumes tab-delimited input format; alternative delimiters or unstructured input containing both ID and structure without clear separation are not addressed.

## Evidence

- [other] ClassyFire accepts query input consisting of an optional compound identifier and structural representation separated by a tab: "The ClassyFire API accepts query input consisting of an optional compound identifier and structural representation separated by a tab"
- [other] structural representation dispatched according to its type: Daylight SMILES format, InChI format, IUPAC name, or FASTA format for peptide or nucleotide sequences: "with the structural representation dispatched according to its type: Daylight SMILES format, InChI format, IUPAC name, or FASTA format for peptide or nucleotide sequences"
- [other] Detect the structural representation type by pattern matching against SMILES syntax rules, InChI prefix conventions, FASTA format indicators, or IUPAC nomenclature patterns: "Detect the structural representation type by pattern matching against SMILES syntax rules, InChI prefix conventions, FASTA format indicators, or IUPAC nomenclature patterns"
- [other] Dispatch the parsed query to the corresponding ClassyFire API endpoint using the REST-client gem in Ruby, submitting via POST method: "Dispatch the parsed query to the corresponding ClassyFire API endpoint using the REST-client gem in Ruby, submitting via POST method with the appropriate parameter key for the detected structure type"
- [intro] A query can be submitted using the POST method: "A query can be submitted using the POST method"
