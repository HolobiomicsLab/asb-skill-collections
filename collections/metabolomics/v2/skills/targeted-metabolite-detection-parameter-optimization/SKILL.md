---
name: targeted-metabolite-detection-parameter-optimization
description: Use when when you have centroided .mzML LC–MS runs and a target list
  (compound ID, theoretical m/z, expected RT, polarity) but are uncertain whether
  your m/z and RT windows are wide enough to capture all targets without false positives.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3645
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  tools:
  - TARDIS
  - Spectra
  - xcms
  - R
  - MsExperiment
  - knitr
  - ProteoWizard (MSConvert)
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1021/acs.analchem.5c00567
  title: tardis
evidence_spans:
- R package for *TArgeted Raw Data Integration In Spectrometry*
- loads MS data as `Spectra` objects so it's easily integrated with other tools
- It makes use of an established retention time correction algorithm from the `xcms`
  package
- Alternatively, instead of using file paths as input for TARDIS, the user can also
  use an `MsExperiment` object
- knitr::include_graphics
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

# Targeted metabolite detection parameter optimization

## Summary

Systematic evaluation and refinement of m/z tolerance windows and retention time (RT) windows to maximize targeted compound visibility and peak detection sensitivity in LC–MS screening workflows. This skill validates detection parameters before committing computational resources to full-batch peak integration.

## When to use

When you have centroided .mzML LC–MS runs and a target list (compound ID, theoretical m/z, expected RT, polarity) but are uncertain whether your m/z and RT windows are wide enough to capture all targets without false positives. Apply this skill before running full peak detection in production mode to verify that target compounds are visible within your chosen parameter ranges across a representative batch of runs.

## When NOT to use

- Input files are not centroided or are in non-mzML format (must convert with MSConvert/ProteoWizard first)
- Target list is missing theoretical m/z or expected RT values
- Analysis goal is hypothesis-free, untargeted peak discovery (use untargeted xcms workflow instead)
- You already have validated, production-ready parameter sets from prior method development and only need to apply them to a new batch (skip screening and use screening_mode=FALSE directly)

## Inputs

- Centroided .mzML LC–MS run files (14+ runs recommended for batch assessment)
- Target list data.frame with columns: compound ID, compound name, theoretical m/z, expected RT (minutes), ionization polarity
- Output directory path for diagnostic QC plots

## Outputs

- Extracted ion chromatogram (EIC) PNG plots for each target, saved to output/screening/Diagnostic_QCs_*/ folder
- Data.frame or tibble with screening metrics per target: Max. Int., SNR, peak_cor, points over the peak
- Average feature metrics table summarizing QC run performance across all targets

## How to apply

Execute tardisPeaks() with screening_mode=TRUE on your LC–MS runs and target list to perform an initial screening step that checks if each target is visible within your specified m/z and RT windows. The function automatically applies polarity filtering during screening. Inspect the resulting extracted ion chromatogram (EIC) plots saved to the diagnostic output folder for each of your 10 targets (or your full target set). For each target, visually confirm (1) that the expected peak appears within the RT window and (2) that no major interference or baseline distortion occurs. Measure signal-to-noise ratio (SNR), peak correlation (peak_cor), and point density (points over the peak) from the screening results. If any target shows SNR below acceptable threshold, peak_cor indicating poor integration, or too few points defining the peak, widen the m/z or RT window incrementally and re-screen. Once all targets show acceptable visibility and metrics, proceed to screening_mode=FALSE for full peak detection and quantification.

## Related tools

- **TARDIS** (Core R package that executes tardisPeaks() screening mode to detect and visualize target compound visibility within m/z and RT windows) — https://github.com/pablovgd/TARDIS
- **xcms** (Underlying retention time correction and peak detection algorithm employed by TARDIS)
- **Spectra** (R package that loads and represents MS data as Spectra objects for integration with TARDIS)
- **MsExperiment** (Alternative input container for TARDIS; allows user to provide pre-loaded MS experiment object instead of file paths)
- **ProteoWizard (MSConvert)** (File conversion tool to prepare raw MS data in centroided .mzML format required by TARDIS)
- **knitr** (R package for embedding and rendering diagnostic plots in screening output reports)

## Examples

```
library(TARDIS); results <- tardisPeaks(ms_runs = list.files('data/', pattern='\.mzML$'), target_list = targets_df, output_folder = 'output/screening/', screening_mode = TRUE)
```

## Evaluation signals

- All 10 targets (or full target set) appear as distinct peaks in their respective EIC plots within the defined m/z and RT windows
- SNR metric for each target exceeds a minimum acceptable threshold (threshold should be defined based on your assay sensitivity requirement; no single threshold is universal)
- Peak correlation (peak_cor) metric indicates well-integrated peaks without significant baseline noise or peak shape distortion
- Point density ('points over the peak') is sufficient to define peak shape accurately (typically ≥5–10 points minimum per peak)
- No major co-eluting interference or loss of signal observed in QC run diagnostic plots when compared to expected retention time

## Limitations

- Screening mode provides only visibility assessment and does not perform absolute peak area quantification; full quantitative metrics require screening_mode=FALSE
- EIC inspection is qualitative and relies on manual visual judgment; SNR and peak_cor thresholds must be set by the user based on assay requirements and are not automatically determined
- Polarity filtering is performed automatically within TARDIS but requires accurate polarity annotation in the target list; incorrect polarity assignments will cause targets to be missed
- Screening workflow assumes well-separated chromatographic peaks; highly overlapping co-eluting metabolites may not be resolved even with optimized windows
- Input data must be centroided; profile (non-centroided) data will not function correctly and will produce degraded EIC quality

## Evidence

- [intro] perform a screening step to check if our targets are visible within our m/z and RT windows: "perform a screening step to check if our targets are visible within our *m/z* and RT windows"
- [intro] Polarity filtering is done within TARDIS, so no polarity subsetting has to be performed: "Polarity filtering is done within `TARDIS`, so no polarity subsetting has to be performed"
- [intro] Input files need to be converted to the .mzML format and have to be centroided: "Input files need to be converted to the .mzML format and have to be centroided"
- [results] The resulting EICs are again saved in the output folder and can be inspected: "The resulting EICs are again saved in the output folder and can be inspected"
- [results] Other results include tables with the other metrics (Max. Int., SNR, peak_cor and points over the peak): "Other results include tables with the other metrics (Max. Int., SNR, peak_cor and points over the peak)"
- [other] tardisPeaks() in screening mode generates EIC plots for all 10 targets that are saved to the output folder and can be inspected: "tardisPeaks() in screening mode generates EIC plots for all 10 targets that are saved to the output folder and can be inspected"
- [intro] automatically calculate area under the peak, max intensity and various quality metrics for targeted chemical compounds in LC-MS data: "automatically calculate area under the peak, max intensity and various quality metrics for targeted chemical compounds in LC-MS data"
