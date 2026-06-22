---
name: chemical-structure-feature-encoding
description: Use when when you have a set of molecules with known chemical structures and need to prepare them for classification or prediction tasks.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3674
  edam_topics:
  - http://edamontology.org/topic_0209
  - http://edamontology.org/topic_3372
  tools:
  - BitterPredict
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jafc.3c09767
  all_source_dois:
  - 10.1021/acs.jafc.3c09767
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# chemical-structure-feature-encoding

## Summary

Encoding molecular structures as quantitative chemical descriptor vectors suitable for machine learning classifiers. This skill transforms raw chemical structures into tabular feature representations (CSV/Excel) that capture structural properties required for predictive modeling of molecular properties like bitterness.

## When to use

When you have a set of molecules with known chemical structures and need to prepare them for classification or prediction tasks. Specifically, when you aim to train or apply a classifier (such as BitterPredict) that requires pre-computed chemical structure descriptors as input rather than raw molecular formats.

## When NOT to use

- Input is already a computed feature table with chemical descriptors—proceed directly to classification.
- Molecular structures are unavailable or incompletely specified.
- The descriptor set required by the downstream classifier is unknown or incompletely documented.

## Inputs

- Chemical structures (SMILES, MOL, or SDF format)
- Molecule identifiers or names

## Outputs

- CSV or Excel file with molecular descriptors as columns
- Table with molecule identifiers and computed descriptor values (one row per molecule)

## How to apply

Compute or obtain a comprehensive set of molecular descriptors (physicochemical properties, structural fingerprints, and topological features) for each molecule in your study set. Organize these descriptors into a structured table format (CSV or Excel) with one row per molecule and one column per descriptor, alongside a column for molecule identifiers. The descriptors should capture the chemical properties relevant to the prediction task—in the BitterPredict use case, descriptors that correlate with bitter taste perception. Validate that all descriptors are numeric and that missing values are handled appropriately before passing the table to the downstream classifier.

## Related tools

- **BitterPredict** (Downstream classifier that consumes encoded molecular descriptors and produces bitter/not-bitter predictions) — https://github.com/Niv-Lab/BitterPredict1

## Evaluation signals

- Output CSV/Excel file has one row per input molecule and contains no empty cells in descriptor columns.
- All descriptor columns are numeric (integer or float) with no non-numeric values or text entries.
- Molecule identifiers in the output table match and are traceable back to input molecule specifications.
- Descriptor statistics (mean, range, distribution) are consistent with published benchmarks for the descriptor set used.
- The BitterPredict classifier successfully reads the encoded file without data type or schema errors and produces valid binary predictions for all rows.

## Limitations

- Descriptor computation quality and completeness depend on the molecular structure input format and the descriptor calculation tool; incomplete or ambiguous structures may yield unreliable descriptors.
- The choice of descriptor set is not fully specified in the article—the README notes that 'Details and examples of how to use the code is available inside bitterPredict.m file', suggesting descriptor requirements must be consulted from the actual implementation.
- The article does not discuss handling of special cases such as stereoisomers, salt forms, or protonation states, which may affect descriptor values and downstream predictions.

## Evidence

- [readme] BitterPredict.m gets as input CSV or EXCEL files with required descriptors of molecules: "BitterPredict.m gets as input CSV or EXCEL files with required descriptors of molecules"
- [intro] BitterPredict is a classifier which predicts whether a compound is bitter or not, based on its chemical structure.: "BitterPredict is a classifier which predicts whether a compound is bitter or not, based on its chemical structure."
- [other] Load input CSV or Excel file containing molecular descriptors for a set of molecules.: "Load input CSV or Excel file containing molecular descriptors for a set of molecules."
- [readme] calucautes a predictions if each molecule is bitter or not: "calucautes a predictions if each molecule is bitter or not"
