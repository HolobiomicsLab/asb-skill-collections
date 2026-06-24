---
name: molecular-weight-prediction-with-modifications
description: Use when when you have metabolite structures (as SMILES strings) and
  need to predict their observable m/z ions under non-standard ionization conditions
  imposed by a derivatizing matrix reagent (such as FMP-10).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - RDKit
  - Met-ID
  techniques:
  - MS-imaging
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.5c00633
  title: metid
evidence_spans:
- Powered by RDKit
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metid
    doi: 10.1021/acs.analchem.5c00633
    title: metid
  dedup_kept_from: coll_metid
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c00633
  all_source_dois:
  - 10.1021/acs.analchem.5c00633
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# molecular-weight-prediction-with-modifications

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Compute expected m/z values for metabolites undergoing derivatizing matrix modifications (e.g., FMP-10) that produce ions beyond standard [M+H]+ and [M-H]− adducts. This skill automates the prediction of multiple ion species for a single metabolite, enabling high-throughput metabolite identification in mass spectrometry imaging.

## When to use

When you have metabolite structures (as SMILES strings) and need to predict their observable m/z ions under non-standard ionization conditions imposed by a derivatizing matrix reagent (such as FMP-10). Use this skill when manual ion enumeration is infeasible for high-throughput studies or when the ionization pattern deviates from common positive-mode [M+H]+ or negative-mode [M-H]− ions.

## When NOT to use

- Input metabolites are already ionized or in m/z space—this skill requires neutral molecular structures as SMILES strings.
- The derivatizing matrix is standard (e.g., ESI producing only [M+H]+ / [M-H]−) with no custom adduct rules—standard ionization prediction suffices.
- Output is required in real time for single-metabolite queries where pre-computed reference libraries are sufficient.

## Inputs

- Metabolite SMILES string
- Derivatizing matrix identifier (e.g., 'FMP-10')
- Matrix-specific adduct ionization ruleset (JSON or structured format)

## Outputs

- Table of predicted adduct ions (columns: formula, adduct type, mass shift, m/z value)
- Annotated list of expected ions with ionization states

## How to apply

Parse the input metabolite SMILES using RDKit to construct and validate the molecular graph. Load the matrix-specific adduct ionization ruleset corresponding to the derivatizing agent (e.g., FMP-10 adduct patterns from Nature Methods reference data). For each adduct rule in the matrix profile, apply RDKit's molecular weight calculation to compute the expected m/z by accounting for the derivatizing matrix modification and ionization state. Return a table of predicted adduct ions with their chemical formulas, mass shifts, and expected m/z values. Validate predictions by comparing against published reference adduct masses (e.g., FMP-10 dataset from Nature Methods) to confirm that the modification pattern and mass accuracy are correct.

## Related tools

- **RDKit** (Parse SMILES strings, construct molecular graphs, compute molecular weights, and apply mass modifications to enumerate adduct ions) — https://www.rdkit.org/
- **Met-ID** (Host software integrating this skill for automated metabolite identification in mass spectrometry imaging with extensible matrix support) — https://github.com/pbjarterot/Met-ID

## Evaluation signals

- Predicted m/z values match published reference adduct masses from the Nature Methods FMP-10 dataset within expected instrumental accuracy (e.g., <5 ppm on high-resolution instruments).
- All expected adduct ions for a given matrix are enumerated (no missing ion types in the ruleset).
- Mass shifts (difference between predicted and neutral molecular mass) conform to the derivatizing matrix's known modification formula.
- Output table is complete and non-empty for valid metabolite SMILES inputs; error handling gracefully reports invalid or unparseable SMILES.
- Comparison of predicted adducts against experimentally observed m/z peaks in MS data shows high recall and minimal false positives.

## Limitations

- Requires a pre-defined, validated adduct ionization ruleset for each derivatizing matrix; prediction accuracy depends on ruleset completeness and accuracy.
- RDKit molecular weight calculation assumes standard isotopic composition; prediction does not account for isotopologues or non-standard labeling.
- Matrix-specific side reactions or secondary modifications not explicitly captured in the ruleset will not be predicted.
- SMILES input must be valid and represent a neutral structure; salts, protonation states, or complex counterions in the SMILES may lead to incorrect mass predictions.

## Evidence

- [other] Met-ID is designed to handle derivatizing matrices such as FMP-10, which produce ions other than the common [M+H]+ in positive mode and [M-H]- in negative mode: "Met-ID is designed to handle derivatizing matrices such as FMP-10, which produce ions other than the common [M+H]+ in positive mode and [M-H]- in negative mode"
- [other] Parse input metabolite SMILES and matrix identifier using RDKit to construct the molecular graph and validate structure. Query or load the matrix-specific adduct ionization ruleset. For each adduct rule in the matrix profile, apply RDKit molecular weight calculation to compute the expected m/z accounting for the derivatizing matrix modification and ionization state.: "Parse input metabolite SMILES and matrix identifier using RDKit to construct the molecular graph and validate structure. Query or load the matrix-specific adduct ionization ruleset (e.g., FMP-10"
- [other] Return a table of predicted adduct ions with their formulas, mass shifts, and expected m/z values, and compare against reference FMP-10 adduct masses from the published Nature Methods dataset.: "Return a table of predicted adduct ions with their formulas, mass shifts, and expected m/z values, and compare against reference FMP-10 adduct masses from the published Nature Methods dataset."
- [readme] As [FMP-10] was developed in house, it features heavily in the software, however, this is mostly to show the point at which to start as Met-ID is extendable to use any derivatizing matrix: "Met-ID is extendable to use any derivatizing matrix with the tools to do local version changes right from inside the software."
