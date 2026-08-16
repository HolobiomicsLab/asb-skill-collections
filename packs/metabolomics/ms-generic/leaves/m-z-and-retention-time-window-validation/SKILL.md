---
name: m-z-and-retention-time-window-validation
description: Use when before committing to full-scale targeted peak integration across all LC–MS runs in a metabolomics or lipidomics study. Apply this skill when you have a curated list of 5–50+ target compounds with theoretical m/z values and expected retention times, centroided .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
  tools:
  - TARDIS
  - Spectra
  - R
  - xcms
  - MSConvert (ProteoWizard)
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
- It makes use of an established retention time correction algorithm from the `xcms` package
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

# m/z and retention time window validation

## Summary

A screening-mode quality-assurance step that verifies targeted compounds are detectable within their specified mass-to-charge and retention-time windows before full peak integration. This skill catches off-target elution, m/z drift, and integration parameter misspecifications early, preventing wasted processing on misconfigured targets.

## When to use

Before committing to full-scale targeted peak integration across all LC–MS runs in a metabolomics or lipidomics study. Apply this skill when you have a curated list of 5–50+ target compounds with theoretical m/z values and expected retention times, centroided .mzML data is available, and you need visual confirmation that targets actually appear within the chromatographic and mass windows you intend to use for automated integration.

## When NOT to use

- Input .mzML files are not centroided (use MSConvert or similar preprocessing first).
- Target compound list is incomplete or lacks retention-time estimates (screening requires both m/z and RT anchors).
- Data has already been processed through full integration; screening is a pre-integration QA step, not a post-hoc validation tool.

## Inputs

- Centroided .mzML files (one or more LC–MS runs)
- Data.frame with columns: compound ID, compound Name, theoretical m/z, expected retention time (minutes), ionization polarity (positive/negative)

## Outputs

- Diagnostic EIC (extracted ion chromatogram) plots for each target, saved to screening output folder
- Visual confirmation of target detectability and localization within m/z and retention-time windows

## How to apply

Prepare a data.frame with columns for compound ID, Name, theoretical m/z, expected retention time (in minutes), and ionization polarity (positive or negative). Load centroided .mzML files as Spectra objects in R. Execute the TARDIS function with screening_mode = TRUE, passing the target data.frame and file paths; TARDIS automatically applies polarity filtering and removes empty spectra to avoid sawtooth artifacts. Inspect the resulting EIC plots saved in the screening output folder for each target: verify visual presence within its m/z and retention-time window, check for unexpected peak shapes or background, and confirm that compounds eluting near retention-time window edges (e.g., targets 1577, 1583) are still within acceptable bounds. Adjust m/z tolerance, retention-time window half-width, or polarity assignments based on findings before running full integration with screening_mode = FALSE.

## Related tools

- **TARDIS** (Primary R package for targeted peak integration; executes screening mode with polarity filtering and EIC generation) — https://github.com/pablovgd/TARDIS
- **Spectra** (R package for loading and managing centroided MS data as objects compatible with TARDIS)
- **xcms** (Provides retention-time correction and peak-detection algorithms integrated into TARDIS workflow)
- **MSConvert (ProteoWizard)** (File conversion and centroiding of raw MS data to .mzML format required for input)

## Examples

```
library(TARDIS); targets_df <- data.frame(ID=1:10, Name=c('Comp1','Comp2',...), mz=c(100.05,120.08,...), RT=c(2.5,3.1,...), polarity=c('pos','neg',...)); results <- tardisPeaks(targets_df, files=c('sample1.mzML','sample2.mzML'), screening_mode=TRUE, output_folder='screening_results/')
```

## Evaluation signals

- All 10+ target compounds appear as discrete peaks in their respective EIC plots within the specified m/z and retention-time windows.
- Compounds eluting near retention-time window edges are still visually present and not truncated by window boundaries.
- No unexpected satellite peaks or integration artifacts appear in diagnostic plots; background signal is low relative to target peak height.
- Polarity filtering correctly segregates positive and negative ionization runs; no targets appear in the wrong polarity EIC.
- After screening adjustments, full integration with screening_mode = FALSE produces area-under-curve (AUC) and signal-to-noise ratio (SNR) metrics for all targets without missing-data or integration failures.

## Limitations

- Screening mode requires accurate prior knowledge of expected retention times; if RT estimates are off by >±1 minute, targets may not be detected within the specified window.
- Empty spectra are filtered out by TARDIS to prevent sawtooth profiles, which can distort peak area and intensity metrics in data with multiple overlapping m/z scan windows.
- Screening is qualitative (visual inspection of EICs); it does not produce quantitative metrics (AUC, SNR, peak correlation) until full integration is run.
- No automated changelog or version history is provided in the current TARDIS package, making it difficult to track parameter changes or diagnose historical screening failures across project iterations.

## Evidence

- [intro] Screening-mode function and polarity filtering: "First, we perform a screening step to check if our targets are visible within our *m/z* and RT windows"
- [intro] Data preparation for screening: "Following columns at least need to be present for each compound: A compound ID, a unique identifier, A compound Name, Theoretical or measured *m/z*, Expected RT (in minutes), A column that indicates"
- [intro] Polarity filtering automation: "Polarity filtering is done within `TARDIS`, so no polarity subsetting has to be performed"
- [results] EIC output and visual inspection: "The resulting EICs are again saved in the output folder and can be inspected"
- [other] Specific task finding on 10 targets: "The screening mode run with tardisPeaks produced diagnostic EIC plots showing successful detection and integration for all 10 targets, with visual confirmation that targets 1577 and 1583 elute toward"
- [intro] Empty spectra filtering rationale: "you will notice that peaks will have a sawtooth profile, because of the filtering of empty spectra within TARDIS"
