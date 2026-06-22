---
name: ms-ms-fragment-assignment-and-annotation
description: Use when when you have predicted MS/MS fragments from quantum chemistry calculations on N-Me derived unsaturated sterol structures and need to map each fragment to its precursor lipid, calculate exact m/z values, estimate relative intensities, and produce a machine-readable reference table for.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_2258
  tools:
  - Python
  - Jupyter Notebook
  - RDkit
  techniques:
  - LC-MS
  - ion-mobility-MS
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

# MS/MS Fragment Assignment and Annotation

## Summary

This skill assigns m/z values and relative intensity annotations to predicted MS/MS fragments from N-Me derivatized unsaturated sterol lipids, then compiles them into a structured record table with lipid identifiers and fragmentation metrics. It bridges quantum chemistry fragmentation predictions and downstream CCS prediction or LC-IM-MS/MS matching workflows.

## When to use

When you have predicted MS/MS fragments from quantum chemistry calculations on N-Me derived unsaturated sterol structures and need to map each fragment to its precursor lipid, calculate exact m/z values, estimate relative intensities, and produce a machine-readable reference table for spectral matching or model training.

## When NOT to use

- Input is already a validated MS/MS spectral library with empirical m/z and intensities — use direct spectral matching instead.
- Lipids lack derivatization or do not contain C=C bonds — the RDkit-based N-Me fragmentation pattern recognition will not apply.
- Input is raw LC-IM-MS/MS instrument data — use data processing and sterol identification workflows instead.

## Inputs

- Predicted fragmentation pathways and collision energies (from quantum chemistry module)
- N-Me derivatized unsaturated sterol lipid structures (SMILES or molecular formula)
- Lipid identifiers (e.g., sterol names, database IDs)
- Double bond position data for each lipid structure

## Outputs

- Structured fragment assignment table (CSV or JSON)
- Columns: lipid identifier, fragment assignment, m/z values, relative intensity annotations, fragmentation metrics
- Reference file compatible with CCS prediction and LC-IM-MS/MS matching workflows

## How to apply

After quantum chemistry calculations predict fragmentation pathways and collision energies for each N-Me derivatized sterol lipid, use RDkit-based functions to recognize double bond positions and generate fragment structures according to N-Me fragmentation patterns. Calculate the m/z value and predict relative intensity for each fragment based on the fragmentation mechanism and collision energy. Assign each fragment to its parent lipid identifier and compile all results into a structured table (CSV or JSON) with columns for lipid identifier, fragment structure/formula, m/z, relative intensity, and fragmentation metric annotations. Export in a format compatible with downstream CCS prediction or LC-IM-MS/MS matching modules.

## Related tools

- **RDkit** (Recognizes double bond positions and generates MS/MS fragments based on N-Me fragmentation patterns; computes molecular properties and m/z calculations) — https://www.rdkit.org/
- **Python** (Primary scripting language for fragment assignment logic, table compilation, and I/O operations)
- **Jupyter Notebook** (Interactive development and execution environment for fragment assignment workflows)

## Evaluation signals

- All fragments in the output table have valid m/z values within the expected mass range for N-Me derivatized sterols.
- Relative intensities sum to 100% or are normalized consistently across all lipids.
- Each fragment is linked to exactly one parent lipid identifier with no missing or orphaned assignments.
- Fragment structures obey N-Me derivatization rules (e.g., fragmentation occurs at predicted double bond positions or N-Me functional groups).
- Output CSV/JSON validates against a predefined schema with required columns (lipid_id, fragment_formula, m_z, relative_intensity, fragmentation_metric).

## Limitations

- Method has been tested primarily on sterol lipids; applicability to other molecule classes with C=C bonds is theoretical.
- Relative intensity predictions depend on the accuracy of the upstream quantum chemistry collision energy calculations.
- RDkit-based pattern matching may not capture rare or unexpected fragmentation pathways not represented in the N-Me derivatization ruleset.
- No empirical validation of predicted m/z or intensities against real LC-IM-MS/MS data is performed within this step; validation occurs downstream in the matching workflow.

## Evidence

- [other] Generate predicted MS/MS fragments with corresponding m/z values and relative intensity annotations.: "Generate predicted MS/MS fragments with corresponding m/z values and relative intensity annotations."
- [other] Compile fragment predictions into a structured table with lipid identifiers, fragment assignments, and fragmentation metrics.: "Compile fragment predictions into a structured table with lipid identifiers, fragment assignments, and fragmentation metrics."
- [other] Export results as a CSV or JSON record file compatible with downstream CCS prediction and LC-IM-MS/MS matching workflows.: "Export results as a CSV or JSON record file compatible with downstream CCS prediction and LC-IM-MS/MS matching workflows."
- [readme] The script recognises double bond positions and generates MS/MS based on N-Me fragmentation patterns.: "The script recognises double bond positions and generates MS/MS based on N-Me fragmentation patterns."
