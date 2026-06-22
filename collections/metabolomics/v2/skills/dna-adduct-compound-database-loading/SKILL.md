---
name: dna-adduct-compound-database-loading
description: Use when you have downloaded fragment records from the experimental or predicted DNA adductomics databases and need to verify that each fragment can be matched to its corresponding compound entry in the SDF-format reference compound database, or when auditing completeness of a DNA adduct resource.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
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

# dna-adduct-compound-database-loading

## Summary

Load and cross-reference experimental and predicted fragment records against a reference compound database in SDF format to validate data integrity and identify orphaned fragments. This skill ensures that all fragment entries in DNA adductomics resources are traceable to their parent compound records.

## When to use

You have downloaded fragment records from the experimental or predicted DNA adductomics databases and need to verify that each fragment can be matched to its corresponding compound entry in the SDF-format reference compound database, or when auditing completeness of a DNA adduct resource for missing parent-compound linkages.

## When NOT to use

- You only need to analyze fragment spectra or molecular properties without compound linkage verification
- Fragment records are already pre-validated and cross-referenced in an integrated database
- Your workflow requires only a subset of fragments; full cross-reference validation is not necessary

## Inputs

- Experimental fragment database records (native format from online database)
- Predicted fragment database records (native format from online database)
- SDF-format compound database file
- Compound identifier mapping or cross-reference schema

## Outputs

- Validation report with fragment counts, match statistics, and success rate
- List of successfully matched fragment-to-compound pairs
- List of orphaned fragments (fragments without parent compound entry)

## How to apply

First, retrieve fragment records in their native format from both the experimental and predicted online fragment databases. Simultaneously load the SDF-format compound database containing reference DNA adduct compounds. Parse each SDF file to extract the internal compound identifiers or cross-reference fields. For each fragment record in both databases, extract the compound identifier and validate that a matching entry exists in the reference compound database. Generate a validation report that documents the total number of fragments retrieved, the count successfully matched to compounds, any orphaned fragments lacking a parent compound entry, and calculate the overall matching success rate as (matched fragments / total fragments).

## Related tools

- **SDF file parser / molecular structure library** (Parse and extract compound identifiers and structural data from SDF-format compound database)

## Evaluation signals

- Validation report shows 100% of fragment records matched to parent compounds with no orphaned entries
- Summary statistics match expected fragment counts from source databases (experimental and predicted counts reconcile)
- No duplicate compound identifiers in the reference database; each match is 1:1 or properly documented as many:1
- Cross-reference validation script runs without parsing errors on all input files
- Spot-check: randomly select 5–10 matched fragment-compound pairs and manually verify the cross-reference identifier is correct

## Limitations

- Relies on consistent compound identifier formatting between fragment and compound databases; inconsistent naming or missing identifiers will inflate orphan counts
- No changelog available for the DNA adductomics database, so version mismatches between fragment and compound data may cause false orphan reports
- SDF parser must support the specific SDF dialect and compound identifier field names used by the resource; non-standard SDF variants may require custom parsing logic
- The skill does not validate the correctness or currency of compound entries themselves—only that the cross-reference link exists

## Evidence

- [other] Can all fragment records in the online experimental and predicted fragment databases be successfully loaded and cross-referenced to their corresponding compound entries in the DNA adduct database?: "Can all fragment records in the online experimental and predicted fragment databases be successfully loaded and cross-referenced to their corresponding compound entries in the DNA adduct database?"
- [other] For each fragment record in both experimental and predicted databases, extract the compound identifier or cross-reference field.: "For each fragment record in both experimental and predicted databases, extract the compound identifier or cross-reference field."
- [other] Validate that each compound identifier present in the fragment databases has a corresponding entry in the reference compound database.: "Validate that each compound identifier present in the fragment databases has a corresponding entry in the reference compound database."
- [other] Generate a validation report documenting the total number of fragments retrieved, the number successfully matched to compounds, any orphaned fragments lacking a parent compound entry, and the overall matching success rate.: "Generate a validation report documenting the total number of fragments retrieved, the number successfully matched to compounds, any orphaned fragments lacking a parent compound entry, and the overall"
- [other] Two separate online databases of experimental and predicted fragments are available as part of the DNA adductomics database resource, alongside the main DNA adduct database and compound database in SDF format.: "Two separate online databases of experimental and predicted fragments are available as part of the DNA adductomics database resource, alongside the main DNA adduct database and compound database in"
