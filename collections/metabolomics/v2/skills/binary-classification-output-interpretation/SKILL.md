---
name: binary-classification-output-interpretation
description: Use when you have executed a binary classifier (such as BitterPredict.m)
  on a set of molecules with chemical structure descriptors and need to translate
  the raw predictions into a structured CSV output file that maps molecule identifiers
  to their predicted class labels (bitter or not-bitter).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3765
  edam_topics:
  - http://edamontology.org/topic_3474
  tools:
  - BitterPredict
  - BitterPredict.m
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.jafc.3c09767
  title: bittermass
evidence_spans:
- BitterPredict is a classifier which predicts whether a compound is bitter or not,
  based on its chemical structure.
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

# binary-classification-output-interpretation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Interpret and compile binary classification predictions (bitter/not-bitter) from a machine-learning classifier into structured output files linked to molecule identifiers. This skill bridges trained model inference and downstream analysis by organizing predictions into a reusable tabular format.

## When to use

You have executed a binary classifier (such as BitterPredict.m) on a set of molecules with chemical structure descriptors and need to translate the raw predictions into a structured CSV output file that maps molecule identifiers to their predicted class labels (bitter or not-bitter).

## When NOT to use

- The classifier output is already in a structured tabular format with molecule IDs and predictions — no recompilation is needed.
- You need confidence scores or probability estimates rather than binary class labels alone.
- The input molecules lack consistent identifiers that can be reliably mapped to predictions.

## Inputs

- Binary classification predictions (bitter/not-bitter) from BitterPredict.m classifier
- Molecule identifiers (from input descriptor file)
- Chemical structure descriptor data (from CSV or Excel input file)

## Outputs

- CSV file containing molecule identifiers and predicted class labels (bitter or not-bitter)

## How to apply

After BitterPredict.m generates binary bitter/not-bitter predictions for each molecule in your input descriptor set, collect the predicted class labels alongside the corresponding molecule identifiers. Organize these pairs into a structured table with columns for molecule ID and predicted class. Write the compiled table to a CSV output file. Verify that each molecule in the input has exactly one prediction and that all class labels are valid binary values (bitter or not-bitter). The output CSV should maintain the same row order as the input molecules to ensure traceability from input descriptors through prediction to final results.

## Related tools

- **BitterPredict.m** (Executes binary classification on molecular descriptors to generate bitter/not-bitter predictions for each molecule) — https://github.com/Niv-Lab/BitterPredict1

## Evaluation signals

- Every molecule identifier from the input descriptor file appears exactly once in the output CSV.
- Every prediction in the output CSV is a valid binary class label (bitter or not-bitter); no null, missing, or invalid values.
- The row order in the output CSV matches the row order of molecules in the input descriptor file, enabling traceability.
- The output CSV is parseable as a valid CSV file with consistent column structure and no formatting errors.
- Spot-check a sample of predictions by re-running BitterPredict.m on a subset of input molecules and confirming predictions match the compiled output.

## Limitations

- The skill assumes BitterPredict.m is fully executed before interpretation; if the classifier fails or produces incomplete predictions, the output CSV will be incomplete or incorrect.
- Full code availability is contingent on publication; current repository access may be restricted and users should contact [redacted-email] for availability.
- The CSV output contains only binary class labels; probability scores or confidence metrics from the classifier are not captured.
- Molecule identifiers must be present and consistent across input and output; missing or mismatched IDs will break traceability.

## Evidence

- [readme] BitterPredict.m gets as input CSV or EXCEL files with required descriptors of molecules, and calucautes a predictions if each molecule is bitter or not.: "BitterPredict.m gets as input CSV or EXCEL files with required descriptors of molecules, and calucautes a predictions if each molecule is bitter or not."
- [other] Generate binary predictions (bitter or not-bitter) for each molecule. 4. Compile predictions into output CSV file with molecule identifiers and predicted class labels.: "Generate binary predictions (bitter or not-bitter) for each molecule. 4. Compile predictions into output CSV file with molecule identifiers and predicted class labels."
- [readme] BitterPredict is a classifier which predicts whether a compound is bitter or not, based on its chemical structure.: "BitterPredict is a classifier which predicts whether a compound is bitter or not, based on its chemical structure."
