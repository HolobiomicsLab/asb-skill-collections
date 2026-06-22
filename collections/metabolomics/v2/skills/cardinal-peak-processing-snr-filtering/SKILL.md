---
name: cardinal-peak-processing-snr-filtering
description: Use when when you have loaded an unprocessed Cardinal object from MS imaging data (e.g., from Zenodo or native formats) containing thousands of m/z features across many spectra, and you need to produce a curated peak list with known expected peak count (e.g., 687 cleaned peaks from PIGII_206).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Cardinal
  - SpaMTP
  - dplyr
  - R
  - Seurat
derived_from:
- doi: 10.1101/2024.10.31.621429v1
  title: SpaMTP
- doi: 10.1101/2024.10.14.618269
  title: ''
evidence_spans:
- library(Cardinal)
- Install SpaMTP if not previously installed devtools::install_github("GenomicsMachineLearning/SpaMTP")
- library(dplyr)
- For plotting + DE plots
- '## Install and Import *R* Libraries'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_spamtp_cq
    doi: 10.1101/2024.10.31.621429v1
    title: SpaMTP
  dedup_kept_from: coll_spamtp_cq
schema_version: 0.2.0
---

# Cardinal peak processing with SNR filtering

## Summary

Apply Cardinal's peakProcess function to detect and filter MS imaging peaks using signal-to-noise ratio thresholds, generating a cleaned peak list suitable for downstream annotation and spatial analysis. This skill reduces noise-driven false positives in high-dimensional MS imaging datasets.

## When to use

When you have loaded an unprocessed Cardinal object from MS imaging data (e.g., from Zenodo or native formats) containing thousands of m/z features across many spectra, and you need to produce a curated peak list with known expected peak count (e.g., 687 cleaned peaks from PIGII_206). Apply this skill after feature summarization and normalization (TIC) but before spatial segmentation or metabolite annotation, especially when SNR varies across the dataset.

## When NOT to use

- Input is already a pre-processed or vendor-supplied peak list (e.g., from mzML, mzXML, or NetCDF with pre-picked peaks).
- SNR threshold and tolerance parameters are not known or cannot be validated against expected output; use peakProcess only when ground truth peak counts or method parameters are documented.
- Dataset contains LC-MS data (not imaging); peakProcess is designed for spatially resolved spectra and may not scale efficiently for non-spatial MS.

## Inputs

- Cardinal object (unprocessed, loaded from Zenodo or local file)
- m/z feature matrix (10,200 features × 4,959 spectra, or similar dimensions)
- Raw spectra with intensity values

## Outputs

- Cleaned peak table (687 peaks, or dataset-specific count)
- Peak m/z values and aggregated intensities
- Cardinal object with peakProcess results slot

## How to apply

Load the unprocessed Cardinal object and apply TIC (total ion count) normalization to account for injection/ionization variability. Call Cardinal's peakProcess() function with SNR threshold=3, sampleSize=0.1 (use 10% of spectra for peak detection), and tolerance=0.5 m/z (merge peaks within ±0.5 m/z to account for mass calibration drift). The SNR=3 threshold filters peaks where signal intensity is at least 3× the local noise estimate. Set sampleSize conservatively to reduce computational burden while maintaining peak detection sensitivity. The function returns a cleaned peak table with m/z values and intensities. Validate that the output peak count matches the expected value (e.g., 687 peaks) and inspect the m/z distribution (e.g., 150–1000 m/z range) to confirm biological plausibility.

## Related tools

- **Cardinal** (Provides peakProcess() function for SNR-based peak detection and filtering in MS imaging data) — https://github.com/Vitek-Lab/Cardinal3-vignettes
- **SpaMTP** (Integrates Cardinal peak output with pathway and annotation workflows; inherits Cardinal functionality) — https://github.com/GenomicsMachineLearning/SpaMTP
- **Seurat** (Receives Cardinal objects converted via CardinalToSeurat() for downstream spatial analysis and visualization)
- **R** (Runtime environment for Cardinal and SpaMTP libraries)

## Examples

```
library(Cardinal); pig206 <- readRDS(url('https://zenodo.org/records/...')); pig206_norm <- normalize(pig206, method='tic'); peaks_cleaned <- peakProcess(pig206_norm, SNR=3, sampleSize=0.1, tolerance=0.5)
```

## Evaluation signals

- Output peak count matches expected value (e.g., 687 cleaned peaks for PIGII_206); if output differs significantly, re-check SNR threshold, sampleSize, or tolerance parameters.
- Cleaned peak m/z values fall within the documented range (e.g., 150–1000 m/z for pig fetus dataset); peaks outside this range suggest parameter drift or data quality issues.
- Peak intensity distribution is non-zero and continuous across spatial locations; isolated or singleton peaks may indicate overfitting with too-low SNR threshold.
- Subsequent spatial segmentation (e.g., SSC with k=8 clusters) produces interpretable spatial domains; poor clustering suggests peaks are still noisy or non-informative.
- Annotated metabolites using RefineLipids() or AnnotateSM() show expected biological relevance (e.g., lipids, amino acids, adenosine triphosphate); spurious annotations suggest peaks are artifactual.

## Limitations

- SNR threshold (=3) is data- and instrument-dependent; no universal cutoff is valid across all MS imaging platforms. The threshold may require optimization if expected peak count is not achieved.
- Tolerance (0.5 m/z) assumes m/z calibration error of ±0.5; datasets with higher mass calibration drift may merge distinct peaks or produce fragmentation artifacts.
- sampleSize=0.1 is a heuristic that trades speed for sensitivity; very large or sparse datasets may require adjustment to ensure peaks are detected in minority of spectra.
- peakProcess assumes spectra are pre-normalized (TIC); unnormalized spectra may produce biased SNR estimates and inconsistent peak detection across spatial regions.
- The article indicates 'Pseudo MS/MS-Based Refinement' and 'Refinement with Paired Targeted Metabolic Data' sections are marked 'To come!', suggesting validation workflows are incomplete and peak results may require manual curation.

## Evidence

- [other] Apply TIC normalization followed by peakProcess with SNR threshold=3, sampleSize=0.1, tolerance=0.5 mz to generate 687 cleaned peaks.: "Apply TIC normalization followed by peakProcess with SNR threshold=3, sampleSize=0.1, tolerance=0.5 mz to generate 687 cleaned peaks."
- [other] Load the unprocessed pig206 Cardinal object from Zenodo (10,200 m/z features, 4,959 spectra, m/z range 150–1000).: "Load the unprocessed pig206 Cardinal object from Zenodo (10,200 m/z features, 4,959 spectra, m/z range 150–1000)."
- [other] Summarize features using mean aggregation with Cardinal's summarizeFeatures().: "Summarize features using mean aggregation with Cardinal's summarizeFeatures()."
- [readme] SpaMTP inherits functionalities from two well established R packages (Cardinal and Seurat) to present a user-friendly platform for integrative spatial-omics analysis.: "SpaMTP inherits functionalities from two well established R packages (Cardinal and Seurat) to present a user-friendly platform for integrative spatial-omics analysis."
