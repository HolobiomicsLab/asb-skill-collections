---
name: spectral-data-normalization-tic
description: Use when apply TIC normalization when you have raw, unprocessed mass spectrometry data (Cardinal objects or imaging matrices with 10,000+ m/z features and 1,000+ spectra) where signal intensity varies across spatial locations or samples due to instrumental drift, uneven sample preparation, or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - SpaMTP
  - dplyr
  - R
  - Cardinal
  techniques:
  - LC-MS
  - MS-imaging
derived_from:
- doi: 10.1101/2024.10.31.621429v1
  title: SpaMTP
- doi: 10.1101/2024.10.14.618269
  title: ''
evidence_spans:
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2024.10.31.621429v1
  all_source_dois:
  - 10.1101/2024.10.31.621429v1
  - 10.1101/2024.10.14.618269
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Spectral Data Normalization (TIC)

## Summary

Total Ion Current (TIC) normalization corrects for systematic variations in ion signal intensity across mass spectrometry imaging or LC-MS samples by dividing each spectrum's m/z intensities by the sum of all intensities in that spectrum. This preprocessing step is essential before peak detection or quantitative comparison, especially when acquisition conditions or sample loading vary.

## When to use

Apply TIC normalization when you have raw, unprocessed mass spectrometry data (Cardinal objects or imaging matrices with 10,000+ m/z features and 1,000+ spectra) where signal intensity varies across spatial locations or samples due to instrumental drift, uneven sample preparation, or variable ionization efficiency. Use it as a prerequisite step before peakProcess() or statistical analysis that assumes comparable signal scales across observations.

## When NOT to use

- Data already normalized or pre-processed by vendor software (check QC plots for intensity distributions across samples)
- Comparative analysis where absolute intensity (e.g., molar concentration estimates) must be preserved across replicates
- Spectra with extreme outliers or near-zero total ion current that would amplify noise after division

## Inputs

- Cardinal object with raw m/z intensities (unprocessed imaging matrix or LC-MS data)
- Mass spectra matrix (n_spectra × n_mz_features) with absolute ion counts
- Optional: pre-summarized feature matrix from Cardinal::summarizeFeatures()

## Outputs

- TIC-normalized Cardinal object or matrix (same dimensions, relative intensities 0–1)
- Spectra with unit-scaled ion current per observation
- Prepared input for peakProcess() or statistical comparison

## How to apply

Load the unprocessed spectral data into Cardinal (or equivalent MSI framework) and apply TIC normalization before any downstream processing. Divide each spectrum's intensity vector by its total ion current (sum of all m/z intensities in that spectrum), converting raw counts to relative proportions. This is typically performed on the full m/z range (e.g., 150–1000 Da) after optional mean-aggregation summarization of redundant features, and before peak detection with SNR thresholding or spatial segmentation. The normalized data becomes the input to peakProcess() with parameters such as SNR threshold=3, sampleSize=0.1, and tolerance=0.5 m/z. Verify normalization by confirming that each spectrum's summed intensity is now 1.0 (or that relative intensities fall within 0–1 range).

## Related tools

- **Cardinal** (Load, store, and apply TIC normalization to mass spectrometry imaging objects; provides normalization methods and integration with peakProcess()) — https://github.com/Vitek-Lab/Cardinal3-vignettes
- **SpaMTP** (High-level R interface for spatial metabolomics preprocessing, including normalization workflows before annotation and statistical analysis) — https://github.com/GenomicsMachineLearning/SpaMTP
- **R** (Programming environment for normalization implementation (arithmetic operations on intensity matrices))

## Examples

```
library(Cardinal); pig206 <- readRDS('pig206_raw.rds'); pig206_norm <- normalize(pig206, method='tic'); peaks <- peakProcess(pig206_norm, SNR=3, sampleSize=0.1, tolerance=0.5)
```

## Evaluation signals

- Each spectrum's summed intensity post-normalization equals 1.0 (or lies within expected normalized range [0, 1]) — verify by sum(spectrum) ≈ 1.0 for random sample of spectra
- Intensity distribution (histogram or violin plot) across samples becomes more uniform; coefficient of variation in median intensity per spectrum decreases
- Peak detection (peakProcess) yields expected number of cleaned peaks (e.g., 687 peaks in PIGII_206 pig fetus dataset) consistent with literature or positive control
- No negative values in normalized data; no spectra with NaN or Inf after division (check for near-zero or zero total ion current edge cases)
- Spatial visualizations (ImageMZPlot, ImageDimPlot) show consistent feature representation across tissue regions without systematic intensity gradients attributable to normalization artifacts

## Limitations

- TIC normalization assumes all m/z features carry biological signal; presence of dominant contaminants or chemical noise can distort normalization by inflating their relative abundance
- Sensitivity to spectra with extremely low or zero total ion current; such spectra may produce spurious high relative intensities after normalization and should be filtered or excluded pre-normalization
- Does not correct for m/z-dependent ionization efficiency or detector saturation; complementary methods (e.g., rank normalization, quantile normalization, or internal standard correction) may be needed for quantitative metabolite comparison
- Unsuitable for rare or low-abundance metabolites in complex mixtures where TIC is dominated by matrix components; consider robust normalization alternatives or m/z-specific weighting

## Evidence

- [other] Apply TIC normalization followed by peakProcess with SNR threshold=3, sampleSize=0.1, tolerance=0.5 mz to generate 687 cleaned peaks.: "Apply TIC normalization followed by peakProcess with SNR threshold=3, sampleSize=0.1, tolerance=0.5 mz to generate 687 cleaned peaks."
- [other] Load the unprocessed pig206 Cardinal object from Zenodo (10,200 m/z features, 4,959 spectra, m/z range 150–1000). Summarize features using mean aggregation with Cardinal's summarizeFeatures().: "Load the unprocessed pig206 Cardinal object from Zenodo (10,200 m/z features, 4,959 spectra, m/z range 150–1000). Summarize features using mean aggregation with Cardinal's summarizeFeatures()."
- [readme] Cardinal inherits functionalities from two well established R packages (Cardinal and Seurat) to present a user-friendly platform for integrative spatial-omics analysis.: "SpaMTP inherits functionalities from two well established R packages (Cardinal and Seurat) to present a user-friendly platform for integrative spatial-omics analysis."
