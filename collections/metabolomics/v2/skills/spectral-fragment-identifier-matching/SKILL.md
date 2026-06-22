---
name: spectral-fragment-identifier-matching
description: Use when when you have downloaded fragment records from separate experimental and predicted online databases and need to verify that each fragment can be traced back to a valid compound entry in a reference compound database (e.g., SDF-format DNA adduct compound collection).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
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

# spectral-fragment-identifier-matching

## Summary

Cross-reference fragment records from experimental and predicted mass spectrometry databases against a reference compound database to validate data integrity and identify orphaned fragments. This skill ensures that all fragment entries in DNA adductomics databases have corresponding parent compound entries in standardized SDF format.

## When to use

When you have downloaded fragment records from separate experimental and predicted online databases and need to verify that each fragment can be traced back to a valid compound entry in a reference compound database (e.g., SDF-format DNA adduct compound collection). Apply this skill during database curation, quality assurance, or when integrating heterogeneous fragment sources into a unified resource.

## When NOT to use

- Fragment records are already known to be validated and cross-referenced (redundant application)
- You have only a single fragment database with no reference compound database available for validation
- Input fragment data lacks compound identifier or cross-reference fields (insufficient metadata for matching)

## Inputs

- Experimental fragment database records (native online format or downloaded)
- Predicted fragment database records (native online format or downloaded)
- Reference compound database in SDF format

## Outputs

- Validation report documenting total fragments retrieved
- Count of fragments successfully matched to compounds
- List of orphaned fragments lacking parent compound entries
- Overall matching success rate (percentage or ratio)

## How to apply

Load the SDF-format reference compound database and extract all valid compound identifiers. Parse the experimental and predicted fragment databases (in their native online or downloaded format) to retrieve the compound identifier or cross-reference field for each fragment record. For each fragment, perform a lookup against the reference compound identifiers. Track successful matches, orphaned fragments (lacking a parent entry), and any identifier format mismatches. Generate a validation report quantifying total fragments retrieved, successful matches, orphaned count, and overall matching success rate (e.g., percentage of fragments with a corresponding compound). Use this report to identify data gaps, format inconsistencies, or missing cross-references that require curation.

## Related tools

- **SDF file parser / molecular structure library** (Parse and load SDF-format reference compound database; extract compound identifiers and validate structure records)

## Evaluation signals

- All fragment records retrieved from both online experimental and predicted databases are successfully parsed and loaded
- Each fragment's compound identifier is extracted without error and formatted consistently
- All compound identifiers present in fragment databases have corresponding entries in the reference SDF compound database (zero or near-zero orphaned fragment rate)
- Validation report totals sum correctly (successful matches + orphaned fragments = total fragments retrieved)
- No duplicate matches or cross-reference conflicts are detected during lookup

## Limitations

- Orphaned fragments may arise from database version mismatches or identifier naming convention differences across online resources, requiring manual curation
- Compound identifier format inconsistencies (e.g., case sensitivity, prefix variations) can cause false negatives in matching; standardization may be required prior to lookup
- The skill depends on the integrity and currency of the online experimental and predicted fragment databases; changes or outages in external sources may affect reproducibility

## Evidence

- [other] Two separate online databases of experimental and predicted fragments are available as part of the DNA adductomics database resource: "Two separate online databases of experimental and predicted fragments are available as part of the DNA adductomics database resource, alongside the main DNA adduct database and compound database in"
- [other] For each fragment record in both experimental and predicted databases, extract the compound identifier or cross-reference field: "For each fragment record in both experimental and predicted databases, extract the compound identifier or cross-reference field."
- [other] Generate a validation report documenting the total number of fragments retrieved, the number successfully matched to compounds, any orphaned fragments lacking a parent compound entry, and the overall matching success rate: "Generate a validation report documenting the total number of fragments retrieved, the number successfully matched to compounds, any orphaned fragments lacking a parent compound entry, and the overall"
- [intro] Multiple formats and access points are available for the DNA adductomics database: Excel, Word, online interactive versions, SDF compound files, experimental and predicted fragment databases: "The DNA adduct database in Excel format, Word format, online, compound database in SDF format"
