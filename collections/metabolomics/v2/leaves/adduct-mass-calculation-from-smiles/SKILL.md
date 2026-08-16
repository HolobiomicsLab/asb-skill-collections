---
name: adduct-mass-calculation-from-smiles
description: Use when when you have a metabolite SMILES structure and need to predict
  which adduct ions will appear in a mass spectrum acquired with a chemical derivatizing
  matrix.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - RDKit
  - Met-ID
  techniques:
  - MS-imaging
  license_tier: open
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

# adduct-mass-calculation-from-smiles

## Summary

Compute expected m/z values for metabolite adduct ions given a SMILES string and a derivatizing matrix profile (e.g., FMP-10). This skill automates the prediction of non-standard ionization products beyond [M+H]+ and [M-H]−, enabling high-throughput metabolite identification in mass spectrometry imaging.

## When to use

When you have a metabolite SMILES structure and need to predict which adduct ions will appear in a mass spectrum acquired with a chemical derivatizing matrix. Use this skill especially when the derivatizing matrix produces ions other than common [M+H]+ in positive mode or [M-H]− in negative mode, such as with FMP-10 or other custom matrices. Apply it during the feature-to-compound matching stage of metabolite identification in mass spectrometry imaging workflows.

## When NOT to use

- Input metabolite structure is already fragmented or is an MS/MS product ion rather than an intact molecule—use MS/MS spectral matching instead.
- The derivatizing matrix is not characterized or no adduct ruleset is available; attempting to guess the matrix profile will produce incorrect predictions.
- You are working with raw mass spectrometry imaging data and need to identify all peaks simultaneously; use this skill as part of a larger feature-matching pipeline, not in isolation.

## Inputs

- metabolite SMILES string
- derivatizing matrix identifier or ruleset (e.g., 'FMP-10' or custom matrix configuration)
- optional: ionization mode ('positive' or 'negative')

## Outputs

- table of predicted adduct ions with formula, mass shift (Δm), and expected m/z values
- ranked list of expected m/z values for the metabolite under the specified matrix conditions

## How to apply

Parse the input metabolite SMILES string using RDKit to construct and validate the molecular graph structure. Load the matrix-specific adduct ionization ruleset—either from built-in reference data (e.g., FMP-10 Nature Methods profiles) or from a user-defined matrix configuration. For each adduct rule in the matrix profile, apply RDKit's molecular weight calculator to compute the expected m/z by accounting for the derivatizing matrix modification mass, the adduct formula (e.g., +H, +Na, +NH4), and the resulting ionization charge state. Return a ranked table of predicted adduct m/z values with their corresponding formulas and mass shifts. Validate the outputs by comparing against reference adduct masses from published datasets or experimental standards to confirm the matrix-specific modifications are correctly applied.

## Related tools

- **RDKit** (molecular graph construction, structure validation, and molecular weight calculation from SMILES) — https://www.rdkit.org/
- **Met-ID** (complete metabolite identification framework integrating adduct mass prediction with MS/MS spectral matching and derivatizing matrix support) — https://github.com/pbjarterot/Met-ID

## Evaluation signals

- Predicted m/z values match reference adduct masses from published FMP-10 or derivatizing matrix datasets within the expected mass tolerance (e.g., <5 ppm for high-resolution instruments).
- All expected adduct ions for the matrix are represented in the output table (no missing adducts for the given ionization mode).
- Molecular weight calculation is internally consistent: computed m/z for each adduct obeys (molecular_weight + matrix_modification + adduct_mass) / charge_state.
- SMILES parsing completes without errors and produces a valid molecular graph; invalid or malformed SMILES are rejected with clear error messages.
- Output can be directly compared to observed mass spectrometry peaks and shows reasonable agreement in rank order and spacing, validating the matrix ruleset application.

## Limitations

- The skill requires a pre-defined or user-provided matrix ruleset; without accurate adduct ionization rules for the derivatizing matrix, predictions will be incorrect.
- Metabolite structural ambiguity from SMILES (e.g., stereoisomers, tautomers) does not affect m/z calculation but may complicate downstream compound identification.
- The skill predicts only the primary and common secondary adducts; multiply-charged ions, dimers, or rare fragmentation adducts are not automatically enumerated.
- Matrix-specific behavior such as salt adducts ([M+Na]+, [M+K]+) must be explicitly included in the matrix ruleset; default ionization rules may not capture all in-source modifications.
- Derivatizing matrix modification masses and adduct rules must be kept current; outdated or incorrect ruleset definitions lead to systematic prediction errors across all metabolites.

## Evidence

- [readme] Met-ID has a particular focus on derivatizing matrices leading to other ions than the common [M+H]+ in positive mode and [M-H]- in negative mode: "Met-ID has a particular focus on derivatizing matrices leading to other ions than the common [M+H]+ in positive mode and [M-H]- in negative mode"
- [other] Parse input metabolite SMILES and matrix identifier using RDKit to construct the molecular graph and validate structure: "Parse input metabolite SMILES and matrix identifier using RDKit to construct the molecular graph and validate structure"
- [other] For each adduct rule in the matrix profile, apply RDKit molecular weight calculation to compute the expected m/z accounting for the derivatizing matrix modification and ionization state: "For each adduct rule in the matrix profile, apply RDKit molecular weight calculation to compute the expected m/z accounting for the derivatizing matrix modification and ionization state"
- [other] Return a table of predicted adduct ions with their formulas, mass shifts, and expected m/z values, and compare against reference FMP-10 adduct masses from the published Nature Methods dataset: "Return a table of predicted adduct ions with their formulas, mass shifts, and expected m/z values, and compare against reference FMP-10 adduct masses"
- [readme] Met-ID is extendable to use any derivatizing matrix with the tools to do local version changes right from inside the software: "Met-ID is extendable to use any derivatizing matrix with the tools to do local version changes right from inside the software"
