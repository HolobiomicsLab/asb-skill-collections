---
name: chromatographic-peak-extraction-and-retention-time-filtering
description: Use when when you have LC-MS/MS raw data (mzML or netCDF format) and
  need to isolate a specific compound's signal based on its known or suspected m/z
  value and retention time range.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - MsBackendMgf
  - MsFeatures
  - xcms
  - Spectra
  - MsExperiment
  techniques:
  - LC-MS
  - GC-MS
  license_tier: open
derived_from:
- doi: 10.1021/ac051437y
  title: XCMS
evidence_spans:
- library(MsBackendMgf)
- General MS feature grouping functionality if defined by the `r Biocpkg("MsFeatures")`
  package with additional functionality being implemented
- VignetteDepends{xcms,BiocStyle,faahKO,pheatmap,MsFeatures}
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_xcms_cq
    doi: 10.1021/ac051437y
    title: XCMS
  dedup_kept_from: coll_xcms_cq
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

# chromatographic-peak-extraction-and-retention-time-filtering

## Summary

Extract chromatographic peaks at specified m/z values from LC-MS/MS raw data after filtering to a defined retention time window. This skill reduces data complexity and focuses downstream analysis on compounds of interest by isolating signals in time and mass space.

## When to use

When you have LC-MS/MS raw data (mzML or netCDF format) and need to isolate a specific compound's signal based on its known or suspected m/z value and retention time range. Use this skill when you want to reduce noise and background, focus on a particular chromatographic peak for annotation, or extract all MS2 spectra associated with a single detected peak.

## When NOT to use

- Input is already a feature table or peak matrix (peaks have already been detected and grouped)
- You are performing untargeted feature detection across the entire m/z and RT space (use centWave peak picking instead)
- Raw data is in GC-MS format without LC separation dimension (RT filtering is less meaningful)

## Inputs

- LC-MS/MS raw data file (mzML or netCDF format)
- retention time range (numeric pair in seconds, e.g., c(230, 610))
- target m/z value (numeric)
- mass tolerance (numeric, in ppm; e.g., 20)

## Outputs

- Filtered XcmsExperiment or MsExperiment object with RT-restricted data
- Chromatographic peak table (chromPeaks) with m/z, retention time, and intensity for peaks matching the query
- MS2 spectra (Spectra object) associated with extracted chromatographic peak(s)

## How to apply

First, load the raw LC-MS/MS data into xcms using readMSData() or filterRt() to restrict analysis to your retention time window of interest (e.g., 230–610 seconds). Then use chromPeaks() with mz and ppm parameters to extract all detected chromatographic peaks within your target m/z range (e.g., m/z 304.1131 ± 20 ppm tolerance). The ppm tolerance accounts for instrument mass accuracy; tighter tolerances require more accurate instrumentation. Finally, retrieve all associated MS2 fragmentation spectra using chromPeakSpectra() at msLevel=2 to obtain the fragmentation patterns for subsequent annotation or consensus spectrum construction. The rationale is that filtering temporally and spectrally reduces computational burden and prevents false matches to contaminants or co-eluting compounds.

## Related tools

- **xcms** (Primary R package providing filterRt(), chromPeaks(), and chromPeakSpectra() functions for retention time filtering and chromatographic peak extraction) — https://github.com/sneumann/xcms
- **Spectra** (Stores and manages MS/MS fragmentation spectra objects returned by chromPeakSpectra()) — https://github.com/RforMassSpectrometry/Spectra
- **MsExperiment** (Container for raw LC-MS/MS data and metadata; works with xcms version 4+) — https://github.com/RforMassSpectrometry/MsExperiment
- **MsFeatures** (Optional downstream package for feature grouping after peak extraction) — https://github.com/RforMassSpectrometry/MsFeatures

## Examples

```
dda_data <- filterRt(dda_data, rt = c(230, 610)); peaks <- chromPeaks(dda_data, mz = 304.1131, ppm = 20); spectra_ms2 <- chromPeakSpectra(dda_data, msLevel = 2)
```

## Evaluation signals

- Returned chromPeaks table contains only peaks with m/z within specified tolerance (e.g., 304.1131 ± 20 ppm = 304.0997–304.1265) and RT within filtered range (230–610 s)
- Number of extracted peaks is small and biologically plausible (typically 1–3 for a targeted query, not hundreds)
- Associated MS2 spectra (from chromPeakSpectra) have non-empty fragment lists and precursor m/z matching the target m/z ± tolerance
- Retention time of extracted peak aligns with expected elution time of the target compound from literature or prior runs
- MS2 fragment patterns are consistent across multiple scans (consensus spectrum has reasonable peak count and signal-to-noise ratio)

## Limitations

- Peak extraction quality depends on centWave algorithm parameters; suboptimal cwp settings may miss weak peaks or detect noise spikes as peaks
- ppm tolerance must match your instrument's mass accuracy; incorrect tolerance (too tight or too loose) causes false negatives or false positives
- Co-eluting compounds with similar m/z values may produce overlapping chromatographic peaks that cannot be separated by RT filtering alone; subsequent MS2 annotation (compareSpectra) is needed to disambiguate
- Some compounds may not fragment efficiently in DDA mode, resulting in few or no MS2 spectra despite clear MS1 signal; this is a limitation of data-dependent acquisition, not the extraction skill
- Missing precursor intensity values (e.g., from Sciex instruments) require estimatePrecursorIntensity() workaround

## Evidence

- [other] 1. Load PestMix1_DDA LC-MS/MS raw data and filter to retention time range 230–610 seconds using filterRt(). 2. Extract chromatographic peaks at m/z 304.1131 (±20 ppm tolerance) using chromPeaks() with mz and ppm parameters. 3. Retrieve all MS2 fragmentation spectra associated with the detected peak(s) using chromPeakSpectra() at msLevel=2.: "Extract chromatographic peaks at m/z 304.1131 (±20 ppm tolerance) using chromPeaks() with mz and ppm parameters. ... Retrieve all MS2 fragmentation spectra associated with the detected peak(s) using"
- [intro] dda_data <- filterRt(dda_data, rt = c(230, 610)): "Filter data to retention time range between 230 and 610 seconds based on total ion chromatogram analysis"
- [intro] Extract chromatographic peaks within specified m/z and retention time range of a feature: "chromPeaks(dda_data, mz = ex_mz, ppm = 20)"
- [readme] The *xcms* R package provides functionality to efficiently preprocess LC-MS (as well as GC-MS and LC-MS/MS) data.: "The *xcms* R package provides functionality to efficiently preprocess LC-MS (as well as GC-MS and LC-MS/MS) data."
- [intro] In a typical LC-MS-based metabolomics experiment compounds eluting from the chromatography are first ionized before being measured by mass spectrometry (MS). During the ionization different ions generated from the same compound being detected as different features: "In typical LC-MS-based metabolomics experiments, compounds eluting from chromatography are ionized and measured by mass spectrometry, with different ions generated from the same compound being"
