---
name: metabolite-record-deduplication
description: Use when you have extracted metabolite records from two or more public metabolomics databases (e.g., HMDB, MassBank, METLIN) and need to merge them into a single reference database.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3364
  edam_topics:
  - http://edamontology.org/topic_0639
  - http://edamontology.org/topic_3172
  tools:
  - openNAU
derived_from:
- doi: 10.21147/j.issn.1000-9604.2023.05.11
  title: OpenNAU
evidence_spans:
- An open-source analysis software for untargeted metabolism data (openNAU) was constructed
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_opennau_cq
    doi: 10.21147/j.issn.1000-9604.2023.05.11
    title: OpenNAU
  dedup_kept_from: coll_opennau_cq
schema_version: 0.2.0
---

# metabolite-record-deduplication

## Summary

Deduplicate metabolite records aggregated from multiple public metabolomics databases by matching on molecular identifiers (molecular formula, InChI, InChIKey) to remove redundant entries and create a unified reference database. This skill is essential when integrating data from heterogeneous sources (HMDB, MassBank, METLIN) to ensure each unique chemical entity is represented only once.

## When to use

Apply this skill when you have extracted metabolite records from two or more public metabolomics databases (e.g., HMDB, MassBank, METLIN) and need to merge them into a single reference database. Deduplication is required when the same metabolite may exist under different molecular identifiers, nomenclature variants, or data entry errors across source databases, and you need to establish a canonical set of metabolite records for downstream mass spectral matching and metabolite annotation.

## When NOT to use

- Input metabolite records are already from a single source database (no cross-database redundancy expected)
- Isomeric or stereoisomeric variants must be kept distinct — deduplication on InChI/InChIKey alone may collapse these into a single record
- Records have already been deduplicated or curated by the source database provider

## Inputs

- Extracted metabolite records from individual public databases with standardized field names
- Molecular identifiers: molecular formula, InChI, InChIKey
- Chemical properties and mass spectral signatures per record

## Outputs

- Deduplicated reference metabolite table with indexed fields
- Merged metabolite records with unique chemical identifiers
- Deduplication report documenting removed redundant entries

## How to apply

After standardizing field names, data types, and nomenclature across all source databases, perform record-level matching on primary identifiers in order of specificity: (1) InChIKey (most specific), (2) InChI, then (3) molecular formula (least specific). Mark records with identical values at any tier as duplicates and retain only one representative entry per unique metabolite, preserving the most complete metadata from the deduplicated set. Index the final merged reference table on these identifiers to enable rapid querying during metabolite annotation. Validate completeness by comparing the merged record count against expected source record counts and verifying key metadata fields are populated in the deduplicated output.

## Related tools

- **openNAU** (Reference metabolomics database platform incorporating deduplicated records from public databases for untargeted metabolomics analysis) — https://github.com/zjuRong/openNAU

## Evaluation signals

- Deduplicated record count is less than or equal to the sum of source database records, with documented reduction ratio
- Each remaining record has a unique InChIKey or InChI value (no duplicate molecular identifiers)
- All key metadata fields (molecular formula, chemical name, mass spectral signatures) are populated for ≥95% of deduplicated records
- Spot-check: known metabolites present in multiple source databases (e.g., glucose, alanine) appear exactly once in the merged table
- Query performance on indexed molecular identifiers is sub-second for reference lookups during downstream metabolite annotation

## Limitations

- Deduplication relies on accuracy and consistency of molecular identifiers (InChIKey, InChI, molecular formula); errors or missing values in source data can cause false duplicates or missed duplicates
- InChI and InChIKey do not distinguish between some structural variants (e.g., salt forms, protonation states); post-deduplication curation may be needed for strict chemical equivalence
- Source databases may use different reference standards or conventions for chemical properties; standardization across databases is a prerequisite and may introduce subtle information loss

## Evidence

- [other] Assembly logic for deduplication: "Perform deduplication by matching records on molecular formula, InChI, or InChIKey to remove redundant entries."
- [other] Source databases integrated: "Identify and access public metabolomics databases (e.g., HMDB, MassBank, METLIN) referenced in openNAU documentation."
- [other] Validation approach: "Validate completeness and consistency of the merged database against source record counts and key metadata fields."
- [readme] Reference database construction context: "A reference metabolomics database based on public databases was also constructed."
