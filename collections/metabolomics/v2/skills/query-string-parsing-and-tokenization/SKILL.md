---
name: query-string-parsing-and-tokenization
description: Use when when you have a user-provided or system-generated query string
  containing a chemical structure in unknown or mixed format, and you need to route
  it to a structure-specific API endpoint (such as ClassyFire) that requires knowing
  whether the input is SMILES, InChI, IUPAC nomenclature, or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_2814
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

# query-string-parsing-and-tokenization

> **License: noncommercial** — confirm your use is a permitted (noncommercial) purpose before applying; commercial use requires a separate license (see `metadata.tool_license`). <!-- asb-license-banner -->
## Summary

Parse and tokenize chemical structure query strings to extract optional compound identifiers and structural representations, then classify the representation type (SMILES, InChI, IUPAC name, or FASTA) for routing to the appropriate ClassyFire API endpoint. This skill enables flexible input handling for automated chemical compound classification.

## When to use

When you have a user-provided or system-generated query string containing a chemical structure in unknown or mixed format, and you need to route it to a structure-specific API endpoint (such as ClassyFire) that requires knowing whether the input is SMILES, InChI, IUPAC nomenclature, or FASTA sequence notation.

## When NOT to use

- The input query is already known to be a single format (e.g., you have already validated it is valid SMILES) — skip to direct endpoint routing.
- The structure format is not one of the four supported types (SMILES, InChI, IUPAC, FASTA) — routing will fail or produce undefined behavior.

## Inputs

- query string (tab-delimited: optional compound identifier + structural representation)
- structural representation string (SMILES, InChI, IUPAC name, or FASTA format)

## Outputs

- parsed query object (compound identifier and structural representation)
- structure type classification (SMILES | InChI | IUPAC | FASTA)
- REST API request object or response from ClassyFire

## How to apply

Split the input query string on a tab delimiter to separate an optional compound identifier from the structural representation. Detect the structural representation type by applying pattern matching against SMILES syntax rules (Daylight conventions), InChI prefix conventions (e.g., 'InChI=' prefix), FASTA format indicators (e.g., '>' header lines), or IUPAC nomenclature patterns. Once the type is identified, dispatch the parsed query to the corresponding ClassyFire API endpoint using the REST-client gem via POST method, supplying the appropriate parameter key for the detected structure type. Return the dispatched request object or API response for downstream classification processing.

## Related tools

- **rest-client gem** (HTTP client library for submitting POST requests to ClassyFire API endpoints with parsed query parameters)
- **Ruby** (Programming language for implementing query parsing, type detection, and REST API dispatch logic)
- **ClassyFire API** (Target API endpoint that receives parsed and routed structure queries for automated chemical compound classification) — bitbucket.org/wishartlab/classyfire_api

## Evaluation signals

- The query string is correctly split into identifier and structural representation components; tab delimiter is respected.
- The detected structure type matches the actual format of the structural representation (e.g., SMILES strings start with valid atom symbols, InChI strings begin with 'InChI=', FASTA lines start with '>', IUPAC names follow nomenclature conventions).
- The REST POST request is dispatched to the correct ClassyFire API endpoint for the detected structure type, with the appropriate parameter key.
- The API response object is returned without transport errors; HTTP status code indicates successful submission (e.g., 200 or 202).
- Compound classification results are retrievable from the returned response, confirming the structure was correctly parsed and routed.

## Limitations

- Pattern matching for IUPAC nomenclature can be ambiguous; complex or non-standard IUPAC names may fail detection.
- Input must be well-formed and follow the tab-delimited convention; malformed queries will not parse correctly.
- FASTA format detection relies on header line indicators; short or atypical FASTA sequences may be misclassified.
- The skill does not validate the chemical correctness of the parsed structure; invalid but syntactically correct representations will still be routed and may fail at the ClassyFire API level.

## Evidence

- [other] The ClassyFire API accepts query input consisting of an optional compound identifier and structural representation separated by a tab: "The ClassyFire API accepts query input consisting of an optional compound identifier and structural representation separated by a tab, with the structural representation dispatched according to its"
- [other] Detect the structural representation type by pattern matching against SMILES syntax rules, InChI prefix conventions, FASTA format indicators, or IUPAC nomenclature patterns: "Detect the structural representation type by pattern matching against SMILES syntax rules, InChI prefix conventions, FASTA format indicators, or IUPAC nomenclature patterns."
- [other] Dispatch the parsed query to the corresponding ClassyFire API endpoint using the REST-client gem in Ruby, submitting via POST method: "Dispatch the parsed query to the corresponding ClassyFire API endpoint using the REST-client gem in Ruby, submitting via POST method with the appropriate parameter key for the detected structure type."
- [intro] A query can be submitted using the POST method: "A query can be submitted using the POST method"
