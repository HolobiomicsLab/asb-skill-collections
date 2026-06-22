---
name: lipid-library-format-schema
description: Use when you have identified lipid species unique to your experimental system (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0091
  tools:
  - LipidMatch
  - MZmine
  - XCMS
  - MS-DIAL
  - Compound Discoverer
derived_from:
- doi: 10.1186/s12859-017-1744-3
  title: lipidmatch
evidence_spans:
- LipidMatch identifications are obtained by matching experimental fragment m/z values with simulated library m/z values
- LipidMatch can be used with various peak picking software (for example MZmine, XCMS, MS-DIAL, and Compound Discoverer)
- for example MZmine, XCMS, MS-DIAL, and Compound Discoverer
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipidmatch_cq
    doi: 10.1186/s12859-017-1744-3
    title: lipidmatch
  dedup_kept_from: coll_lipidmatch_cq
schema_version: 0.2.0
---

# lipid-library-format-schema

## Summary

Define and validate the structure of user-generated lipid libraries in .csv format for integration into LipidMatch workflows. This skill ensures that custom lipid entries conform to LipidMatch schema specifications so they can be combined with built-in libraries for specialized lipidomics applications.

## When to use

You have identified lipid species unique to your experimental system (e.g., synthetic lipids, rare natural variants, or lipids from non-model organisms) that are absent from the built-in LipidMatch library, and you want to augment LipidMatch identifications by adding these species with known or computationally predicted fragmentation patterns.

## When NOT to use

- You are working exclusively with common, well-characterized lipid species already present in the built-in LipidMatch library (500,000+ lipid species across 60+ types); the custom library adds no discriminatory value.
- Your instrument produces Waters vendor files; LipidMatch does not currently support Waters file formats, so validation against experimental data will not be possible.
- You lack reliable fragmentation rules or empirical MS/MS data to populate the fragment m/z column; unpredictable or missing fragmentation data will cause false negatives or misidentifications.

## Inputs

- Tab-separated or comma-separated values (.csv) file with lipid metadata
- Lipid nomenclature list (standardized names)
- Molecular formulas for candidate lipid species
- Adduct type specifications
- In-silico fragment m/z values (simulated or empirically derived)

## Outputs

- Validated .csv lipid library conforming to LipidMatch schema
- Extended LipidMatch library combining built-in and user-generated entries
- LipidMatch identification results from combined library applied to UHPLC-HRMS/MS data

## How to apply

Create a .csv file following LipidMatch schema specifications, including required columns: lipid names (standardized nomenclature), molecular formulas, adduct types (e.g., [M+H]+, [M+Na]+), and in-silico fragment m/z values computed by gas-phase fragmentation rules or empirically validated. Validate the .csv structure and content against LipidMatch format requirements (correct data types, no missing mandatory fields, m/z values within instrument resolution). Integrate the user library into LipidMatch using the documented integration mechanism provided by the software. Test the extended workflow by running LipidMatch identifications against UHPLC-HRMS/MS data (peak-picked by MZmine, XCMS, MS-DIAL, or Compound Discoverer) using the combined library (built-in + user-generated), and verify that custom lipids are correctly matched to experimental fragment m/z values with expected mass accuracy.

## Related tools

- **LipidMatch** (Host software that performs fragment m/z matching; accepts integrated user-generated .csv libraries and combines them with built-in library for lipid identification) — https://github.com/GarrettLab-UF/LipidMatch
- **MZmine** (Peak picking and feature detection for UHPLC-HRMS/MS data; output used with LipidMatch for validation of user library identifications)
- **XCMS** (Peak picking and feature detection for UHPLC-HRMS/MS data; output used with LipidMatch for validation of user library identifications)
- **MS-DIAL** (Peak picking and feature detection for UHPLC-HRMS/MS data; output used with LipidMatch for validation of user library identifications)
- **Compound Discoverer** (Peak picking and feature detection for UHPLC-HRMS/MS data; output used with LipidMatch for validation of user library identifications)

## Evaluation signals

- The .csv file passes schema validation: all required columns present, correct data types (lipid name = string, molecular formula = string, adduct type = string, m/z values = numeric), no missing mandatory fields.
- User-generated lipid entries match experimental UHPLC-HRMS/MS peaks with mass accuracy consistent with instrument resolution (Q-Exactive orbitrap ~5 ppm; Q-TOF ~10 ppm).
- Fragment m/z values in the custom library align with observed MS/MS spectra; cosine similarity or spectral contrast angle between experimental and simulated fragmentation patterns is above instrument-specific threshold.
- Combined library (built-in + user) produces no false-positive identifications on negative control samples; custom lipid identifications are rank-ordered with confidence scores consistent with match quality.
- User library entries are successfully combined with built-in library in LipidMatch workflow without runtime errors; output file lists both standard and custom lipid identifications in annotated feature table.

## Limitations

- LipidMatch does not currently support Waters vendor file formats, limiting validation to Thermo Q-Exactive, Agilent, Bruker, and SCIEX Q-TOF platforms.
- User-generated fragment m/z values rely on in-silico fragmentation rules or empirical data; if fragmentation patterns are misspecified or absent, custom lipids will not be identified or will be ranked incorrectly.
- The .csv schema specifications are not formally documented in the provided README; users must infer requirements from examples or contact developers.
- Large custom libraries may increase computational burden and collision risk with similar-mass lipids; no filtering or library compression is described.

## Evidence

- [readme] LipidMatch identifications are obtained by matching experimental fragment m/z values with simulated library m/z values: "LipidMatch identifications are obtained by matching experimental fragment m/z values with simulated library m/z values"
- [readme] User library format and integration mechanism: "LipidMatch allows for facile integration of user generated libraries for unique applications"
- [readme] Built-in library comprehensiveness and composition: "in-silico fragmentation libraries of over 500,000 lipid species across over 60 lipid types"
- [readme] Validation instruments and acquisition modes: "LipidMatch has been tested and validated using Q-Exactive orbitrap UHPLC-HRMS/MS data obtained from multiple sample types using targeted, data-dependent top-N (ddMS2-topN), and all ion fragmentation"
- [readme] Workflow modularity and peak picking compatibility: "LipidMatch can be used with various peak picking software (for example MZmine, XCMS, MS-DIAL, and Compound Discoverer)"
- [other] Workflow steps for user library integration (from task card): "Create a user-generated lipid library in .csv format following LipidMatch schema specifications (lipid names, molecular formulas, adduct types, and in-silico fragment m/z values)"
- [other] Testing and validation approach: "Test the extended workflow by running LipidMatch identifications against experimental UHPLC-HRMS/MS data using the combined library (built-in library + user-generated library)"
- [readme] Known limitation: Waters files not supported: "The software does not currently support Waters files"
