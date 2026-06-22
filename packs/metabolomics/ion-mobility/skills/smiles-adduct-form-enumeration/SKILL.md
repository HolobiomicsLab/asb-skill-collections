---
name: smiles-adduct-form-enumeration
description: Use when when you have SMILES structures of small organic molecules and need to predict CCS values for metabolite annotation in untargeted mass spectrometry workflows. Specifically, apply this skill when the same chemical entity may appear in multiple ionization states (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
  tools:
  - Dimorphite-DL
  - RDKit
  techniques:
  - ion-mobility-MS
derived_from:
- doi: 10.1021/jasms.1c00315
  title: POMICS
evidence_spans:
- 'Dimorphite-DL: For ionization state determination'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pomics_cq
    doi: 10.1021/jasms.1c00315
    title: POMICS
  dedup_kept_from: coll_pomics_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.1c00315
  all_source_dois:
  - 10.1021/jasms.1c00315
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# SMILES Adduct Form Enumeration

## Summary

Enumerate protonated and deprotonated adduct forms of organic molecules from SMILES strings using Dimorphite-DL to predict ionization states. This is essential for downstream collision cross section (CCS) prediction when multiple ion forms may be observed in mass spectrometry.

## When to use

When you have SMILES structures of small organic molecules and need to predict CCS values for metabolite annotation in untargeted mass spectrometry workflows. Specifically, apply this skill when the same chemical entity may appear in multiple ionization states (e.g., [M+H]+, [M-H]−) in the mass spectrometer, and you need to generate and score conformers for each adduct separately.

## When NOT to use

- Your molecules contain elements outside CHNO (e.g., metals, sulfur, halogens) — Dimorphite-DL's neural network was trained primarily on CHNO and does not handle extended periodic table elements reliably.
- You already have experimental mass spectrometry data with measured m/z values — use direct ion pairing instead of enumeration.
- Your workflow requires custom ionization logic not covered by Dimorphite-DL's default rules (e.g., coordination chemistry, radical cations) — you may need manual curation or alternative ionization tools.

## Inputs

- SMILES strings (text file, one per line or in a table with identifiers)
- Dimorphite-DL parameter settings (pH range, ionization mode)

## Outputs

- Protonated and deprotonated adduct SMILES with explicit hydrogen counts
- Mapping of original SMILES to enumerated adduct forms with ionization states
- Structured output file (e.g., CSV or TSV) suitable for conformation generation

## How to apply

Load SMILES strings from your input file and apply Dimorphite-DL, which uses chemoinformatic rules to predict the probable ionization states of each molecule. Dimorphite-DL generates protonated and deprotonated forms by transferring hydrogens according to ionization equilibria; it handles CHNO chemistry and respects functional group logic. For each input SMILES, the tool outputs multiple adduct forms (e.g., neutral, +1, −1) with explicit hydrogen counts. Export the resulting adduct SMILES and their corresponding ionization states to a structured output file for consumption by the next step in the CCS pipeline (conformation generation).

## Related tools

- **Dimorphite-DL** (Determines protonated and deprotonated ionization states from SMILES; core tool for adduct form enumeration) — https://durrantlab.pitt.edu/dimorphite-dl
- **RDKit** (Canonicalizes and validates SMILES strings; used downstream for conformation generation on enumerated adducts) — https://www.rdkit.org

## Evaluation signals

- All output SMILES are valid and parseable by RDKit; canonical SMILES can be regenerated without error.
- Hydrogen counts are explicit in output SMILES and match expected ionization states (e.g., [M+H]+ has one more H than neutral form).
- Enumerated adduct forms produce chemically sensible structures (e.g., deprotonation occurs at acidic sites; protonation at basic sites).
- Each adduct SMILES in the output maps back to exactly one input SMILES with a consistent ionization offset.
- Output file schema matches downstream tool expectations (column names, delimiter, charge/adduct notation).

## Limitations

- Dimorphite-DL is trained on CHNO chemistry and may produce unreliable predictions for molecules containing other elements (e.g., S, P, halogens, metals).
- The tool uses chemoinformatic rules and machine learning heuristics, not quantum chemical calculations; accuracy depends on whether your molecular space resembles the training data.
- Dimorphite-DL generates a fixed set of adduct forms per molecule; it does not model unusual or context-dependent ionization (e.g., adduct formation with buffer salts, in-source fragmentation).
- The ASE-ANI conformation filter repository is deprecated and no longer supported; the workflow documentation recommends TorchANI as a replacement.

## Evidence

- [other] Dimorphite-DL to determine ionization states and generate protonated/deprotonated adduct forms for each molecule.: "Apply Dimorphite-DL to determine ionization states and generate protonated/deprotonated adduct forms for each molecule."
- [other] Dimorphite-DL: For ionization state determination. Available at: [https://durrantlab.pitt.edu/dimorphite-dl]: "Dimorphite-DL: For ionization state determination. Available at: [https://durrantlab.pitt.edu/dimorphite-dl]"
- [intro] The workflow enables prediction of CCS values for multiple protonated/deprotonated adducts and models with high automation and parallelized computation on HPC systems: "workflow allows users to predict CCS values for multiple protonated/deprotonated adducts and models with high automation and parallelized computation on high-performance computing (HPC) systems"
- [readme] DEPRECATED and no longer supported, please use [TorchANI] implementation: "DEPRECATED and no longer supported, please use [TorchANI] implementation"
- [readme] Current ANI-1x and ANI-1ccx potentials provide predictions for the CHNO elements.: "Current ANI-1x and ANI-1ccx potentials provide predictions for the CHNO elements."
