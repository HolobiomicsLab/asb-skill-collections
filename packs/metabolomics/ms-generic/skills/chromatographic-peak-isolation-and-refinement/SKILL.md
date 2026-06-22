---
name: chromatographic-peak-isolation-and-refinement
description: Use when after sliding-window analysis has identified candidate TIC peaks but before extracting chromatographic parameters (retention time, peak width, intensity) from extracted ion chromatograms.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - R
  - Autotuner
  - XCMS
  - MZmine2
  - MSconvert
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# chromatographic-peak-isolation-and-refinement

## Summary

Refine and expand the boundaries of total ion current (TIC) peaks identified by sliding-window analysis using the isolatePeaks function, producing improved peak boundary estimates (start time, end time, apex position) for subsequent parameter extraction. This skill bridges coarse sliding-window peak detection with fine-grained parameter estimation in untargeted metabolomics data processing.

## When to use

After sliding-window analysis has identified candidate TIC peaks but before extracting chromatographic parameters (retention time, peak width, intensity) from extracted ion chromatograms. Use this skill when you need to refine peak boundaries around initial window-detected regions to reduce false positives and improve parameter estimation accuracy for downstream XCMS or MZmine2 feature detection.

## When NOT to use

- Raw mass spectra have not yet been converted to an open format (mzML, mzXML, CDF) or preprocessed by MSconvert — isolatePeaks requires the AutoTuner object initialized from converted data.
- Sliding-window analysis has not been run or returned zero peaks — isolatePeaks operates on existing window-detected signals and cannot generate peaks de novo.
- Peak boundaries have already been manually inspected and validated by an expert — re-running isolatePeaks on finalized peaks adds no analytical value.

## Inputs

- AutoTuner object containing sliding-window-identified TIC peaks
- returned_peaks parameter (integer, e.g., 10)
- Raw mass spectral data (mzML, mzXML, or CDF format, preprocessed by MSconvert)

## Outputs

- Isolated peaks object with refined boundary estimates
- Peak boundary table (start time, end time, apex position for each peak)
- CSV export of peak boundaries for validation

## How to apply

Load the AutoTuner object containing sliding-window-identified peaks into R and call the isolatePeaks function with the returned_peaks parameter (e.g., 10) specifying the number of peaks to return. The function expands each sliding-window-detected region to obtain improved boundary estimates. Extract the resulting peak boundary table (start time, end time, apex position) for each of the returned peaks and export to CSV for review and subsequent EICparams parameter extraction. The rationale is that isolatePeaks uses statistical inference to widen the initial narrow window boundaries, capturing the full peak shape and improving robustness to noise-induced boundary artifacts.

## Related tools

- **Autotuner** (R package providing the isolatePeaks function and AutoTuner class for TIC peak detection and boundary refinement) — https://github.com/KujawinskiLaboratory/Autotuner
- **XCMS** (Peak detection software that Autotuner parameters are tuned to optimize)
- **MZmine2** (Peak detection software that Autotuner parameters are tuned to optimize)
- **MSconvert** (Converts raw mass spectrometer data to open formats (mzML, mzXML, CDF) required for AutoTuner input)
- **R** (Programming environment for running isolatePeaks and AutoTuner workflows)

## Examples

```
library(Autotuner); isolated <- isolatePeaks(autotuner_object, returned_peaks = 10); write.csv(isolated$peaks, 'peak_boundaries.csv')
```

## Evaluation signals

- Peak boundary table contains exactly returned_peaks rows (e.g., 10) with valid start time, end time, and apex position columns; apex is between start and end.
- Expanded boundaries are wider than the original sliding-window boundaries (visual inspection or boundary width delta > 0).
- All boundary time values are within the chromatographic run duration and in ascending order (start < apex < end).
- Export to CSV is successful and table is readable by downstream EICparams parameter extraction step without format errors.
- Refined peaks show reduced overlap or clustering compared to raw sliding-window peaks, indicating effective boundary separation.

## Limitations

- isolatePeaks depends on the quality of initial sliding-window peak detection; if the window analysis is misconfigured (lag, threshold, influence parameters), boundary refinement cannot recover missing or spurious peaks.
- Performance has been validated only on qTOF, Orbitrap, and Fourier transform ion cyclotron resonance mass analyzers; performance on other instrument types is untested.
- Requires at least 3 raw samples and a metadata spreadsheet linking samples to experimental factors; isolated peaks are not meaningful if AutoTuner has not been initialized with multi-sample data.
- No changelog or version history is available in the repository, limiting traceability of boundary refinement algorithm changes across releases.

## Evidence

- [other] The isolatePeaks function accepts an AutoTuner object, a returned_peaks parameter specifying the number of peaks to return (e.g., 10), and signals from the sliding window analysis, then outputs isolated peaks with expanded boundary estimates for subsequent parameter estimation.: "The isolatePeaks function accepts an AutoTuner object, a returned_peaks parameter specifying the number of peaks to return (e.g., 10), and signals from the sliding window analysis, then outputs"
- [intro] The first part of AutoTuner involves the identification of peaks within the total ion current (TIC) of the samples loaded up into AutoTuner.: "The first part of AutoTuner involves the identification of peaks within the total ion current (TIC) of the samples"
- [intro] Autotuner will expand each of these regions to obtain improved estimates on the bounds within the isolatePeaks function: "Autotuner will expand each of these regions to obtain improved estimates on the bounds within the isolatePeaks function"
- [intro] AutoTuner is designed to work directly with raw mass spectral data that has been processed by using MSconvert.: "AutoTuner is designed to work directly with raw mass spectral data that has been processed by using MSconvert"
- [readme] AutoTuner has been tested on untargeted data generated on qTOF, orbitrap and Fourier transform ion cyclotron resonance mass analyzers.: "AutoTuner has been tested on untargeted data generated on qTOF, orbitrap and Fourier transform ion cyclotron resonance mass analyzers"
- [readme] AutoTuner requires at least 3 samples of raw data converted from proprietary instrument formats (eg .mzML, .mzXML, or .CDF).: "AutoTuner requires at least 3 samples of raw data converted from proprietary instrument formats (eg .mzML, .mzXML, or .CDF)"
