---
name: derivatizing-matrix-ionization-rule-application
description: Use when when working with mass spectrometry imaging data from metabolites
  treated with derivatizing matrices (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3800
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - RDKit
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

# derivatizing-matrix-ionization-rule-application

## Summary

Apply matrix-specific adduct ionization rulesets to predict non-standard ion forms (beyond [M+H]+ and [M-H]-) that arise from derivatizing matrices like FMP-10 in mass spectrometry metabolite identification. This skill is essential for correctly identifying metabolites when chemical derivatization alters the ionization behavior in MSI experiments.

## When to use

When working with mass spectrometry imaging data from metabolites treated with derivatizing matrices (e.g., FMP-10) that produce adduct ions beyond the common [M+H]+ in positive mode and [M-H]- in negative mode, and you need to enumerate and validate predicted m/z values for metabolite annotation.

## When NOT to use

- Input metabolites are not chemically derivatized or are analyzed under standard ionization conditions ([M+H]+, [M-H]- only).
- Matrix-specific adduct ruleset is unknown or unavailable for the derivatizing matrix being used.
- Input SMILES cannot be parsed or validated as a valid molecular structure by RDKit.

## Inputs

- Metabolite SMILES string
- Derivatizing matrix identifier (e.g., 'FMP-10')
- Matrix-specific adduct ruleset (lookup table or configuration file mapping ionization rules to mass shifts)

## Outputs

- Adduct ion prediction table (columns: adduct formula, mass shift, predicted m/z, ionization mode)
- Validated adduct ion list (filtered against reference matrix characterization data)

## How to apply

Parse the input metabolite structure as SMILES and identify the derivatizing matrix identifier (e.g., FMP-10). Load the matrix-specific adduct ionization ruleset (which maps derivatizing matrix modifications and ionization states to mass shifts). For each adduct rule, use RDKit to calculate molecular weight and apply the matrix-specific mass modification to compute expected m/z. Generate a table of predicted adduct ions with formulas, mass shifts, and m/z values. Compare the predicted m/z against reference data from published matrix characterization studies (e.g., Nature Methods FMP-10 dataset) to validate rule accuracy and filter false positives based on literature-reported adduct patterns.

## Related tools

- **RDKit** (Parse metabolite SMILES, construct molecular graphs, validate structures, and compute molecular weights for m/z prediction) — https://www.rdkit.org/

## Evaluation signals

- Predicted m/z values for all enumerated adducts fall within expected tolerance of reference matrix characterization data (e.g., FMP-10 Nature Methods dataset).
- Adduct formulas and mass shifts are consistent with known ionization chemistry for the specified derivatizing matrix.
- No RDKit parsing or validation errors on input SMILES; molecular structure graph is chemically valid.
- All adduct m/z predictions are sorted and indexed consistently; table schema includes required columns (formula, mass shift, m/z, mode).
- Comparison output indicates agreement or discrepancy with literature reference values, flagging novel or unexpected adducts for manual review.

## Limitations

- Skill is dependent on the availability and accuracy of the matrix-specific adduct ruleset; if the ruleset is incomplete or derived from limited reference data, predictions may be incomplete or incorrect.
- RDKit molecular weight calculations assume standard atomic masses and do not account for isotopic variants; isotopic fine-structure predictions are not supported.
- The skill assumes the input SMILES is chemically realistic and non-ambiguous; highly complex or ambiguously drawn structures may fail RDKit validation.
- Mat-ID is extendable to any derivatizing matrix in principle, but as of the README publication, FMP-10 is the primary validated use case; other matrices require manual ruleset development and validation.

## Evidence

- [other] Parse input metabolite SMILES and matrix identifier using RDKit to construct the molecular graph and validate structure.: "Parse input metabolite SMILES and matrix identifier using RDKit to construct the molecular graph and validate structure."
- [other] Query or load the matrix-specific adduct ionization ruleset (e.g., FMP-10 adduct patterns from Nature Methods reference data).: "Query or load the matrix-specific adduct ionization ruleset (e.g., FMP-10 adduct patterns from Nature Methods reference data)."
- [other] For each adduct rule in the matrix profile, apply RDKit molecular weight calculation to compute the expected m/z accounting for the derivatizing matrix modification and ionization state.: "For each adduct rule in the matrix profile, apply RDKit molecular weight calculation to compute the expected m/z accounting for the derivatizing matrix modification and ionization state."
- [readme] Met-ID has a particular focus on derivatizing matrices leading to other ions than the common [M+H]+ in positive mode and [M-H]- in negative mode.: "Met-ID has a particular focus on derivatizing matrices leading to other ions than the common [M+H]+ in positive mode and [M-H]- in negative mode."
- [readme] Met-ID is extendable to use any derivatizing matrix with the tools to do local version changes right from inside the software.: "Met-ID is extendable to use any derivatizing matrix with the tools to do local version changes right from inside the software."
