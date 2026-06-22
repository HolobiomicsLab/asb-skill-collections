---
name: lipid-derivatization-chemistry-modeling
description: Use when you have N-methyl-derivatized unsaturated sterol lipid structures (as SMILES or molecular formula) and need to predict their MS/MS fragmentation behavior before experimental acquisition, or to build a reference spectral library for isomer-level sterol identification in tissue samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3941
  edam_topics:
  - http://edamontology.org/topic_0702
  - http://edamontology.org/topic_3375
  tools:
  - Python
  - Jupyter Notebook
  - RDKit
  - Python (scikit-learn, quantum chemistry libraries)
  techniques:
  - ion-mobility-MS
  - tandem-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# lipid-derivatization-chemistry-modeling

## Summary

Models fragmentation chemistry and MS/MS patterns for N-methyl-derivatized unsaturated sterol lipids using quantum chemistry calculations and RDKit-based double-bond recognition. Produces predicted fragment ions with m/z values and relative intensities for downstream CCS prediction and LC-IM-MS/MS matching.

## When to use

You have N-methyl-derivatized unsaturated sterol lipid structures (as SMILES or molecular formula) and need to predict their MS/MS fragmentation behavior before experimental acquisition, or to build a reference spectral library for isomer-level sterol identification in tissue samples.

## When NOT to use

- Input lipids lack N-methyl derivatization or do not contain C=C bonds (model is specialized to N-Me sterols with unsaturation; applicability to other lipid classes not validated).
- Experimental MS/MS spectra are already available and you only need to match against reference libraries (use spectral matching instead of de novo prediction).
- Fragment intensities must be predicted without consideration of collision energy or fragmentation mechanism (this skill requires quantum chemistry input).

## Inputs

- Lipid structure data (SMILES strings or molecular formulas for N-Me derivatized unsaturated sterols)
- Quantum chemistry parameters (collision energies, fragmentation rule definitions)
- RDKit molecular graph representation

## Outputs

- Predicted MS/MS fragment table (lipid ID, fragment assignment, m/z values, relative intensities)
- Fragmentation metrics and collision energy annotations
- CSV or JSON export compatible with CCS prediction and LC-IM-MS/MS matching pipelines

## How to apply

Load lipid structure data (SMILES or molecular formula) into a Jupyter notebook environment. Use RDKit's built-in functions to recognize double bond positions within the N-Me derivatized sterol scaffold. Apply quantum chemistry calculation methods to predict fragmentation pathways and collision energies specific to N-Me cleavage patterns. Generate predicted MS/MS fragments with annotated m/z values and relative intensity scores based on the fragmentation model. Compile results into a structured table indexed by lipid identifier, fragment assignment, and fragmentation metrics (e.g., collision energy thresholds), then export as CSV or JSON for input to CCS prediction and LC-IM-MS/MS matching workflows.

## Related tools

- **RDKit** (Recognizes double bond positions and generates fragmentation patterns from N-Me derivatized lipid molecular structures)
- **Jupyter Notebook** (Execution environment for implementing MS/MS calculation functions and managing the workflow pipeline)
- **Python (scikit-learn, quantum chemistry libraries)** (Applies quantum chemistry calculation methods to predict fragmentation pathways and collision energies)

## Evaluation signals

- Fragment m/z values are chemically consistent with N-Me cleavage of the parent sterol structure (no impossible mass losses or gain of atoms).
- Relative intensity annotations follow expected patterns for charge-retaining versus neutral loss fragments under the specified collision energy.
- CSV/JSON export contains all required fields (lipid ID, fragment assignment, m/z, intensity) with no missing or non-numeric values in the intensity column.
- Predicted fragments can be successfully matched to experimental LC-IM-MS/MS spectra with cosine similarity or similar metrics at expected m/z tolerances.
- Output is reproducible: re-running the notebook on the same input SMILES/formulas produces identical fragment tables within floating-point precision.

## Limitations

- Model is specialized to N-Me derivatized unsaturated sterols; applicability to other lipid classes with C=C bonds is theoretical and not yet experimentally validated.
- Quantum chemistry predictions depend on the accuracy of the underlying collision energy model and fragmentation rule definitions; systematic deviations from experimental MS/MS may occur for unusual sterol isomers.
- Double bond position recognition relies on RDKit's chemical parsing; malformed or ambiguous SMILES strings may produce incorrect or failed predictions.
- Relative intensity predictions are computational approximations; absolute peak heights in real MS/MS data will depend on instrumental parameters (e.g., ionization efficiency, detector gain) not captured by the model.

## Evidence

- [other] MS/MS calculations as the first of three main workflow parts for processing N-Me derived unsaturated sterol lipids, with all functions implemented in Jupyter notebooks: "The project implements MS/MS calculations as the first of three main workflow parts for processing N-Me derived unsaturated sterol lipids, with all functions implemented in Jupyter notebooks."
- [other] Apply quantum chemistry methods to predict fragmentation and export structured results: "Apply quantum chemistry calculation methods to predict fragmentation pathways and collision energies for each lipid structure. Generate predicted MS/MS fragments with corresponding m/z values and"
- [readme] RDKit-based double bond recognition for N-Me fragmentation patterns: "The script is written on the basis of RDkit's built-in functions. The script recognises double bond positions and generates MS/MS based on N-Me fragmentation patterns."
- [readme] Applicability scope statement: "Theoretically applicable to all molecules including C=C bond (only test sterol lipids)."
- [other] CSV or JSON export for downstream workflows: "Export results as a CSV or JSON record file compatible with downstream CCS prediction and LC-IM-MS/MS matching workflows."
