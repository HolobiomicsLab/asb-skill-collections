---
name: metabolite-biomarker-classification-via-unsupervised-projection
description: Use when after preprocessing GCxGC-MS chromatograms (smoothing, baseline correction, peak alignment) when you need to uncover latent metabolite patterns that distinguish biological groups without prior class labels. Specifically useful for exploratory separation of disease states (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3935
  edam_topics:
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_3172
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1016/j.microc.2020.104830
  all_source_dois:
  - 10.1016/j.microc.2020.104830
  - 10.1371/journal.pntd.0006215
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-biomarker-classification-via-unsupervised-projection

## Summary

Extract and visualize principal component scores from preprocessed GCxGC-MS chromatogram data to reveal multivariate metabolite structure and separate sample groups (e.g., carriage vs. control) in an unsupervised manner. This skill uses multiway PCA to project high-dimensional chromatographic signals into a reduced score space where biomarker patterns become interpretable.

## When to use

Apply this skill after preprocessing GCxGC-MS chromatograms (smoothing, baseline correction, peak alignment) when you need to uncover latent metabolite patterns that distinguish biological groups without prior class labels. Specifically useful for exploratory separation of disease states (e.g., chronic typhoid carriage vs. controls) or phenotypic cohorts where the discriminant metabolites are unknown a priori.

## When NOT to use

- Input chromatograms have not been preprocessed (raw signals contain baseline drift, noise, or misaligned peaks); perform smoothing, baseline correction, and 2DCOW alignment first.
- Sample groups are already well-characterized by targeted metabolite assays; supervised methods (e.g., PLS-DA via mixOmics) may be more powerful for biomarker validation.
- Chromatogram intensities span multiple orders of magnitude and scale=FALSE is inappropriate; consider scale=TRUE if relative metabolite abundance (not absolute intensity) is the focus.

## Inputs

- preprocessed 2D chromatogram matrix (NetCDF-imported, smoothed, baseline-corrected, and peak-aligned via RGCxGC)
- joined chromatogram R object from join_chromatograms()
- metadata associating each chromatogram to a sample group (e.g., carriage, control)

## Outputs

- MPCA scores matrix (samples × principal components)
- MPCA loadings matrix (retention time regions × principal components)
- 2D or 3D scores scatter plot showing sample clustering by group
- summary statistics from print_mpca() (explained variance, eigenvalues)

## How to apply

Run multiway principal component analysis (m_prcomp) on the joined, preprocessed chromatogram matrix with center=TRUE and scale=FALSE to preserve the magnitude of metabolite signals. Extract the scores matrix using the scores() function to obtain the projection of each sample into principal component space. Visualize the scores plot to assess whether samples cluster by group; if clear separation emerges, it indicates that the multivariate metabolite structure inherently distinguishes the phenotypes. The choice of center=TRUE and scale=FALSE is grounded in the metabolomics principle that signal intensity carries quantitative meaning—baseline-corrected chromatograms should be centered but not variance-scaled, to avoid inflating noise-driven features. Examine the loading plots (via plot_loading()) to identify which retention-time regions (m/z and 1D retention time coordinates) contribute most to group separation.

## Related tools

- **RGCxGC** (provides m_prcomp function for multiway PCA, scores() and plot_loading() for result extraction/visualization, and preprocessing pipeline (wsmooth, baseline_corr, twod_cow, join_chromatograms)) — https://github.com/DanielQuiroz97/RGCxGC
- **mixOmics** (provides supervised and semi-supervised multivariate methods (e.g., PLS-DA) for downstream biomarker validation after unsupervised clustering)
- **colorRamps** (supplies color palettes (matlab.like, matlab.like2) for chromatogram and scores plot visualization)

## Examples

```
scores_matrix <- scores(m_prcomp(join_chromatograms(preproc_chroms), center=TRUE, scale=FALSE)); plot(scores_matrix[,1:2], col=sample_groups, main='MPCA Scores: S. typhi Carriage vs. Control')
```

## Evaluation signals

- Scores plot shows visually distinct clusters by sample group; within-group samples cluster tightly, between-group separation is clear.
- Loadings plot (via plot_loading) identifies non-random, interpretable retention-time regions (metabolite signatures) that drive group separation; peak heights in loading profile correspond to known chromatographic features.
- print_mpca() output shows cumulative explained variance ≥70% in first 2–3 PCs, indicating that group structure is captured by a small number of latent factors.
- Permutation or cross-validation test (if performed) shows that observed separation is significantly stronger than random reassignment of group labels.
- Preprocessed chromatogram matrix has consistent dimensions (rows = samples, columns = 1D retention time × 2D retention time bins) and no missing values after joining.

## Limitations

- MPCA assumes linear relationships among metabolite signals; non-linear metabolite co-regulation may be missed.
- The scores plot is unsupervised and may reveal batch effects, instrumental drift, or other confounders rather than true biomarker differences; cross-validation against sample metadata is essential.
- Choice of center=TRUE and scale=FALSE is sensitive to preprocessing quality; poor baseline correction or peak alignment will propagate into misleading scores.
- MPCA does not directly identify individual metabolite biomarkers; loadings indicate contributing regions, but annotation (MS fragmentation matching, retention index databases) requires additional analysis (e.g., via supervised methods or targeted follow-up).
- The method requires a sufficient number of chromatograms per group to estimate reliable principal component structure; small sample sizes may yield unstable or non-reproducible scores.

## Evidence

- [other] The MPCA scores matrix can be extracted from the preprocessed MTBLS579 dataset (6 chromatograms across S. typhy carriage and control groups) using the scores() function after running m_prcomp with center=TRUE and scale=FALSE: "The MPCA scores matrix can be extracted from the preprocessed MTBLS579 dataset (6 chromatograms across S. typhy carriage and control groups) using the scores() function after running m_prcomp with"
- [intro] After signal preprocessing, MPCA can be performed over the dataset by using the m_prcomp functions. you can access to the score matrix through scores function, or plot the loading matrix with the plot_loading function.: "After signal preprocessing, MPCA can be performed over the dataset by using the m_prcomp functions. you can access to the score matrix through scores function, or plot the loading matrix with the"
- [intro] noise can be significantly reduced by using preprocessing algorithms, herein smoothing, baseline correction, and peak alignment. Then, in order to reveal differences between groups, multivariate: "Preprocessing steps including smoothing, baseline correction, and peak alignment can reduce noise and reveal differences between groups for multivariate analysis"
- [readme] RGCxGC offers common pre-processing algorithms for signal enhancement, such as baseline correction based on asymetric least squares, smoothing based on the Whittaker smoother, and peak alignment 2D COW.: "RGCxGC offers common pre-processing algorithms for signal enhancement, such as baseline correction based on asymetric least squares, smoothing based on the Whittaker smoother, and peak alignment 2D"
- [readme] the multiway principal component analysis is implemented based on the Wold's approach: "Furthermore, the multiway principal component analysis is implemented based on the Wold's approach"
