---
name: lipid-sample-separation-visualization
description: Use when after normalizing and log-transforming lipidomics intensity data in a LipidomicsExperiment object, use this skill when you need to assess whether your sample groups (e.
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
derived_from:
- doi: 10.1021/acs.jproteome.0c00082
  title: lipidr
evidence_spans:
- Datasets can be easily downloaded and parsed into `LipidomicsExperiment` object using `lipidr` function `fetch_mw_study()`
- '`lipidr` allows users, to quickly explore public lipidomics experiments. `lipidr` provides an easy way to re-analyze and visualize these datasets.'
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

# lipid-sample-separation-visualization

## Summary

Principal component analysis (PCA) applied to normalized and logged lipidomics intensity data to visualize sample clustering by phenotype and detect outlier samples with anomalous lipid profiles. This skill reveals whether biological groups (benign, cancer, metastasis) separate in reduced dimensionality space and identifies samples warranting removal due to high dispersion.

## When to use

After normalizing and log-transforming lipidomics intensity data in a LipidomicsExperiment object, use this skill when you need to assess whether your sample groups (e.g., disease stage, treatment arm) cluster distinctly on the first two principal components, and to identify outlier samples whose lipid profiles deviate significantly from their assigned group. Particularly useful before differential abundance analysis to ensure sample homogeneity within groups.

## When NOT to use

- Input intensity data has not been normalized and log-transformed; apply preprocessing steps first.
- Sample size is very small (< 6 total samples); PCA may be unstable and visual separation unreliable.
- The research question requires supervised classification (e.g., predictive modeling); use PLS-DA or OPLS-DA instead.

## Inputs

- LipidomicsExperiment object with pre-normalized and pre-logged intensity measure (e.g., 'Area')
- Sample metadata with phenotype classification (SampleType, Cancer Stage, or equivalent grouping variable)

## Outputs

- PCA score plot (2D scatter) colored by sample phenotype
- Coordinates of principal components (loadings and scores)
- List of flagged outlier sample identifiers with high within-group dispersion

## How to apply

Load the LipidomicsExperiment object and confirm that the intensity measure (typically 'Area') has been marked as logged and normalized using set_logged() and set_normalized(). Call mva(d, measure='Area', method='PCA') to compute principal components on the lipid feature matrix. Generate a score plot via plot_mva(mvaresults, color_by='SampleType', components=(1,2)) to color samples by phenotype group. Inspect the resulting scatter plot for visual separation between groups on PC1 and PC2; mild separation may indicate biological signal but limited discriminatory power. Identify outlier samples as those with large distance from their group centroid or positioned in extreme regions of the plot. Flag samples with significantly large dispersion (e.g., samples 18 and 42 in ST001111) for consideration of removal prior to downstream univariate analysis.

## Related tools

- **lipidr** (Provides mva() function for PCA computation and plot_mva() for visualization; manages LipidomicsExperiment object lifecycle and sample annotation integration) — https://github.com/ahmohamed/lipidr
- **R** (Runtime environment for lipidr and statistical computation)
- **SummarizedExperiment** (Base class extended by LipidomicsExperiment for structured storage of assays and sample metadata) — http://bioconductor.org/packages/SummarizedExperiment/

## Examples

```
mvaresults = mva(d, measure="Area", method="PCA")
plot_mva(mvaresults, color_by="SampleType", components = c(1,2))
```

## Evaluation signals

- PCA score plot displays clear or mild visual separation between phenotype groups on PC1/PC2 axes, matching the expected biological signal.
- Outlier samples are spatially distant (> 2–3 standard deviations) from their assigned group centroid and do not form a coherent sub-cluster.
- Removal of flagged outliers (e.g., samples 18 and 42) increases within-group homogeneity and tightens cluster boundaries in a re-plotted PCA.
- Variance explained by PC1 and PC2 is sufficient to interpret biological separation (typically > 30–50% cumulative variance for lipidomics datasets).
- Sample identifiers of outliers are reproducible across independent PCA runs and are confirmed by manual visual inspection of the scatter plot.

## Limitations

- PCA reveals only linear combinations of lipid abundances; mild or no separation does not exclude subtle biological differences detectable by supervised methods (PLS-DA, OPLS-DA).
- No separation between cancer and metastasis groups was observed in ST001111, indicating that cancer stage does not substantially affect the lipid molecules profiled in that experiment.
- Outlier detection is subjective and depends on visual inspection or ad-hoc distance thresholds; formal statistical tests (e.g., Mahalanobis distance) may be needed for objective flagging.
- Confounding variables (e.g., Race in ST001111) can obscure or create spurious separation; stratification or ANOVA-style designs (~ Stage) are needed to disentangle batch and biological effects.

## Evidence

- [other] PCA revealed mild separation between benign and cancer samples but not between cancer and metastasis, with samples 18 and 42 identified as outliers with significantly large dispersion warranting consideration for removal.: "PCA revealed mild separation between benign and cancer samples but not between cancer and metastasis, with samples 18 and 42 identified as outliers with significantly large dispersion warranting"
- [other] Apply PCA using mva() with method='PCA' on the Area measure and generate a score plot from mva results using plot_mva() with color_by='SampleType' and components=(1,2).: "Apply PCA using mva() with method='PCA' on the Area measure. 3. Generate a score plot from mva results using plot_mva() with color_by='SampleType' and components=(1,2)."
- [intro] We can see mild separation between benign and cancer samples, but not between cancer and metastasis.: "We can see mild separation between benign and cancer samples, but not between cancer and metastasis."
- [readme] lipidr implements PCA, PCoA and OPLS(DA) to reveal patterns in data and discover variables related to an outcome of interest. Top associated lipids as well as scores and loadings plots can be interactively investigated.: "lipidr implements PCA, PCoA and OPLS(DA) to reveal patterns in data and discover variables related to an outcome of interest."
- [intro] Set logged and normalized status for data using set_logged(d, 'Area', TRUE) and set_normalized(d, 'Area', TRUE): "d <- set_logged(d, "Area", TRUE)
d <- set_normalized(d, "Area", TRUE)"
