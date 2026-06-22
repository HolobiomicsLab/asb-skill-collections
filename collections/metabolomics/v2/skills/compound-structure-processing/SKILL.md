---
name: compound-structure-processing
description: Use when you have a collection of DNA adduct or small-molecule compound structures stored in SDF format and need to prepare them for computational workflows like CFM-ID fragment prediction, or when integrating new compounds into a structured compound database.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3407
  tools:
  - CFM-ID
derived_from:
- doi: 10.3389/fchem.2022.908572
  title: DNA adduct database
evidence_spans:
- CFM-ID
- the CFM-ID spectra, the Chemdraw files, the mol files and the SDF files of the DNA adducts
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

# compound-structure-processing

## Summary

Load and prepare chemical compound structures from SDF format files for downstream computational analysis, such as in-silico fragment prediction. This skill ensures compound structures are correctly formatted and validated before submission to spectral prediction tools.

## When to use

Use this skill when you have a collection of DNA adduct or small-molecule compound structures stored in SDF format and need to prepare them for computational workflows like CFM-ID fragment prediction, or when integrating new compounds into a structured compound database.

## When NOT to use

- Input structures are already in a processed intermediate format (e.g., SMILES strings or serialized objects) and do not require SDF parsing.
- Compounds lack required metadata (e.g., molecular formula, charge state) and cannot be validated against downstream tool requirements.
- SDF file is corrupted, incomplete, or contains malformed structure records that cannot be reliably parsed.

## Inputs

- SDF format file containing DNA adduct compound structures
- Compound structure records with molecular connectivity and metadata

## Outputs

- Parsed and validated compound structures in memory or intermediate format
- Structured compound records with IDs, names, and molecular properties
- Compound inventory log documenting successful parsing

## How to apply

Load compound structures from the SDF format file into a computational environment (e.g., via chemistry library APIs). Validate that all structures are well-formed and contain required molecular properties (e.g., formal charge, connectivity). Parse structure metadata (e.g., compound IDs, names) from the SDF header and annotation fields. Confirm the structure count and diversity match the expected sample set. Structure the parsed data into a format compatible with the downstream tool (e.g., CFM-ID requires specific ionization levels and mass range specifications). Document the loading step and validate that all input compounds have been successfully parsed before proceeding to prediction.

## Related tools

- **CFM-ID** (Downstream tool for predicting fragment spectra from processed compound structures at specified ionization levels and mass ranges)

## Evaluation signals

- All compound records in the input SDF file are successfully parsed with no errors or warnings
- Parsed compound count matches the expected number of input structures
- Each parsed compound contains required fields: unique identifier, molecular structure, and ionization/mass parameters compatible with CFM-ID
- No duplicate or malformed structure records remain after validation
- Output can be directly ingested by CFM-ID without format conversion or manual curation

## Limitations

- SDF parsing quality depends on proper file formatting and adherence to standard SDF conventions; non-standard or legacy SDF variants may fail to parse correctly.
- Compound structures lacking formal charge information or containing ambiguous connectivity may not be compatible with downstream fragment prediction.
- No changelog or versioning system documented for tracking changes to compound structures or SDF file updates.

## Evidence

- [other] Load compound structures from the SDF format file containing DNA adduct compounds: "Load compound structures from the SDF format file containing DNA adduct compounds."
- [intro] Compound structures in SDF format available from database: "The following files are available: [Excel format, Word format, online, SDF format, experimental fragments online, predicted fragments online, collection of Excel file, online databases, CFM-ID]"
- [other] SDF files are input to CFM-ID for fragment prediction: "Execute CFM-ID on each compound structure to predict fragment spectra at the appropriate ionization level and mass range."
- [other] Validation required for completeness: "Validate output by confirming all input compounds have corresponding predicted spectra entries."
