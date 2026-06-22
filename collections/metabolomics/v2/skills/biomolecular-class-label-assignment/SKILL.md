---
name: biomolecular-class-label-assignment
description: Use when you have raw or processed TWIM-MS data with arrival time and m/z values for multiple features, but lack prior structural identification (e.g., from spectral libraries or databases).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - HinesLab/MOCCal
  - MOCCal
  - DEIMoS (pnnl version 1.3.2)
derived_from:
- doi: 10.1021/acs.analchem.3c04290
  title: moccal
evidence_spans:
- MOCCal, or Multi-Omic CCS Calibrator, is a Python application
- HinesLab/MOCCal
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_moccal
    doi: 10.1021/acs.analchem.3c04290
    title: moccal
  dedup_kept_from: coll_moccal
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.3c04290
  all_source_dois:
  - 10.1021/acs.analchem.3c04290
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# biomolecular-class-label-assignment

## Summary

Assign biomolecular class labels (e.g., lipid, peptide, carbohydrate) to unidentified TWIM-MS features based on their physico-chemical properties, without requiring prior feature identification. This enables downstream class-specific collision cross section (CCS) calculations and multi-omic data interpretation.

## When to use

You have raw or processed TWIM-MS data with arrival time and m/z values for multiple features, but lack prior structural identification (e.g., from spectral libraries or databases). You need to classify features by biomolecular class to enable class-specific downstream analysis such as CCS calibration or metabolomic/lipidomic interpretation across multiple omic layers.

## When NOT to use

- Input features are already structurally identified (e.g., from spectral library matching or high-confidence MS/MS annotation); use those identities directly instead of re-assigning classes.
- Data is not from traveling-wave ion mobility mass spectrometry; MOCCal is specific to TWIM platforms and arrival time / drift time conventions.
- Your goal is to assign specific molecular structures or identities rather than broad biomolecular classes; this skill assigns class labels, not compound identities.

## Inputs

- TWIM-MS feature table in RawDT format (raw arrival time and m/z values)
- TWIM-MS feature table in UserDT format (processed calibration data with arrival time and m/z)
- Feature identifiers (one per feature)

## Outputs

- Tabular biomolecular class assignment result (one row per feature)
- Feature identifier column
- Assigned class label column (e.g., lipid, peptide, carbohydrate, small molecule)

## How to apply

Load experimental TWIM-MS data in either RawDT format (raw arrival times and m/z, requiring DEIMoS pre-processing) or UserDT format (processed calibration data). Execute MOCCal's biomolecular class-assignment algorithm, which internally evaluates physico-chemical properties (derived from m/z, charge state, and ion mobility) of each feature to assign it to a biomolecular class. The algorithm operates without requiring external identifications or spectral library matches. Compile the output into a tabular result with one row per feature, indexed by feature identifier, containing assigned class labels. Validate that all input features received a class assignment and that the assigned classes are appropriate for downstream class-specific CCS calculations.

## Related tools

- **MOCCal** (Core Python application performing biomolecular class assignment via physico-chemical property evaluation on TWIM-MS features) — https://github.com/HinesLab/MOCCal
- **DEIMoS (pnnl version 1.3.2)** (Required upstream preprocessing tool for RawDT workflow; converts raw TWIM data to calibrated arrival times and m/z) — http://github.com/pnnl/deimos

## Evaluation signals

- All input features receive a non-null, non-ambiguous class assignment (coverage = 100%)
- Assigned classes are consistent with expected biomolecular composition of the sample (e.g., lipid-rich sample should have high proportion of lipid-class features)
- Output table has correct structure: one row per input feature, with feature ID and class columns present and non-empty
- Class assignments are stable across repeated runs on the same input data (deterministic execution)
- Downstream class-specific CCS calculations execute successfully using the assigned classes without field-structure errors

## Limitations

- Assignment is based on physico-chemical properties (m/z, charge, mobility) rather than structural information; broad class labels do not guarantee specificity within a class (e.g., two structurally distinct lipids may be indistinguishable by class assignment alone).
- TWIM platforms record arrival time (time to detector) rather than drift time (time in cell); MOCCal uses these terms interchangeably for convenience, but the distinction affects interpretation if migrating to other ion mobility platforms.
- No changelog is available for this tool, limiting visibility into past behavior changes or bug fixes.
- Class assignment algorithm specifics are not detailed in the available documentation; validation against independent structural databases is recommended for novel or unexpected classes.

## Evidence

- [other] MOCCal performs experimental data biomolecular class assignment as a core functionality alongside CCS calibration and class-specific CCS calculations.: "MOCCal performs experimental data biomolecular class assignment as a core functionality alongside CCS calibration and class-specific CCS calculations."
- [other] Execute MOCCal's biomolecular class-assignment algorithm to classify each feature based on its physico-chemical properties.: "Execute MOCCal's biomolecular class-assignment algorithm to classify each feature based on its physico-chemical properties."
- [intro] MOCCal offers class assignment and CCS calculations without need for identifying the features first: "MOCCal offers class assignment and CCS calculations without need for identifying the features first"
- [other] Load experimental TWIM-MS data (arrival time and m/z values) from RawDT or UserDT input format.: "Load experimental TWIM-MS data (arrival time and m/z values) from RawDT or UserDT input format."
- [other] Compile assigned class labels into a tabular output indexed by feature identifier, with one row per feature and columns for feature ID and assigned class.: "Compile assigned class labels into a tabular output indexed by feature identifier, with one row per feature and columns for feature ID and assigned class."
- [readme] TWIM platforms record the time at which the ion reaches the detector (arrival time) rather than the time an ion spends within the TWIM cell (drift time).: "TWIM platforms record the time at which the ion reaches the detector (arrival time) rather than the time an ion spends within the TWIM cell (drift time)."
