---
name: fragment-record-cross-reference-validation
description: Use when you have downloaded fragment records from separate experimental and predicted fragment databases and need to verify that every fragment can be traced back to a valid compound entry in the reference SDF-format compound database, particularly when integrating multiple database sources into a.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3407
  tools:
  - SDF file parser / molecular structure library
derived_from:
- doi: 10.3389/fchem.2022.908572
  title: DNA adduct database
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_dna_adduct_database_cq
    doi: 10.3389/fchem.2022.908572
    title: DNA adduct database
  dedup_kept_from: coll_dna_adduct_database_cq
schema_version: 0.2.0
---

# fragment-record-cross-reference-validation

## Summary

Validate that all fragment records from experimental and predicted fragment databases can be successfully matched to their parent compound entries in a reference compound database. This skill ensures data integrity and completeness of DNA adductomics database resources by detecting orphaned fragments lacking parent compound records.

## When to use

Apply this skill when you have downloaded fragment records from separate experimental and predicted fragment databases and need to verify that every fragment can be traced back to a valid compound entry in the reference SDF-format compound database, particularly when integrating multiple database sources into a unified DNA adductomics resource.

## When NOT to use

- Fragment databases have already been validated and cross-referenced in a prior workflow step
- Only a single fragment database is available (validation requires both experimental and predicted sources for comprehensive coverage)
- Reference compound database is not available or in an unparseable format

## Inputs

- Experimental fragment records (native online database format)
- Predicted fragment records (native online database format)
- Reference compound database (SDF format)

## Outputs

- Validation report with fragment count metrics
- Orphaned fragment list (fragments without parent compounds)
- Cross-reference matching success rate (%)

## How to apply

First, retrieve fragment records from both the online experimental fragments database and the online predicted fragments database in their native format. Load the reference compound database in SDF format using an SDF parser. For each fragment record in both databases, extract the compound identifier or cross-reference field that links to the parent compound. Validate that each extracted compound identifier has a corresponding entry in the loaded reference compound database. Generate a validation report that documents the total number of fragments retrieved, the count successfully matched to compounds, any orphaned fragments lacking a parent compound entry, and the overall matching success rate as a percentage.

## Related tools

- **SDF file parser / molecular structure library** (Parse and index the SDF-format reference compound database to enable cross-reference lookups by compound identifier)

## Evaluation signals

- All fragment records from both databases are processed without parser errors or missing values
- Cross-reference matching success rate is ≥95% (industry standard for database integration)
- Validation report explicitly lists any orphaned fragments by compound ID for manual investigation
- The sum of matched fragments plus orphaned fragments equals the total fragments retrieved
- Sample spot-checks of matched fragment–compound pairs confirm that identifiers in fragments database correspond to valid SDF entries

## Limitations

- Validation depends on the completeness and accuracy of the reference compound database; a missing or outdated reference entry will incorrectly flag valid fragments as orphaned
- Cross-reference fields may be inconsistently formatted (e.g., leading zeros, whitespace, case sensitivity) across databases, requiring normalization before matching
- Validation cannot detect fragments that have been assigned to the wrong parent compound; it only confirms that a matching identifier exists

## Evidence

- [other] Can all fragment records in the online experimental and predicted fragment databases be successfully loaded and cross-referenced to their corresponding compound entries in the DNA adduct database?: "Can all fragment records in the online experimental and predicted fragment databases be successfully loaded and cross-referenced to their corresponding compound entries"
- [other] Two separate online databases of experimental and predicted fragments are available as part of the DNA adductomics database resource: "Two separate online databases of experimental and predicted fragments are available as part of the DNA adductomics database resource"
- [other] For each fragment record in both experimental and predicted databases, extract the compound identifier or cross-reference field. Validate that each compound identifier present in the fragment databases has a corresponding entry in the reference compound database.: "For each fragment record in both experimental and predicted databases, extract the compound identifier or cross-reference field. Validate that each compound identifier present in the fragment"
- [other] Generate a validation report documenting the total number of fragments retrieved, the number successfully matched to compounds, any orphaned fragments lacking a parent compound entry, and the overall matching success rate.: "Generate a validation report documenting the total number of fragments retrieved, the number successfully matched to compounds, any orphaned fragments lacking a parent compound entry, and the overall"
- [intro] The DNA adduct database in Excel format, Word format, online, compound database in SDF format: "compound database in SDF format"
