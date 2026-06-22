---
name: chromatographic-peak-characterization
description: Use when after screening-mode validation of your m/z and retention time (RT) windows has confirmed that targets are visible in your data. Use it when you have centroided .mzML files, a validated target compound table with adjusted expected RT values (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3172
  tools:
  - TARDIS
  - Spectra
  - R
  - xcms
  - MSConvert (ProteoWizard)
derived_from:
- doi: 10.1021/acs.analchem.5c00567
  title: tardis
evidence_spans:
- Targeted peak integration of LC-MS data using TARDIS
- loads MS data as `Spectra` objects so it's easily integrated with other tools
- rmarkdown::html_document
- Quick start for targeted peak integration of LC-MS data using TARDIS
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_idia_qc_cq
    doi: 10.1038/s41467-024-54871-1
    title: iDIA-QC
  - build: coll_metaclean_cq
    doi: 10.1007/s11306-020-01738-3
    title: MetaClean
  - build: coll_tardis_cq
    doi: 10.1021/acs.analchem.5c00567
    title: tardis
  dedup_kept_from: coll_tardis_cq
schema_version: 0.2.0
---

# chromatographic-peak-characterization

## Summary

Automated extraction and quality assessment of chromatographic peaks for targeted compounds in LC–MS data, producing integrated area-under-curve (AUC), intensity, signal-to-noise ratio, and peak correlation metrics across multiple sample runs. This skill is essential when transitioning from targeted screening to full quantitative analysis of metabolomic or lipidomic cohorts.

## When to use

Apply this skill after screening-mode validation of your m/z and retention time (RT) windows has confirmed that targets are visible in your data. Use it when you have centroided .mzML files, a validated target compound table with adjusted expected RT values (e.g., based on screening results), and you need quantitative peak metrics (AUC, Max. Int., SNR, peak_cor, points_over_peak) across all 14+ sample runs for metabolomics or lipidomics workflows.

## When NOT to use

- Input files are not centroided or are in non-.mzML formats — first convert and centroid using MSConvert.
- Expected RT values have not been validated via screening_mode = TRUE — perform screening adjustment before full peak characterization.
- You are working with non-targeted or untargeted data without a predefined compound list — TARDIS is designed for targeted integration only.

## Inputs

- Centroided .mzML files (converted via MSConvert/ProteoWizard)
- Spectra objects loaded from .mzML files
- Target compound table (data.frame with columns: compound ID, Name, m/z, expected RT in minutes, ionization polarity)
- Adjusted retention time values from prior screening mode execution

## Outputs

- Results list object containing data.frame with AUC per target per run
- Tibble with average metrics (Max. Int., SNR, peak_cor, points_over_peak) for targets in QC runs
- EICs saved to output folder
- Tables for Max. Int., SNR, peak_cor, and points_over_peak metrics saved to output folder

## How to apply

Load centroided .mzML files as Spectra objects via the Spectra package, then execute the tardisPeaks function with screening_mode = FALSE to perform peak detection and integration across all runs. The function automatically applies polarity filtering based on your target compound table's ionization mode column. TARDIS returns a results list object containing: (1) a data.frame with AUC for each target in each run, (2) a tibble with average metrics (Max. Int., SNR, peak_cor, points_over_peak) for targets in QC runs, and (3) extracted ion chromatograms (EICs) saved to the output folder for visual inspection. Monitor for sawtooth peak profiles caused by filtering of empty spectra when using multiple overlapping m/z scan windows.

## Related tools

- **TARDIS** (Core package performing automated peak detection, integration, and quality metric calculation for targeted LC–MS compounds) — https://github.com/pablovgd/TARDIS
- **Spectra** (Loads centroided MS data as Spectra objects for input to TARDIS peak detection)
- **xcms** (Provides the established retention time correction algorithm underlying TARDIS alignment)
- **MSConvert (ProteoWizard)** (Converts raw LC–MS files to .mzML format and applies centroiding before TARDIS analysis)
- **R** (Programming environment for loading target tables, updating RT values, and executing TARDIS workflow) — https://cloud.r-project.org/index.html

## Examples

```
library(TARDIS); results <- tardisPeaks(spectra_obj, targets_df, screening_mode = FALSE, output_folder = './peak_results'); AUC_table <- results$AUC_data; QC_metrics <- results$qc_metrics
```

## Evaluation signals

- Results list object contains a data.frame with non-null AUC values for all targets across all 14+ runs, with no missing run entries.
- Returned tibble matches expected number of targets and QC runs; average metrics (Max. Int., SNR, peak_cor, points_over_peak) are numeric and within expected ranges for your compound class (e.g., SNR > 3 for well-integrated peaks).
- EICs saved to output folder are visually inspectable and show expected peak shapes without excessive sawtooth artifacts (or sawtooth is documented as expected given your scan-window configuration).
- Peak_cor values are close to 1.0 for high-quality peaks; values < 0.7 may indicate poor peak shape or coelution and should trigger manual review.
- Points_over_peak metric confirms adequate sampling: lower values may indicate sparse data or integration window misalignment relative to peak apex.

## Limitations

- Sawtooth peak profiles may occur due to filtering of empty spectra when using multiple overlapping m/z scan windows; this does not affect integration accuracy but affects visual inspection.
- Polarity filtering is automatic; if your target compound table contains incorrect ionization mode annotations, peaks may be missed or misattributed.
- RT adjustment is manual and must be validated via screening_mode before full-cohort analysis; incorrect RT values will lead to off-target integrations.
- TARDIS assumes .mzML format and centroided data; non-centroided or alternative formats will cause errors.

## Evidence

- [intro] Automated area under the peak and quality metrics: "`TARDIS` offers an easy and straightforward way to automatically calculate area under the peak, max intensity and various quality metrics for targeted chemical compounds in LC-MS data"
- [results] Results structure and output tables: "The `results` object is a `list` that contains a `data.frame` with the AUC of each target in each run and a `tibble` that contains a feature table with the average metrics for each target in the QC"
- [intro] Workflow transition from screening to full analysis: "Now we can perform peak detection in all our runs by setting `screening_mode = FALSE`"
- [intro] Input file format and preprocessing requirements: "Input files need to be converted to the .mzML format and have to be centroided"
- [intro] Sawtooth artifact from empty spectra filtering: "you will notice that peaks will have a sawtooth profile, because of the filtering of empty spectra within TARDIS"
- [readme] R version and BiocManager requirements: "For the latest version of `TARDIS`, `BiocManager` **version 3.20** is required"
