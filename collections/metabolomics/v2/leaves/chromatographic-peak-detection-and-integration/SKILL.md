---
name: chromatographic-peak-detection-and-integration
description: 'Use when after loading centroided .mzML LC-MS data and defining a target
  list (compound ID, name, m/z, RT, polarity) when you need to: (1) automatically
  locate and integrate peaks for known compounds across multiple runs; (2) generate
  per-target and per-run quantitative metrics;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
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

# chromatographic-peak-detection-and-integration

## Summary

Automated detection and integration of chromatographic peaks in LC-MS data using TARDIS to generate targeted quantitative metrics (AUC, max intensity, SNR, peak_cor) and QC feature tables. This skill is essential for high-throughput metabolomics and lipidomics workflows where multiple compounds must be consistently quantified across sample runs.

## When to use

Apply this skill after loading centroided .mzML LC-MS data and defining a target list (compound ID, name, m/z, RT, polarity) when you need to: (1) automatically locate and integrate peaks for known compounds across multiple runs; (2) generate per-target and per-run quantitative metrics; (3) produce QC feature tables with average metrics for targets detected in QC runs; or (4) export extracted ion chromatograms (EICs) for visual inspection. Most relevant when screening_mode=FALSE (peak detection across all runs) rather than screening_mode=TRUE (visibility check only).

## When NOT to use

- Input data is already centroided and converted to .mzML format but you need profile-mode peak detection; TARDIS requires centroided input.
- You only need to verify target visibility within m/z and RT windows without quantification; use screening_mode=TRUE instead.
- Output is already a finalized feature table or the analysis does not require per-run metric tracking.

## Inputs

- Centroided .mzML LC-MS data files (loaded as Spectra objects)
- Target list data.frame with columns: compound ID, compound name, m/z, expected retention time (minutes), polarity

## Outputs

- data.frame with AUC values per target per run
- QC feature table tibble with average metrics (Max Intensity, SNR, peak_cor, points over peak) for each target in QC runs
- CSV files: one per metric (AUC, Max Intensity, SNR, peak_cor, points over peak) with all target-run values
- Extracted ion chromatograms (EICs) saved to output folder

## How to apply

Load centroided .mzML files into R using the Spectra package and construct a target data.frame with columns for compound ID, name, theoretical m/z, expected retention time (minutes), and polarity. Apply xcms retention-time correction algorithm to adjust RT windows if needed (e.g., for targets 1577 and 1583). Call tardisPeaks(screening_mode=FALSE) on the full dataset to perform peak detection across all runs; TARDIS automatically handles polarity filtering internally. Extract the results list, which contains: a data.frame with per-target AUC values across runs, a tibble with average metrics (Max Intensity, SNR, peak_cor, points over peak) for each target in QC runs, and individual CSV files for each metric. Write the QC feature table and metric CSVs to the output directory and verify that EICs have been saved for manual inspection. The rationale: automated integration with internal polarity filtering reduces manual curation overhead while standardizing metric calculation across samples.

## Related tools

- **TARDIS** (R package that performs automated peak detection, integration, and QC metric calculation for targeted LC-MS compounds with internal polarity filtering) — https://github.com/pablovgd/TARDIS
- **Spectra** (R package for loading and representing MS data as Spectra objects, enabling integration with TARDIS and other downstream tools)
- **xcms** (R package providing retention-time correction algorithm used to adjust RT windows for targets before peak detection)
- **MsExperiment** (Alternative R object format for organizing MS experimental metadata and spectra; can be used as input to TARDIS instead of file paths)

## Examples

```
library(TARDIS); library(Spectra); targets <- data.frame(ID=c(1577,1583), name=c('cpd_A','cpd_B'), mz=c(123.45,234.56), rt=c(5.2,6.1), polarity=c('+','+')); results <- tardisPeaks(files=mzML_paths, targets=targets, screening_mode=FALSE); write.csv(results$AUC, 'AUC.csv'); write.csv(results$QC_feature_table, 'QC_features.csv')
```

## Evaluation signals

- QC feature table tibble contains all targets with valid numeric values for Max Intensity, SNR, peak_cor, and points over peak; no missing or infinite values.
- Per-run AUC data.frame has one row per target and one column per run, with no NaN or negative AUC values.
- All exported CSV files have consistent row (target) and column (run) counts; row order matches the input target list.
- Extracted ion chromatograms (EICs) are visually inspectable and correspond to the m/z and RT windows specified in the target list; no EICs are missing or malformed.
- Peak integration produces non-zero AUC values for expected targets and zero or near-zero values only when peaks are genuinely absent within the defined windows.

## Limitations

- Input files must be pre-converted to centroided .mzML format; raw or non-centroided data will not be processed correctly.
- Retention-time correction requires a separate step using xcms; poor RT alignment can lead to missed or misaligned peak detection.
- Polarity filtering is automatic within TARDIS, but the target list must contain accurate polarity assignments (positive or negative) for each compound.
- Peak detection relies on user-defined m/z and RT windows; excessively wide windows may cause interference from coeluting compounds; excessively narrow windows may miss real peaks.
- No changelog is available in the repository, making it difficult to track breaking changes or bug fixes between versions.

## Evidence

- [intro] Input files need to be converted to the .mzML format and have to be centroided: "Input files need to be converted to the .mzML format and have to be centroided"
- [intro] Create target list data.frame with compound ID, name, m/z, RT, and polarity: "compound ID, a unique identifier; A compound Name; Theoretical or measured *m/z*; Expected RT (in minutes); A column that indicates the polarity"
- [results] tardisPeaks() with screening_mode=FALSE produces multiple output tables: "The `results` object is a `list` that contains a `data.frame` with the AUC of each target in each run"
- [results] QC feature table tibble with average metrics for each target in QC runs: "a `tibble` that contains a feature table with the average metrics for each target in the QC runs"
- [results] Other results include tables with metrics: Max. Int., SNR, peak_cor, and points over peak: "Other results include tables with the other metrics (Max. Int., SNR, peak_cor and points over the peak)"
- [intro] Polarity filtering is done within TARDIS automatically: "Polarity filtering is done within `TARDIS`, so no polarity subsetting has to be performed"
- [results] EICs are saved in the output folder and can be inspected: "The resulting EICs are again saved in the output folder and can be inspected"
- [intro] xcms retention time correction algorithm is used: "It makes use of an established retention time correction algorithm from the `xcms` package"
- [intro] loads MS data as Spectra objects for easy integration: "loads MS data as `Spectra` objects so it's easily integrated with other tools"
