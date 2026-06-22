---
name: gcxgc-ms-multivariate-analysis
description: Use when after preprocessing a set of aligned 2D-TIC (two-dimensional Total Intensity Chromatogram) matrices from GCxGC-MS experiments—when you have multiple samples across distinct biological groups (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0602
  tools:
  - RGCxGC
  - R
  - mixOmics
  - colorRamps
derived_from:
- doi: 10.1016/j.microc.2020.104830
  title: RGCxGC
- doi: 10.1371/journal.pntd.0006215
  title: ''
evidence_spans:
- The goal of RGCxGC is to provide an easy-to-use platform to analyze two-dimensional gas chromatography data.
- This is the vignette to explain the implementation of RGCxGC package.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_rgcxgc_cq
    doi: 10.1016/j.microc.2020.104830
    title: RGCxGC
  dedup_kept_from: coll_rgcxgc_cq
schema_version: 0.2.0
---

# GCxGC-MS Multivariate Analysis

## Summary

Applies multiway principal component analysis (MPCA) to preprocessed two-dimensional gas chromatography–mass spectrometry data to reveal multivariate structure and group differences in metabolite profiles. This skill extracts and interprets principal component scores and loadings from chromatographic intensity matrices to identify discriminative metabolite patterns.

## When to use

After preprocessing a set of aligned 2D-TIC (two-dimensional Total Intensity Chromatogram) matrices from GCxGC-MS experiments—when you have multiple samples across distinct biological groups (e.g., disease vs. control) and need to uncover latent structure or validate that preprocessing has adequately separated group signals in reduced dimensions.

## When NOT to use

- Input chromatograms have not undergone baseline correction and smoothing—preprocessing artifacts will dominate the multivariate structure.
- Samples have not been peak-aligned using 2DCOW or equivalent—misalignment will inflate noise in the loading structure.
- You need supervised classification or biomarker discovery—use mixOmics functions for supervised PLS-DA instead.

## Inputs

- Preprocessed 2D chromatogram matrix (aligned across samples, baseline-corrected, smoothed)
- Joined chromatograms R object (output of join_chromatograms function)
- Sample group labels or metadata (for interpretation of scores)

## Outputs

- MPCA scores matrix (sample coordinates in principal component space)
- MPCA loadings matrix (contribution of chromatographic regions to each PC)
- Scree plot or variance explained per component
- Score plot visualization (samples projected onto PCs, colored by group)

## How to apply

Load preprocessed chromatograms joined into a single R object using join_chromatograms(). Apply m_prcomp() with center=TRUE and scale=FALSE to perform MPCA on the 2D intensity matrix, which projects samples onto principal components while preserving the variance structure. Extract the scores matrix using scores() to obtain sample coordinates in PC space, revealing group separation; extract and visualize loadings with plot_loading() to identify which regions of the chromatogram drive the separation. Validate group separation by inspecting score plots and confirm signal-to-noise improvement by comparing within-group vs. between-group variance ratios. The choice of center=TRUE and scale=FALSE preserves absolute intensity information, appropriate when baseline-corrected and smoothed signals are in consistent units across samples.

## Related tools

- **RGCxGC** (Provides m_prcomp for multiway PCA, scores() and plot_loading() for MPCA result extraction and visualization; includes preprocessing pipeline (baseline_corr, wsmooth, twod_cow, join_chromatograms).) — https://github.com/DanielQuiroz97/RGCxGC
- **mixOmics** (Optional downstream tool for supervised multivariate analysis (e.g., PLS-DA) if biomarker discrimination is the goal.)
- **colorRamps** (Provides color palettes (matlab.like, matlab.like2) for enhanced visualization of 2D chromatograms and heatmaps.)

## Examples

```
scores_matrix <- scores(m_prcomp(joined_chrom_matrix, center=TRUE, scale=FALSE)); plot_loading(m_prcomp_obj); print_mpca(m_prcomp_obj)
```

## Evaluation signals

- Score plot shows clear spatial separation between biological groups (e.g., S. typhy carriage vs. control) along first 1–2 principal components.
- Scree plot indicates that 2–4 components capture ≥70% cumulative variance, suggesting meaningful dimensionality reduction without over-fitting.
- Loadings heatmap reveals concentrated regions of high contribution (e.g., specific retention-time windows), not uniformly distributed noise.
- Scores have lower within-group variance and higher between-group variance compared to raw intensity matrices, confirming preprocessing efficacy.
- Results are reproducible across independent runs with the same center=TRUE, scale=FALSE parameters on the same aligned dataset.

## Limitations

- MPCA assumes linear relationships; nonlinear structure may not be captured.
- Results depend critically on quality of preprocessing (baseline correction, smoothing, alignment)—poor alignment or residual baseline will obscure true metabolite variance.
- Interpretation of loadings can be ambiguous in high-dimensional chromatographic data; requires correlation with reference standards or external metabolite databases to assign chemical identity.
- Small sample size (e.g., 6 samples as in MTBLS579) increases risk of overfitting; PC scores should be validated on independent test data before claiming biomarker utility.

## Evidence

- [intro] After signal preprocessing, MPCA can be performed over the dataset by using the m_prcomp functions.: "After signal preprocessing, MPCA can be performed over the dataset by using the m_prcomp functions."
- [intro] you can access to the score matrix through scores function, or plot the loading matrix with the plot_loading function.: "you can access to the score matrix through scores function, or plot the loading matrix with the plot_loading function."
- [readme] RGCxGC offers common pre-processing algorithms for signal enhancement, such as baseline correction based on asymetric least squares, smoothing based on the Whittaker smoother, and peak alignment 2D COW.: "RGCxGC offers common pre-processing algorithms for signal enhancement, such as baseline correction based on asymetric least squares, smoothing based on the Whittaker smoother, and peak alignment 2D"
- [other] The MPCA scores matrix can be extracted from the preprocessed MTBLS579 dataset (6 chromatograms across S. typhy carriage and control groups) using the scores() function after running m_prcomp with center=TRUE and scale=FALSE.: "The MPCA scores matrix can be extracted from the preprocessed MTBLS579 dataset (6 chromatograms across S. typhy carriage and control groups) using the scores() function after running m_prcomp with"
- [intro] Preprocessing steps including smoothing, baseline correction, and peak alignment can reduce noise and reveal differences between groups for multivariate analysis.: "Preprocessing steps including smoothing, baseline correction, and peak alignment can reduce noise and reveal differences between groups for multivariate analysis."
