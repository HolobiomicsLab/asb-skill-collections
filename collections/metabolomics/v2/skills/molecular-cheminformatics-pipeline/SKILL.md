---
name: molecular-cheminformatics-pipeline
description: Use when you have raw molecular structures in SMILES or SDF format and need to prepare molecular descriptors as input to a descriptor-based classifier (e.g., BitterPredict.m).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3627
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3407
  tools:
  - BitterPredict
  - RDKit
  - BitterPredict.m
derived_from:
- doi: 10.1021/acs.jafc.3c09767
  title: bittermass
evidence_spans:
- BitterPredict is a classifier which predicts whether a compound is bitter or not, based on its chemical structure.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_bittermass
    doi: 10.1021/acs.jafc.3c09767
    title: bittermass
  dedup_kept_from: coll_bittermass
schema_version: 0.2.0
---

# Reconstruct the chemical structure descriptor extraction pipeline

## Summary

Convert raw molecular structures (SMILES or SDF) into pre-computed descriptor tables (CSV or Excel) suitable for downstream machine-learning classifiers like BitterPredict. This pipeline bridges molecular representation and feature engineering by validating chemical syntax, calculating descriptors, and formatting output.

## When to use

You have raw molecular structures in SMILES or SDF format and need to prepare molecular descriptors as input to a descriptor-based classifier (e.g., BitterPredict.m). Use this skill when the classifier requires CSV or Excel files containing pre-calculated structural descriptors, and you need to document the complete preparation workflow from structure to feature table.

## When NOT to use

- Input is already a pre-computed CSV or Excel descriptor table; proceed directly to classification.
- Descriptor specification is unavailable or undocumented for the target classifier.
- Raw structures contain unresolvable or non-standard chemical notation that the chosen parser cannot validate.

## Inputs

- SMILES strings (text file or list)
- SDF (Structure Data Format) files
- Molecular identifier metadata (optional)

## Outputs

- CSV file with molecular descriptors
- Excel file with molecular descriptors
- Descriptor table (molecules × descriptors)

## How to apply

Load raw molecular structures in SMILES or SDF format and parse them using a cheminformatics library (e.g., RDKit) to validate chemical syntax and catch malformed SMILES. Calculate the full set of molecular descriptors required by the downstream classifier from the validated structures. Assemble the computed descriptors into a structured table with one molecule per row and one descriptor per column. Export the resulting descriptor table to CSV or Excel format matching the classifier's input specification (as documented in BitterPredict.m, which requires pre-computed descriptors without specification of which descriptors are required). Verify row and column alignment before export.

## Related tools

- **RDKit** (Parses and validates SMILES/SDF structures; calculates molecular descriptors from validated structures)
- **BitterPredict.m** (Target classifier that accepts the prepared CSV/Excel descriptor tables as input for taste prediction) — https://github.com/Niv-Lab/BitterPredict1

## Evaluation signals

- All input SMILES/SDF strings parse without errors; validation report shows 0 syntax failures.
- Descriptor table has one row per input molecule and one column per descriptor; no missing values in required descriptor columns.
- Exported CSV or Excel file conforms to BitterPredict.m input specification (details found in BitterPredict.m file).
- Row order and molecule identifiers are consistent between input structures and output descriptor table.
- Descriptor values fall within chemically plausible ranges (e.g., molecular weight > 0, no NaN in required fields).

## Limitations

- Descriptor specification and preparation workflow details are documented only within the BitterPredict.m file itself; no standalone descriptor documentation is provided in the publication or README.
- The README states 'full code will be available upon publication,' implying descriptor lists and exact calculation methods may not be accessible before publication.
- No validation or normalization of descriptor ranges is mentioned; classifiers may be sensitive to descriptor scale.
- Descriptor calculation depends entirely on the cheminformatics parser chosen (e.g., RDKit); different tools may yield slightly different descriptors for the same structure.

## Evidence

- [readme] BitterPredict.m gets as input CSV or EXCEL files with required descriptors of molecules: "BitterPredict.m gets as input CSV or EXCEL files with required descriptors of molecules"
- [other] Load raw molecular structures in SMILES or SDF format. Parse and validate molecular structure syntax using a cheminformatics parser (e.g., RDKit). Calculate the complete set of molecular descriptors required by BitterPredict.m from the validated structures. Assemble descriptors into a structured table with molecules as rows and descriptor columns as required. Export the descriptor table to CSV or Excel format compatible with BitterPredict.m input specification.: "1. Load raw molecular structures in SMILES or SDF format. 2. Parse and validate molecular structure syntax using a cheminformatics parser (e.g., RDKit). 3. Calculate the complete set of molecular"
- [readme] Details and examples of how to use the code is avalibale inside bitterPredict.m file.: "Details and examples of how to use the code is avalibale inside bitterPredict.m file."
- [intro] BitterPredict is a classifier which predicts whether a compound is bitter or not, based on its chemical structure.: "BitterPredict is a classifier which predicts whether a compound is bitter or not, based on its chemical structure."
