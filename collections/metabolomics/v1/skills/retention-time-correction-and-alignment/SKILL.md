---
name: retention-time-correction-and-alignment
description: Use when you have multiple LC-MS runs with the same set of targets (compounds) and observe or expect retention time drift or jitter between runs.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0121
  tools:
  - Spectra
  - xcms
  - R
  - knitr
  - kableExtra
  - TARDIS
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
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_tardis
    doi: 10.1021/acs.analchem.5c00567
    title: tardis
  dedup_kept_from: coll_tardis
schema_version: 0.2.0
---

# retention-time-correction-and-alignment

## Summary

Correct systematic shifts in retention times across LC-MS runs using established algorithms (e.g., from xcms) to ensure accurate target matching and downstream peak detection. This step is essential before targeted peak integration when retention time variability between runs could cause targets to fall outside their expected RT windows.

## When to use

Apply this skill when you have multiple LC-MS runs with the same set of targets (compounds) and observe or expect retention time drift or jitter between runs. Specifically, use it before running tardisPeaks() in peak detection mode (screening_mode=FALSE) if you have identified targets whose observed retention times deviate from the expected values—as demonstrated in the vignette where targets 1577 and 1583 required RT correction prior to full peak detection.

## When NOT to use

- Retention times are already well-aligned across runs (drift < acceptable tolerance for your RT window width).
- You are running tardisPeaks() in screening mode (screening_mode=TRUE) only, which does not require pre-corrected RTs.
- Input data is already a feature table or integrated peak table; RT correction applies to raw MS data.

## Inputs

- Spectra object(s) loaded from .mzML centroided LC-MS data
- target list data.frame with expected retention times (in minutes) per target
- identification of targets showing retention time drift across runs

## Outputs

- Spectra object(s) with corrected retention times applied
- corrected retention time values per target per run (ready for use in tardisPeaks())

## How to apply

Load your MS data (e.g., from .mzML centroided files) as Spectra objects using the Spectra package. Identify targets with observed retention time deviations from their theoretical expected values. Apply the xcms retention-time correction algorithm to align retention times across runs using these targets as anchors. The corrected retention times are then used by tardisPeaks() to ensure that the peak detection window (m/z and RT bounds) correctly captures each target in all runs. The rationale is that accurate RT alignment reduces false negatives (missed peaks) when targets fall outside their search windows due to drift, and improves the reliability of per-target AUC and quality metrics downstream.

## Related tools

- **xcms** (Provides the retention-time correction algorithm for aligning RT across LC-MS runs)
- **Spectra** (Loads and manages MS data objects in R; works with corrected retention times)
- **TARDIS** (Downstream peak detection function (tardisPeaks) consumes corrected RT values) — https://github.com/pablovgd/TARDIS

## Examples

```
# Load LC-MS data and apply xcms RT correction before tardisPeaks
library(Spectra)
library(TARDIS)
sp <- Spectra::readMsExperiment(files = c('run1.mzML', 'run2.mzML', 'run3.mzML'))
# Correct RTs using xcms (details via TARDIS vignette or xcms documentation)
# Then invoke: results <- tardisPeaks(sp, targets=target_df, screening_mode=FALSE)
```

## Evaluation signals

- Corrected retention times for targets across all runs fall within or closer to their expected RT windows (compare before/after distributions).
- tardisPeaks() in peak detection mode (screening_mode=FALSE) successfully detects peaks for all targets that were visible in screening mode—no targets are lost due to RT drift.
- Per-target AUC and QC metrics (SNR, peak_cor, Max Intensity) are stable and non-zero across runs, indicating consistent peak capture.
- Extracted ion chromatograms (EICs) saved by tardisPeaks() show well-aligned peaks across runs, with no chromatographic features shifted outside their search windows.
- No systematic bias in peak detection: the number of detected peaks per target does not correlate with run order or instrument drift.

## Limitations

- The xcms retention-time correction algorithm requires at least a small set of reliably detected anchor targets across all runs; if too few targets are present or detectable, alignment may be unreliable.
- RT correction is sensitive to the choice of alignment algorithm parameters; tuning may be required for different LC methods or sample types.
- If retention time variability is caused by non-systematic sources (e.g., column degradation, temperature fluctuations during run), correction may be incomplete or mask underlying instrumental issues.
- The vignette does not report a quantitative threshold for 'acceptable' RT drift; practitioners must define this based on their RT window width and tolerance.

## Evidence

- [results] xcms retention-time correction and alignment: "Adjust retention times for targets 1577 and 1583 using the xcms retention-time correction algorithm."
- [intro] RT correction improves peak detection coverage: "It makes use of an established retention time correction algorithm from the `xcms` package"
- [results] corrected RT values feed into tardisPeaks: "Execute tardisPeaks() with screening_mode=FALSE to perform peak detection across all runs with polarity filtering applied automatically within TARDIS."
- [intro] Spectra objects as input container: "loads MS data as `Spectra` objects so it's easily integrated with other tools"
- [intro] RT correction is a standard preprocessing step: "perform a screening step to check if our targets are visible within our *m/z* and RT windows"
