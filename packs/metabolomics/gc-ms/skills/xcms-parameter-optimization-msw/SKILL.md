---
name: xcms-parameter-optimization-msw
description: Use when when you have direct-injection or low-complexity mass spectrometry data (mzML files) and need to detect chromatographic peaks using wavelet-based methods instead of centWave, especially when standard retention-time-dependent peak detection is not suitable or when you need to tune.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - xcms
  - MsDataHub
  - MassSpecWavelet
  - MSnbase
  techniques:
  - LC-MS
  - GC-MS
derived_from:
- doi: 10.1021/ac051437y
  title: XCMS
evidence_spans:
- The *xcms* R package provides functionality to efficiently preprocess LC-MS (as well as GC-MS and LC-MS/MS) data.
- 'Package: xcms'
- library(MsDataHub)
- '`r Biocpkg("xcms")` uses functionality from the *MassSpecWavelet* package to identify such peaks'
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# xcms-parameter-optimization-msw

## Summary

Optimize MSWParam (MassSpecWavelet) peak detection parameters in xcms for direct-injection or low-complexity FTICR-MS and similar spectra by selecting appropriate wavelet scales, noise window sizes, and signal-to-noise thresholds to maximize chromatographic peak detection accuracy.

## When to use

When you have direct-injection or low-complexity mass spectrometry data (mzML files) and need to detect chromatographic peaks using wavelet-based methods instead of centWave, especially when standard retention-time-dependent peak detection is not suitable or when you need to tune sensitivity and specificity for a particular instrument or sample matrix.

## When NOT to use

- If your data is already preprocessed into a feature table or aligned peak matrix — peak detection is the first step, not a refinement step.
- If you have high-resolution LC-MS data with well-separated chromatographic peaks; centWave algorithm is typically more appropriate for conventional gradient LC-MS.
- If you lack domain knowledge or reference standards to validate optimized parameters; MSWParam tuning requires iteration and validation against known compounds.

## Inputs

- mzML files (raw mass spectrometry data)
- XCMSnExp object (xcms in-memory or on-disk representation)
- Sample metadata (phenotype data frame for sample annotation)

## Outputs

- chromPeaks matrix (detected chromatographic peaks with m/z, retention time, intensity)
- MSWParam configuration object
- XCMSnExp object with integrated chromPeaks slot

## How to apply

Load your mzML data into xcms as an XCMSnExp object using readMSData() in on-disk mode. Configure MSWParam by selecting wavelet scales (e.g., c(1, 4, 9) for multi-resolution analysis), setting the noise window size (e.g., 500 data points), choosing a signal-to-noise estimation method (e.g., data.mean), and defining a signal-to-noise ratio threshold (e.g., snthresh=10). Optionally enable nearbyPeak=TRUE to group nearby detected peaks. Execute findChromPeaks() with the configured MSWParam on your XCMSnExp object to generate a chromPeaks matrix. Validate results by examining detected peak counts, m/z ranges, and retention time distributions, and iteratively refine parameters if peak detection is too sparse or too permissive for your application.

## Related tools

- **xcms** (Core package providing XCMSnExp class, readMSData(), findChromPeaks(), and MSWParam configuration interface) — https://github.com/sneumann/xcms
- **MassSpecWavelet** (Provides wavelet-based peak detection algorithm wrapped by xcms MSWParam)
- **MsDataHub** (Supplies mzML test datasets (HAM004, HAM005) for reproducible benchmarking)
- **MSnbase** (Bioconductor base class framework for mass spectrometry data representation)

## Examples

```
library(xcms); xmse <- readMSData(files = c('HAM004.mzML', 'HAM005.mzML'), mode = 'onDisk'); param <- MSWParam(scales = c(1, 4, 9), nearbyPeak = TRUE, winSize.noise = 500, SNR.method = 'data.mean', snthresh = 10); xmse <- findChromPeaks(xmse, param); head(chromPeaks(xmse))
```

## Evaluation signals

- chromPeaks matrix is non-empty and contains expected number of peaks (typically 100–10,000 depending on sample complexity); absence of peaks suggests snthresh is too high or scales poorly chosen.
- Detected peak m/z values fall within expected range for your instrument and sample (e.g., 200–2000 m/z for small-molecule metabolomics).
- Peak retention times are physically plausible (e.g., 0–1200 seconds for typical LC methods, or concentrated near injection point for direct injection).
- Signal-to-noise ratio of detected peaks is ≥ the specified threshold; spot-check a few peaks in the raw data to verify SNR calculation.
- Reproducibility: running the same workflow twice with identical parameters on the same data produces identical chromPeaks matrix (deterministic result).

## Limitations

- MSWParam is sensitive to wavelet scale selection; inappropriate scales may miss small peaks or detect noise. No automated scale selection is provided; scales must be chosen a priori or via grid search.
- Noise window size (winSize.noise) is fixed across the entire spectrum; varying local noise characteristics (e.g., low m/z vs. high m/z) may not be captured.
- Direct-injection data often lacks retention-time dimension, reducing the utility of retention-time-based grouping steps downstream; peak grouping must rely on m/z similarity or other metrics.
- SNR method (data.mean, data.median, etc.) assumes stationarity; highly variable baseline or instrumental drift may lead to biased noise estimates.
- No built-in visual diagnostics for parameter tuning; practitioners must export and plot chromPeaks matrix manually to assess adequacy.

## Evidence

- [other] MSWParam peak detection configuration: "MSWParam peak detection uses wavelet scales of 1, 4, and 9 with nearbyPeak=TRUE, a noise window size of 500, data mean signal-to-noise ratio method, and signal-to-noise threshold of 10"
- [other] Workflow for loading and applying MSWParam: "Load the HAM004 and HAM005 mzML files from MsDataHub using readMSData() in xcms with on-disk mode to create an XCMSnExp object. Configure MSWParam with scales c(1,4,9), nearbyPeak=TRUE,"
- [intro] MassSpecWavelet role in xcms: "`r Biocpkg("xcms")` uses functionality from the *MassSpecWavelet* package to identify such peaks"
- [readme] Direct injection and data format support: "The *xcms* R package provides functionality to efficiently preprocess LC-MS (as well as GC-MS and LC-MS/MS) data."
- [other] Output validation: chromPeaks matrix extraction: "Extract and validate the resulting chromPeaks matrix containing peak detection results."
