---
name: protonation-state-assignment
description: Use when you have SMILES-encoded molecular structures and need to model their behavior under electrospray ionization (ESI) or other ionization methods in mass spectrometry.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0417
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0593
  tools:
  - Dimorphite-DL
  - RDKit
  - Snakemake
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

# Protonation-State Assignment

## Summary

Automated determination of ionization states (protonation and deprotonation forms) for small molecules from SMILES strings using machine-learning-guided rule sets. This skill is essential for predicting collision cross section (CCS) values of metabolites in their native ionization states during mass spectrometry analysis.

## When to use

Apply this skill when you have SMILES-encoded molecular structures and need to model their behavior under electrospray ionization (ESI) or other ionization methods in mass spectrometry. Essential before CCS prediction workflows because metabolites exist in multiple ionization states at physiological pH, and CCS values differ significantly between protonated and deprotonated adducts. Use this when downstream steps (e.g., quantum chemical calculations or CCS modeling) require explicit ionization-state specifications.

## When NOT to use

- Input molecules are already explicitly protonated or deprotonated and ionization state is not a variable (e.g., you are only modeling [M+H]+ in positive-mode MS).
- Your downstream analysis does not depend on ionization state differences (e.g., you are only predicting physicochemical properties that are ionization-independent).
- Molecules contain non-organic elements or exotic functional groups outside the CHNO scope of Dimorphite-DL's training data; the tool may fail to generate chemically reasonable adducts.

## Inputs

- SMILES strings (one per line or in a structured file)
- Optional: pH value (default ~7.4 for physiological conditions)
- Optional: charge constraints or adduct specifications

## Outputs

- Protonated/deprotonated SMILES strings with ionization state labels
- Adduct form annotation (e.g., [M+H]+, [M-H]−, [M+Na]+)
- Structured output file (CSV or JSON) pairing input SMILES with all predicted adduct forms

## How to apply

Load SMILES strings from your input file and apply Dimorphite-DL, which uses ionization-state prediction rules trained on experimental pKa and protonation data to generate all chemically plausible protonated and deprotonated adduct forms for each molecule. Dimorphite-DL outputs SMILES strings annotated with their ionization state (e.g., [M+H]+, [M-H]−). The tool accepts optional pH and charge constraints; for metabolomics applications, use physiological pH (~7.4) or instrument-specific ESI conditions. Export the resulting adduct SMILES with state labels to a structured output (CSV/JSON) for use in downstream conformation generation and CCS calculation. Verify output completeness by checking that major adduct forms (at minimum [M+H]+ for positive mode, [M-H]− for negative mode) are present for each input molecule.

## Related tools

- **Dimorphite-DL** (Predicts ionization states and generates protonated/deprotonated adduct SMILES from input structures) — https://durrantlab.pitt.edu/dimorphite-dl
- **RDKit** (Downstream tool: parses and manipulates the SMILES strings output by Dimorphite-DL for conformation generation) — https://www.rdkit.org
- **Snakemake** (Workflow orchestration: runs Dimorphite-DL as the first step in the CCS prediction pipeline with parallelization on HPC systems) — https://github.com/DasSusanta/snakemake_ccs

## Evaluation signals

- All input SMILES yield at least one valid output adduct form; no malformed or empty outputs.
- For typical organic molecules (CHNO elements), both [M+H]+ and [M-H]− forms are generated in positive and negative modes respectively.
- Output SMILES strings are valid and parseable by RDKit (no invalid SMILES syntax).
- Adduct form labels match expected ionization states (check for presence of +1/−1 charge and +H/−H mass deltas).
- CCS predictions downstream show expected trends (e.g., protonated forms have smaller CCS than deprotonated forms for the same molecule, consistent with charge-to-size effects).

## Limitations

- Dimorphite-DL is trained on CHNO elements; molecules with S, F, Cl, Br, or other heteroatoms may receive inaccurate or missing ionization predictions.
- The tool uses empirical pKa rules and may not capture ionization behavior of unusual functional groups, macrocycles, or highly strained structures.
- Predictions assume aqueous solution at the specified pH; ionization states in aprotic solvents, ion pairing effects, or ion-mobility-specific solvation are not modeled.
- No explicit output of relative abundance or confidence scores for different adduct forms; all generated forms are treated as equally plausible without quantitative ranking.

## Evidence

- [other] Apply Dimorphite-DL to determine ionization states and generate protonated/deprotonated adduct forms for each molecule.: "Apply Dimorphite-DL to determine ionization states and generate protonated/deprotonated adduct forms for each molecule."
- [intro] Dimorphite-DL: For ionization state determination. Available at: [https://durrantlab.pitt.edu/dimorphite-dl]: "Dimorphite-DL: For ionization state determination"
- [intro] workflow allows users to predict CCS values for multiple protonated/deprotonated adducts: "workflow allows users to predict CCS values for multiple protonated/deprotonated adducts"
- [intro] Ionization state determination using Dimorphite-DL: "Ionization state determination using Dimorphite-DL"
- [readme] This is a prototype interface for ANI-1x and ANI-1ccx neural network potentials: "This is a prototype interface for ANI-1x and ANI-1ccx neural network potentials for The Atomic Simulation Environment (ASE)"
