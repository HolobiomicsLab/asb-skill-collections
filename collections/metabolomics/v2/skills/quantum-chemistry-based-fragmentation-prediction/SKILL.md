---
name: quantum-chemistry-based-fragmentation-prediction
description: Use when when you have SMILES strings or molecular formulae for N-Me derivatized unsaturated sterol lipids and need to generate theoretical MS/MS spectra (predicted fragment m/z values and intensities) to compare against experimental LC-IM-MS/MS data before performing CCS prediction or downstream.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3637
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - Python
  - Jupyter Notebook
  - RDKit
derived_from:
- doi: 10.1002/anie.202507483
  title: NA
evidence_spans:
- collection of Python scripts
- All functions are implemented in jupyter notebook
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_na_cq
    doi: 10.1002/anie.202507483
    title: NA
  dedup_kept_from: coll_na_cq
schema_version: 0.2.0
---

# quantum-chemistry-based-fragmentation-prediction

## Summary

Predicts MS/MS fragmentation patterns and collision-induced dissociation (CID) pathways for N-Me derivatized unsaturated sterol lipids using quantum chemistry calculations and RDKit-based double-bond recognition. This workflow generates theoretical m/z values and relative intensity annotations to support isomer-level lipid identification in 4D sterolomics.

## When to use

When you have SMILES strings or molecular formulae for N-Me derivatized unsaturated sterol lipids and need to generate theoretical MS/MS spectra (predicted fragment m/z values and intensities) to compare against experimental LC-IM-MS/MS data before performing CCS prediction or downstream lipid identification.

## When NOT to use

- Input lipids are not N-Me derivatized (fragmentation rules are specific to N-Me substitution patterns)
- Lipid structures contain no C=C bonds or are fully saturated (the RDKit-based double-bond recognition module will not identify fragmentation sites)
- Experimental MS/MS spectra are already available and validated (use direct spectrum matching instead of prediction)

## Inputs

- SMILES strings for N-Me derivatized unsaturated sterol lipids
- Molecular formula for N-Me derived sterols
- Lipid structure metadata (lipid class, double-bond positions, N-Me derivatization site)

## Outputs

- CSV or JSON table of predicted MS/MS fragments with m/z values and relative intensities
- Fragment assignment records linked to lipid identifiers
- Fragmentation metrics (collision energy, pathway probability)

## How to apply

Load input lipid structures as SMILES or molecular formula into a Jupyter notebook environment. Apply RDKit-based functions to recognize double-bond positions within each structure, then apply N-Me fragmentation pattern rules to enumerate likely CID pathways at physiologically relevant collision energies. For each fragmentation pathway, compute the theoretical m/z value of each fragment and estimate relative intensity based on fragmentation likelihood. Compile predictions into a structured table (CSV or JSON) with columns for lipid identifier, fragment assignment, m/z, intensity, and fragmentation metrics. Export this table for downstream CCS prediction and LC-IM-MS/MS matching workflows.

## Related tools

- **RDKit** (Recognizes double-bond positions in lipid structures and generates N-Me fragmentation patterns)
- **Python** (Language for implementing MS/MS calculation functions and data compilation)
- **Jupyter Notebook** (Interactive environment for implementing and executing MS/MS calculation workflows)

## Evaluation signals

- All output m/z values fall within expected mass range for predicted fragments (check against lipid parent mass and typical loss patterns for sterols)
- Fragmentation table contains no missing or null m/z entries; all lipid identifiers are present and unique
- Relative intensities sum to a consistent baseline (e.g., normalized to 100% or log-scale); no negative or physically impossible intensity values
- Double-bond recognition correctly identified C=C bond positions in input SMILES; verify by spot-checking 5–10 structures against original formula
- Output CSV/JSON schema matches downstream CCS prediction and LC-IM-MS/MS matching input requirements (schema validation against expected column names and data types)

## Limitations

- Script is theoretically applicable to all molecules with C=C bonds but has only been tested on sterol lipids; performance on other lipid classes is unvalidated.
- N-Me fragmentation rules are fixed; they do not adapt to novel derivatization sites or unexpected structural modifications.
- Quantum chemistry collision energy predictions rely on theoretical models; predicted CID pathways may diverge from experimental spectra, especially for complex isomers or unexpected rearrangements.
- RDKit-based double-bond recognition may fail or produce ambiguous assignments for highly unsaturated or conjugated systems not represented in training data.

## Evidence

- [intro] MS/MS calculations as the first of three main workflow parts for processing N-Me derived unsaturated sterol lipids: "The project implements MS/MS calculations as the first of three main workflow parts for processing N-Me derived unsaturated sterol lipids"
- [readme] RDKit-based double-bond recognition and N-Me fragmentation pattern generation: "The script is written on the basis of RDkit's built-in functions. The script recognises double bond positions and generates MS/MS based on N-Me fragmentation patterns."
- [intro] Input and output data formats for the MS/MS calculation workflow: "Load input lipid structure data (SMILES or molecular formula) for N-Me derivatized unsaturated sterols. ... Generate predicted MS/MS fragments with corresponding m/z values and relative intensity"
- [readme] Scope of applicability: sterol lipids only, despite theoretical generality: "Theoretically applicable to all molecules including C=C bond (only test sterol lipids)."
- [readme] Implementation environment and tools: "All functions are implemented in jupyter notebook"
