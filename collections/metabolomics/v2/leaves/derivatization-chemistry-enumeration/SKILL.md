---
name: derivatization-chemistry-enumeration
description: Use when when performing metabolite identification in mass spectrometry
  imaging and the metabolites have been chemically derivatized with a known derivatizing
  matrix (such as FMP-10) that produces ions other than the standard [M+H]+ in positive
  mode or [M-H]− in negative mode.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
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
- '[![Powered by RDKit]'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metid_cq
    doi: 10.1021/acs.analchem.5c00633
    title: metid
  dedup_kept_from: coll_metid_cq
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

# derivatization-chemistry-enumeration

## Summary

Enumerate adduct ions produced by chemical derivatization matrices (e.g., FMP-10) applied to metabolites, extending beyond common [M+H]+ and [M-H]− ions to capture matrix-specific ionization products. This skill automates the generation of expected m/z values for metabolite identification in mass spectrometry imaging workflows.

## When to use

When performing metabolite identification in mass spectrometry imaging and the metabolites have been chemically derivatized with a known derivatizing matrix (such as FMP-10) that produces ions other than the standard [M+H]+ in positive mode or [M-H]− in negative mode. Use this skill to generate the complete set of expected adduct ion m/z values for database matching or feature annotation.

## When NOT to use

- Input metabolites are not chemically derivatized or expected to remain in their native form.
- The derivatizing matrix used is not defined or its reaction scheme is not available in the software.
- Only standard [M+H]+ and [M-H]− adducts are expected; matrix-specific ionization is not relevant to the analysis.

## Inputs

- metabolite structures (SMILES or mol format)
- derivatizing matrix type identifier (e.g., 'FMP-10')
- derivatization chemistry rules / reaction scheme (matrix-specific)

## Outputs

- adduct ion list (m/z, charge, ion type annotation)
- derivatized metabolite structure

## How to apply

Parse input metabolite structures (SMILES or mol format) using RDKit. Load the derivatization chemistry rules for the target matrix (e.g., FMP-10 reaction scheme). Apply the derivatization transformation to each metabolite structure using RDKit chemistry operations to compute the derivatized product structure. Calculate the molecular weight of the derivatized product. Enumerate all derivatization-specific adduct ions (e.g., [M+derivatization_tag]+, [M+Na]+, [M+K]+, and any matrix-specific ions documented in the derivatization scheme) and compute their m/z values. Output a structured list of adduct ions with m/z, charge state, and ion type annotation for downstream matching against experimental imaging MS data.

## Related tools

- **RDKit** (Parse metabolite structures (SMILES/mol), apply derivatization transformations, and calculate molecular weights and m/z values) — https://www.rdkit.org/
- **Met-ID** (Complete software platform for metabolite identification in mass spectrometry imaging with built-in FMP-10 derivatization chemistry rules and adduct enumeration) — https://github.com/pbjarterot/Met-ID

## Evaluation signals

- All enumerated adduct ions have valid, non-negative m/z values consistent with the derivatized molecular weight and specified charge states.
- Ion type annotations match the derivatization scheme (e.g., FMP-10-specific ions are correctly labeled and distinguished from common adducts).
- Derivatized structures retain chemical validity (verified by RDKit) and differ from input structures by the expected derivatization chemistry.
- Output adduct list is exhaustive with respect to the documented derivatization scheme; no expected ion types are missing.
- m/z values for identical ion types across multiple metabolites scale correctly with molecular weight differences.

## Limitations

- Software is currently under development with platform-specific issues; macOS has reported functional group addition problems.
- Extensibility to new derivatizing matrices requires local modification of derivatization chemistry rule files; no user-friendly interface yet confirmed in README for adding custom matrices.
- Met-ID is designed specifically for derivatized matrices; applicability to non-derivatized metabolite adduct enumeration or novel matrices not yet tested in-house is unclear.
- Database files must be manually removed and Met-ID reinstalled when updating to newer versions to ensure derivatization rules are properly updated.

## Evidence

- [readme] Met-ID has a particular focus on derivatizing matrices leading to other ions than the common [M+H]+ in positive mode and [M-H]− in negative mode: "Met-ID has a particular focus on derivatizing matrices leading to other ions than the common [M+H]+ in positive mode and [M-H]− in negative mode"
- [readme] As [FMP-10] was developed in house, it features heavily in the software: "As [FMP-10] was developed in house, it features heavily in the software"
- [other] Identify the derivatizing matrix type and load its derivatization chemistry rules (e.g., FMP-10 reaction scheme). Apply derivatization transformation to each metabolite structure using RDKit chemistry operations.: "Identify the derivatizing matrix type and load its derivatization chemistry rules (e.g., FMP-10 reaction scheme). Apply derivatization transformation to each metabolite structure using RDKit"
- [other] Enumerate derivatization-specific adduct ions (e.g., [M+derivatization_tag]+, [M+Na]+, [M+K]+, or matrix-specific ions) and calculate their m/z values: "Enumerate derivatization-specific adduct ions (e.g., [M+derivatization_tag]+, [M+Na]+, [M+K]+, or matrix-specific ions) and calculate their m/z values"
- [readme] Met-ID is extendable to use any derivatizing matrix with the tools to do local version changes right from inside the software: "Met-ID is extendable to use any derivatizing matrix with the tools to do local version changes right from inside the software"
