---
name: peak-apex-identification-from-intensity-profiles
description: Use when after EIC candidate generation and peak detection have been completed on LC/HRMS data, when you need to extract the retention time and intensity values at peak maxima for each detected peak.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - IDSL.IPA
  - R
  - MZmine 2
  - xcms
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1021/acs.jproteome.2c00120
  title: IDSL.IPA
evidence_spans:
- '**Intrinsic Peak Analysis (IPA)** by the [**Integrated Data Science Laboratory for Metabolomics and Exposomics (IDSL.ME)**](https://www.idsl.me) is a light-weight R package'
- light-weight R package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_idsl_ipa_cq
    doi: 10.1021/acs.jproteome.2c00120
    title: IDSL.IPA
  dedup_kept_from: coll_idsl_ipa_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.2c00120
  all_source_dois:
  - 10.1021/acs.jproteome.2c00120
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# peak-apex-identification-from-intensity-profiles

## Summary

Identify the apex (maximum intensity point) and associated properties of chromatographic peaks within EIC candidate signal intensity profiles from LC/HRMS data. This skill is essential for quantification and peak characterization in untargeted metabolomics workflows.

## When to use

Apply this skill after EIC candidate generation and peak detection have been completed on LC/HRMS data, when you need to extract the retention time and intensity values at peak maxima for each detected peak. Use it when building peak property tables that require apex intensity, retention time coordinates, and detection confidence scores for downstream alignment and annotation.

## When NOT to use

- Peak detection has not yet been run — apex identification requires validated peak boundaries as input.
- EIC candidate data is missing or malformed (absent retention time ranges or intensity profiles).
- Retention time or mass calibration is known to be severely drifted — apply retention time correction and mass correction before apex identification.

## Inputs

- EIC candidate signal intensity profiles (m/z values, retention time ranges, intensity scans)
- Detected peak list with peak boundaries and confidence flags
- Signal-to-noise ratio thresholds (configurable via parameter spreadsheet)
- Peak width constraints and baseline separation criteria

## Outputs

- Peak list with retention time at apex, m/z value, apex intensity, and detection confidence score
- Annotated peak properties including peak area, nIsoPair, RCS, S/N ratio, asymmetry factor, USP tailing factor, gaussianity, and sharpness

## How to apply

Within the IDSL.IPA workflow, the peak apex identification operates on detected peaks by analyzing the intensity profile within each peak's boundaries (defined by signal continuity and baseline separation). For each detected peak, locate the scan with maximum intensity value within the peak's retention time window. Record the retention time coordinate of this apex scan, the apex intensity value, and compute a detection confidence score based on signal-to-noise ratio (S/N using baseline, xcms method, or RMS method as configured) and peak width constraints. Filter out peaks where apex intensity does not meet the configured S/N threshold or where peak width falls outside algorithm-defined acceptable ranges. The identified apex becomes the primary quantification point for the peak.

## Related tools

- **IDSL.IPA** (Implements peak apex identification as part of the integrated peak detection and property evaluation pipeline for LC/HRMS data) — https://github.com/idslme/IDSL.IPA
- **R** (Execution environment for IDSL.IPA peak apex extraction and property calculation)
- **MZmine 2** (Comparative peak picking tool against which IDSL.IPA peak apex identification is benchmarked)
- **xcms** (Comparative peak picking tool; IDSL.IPA implements alternative S/N methods compatible with xcms approach)

## Examples

```
library(IDSL.IPA); IPA_workflow("path/to/IPA_parameters.xlsx")
```

## Evaluation signals

- Apex retention time falls strictly within the detected peak's retention time boundaries (between peak start and end scans).
- Apex intensity is the maximum value among all scans in the peak window; no scan within the window has higher intensity.
- Detection confidence score (S/N ratio) exceeds the configured threshold for the dataset; peaks below threshold are absent from output.
- Peak width (derived from apex apex location) satisfies algorithm-defined constraints; peaks outside width bounds are filtered.
- For each peak, exactly one apex is reported; multiple intensity maxima indicate a multi-peak signal requiring re-segmentation by peak detection.
- Apex intensity values are non-negative and scale appropriately with biological variation across replicate samples.

## Limitations

- Peak apex identification assumes a single well-defined intensity maximum per peak; co-eluting peaks or multiplet structures may produce spurious or ambiguous apexes.
- Signal-to-noise ratio calculation depends on reliable baseline estimation; noisy backgrounds or baseline drift can yield inflated S/N and false apex confidence.
- Peak width constraints are fixed by parameter configuration and may not adapt to variation in peak shape (asymmetry, tailing, fronting) across different chromatographic conditions or analyte classes.
- Apex identification does not account for isotope patterns or ion pairing; apex coordinates are per m/z independently. Ion pairing must be applied separately.
- Retention time correction (batch-level alignment) should be applied before apex identification for multi-batch studies to avoid false apex coordinate variation.

## Evidence

- [other] Apply the IDSL.IPA peak detection algorithm to identify peaks within each EIC candidate by analyzing signal continuity and intensity transitions.: "Apply the IDSL.IPA peak detection algorithm to identify peaks within each EIC candidate by analyzing signal continuity and intensity transitions."
- [other] Filter detected peaks according to algorithm-defined quality criteria (signal-to-noise ratio, peak width constraints, baseline separation).: "Filter detected peaks according to algorithm-defined quality criteria (signal-to-noise ratio, peak width constraints, baseline separation)."
- [other] Output detected peak list with retention time, m/z, peak apex intensity, and detection confidence scores.: "Output detected peak list with retention time, m/z, peak apex intensity, and detection confidence scores."
- [readme] Calculating 19 chromatographic peak properties such as peak area, nIsoPair, RCS, cumulated intensity, R13C, peak width, RPW, number of separation trays, asymmetry factor, USP tailing factor, skewness using derivative method, symmetry using pseudo-moments, skewness using pseudo-moments, gaussianity, S/N using baseline, S/N using the xcms method, S/N using the RMS method, and sharpness.: "Calculating 19 chromatographic peak properties such as peak area, nIsoPair, RCS, cumulated intensity, R13C, peak width, RPW, number of separation trays, asymmetry factor, USP tailing factor, skewness"
- [readme] IDSL.IPA is a suite of new algorithms covering extracted ion chromatogram (EIC) candidate generation, peak detection, peak property evaluation, recursive mass correction, retention time correction across multiple batches and peak annotation.: "IDSL.IPA is a suite of new algorithms covering extracted ion chromatogram (EIC) candidate generation, peak detection, peak property evaluation, recursive mass correction, retention time correction"
