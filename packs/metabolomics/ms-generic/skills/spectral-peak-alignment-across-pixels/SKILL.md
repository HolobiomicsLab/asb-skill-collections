---
name: spectral-peak-alignment-across-pixels
description: Use when after peak picking across individual spectra in an MSImagingExperiment, when you need to harmonize peak m/z positions across pixels to account for small shifts in peak location due to instrumental drift, calibration differences, or natural variation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3645
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Cardinal
  - R
  - Cardinal 3.6
  - BiocParallel
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1093/bioinformatics/btv146
  title: Cardinal
evidence_spans:
- library(Cardinal)
- '*Cardinal 3.6* is a major update with breaking changes. It bring support many of the new low-level signal processing functions'
- 'Once installed, Cardinal can be loaded with library(): library(Cardinal)'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cardinal_cq
    doi: 10.1093/bioinformatics/btv146
    title: Cardinal
  dedup_kept_from: coll_cardinal_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btv146
  all_source_dois:
  - 10.1093/bioinformatics/btv146
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-peak-alignment-across-pixels

## Summary

Aligns detected mass spectrometry peaks across all pixels in an imaging dataset to establish consistent m/z values for downstream feature-level analysis. This is a prerequisite for identifying peaks present in a sufficient fraction of pixels and for statistical analysis of imaging features.

## When to use

After peak picking across individual spectra in an MSImagingExperiment, when you need to harmonize peak m/z positions across pixels to account for small shifts in peak location due to instrumental drift, calibration differences, or natural variation. Use this before subsetting to high-frequency peaks or before statistical analysis that assumes consistent peak identity across the imaging array.

## When NOT to use

- Input peaks are already aligned or normalized to a reference peak list—alignment would be redundant.
- Working with a single spectrum or single pixel—alignment requires variation across multiple spectra to be meaningful.
- Peak positions are intentionally kept per-pixel for drift analysis or temporal tracking rather than harmonized for statistical analysis.

## Inputs

- MSImagingExperiment with detected peaks in featureData (from peakPick())
- Spectra matrix with per-pixel peak detections

## Outputs

- MSImagingExperiment with aligned peaks in featureData
- Unified peak m/z feature space across all pixels
- Peak frequency information (presence/absence per pixel)

## How to apply

Load the MSImagingExperiment containing detected peaks (typically output from peakPick()). Apply peakAlign() to align peaks detected across all spectra in the imaging dataset—this function registers peak m/z values from different pixels to a common set of peak positions, reducing m/z jitter across the array. The alignment establishes a unified feature space where each aligned peak represents the same m/z across all pixels. After alignment, use subsetFeatures() with a frequency threshold (e.g., > 0.1 to retain peaks in >10% of pixels) to filter out spurious or rare peaks. Verify success by confirming the resulting featureData contains the expected number of aligned peaks and that their m/z values are stable across pixels.

## Related tools

- **Cardinal 3.6** (Provides peakAlign() function for aligning peak m/z positions across pixels and subsetFeatures() for frequency-based peak filtering) — https://github.com/kuwisdelu/Cardinal
- **R** (Runtime environment for executing Cardinal functions and MSImagingExperiment operations)
- **BiocParallel** (Optional parallel processing support for peakAlign() across large imaging datasets)

## Examples

```
library(Cardinal); mse <- peakAlign(mse); mse_filtered <- subsetFeatures(mse, mz ~ frequency > 0.1)
```

## Evaluation signals

- The resulting MSImagingExperiment featureData contains a consistent set of aligned peaks (e.g., 37 peaks) present across multiple pixels.
- Peak m/z values in featureData show reduced variance compared to pre-alignment per-pixel detections, indicating successful harmonization.
- Frequency counts in feature metadata indicate each peak is present in a reasonable fraction of pixels (e.g., ≥10% for common peaks).
- Subsetting to peaks with frequency > threshold retains only peaks meeting the frequency criterion; no spurious single-pixel peaks remain in the filtered result.
- Manual inspection or plotting of aligned peaks across pixel coordinates confirms visual alignment without m/z drift artifacts.

## Limitations

- Peak alignment quality depends on sufficient peak overlap across pixels; sparse or highly localized spatial features may not align robustly.
- The choice of frequency threshold (e.g., > 0.1) is user-dependent and affects the final feature count; no universal optimal threshold is provided in the article.
- Alignment assumes peaks are real chemical species; false positives from noise in individual pixels may introduce spurious aligned features if peak-picking thresholds are too lenient.
- Large m/z shifts or systematic calibration drift across the imaging array may exceed alignment tolerance, resulting in multiple m/z entries for a single true peak.

## Evidence

- [other] After filtering to peaks with frequencies > 0.1, the resulting MSImagingExperiment contains exactly 37 peaks in featureData.: "After filtering to peaks with frequencies > 0.1, the resulting MSImagingExperiment contains exactly 37 peaks in featureData."
- [other] Apply peakAlign() to align detected peaks across all spectra in the imaging dataset.: "Apply peakAlign() to align detected peaks across all spectra in the imaging dataset."
- [other] Subset features using subsetFeatures() with a frequency threshold of > 0.1 to retain only peaks present in >10% of pixels.: "Subset features using subsetFeatures() with a frequency threshold of > 0.1 to retain only peaks present in >10% of pixels."
- [intro] New spectral alignment methods in recalibrate(): Local maxima-based alignment using local regression, Dynamic time warping, Correlation optimized warping: "New spectral alignment methods in recalibrate(): Local maxima-based alignment using local regression, Dynamic time warping, Correlation optimized warping"
- [intro] Parallel processing support via the BiocParallel package for all pre-processing methods and any statistical analysis methods with a BPPARAM option: "Parallel processing support via the BiocParallel package for all pre-processing methods and any statistical analysis methods with a BPPARAM option"
