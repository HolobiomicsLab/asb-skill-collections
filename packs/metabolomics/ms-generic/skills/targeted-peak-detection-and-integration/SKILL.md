---
name: targeted-peak-detection-and-integration
description: Use when you have centroided LC–MS data in .mzML format, a validated table of target compounds with adjusted expected retention times (RT in minutes), and you need to extract peak areas and quality metrics across all sample runs.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_3520
  tools:
  - TARDIS
  - Spectra
  - R
  - MSConvert (ProteoWizard)
  - xcms
  - MsExperiment
  techniques:
  - mass-spectrometry
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
  - build: coll_tardis_cq
    doi: 10.1021/acs.analchem.5c00567
    title: tardis
  dedup_kept_from: coll_tardis_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c00567
  all_source_dois:
  - 10.1021/acs.analchem.5c00567
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Targeted Peak Detection and Integration

## Summary

Automated detection and integration of chromatographic peaks for known target compounds across multiple LC–MS runs, producing area-under-curve (AUC) and quality metrics (Max. Int., SNR, peak_cor, points_over_peak). This skill is applied after retention time adjustment to extract quantitative and qualitative peak characteristics across a batch of centroided .mzML files.

## When to use

Apply this skill when you have centroided LC–MS data in .mzML format, a validated table of target compounds with adjusted expected retention times (RT in minutes), and you need to extract peak areas and quality metrics across all sample runs. Use this after screening mode confirms target visibility within m/z and RT windows, or when your expected retention times have been refined based on pilot/screening results.

## When NOT to use

- Input data is in profile mode (not centroided) or in incompatible formats other than .mzML — convert or centroid first.
- Target compounds lack validated or refined expected retention times — run screening mode first to adjust RT windows before full-batch integration.
- Polarity information is not available in the target compound table — the function requires a column indicating ionization mode (positive/negative).

## Inputs

- Centroided .mzML LC–MS files (one or more sample runs)
- Spectra object(s) loaded from .mzML files via the Spectra package
- Target compound table (data.frame) with columns: compound ID, Name, m/z, expected RT (minutes), polarity or ionization mode

## Outputs

- List object containing data.frame with AUC values for each target in each run
- Tibble with average peak metrics (Max. Int., SNR, peak_cor, points_over_peak) for each target in QC runs
- Extracted Ion Chromatograms (EICs) saved to output folder
- Tables with Max. Int., SNR, peak_cor, and points_over_peak metrics saved to output folder

## How to apply

Load the target compound table with ID, Name, m/z, expected RT (in minutes), and polarity into R. Convert all raw MS data to centroided .mzML format using MSConvert (ProteoWizard). Load the .mzML files as Spectra objects via the Spectra package. Execute the tardisPeaks function with screening_mode = FALSE, providing the compound table and Spectra object as inputs. The function performs polarity filtering internally, detects peaks within the defined m/z and RT windows for each target, integrates peak areas, and calculates SNR, maximum intensity, peak correlation, and points over the peak. Collect the returned results list, which contains a data.frame with AUC for each target in each run and a tibble with average metrics across QC runs.

## Related tools

- **TARDIS** (Core R package that executes targeted peak detection, integration, and quality metric calculation on Spectra objects with screening_mode control) — https://github.com/pablovgd/TARDIS
- **Spectra** (Loads centroided MS data from .mzML files as Spectra objects for input to tardisPeaks)
- **MSConvert (ProteoWizard)** (Converts raw MS data to centroided .mzML format before Spectra import)
- **xcms** (Provides established retention time correction algorithm integrated into TARDIS)
- **MsExperiment** (Alternative input format to file paths for TARDIS (can be used instead of Spectra file paths))

## Examples

```
library(TARDIS); library(Spectra); targets <- data.frame(ID=c(1577,1583), Name=c('Compound_A','Compound_B'), mz=c(123.4, 234.5), RT=c(8.82, 4.0), polarity=c('pos','neg')); sps <- Spectra(c('run1.mzML','run2.mzML')); results <- tardisPeaks(targets, sps, screening_mode=FALSE, output_dir='./peaks_output')
```

## Evaluation signals

- Results list is non-empty and contains both a data.frame (AUC by target and run) and a tibble (average metrics for QC runs)
- AUC values are numeric, non-negative, and present for all targets in all runs; missing values indicate peaks not found or integration failures
- Quality metrics (Max. Int., SNR, peak_cor, points_over_peak) are present for each target; SNR > 3 is typical for acceptable peaks, peak_cor close to 1 indicates good peak shape fidelity
- EIC plots in the output folder show clean, unimodal peaks within expected RT windows; sawtooth profile is expected due to empty spectrum filtering in data with overlapping m/z scan windows
- Consistency check: QC run average metrics should be comparable across replicates; large variation suggests retention time drift or instrument instability

## Limitations

- Empty spectra filtering within TARDIS can produce sawtooth profiles in peak data when multiple overlapping m/z scan windows are present — this is expected and does not indicate failure.
- Peak detection success depends critically on accurate expected RT values; significant drift from true retention times will cause peaks to fall outside the search window and produce zero or missing AUC values.
- The function does not perform polarity subsetting on input files — polarity filtering is applied internally, so input Spectra objects should contain both positive and negative ionization data if both are present in the raw files.
- Timeout issues can occur during installation or data loading due to example data; increasing the R timeout setting (via options(timeout = '300')) may be necessary.

## Evidence

- [intro] Input files need to be converted to the .mzML format and have to be centroided: "Input files need to be converted to the .mzML format and have to be centroided"
- [intro] Following columns at least need to be present for each compound: A compound ID, a unique identifier, A compound Name, Theoretical or measured m/z, Expected RT (in minutes): "Following columns at least need to be present for each compound: A compound ID, a unique identifier, A compound Name, Theoretical or measured m/z, Expected RT (in minutes)"
- [intro] loads MS data as Spectra objects so it's easily integrated with other tools: "loads MS data as `Spectra` objects so it's easily integrated with other tools"
- [intro] Peak detection in all runs after screening mode adjustment: "Now we can perform peak detection in all our runs by setting `screening_mode = FALSE`"
- [results] The results object is a list containing a data.frame with the AUC of each target in each run and a tibble with average metrics for each target in the QC runs: "The `results` object is a `list` that contains a `data.frame` with the AUC of each target in each run"
- [results] Results include tables with metrics: Max. Int., SNR, peak_cor and points over the peak: "Other results include tables with the other metrics (Max. Int., SNR, peak_cor and points over the peak)"
- [intro] Polarity filtering is done within TARDIS, so no polarity subsetting has to be performed: "Polarity filtering is done within `TARDIS`, so no polarity subsetting has to be performed"
- [intro] Sawtooth profile in data with multiple overlapping m/z scan windows: "you will notice that peaks will have a sawtooth profile, because of the filtering of empty spectra within TARDIS"
- [readme] README installation instructions specify R version >= 4.4.0 and BiocManager version 3.20 required: "Make sure `R` (**version >= 4.4.0**) is installed on your computer"
- [readme] README notes connection timeout is often an issue for example data: "Since the package contains some example data, connection timeout is often an issue. You can increase your timeout setting in R using: options(timeout = "300")"
