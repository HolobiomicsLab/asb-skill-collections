---
name: feature-filtering-and-quality-control
description: Use when after batch correction and concentration normalization have been applied to a merged m/z peak table and metadata file, but before statistical testing or machine learning.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - MetaboShiny
  - R
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1007/s11306-020-01717-8
  title: MetaboShiny
evidence_spans:
- Welcome to the info page on MetaboShiny
- Welcome to the info page on MetaboShiny! We are currently on BioRXiv
- Through R
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metaboshiny_cq
    doi: 10.1007/s11306-020-01717-8
    title: MetaboShiny
  dedup_kept_from: coll_metaboshiny_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1007/s11306-020-01717-8
  all_source_dois:
  - 10.1007/s11306-020-01717-8
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# feature-filtering-and-quality-control

## Summary

Remove low-intensity m/z peaks and features below detection limits from metabolomic peak tables prior to statistical analysis. This quality-control step reduces noise and improves the signal-to-noise ratio of the normalized feature matrix.

## When to use

After batch correction and concentration normalization have been applied to a merged m/z peak table and metadata file, but before statistical testing or machine learning. Use this skill when your m/z feature table contains peaks with very low intensities across most samples, or when you need to enforce a minimum detection threshold to exclude features that may be instrument noise rather than true metabolite signals.

## When NOT to use

- Input is already a pre-filtered feature table or known to contain only confident identifications.
- Rare metabolite discovery is the primary goal and weak signals must be preserved for follow-up validation.
- Your study design requires retention of all detected peaks to assess the full dynamic range (e.g., biomarker screening where sensitivity is prioritized over specificity).

## Inputs

- Batch-corrected m/z peak intensity table (feature × sample matrix)
- Sample metadata with batch and concentration information
- Normalization parameters (applied concentration and batch factors)

## Outputs

- Filtered m/z feature table (reduced feature set, same sample count)
- Pre- and post-filtering intensity distribution plots for validation
- Quality-control report listing removed features and filtering thresholds applied

## How to apply

Apply one filtering method from the available statistical options: interquartile range (IQR), mean, median absolute deviation (MAD), median, relative standard deviation (stdev), standard deviation, or a non-parametric relative standard deviation approach. Each method identifies intensity outliers or features with insufficient signal consistency. Select the threshold that best suits your instrument's dynamic range and your study design (e.g., IQR is robust to outliers; MAD is more conservative). After filtering, visualize the pre- and post-filtered peak intensity distributions for a random sample of m/z values and samples to confirm that low-intensity noise has been removed while retaining true biological signal. Adjust parameters iteratively if the distribution suggests over-filtering (loss of weak but genuine metabolites) or under-filtering (retained noise).

## Related tools

- **MetaboShiny** (Interactive R/Shiny application providing filtering method selection, parameter tuning, and visualization of pre- and post-filtering distributions within the normalization module.) — https://github.com/joannawolthuis/MetaboShiny
- **R** (Computational environment for implementing filtering algorithms and generating statistical distributions.)

## Evaluation signals

- Pre- and post-filtering intensity distribution plots show removal of low-intensity tail without loss of high-intensity peaks.
- Feature count is reduced while sample count remains constant; proportion of retained features is consistent with the chosen filtering threshold.
- Filtered feature table contains no m/z values with zero or missing intensity across all samples (or meets the specified m/z missingness percentage threshold).
- Downstream statistical analyses (e.g., PCA, t-test) show improved signal-to-noise ratio and reduced spurious associations when using filtered versus unfiltered data.

## Limitations

- Filtering is a lossy operation; weak but genuine metabolite signals may be discarded if thresholds are set too stringently, potentially missing biomarkers with low abundance.
- Choice of filtering method (IQR vs. MAD vs. stdev) depends on data distribution assumptions; inappropriate method selection can introduce bias or fail to remove instrument noise.
- MetaboShiny's filtering and normalization are performed on combined positive and negative mode m/z peak data; separate method selection for each mode may be necessary if ionization modes have different noise profiles.
- No automated guidance is provided for parameter selection; visual inspection and iterative adjustment are required, introducing subjective judgment into the QC process.

## Evidence

- [intro] Apply filtering thresholds to remove low-intensity peaks and features below detection limits.: "Apply filtering thresholds to remove low-intensity peaks and features below detection limits."
- [readme] Filtering options include Interquartile range, Mean, Median absolute deviation, Median, Non-parametric relative standard deviation (stdev), Relative standard deviation (stdev), Standard deviation, and None.: "- **Filtering options**
  - Interquartile range
  - Mean
  - Median absolute deviation
  - Median
  - Non-parametric relative standard deviation (stdev)
  - Relative standard deviation (stdev)
  -"
- [readme] After normalization, the distribution of pre- and post-normalized peak values will be plotted for a randomly selected set of m/z values and samples, so the user can see how the data distribution has changed.: "After normalization, the distribution of pre- and post-normalized peak values will be plotted for a randomly selected set of m/z values and samples, so the user can see how the data distribution has"
