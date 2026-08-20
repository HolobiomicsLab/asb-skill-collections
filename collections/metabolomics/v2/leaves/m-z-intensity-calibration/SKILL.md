---
name: m-z-intensity-calibration
description: Use when you have raw or processed MS spectrum data (m/z and intensity
  pairs) from DI-MS, ASAP-MS, or other high-throughput mass spectrometry instruments
  that requires automated peak detection.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - RapidMass
  - DI-MS
  - ASAP-MS
  techniques:
  - direct-infusion-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.4c05062
  title: RapidMass
evidence_spans:
- We have developed a versatile software platform, RapidMass.
- We have developed a versatile software platform, RapidMass
- supports data from multiple instruments, including DI-MS and ASAP-MS
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_rapidmass_cq
    doi: 10.1021/acs.analchem.4c05062
    title: RapidMass
  dedup_kept_from: coll_rapidmass_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c05062
  all_source_dois:
  - 10.1021/acs.analchem.4c05062
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# m/z-Intensity Calibration

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Calibration of mass-to-charge ratio (m/z) and intensity values in raw or processed mass spectrometry spectra to ensure accurate peak detection and quantification. This skill normalizes spectral data before downstream analysis, enabling reliable automated peak identification and sample discrimination.

## When to use

Apply this skill when you have raw or processed MS spectrum data (m/z and intensity pairs) from DI-MS, ASAP-MS, or other high-throughput mass spectrometry instruments that requires automated peak detection. Use it before peak identification workflows when spectral calibration state is unknown or when comparing spectra across multiple instrument runs or sample batches.

## When NOT to use

- Input spectra are already verified as calibrated and instrument-corrected by the source data provider.
- Analysis goal is qualitative only (e.g., presence/absence of known m/z markers) and does not require quantitative intensity accuracy.
- Data have been processed through external calibration pipelines (e.g., vendor software) and you are working only with already-normalized feature tables.

## Inputs

- Raw mass spectrometry spectrum data (m/z and intensity pairs)
- Processed MS spectrum data in vendor or open formats (mzML, mzXML, or NetCDF)
- Instrument metadata (instrument type: DI-MS, ASAP-MS, AI-MS, or LDI-MS)

## Outputs

- Calibrated m/z values (mass-to-charge ratios normalized to reference scale)
- Normalized intensity values (standardized across spectral range)
- Calibration report with reference peak assignments and residual errors
- Pre-processed spectrum file ready for automatic peak detection

## How to apply

Load raw or processed MS spectrum data as m/z/intensity pairs from the input file. Apply RapidMass's integrated calibration routines to normalize m/z values against known reference peaks and to standardize intensity measurements across the spectral range. The calibration step is part of the data pre-processing phase that precedes peak detection. Verify calibration quality by checking that peak positions align with expected m/z values and that intensity distributions are consistent across replicate runs. Store calibrated spectra in a structured intermediate format before passing to the automatic peak detection algorithm.

## Related tools

- **RapidMass** (Integrated software platform that performs m/z-intensity calibration as part of its data pre-processing workflow before automatic peak detection and species authentication) — https://github.com/Katherine00689/RapidMass
- **DI-MS** (Direct infusion mass spectrometry instrument; spectra from this instrument require calibration before downstream analysis in RapidMass)
- **ASAP-MS** (Ambient sampling analysis probe mass spectrometry instrument; spectra from this instrument require calibration before downstream analysis in RapidMass)

## Evaluation signals

- Calibrated m/z values match expected theoretical m/z within ±5 ppm (or instrument-specific tolerance) of known reference peaks or previously validated standards.
- Intensity distributions are consistent when replicate spectra are calibrated, showing reproducible peak heights and area under curve (AUC) across multiple runs.
- Peak detection algorithm successfully identifies expected peaks of interest after calibration, with confidence scores above the threshold used for downstream sample discrimination.
- Calibration residuals (difference between observed and expected m/z for reference peaks) show no systematic drift across the mass range.
- Calibrated spectrum can be directly compared to a validated database using database search algorithms without further normalization steps.

## Limitations

- Calibration accuracy depends on availability of well-defined reference peaks in the raw spectrum; spectra with poor signal-to-noise ratio or missing reference regions may require manual intervention or may not calibrate successfully.
- RapidMass README does not specify exact calibration algorithms, reference standards, or m/z tolerance thresholds—users should consult the full article or contact the authors for methodological details.
- No changelog available for RapidMass, making it unclear which versions have calibration improvements or bug fixes affecting m/z accuracy.
- Calibration may vary by instrument type (DI-MS vs. ASAP-MS vs. ambient ionization methods); cross-platform database searches may require instrument-specific calibration profiles.

## Evidence

- [readme] data pre-processing and peak detection integration: "This tool integrates data pre-processing, analysis, and evaluation"
- [other] m/z and intensity pair input format: "Load raw or processed MS spectrum data (mz/intensity pairs) from input file."
- [other] automatic peak detection follows calibration: "Apply RapidMass automatic peak detection algorithm to identify peaks of interest from the spectrum."
- [readme] multi-instrument support requirement: "supports data from multiple instruments, including DI-MS and ASAP-MS"
- [other] structured output with m/z and intensity metrics: "Aggregate results into a structured output table with peak identifiers, m/z, intensity, and confidence scores."
