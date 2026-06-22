---
name: compound-identifier-extraction
description: Use when when you receive a raw query string destined for the ClassyFire API and need to distinguish between a user-supplied compound identifier (e.g., a database accession or common name) and the actual chemical structure representation (SMILES, InChI, IAPNIC name, or FASTA sequence).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0209
  - http://edamontology.org/topic_3070
  tools:
  - Ruby
  - rest-client gem
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
---

# compound-identifier-extraction

## Summary

Extract and separate optional compound identifiers from structural representation strings in chemical query inputs. This skill enables routing of multi-format chemical data (SMILES, InChI, IUPAC name, FASTA) by first isolating metadata from structure.

## When to use

When you receive a raw query string destined for the ClassyFire API and need to distinguish between a user-supplied compound identifier (e.g., a database accession or common name) and the actual chemical structure representation (SMILES, InChI, IAPNIC name, or FASTA sequence). Apply this skill before attempting structure format detection or API dispatch.

## When NOT to use

- Input is already pre-parsed or originated from a structured database field with identifier and structure stored separately
- The delimiter convention for your workflow uses a character other than tab (e.g., comma, pipe, or space)

## Inputs

- Query string with optional tab-delimited compound identifier and structural representation

## Outputs

- Compound identifier (string or nil)
- Structural representation (string: SMILES, InChI, IUPAC name, or FASTA sequence)

## How to apply

Split the input query string on a tab delimiter to separate the optional compound identifier from the structural representation. The compound identifier is optional and appears first; if only one field is present, the entire string is the structural representation with no identifier. Retain both components for downstream dispatch and annotation: the identifier is used for result tracking and compound reference, while the structural representation is routed to the appropriate ClassyFire API endpoint based on its format. This two-stage parsing (extraction first, then format detection) ensures that classification results can be reliably mapped back to the original query.

## Related tools

- **rest-client gem** (Ruby HTTP client for dispatching parsed queries to ClassyFire API via POST after identifier extraction) — https://bitbucket.org/wishartlab/classyfire_api

## Evaluation signals

- Tab-delimited input consistently splits into exactly two fields (or one if no identifier present)
- Extracted compound identifier is a non-empty string (or nil/empty when absent) and does not contain tab or newline characters
- Structural representation field contains one of the expected syntax patterns (SMILES, InChI prefix, FASTA format indicator, or IUPAC-like nomenclature) suitable for downstream format detection
- When re-joined on tab (if identifier is present), the original input string is recovered
- Downstream format detection and API dispatch succeed using the extracted structural representation

## Limitations

- If the compound identifier itself legitimately contains tab characters, this parsing strategy will fail; alternative delimiters or escape conventions would be needed
- No validation of identifier format or content is performed; malformed or oversized identifiers pass through to the API, which may reject them
- If the input uses a different delimiter convention (e.g., comma or pipe) instead of tab, extraction will fail silently and misinterpret the input as structure-only

## Evidence

- [other] The ClassyFire API accepts query input consisting of an optional compound identifier and structural representation separated by a tab: "The ClassyFire API accepts query input consisting of an optional compound identifier and structural representation separated by a tab"
- [other] Parse the input query string to extract the optional compound identifier and structural representation, splitting on tab delimiter.: "Parse the input query string to extract the optional compound identifier and structural representation, splitting on tab delimiter"
- [intro] ClassyFire is a resource that allows you to automatically classify any chemical compound based on its structure: "ClassyFire is a resource that allows you to automatically classify any chemical compound based on its structure"
