---
name: automated-metabolite-property-computation
description: Use when you have ion mobility-mass spectrometry data (raw drift times, m/z values, and feature intensities) from DTIMS-MS or SLIM-based IMS-MS platforms and need to compute collision cross section values using a calibration standard (e.g., Agilent tune-mix).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3520
  tools:
  - AutoCCS
  techniques:
  - LC-MS
  - ion-mobility-MS
  - tandem-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# automated-metabolite-property-computation

## Summary

AutoCCS is software that automates collision cross section (CCS) calculation for ion mobility-mass spectrometry data across multiple instrument platforms and calibration methods. Use this skill when you have drift time and m/z measurements from IMS-MS and need to compute standardized CCS values for molecular ion characterization.

## When to use

You have ion mobility-mass spectrometry data (raw drift times, m/z values, and feature intensities) from DTIMS-MS or SLIM-based IMS-MS platforms and need to compute collision cross section values using a calibration standard (e.g., Agilent tune-mix). This is essential when CCS values are required as input for downstream metabolite annotation, structure elucidation, or comparative lipidomics workflows.

## When NOT to use

- Input data are already pre-calculated CCS values or literature reference standards; this skill is for computing CCS from raw IMS-MS measurements.
- You lack a suitable calibration standard (e.g., no tune-mix or reference compound with known CCS co-measured with your samples).
- Your instrument data are from non-IMS platforms (e.g., LC-MS/MS without ion mobility separation).

## Inputs

- Target list file (CSV): analyte identifiers and metadata
- Frame metadata files (*.txt): IMS drift tube calibration and timing parameters
- Feature files (CSV): m/z, drift time, intensity per detected ion
- Calibrant file (TXT): reference CCS values for known standards
- Sample metadata file (CSV): raw filename, ionization polarity, sample type
- Configuration file (XML): platform and method settings

## Outputs

- CCS value table (CSV): collision cross section per molecular ion, indexed by m/z and drift time
- Calibration regression coefficients and fit metrics
- QC report: calibrant recovery, residuals, and per-sample CCS statistics

## How to apply

Install AutoCCS via conda or pip with required dependencies. Prepare three input components: (1) a target list (CSV) containing analyte metadata; (2) frame metadata files (*.txt) with drift time calibration information; (3) feature files (CSV format) extracted from raw IMS-MS runs containing m/z, drift time, and intensity per feature. Select the appropriate execution mode (stepped-field DTIMS, single-field RapidFire-DTIMS, or SLIM-IMS) and calibration method (linear, polynomial degree 1–4, or linearized power function). Execute AutoCCS with platform-specific parameters, including a calibrant file (e.g., TuneMix-CCS.txt) and sample metadata linking raw filenames to ionization polarity. The software performs field-dependent or field-independent CCS regression against calibrant standards, then outputs tabular CCS values indexed by ion. Validate output by comparing calibrant-derived CCS to literature reference values and checking for systematic drift across samples.

## Related tools

- **AutoCCS** (Core software for automated CCS calculation from IMS-MS drift time and m/z data; executes calibration regression and outputs CCS tables) — https://github.com/PNNL-Comp-Mass-Spec/AutoCCS

## Examples

```
python -u autoCCS.py --config_file data/SLIM-IMS/autoCCS_config.xml --feature_files "data/SLIM-IMS/Features_csv/*.csv" --output_dir data/SLIM-IMS/Results/ --mode single --calibrant_file data/SLIM-IMS/TuneMix-CCS_POS.txt --sample_meta data/SLIM-IMS/Datasets.csv --tunemix_sample_type AgilentTuneMix --colname_for_sample_type SampleType --colname_for_filename RawFileName --colname_for_ionization IonPolarity --single_mode batch --degree 2 --calib_method poly --ppm 150
```

## Evaluation signals

- Calibrant CCS values recovered from AutoCCS output match published reference values within ≤2% relative error
- Output CSV contains no missing or NaN CCS entries for valid feature detections above signal threshold
- Calibration regression fit (R² or residual standard error) meets or exceeds platform-specific quality thresholds reported in method documentation
- CCS values are monotonically consistent across replicate injections of the same sample (coefficient of variation <3%)
- Output schema includes required columns: m/z, drift time, CCS, ionization mode, sample identifier, and confidence/QC flags

## Limitations

- Requires high-quality calibration standards (tune-mix) co-analyzed with samples; poor calibrant recovery indicates systematic instrument drift or misalignment.
- Different platforms (DTIMS, TWIMS, SLIM) use distinct calibration physics; method selection must match instrument hardware and cannot be switched mid-workflow.
- Polynomial calibration (degree >2) may overfit to calibrant points and introduce artifacts in regions sparse in standards; stepped-field method preferred for broad m/z range coverage.
- Feature extraction upstream of AutoCCS (drift time deconvolution, m/z binning) is not handled by the tool; poor quality in input feature files propagates directly to CCS accuracy.

## Evidence

- [other] AutoCCS is software designed to perform automated collision cross section calculations for ion mobility-mass spectrometry data.: "AutoCCS is software designed to perform automated collision cross section calculations for ion mobility-mass spectrometry data."
- [readme] AutoCCS supports DTIMS-MS, TWIMS-MS (SLIM-based), stepped-field, single-field, and traveling wave-based methods with multiple calibration functions.: "AutoCCS supports the following platforms and methods: Platforms - Drift tube-based ion mobility spectrometry coupled with mass spectrometry (DTIMS-MS) instrument, Traveling wave based-IMS MS"
- [readme] Execute autoCCS.py with target list, config file, frame metadata, feature files, calibrant file, and sample metadata to compute CCS.: "python autoCCS.py --target_list_file data/SteppedField-DTIMS/TargetList.csv --config_file data/SteppedField-DTIMS/autoCCS_config.xml --framemeta_files "data/SteppedField-DTIMS/ImsMetadata/*.txt""
- [readme] Polynomial calibration degree and calibration method (poly or power) are user-selectable parameters for single-field and traveling wave methods.: "Users are allowed to apply high-order polynomial functions: quadratic (`--degree 2`), cubic (`--degree 3`), quartic (`--degree 4`), and so on. Also, it allows users to apply non-linear regression"
- [readme] Demo datasets and tutorials are provided for stepped-field DTIMS, single-field RapidFire-DTIMS, and SLIM-based IMS on Agilent tune-mix samples.: "In this tutorial, we demonstrated the CCS determination using AutoCCS for the Agilent tune-mix samples in three different platforms: stepped-field DTIMS-MS, single-field RapidFire-DTIMS-MS,"
