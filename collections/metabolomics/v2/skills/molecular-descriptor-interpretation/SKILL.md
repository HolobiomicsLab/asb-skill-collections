---
name: molecular-descriptor-interpretation
description: Use when you have a collection of molecules represented as CSV or EXCEL files containing computed molecular descriptors (e.g., physicochemical properties, structural features) and you need to predict whether each molecule will taste bitter.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_2258
  tools:
  - BitterPredict.m
derived_from:
- doi: 10.1021/acs.jafc.3c09767
  title: bittermass
evidence_spans:
- BitterPredict.m gets as input CSV or EXCEL files with required descriptors of molecules, and calucautes a predictions if each molecule is bitter or not
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_bittermass_cq
    doi: 10.1021/acs.jafc.3c09767
    title: bittermass
  dedup_kept_from: coll_bittermass_cq
schema_version: 0.2.0
---

# molecular-descriptor-interpretation

## Summary

Interpret molecular descriptor files (CSV or EXCEL format) as input to a bitterness classification model, translating chemical structure representations into per-molecule binary predictions (bitter or non-bitter). This skill bridges chemical descriptor preprocessing and taste prediction inference.

## When to use

You have a collection of molecules represented as CSV or EXCEL files containing computed molecular descriptors (e.g., physicochemical properties, structural features) and you need to predict whether each molecule will taste bitter. Use this skill when descriptor computation is complete and you are ready to pass structured descriptor tables to a trained classifier for binary outcome prediction.

## When NOT to use

- Molecular descriptors have not yet been computed from chemical structures
- Input file is missing required descriptor columns expected by the classifier
- You need probabilistic confidence scores rather than hard binary predictions

## Inputs

- CSV or EXCEL file with molecular descriptors
- Descriptor table (rows = molecules, columns = required molecular features)

## Outputs

- Binary predictions (bitter / not bitter) per molecule
- Structured output file with molecule identifiers and predicted class labels

## How to apply

Load the CSV or EXCEL file containing required molecular descriptors using file I/O (e.g., pandas.read_csv or readtable equivalents). Ensure the descriptor table includes all required molecular features expected by the BitterPredict.m classifier and is organized with one molecule per row. Pass the descriptor table directly to the BitterPredict.m classifier function. The classifier computes a binary prediction (bitter or not bitter) for each molecule. Compile the predictions into a structured output file mapping each molecule identifier to its predicted class label, preserving row order and providing clear column headers for molecule ID and predicted class.

## Related tools

- **BitterPredict.m** (Binary classifier that ingests molecular descriptor tables and generates per-molecule bitterness predictions) — https://github.com/Niv-Lab/BitterPredict1

## Evaluation signals

- Output file contains one prediction (bitter or not bitter) for each input molecule with no missing values
- Molecule identifiers in output match those in the input descriptor file
- Predictions are binary categorical values (not continuous scores or NaN)
- Row order and molecule count are preserved between input and output
- Output file schema includes explicit columns for molecule ID and predicted class label

## Limitations

- BitterPredict.m requires a specific set of precomputed molecular descriptors; missing or incorrectly scaled descriptors will cause errors or invalid predictions
- Full code availability was conditional on publication status at the time of documentation; implementation details for replication may be limited
- Binary predictions do not provide uncertainty estimates or confidence intervals
- Predictions are based on chemical structure only and do not account for biological context, formulation, or individual taste perception variability

## Evidence

- [readme] BitterPredict.m gets as input CSV or EXCEL files with required descriptors of molecules, and calucautes a predictions if each molecule is bitter or not: "gets as input CSV or EXCEL files with required descriptors of molecules, and calucautes a predictions if each molecule is bitter or not"
- [other] BitterPredict is a classifier which predicts whether a compound is bitter or not, based on its chemical structure: "BitterPredict is a classifier which predicts whether a compound is bitter or not, based on its chemical structure"
- [other] Load the input CSV or EXCEL file containing molecular descriptors using appropriate file I/O (pandas or equivalent). Pass the descriptor table to the BitterPredict.m classifier. Generate binary predictions (bitter/not bitter) for each molecule. Compile predictions into a structured output file with molecule identifiers and predicted class labels.: "Load the input CSV or EXCEL file containing molecular descriptors using appropriate file I/O (pandas or equivalent). Pass the descriptor table to the BitterPredict.m classifier. Generate binary"
- [readme] Details and examples of how to use the code is avalibale inside bitterPredict.m file: "Details and examples of how to use the code is avalibale inside bitterPredict.m file"
