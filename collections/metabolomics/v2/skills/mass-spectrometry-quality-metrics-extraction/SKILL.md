---
name: mass-spectrometry-quality-metrics-extraction
description: Use when you have centroided .mzML LC–MS data, a validated target compound
  list with adjusted expected retention times (e.g., after a screening mode run),
  and need to quantify peak quality and integration reliability across multiple sample
  runs to support metabolomics or lipidomics workflows.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - TARDIS
  - Spectra
  - R
  - xcms
  techniques:
  - LC-MS
  license_tier: restricted
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-quality-metrics-extraction

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Automated extraction of quantitative quality metrics (AUC, Max. Int., SNR, peak_cor, points_over_peak) for targeted chemical compounds from LC–MS data using TARDIS. This skill enables systematic assessment of peak detection reliability across multiple sample runs after retention time adjustment.

## When to use

Apply this skill when you have centroided .mzML LC–MS data, a validated target compound list with adjusted expected retention times (e.g., after a screening mode run), and need to quantify peak quality and integration reliability across multiple sample runs to support metabolomics or lipidomics workflows.

## When NOT to use

- Input files are not in centroided .mzML format; file conversion and centroiding must be completed first.
- Target compound list lacks adjusted retention times or was not validated through prior screening mode; execute screening_mode = TRUE first to identify correct RT windows.
- Data contains only profile-mode (non-centroided) spectra; TARDIS requires centroided input to avoid sawtooth profiles from overlapping m/z scan windows.

## Inputs

- Centroided .mzML files (LC–MS raw data)
- Spectra object (loaded via Spectra package)
- Target compound data.frame with columns: compound ID, Name, m/z, expected RT (minutes), polarity

## Outputs

- Results list object containing data.frame with AUC per target per run
- Tibble with average metrics (Max. Int., SNR, peak_cor, points_over_peak) per target in QC runs
- Tables saved to output folder: Max. Int., SNR, peak_cor, points_over_peak matrices
- Extracted Ion Chromatograms (EICs) saved to output folder

## How to apply

Load centroided .mzML files as Spectra objects using the Spectra package. Create or update a data.frame describing target compounds with columns for compound ID, Name, m/z, expected RT (in minutes), and polarity. Execute the tardisPeaks function with screening_mode = FALSE to perform peak detection and integration across all runs. The function automatically applies polarity filtering and outputs a results list containing a data.frame with AUC for each target in each run, a tibble with average metrics for QC runs, and separate tables for Max. Int., SNR, peak_cor, and points_over_peak saved to the output folder. Use the returned metrics to evaluate consistency and reliability of peak detection across the sample cohort.

## Related tools

- **TARDIS** (Primary peak detection, integration, and quality metrics computation engine; executes tardisPeaks function with specified screening_mode and polarity parameters) — https://github.com/pablovgd/TARDIS
- **Spectra** (Loads centroided .mzML files as Spectra objects for integration with TARDIS; provides data structure interface to mass spectrometry data)
- **xcms** (Supplies established retention time correction algorithm used within TARDIS for RT alignment)
- **R** (Runtime environment for TARDIS package, Spectra integration, and target compound table manipulation) — https://cloud.r-project.org/index.html

## Examples

```
library(TARDIS); library(Spectra); targets <- read.csv('targets_adjusted.csv'); sp <- readMsExperiment(files = list.files('mzML/', full.names=TRUE)); results <- tardisPeaks(Spectra = sp, targets = targets, screening_mode = FALSE, output_folder = './results/')
```

## Evaluation signals

- Results object is a list containing a data.frame with AUC values and a tibble with average metrics (no missing or malformed rows for valid targets).
- Output folder contains expected tables: Max. Int., SNR, peak_cor, points_over_peak matrices with dimensions matching number of targets × number of runs.
- AUC values are numeric and fall within expected range for integrated peak areas in the sample's m/z and RT domain.
- SNR values are positive and vary appropriately across runs and targets (high SNR for strong peaks, low for weak or absent peaks).
- EICs saved to output folder are visually inspectable and display expected peak shapes consistent with the adjusted retention times.

## Limitations

- Peaks in data with multiple overlapping m/z scan windows may display a sawtooth profile due to filtering of empty spectra within TARDIS; this is a known artifact of the data structure, not a quality failure.
- Polarity filtering is performed automatically within TARDIS; users cannot customize polarity thresholds—all targets must be assigned a polarity column value.
- Retention time adjustment must be performed prior to full-run execution; if expected RT values are incorrect, peak detection will fail silently or return zero/low metrics for affected targets.

## Evidence

- [results] describes_metrics_output: "TARDIS automatically calculates area under the peak, max intensity and various quality metrics for targeted chemical compounds in LC-MS data"
- [results] describes_results_list_structure: "The results object is a list containing a data.frame with the AUC of each target in each run and a tibble with average metrics for each target in the QC runs"
- [results] describes_additional_metrics_tables: "Other results include tables with the other metrics (Max. Int., SNR, peak_cor and points over the peak)"
- [intro] describes_screening_mode_prerequisite: "First, we perform a screening step to check if our targets are visible within our m/z and RT windows"
- [intro] describes_full_run_execution: "Now we can perform peak detection in all our runs by setting screening_mode = FALSE"
- [intro] describes_input_format_requirement: "Input files need to be converted to the .mzML format and have to be centroided"
- [intro] describes_polarity_filtering: "Polarity filtering is done within TARDIS, so no polarity subsetting has to be performed"
- [intro] describes_sawtooth_artifact: "you will notice that peaks will have a sawtooth profile, because of the filtering of empty spectra within TARDIS"
- [readme] describes_installation_r_requirement: "Make sure R (version >= 4.4.0) is installed on your computer"
- [readme] describes_gui_launch_method: "To launch the GUI in R: runTardis()"
