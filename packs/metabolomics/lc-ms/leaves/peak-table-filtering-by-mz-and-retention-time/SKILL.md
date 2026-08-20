---
name: peak-table-filtering-by-mz-and-retention-time
description: Use when you have a table of detected chromatographic peaks (e.g., from CentWave peak detection in xcms) and need to isolate a single target m/z (e.g., m/z 304.1131 for a pesticide) or a narrow m/z range, or when you must restrict analysis to a known retention time window (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0121
  tools:
  - MsFeatures
  - Spectra
  - MsBackendMgf
  - MetaboCoreUtils
  - xcms
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/ac051437y
  title: XCMS
evidence_spans:
- General MS feature grouping functionality if defined by the `r Biocpkg("MsFeatures")` package
- library(Spectra)
- library(MsBackendMgf)
- '%\VignetteDepends{xcms,MsDataHub,BiocStyle,pander,Spectra,MsBackendMgf,MetaboCoreUtils}'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_xcms
    doi: 10.1021/ac051437y
    title: XCMS
  dedup_kept_from: coll_xcms
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/ac051437y
  all_source_dois:
  - 10.1021/ac051437y
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# peak-table-filtering-by-mz-and-retention-time

## Summary

Filter LC-MS chromatographic peaks by m/z and retention time windows to isolate target analytes or remove interfering signals before downstream analysis. This skill selects a subset of detected peaks matching exact mass and temporal criteria, reducing computational load and background noise in spectral matching and feature grouping workflows.

## When to use

Apply this skill when you have a table of detected chromatographic peaks (e.g., from CentWave peak detection in xcms) and need to isolate a single target m/z (e.g., m/z 304.1131 for a pesticide) or a narrow m/z range, or when you must restrict analysis to a known retention time window (e.g., 230–610 seconds) to focus on a region of interest or remove co-eluting interference.

## When NOT to use

- Input is already a feature table or MS2 spectrum—filtering is most useful on raw chromatographic peak tables, not on consensus spectra or post-grouping feature summaries.
- Your analysis requires untargeted discovery across the full m/z–rt plane; restrictive filtering may eliminate unexpected or unexpected compounds of interest.
- Retention time or m/z range is unknown or very broad (>100 ppm or >60 seconds); filtering becomes ineffective and you should use subsequent annotation steps instead.

## Inputs

- XcmsExperiment or OnDiskMSnExp object with detected chromatographic peaks (from findChromPeaks)
- target m/z value (numeric, e.g., 304.1131)
- ppm tolerance (numeric, e.g., 10–20)
- optional: retention time range [rt_min, rt_max] in seconds

## Outputs

- filtered XcmsExperiment or OnDiskMSnExp object containing only peaks within the specified m/z and/or retention time window
- chromPeaks table (matrix or data.frame) with columns: mz, mzmin, mzmax, rt, rtmin, rtmax, into, intb, maxo, sn

## How to apply

Use chromPeaks() with mz and ppm parameters to filter peaks by mass-to-charge ratio with a specified mass accuracy tolerance (e.g., 20 ppm), or use filterRt() to restrict the data object to a retention time range before peak extraction. The ppm tolerance should be set based on your instrument's mass accuracy—10–20 ppm is typical for high-resolution instruments. For isolation of a single peak, calculate the target m/z range as [mz - (mz × ppm / 1e6), mz + (mz × ppm / 1e6)]. Combine m/z and retention time filters sequentially if both constraints apply. Validate that the filtered result contains the expected number of peaks and that signal intensity is retained at the target m/z-rt location.

## Related tools

- **xcms** (provides chromPeaks() and filterRt() methods for mass-accuracy and retention-time filtering of chromatographic peak tables) — https://github.com/sneumann/xcms
- **Spectra** (filters extracted MS2 spectra by retention time and MS level after peak detection)

## Examples

```
chromPeaks(dda_data, mz = 304.1131, ppm = 20); dda_data_filtered <- filterRt(dda_data, rt = c(230, 610))
```

## Evaluation signals

- Filtered peak table contains only peaks with m/z within [target_mz - (target_mz × ppm / 1e6), target_mz + (target_mz × ppm / 1e6)]
- All peaks in filtered result have rt within the specified [rt_min, rt_max] window (if retention time filter applied)
- Number of filtered peaks is ≤ number of input peaks; verify no unexpected peaks are retained due to rounding or tolerance miscalculation
- Chromatographic peak signal (intensity, 'into' column) is preserved and non-zero for the target peak
- Downstream spectral matching against reference compounds (Flumazenil, Fenamiphos) shows expected similarity scores and correct compound identification

## Limitations

- Mass accuracy tolerance (ppm) must be set appropriately for your instrument; setting ppm too large may capture off-target peaks, too small may exclude true signals due to calibration drift.
- Retention time filtering assumes reproducible chromatography; large shifts between samples or runs may cause correct peaks to fall outside the specified window.
- Filtering does not perform gap-filling; samples in which no chromatographic peak was detected at the target m/z–rt location will not be recovered by this step alone.
- m/z filtering is sensitive to isotope and adduct form; if your target is [M+H]+ but signal appears as [M+Na]+, filters on nominal m/z will miss the peak.

## Evidence

- [methods] Filter by m/z: "Filter chromatographic peaks by m/z using chromPeaks() with mz and ppm parameters"
- [methods] Filter by retention time: "Filter data to retention time range using filterRt()"
- [intro] Example m/z filtering in context: "chromPeaks(dda_data, mz = ex_mz, ppm = 20)"
- [intro] Example retention time filtering in context: "We thus filter the DDA data to this retention time range. dda_data <- filterRt(dda_data, rt = c(230, 610))"
- [intro] Purpose in workflow context: "Spectra for identified chromatographic peaks can be extracted with the `chromPeakSpectra()` method."
