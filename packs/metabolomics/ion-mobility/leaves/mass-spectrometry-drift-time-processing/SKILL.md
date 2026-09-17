---
name: mass-spectrometry-drift-time-processing
description: Use when when you have raw ion mobility-mass spectrometry data (drift
  times, m/z values, and frame metadata) from DTIMS-MS, TWIMS-MS, or SLIM-based instruments
  and need to compute CCS values for structural characterization or database matching.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - AutoCCS
  - conda/pip
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

# mass-spectrometry-drift-time-processing

## Summary

Automated calculation of collision cross section (CCS) values from ion mobility-mass spectrometry data by processing drift time and mass-to-charge measurements across multiple instrument platforms and calibration methods. This skill converts raw ion mobility measurements into standardized structural descriptors suitable for compound identification and database comparison.

## When to use

When you have raw ion mobility-mass spectrometry data (drift times, m/z values, and frame metadata) from DTIMS-MS, TWIMS-MS, or SLIM-based instruments and need to compute CCS values for structural characterization or database matching. Apply this skill when input includes feature tables with drift time information and access to calibration standards (tune-mix or known CCS compounds).

## When NOT to use

- Input data lack drift time information or frame metadata (required for CCS calculation).
- Samples were analyzed on platforms not supported by AutoCCS (DTIMS-MS, TWIMS-MS, or SLIM-based IMS only).
- No calibration standard (tune-mix or known CCS compounds) is available for the ionization polarity and platform used.

## Inputs

- target_list_file (CSV): molecular identifiers and expected masses
- framemeta_files (TXT): drift time windows, electric field strengths, pressure, temperature per frame
- feature_files (CSV): detected m/z, drift time, and intensity per feature per sample
- calibrant_file (TXT): reference CCS values for calibration standards (tune-mix or custom)
- config_file (XML): instrument-specific parameters and processing settings
- sample_meta (CSV, optional): sample metadata including sample type, raw filename, ionization polarity

## Outputs

- CCS_values (CSV): calculated collision cross section per molecular ion per sample, with metadata
- calibration_curve (plot/parameters): fitted calibration function (linear/polynomial/power) with R² and residuals
- feature_summary (CSV): annotated features with assigned CCS, quality flags, and calibration error

## How to apply

Install AutoCCS via conda (recommended) or pip with Python 3.7+. Prepare input data: (1) a target list file (CSV) containing molecular targets; (2) frame metadata files (.txt) with drift time and electric field parameters; (3) feature files (CSV) with detected m/z, drift time, and intensity values; (4) a calibration file (TXT) with known CCS standards for the platform and polarity used. Select the appropriate mode (multi for stepped-field DTIMS with multiple E/V ratios, or single for single-field/traveling-wave methods) and calibration function (linear, polynomial degree 1–4, or linearized power function). Execute autoCCS.py with these inputs, specifying output directory and optional sample metadata for batch processing. Extract computed CCS values from the output CSV, indexed by molecular ion and sample. Validate results by confirming CCS values fall within expected ranges for the compound class and instrument type, and that calibration R² or residuals meet quality thresholds.

## Related tools

- **AutoCCS** (Executes automated CCS calculation workflow; handles stepped-field DTIMS, single-field DTIMS, and traveling-wave IMS; manages calibration and batch processing) — https://github.com/PNNL-Comp-Mass-Spec/AutoCCS
- **conda/pip** (Dependency manager and Python environment setup for AutoCCS installation)

## Examples

```
python -u autoCCS.py --config_file data/SteppedField-DTIMS/autoCCS_config.xml --framemeta_files "data/SteppedField-DTIMS/ImsMetadata/*.txt" --feature_files "data/SteppedField-DTIMS/Features_csv/*.csv" --target_list_file data/SteppedField-DTIMS/TargetList.csv --output_dir data/SteppedField-DTIMS/Results/ --threshold_n_fields 5 --mode multi
```

## Evaluation signals

- Calibration curve R² or fit residuals meet instrument-specific acceptance criteria (typically R² > 0.99 for linear, R² > 0.995 for polynomial).
- Computed CCS values for reference standards (tune-mix ions) match literature or vendor-provided CCS within ±2% error tolerance.
- Output CCS values are monotonic with m/z within each sample (larger, more compact ions should show expected CCS trends).
- Feature-level CCS variance across replicates (same compound, different runs) is < 1–2% relative standard deviation.
- Output CSV schema matches expected columns (m/z, CCS, drift time, intensity, calibration_method, quality_flag) with no missing or NaN values for valid features.

## Limitations

- AutoCCS is validated only for DTIMS-MS (stepped-field and single-field), TWIMS-MS, and SLIM-based IMS; other ion mobility platforms are not supported.
- Accuracy depends critically on calibration standard quality and availability for the specific ionization polarity; systematic calibration errors propagate to all sample CCS values.
- Stepped-field mode requires at least 5 electric field ratios (--threshold_n_fields 5); samples with fewer field strengths cannot be reliably processed in multi mode.
- High-order polynomial calibration functions (degree ≥ 3) risk overfitting to calibration standards and may produce unstable CCS estimates for out-of-range m/z values.
- Feature detection and assignment upstream of AutoCCS (e.g., m/z picking, drift time alignment) are assumed correct; errors in feature calling are not corrected by AutoCCS.

## Evidence

- [readme] Automated Collision Cross Section calculation software for ion mobility-mass spectrometry: "Automated Collision Cross Section calculation software for ion mobility-mass spectrometry"
- [readme] AutoCCS supports the following platforms and methods: Drift tube-based ion mobility spectrometry coupled with mass spectrometry (DTIMS-MS) instrument, Traveling wave based-IMS MS (TWIMS-MS) such as Structures for Lossless Ion Manipulations (SLIM)-based IMS-MS: "Drift tube-based ion mobility spectrometry coupled with mass spectrometry (DTIMS-MS) instrument; Traveling wave based-IMS MS (TWIMS-MS) such as Structures for Lossless Ion Manipulations (SLIM)-based"
- [readme] Methods supported include Stepped field method, Single field method, Traveling wave-based method: "Stepped field method, Single field method, Traveling wave-based method"
- [readme] Calibration functions for single field and traveling wave-based methods: Linear function, Polynomial functions (e.g. quadratic or cubic functions), Linearized power function: "Linear function, Polynomial functions (e.g. quadratic or cubic functions), Linearized power function"
- [readme] Install Python 3.7 (or newer) and use pip as follows to install dependencies: "Install Python 3.7 (or newer) and use pip"
- [readme] Users are allowed to apply high-order polynomial functions: quadratic (--degree 2), cubic (--degree 3), quartic (--degree 4), and so on: "Users are allowed to apply high-order polynomial functions: quadratic (--degree 2), cubic (--degree 3), quartic (--degree 4)"
- [readme] --threshold_n_fields 5 for stepped-field DTIMS workflow: "--threshold_n_fields 5"
- [readme] Demo dataset is publicly available at MassIVE (Accession: MSV000085979): "Demo dataset is publicly available at MassIVE"
