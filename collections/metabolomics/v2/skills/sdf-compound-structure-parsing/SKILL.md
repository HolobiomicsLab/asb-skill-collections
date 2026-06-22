---
name: sdf-compound-structure-parsing
description: Use when when you have fragment records (experimental or predicted) with compound identifiers or cross-reference fields that need to be validated against a reference compound database in SDF format.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3778
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  tools:
  - SDF file parser / molecular structure library
derived_from:
- doi: 10.3389/fchem.2022.908572
  title: DNA adduct database
evidence_spans:
- SDF format
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3389/fchem.2022.908572
  all_source_dois:
  - 10.3389/fchem.2022.908572
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# sdf-compound-structure-parsing

## Summary

Parse and extract molecular structure and metadata from SDF-format compound databases to enable cross-referencing with fragment records and validation of compound identifiers. This skill is essential when working with DNA adduct reference databases where fragment entries must be matched to their parent compound records.

## When to use

When you have fragment records (experimental or predicted) with compound identifiers or cross-reference fields that need to be validated against a reference compound database in SDF format. Specifically, use this skill when you need to confirm that every fragment in your fragment databases has a corresponding parent compound entry in the reference compound collection.

## When NOT to use

- When fragment records do not contain compound identifiers or cross-reference fields to match against
- When the compound database is not in SDF format (e.g., already in Excel or Word format without structure data needed for this validation)
- When your goal is to perform molecular structure similarity or structural analysis rather than identifier validation

## Inputs

- SDF-format compound database file containing DNA adduct reference compounds
- Experimental fragment database records (with compound identifiers or cross-reference fields)
- Predicted fragment database records (with compound identifiers or cross-reference fields)

## Outputs

- Indexed lookup table of compound identifiers from SDF file
- Validation report documenting total fragments retrieved, successfully matched compounds, orphaned fragments, and matching success rate
- List of orphaned fragments lacking parent compound entries

## How to apply

Load the SDF-format compound database using a molecular structure library or SDF parser. Extract the compound identifier field from each record in the SDF file and build an indexed lookup table. For each fragment record in your experimental or predicted fragment database, retrieve its compound identifier and query the lookup table to verify a match exists. Track successful matches, orphaned fragments (those lacking a parent compound), and calculate the overall matching success rate. Generate a validation report documenting total fragments retrieved, number successfully matched to compounds, any unmatched fragments, and the success percentage to assess data integrity.

## Related tools

- **SDF file parser / molecular structure library** (Parse SDF format compound records, extract identifiers and metadata for lookup and cross-referencing)

## Evaluation signals

- All compound identifiers extracted from SDF file are unique and indexed correctly without duplicates
- Every fragment record in both experimental and predicted databases receives a matching attempt against the SDF lookup table
- The validation report accounts for 100% of input fragments (successfully matched + orphaned = total retrieved)
- Matching success rate is documented with explicit counts: total fragments, successful matches, and unmatched count
- Orphaned fragments (if any) are explicitly listed with their identifiers for manual inspection and database correction

## Limitations

- Compound identifier format must match exactly between fragment records and SDF file entries; format inconsistencies (leading zeros, case sensitivity, whitespace) will cause false non-matches
- SDF parser performance may degrade with very large compound databases; indexing strategy and memory management become critical
- Cross-reference fields in fragment databases may be missing, malformed, or inconsistent, requiring data cleaning prior to validation
- No changelog is available to track whether the reference compound database has been updated, potentially causing stale matches

## Evidence

- [other] Load the SDF-format compound database containing the DNA adduct reference compounds: "Load the SDF-format compound database containing the DNA adduct reference compounds."
- [other] Extract compound identifier and validate against reference database: "For each fragment record in both experimental and predicted databases, extract the compound identifier or cross-reference field. Validate that each compound identifier present in the fragment"
- [other] Generate validation report with matching metrics: "Generate a validation report documenting the total number of fragments retrieved, the number successfully matched to compounds, any orphaned fragments lacking a parent compound entry, and the overall"
- [intro] Multiple formats available for DNA adductomics database: "The DNA adduct database in Excel format, Word format, online, compound database in SDF format"
- [other] Tool for SDF parsing and molecular structures: "tools: SDF file parser / molecular structure library"
