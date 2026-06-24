---
name: mass-spectrometry-data-table-formatting
description: Use when when you have raw or processed TWIM-MS data (arrival time and
  m/z values) from a mass spectrometry instrument and need to organize it into a feature
  table before biomolecular class assignment or CCS calculations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3937
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - MOCCal
  - DEIMoS
  techniques:
  - LC-MS
  - ion-mobility-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.3c04290
  title: moccal
evidence_spans:
- MOCCal, or Multi-Omic CCS Calibrator, is a Python application
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-data-table-formatting

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Format TWIM-MS experimental data into tabular structures indexed by feature identifier, with columns for arrival time, m/z values, and assigned biomolecular class labels. This enables downstream CCS calibration and class-specific calculations without prior feature identification.

## When to use

When you have raw or processed TWIM-MS data (arrival time and m/z values) from a mass spectrometry instrument and need to organize it into a feature table before biomolecular class assignment or CCS calculations. Use this skill if your data is currently in RawDT or UserDT input formats and you need indexed feature rows.

## When NOT to use

- Input data is already a fully annotated and identified feature table with known metabolite/protein identities
- Data is from non-ion-mobility mass spectrometry platforms (e.g., standard LC-MS without TWIM capability)
- Only drift time is available and arrival time cannot be reconstructed from the instrument output

## Inputs

- Raw TWIM-MS data files (RawDT format with arrival time and m/z)
- Processed experimental TWIM-MS data (UserDT format)
- Feature-level arrival time and m/z values

## Outputs

- Tabular feature table indexed by feature identifier
- Feature table with columns for feature ID, arrival time, m/z, and assigned biomolecular class
- Class-labeled features ready for CCS calibration

## How to apply

Load experimental TWIM-MS data containing arrival time and m/z values from either raw instrument files (via DEIMoS import in RawDT mode) or pre-processed data (UserDT mode). Organize the data into a tabular format with one row per feature and columns for feature identifier, arrival time, m/z, and any physico-chemical properties used for biomolecular class assignment. The MOCCal algorithm then classifies each feature based on these properties and appends the assigned class label as an output column. Compile the result into indexed tabular output with feature ID as the primary key for downstream workflow steps like CCS calculation.

## Related tools

- **MOCCal** (Performs biomolecular class assignment and CCS calibration on formatted feature tables; accepts UserDT and RawDT input formats) — https://github.com/HinesLab/MOCCal
- **DEIMoS** (Preprocesses raw TWIM-MS data into formats compatible with MOCCal RawDT pipeline) — http://github.com/pnnl/deimos

## Evaluation signals

- Output table has exactly one row per unique feature with no missing feature IDs
- All rows contain valid arrival time (numeric) and m/z (numeric) values within instrument-expected ranges
- Feature table schema matches MOCCal input specification: feature ID column + arrival time + m/z + optional physico-chemical property columns
- Biomolecular class labels are assigned to all features without errors; each feature has exactly one class label
- Table can be successfully loaded by MOCCal without format errors or data type mismatches

## Limitations

- TWIM platforms record arrival time (time at detector) not drift time (residence in TWIM cell); the software uses these interchangeably for convenience but this distinction affects calibration interpretation
- Class assignment requires implicit physico-chemical property information; features lacking sufficient property diversity may receive unreliable or ambiguous class assignments
- No changelog or version history documented in the repository; unclear how breaking changes to input format are tracked or communicated

## Evidence

- [other] Load experimental TWIM-MS data (arrival time and m/z values) from RawDT or UserDT input format.: "Load experimental TWIM-MS data (arrival time and m/z values) from RawDT or UserDT input format."
- [other] Compile assigned class labels into a tabular output indexed by feature identifier, with one row per feature and columns for feature ID and assigned class.: "Compile assigned class labels into a tabular output indexed by feature identifier, with one row per feature and columns for feature ID and assigned class."
- [readme] TWIM platforms record the time at which the ion reaches the detector (arrival time) rather than the time an ion spends within the TWIM cell (drift time).: "TWIM platforms record the time at which the ion reaches the detector (arrival time) rather than the time an ion spends within the TWIM cell (drift time)."
- [readme] MOCCal offers class assignment and CCS calculations without need for identifying the features first.: "MOCCal offers class assignment and CCS calculations without need for identifying the features first."
- [readme] For python scripts, usage tutorials, data templates, and example data, please see the UserDT or RawDT folders.: "For python scripts, usage tutorials, data templates, and example data, please see the UserDT or RawDT folders."
