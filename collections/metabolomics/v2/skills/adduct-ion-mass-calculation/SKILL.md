---
name: adduct-ion-mass-calculation
description: Use when when you have derivatized metabolite structures (SMILES or mol format) and need to predict their ionization products in MS imaging, particularly when the derivatizing matrix produces non-standard adducts (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - RDKit
  - Met-ID
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# adduct-ion-mass-calculation

## Summary

Calculate m/z values for derivatized metabolite adduct ions beyond common [M+H]+ and [M-H]- forms, with explicit support for matrix-specific ions like those produced by FMP-10 derivatizing agents. This skill automates adduct enumeration for high-throughput metabolite identification in mass spectrometry imaging.

## When to use

When you have derivatized metabolite structures (SMILES or mol format) and need to predict their ionization products in MS imaging, particularly when the derivatizing matrix produces non-standard adducts (e.g., FMP-10-tagged ions, [M+Na]+, [M+K]+, or matrix-specific ion forms) rather than the common [M+H]+ and [M-H]- ions. Use this skill to generate a searchable list of expected m/z values for spectral matching and compound identification.

## When NOT to use

- Input metabolites are not derivatized; use standard adduct enumeration for underivatized compounds ([M+H]+, [M-H]-, etc.).
- Derivatizing matrix chemistry rules are not defined or unknown; this skill requires explicit reaction scheme input.
- You are analyzing raw MS spectra directly; this skill produces expected m/z predictions and must be paired with spectral matching or peak detection downstream.

## Inputs

- metabolite structures in SMILES or mol file format
- derivatizing matrix chemistry rules (reaction scheme definition)
- metabolite molecular weights (computed from input structures)

## Outputs

- adduct ion enumeration list with m/z values
- ion type annotations (e.g., [M+H]+, [M+Na]+, [M+FMP-10]+)
- charge state assignments for each adduct

## How to apply

Parse input metabolite structures using RDKit to obtain molecular graphs. Load the derivatizing matrix chemistry rules (e.g., FMP-10 reaction scheme) and apply the derivatization transformation to each metabolite structure using RDKit chemistry operations. Compute the molecular weight of the derivatized product. Enumerate matrix-specific adduct forms (including [M+derivatization_tag]+, [M+Na]+, [M+K]+, and any other known ionization products for that matrix) and calculate their m/z values by dividing the mass by charge state. Annotate each adduct ion with its type, calculated m/z, and charge state. Output the adduct ion list for use in spectral library matching and metabolite annotation workflows.

## Related tools

- **RDKit** (Parse metabolite structures, apply derivatization transformations, and compute molecular weights of derivatized products) — https://www.rdkit.org/
- **Met-ID** (Software platform that integrates adduct ion enumeration for FMP-10 derivatized metabolites with MS2 spectral matching for automated metabolite identification in mass spectrometry imaging) — https://github.com/pbjarterot/Met-ID

## Evaluation signals

- All enumerated m/z values are numeric, positive, and within the expected instrument range (typically 50–2000 m/z for small-molecule metabolomics).
- Charge states match the ionization mode (e.g., +1 for positive-mode adducts, −1 for negative-mode); no mixed charges in a single adduct list.
- Adduct ion annotations include the matrix-specific tag or derivatization marker (e.g., 'FMP-10' appears in ion type labels for matrix-specific ions).
- m/z values differ consistently between adduct types (e.g., [M+Na]+ is ~22 Da higher than [M+H]+ after derivatization); monotonic spacing validates mass shift logic.
- Enumerated adducts match observed peaks in authentic MS spectra when compared to standards with known FMP-10 derivatization.

## Limitations

- Derivatization chemistry rules must be manually defined or loaded from a curated database; incorrect or incomplete reaction schemes will produce incorrect adduct predictions.
- FMP-10 is the primary implemented matrix in Met-ID; extensibility to other derivatizing matrices requires local version changes and manual chemistry rule entry.
- The skill does not account for in-source fragmentation, neutral loss, or multimeric adducts; it assumes a single intact derivatized molecule ionizes to a single adduct.
- macOS has known functional group addition issues in Met-ID (documented in README), which may affect derivatization rule application on that platform.

## Evidence

- [readme] Met-ID has a particular focus on derivatizing matrices leading to other ions than the common [M+H]+ in positive mode and [M-H]- in negative mode: "Met-ID has a particular focus on derivatizing matrices leading to other ions than the common [M+H]+ in positive mode and [M-H]- in negative mode"
- [other] Apply derivatization transformation to each metabolite structure using RDKit chemistry operations. Compute molecular weight of derivatized product. Enumerate derivatization-specific adduct ions (e.g., [M+derivatization_tag]+, [M+Na]+, [M+K]+, or matrix-specific ions) and calculate their m/z values.: "Apply derivatization transformation to each metabolite structure using RDKit chemistry operations. Compute molecular weight of derivatized product. Enumerate derivatization-specific adduct ions"
- [readme] As [FMP-10] was developed in house, it features heavily in the software, however, this is mostly to show the point at which to start as Met-ID is extendable to use any derivatizing matrix: "As [FMP-10] was developed in house, it features heavily in the software, however, this is mostly to show the point at which to start as Met-ID is extendable to use any derivatizing matrix"
- [other] Parse input metabolite structures (SMILES or mol format) using RDKit. Identify the derivatizing matrix type and load its derivatization chemistry rules: "Parse input metabolite structures (SMILES or mol format) using RDKit. Identify the derivatizing matrix type and load its derivatization chemistry rules"
- [other] Output adduct ion list with m/z, charge, and ion type annotation.: "Output adduct ion list with m/z, charge, and ion type annotation"
