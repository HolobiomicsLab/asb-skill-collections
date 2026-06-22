---
name: gcxgc-preprocessed-data-handling
description: Use when you have preprocessed individual GCxGC-MS chromatograms (each smoothed with Whittaker smoother, baseline-corrected with asymmetric least squares, and aligned against a reference using 2D correlation optimized warping) and need to consolidate them into a single analytical object for.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3365
  - http://edamontology.org/topic_0091
  tools:
  - RGCxGC
  - R
  - mixOmics
  - colorRamps
  techniques:
  - GC-MS
  - tandem-MS
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

# GCxGC Preprocessed Data Handling

## Summary

This skill encompasses the assembly, alignment, and multivariate analysis of preprocessed two-dimensional gas chromatography–mass spectrometry (GCxGC-MS) data after individual samples have undergone smoothing, baseline correction, and peak alignment. It transforms aligned chromatogram objects into unified data structures suitable for multiway principal component analysis (MPCA) to reveal group differences in metabolite profiles.

## When to use

You have preprocessed individual GCxGC-MS chromatograms (each smoothed with Whittaker smoother, baseline-corrected with asymmetric least squares, and aligned against a reference using 2D correlation optimized warping) and need to consolidate them into a single analytical object for unsupervised or supervised multivariate analysis. Use this skill when your goal is to compare metabolite patterns across sample groups (e.g., diseased vs. control) or identify biomarker candidates.

## When NOT to use

- Chromatograms have not yet undergone baseline correction or smoothing; perform preprocessing (baseline_corr, wsmooth) first.
- Individual samples have not been aligned to a common reference; use twod_cow or batch_2DCOW before joining.
- Your goal is to extract or identify individual metabolite peaks rather than discover global metabolic patterns; use targeted peak detection instead.
- Sample size is very small (n < 3 per group); MPCA requires sufficient samples to estimate meaningful components.

## Inputs

- Multiple aligned chromatogram objects (output from twod_cow or batch_2DCOW)
- Sample metadata or group labels (optional, for interpretation)

## Outputs

- Unified chromatogram object (from join_chromatograms)
- MPCA score matrix (sample × component)
- MPCA loading matrices (retention time dimension 1 × component, retention time dimension 2 × component)
- MPCA summary statistics (variance per component, cumulative variance)

## How to apply

After all individual samples have been preprocessed via smoothing (wsmooth), baseline correction (baseline_corr), and peak alignment (twod_cow or batch_2DCOW), use the join_chromatograms function to combine all aligned chromatogram objects into a single R object. Then apply multiway principal component analysis (MPCA) using the m_prcomp function to decompose the combined 2D chromatographic data tensor. Extract and visualize results using the scores function to retrieve the score matrix, plot_loading to display loadings across dimensions, and print_mpca to summarize variance explained and component contributions. The rationale is that MPCA preserves the inherent dimensionality of GCxGC data (retention time in first dimension, retention time in second dimension, and sample) while identifying latent metabolic patterns that univariate peak picking might miss.

## Related tools

- **RGCxGC** (Provides join_chromatograms, m_prcomp, scores, plot_loading, and print_mpca functions for data consolidation and MPCA computation) — https://github.com/DanielQuiroz97/RGCxGC
- **mixOmics** (Optional downstream tool for supervised multivariate modeling (PLS-DA, sparse PLS) if group labels are known)
- **colorRamps** (Provides color palettes (matlab.like, matlab.like2) for MPCA loading visualizations)

## Examples

```
# Combine preprocessed aligned chromatograms and perform MPCA
combined <- join_chromatograms(aligned_samples_list)
mpca_result <- m_prcomp(combined, ncomp = 3)
scores_df <- scores(mpca_result)
plot_loading(mpca_result, comp = c(1, 2))
print(print_mpca(mpca_result))
```

## Evaluation signals

- join_chromatograms produces a single R object with consistent dimensionality (2D chromatographic space × number of samples) without data loss or duplication.
- MPCA cumulative variance explained by first 2–3 components is ≥ 60%, indicating adequate data compression and interpretability.
- Score plot (samples in PC1 vs. PC2 space) shows visual separation or clustering consistent with known sample groups or phenotypes.
- Loading plots highlight retention time regions (1st and 2nd dimensions) with highest absolute loadings, interpretable as metabolite-rich zones or compound retention patterns.
- Reproducibility check: re-running join_chromatograms and m_prcomp on the same preprocessed dataset yields identical scores, loadings, and variance statistics.

## Limitations

- MPCA assumes aligned chromatograms are already in comparable units and scales; severe batch effects or instrumental drift not corrected in preprocessing will propagate into components.
- The method is sensitive to outlier samples; robust MPCA variants or outlier detection should be considered for datasets with suspected instrumental anomalies.
- Interpretation of MPCA components requires domain knowledge; high variance in a component does not guarantee biological relevance without external validation (e.g., MS/MS identification, ROC curves).
- Memory usage scales with the tensor size (retention time × retention time × samples); very large datasets or high-resolution chromatograms may require subsampling or distributed computation.

## Evidence

- [intro] join_chromatograms_preprocessing: "Once the chromatograms are already preprocessed, it has to be in a single R object. To meet this requirement, the join_chromatograms functions does it."
- [intro] preprocessing_rationale: "noise can be significantly reduced by using preprocessing algorithms, herein smoothing, baseline correction, and peak alignment. Then, in order to reveal differences between groups, multivariate"
- [intro] mpca_application: "After signal preprocessing, MPCA can be performed over the dataset by using the m_prcomp functions."
- [intro] mpca_extraction_visualization: "you can access to the score matrix through scores function, or plot the loading matrix with the plot_loading function. Finally, the MPCA summary can be retrieved with the print_mpca function."
- [intro] twod_cow_alignment_workflow: "peak alignment of a single sample against a reference chromatogram can be performed based on the two-dimensional correlation optimized warping (2DCOW) algorithm. Alternatively, multiple sample"
- [readme] preprocessing_algorithms_overview: "RGCxGC offers common pre-processing algorithms for signal enhancement, such as baseline correction based on asymetric least squares, smoothing based on the Whittaker smoother, and peak alignment 2D"
