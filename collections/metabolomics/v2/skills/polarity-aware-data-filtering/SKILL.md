---
name: polarity-aware-data-filtering
description: Use when when performing targeted peak detection on LC-MS data where compounds have been assigned expected ionization polarities (positive or negative mode) in the target list, and you want to prevent false peak assignments from the opposite polarity and avoid manual pre-filtering of raw data by.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_3520
  tools:
  - Spectra
  - xcms
  - R
  - knitr
  - kableExtra
  - TARDIS
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.5c00567
  title: tardis
evidence_spans:
- loads MS data as `Spectra` objects so it's easily integrated with other tools
- It makes use of an established retention time correction algorithm from the `xcms` package
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# polarity-aware-data-filtering

## Summary

Automatic filtering of LC-MS data by ionization polarity (positive/negative) within the TARDIS peak detection pipeline, ensuring that only targets matching their expected polarity are included in quantitative output. This eliminates the need for manual polarity subsetting before peak detection.

## When to use

When performing targeted peak detection on LC-MS data where compounds have been assigned expected ionization polarities (positive or negative mode) in the target list, and you want to prevent false peak assignments from the opposite polarity and avoid manual pre-filtering of raw data by polarity.

## When NOT to use

- Input data is already pre-filtered by polarity or contains only a single ionization mode — no polarity filtering is needed.
- Target list lacks a polarity annotation column — the filtering step cannot be applied without this metadata.
- Analysis goal is exploratory or untargeted discovery rather than targeted quantification — broad polarity filtering may discard relevant signals.

## Inputs

- target list data.frame with columns: compound ID, compound name, m/z, expected retention time (minutes), and polarity (positive/negative)
- LC-MS data in .mzML centroided format from multi-polarity acquisition

## Outputs

- Per-target AUC values across runs (filtered by matching polarity)
- QC feature table tibble with average metrics (Max Intensity, SNR, peak_cor, points over peak) for polarity-matched targets in QC runs
- Extracted ion chromatograms (EICs) for polarity-matched targets saved to output folder
- CSV files containing polarity-filtered metric tables

## How to apply

Ensure your target list data.frame includes a polarity column indicating the expected ionization mode (positive or negative) for each compound. During tardisPeaks() execution with screening_mode=FALSE, TARDIS automatically filters detected peaks by matching against this polarity annotation: only peaks from runs acquired in the matching polarity are retained in the output metrics (AUC, Max Intensity, SNR, peak_cor, points over peak) and QC feature tables. This is performed internally within TARDIS without requiring separate polarity subsetting of the raw data or .mzML files prior to analysis.

## Related tools

- **TARDIS** (Performs automatic polarity filtering internally during peak detection; user provides polarity annotations in target list) — https://github.com/pablovgd/TARDIS
- **Spectra** (Loads and represents LC-MS data as Spectra objects that retain polarity metadata for downstream TARDIS filtering)
- **xcms** (Provides retention-time correction algorithm that may be applied to targets before TARDIS polarity-aware peak detection)

## Examples

```
library(TARDIS); targets <- data.frame(compound_id=c(1577,1583), name=c('Target1','Target2'), mz=c(400.12,450.25), rt=c(5.2,6.8), polarity=c('positive','negative')); result <- tardisPeaks(files=mzML_paths, targets=targets, screening_mode=FALSE, output_dir='./results')
```

## Evaluation signals

- Output AUC, Max Intensity, and QC feature tables contain only compounds whose detected polarity matches the target list polarity annotation.
- No peaks or metrics appear in output for targets whose expected polarity was opposite to the run's acquisition mode.
- EIC files generated correspond only to polarity-matched target–run pairs; chromatograms from opposite-polarity runs are absent.
- Compare row counts and target presence in output CSVs before and after polarity filtering to confirm exclusion of off-polarity peaks.
- Verify that the target list polarity column is read and honored by tardisPeaks() via inspection of function logs or by confirming that manually pre-filtered (polarity-subset) input and automatic TARDIS filtering produce identical metric tables.

## Limitations

- Polarity filtering is applied only during peak detection (screening_mode=FALSE); screening mode does not apply polarity filtering.
- Requires accurate polarity metadata in the target list — missing or mislabeled polarity values will lead to incorrect exclusion or inclusion of peaks.
- No explicit control over polarity filtering intensity (e.g., soft vs. hard thresholds); filtering is binary — a peak either matches or does not match the target's expected polarity.
- Polarity filtering occurs after peak detection, not before; peaks may be detected and then discarded if they do not match polarity, which can waste computation on false peaks in high-noise regions.

## Evidence

- [intro] Polarity filtering is done within `TARDIS`, so no polarity subsetting has to be performed: "Polarity filtering is done within `TARDIS`, so no polarity subsetting has to be performed"
- [results] Polarity filtering applied automatically within TARDIS during peak detection: "polarity filtering applied automatically within TARDIS"
- [intro] A column that indicates the polarity: "A column that indicates the polarity"
- [intro] perform peak detection in all our runs by setting `screening_mode = FALSE`: "perform peak detection in all our runs by setting `screening_mode = FALSE`"
