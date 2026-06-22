---
name: peak-intensity-distribution-analysis
description: Use when after executing feature detection and quantification on raw LC-MS data (mzML or NetCDF format) using an automated pipeline such as MetaboAnalystR 4.0, and before proceeding to downstream normalization, scaling, or functional analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0091
  tools:
  - MetaboAnalystR
  - MetaboAnalystR 4.0
  techniques:
  - LC-MS
  - tandem-MS
derived_from:
- doi: 10.1038/s41467-024-48009-6
  title: metaboanalystr
evidence_spans:
- 'MetaboAnalystR 4.0: a unified LC-MS workflow for global metabolomics'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metaboanalystr
    doi: 10.1038/s41467-024-48009-6
    title: metaboanalystr
  dedup_kept_from: coll_metaboanalystr
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-024-48009-6
  all_source_dois:
  - 10.1038/s41467-024-48009-6
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# peak-intensity-distribution-analysis

## Summary

Computation and statistical characterization of mass spectrometry peak intensity values across LC-MS feature tables to quantify detection sensitivity, data quality, and feature abundance distributions. Essential for validating feature detection output and assessing the dynamic range and noise profile of metabolomics datasets.

## When to use

After executing feature detection and quantification on raw LC-MS data (mzML or NetCDF format) using an automated pipeline such as MetaboAnalystR 4.0, and before proceeding to downstream normalization, scaling, or functional analysis. Apply this skill when you need to characterize the shape, spread, and outliers in peak intensities to justify preprocessing decisions (e.g., missing value imputation thresholds, log transformation, outlier removal).

## When NOT to use

- Input is already a normalized or log-transformed feature table with intensity statistics already computed and validated.
- Analysis goal is compound identification or functional pathway inference; use this skill for data quality control, not for biological interpretation.
- Raw spectra have not yet been processed into a feature table (i.e., peak picking and alignment have not been performed).

## Inputs

- Feature intensity matrix from MetaboAnalystR 4.0 LC-MS unified workflow (rows = features, columns = samples, values = peak intensity or area)
- Raw LC-MS data in mzML or NetCDF format (optional, if re-extracting intensities)

## Outputs

- Summary statistics table (mean, median, SD, min, max intensity per feature or globally)
- Intensity distribution histogram or density plot
- Feature-level coefficient of variation (CV) table
- Outlier flagging report (samples or features with extreme intensity values)
- Diagnostic plots (boxplot, quantile–quantile plot) for assessing normality and transformation needs

## How to apply

Extract the feature intensity matrix (rows = detected features, columns = samples) from the MetaboAnalystR 4.0 LC-MS workflow output. Compute univariate summary statistics for all peak intensity values: mean, median, standard deviation, minimum, and maximum. Generate a histogram or density plot to visualize the distribution shape (e.g., right-skewed, bimodal, or log-normal). Check for extreme outliers using boxplots or z-score thresholding (typically |z| > 3). Document the intensity range (min–max) and coefficient of variation (CV = SD / mean) per feature to assess replicate consistency. These diagnostics inform whether log-transformation, quantile normalization, or robust scaling is appropriate before statistical analysis.

## Related tools

- **MetaboAnalystR 4.0** (Performs automated LC-MS feature detection, quantification, and generates the feature intensity matrix that serves as input to peak-intensity distribution analysis.) — https://github.com/xia-lab/MetaboAnalystR

## Examples

```
# After loading a feature intensity matrix from MetaboAnalystR 4.0:
feature_stats <- data.frame(
  mean_intensity = colMeans(intensity_matrix),
  median_intensity = apply(intensity_matrix, 2, median),
  sd_intensity = apply(intensity_matrix, 2, sd),
  min_intensity = apply(intensity_matrix, 2, min),
  max_intensity = apply(intensity_matrix, 2, max),
  cv = apply(intensity_matrix, 2, sd) / colMeans(intensity_matrix)
)
hist(log10(colMeans(intensity_matrix)), breaks=50, main='Peak Intensity Distribution (log10 scale)')
```

## Evaluation signals

- Feature table dimensions are correctly extracted: number of rows matches number of detected features, number of columns matches number of samples.
- Summary statistics (mean, median, SD, min, max) are mathematically consistent and within expected ranges for the instrument and sample type (e.g., no negative intensities, min < median < mean for right-skewed distributions).
- Intensity distribution visualization shows expected shape (typically right-skewed for LC-MS peak areas); bimodal or severely multimodal distributions warrant investigation of batch effects or data quality issues.
- Coefficient of variation across replicates is reasonable (typically 10–30% for high-quality LC-MS metabolomics data); CV > 50% flags features with poor reproducibility.
- Outlier detection is reproducible and justified: documented criteria (e.g., z-score > 3, interquartile range * 1.5) are applied consistently, and flagged outliers are visually confirmed in boxplots.

## Limitations

- Summary statistics alone do not distinguish between true biological variation and technical noise; validation against blank/QC samples is needed.
- Peak intensity distributions are highly dependent on sample preparation, ionization efficiency, and instrumental parameters; direct comparison across different LC-MS platforms or methods is not valid without normalization.
- Extreme outliers may reflect authentic features (e.g., isotopologue peaks, adducts) or instrumental artifacts; statistical flagging alone does not determine biological relevance.
- The README states that MetaboAnalystR 4.0 demonstrates improved quantification accuracy and > 10% higher feature detection versus prior versions, but individual dataset results depend on parameter tuning and data quality; no universal thresholds for acceptable intensity ranges are provided.

## Evidence

- [other] Extract feature table dimensions (number of rows as features, number of columns as samples) and compute summary statistics on peak intensity values (mean, median, standard deviation, min, max).: "Extract feature table dimensions (number of rows as features, number of columns as samples) and compute summary statistics on peak intensity values (mean, median, standard deviation, min, max)."
- [readme] MetaboAnalystR 4.0 contains the R functions and libraries underlying the popular MetaboAnalyst web server, including metabolomic data analysis, visualization, and functional interpretation.: "MetaboAnalystR 4.0 contains the R functions and libraries underlying the popular MetaboAnalyst web server, including metabolomic data analysis, visualization, and functional interpretation."
- [readme] an auto-optimized feature detection and quantification module for LC-MS1 spectra processing: "an auto-optimized feature detection and quantification module for LC-MS1 spectra processing"
- [readme] Serial dilutions demonstrate that MetaboAnalystR 4.0 can accurately detect and identify > 10% more high-quality MS and MS/MS features.: "Serial dilutions demonstrate that MetaboAnalystR 4.0 can accurately detect and identify > 10% more high-quality MS and MS/MS features."
