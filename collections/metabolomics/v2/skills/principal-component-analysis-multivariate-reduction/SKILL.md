---
name: principal-component-analysis-multivariate-reduction
description: Use when after normalizing and log-transforming lipidomics abundance
  data (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3935
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - lipidr
  - R
  - SummarizedExperiment
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.jproteome.0c00082
  title: lipidr
evidence_spans:
- Datasets can be easily downloaded and parsed into `LipidomicsExperiment` object
  using `lipidr` function `fetch_mw_study()`
- '`lipidr` allows users, to quickly explore public lipidomics experiments. `lipidr`
  provides an easy way to re-analyze and visualize these datasets.'
- Data Mining and Analysis of Lipidomics Datasets in R
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipidr_cq
    doi: 10.1021/acs.jproteome.0c00082
    title: lipidr
  dedup_kept_from: coll_lipidr_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.0c00082
  all_source_dois:
  - 10.1021/acs.jproteome.0c00082
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# principal-component-analysis-multivariate-reduction

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Apply PCA to normalized and log-transformed lipidomics data to reveal separation patterns between sample groups (e.g., benign vs. cancer phenotypes) and detect outlier samples with anomalous lipid profiles. This multivariate analysis serves as an unsupervised quality control and exploratory step prior to differential lipid abundance testing.

## When to use

After normalizing and log-transforming lipidomics abundance data (e.g., Area measures from Skyline or Metabolomics Workbench), apply this skill when you need to assess whether biological sample groups segregate in principal component space, identify samples with unusual lipid composition (candidates for removal), or visualize global lipidomic structure before univariate comparisons. Use it especially when sample sizes are modest and visual outlier detection is feasible.

## When NOT to use

- Input data is not log-transformed or normalized; PCA performance degrades on unnormalized, skewed count distributions.
- Sample metadata lacks clear phenotypic grouping or all samples are from a single category (no biological contrast to reveal).
- Dataset contains <5 samples; PCA becomes unreliable and outlier detection lacks statistical power.

## Inputs

- LipidomicsExperiment object with normalized and log-transformed Area measure
- Sample metadata with phenotype annotation (e.g., SampleType: benign, cancer, metastasis)

## Outputs

- PCA score plot (2D scatter) with samples colored by SampleType
- MVA results object (mvaresults) containing PC scores, loadings, and variance explained
- List of candidate outlier samples flagged for inspection or removal

## How to apply

Load a LipidomicsExperiment object (pre-normalized and logged via lipidr) and invoke mva() with method='PCA' on the Area measure to compute principal components. Generate a 2D score plot using plot_mva() with color_by='SampleType' and components=(1,2) to visualize separation and identify outliers. Inspect the plot for (a) visual clustering of sample groups (mild separation may be expected), (b) samples with large dispersion from their group centroid, and (c) overall data quality. Flag samples with extreme PC scores (e.g., samples 18 and 42 in ST001111) as candidates for removal if their dispersion is significantly larger than peers. Retain the mva results object for subsequent loadings and variable importance inspection.

## Related tools

- **lipidr** (Provides LipidomicsExperiment data structure, mva() function for PCA computation, and plot_mva() for interactive score plot visualization) — https://github.com/ahmohamed/lipidr
- **R** (Host language for lipidr and underlying statistical computation)
- **SummarizedExperiment** (Base Bioconductor class extended by LipidomicsExperiment for data representation)

## Examples

```
mvaresults <- mva(d, measure="Area", method="PCA")
plot_mva(mvaresults, color_by="SampleType", components=c(1,2))
```

## Evaluation signals

- Score plot shows visual separation or stratification of samples by SampleType (even if mild), confirming PCA captured phenotype-relevant variation.
- Variance explained by PC1 and PC2 is documented and >5–10% per component, indicating meaningful signal capture (not random noise).
- Outlier samples (flagged by inspection) have PC scores ≥2–3 standard deviations from group means; verify they correlate with technical issues, sample degradation, or mislabeling.
- After removing flagged outliers and re-running PCA, group separation improves or variance explained per component increases, validating removal.
- Loadings (variable contributions) identify lipid classes or individual lipids that drive PC1 and PC2; should be interpretable (e.g., PCs and PGs dominate PC1 in cancer vs. benign).

## Limitations

- PCA assumes linear relationships; non-linear structure (e.g., multi-modal distributions) may be obscured.
- Outlier detection via visual inspection of PC scores is subjective and sensitive to sample size; formal statistical tests (e.g., Mahalanobis distance) are recommended for large cohorts.
- Cancer stage does not appear to affect lipid molecules profiled in the ST001111 experiment (as noted in the article), so PCA may not resolve all phenotypic subdivisions; hierarchical or other non-linear methods may be needed.
- Small but detectable confounding (e.g., Race effect in ST001111) can inflate or distort PC1 or PC2; include relevant covariates in post-hoc factorial analysis if such effects are suspected.

## Evidence

- [other] PCA revealed mild separation between benign and cancer samples but not between cancer and metastasis, with samples 18 and 42 identified as outliers with significantly large dispersion warranting consideration for removal.: "PCA revealed mild separation between benign and cancer samples but not between cancer and metastasis, with samples 18 and 42 identified as outliers with significantly large dispersion warranting"
- [other] Apply PCA using mva() with method='PCA' on the Area measure. Generate a score plot from mva results using plot_mva() with color_by='SampleType' and components=(1,2).: "Apply PCA using mva() with method='PCA' on the Area measure. Generate a score plot from mva results using plot_mva() with color_by='SampleType' and components=(1,2)."
- [intro] lipidr provides an easy way to re-analyze and visualize these datasets.: "lipidr provides an easy way to re-analyze and visualize these datasets."
- [intro] We can see mild separation between benign and cancer samples, but not between cancer and metastasis.: "We can see mild separation between benign and cancer samples, but not between cancer and metastasis."
- [intro] mvaresults = mva(d, measure="Area", method="PCA") plot_mva(mvaresults, color_by="SampleType", components = c(1,2)): "mvaresults = mva(d, measure="Area", method="PCA") plot_mva(mvaresults, color_by="SampleType", components = c(1,2))"
