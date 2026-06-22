---
name: tic-peak-identification-sliding-window
description: Use when you have loaded raw mass spectrometry data (mzML, mzXML, or CDF format) into AutoTuner and need to identify peak regions in the TIC trace prior to extracted ion chromatogram (EIC) analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0121
  tools:
  - mtbls2
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Total Ion Current Peak Identification via Sliding Window Analysis

## Summary

Identifies and flags significant peaks in mass spectrometry total ion current (TIC) traces using a sliding window algorithm with configurable lag, threshold, and influence parameters. This skill is essential for detecting anomalous intensity spikes that represent genuine analyte signals before feature extraction and parameter optimization.

## When to use

Apply this skill when you have loaded raw mass spectrometry data (mzML, mzXML, or CDF format) into AutoTuner and need to identify peak regions in the TIC trace prior to extracted ion chromatogram (EIC) analysis. The skill is triggered when you require automated, parameter-driven peak detection on intensity time-series to seed subsequent feature isolation and bounds expansion.

## When NOT to use

- Input is already a feature table or processed peak list — use this skill only on raw TIC traces
- TIC trace contains severe baseline drift or multiplicative noise not amenable to additive sliding window thresholding
- Sample size is fewer than 3 replicates — AutoTuner requires minimum 3 samples for robust statistical inference

## Inputs

- Raw mass spectrometry data files (mzML, mzXML, or CDF format)
- AutoTuner R object with loaded sample data
- Total ion current (TIC) intensity trace (scan index × intensity vector)

## Outputs

- Per-sample signal vectors with peak flags and coordinates
- Structured output file containing TIC peaks, boundary coordinates, and flagging metadata
- Isolated peak regions suitable for EIC parameter extraction

## How to apply

Load raw data files into the AutoTuner R package and extract the TIC intensity trace for each sample. Apply the sliding window peak detection algorithm by configuring three parameters: lag (moving average window size in scans), threshold (multiplier determining how many times greater an adjacent scan intensity must be relative to the window average to flag as significant), and influence (scaling factor for the magnitude of flagged scans when incorporated back into the window for subsequent comparisons). The algorithm iterates through the TIC trace, computing a rolling mean and standard deviation over the lag window, and flags scans where intensity exceeds (mean + threshold × standard deviation). Flagged peaks are then passed to isolatePeaks for bound expansion to refine peak region estimates. Export the per-sample signal vectors with peak flags and scan coordinates to a structured output file for downstream parameter extraction.

## Related tools

- **Autotuner** (R package that implements TIC peak identification and sliding window analysis; loads raw data and exports flagged peak vectors) — https://github.com/KujawinskiLaboratory/Autotuner
- **mtbls2** (R package providing raw untargeted metabolomics dataset used to test and demonstrate TIC peak detection)
- **XCMS** (Downstream metabolomics data processing software; AutoTuner estimates parameters for XCMS feature detection)
- **MZmine2** (Downstream metabolomics data processing software; AutoTuner estimates parameters for MZmine2)
- **MSconvert** (Tool for converting proprietary mass spectrometry formats to open formats (mzML, mzXML, CDF) prior to AutoTuner input)

## Examples

```
library(Autotuner); data(mtbls2); autoTuner_obj <- Autotuner(ms_file_path, sample_metadata, lag=10, threshold=3, influence=0.5)
```

## Evaluation signals

- Verify peak flags align visually with TIC trace intensity maxima and do not occur in flat baseline regions
- Confirm lag parameter is set smaller than expected peak width (in scans) to avoid oversmooting genuine peaks
- Check that threshold parameter (typically 2–5×) produces a reasonable number of flagged peaks (e.g., 5–50 per sample depending on sample complexity)
- Validate that influence parameter (0–1) reduces weight of outliers appropriately; influence=1 treats all flagged scans equally, while influence<1 downweights them on re-entry to the rolling window
- Inspect isolatePeaks output to confirm peak boundaries are tighter and more accurate than raw flag coordinates, indicating successful bound expansion

## Limitations

- Sliding window approach assumes additive noise and may fail on TIC traces with severe baseline drift, multiplicative noise, or non-stationary background
- Algorithm performance is sensitive to lag, threshold, and influence parameter choices; suboptimal values can cause missed peaks or false positives
- Requires manual tuning or cross-validation of the three parameters; no automatic selection method is described in the article
- TIC peak detection does not distinguish chemical noise from true analyte signal; peaks flagged here are passed to EIC analysis for further refinement
- No changelog available in the repository, limiting traceability of algorithmic changes or bug fixes

## Evidence

- [other] The sliding window analysis uses three parameters to detect TIC peaks: lag defines the moving average window size; threshold sets how many times greater an adjacent scan intensity must be relative to the window average to be flagged as significant; and influence scales the magnitude of flagged scans when added back into the window for subsequent comparisons.: "lag defines the moving average window size; threshold sets how many times greater an adjacent scan intensity must be relative to the window average to be flagged as significant; and influence scales"
- [intro] The first part of AutoTuner involves the identification of peaks within the total ion current (TIC) of the samples loaded up into AutoTuner.: "The first part of AutoTuner involves the identification of peaks within the total ion current (TIC) of the samples loaded up into AutoTuner."
- [intro] Autotuner will expand each of these regions to obtain improved estimates on the bounds within the isolatePeaks function: "Autotuner will expand each of these regions to obtain improved estimates on the bounds within the isolatePeaks function"
- [intro] The user should play with the lag, threshold, and influence parameters to perform the sliding window analysis.: "The user should play with the lag, threshold, and influence parameters to perform the sliding window analysis."
- [readme] AutoTuner requires at least 3 samples of raw data converted from proprietary instrument formats (eg .mzML, .mzXML, or .CDF).: "AutoTuner requires at least 3 samples of raw data converted from proprietary instrument formats (eg .mzML, .mzXML, or .CDF)."
