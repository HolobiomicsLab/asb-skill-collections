---
name: parameter-tuning-metabolomics
description: Use when you have at least 3 raw mass spectrometry samples in open formats (mzML, mzXML, CDF) from untargeted metabolomics experiments and need to configure parameters for XCMS, MZmine2, or similar processing software.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - mtbls2
  - R
  - XCMS
  - MZmine2
  - MSconvert
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1101/812370
  title: AutoTuner parameter selection
evidence_spans:
- library(mtbls2)
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

# Automated parameter tuning for metabolomics data processing

## Summary

AutoTuner uses statistical inference on raw mass spectrometry data to automatically estimate dataset-specific parameters for untargeted metabolomics processing pipelines. This skill is essential when processing new metabolomics datasets where manual parameter optimization is infeasible or when reproducible, data-driven parameter selection is required.

## When to use

Apply this skill when you have at least 3 raw mass spectrometry samples in open formats (mzML, mzXML, CDF) from untargeted metabolomics experiments and need to configure parameters for XCMS, MZmine2, or similar processing software. Use it especially when samples are from new instrument types (qTOF, Orbitrap, FT-ICR), experimental designs, or when manual parameter tuning introduces subjectivity into your workflow.

## When NOT to use

- Input data are already processed into a feature table or peak list; use this skill only on raw instrument data.
- Samples are from fewer than 3 replicates; AutoTuner requires sufficient replication for robust statistical inference.
- You have already manually optimized parameters for your specific instrument and experimental design and reproducibility across datasets is not a priority.

## Inputs

- Raw mass spectrometry data files (mzML, mzXML, or CDF format)
- Experimental metadata spreadsheet with sample names and factor annotations
- User-defined sliding window parameters (lag, threshold, influence) for TIC analysis
- Mass threshold value specific to mass analyzer type

## Outputs

- Per-sample TIC intensity trace with flagged peaks and coordinates
- Nine optimized parameter estimates for XCMS/MZmine2 processing
- Feature table or peak list ready for downstream statistical analysis

## How to apply

Load raw data files and an experimental metadata spreadsheet (with sample names and experimental factors) into the AutoTuner R package. AutoTuner performs sliding-window analysis on the total ion current (TIC) trace with user-configurable lag, threshold, and influence parameters to identify significant peaks; lag defines the moving average window size, threshold sets the multiplier for flagging anomalous scans relative to the window average, and influence scales flagged scan magnitudes when reintegrated into subsequent comparisons. Extract per-sample signal vectors with peak flags and coordinates. Then run the EICparams function on extracted ion chromatograms (EICs) while setting the massThreshold parameter to exceed your mass analyzer's expected analytical capability. AutoTuner returns nine optimized parameter estimates suitable for downstream processing by XCMS or MZmine2. Validate outputs by inspecting the stability and biological relevance of detected peaks across replicates.

## Related tools

- **XCMS** (Target metabolomics processing software whose parameters are estimated by AutoTuner)
- **MZmine2** (Alternative target metabolomics processing software whose parameters are estimated by AutoTuner)
- **MSconvert** (Converts proprietary mass spectrometry formats to open formats (mzML, mzXML) required as input to AutoTuner)
- **mtbls2** (R package containing reference untargeted metabolomics datasets used for validation and tutorial workflows)

## Examples

```
library(Autotuner); library(mtbls2); data <- readAutoTuner(files=c('sample1.mzML','sample2.mzML','sample3.mzML'), metadata=metadata.csv); ticPeaks <- tic_peak_detect(data, lag=5, threshold=3, influence=0.5); params <- EICparams(ticPeaks, massThreshold=0.01)
```

## Evaluation signals

- TIC peak detection produces reproducible peak flags and coordinates across replicate samples within the same experimental group.
- The nine returned parameters yield feature tables with peak counts and intensities consistent across technical replicates (correlation > 0.9).
- Detected metabolites in the feature table match expected biochemical signatures for the organism or tissue type (e.g., CYP79 pathway intermediates in the mtbls2 cyp79 dataset).
- Mass error across detected m/z values remains within the specified massThreshold and below the analytical capability of the mass analyzer.
- Downstream statistical tests (e.g., fold-change analysis, PCA) show clear separation between experimental groups, indicating parameter optimization preserved biological signal.

## Limitations

- Requires a minimum of 3 samples per analysis; smaller datasets may yield unstable parameter estimates.
- AutoTuner has been validated on qTOF, Orbitrap, and FT-ICR mass analyzers; performance on other instrument types is not documented.
- Parameter estimation assumes samples span sufficient chemical diversity; datasets with artificially uniform composition may not trigger robust statistical inference.
- The massThreshold parameter must be manually specified based on instrument specifications and is critical to EIC parameter extraction; incorrect threshold values can propagate downstream errors.
- No changelog or version history is publicly documented, limiting reproducibility across different software versions.

## Evidence

- [intro] Nine distinct parameters: "Using statistical inference, AutoTuner quickly finds estimates for nine distinct parameters."
- [intro] TIC peak identification via sliding window: "The first part of AutoTuner involves the identification of peaks within the total ion current (TIC) of the samples loaded up into AutoTuner."
- [intro] Sliding window parameters: lag, threshold, influence: "The user should play with the lag, threshold, and influence parameters to perform the sliding window analysis."
- [other] Lag, threshold, influence definitions: "lag defines the moving average window size; threshold sets how many times greater an adjacent scan intensity must be relative to the window average to be flagged as significant; and influence scales"
- [intro] EICparams function with massThreshold: "The massThreshold is an absolute mass error that should be greater than the expected analytical capabilities of the mass analyzer."
- [readme] Minimum sample requirement: "For input, AutoTuner requires at least 3 samples of raw data converted from proprietary instrument formats (eg .mzML, .mzXML, or .CDF)."
- [readme] Instrument validation scope: "So far, AutoTuner has been tested on untargeted data generated on qTOF, orbitrap and Fourier transform ion cyclotron resonance mass analyzers."
