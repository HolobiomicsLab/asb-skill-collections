---
name: signal-anomaly-detection-chromatography
description: Use when you have raw total ion current (TIC) traces extracted from mass
  spectrometry samples (e.g., from qTOF, orbitrap, or FTICR instruments) and need
  to identify and flag scans with anomalous peak intensities before feature detection.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - mtbls2
  - R
  - Autotuner
  - MSconvert
  - XCMS
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
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

# signal-anomaly-detection-chromatography

## Summary

Detect and flag anomalous peaks in total ion current (TIC) traces from mass spectrometry samples using a sliding window analysis with configurable lag, threshold, and influence parameters. This skill identifies significant intensity deviations that warrant further investigation or exclusion during metabolomics data processing.

## When to use

Apply this skill when you have raw total ion current (TIC) traces extracted from mass spectrometry samples (e.g., from qTOF, orbitrap, or FTICR instruments) and need to identify and flag scans with anomalous peak intensities before feature detection. Use it as a preparatory step in the AutoTuner workflow when TIC traces exhibit irregular spikes or baseline drift that could confound downstream peak picking.

## When NOT to use

- Input is already a feature table or peak-picked matrix; this skill operates on raw chromatographic traces, not quantified features.
- TIC trace has already been smoothed or filtered by other preprocessing; the sliding window analysis assumes raw, unsmoothed intensity data.
- You need to detect anomalies in extracted ion chromatograms (EICs) rather than the total ion current; use this skill only on the summed TIC.

## Inputs

- Raw mass spectrometry data files (mzML, mzXML, or CDF format)
- Total ion current (TIC) intensity trace vector for each sample
- Sample metadata spreadsheet (sample name column + experimental factor column)

## Outputs

- Per-sample signal vectors with anomalous peak flags
- Coordinates (scan indices) of flagged peaks
- Structured output file containing TIC anomaly annotations

## How to apply

Load raw mass spectrometry data (in mzML, mzXML, or CDF format) into the AutoTuner R package and extract the TIC intensity trace for each sample. Apply sliding window analysis by iteratively computing a moving average over a window of size defined by the lag parameter. For each scan, compare its intensity to the moving average; flag the scan as anomalous if it exceeds the average by a factor specified by the threshold parameter. When a scan is flagged, scale its contribution to the moving average by the influence parameter (0–1) before updating the window for the next comparison. Iterate through all scans and export per-sample signal vectors annotated with peak flags and coordinates. Tune lag (typically 5–50 scans), threshold (typically 2–5×), and influence (typically 0–1) based on visual inspection of TIC traces and the expected noise characteristics of your mass analyzer.

## Related tools

- **Autotuner** (Primary R package that implements sliding window peak detection for TIC traces and parameter tuning for metabolomics data processing) — https://github.com/KujawinskiLaboratory/Autotuner
- **mtbls2** (R package providing raw untargeted metabolomics data and sample metadata for testing and validation)
- **MSconvert** (Tool for converting proprietary mass spectrometry instrument formats to open standards (mzML, mzXML, CDF) prior to loading into AutoTuner)
- **XCMS** (Downstream metabolomics data processing software for which AutoTuner tunes parameters; AutoTuner estimates parameters to optimize XCMS peak detection)

## Examples

```
library(Autotuner); library(mtbls2); at <- readAutoTuner(data_directory, metadata_file); tic_anomalies <- detectAnomalies(at, lag=20, threshold=3, influence=0.5); export_anomaly_flags(tic_anomalies, output_file='flagged_peaks.csv')
```

## Evaluation signals

- Flagged peaks correspond visually to obvious TIC intensity spikes when the TIC trace is plotted; no false positives in flat baseline regions.
- The number and distribution of flagged peaks are stable when lag and threshold parameters are adjusted incrementally (±10–20% changes).
- Downstream feature detection (e.g., in XCMS or MZmine2) produces a higher-quality feature table when input data is pre-filtered using the flagged anomalies.
- Influence parameter values between 0 and 1 produce smooth, interpretable flag patterns; influence = 0 (complete rejection) and influence = 1 (full inclusion) represent expected boundary behaviors.
- Output coordinates are consistent with manual inspection of raw TIC files; spot-checking 5–10 flagged peaks confirms correct scan indexing and intensity thresholding.

## Limitations

- Requires tuning of three interdependent parameters (lag, threshold, influence); optimal values are dataset- and instrument-specific and may not transfer across different mass analyzers or experimental designs.
- Sliding window approach assumes that anomalies are localized in time; systematic baseline drift or gradual intensity changes may not be detected reliably.
- Performance has been validated only on qTOF, orbitrap, and FTICR instruments; generalization to other mass analyzer types is not documented.
- Requires at least 3 raw samples and a sample metadata spreadsheet; single-sample or metadata-free inputs cannot be processed through the full AutoTuner pipeline.
- No published changelog available; version compatibility and parameter stability across Autotuner releases are not formally documented.

## Evidence

- [intro] The first part of AutoTuner involves the identification of peaks within the total ion current (TIC) of the samples loaded up into AutoTuner.: "The first part of AutoTuner involves the identification of peaks within the total ion current (TIC)"
- [other] lag defines the moving average window size; threshold sets how many times greater an adjacent scan intensity must be relative to the window average to be flagged as significant; and influence scales the magnitude of flagged scans when added back into the window for subsequent comparisons.: "lag defines the moving average window size; threshold sets how many times greater an adjacent scan intensity must be relative to the window average to be flagged as significant; and influence scales"
- [intro] The user should play with the lag, threshold, and influence parameters to perform the sliding window analysis.: "The user should play with the lag, threshold, and influence parameters to perform the sliding window analysis."
- [readme] AutoTuner requires at least 3 samples of raw data converted from proprietary instrument formats (eg .mzML, .mzXML, or .CDF).: "AutoTuner requires at least 3 samples of raw data converted from proprietary instrument formats (eg .mzML, .mzXML, or .CDF)"
- [readme] AutoTuner has been tested on untargeted data generated on qTOF, orbitrap and Fourier transform ion cyclotron resonance mass analyzers.: "AutoTuner has been tested on untargeted data generated on qTOF, orbitrap and Fourier transform ion cyclotron resonance mass analyzers."
