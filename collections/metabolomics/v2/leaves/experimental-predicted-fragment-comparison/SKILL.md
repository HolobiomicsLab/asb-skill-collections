---
name: experimental-predicted-fragment-comparison
description: Use when when you have downloaded or retrieved fragment records from
  both experimental and predicted fragment databases as part of the DNA adductomics
  resource, and you need to verify that all fragments can be successfully mapped to
  their parent compound entries in the reference SDF-format compound.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3283
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_0154
  tools:
  - SDF file parser / molecular structure library
  license_tier: restricted
  provenance_tier: literature
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

# experimental-predicted-fragment-comparison

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Cross-reference and validate fragment records from experimental and predicted online databases against a reference compound database in SDF format to identify orphaned fragments and quantify matching success. This skill ensures data integrity and completeness in DNA adductomics fragment resources.

## When to use

When you have downloaded or retrieved fragment records from both experimental and predicted fragment databases as part of the DNA adductomics resource, and you need to verify that all fragments can be successfully mapped to their parent compound entries in the reference SDF-format compound database.

## When NOT to use

- Fragment records have already been independently verified or curated by the database maintainers and no uncertainty exists regarding compound linkage.
- You do not have access to the reference SDF-format compound database or an up-to-date version of it.
- Fragment identifiers use proprietary or undocumented encoding that cannot be reliably cross-referenced to compound entries.

## Inputs

- Online experimental fragments database records (native format)
- Online predicted fragments database records (native format)
- Reference compound database in SDF format

## Outputs

- Validation report documenting total fragments retrieved
- Count of successfully matched fragments to compounds
- List of orphaned fragments lacking parent entry
- Overall matching success rate (percentage)

## How to apply

First, parse and load the SDF-format DNA adduct reference compound database into memory using an SDF parser or molecular structure library. Next, download or retrieve fragment records from both the experimental and predicted online fragment databases in their native format. For each fragment record in both databases, extract the compound identifier or cross-reference field. Validate each identifier by querying against the loaded reference compound database, tracking matches and mismatches. Finally, aggregate results to calculate the matching success rate and identify orphaned fragments lacking parent compound entries.

## Related tools

- **SDF file parser / molecular structure library** (Parses and loads the SDF-format compound reference database for cross-referencing during validation)

## Evaluation signals

- All fragment records from both experimental and predicted databases are successfully retrieved and parsed without truncation or decoding errors.
- Every compound identifier present in the fragment databases can be located in the reference compound database; no unresolved references remain.
- The validation report lists the total number of fragments, the count matched to compounds, any orphaned fragments, and a calculated success rate that is reproducible and audit-traceable.
- Orphaned fragments (if any) are documented with their identifiers and potential reasons for mismatches (e.g., database version mismatch, naming convention changes).
- The matching success rate meets or exceeds expected thresholds for database quality assurance as defined by the DNA adductomics project standards.

## Limitations

- The success of this comparison depends on the currency and consistency of all three data sources (experimental fragments, predicted fragments, reference compounds); version mismatch or stale data can inflate orphan counts.
- Compound identifiers must use a consistent naming or encoding scheme across all three databases; heterogeneous identifier formats may lead to false negatives.
- The validation reports the presence or absence of cross-references but does not assess the scientific accuracy or chemical relevance of the fragments themselves.
- No changelog is available to track historical changes or corrections to the fragment databases, limiting ability to audit why orphaned fragments may have emerged.

## Evidence

- [other] Two separate online databases of experimental and predicted fragments are available as part of the DNA adductomics database resource: "Two separate online databases of experimental and predicted fragments are available as part of the DNA adductomics database resource, alongside the main DNA adduct database and compound database in"
- [other] For each fragment record in both experimental and predicted databases, extract the compound identifier or cross-reference field: "For each fragment record in both experimental and predicted databases, extract the compound identifier or cross-reference field."
- [other] Validate that each compound identifier present in the fragment databases has a corresponding entry in the reference compound database: "Validate that each compound identifier present in the fragment databases has a corresponding entry in the reference compound database."
- [other] Generate a validation report documenting the total number of fragments retrieved, the number successfully matched to compounds, any orphaned fragments lacking a parent compound entry, and the overall matching success rate: "Generate a validation report documenting the total number of fragments retrieved, the number successfully matched to compounds, any orphaned fragments lacking a parent compound entry, and the overall"
- [other] SDF file parser / molecular structure library used as tools for the workflow: "tools: SDF file parser / molecular structure library"
