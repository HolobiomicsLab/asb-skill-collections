---
name: smiles-inchi-fasta-format-recognition
description: Use when when you have a mixed batch of chemical structure queries in unknown or variable formats (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3778
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3372
  tools:
  - Ruby
  - rest-client gem
  - ClassyFire API
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# smiles-inchi-fasta-format-recognition

## Summary

Detect and classify chemical structure input formats (SMILES, InChI, IUPAC name, or FASTA) from raw query strings to route them to the appropriate ClassyFire API endpoint. This skill enables automated dispatch of heterogeneous structural representations without manual reformatting.

## When to use

When you have a mixed batch of chemical structure queries in unknown or variable formats (e.g., user-submitted compound identifiers paired with Daylight SMILES, InChI strings, IUPAC nomenclature, or peptide/nucleotide FASTA sequences) and need to submit them to the ClassyFire API for automatic compound classification without prior format standardization.

## When NOT to use

- Input is already classified and routed to a specific ClassyFire endpoint — use direct submission instead.
- Structural representation is malformed or does not conform to any recognized syntax (SMILES, InChI, IUPAC, FASTA) — preprocessing or manual curation is needed first.
- Query string does not contain a structural representation component — validation or user clarification is required before classification.

## Inputs

- Query string with optional compound identifier and structural representation (tab-delimited)
- Daylight SMILES format string
- InChI format string
- IUPAC chemical name string
- FASTA format string (peptide or nucleotide sequences)

## Outputs

- Classified query object with detected format type
- HTTP POST request object dispatched to ClassyFire API
- API response object from ClassyFire service

## How to apply

Parse the input query string by splitting on a tab delimiter to extract an optional compound identifier and a structural representation component. Apply pattern matching against known syntax rules: test for SMILES compliance with Daylight conventions, check for InChI prefix markers (e.g., 'InChI='), detect FASTA format indicators (header lines starting with '>' for peptide or nucleotide sequences), or fall back to IAPIC nomenclature patterns. Once the structural type is identified, dispatch the parsed query to the corresponding ClassyFire POST endpoint using the rest-client gem in Ruby, submitting via the appropriate parameter key (e.g., 'smiles', 'inchi', 'fasta'). Capture and return the dispatched request object or API response for downstream validation.

## Related tools

- **rest-client gem** (Dispatch parsed queries to ClassyFire API endpoints via REST POST requests)
- **Ruby** (Execution environment for parsing, pattern matching, and API client logic)
- **ClassyFire API** (Target service receiving routed queries; returns compound classification results) — bitbucket.org/wishartlab/classyfire_api

## Evaluation signals

- Correctly identified format type matches the expected structural syntax (SMILES parses without Daylight rule violations, InChI begins with 'InChI=' prefix, FASTA header lines are present, IUPAC names are recognized by nomenclature patterns).
- HTTP POST request is dispatched to the correct ClassyFire API endpoint for the detected format (no misrouting or 400-level API errors).
- API response contains a valid classification result or acknowledgment (HTTP 200 or 201 status), not a parsing or parameter error.
- Compound identifier (if present) is preserved and returned in the API response metadata or downstream output.
- Tab-delimited parsing preserves both identifier and structural components without truncation or loss of special characters.

## Limitations

- Format detection relies on pattern matching heuristics; ambiguous or malformed inputs may be misclassified (e.g., a short SMILES string resembling IUPAC nomenclature).
- IUPAC name recognition is not fully formalized in the article; classification may default to IUPAC only after SMILES, InChI, and FASTA patterns are ruled out.
- The tab delimiter is mandatory for separating compound identifier and structural representation; queries without this delimiter may not parse correctly if an identifier is expected.
- No changelog or version history is documented, limiting understanding of API stability and backwards compatibility across rest-client gem versions.

## Evidence

- [other] The ClassyFire API accepts query input consisting of an optional compound identifier and structural representation separated by a tab, with the structural representation dispatched according to its type: Daylight SMILES format, InChI format, IUPAC name, or FASTA format for peptide or nucleotide sequences.: "The ClassyFire API accepts query input consisting of an optional compound identifier and structural representation separated by a tab, with the structural representation dispatched according to its"
- [other] Detect the structural representation type by pattern matching against SMILES syntax rules, InChI prefix conventions, FASTA format indicators, or IUPAC nomenclature patterns.: "Detect the structural representation type by pattern matching against SMILES syntax rules, InChI prefix conventions, FASTA format indicators, or IUPAC nomenclature patterns."
- [other] Dispatch the parsed query to the corresponding ClassyFire API endpoint using the REST-client gem in Ruby, submitting via POST method with the appropriate parameter key for the detected structure type.: "Dispatch the parsed query to the corresponding ClassyFire API endpoint using the REST-client gem in Ruby, submitting via POST method with the appropriate parameter key for the detected structure type."
- [intro] A query can be submitted using the POST method: "A query can be submitted using the POST method"
- [intro] ClassyFire is a resource that allows you to automatically classify any chemical compound based on its structure: "ClassyFire is a resource that allows you to automatically classify any chemical compound based on its structure"
