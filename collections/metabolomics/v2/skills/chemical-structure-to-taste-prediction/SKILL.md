---
name: chemical-structure-to-taste-prediction
description: Use when you have a CSV or EXCEL file containing molecular descriptors (pre-computed structural features) for one or more chemical compounds, and you need binary bitterness predictions (bitter vs. non-bitter) for each molecule.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0209
  - http://edamontology.org/topic_3314
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

# chemical-structure-to-taste-prediction

## Summary

BitterPredict is a binary classification skill that predicts whether a chemical compound will taste bitter based on its molecular structure, encoded as a set of computed molecular descriptors. Use this skill to rapidly screen chemical libraries or predict bitterness of novel compounds without requiring direct sensory evaluation.

## When to use

You have a CSV or EXCEL file containing molecular descriptors (pre-computed structural features) for one or more chemical compounds, and you need binary bitterness predictions (bitter vs. non-bitter) for each molecule. This skill is appropriate when molecular structure is the primary information available and you seek to avoid costly or time-consuming gustatory assays.

## When NOT to use

- Input is raw chemical structure data (SMILES, MOL, or PDB) rather than pre-computed molecular descriptors—descriptors must be calculated separately first.
- You require confidence scores, probabilities, or uncertainty quantification rather than hard binary predictions.
- The set of required molecular descriptors for the input molecules is unknown or differs from BitterPredict.m's expected feature set.

## Inputs

- CSV file with molecular descriptors
- EXCEL file with molecular descriptors
- Table of molecules with computed structural features and identifiers

## Outputs

- Binary predictions (bitter / not bitter) per molecule
- Structured output file with molecule identifiers and predicted class labels

## How to apply

Load your input CSV or EXCEL file containing the required molecular descriptors for each molecule using standard file I/O libraries (e.g., pandas in Python or readtable in MATLAB). Pass the descriptor table to the BitterPredict.m classifier, which will compute a binary prediction (bitter or not bitter) for each row. Compile the predictions into a structured output file that associates each molecule identifier with its predicted class label. Verify that the descriptor set matches the features expected by the classifier (as documented in the BitterPredict.m function header) to ensure valid predictions.

## Related tools

- **BitterPredict.m** (Core classifier that accepts descriptor tables and outputs binary bitterness predictions for each molecule.) — https://github.com/Niv-Lab/BitterPredict1

## Evaluation signals

- Output file contains one prediction row per input molecule with correct molecule identifiers.
- All predictions are valid binary labels (bitter or not bitter), with no missing or invalid values.
- Output schema matches expected structure (molecule ID column + prediction class column).
- Descriptor columns used by the classifier are present and non-empty in the input file.
- Processing completes without errors or warnings related to missing or malformed descriptor data.

## Limitations

- Full code is not publicly available until publication; availability may be restricted or incomplete.
- No changelog or version history is documented, limiting reproducibility across time.
- The skill is limited to binary classification and does not provide probability scores or confidence measures.
- Prediction quality depends entirely on the correctness and completeness of the input molecular descriptors.

## Evidence

- [readme] BitterPredict is a classifier which predicts whether a compound is bitter or not, based on its chemical structure.: "BitterPredict is a classifier which predicts whether a compound is bitter or not, based on its chemical structure."
- [readme] BitterPredict.m gets as input CSV or EXCEL files with required descriptors of molecules, and calucautes a predictions if each molecule is bitter or not.: "BitterPredict.m gets as input CSV or EXCEL files with required descriptors of molecules, and calucautes a predictions if each molecule is bitter or not."
- [other] Pass the descriptor table to the BitterPredict.m classifier. 3. Generate binary predictions (bitter/not bitter) for each molecule. 4. Compile predictions into a structured output file with molecule identifiers and predicted class labels.: "Pass the descriptor table to the BitterPredict.m classifier. Generate binary predictions (bitter/not bitter) for each molecule. Compile predictions into a structured output file with molecule"
- [readme] Details and examples of how to use the code is avalibale inside bitterPredict.m file.: "Details and examples of how to use the code is avalibale inside bitterPredict.m file."
