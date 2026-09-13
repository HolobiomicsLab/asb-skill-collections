---
name: mass-spectrometry-ion-formula-assignment
description: Use when when you have a metabolite structure (SMILES or molecular graph)
  and need to predict its ionization behavior in a mass spectrometry experiment using
  a specific derivatizing matrix or ionization mode. Use this skill when the expected
  ions are non-standard (i.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - RDKit
  - Met-ID
  techniques:
  - MS-imaging
  license_tier: open
  provenance_tier: literature
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

# mass-spectrometry-ion-formula-assignment

## Summary

Automated prediction and enumeration of expected adduct ion formulas and m/z values for metabolites in mass spectrometry imaging, with support for derivatizing matrices (e.g. FMP-10) that produce non-standard ionization patterns. This skill replaces manual expert-driven ion assignment in high-throughput MS workflows.

## When to use

When you have a metabolite structure (SMILES or molecular graph) and need to predict its ionization behavior in a mass spectrometry experiment using a specific derivatizing matrix or ionization mode. Use this skill when the expected ions are non-standard (i.e., not just [M+H]+ in positive mode or [M-H]- in negative mode) and you need to enumerate all plausible adduct forms for database matching or MS/MS validation.

## When NOT to use

- Input metabolite structure is unknown or unvalidated (use de novo structure elucidation first).
- You are working with a standard ionization mode ([M+H]+, [M-H]-) and no derivatizing matrix is used (simpler, non-extensible tools may suffice).
- The derivatizing matrix used in the experiment is not defined or its adduct ruleset is unavailable.

## Inputs

- metabolite SMILES string
- derivatizing matrix identifier (e.g., 'FMP-10')
- ionization mode (positive or negative)
- matrix-specific adduct ruleset or reference data file

## Outputs

- table of predicted adduct ions with formula, mass shift, and m/z
- list of expected [M+adduct]±n ion species
- comparison/validation report against reference adduct masses

## How to apply

Parse the input metabolite SMILES string using RDKit to construct a validated molecular graph and extract the neutral molecular weight. Load or query the matrix-specific adduct ionization ruleset corresponding to your derivatizing matrix (e.g., FMP-10 reference patterns from Nature Methods). For each adduct rule in the matrix profile, calculate the expected m/z by applying RDKit molecular weight computation accounting for the derivatizing matrix modification mass and ionization state (charge and electron mass shifts). Return a table listing all predicted adduct ions with their chemical formulas, mass shifts (Δm), and m/z values. Validate results by comparing against reference adduct masses from published datasets (e.g., FMP-10 masses from Nature Methods) to ensure matrix-specific rules were correctly applied.

## Related tools

- **RDKit** (Parses metabolite SMILES, constructs molecular graph, validates structure, and computes molecular weights for m/z calculations) — https://www.rdkit.org/
- **Met-ID** (Integrated software platform for automated metabolite identification in mass spectrometry imaging; implements adduct ion enumeration for derivatizing matrices including FMP-10) — https://github.com/pbjarterot/Met-ID

## Evaluation signals

- All predicted adduct m/z values match or fall within expected mass tolerance (e.g., <5 ppm) of reference FMP-10 adduct masses from Nature Methods dataset.
- Predicted adduct formulas are chemically valid (charge state consistent with ionization mode, mass shift is positive and sensible for the matrix).
- Number and distribution of predicted adducts is consistent with known ionization behavior of the matrix (e.g., FMP-10 produces specific characteristic adducts in documented order of abundance).
- Table schema includes all required fields: ion formula, mass shift (Δm), m/z, charge state, and matrix modification label.
- Neutral molecular weight computed by RDKit from input SMILES is reproducible across runs and matches literature values for known standards.

## Limitations

- Ruleset accuracy depends on completeness of the input matrix-specific adduct profile; incomplete or incorrect rules will produce spurious predictions.
- RDKit's SMILES parsing requires structurally valid input; malformed SMILES or rare structural motifs (strained rings, unusual valence) may fail validation.
- The skill predicts theoretical m/z values under ideal conditions; actual observed ions may be suppressed, enhanced, or absent due to ionization efficiency, in-source fragmentation, or matrix effects not accounted for in the ruleset.
- Software is under active development; database files may require manual reset and reinstallation when upgrading versions.

## Evidence

- [intro] Met-ID is designed to handle derivatizing matrices such as FMP-10, which produce ions other than the common [M+H]+ in positive mode and [M-H]- in negative mode: "Met-ID has a particular focus on derivatizing matrices leading to other ions than the common [M+H]+ in positive mode and [M-H]- in negative mode"
- [other] The workflow parses metabolite SMILES using RDKit, loads matrix-specific adduct rules, applies molecular weight calculations to compute m/z for each adduct, and compares against reference data: "Parse input metabolite SMILES and matrix identifier using RDKit to construct the molecular graph and validate structure. Query or load the matrix-specific adduct ionization ruleset (e.g., FMP-10"
- [readme] Met-ID automates metabolite identification because manual expert-driven ion assignment is not feasible in high-throughput studies: "Met-ID has been developed to automate metabolite identification in Mass Spectrometry Imaging, at the moment most of this is done manually by experts which in the world of high throughput studies is"
- [readme] Met-ID is extensible to use any derivatizing matrix, with built-in support for FMP-10 as a reference example: "Met-ID is extendable to use any derivatizing matrix with the tools to do local version changes right from inside the software"
