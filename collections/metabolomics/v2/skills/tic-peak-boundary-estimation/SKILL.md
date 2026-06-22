---
name: tic-peak-boundary-estimation
description: Use when after sliding-window analysis has identified candidate TIC peaks but before parameter extraction from Extracted Ion Chromatograms (EICs).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0121
  tools:
  - R
  - Autotuner
  - MSconvert
  - XCMS
  - MZmine2
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1101/812370
  title: AutoTuner parameter selection
evidence_spans:
- knitr::rmarkdown
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_autotuner_parameter_selection_cq
    doi: 10.1101/812370
    title: AutoTuner parameter selection
  dedup_kept_from: coll_autotuner_parameter_selection_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/812370
  all_source_dois:
  - 10.1101/812370
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# TIC Peak Boundary Estimation via isolatePeaks

## Summary

Expands the boundaries of Total Ion Current peaks identified by sliding-window analysis to produce refined peak boundary estimates (start time, end time, apex position) suitable for downstream parameter extraction. This skill uses the AutoTuner isolatePeaks function to refine coarse sliding-window-detected peak regions into precise boundaries for subsequent EIC parameter estimation.

## When to use

After sliding-window analysis has identified candidate TIC peaks but before parameter extraction from Extracted Ion Chromatograms (EICs). Use this skill when you have AutoTuner-detected TIC peaks from raw mass spectral data (mzML, mzXML, or CDF format) and need to establish accurate peak start/end times and apex positions to feed into the EICparams function.

## When NOT to use

- Input data has not yet been processed through sliding-window peak detection; run sliding window analysis first.
- Peak boundaries are already known or have been manually validated; isolatePeaks is designed to refine automated estimates, not override expert annotation.
- Raw data is in proprietary vendor formats (e.g., .d, .raw); convert to open formats (mzML, mzXML, CDF) using MSconvert before running AutoTuner.

## Inputs

- AutoTuner object containing sliding-window-identified TIC peaks
- Signals from sliding window analysis (lag, threshold, influence parameters applied)
- Raw mass spectral data in mzML, mzXML, or CDF format (already loaded in AutoTuner)

## Outputs

- Isolated peaks with expanded boundary estimates
- Peak boundary table (start time, end time, apex position for each peak)
- CSV file containing tabulated peak boundaries (optional export)

## How to apply

Load the AutoTuner object containing sliding-window-identified TIC peaks into R and call the isolatePeaks function with the returned_peaks parameter (e.g., 10) specifying how many peaks to return. The function accepts the AutoTuner object and signals from the sliding window analysis, then outputs isolated peaks with expanded boundary estimates. Extract and tabulate the peak boundary estimates (start time, end time, apex position) for each returned peak. Rationale: isolatePeaks expands each sliding-window-detected region to obtain improved estimates on peak bounds, which increases fidelity for downstream parameter estimation and reduces sensitivity to the initial sliding-window lag, threshold, and influence parameter choices.

## Related tools

- **Autotuner** (Primary R package containing the isolatePeaks function and AutoTuner object class) — https://github.com/KujawinskiLaboratory/Autotuner
- **R** (Execution environment for loading AutoTuner and calling isolatePeaks)
- **MSconvert** (Preprocesses raw mass spectral data from proprietary formats into open formats (mzML, mzXML, CDF) compatible with AutoTuner)
- **XCMS** (Downstream metabolomics data processing software to which optimized AutoTuner parameters are transferred)
- **MZmine2** (Alternative downstream metabolomics data processing software to which optimized AutoTuner parameters are transferred)

## Examples

```
library(Autotuner); isolatePeaks(autotuner_object, returned_peaks=10)
```

## Evaluation signals

- Returned peaks count matches the returned_peaks parameter value (e.g., 10 peaks returned when returned_peaks=10).
- Each peak boundary tuple contains three numeric fields: start_time < apex_position < end_time, all in consistent chromatographic time units.
- Peak boundaries do not overlap excessively (no single m/z region claimed by multiple peaks without justification).
- Downstream EICparams function successfully accepts the isolated peak boundaries and completes parameter extraction without error.
- Peak boundary estimates are reproducible when isolatePeaks is run on the same AutoTuner object with identical returned_peaks parameter.

## Limitations

- Requires at least 3 samples of raw mass spectral data; AutoTuner is not designed for single-sample or two-sample datasets.
- Performance depends on quality of initial sliding-window peak detection (lag, threshold, influence parameters); poor sliding-window settings propagate to boundary expansion.
- Tested on qTOF, orbitrap, and FTICR mass analyzers; behavior on other instrument types is not documented.
- Requires R version 3.6 or greater; compatibility with older R versions is not supported.

## Evidence

- [other] The isolatePeaks function accepts an AutoTuner object, a returned_peaks parameter specifying the number of peaks to return (e.g., 10), and signals from the sliding window analysis, then outputs isolated peaks with expanded boundary estimates for subsequent parameter estimation.: "The isolatePeaks function accepts an AutoTuner object, a returned_peaks parameter specifying the number of peaks to return (e.g., 10), and signals from the sliding window analysis, then outputs"
- [intro] Autotuner will expand each of these regions to obtain improved estimates on the bounds within the isolatePeaks function: "Autotuner will expand each of these regions to obtain improved estimates on the bounds within the isolatePeaks function"
- [intro] The first part of AutoTuner involves the identification of peaks within the total ion current (TIC) of the samples loaded up into AutoTuner.: "The first part of AutoTuner involves the identification of peaks within the total ion current (TIC) of the samples loaded up into AutoTuner."
- [readme] AutoTuner requires at least 3 samples of raw data converted from proprietary instrument formats (eg .mzML, .mzXML, or .CDF).: "AutoTuner requires at least 3 samples of raw data converted from proprietary instrument formats (eg .mzML, .mzXML, or .CDF)."
- [readme] AutoTuner has been tested on untargeted data generated on qTOF, orbitrap and Fourier transform ion cyclotron resonance mass analyzers.: "AutoTuner has been tested on untargeted data generated on qTOF, orbitrap and Fourier transform ion cyclotron resonance mass analyzers."
