---
name: tic-peak-isolation-validation
description: Use when you have raw mass spectrometry data (mzML, mzXML, or CDF format) from at least 3 samples and need to automatically identify candidate peak regions in the TIC chromatogram before extracting ion-level parameters for XCMS or MZmine2 processing.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - R
  - AutoTuner
  - MSconvert
  - XCMS
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

# TIC Peak Isolation and Validation

## Summary

This skill identifies and isolates peaks within the total ion current (TIC) of mass spectrometry samples using sliding window analysis, then expands their boundaries to refine peak localization for downstream parameter estimation. It is essential for automating the discovery of meaningful chromatographic regions in untargeted metabolomics workflows where manual peak curation is impractical.

## When to use

Apply this skill when you have raw mass spectrometry data (mzML, mzXML, or CDF format) from at least 3 samples and need to automatically identify candidate peak regions in the TIC chromatogram before extracting ion-level parameters for XCMS or MZmine2 processing. Use it as the first step in AutoTuner's parameter tuning pipeline, after data has been converted to open format and loaded into an AutoTuner object.

## When NOT to use

- Input data has not been converted from proprietary instrument formats; MSconvert processing is required first.
- You already possess manually validated peak regions or a pre-curated feature list; isolation is redundant.
- Sample size is fewer than 3 replicates; AutoTuner requires sufficient replication for robust parameter inference.
- Data originates from a targeted method with known analytes; isolation is unnecessary when peak identity is predetermined.

## Inputs

- Raw mass spectrometry data in open format (mzML, mzXML, or CDF)
- AutoTuner object containing loaded samples
- Experimental metadata spreadsheet (sample names and group assignments)

## Outputs

- AutoTuner object with isolated TIC peak regions and expanded bounds
- Peak boundary coordinates (retention time start/end for each isolated region)

## How to apply

Load raw mass spectrometry data (post-MSconvert) into an AutoTuner object. Apply sliding window analysis to the total ion current (TIC) by tuning three key parameters: lag (the lookback window size), threshold (the Z-score cutoff for anomaly detection), and influence (the weight of previous anomalies on future detections). The sliding window identifies peaks as local maxima exceeding the threshold. Once candidate peaks are detected, invoke the isolatePeaks function to expand each region's boundaries beyond the initial detection window, capturing the full chromatographic width needed for stable parameter estimation. The expanded bounds serve as the input for downstream EICparams extraction. Validate that isolated regions do not overlap excessively and that boundary expansion captures the rising and falling edges of each peak.

## Related tools

- **AutoTuner** (Primary orchestration framework for loading raw data, executing sliding window peak detection, and managing isolated peak regions through isolatePeaks function) — https://github.com/KujawinskiLaboratory/Autotuner
- **MSconvert** (Prerequisite tool for converting raw proprietary mass spectrometry formats to open formats (mzML, mzXML, CDF) required by AutoTuner)
- **XCMS** (Downstream peak processing tool that consumes the parameter estimates derived from isolated TIC peak regions)
- **R** (Execution environment for AutoTuner package (requires version 3.6 or greater))

## Examples

```
library(Autotuner); at <- AutoTuner(raw_files=c('sample1.mzML','sample2.mzML','sample3.mzML'), metadata=pheno_data); at <- isolatePeaks(at, lag=5, threshold=2.5, influence=0.1)
```

## Evaluation signals

- Isolated peak regions do not overlap; each TIC local maximum is assigned a unique, non-intersecting boundary window.
- Boundary expansion captures full peak width: verify that the rising and falling edges of the chromatographic peak fall within the expanded bounds, not truncated.
- Sliding window parameters (lag, threshold, influence) are tuned to recover known or expected peak count; sensitivity/specificity trade-off should be documented.
- All isolated regions pass downstream EICparams extraction without errors or singular matrix conditions, confirming sufficient ion chromatogram density within bounds.
- Peak isolation reproducibility: the same sample run twice produces identical or near-identical boundary coordinates, indicating stable detection.

## Limitations

- Requires at least 3 samples for reliable statistical inference; insufficient replication may yield unstable or spurious parameter estimates.
- Sliding window parameters (lag, threshold, influence) are user-tunable but lack automated defaults; manual exploration is often necessary for new instrument types or sample matrices.
- High baseline noise, solvent peaks, or contamination in the TIC can create false positives; pre-filtering or sample quality control may be needed.
- Method has been validated on qTOF, Orbitrap, and Fourier transform ion cyclotron resonance mass analyzers; behavior on other analyzer types is untested.
- No changelog documented for version-to-version reproducibility; users upgrading AutoTuner may encounter parameter re-estimation differences.

## Evidence

- [intro] The first part of AutoTuner involves the identification of peaks within the total ion current (TIC) of the samples loaded up into AutoTuner.: "The first part of AutoTuner involves the identification of peaks within the total ion current (TIC) of the samples loaded up into AutoTuner."
- [intro] Autotuner will expand each of these regions to obtain improved estimates on the bounds within the isolatePeaks function: "Autotuner will expand each of these regions to obtain improved estimates on the bounds within the isolatePeaks function"
- [intro] The user should play with the lag, threshold, and influence parameters to perform the sliding window analysis.: "The user should play with the lag, threshold, and influence parameters to perform the sliding window analysis."
- [intro] AutoTuner is designed to work directly with raw mass spectral data that has been processed by using MSconvert.: "AutoTuner is designed to work directly with raw mass spectral data that has been processed by using MSconvert."
- [readme] Currently, AutoTuner requires R version 3.6 or greater.: "Currently, AutoTuner requires R version 3.6 or greater."
- [readme] For input, AutoTuner requires at least 3 samples of raw data converted from proprietary instrument formats (eg .mzML, .mzXML, or .CDF).: "For input, AutoTuner requires at least 3 samples of raw data converted from proprietary instrument formats (eg .mzML, .mzXML, or .CDF)."
- [readme] AutoTuner has been tested on untargeted data generated on qTOF, orbitrap and Fourier transform ion cyclotron resonance mass analyzers.: "AutoTuner has been tested on untargeted data generated on qTOF, orbitrap and Fourier transform ion cyclotron resonance mass analyzers."
