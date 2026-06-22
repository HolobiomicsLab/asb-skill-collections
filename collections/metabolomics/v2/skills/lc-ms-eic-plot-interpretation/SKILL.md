---
name: lc-ms-eic-plot-interpretation
description: Use when after executing TARDIS in screening_mode = TRUE on centroided .mzML files with a defined target compound list.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - TARDIS
  - Spectra
  - R
  - xcms
  techniques:
  - LC-MS
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

# LC-MS EIC Plot Interpretation

## Summary

Visual inspection and validation of extracted ion chromatogram (EIC) plots to confirm successful target detection, peak localization within expected m/z and retention time windows, and integration quality in targeted LC-MS metabolomics workflows. This skill bridges automated peak detection (via TARDIS) and quality assessment by examining diagnostic EIC plots for visibility, correct elution timing, and peak morphology.

## When to use

After executing TARDIS in screening_mode = TRUE on centroided .mzML files with a defined target compound list. Use this skill when you need to verify that all target compounds are visually detectable within their specified m/z and retention time windows before committing to full-run peak detection and quantification. Critical for validating window parameters and identifying compounds that elute at retention time boundaries (e.g., early or late elution requiring window adjustment).

## When NOT to use

- Input is already a feature table or quantification results table — interpretation applies to raw EIC plots, not aggregated data.
- Screening mode has not been executed or EIC plot files are not available — this skill requires diagnostic visual outputs from TARDIS.
- Data are in profile (not centroided) mode or in non-mzML formats — TARDIS screening_mode requires centroided .mzML input.

## Inputs

- TARDIS screening_mode output folder containing diagnostic EIC plots (images or .pdf files)
- Target compound metadata data.frame with columns: compound ID, Name, theoretical m/z, expected retention time (minutes), ionization polarity
- Centroided .mzML LC-MS data files (already processed by TARDIS Spectra object loading)

## Outputs

- Visual assessment report documenting presence/absence and localization of each target EIC within m/z and RT windows
- List of targets requiring m/z or retention time window adjustment before full quantification
- Confirmation that all 10 targets are visible and correctly localized (or identification of problematic targets)

## How to apply

Load and examine the diagnostic EIC plots saved by TARDIS in the screening output folder. For each of the 10 (or N) target compounds, visually confirm: (1) the target signal is present and distinguishable from baseline noise within the defined m/z tolerance window; (2) the peak elutes within the expected retention time window, noting compounds that elute toward window edges (e.g., targets 1577 and 1583); (3) peak morphology is consistent with a single, well-integrated peak (not split or heavily distorted by instrument scan patterns). Document any targets with missing or mislocalized signals as requiring window parameter re-optimization. This visual triage prevents wasteful full-run quantification on poorly parameterized targets and informs retention time correction calibration.

## Related tools

- **TARDIS** (Generates diagnostic EIC plots in screening_mode and performs automated polarity filtering and empty spectra removal; user interprets output plots to validate target detection and window parameters) — https://github.com/pablovgd/TARDIS
- **Spectra** (Loads centroided .mzML MS data as objects for TARDIS processing; enables polarity and spectrum metadata filtering upstream of EIC plot generation)
- **xcms** (Provides retention time correction algorithm integrated into TARDIS; supports validation of expected retention times used in EIC window definitions)

## Examples

```
# After TARDIS screening_mode = TRUE execution:
# Visually inspect EIC plots in output folder; verify all targets present within m/z ± tolerance and expected RT; document targets with edge elution (e.g., 1577, 1583) for window refinement.
```

## Evaluation signals

- All 10 target compounds are visually present in their corresponding EIC plots with signal-to-baseline ratio sufficient to distinguish peak from noise.
- Each target peak is localized within ±tolerance of its expected m/z and retention time window; compounds eluting at window edges are flagged for parameter review.
- Peak morphology is single, well-defined (not split or sawtooth-distorted); sawtooth patterns indicate empty spectra were not fully filtered by TARDIS.
- No targets are missing or completely absent from plots — if absent, confirm target is in the input data.frame and ionization polarity is correct.
- Retention time localization is reproducible across replicate runs or QC samples (if available) — large shifts between runs suggest RT correction calibration is needed.

## Limitations

- Visual interpretation is subjective and may vary by analyst; no quantitative acceptance criteria are specified in the article. Peak visibility depends on compound ionization efficiency and instrument sensitivity, not only window parameters.
- Sawtooth peak profiles may occur in data with multiple overlapping m/z scan windows even after TARDIS empty spectra filtering, complicating visual assessment of peak integration quality.
- EIC plot resolution and dynamic range settings (not detailed in the article) affect visibility of low-abundance targets; plots must be examined at consistent zoom/contrast to enable fair comparison.
- Screening mode validates target detection in a subset of runs; full quantification may still fail if target signals drop below detection limit in some samples or QC runs are not included.

## Evidence

- [other] The screening mode run with tardisPeaks produced diagnostic EIC plots showing successful detection and integration for all 10 targets: "The screening mode run with tardisPeaks produced diagnostic EIC plots showing successful detection and integration for all 10 targets, with visual confirmation that targets 1577 and 1583 elute toward"
- [intro] First, we perform a screening step to check if our targets are visible within our m/z and RT windows: "First, we perform a screening step to check if our targets are visible within our *m/z* and RT windows"
- [other] Inspect the resulting EIC plots saved in the screening output folder to verify each target is visible and correctly localized within its m/z and retention-time window: "Inspect the resulting EIC plots saved in the screening output folder to verify each target is visible and correctly localized within its m/z and retention-time window."
- [results] The resulting EICs are again saved in the output folder and can be inspected: "The resulting EICs are again saved in the output folder and can be inspected"
- [intro] you will notice that peaks will have a sawtooth profile, because of the filtering of empty spectra within TARDIS: "you will notice that peaks will have a sawtooth profile, because of the filtering of empty spectra within TARDIS"
