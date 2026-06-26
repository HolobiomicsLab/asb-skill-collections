---
name: multiway-principal-component-analysis-score-extraction
description: Use when after preprocessing and aligning 2D chromatogram data (baseline
  correction, smoothing, peak alignment) and after running m_prcomp multiway PCA on
  the joined chromatogram matrix.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - RGCxGC
  - R
  - mixOmics
  techniques:
  - GC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1016/j.microc.2020.104830
  title: RGCxGC
- doi: 10.1371/journal.pntd.0006215
  title: ''
evidence_spans:
- The goal of RGCxGC is to provide an easy-to-use platform to analyze two-dimensional
  gas chromatography data.
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Multiway Principal Component Analysis Score Extraction

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Extract principal component scores from preprocessed GCxGC-MS chromatogram data after multiway PCA decomposition using Wold's approach. This skill recovers the projection of individual samples onto the reduced principal component space, enabling downstream sample-level visualization and classification.

## When to use

Apply this skill after preprocessing and aligning 2D chromatogram data (baseline correction, smoothing, peak alignment) and after running m_prcomp multiway PCA on the joined chromatogram matrix. Use it when you need to obtain sample-level coordinates in PC space for visualization, clustering, or as input to supervised classification models (e.g., mixOmics).

## When NOT to use

- Input chromatograms have not been preprocessed (smoothed, baseline-corrected, peak-aligned) — scores will reflect noise and misalignment artifacts.
- m_prcomp has not yet been run on the chromatogram matrix — the m_prcomp object does not exist.
- Scores are not the appropriate output — if you need loading vectors or explained variance, use plot_loading() or print_mpca() functions instead.

## Inputs

- m_prcomp object (output from multiway PCA on preprocessed, aligned chromatogram matrix)
- Preprocessed 2D chromatogram data (joined via join_chromatograms function)

## Outputs

- MPCA scores matrix (samples × principal components)
- Sample coordinates in reduced PC space suitable for visualization and classification

## How to apply

After running m_prcomp with specified parameters (e.g., center=TRUE, scale=FALSE), call the scores() function on the resulting m_prcomp object to extract the scores matrix. This matrix contains principal component coordinates for each preprocessed chromatogram (rows) across the computed principal components (columns). The choice of center and scale parameters affects the interpretation: center=TRUE removes mean intensity offsets, while scale=FALSE preserves intensity variance structure without standardization. Verify that the extracted scores matrix has dimensions matching the number of input chromatograms and the number of retained PCs.

## Related tools

- **RGCxGC** (Contains m_prcomp function for multiway PCA decomposition and scores() function for score matrix extraction) — https://github.com/DanielQuiroz97/RGCxGC
- **mixOmics** (Downstream supervised classification using extracted MPCA scores as input features)

## Examples

```
scores_matrix <- scores(m_prcomp_object)
```

## Evaluation signals

- Scores matrix dimensions equal (n_chromatograms, n_retained_PCs) — verify shape matches input and m_prcomp configuration.
- All scores are numeric and finite (no NaN or Inf) after extraction.
- Scores reflect separation between study groups (e.g., S. typhoid carriage vs. control) when visualized in PC1 vs. PC2 plane — absence of separation suggests preprocessing or parameter issues.
- Scores are reproducible across independent runs with identical input and m_prcomp parameters (center, scale, rank).
- Sum of explained variance by extracted PCs matches the cumulative variance reported by print_mpca() function.

## Limitations

- Score quality depends entirely on preprocessing quality — poor baseline correction, incomplete peak alignment, or residual noise will propagate into scores.
- center=FALSE and scale=FALSE preserve raw intensity scale, making scores sensitive to instrumental drift or uneven sample concentration; centering and scaling may be needed for robust biological interpretation.
- MPCA assumes trilinear decomposition (Wold's approach); nonlinear structure in chromatogram data may not be captured and should be validated via residual analysis.
- Scores are specific to the selected number of retained principal components; choosing too few PCs loses information, too many overfits noise.

## Evidence

- [other] The MPCA scores matrix can be extracted from the preprocessed MTBLS579 dataset (6 chromatograms across S. typhy carriage and control groups) using the scores() function after running m_prcomp with center=TRUE and scale=FALSE, showing the projection of samples in the reduced principal component space.: "The MPCA scores matrix can be extracted from the preprocessed MTBLS579 dataset using the scores() function after running m_prcomp with center=TRUE and scale=FALSE, showing the projection of samples"
- [intro] After signal preprocessing, MPCA can be performed over the dataset by using the m_prcomp functions.: "After signal preprocessing, MPCA can be performed over the dataset by using the m_prcomp functions."
- [intro] you can access to the score matrix through scores function, or plot the loading matrix with the plot_loading function. Finally, the MPCA summary can be retrieved with the print_mpca function.: "you can access to the score matrix through scores function, or plot the loading matrix with the plot_loading function."
- [readme] RGCxGC offers common pre-processing algorithms for signal enhancement, such as baseline correction based on asymetric least squares, smoothing based on the Whittaker smoother, and peak alignment 2D COW. Furthermore, the multiway principal component analysis is implemented based on the Wold's approach.: "the multiway principal component analysis is implemented based on the Wold's approach."
- [intro] Preprocessing steps including smoothing, baseline correction, and peak alignment can reduce noise and reveal differences between groups for multivariate analysis: "Preprocessing steps including smoothing, baseline correction, and peak alignment can reduce noise and reveal differences between groups for multivariate analysis"
