---
name: targeted-metabolite-extraction
description: Use when you have centroided LC-MS data (.mzML format) and a curated
  list of targeted metabolites or lipids (with m/z, retention time, and polarity)
  that you want to quantify and quality-assess across multiple analytical runs, and
  you need both per-run AUC values and averaged QC metrics for each.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3704
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
  tools:
  - Spectra
  - xcms
  - R
  - knitr
  - kableExtra
  - TARDIS
  - ProteoWizard
  - MsExperiment
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
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

# targeted-metabolite-extraction

## Summary

Extract quantitative metrics (area under curve, max intensity, signal-to-noise ratio, peak correlation, and points over peak) for user-defined targeted compounds from centroided LC-MS data in .mzML format using the TARDIS tardisPeaks() function with screening_mode=FALSE. This skill automates peak detection and quality assessment across all runs after validating target visibility in a screening pass.

## When to use

Apply this skill when you have centroided LC-MS data (.mzML format) and a curated list of targeted metabolites or lipids (with m/z, retention time, and polarity) that you want to quantify and quality-assess across multiple analytical runs, and you need both per-run AUC values and averaged QC metrics for each target compound.

## When NOT to use

- Input files are not in centroided .mzML format — TARDIS requires centroided data and will not process profile-mode or unconverted raw formats.
- You only have untargeted metabolomics data and no predefined compound list — TARDIS is purpose-built for targeted analysis and requires a curated target list.
- You already have a pre-computed feature table with integrated peak areas — there is no need to re-extract and re-quantify.

## Inputs

- Centroided LC-MS data files in .mzML format
- Spectra object loaded from .mzML files
- Target list data.frame with columns: compound ID, name, m/z, retention time (minutes), polarity

## Outputs

- List object containing data.frame with per-target AUC values across all runs
- QC feature table tibble with average metrics (AUC, Max Intensity, SNR, peak_cor, points over peak) per target
- CSV files with per-metric tables exported to output directory
- Extracted ion chromatograms (EICs) saved to output folder for inspection

## How to apply

First, prepare input: convert raw LC-MS files to centroided .mzML format (e.g., using ProteoWizard MSConvert) and create a target list data.frame with compound ID, name, theoretical m/z, expected retention time in minutes, and polarity annotation. Load the mzML files as Spectra objects and apply retention-time correction using the xcms algorithm if needed (e.g., for targets with drift across runs). Execute tardisPeaks() with screening_mode=FALSE to perform peak detection across all runs; polarity filtering is applied automatically within TARDIS. Extract the resulting list object, which contains: a data.frame with AUC values per target per run, a tibble with average metrics (AUC, Max Intensity, SNR, peak_cor, points over peak) computed from QC runs, and per-metric CSV tables. Verify output by inspecting extracted ion chromatograms (EICs) saved to the output folder and checking that all targets produced valid peak detections.

## Related tools

- **TARDIS** (Primary R package that implements tardisPeaks() function for targeted peak detection, integration, and QC metric calculation in LC-MS data) — https://github.com/pablovgd/TARDIS
- **Spectra** (R/Bioconductor package for loading and representing LC-MS data as objects for input to TARDIS)
- **xcms** (Bioconductor package providing retention-time correction algorithm applied optionally before peak detection)
- **ProteoWizard** (MSConvert tool for converting raw LC-MS files to centroided .mzML format required by TARDIS)
- **MsExperiment** (Alternative input format (instead of file paths) for TARDIS peak detection)

## Examples

```
library(TARDIS); library(Spectra); spectra_obj <- Spectra(files=c('run1.mzML', 'run2.mzML')); targets <- data.frame(compound_id=c(1,2), name=c('metaboliteA', 'metaboliteB'), mz=c(200.05, 250.10), rt_min=c(5.2, 8.7), polarity=c(1,1)); results <- tardisPeaks(spectra=spectra_obj, targets=targets, screening_mode=FALSE, output_dir='./output')
```

## Evaluation signals

- All targets in the input list produce valid peak detections (non-zero AUC values) across sample runs and QC runs.
- EICs are successfully saved to the output folder and visual inspection confirms peak detection aligns with expected retention time and m/z windows for each target.
- QC feature table tibble contains averaged metrics (AUC, Max Intensity, SNR, peak_cor, points over peak) with values in expected ranges for your sample type (e.g., SNR > 3 for confident detections).
- Per-metric CSV files contain rows for all targets and columns for all analytical runs with no missing values (NaN/NA); numeric values are non-negative.
- Data.frame with per-run AUC values has dimensions matching (number of targets) × (number of analytical runs) with no NaN entries for successfully detected peaks.

## Limitations

- Requires input files to be in centroided .mzML format; profile-mode or non-standard formats will not be processed.
- Polarity filtering is automatic within TARDIS; users cannot override or manually adjust polarity assignments post hoc.
- Retention-time drift correction relies on the xcms algorithm; if xcms correction is inadequate for your data, targets may fail to integrate correctly.
- Peak detection performance depends on signal-to-noise ratio and peak resolution; low-abundance or co-eluting metabolites may not be reliably extracted.
- No changelog is available in the repository documentation, so users should verify version compatibility and breaking changes manually.

## Evidence

- [intro] Input files requirement: "Input files need to be converted to the .mzML format and have to be centroided"
- [intro] Target list format: "compound ID, a unique identifier; A compound Name; Theoretical or measured *m/z*; Expected RT (in minutes); A column that indicates the polarity"
- [intro] Peak detection mode execution: "perform peak detection in all our runs by setting `screening_mode = FALSE`"
- [results] Output data structures: "The `results` object is a `list` that contains a `data.frame` with the AUC of each target in each run"
- [results] QC metrics output: "a `tibble` that contains a feature table with the average metrics for each target in the QC runs"
- [results] Per-metric CSV tables: "Other results include tables with the other metrics (Max. Int., SNR, peak_cor and points over the peak)"
- [results] EIC output and inspection: "The resulting EICs are again saved in the output folder and can be inspected"
- [intro] Polarity handling: "Polarity filtering is done within `TARDIS`, so no polarity subsetting has to be performed"
- [intro] xcms retention-time correction: "It makes use of an established retention time correction algorithm from the `xcms` package"
- [intro] Spectra integration: "loads MS data as `Spectra` objects so it's easily integrated with other tools"
