---
name: collision-energy-optimization-for-fragmentation
description: Use when when you have N-Me derivatized unsaturated sterol lipid structures
  (as SMILES or molecular formula) and need to predict MS/MS fragmentation patterns
  with collision-energy-dependent m/z values and intensities for downstream CCS prediction
  or LC-IM-MS/MS library matching.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3375
  tools:
  - Python
  - Jupyter Notebook
  - RDKit
  techniques:
  - LC-MS
  - ion-mobility-MS
  license_tier: restricted
  provenance_tier: literature
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1002/anie.202507483
  all_source_dois:
  - 10.1002/anie.202507483
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# collision-energy-optimization-for-fragmentation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Predict and optimize collision energies for MS/MS fragmentation of N-Me derived unsaturated sterol lipids by applying quantum chemistry calculation methods to fragmentation pathways. This enables accurate m/z and relative intensity annotation for isomer-level lipid characterization in LC-IM-MS/MS workflows.

## When to use

When you have N-Me derivatized unsaturated sterol lipid structures (as SMILES or molecular formula) and need to predict MS/MS fragmentation patterns with collision-energy-dependent m/z values and intensities for downstream CCS prediction or LC-IM-MS/MS library matching. Specifically applicable when double bond position isomerism must be resolved and quantitative fragment intensity ratios are required.

## When NOT to use

- Input molecules lack C=C double bonds or are not N-Me derivatized (README states 'only test sterol lipids' despite theoretical applicability to all C=C-containing molecules)
- Raw experimental MS/MS data is already available and does not require prediction (this skill is for generating predicted spectra, not interpreting acquired data)
- Collision energy optimization is not a constraint — if simple fragmentation rules suffice without energy tuning, this quantum chemistry approach is overkill

## Inputs

- SMILES strings of N-Me derivatized unsaturated sterol lipids
- Molecular formulas of N-Me derived sterol lipids
- Lipid structure identifiers with double bond position annotations

## Outputs

- Structured table with lipid identifiers, fragment assignments, m/z values, and relative intensities
- CSV or JSON record file of predicted MS/MS fragments indexed by collision energy
- Collision energy parameters and fragmentation metrics per lipid

## How to apply

Load input lipid structure data (SMILES or molecular formula) for N-Me derivatized unsaturated sterols into a Jupyter notebook environment. Apply quantum chemistry calculation methods to predict fragmentation pathways, recognizing C=C double bond positions and applying N-Me fragmentation patterns to generate collision-energy-dependent fragmentation predictions. For each lipid structure, compute predicted m/z values and relative fragment intensities as a function of collision energy. Compile results into a structured table with lipid identifiers, fragment assignments, fragmentation metrics, and collision energy parameters. Export as CSV or JSON for integration into CCS prediction and LC-IM-MS/MS matching pipelines. Validation occurs through comparison of predicted m/z and intensity patterns against experimental LC-IM-MS/MS data.

## Related tools

- **RDKit** (Structure parsing and recognition of double bond positions; generation of fragmentation patterns based on N-Me derivatization)
- **Python** (Implementation language for quantum chemistry calculation methods and fragmentation prediction scripts)
- **Jupyter Notebook** (Execution environment for all MS/MS calculation functions and collision energy optimization workflows) — github.com/Chen-micslab/QCCAssisted4DSterol

## Evaluation signals

- Predicted m/z values match experimental LC-IM-MS/MS observed fragment masses within instrument resolution (typically ≤5 ppm for high-resolution instruments)
- Relative fragment intensities show consistent collision-energy dependence: low-energy fragments are abundant for low m/z, high-energy fragments increase with collision energy
- All predicted fragments correspond to chemically plausible N-Me fragmentation cleavages at double bonds
- Exported CSV/JSON records are parseable and contain no missing values for lipid ID, fragment assignment, m/z, intensity, and collision energy fields
- Predicted spectrum comparison against experimental 4D sterolomics data (LC, IM, MS/MS, RT) yields high cosine similarity (>0.7) for matched lipid identifications

## Limitations

- Method has been tested only on sterol lipids despite theoretical applicability to all molecules with C=C bonds; generalization to other lipid classes remains unvalidated
- Quantum chemistry calculation accuracy depends on quality of input SMILES/molecular formula; incorrect or ambiguous structure notation will propagate errors
- Collision energy optimization assumes standard N-Me derivatization chemistry; alternative derivatization schemes or modifications not represented in the training basis may produce unreliable predictions

## Evidence

- [other] Apply quantum chemistry calculation methods to predict fragmentation pathways and collision energies for each lipid structure.: "Apply quantum chemistry calculation methods to predict fragmentation pathways and collision energies for each lipid structure."
- [readme] The script recognises double bond positions and generates MS/MS based on N-Me fragmentation patterns.: "The script  recognises double bond positions and generates MS/MS based on N-Me fragmentation patterns."
- [other] Generate predicted MS/MS fragments with corresponding m/z values and relative intensity annotations.: "Generate predicted MS/MS fragments with corresponding m/z values and relative intensity annotations."
- [readme] All functions are implemented in jupyter notebook: "All functions are implemented in jupyter notebook"
- [readme] The script is written on the basis of RDkit's built-in functions.: "The script is written on the basis of RDkit's built-in functions."
