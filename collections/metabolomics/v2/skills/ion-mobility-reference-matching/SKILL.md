---
name: ion-mobility-reference-matching
description: Use when you have raw arrival-time data from TWIM-MS and need to convert
  it to collision cross section (CCS) values for multi-omic analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - MOCCal
  - DEIMoS
  techniques:
  - ion-mobility-MS
  license_tier: open
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

# ion-mobility-reference-matching

## Summary

Transform raw arrival-time measurements from traveling-wave ion mobility mass spectrometry (TWIM-MS) into calibrated collision cross section (CCS) values by establishing a mapping function between reference compounds with known CCS values and their corresponding arrival times. This skill enables standardization of ion-mobility data across experiments and instruments without requiring prior feature identification.

## When to use

Apply this skill when you have raw arrival-time data from TWIM-MS and need to convert it to collision cross section (CCS) values for multi-omic analysis. Use it when you have access to a calibration template containing reference compounds with known CCS values that span the mass and charge ranges of your experimental ions. This skill is essential before downstream biomolecular class assignment or cross-dataset comparison of ion-mobility properties.

## When NOT to use

- Input data is already in calibrated CCS units or processed from a vendor-supplied calibration
- Calibration reference compounds do not span the mass or arrival-time range of experimental ions
- Raw arrival-time data are from drift-time ion mobility (DTIM) instruments rather than TWIM platforms, as the calibration assumptions differ

## Inputs

- raw arrival-time data from TWIM-MS instrument
- calibration template with reference compounds and known CCS values
- ion identifiers (m/z, charge state, or other molecular identifiers)

## Outputs

- calibrated collision cross section (CCS) values
- CCS table with corresponding ion identifiers
- arrival-time-to-CCS mapping function

## How to apply

Load raw arrival-time data and a calibration template containing reference compounds and their known CCS values into MOCCal. Parse the reference compounds to identify arrival-time and CCS pairs. Establish a continuous arrival-time-to-CCS mapping function using these reference points (typically via interpolation or regression). Apply this calibration function to all experimental arrival-time values to produce calibrated CCS values. Output a table with ion identifiers and their corresponding calibrated CCS values. The mapping function quality depends on reference coverage of the mass and arrival-time ranges present in the experimental data.

## Related tools

- **MOCCal** (Python application that implements CCS calibration transformation, biomolecular class assignment, and class-specific CCS calculations for TWIM-MS data) — https://github.com/HinesLab/MOCCal
- **DEIMoS** (PNNL package required for MOCCal_RawDT workflow when processing raw calibration files) — http://github.com/pnnl/deimos

## Evaluation signals

- Calibrated CCS values are physically reasonable and fall within expected ranges for the ion types analyzed
- Arrival-time-to-CCS mapping function shows monotonic or expected functional form when plotted against reference points
- Calibration residuals (observed vs. expected CCS for reference compounds) are below instrument precision threshold
- Output CCS table contains no null or NaN values for ions whose arrival times fall within the calibration range
- Class-specific CCS values computed from calibrated data align with literature or database values for known biomolecular species

## Limitations

- Calibration accuracy is constrained by the coverage and density of reference compounds; sparse reference points may lead to extrapolation error outside the reference arrival-time range
- TWIM platforms record arrival time (detector contact) rather than drift time (cell residence), which can be confused; the software uses these terms interchangeably but the distinction affects calibration mapping
- MOCCal offers class assignment without prior feature identification, but CCS calibration itself requires a reference template; users with non-standard or novel biomolecules may lack appropriate calibration references
- No changelog is available, limiting visibility into version-specific changes or bug fixes

## Evidence

- [other] How does MOCCal convert raw arrival-time measurements from TWIM-MS into collision cross section (CCS) values through calibration?: "MOCCal implements CCS calibration as a core functionality that transforms TWIM-MS arrival-time data into collision cross section values"
- [other] Workflow step 3 of the source card: "Establish arrival-time-to-CCS mapping function using calibration reference points"
- [readme] README introduction on TWIM vs drift time distinction: "TWIM platforms record the time at which the ion reaches the detector (arrival time) rather than the time an ion spends within the TWIM cell (drift time)"
- [readme] README on functionality scope: "MOCCal offers class assignment and CCS calculations without need for identifying the features first"
- [other] Source card workflow output: "Output calibrated CCS table with corresponding ion identifiers"
