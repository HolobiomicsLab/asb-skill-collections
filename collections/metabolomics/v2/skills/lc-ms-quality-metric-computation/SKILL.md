---
name: lc-ms-quality-metric-computation
description: Use when after performing peak detection on centroided .mzML LC-MS data
  with screening_mode=FALSE in TARDIS.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Spectra
  - xcms
  - R
  - knitr
  - kableExtra
  - TARDIS
  - ProteoWizard (MSConvert)
  - MsExperiment
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1021/acs.analchem.5c00567
  title: tardis
evidence_spans:
- loads MS data as `Spectra` objects so it's easily integrated with other tools
- It makes use of an established retention time correction algorithm from the `xcms`
  package
- R package for *TArgeted Raw Data Integration In Spectrometry*
- knitr::include_graphics
- kableExtra::kable
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_tardis
    doi: 10.1021/acs.analchem.5c00567
    title: tardis
  dedup_kept_from: coll_tardis
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c00567
  all_source_dois:
  - 10.1021/acs.analchem.5c00567
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# LC-MS Quality Metric Computation

## Summary

Automated computation of quantitative quality metrics (AUC, max intensity, SNR, peak correlation, points over peak) for targeted compounds detected in LC-MS runs. This skill evaluates peak detection accuracy and signal quality across multiple injections and QC samples.

## When to use

Apply this skill after performing peak detection on centroided .mzML LC-MS data with screening_mode=FALSE in TARDIS. Use it when you need to assess the reliability and consistency of chromatographic peak integration across multiple runs or to generate QC feature tables summarizing per-target metrics in quality control samples.

## When NOT to use

- Input .mzML files are not centroided; TARDIS requires centroided data and will fail on profile-mode spectra.
- Target list is incomplete or lacks polarity annotations; polarity filtering cannot be applied automatically without this information.
- Data is already aggregated into a feature table; re-computing metrics on processed data may introduce bias.

## Inputs

- Target list data.frame with columns: compound ID, compound name, theoretical m/z, expected retention time (minutes), polarity indicator
- Directory of centroided .mzML LC-MS raw data files
- Optionally, MsExperiment object containing loaded MS data

## Outputs

- Data.frame with per-target AUC values across all runs
- QC feature table tibble with average metrics (Max Intensity, SNR, peak_cor, points over peak) for each target in QC runs
- CSV files: one per metric (AUC, Max Intensity, SNR, peak_cor, points over peak) with values for all targets
- Extracted ion chromatograms (EICs) saved to output folder for visual inspection

## How to apply

Execute tardisPeaks() with screening_mode=FALSE on a target list data.frame (containing compound ID, name, m/z, RT, and polarity) and an input directory of centroided .mzML files. TARDIS automatically performs polarity filtering and calculates per-run AUC for each target, then generates a QC feature table tibble with average metrics (Max Intensity, SNR, peak_cor, points over peak) computed across QC runs. The function writes metric-specific CSV files to the output folder alongside extracted ion chromatograms (EICs) for visual inspection. Verify output consistency by checking that all targets produce values for each metric and that SNR and peak_cor values fall within expected ranges for your instrument and analyte class.

## Related tools

- **xcms** (Retention time correction algorithm applied to targets before peak detection)
- **Spectra** (Loads MS data as Spectra objects for integration with TARDIS and other downstream tools)
- **TARDIS** (Core R package executing tardisPeaks() for automated peak detection and metric computation) — https://github.com/pablovgd/TARDIS
- **ProteoWizard (MSConvert)** (File conversion to .mzML format with centroiding prior to TARDIS analysis)
- **MsExperiment** (Alternative input container for MS data instead of file paths)

## Examples

```
tardisPeaks(input_dir = './mzml_files', target_list = targets_df, output_dir = './results', screening_mode = FALSE)
```

## Evaluation signals

- All targets in the target list produce a row in the output AUC data.frame with numeric values for every run.
- QC feature table contains exactly one row per target with non-null average values for Max Intensity, SNR, peak_cor, and points over peak.
- Each metric-specific CSV file contains the same set of targets (rows) and runs (columns) with consistent numeric ranges (e.g., SNR ≥ 0, peak_cor ∈ [0,1], AUC > 0).
- EICs saved to output folder correspond to each target with expected m/z and RT windows; visual inspection confirms peaks align with expected retention times.
- Polarity filtering correctly excluded targets or runs that did not match the specified polarity in the target list (no cross-polarity detections in output).

## Limitations

- Requires input files to be in centroided .mzML format; profile-mode data must be converted beforehand using ProteoWizard or similar.
- Metric computation depends on successful peak detection; poor peak detection due to low signal, co-elution, or weak ionization will produce unreliable metrics.
- QC feature table is computed only for samples labeled as QC runs; non-QC samples appear in per-run AUC data.frame but not in the averaged metrics tibble.
- SNR and peak_cor calculations are sensitive to baseline estimation and peak boundary detection; tuning of TARDIS parameters may be needed for data with high chemical noise or broad peaks.

## Evidence

- [other] tardisPeaks() with screening_mode=FALSE produces multiple output tables including: a data.frame with per-target AUC values across runs, a QC feature table tibble with average metrics, and CSV files containing Max Intensity, SNR, peak_cor, and points over the peak for all targets.: "tardisPeaks() with screening_mode=FALSE produces multiple output tables including: a data.frame with per-target AUC values across runs, a QC feature table tibble with average metrics, and CSV files"
- [intro] automatically calculate area under the peak, max intensity and various quality metrics for targeted chemical compounds in LC-MS data: "automatically calculate area under the peak, max intensity and various quality metrics for targeted chemical compounds in LC-MS data"
- [results] The results object is a list that contains a data.frame with the AUC of each target in each run: "The `results` object is a `list` that contains a `data.frame` with the AUC of each target in each run"
- [results] a tibble that contains a feature table with the average metrics for each target in the QC runs: "a `tibble` that contains a feature table with the average metrics for each target in the QC runs"
- [results] Other results include tables with the other metrics (Max. Int., SNR, peak_cor and points over the peak): "Other results include tables with the other metrics (Max. Int., SNR, peak_cor and points over the peak)"
- [intro] Input files need to be converted to the .mzML format and have to be centroided: "Input files need to be converted to the .mzML format and have to be centroided"
- [intro] Polarity filtering is done within `TARDIS`, so no polarity subsetting has to be performed: "Polarity filtering is done within `TARDIS`, so no polarity subsetting has to be performed"
- [intro] perform peak detection in all our runs by setting `screening_mode = FALSE`: "perform peak detection in all our runs by setting `screening_mode = FALSE`"
- [intro] It makes use of an established retention time correction algorithm from the `xcms` package: "It makes use of an established retention time correction algorithm from the `xcms` package"
- [intro] loads MS data as `Spectra` objects so it's easily integrated with other tools: "loads MS data as `Spectra` objects so it's easily integrated with other tools"
