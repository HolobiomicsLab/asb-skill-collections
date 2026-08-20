---
name: ion-mobility-spectrometry-data-interpretation
description: Use when you have raw ion mobility-mass spectrometry data (drift time
  and m/z measurements) from DTIMS-MS, TWIMS-MS, or SLIM-based IMS-MS instruments
  and need to derive collision cross section values for molecular ion characterization.
  Use it specifically when calibrant standards (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - AutoCCS
  techniques:
  - ion-mobility-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1093/bioinformatics/btab429
  title: AutoCCS
evidence_spans:
- github.com__PNNL-Comp-Mass-Spec__AutoCCS
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_autoccs_cq
    doi: 10.1093/bioinformatics/btab429
    title: AutoCCS
  dedup_kept_from: coll_autoccs_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btab429
  all_source_dois:
  - 10.1093/bioinformatics/btab429
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ion-mobility-spectrometry-data-interpretation

## Summary

Automated calculation of collision cross section (CCS) values from ion mobility-mass spectrometry measurements using platform-specific calibration methods. This skill enables standardized structural characterization of ionized molecules across different IMS platforms (DTIMS, TWIMS, SLIM) by calibrating drift time observations against known standards and computing CCS metrics.

## When to use

Apply this skill when you have raw ion mobility-mass spectrometry data (drift time and m/z measurements) from DTIMS-MS, TWIMS-MS, or SLIM-based IMS-MS instruments and need to derive collision cross section values for molecular ion characterization. Use it specifically when calibrant standards (e.g., Agilent TuneMix) are available and you need reproducible, high-throughput CCS computation across multiple samples or experimental conditions.

## When NOT to use

- Input data are already processed into a feature table without raw drift time measurements or frame metadata — CCS calculation requires raw drift time and m/z pairs.
- No suitable calibrant standard is available or calibrant CCS values are unknown — the calibration step is mandatory for accurate CCS computation.
- Data originate from ion mobility instruments not explicitly supported by AutoCCS (e.g., field asymmetric IMS, drift cell IMS without traveling wave mode) — platform-specific calibration logic may not apply.

## Inputs

- Ion mobility frame metadata files (drift time measurements with frame IDs)
- Feature files in CSV format (m/z, intensity, and retention/drift time per peak)
- Target list CSV (analyte names, m/z values, expected identifications)
- Calibrant file with reference CCS values for standard compounds
- Configuration XML file with instrument parameters (platform, field voltage, gas properties)
- Optional: sample metadata CSV (sample types, ionization mode, raw filenames)

## Outputs

- Structured CSV file containing calculated CCS values per molecular ion
- CCS values indexed by sample, m/z, drift time, and associated metadata
- Calibration fit plots and residual diagnostics (platform-dependent)
- Log file documenting processing steps, calibration statistics, and any warnings

## How to apply

Install AutoCCS via conda or pip with required Python dependencies. Prepare input files: (1) ion mobility frame metadata (drift times from raw instrument output), (2) feature files (detected m/z and intensity peaks in CSV format), (3) a target list CSV specifying analytes of interest, (4) a calibrant file with known CCS values for your standard mixture, and (5) a configuration XML file defining instrument parameters (gas flow, temperature, voltage). Execute autoCCS.py with appropriate flags for your platform (--mode multi for stepped-field DTIMS; --mode single for single-field or traveling wave methods) and calibration function (--calib_method poly for polynomial fitting, or power for linearized power function). Select the polynomial degree (--degree 1 for linear, 2 for quadratic, 3 for cubic) based on the calibration curve fit quality. The workflow automatically performs drift time normalization, applies the calibration function to convert drift times to CCS values, and outputs a structured CSV file with CCS values indexed by molecular ion, sample, and metadata.

## Related tools

- **AutoCCS** (Core software for automated collision cross section calculation; accepts IMS-MS data (drift time, m/z, intensity) and outputs calibrated CCS values via polynomial or power-law fitting against standards.) — https://github.com/PNNL-Comp-Mass-Spec/AutoCCS

## Examples

```
python -u autoCCS.py --config_file data/SLIM-IMS/autoCCS_config.xml --feature_files "data/SLIM-IMS/Features_csv/*.csv" --output_dir data/SLIM-IMS/Results/ --mode single --calibrant_file data/SLIM-IMS/TuneMix-CCS_POS.txt --sample_meta data/SLIM-IMS/Datasets.csv --tunemix_sample_type AgilentTuneMix --colname_for_sample_type SampleType --colname_for_filename RawFileName --colname_for_ionization IonPolarity --single_mode batch --degree 2 --calib_method poly --ppm 150
```

## Evaluation signals

- Calibration curve R² or fit statistic exceeds 0.98 (ensemble of calibrant ions should cluster tightly on the regression line).
- Output CCS values for calibrant standards match reference values within ±2% (or instrument-specific tolerance); residuals should show no systematic bias across m/z range.
- All input features are represented in the output CSV with no unexpected nulls or NaN values (except for ions failing quality thresholds).
- Drift time normalization is consistent: replicate analyses of the same sample produce CCS distributions with coefficient of variation <3%.
- Log file contains no errors during frame metadata parsing, feature file reading, or calibration fitting; warnings (e.g., low signal intensity) are documented with affected feature IDs.

## Limitations

- Accuracy and precision depend on calibrant availability and quality; if calibrant CCS values are inaccurate or the standard mixture is degraded, all downstream CCS estimates will be biased.
- Requires platform-specific configuration (instrument voltage, drift gas properties, collision cell geometry); incorrect parameters in the configuration XML will invalidate results.
- Polynomial calibration functions (degree >2) may overfit at the extremes of m/z range if calibrants are sparse; linearized power function is more robust but assumes a specific physical model.
- Traveling wave field calibration (TWIMS, SLIM) is more sensitive to wave parameters (frequency, amplitude) than stepped-field methods; small drifts in instrument tuning between runs can affect reproducibility.
- Feature detection and peak picking are upstream; poor quality feature files (e.g., unresolved multiplets, noise artifacts) will propagate into incorrect CCS assignments.

## Evidence

- [other] AutoCCS is software designed to perform automated collision cross section calculations for ion mobility-mass spectrometry data.: "AutoCCS is software designed to perform automated collision cross section calculations for ion mobility-mass spectrometry data."
- [readme] AutoCCS supports Drift tube-based ion mobility spectrometry coupled with mass spectrometry (DTIMS-MS), Traveling wave based-IMS MS (TWIMS-MS) such as Structures for Lossless Ion Manipulations (SLIM)-based IMS-MS.: "Platforms
  - Drift tube-based ion mobility spectrometry coupled with mass spectrometry (DTIMS-MS)
  - Traveling wave based-IMS MS (TWIMS-MS) such as Structures for Lossless Ion Manipulations"
- [readme] AutoCCS supports Stepped field method, Single field method, and Traveling wave-based method with calibration functions including Linear function, Polynomial functions (e.g. quadratic or cubic functions), and Linearized power function.: "Methods
  - Stepped field method
  - Single field method
  - Traveling wave-based method
- Calibration functions for single field and traveling wave-based methods
  - Linear function
  - Polynomial"
- [other] Execute the AutoCCS software with the input data to perform automated collision cross section calculations. Extract and aggregate computed CCS values from the AutoCCS output.: "Execute the AutoCCS software with the input data to perform automated collision cross section calculations. Extract and aggregate computed CCS values from the AutoCCS output."
- [readme] Users are allowed to apply high-order polynomial functions: quadratic (--degree 2), cubic (--degree 3), quartic (--degree 4). Also, it allows users to apply non-linear regression based on the linearized power function.: "Users are allowed to apply high-order polynomial functions: quadratic (`--degree 2`), cubic (`--degree 3`), quartic (`--degree 4`), and so on. Also, it allows users to apply non-linear regression"
- [other] Prepare ion mobility-mass spectrometry input data in the format required by AutoCCS (raw spectrometry measurements with drift time and mass-to-charge information).: "Prepare ion mobility-mass spectrometry input data in the format required by AutoCCS (raw spectrometry measurements with drift time and mass-to-charge information)."
- [readme] In this tutorial, we demonstrated the CCS determination using AutoCCS for the Agilent tune-mix samples in three different platforms: stepped-field DTIMS-MS, single-field RapidFire-DTIMS-MS, SLIM-based IMS.: "In this tutorial, we demonstrated the CCS determination using AutoCCS for the Agilent tune-mix samples in three different platforms: stepped-field DTIMS-MS, single-field RapidFire-DTIMS-MS,"
