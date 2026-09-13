---
name: ionization-state-prediction
description: Use when when you have SMILES strings representing neutral organic molecules
  and need to enumerate the likely protonated (e.g., [M+H]+) and deprotonated (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3375
  tools:
  - Snakemake
  - Dimorphite-DL
  - ASE-ANI
  - QUICK
  techniques:
  - ion-mobility-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/jasms.1c00315
  title: POMICS
evidence_spans:
- Snakemake workflow manager for predicting collisional cross sections
- This repository contains a Snakemake workflow manager for predicting collisional
  cross sections (CCS)
- 'Dimorphite-DL: For ionization state determination'
- 'ASE-ANI: For conformation filtering'
- 'QUICK: For quantum calculations'
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

# ionization-state-prediction

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Predict protonated and deprotonated adduct forms of organic molecules from SMILES strings using machine learning-based ionization state determination. This skill is essential as a first step in computational workflows that require multiple ionization states (e.g., for CCS prediction in metabolomics), since most mass spectrometry experiments detect molecules in specific ionization forms.

## When to use

When you have SMILES strings representing neutral organic molecules and need to enumerate the likely protonated (e.g., [M+H]+) and deprotonated (e.g., [M−H]−) forms for downstream computational analysis such as CCS prediction, conformation generation, or quantum mechanical property calculation. This is necessary because collisional cross section and molecular properties differ by ionization state, and mass spectrometry detects specific adducts rather than neutral molecules.

## When NOT to use

- Input molecules are already in a specific ionization state (e.g., pre-protonated SMILES); applying this skill would add redundant or incorrect states.
- You are interested only in neutral molecule properties and do not need to model ionization equilibria.
- Input SMILES contain metal coordination complexes or inorganic species; Dimorphite-DL is trained on organic CHNO molecules and will not correctly predict ionization states for these.

## Inputs

- SMILES strings (simplified molecular-input line-entry system format)
- Text file with one SMILES per line (optional: with molecule identifiers)

## Outputs

- SMILES strings for protonated adducts (e.g., [M+H]+ forms)
- SMILES strings for deprotonated adducts (e.g., [M−H]− forms)
- Ionization state labels or annotations per adduct
- Mapping file linking original molecule ID to each adduct SMILES

## How to apply

Load SMILES strings from your input file. Apply Dimorphite-DL, a machine learning tool trained to predict ionization equilibria, to generate the set of chemically probable protonated and deprotonated adduct forms for each molecule. Dimorphite-DL assigns ionization states by identifying acidic and basic functional groups using pKa-based rules and neural network scoring. The tool outputs one SMILES string per adduct form (e.g., two or more per input molecule) along with the corresponding ionization state label. Export these adduct SMILES to a new file, preserving the association between parent molecule and each generated adduct, as this mapping is required for subsequent workflow steps like conformation generation and final CCS value aggregation.

## Related tools

- **Dimorphite-DL** (Predicts protonated and deprotonated adduct forms by identifying ionizable functional groups and applying machine learning scoring of ionization states.) — https://durrantlab.pitt.edu/dimorphite-dl

## Evaluation signals

- Check that each output SMILES is valid and chemically reasonable (parse with RDKit; verify no valence errors).
- Verify that the number of adducts per input molecule matches the expected distribution for typical organic molecules (commonly 2–3 forms per molecule: neutral, protonated, deprotonated).
- Confirm that protonated forms have increased hydrogen count and deprotonated forms have decreased hydrogen count relative to the input SMILES.
- Validate that ionization state labels (e.g., '+1', '−1', '0') are correctly assigned and distinct across adducts.
- Cross-check a subset of adducts against known ionization states in the chemical literature or prior CCS measurements for the same molecules.

## Limitations

- Dimorphite-DL predictions are based on pKa estimation and may not capture context-dependent ionization in complex environments (e.g., protein-bound states, non-aqueous solvents).
- The tool is trained on organic molecules containing C, H, N, O elements; predictions for molecules with other elements (e.g., halogens, metals, sulfur) may be unreliable.
- Ionization state determination is probabilistic; rare or non-equilibrium adducts may be missed or over-predicted, affecting downstream CCS accuracy if the predicted states do not match the actually-detected ions in mass spectrometry.
- The workflow generates multiple adducts per input molecule, increasing computational burden for large compound libraries if all adducts are carried through subsequent steps (e.g., conformation generation, quantum calculations).

## Evidence

- [other] Determine ionization states (protonated/deprotonated adducts) using Dimorphite-DL for each SMILES.: "Determine ionization states (protonated/deprotonated adducts) using Dimorphite-DL for each SMILES."
- [other] How does Dimorphite-DL convert input SMILES structures into protonated and deprotonated adduct forms for use in downstream CCS prediction?: "How does Dimorphite-DL convert input SMILES structures into protonated and deprotonated adduct forms for use in downstream CCS prediction?"
- [other] Apply Dimorphite-DL to determine ionization states and generate protonated/deprotonated adduct forms for each molecule.: "Apply Dimorphite-DL to determine ionization states and generate protonated/deprotonated adduct forms for each molecule."
- [readme] Dimorphite-DL: For ionization state determination. Available at: [https://durrantlab.pitt.edu/dimorphite-dl]: "Dimorphite-DL: For ionization state determination. Available at: [https://durrantlab.pitt.edu/dimorphite-dl]"
- [readme] This is a prototype interface for ANI-1x and ANI-1ccx neural network potentials: "Current ANI-1x and ANI-1ccx potentials provide predictions for the CHNO elements."
