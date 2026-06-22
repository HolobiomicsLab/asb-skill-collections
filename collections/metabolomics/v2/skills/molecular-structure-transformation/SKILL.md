---
name: molecular-structure-transformation
description: Use when when you have native metabolite structures (SMILES or mol format) and need to predict adduct ions for a mass spectrometry imaging experiment that uses a derivatizing matrix known to produce ions other than common [M+H]+ (positive mode) or [M-H]- (negative mode).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0335
  edam_topics:
  - http://edamontology.org/topic_0154
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

# molecular-structure-transformation

## Summary

Apply chemical derivatization reactions to metabolite structures to enumerate non-standard adduct ions characteristic of specific derivatizing matrices (e.g., FMP-10). This skill transforms native SMILES/mol structures into derivatized products and predicts their mass-to-charge ratios for mass spectrometry metabolite identification.

## When to use

When you have native metabolite structures (SMILES or mol format) and need to predict adduct ions for a mass spectrometry imaging experiment that uses a derivatizing matrix known to produce ions other than common [M+H]+ (positive mode) or [M-H]- (negative mode). Apply this skill before matching experimental m/z values to a metabolite library in high-throughput MS imaging workflows where manual expert annotation is infeasible.

## When NOT to use

- Input metabolites are already derivatized or adduct masses are already experimentally measured—direct spectral matching is more efficient.
- Derivatizing matrix and its reaction scheme are unknown or unavailable—the skill requires explicit chemistry rules to enumerate correct adducts.
- Analysis requires only common [M+H]+ and [M-H]- adducts without matrix-specific ions—standard mass difference lookup is faster and does not require RDKit.

## Inputs

- metabolite structures in SMILES or mol format
- derivatizing matrix type identifier (e.g., 'FMP-10')
- derivatization reaction scheme rules (SMARTS or RDKit-executable reaction SMILES)

## Outputs

- enumerated adduct ion list with m/z values, charge states, and ion type annotations
- derivatized metabolite structures (mol or SMILES)
- molecular weight of derivatized product

## How to apply

Parse input metabolite structures (SMILES or mol format) using RDKit. Load the derivatization chemistry rules (reaction scheme) for your derivatizing matrix—for FMP-10, this includes the in-house-developed transformation rules. Apply the derivatization reaction to each metabolite using RDKit chemistry operations, computing the molecular weight of the derivatized product. Enumerate derivatization-specific adduct ions (e.g., [M+derivatization_tag]+, [M+Na]+, [M+K]+, or matrix-specific ions) and calculate their m/z values. Output the adduct ion list with m/z, charge state, and ion type annotation for library matching.

## Related tools

- **RDKit** (Parse metabolite structures from SMILES/mol format, apply derivatization transformations, and compute molecular weights and m/z values) — https://www.rdkit.org/
- **Met-ID** (End-to-end metabolite identification workflow in mass spectrometry imaging that integrates this transformation skill with MS2 spectral comparison and derivatizing matrix support) — https://github.com/pbjarterot/Met-ID

## Evaluation signals

- Derived m/z values match experimental peaks in mass spectrometry imaging data for known metabolite standards.
- Enumerated adduct ion list contains at least one entry per metabolite and distinguishes matrix-specific ions from common [M+H]+ / [M-H]- adducts.
- Molecular weight of derivatized product is greater than native metabolite weight by the expected derivatization tag mass.
- Output adduct annotations (e.g., '[M+FMP-10]+') are consistent with the input derivatizing matrix type and its published chemistry.
- No structural transformations produce chemically invalid or duplicate adduct ions (e.g., contradictory charge states for the same m/z).

## Limitations

- Requires explicit, validated derivatization chemistry rules for each matrix; extensibility depends on accurate SMARTS/reaction SMILES specifications.
- RDKit structure parsing may fail or produce unexpected results on highly complex or non-standard SMILES notations; validation of input structures is necessary.
- Met-ID database files require manual removal and reinstallation on version updates (noted in README) and currently has known functional group addition issues on macOS.
- Enumeration does not account for in-source fragmentation, thermal decomposition, or ion suppression effects that may suppress or enhance certain adducts in real MS data.

## Evidence

- [readme] Met-ID has a particular focus on derivatizing matrices leading to other ions than the common [M+H]+ in positive mode and [M-H]- in negative mode: "Met-ID has a particular focus on derivatizing matrices leading to other ions than the common [M+H]+ in positive mode and [M-H]- in negative mode"
- [other] Parse input metabolite structures, load derivatization chemistry rules, apply transformations, enumerate adducts, and output m/z with annotation: "Parse input metabolite structures (SMILES or mol format) using RDKit. 2. Identify the derivatizing matrix type and load its derivatization chemistry rules (e.g., FMP-10 reaction scheme). 3. Apply"
- [readme] FMP-10 derivatizing matrix was developed in-house and features heavily in Met-ID: "As [FMP-10] was developed in house, it features heavily in the software"
- [readme] Met-ID is extendable to use any derivatizing matrix with tools for local version changes: "Met-ID is extendable to use any derivatizing matrix with the tools to do local version changes right from inside the software"
- [readme] Metabolite identification in Mass Spectrometry Imaging is mostly done manually by experts, which is not feasible in high throughput studies: "most of this is done manually by experts which in the world of high throughput studies is not feasable"
