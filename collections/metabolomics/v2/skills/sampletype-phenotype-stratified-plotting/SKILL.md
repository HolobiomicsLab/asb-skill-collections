---
name: sampletype-phenotype-stratified-plotting
description: Use when after loading and normalizing a LipidomicsExperiment object
  with logged Area measurements, when you need to assess whether clinical sample groups
  (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3935
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - lipidr
  - R
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

# sampletype-phenotype-stratified-plotting

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Generate multivariate analysis (PCA) visualizations stratified by sample phenotype or clinical group to reveal sample clustering patterns and identify potential outliers within a lipidomics dataset. This skill enables visual assessment of biological separation between disease states and quality control screening for anomalous samples.

## When to use

After loading and normalizing a LipidomicsExperiment object with logged Area measurements, when you need to assess whether clinical sample groups (e.g., benign vs. cancer vs. metastasis) cluster distinctly in reduced-dimensionality space, or when you suspect outlier samples with aberrant lipid profiles that should be flagged for removal before downstream differential analysis.

## When NOT to use

- Input data is unnormalized or not yet log-transformed; apply normalization and log transformation first.
- Sample annotation is missing or phenotype grouping is undefined.
- Data has already undergone outlier removal and you are attempting to reapply this filter on the filtered set.

## Inputs

- LipidomicsExperiment object with normalized, logged Area measurements
- SampleType or clinical phenotype annotation (e.g., benign, cancer, metastasis)

## Outputs

- PCA score plot (PC1 vs. PC2) colored by sample phenotype
- List of outlier sample IDs and their visual characteristics
- Qualitative assessment of phenotype separation strength (mild, strong, absent)

## How to apply

Load the normalized LipidomicsExperiment object and apply PCA using mva() with method='PCA' on the Area measure. Generate a score plot using plot_mva() with color_by set to the relevant phenotype variable (e.g., 'SampleType') and components=(1,2) to visualize PC1 vs. PC2. Inspect the plot for visual separation between phenotype groups and visually identify samples with large dispersion or unusual positioning that deviate from their phenotype cluster as potential outliers. Document identified outliers (e.g., samples 18 and 42 in ST001111) and their sample IDs for subsequent removal if warranted by quality thresholds or biological plausibility.

## Related tools

- **lipidr** (Provides mva() function to perform PCA and plot_mva() to generate stratified score plots; manages LipidomicsExperiment object throughout workflow) — https://github.com/ahmohamed/lipidr
- **R** (Execution environment for lipidr functions and visualization)

## Examples

```
mvaresults = mva(d, measure='Area', method='PCA')
plot_mva(mvaresults, color_by='SampleType', components = c(1,2))
```

## Evaluation signals

- PCA plot displays clear visual clustering by SampleType with distinct color groups corresponding to each phenotype level.
- Outlier samples identified show visually anomalous positioning (large distance from phenotype centroid or isolated points) compared to typical samples in their group.
- Separation pattern matches expected biological relationships (e.g., benign and cancer separate; cancer and metastasis do not, as reported in ST001111 findings).
- Sample IDs of flagged outliers are reproducible across repeated plot generation and can be traced back to original measurement data for validation.
- Removal of identified outliers (via keep_samples filtering) produces improved separation or reduced within-group variance in subsequent differential analysis.

## Limitations

- PCA visualizes only PC1 and PC2; weak or absent separation in these components does not rule out separation in higher PCs or via alternative multivariate methods (e.g., PCoA, OPLS-DA).
- Visual outlier detection is subjective and may not capture statistical outliers; consider supplementing with quantitative outlier tests (e.g., Mahalanobis distance) for rigorous thresholds.
- Outlier removal decisions should be validated biologically; samples with large dispersion may represent true biological heterogeneity rather than technical error.
- Sample annotation quality directly affects stratification; misclassified or mislabeled phenotypes will produce misleading cluster patterns.

## Evidence

- [intro] PCA revealed mild separation between benign and cancer samples but not between cancer and metastasis, with samples 18 and 42 identified as outliers: "PCA revealed mild separation between benign and cancer samples but not between cancer and metastasis, with samples 18 and 42 identified as outliers with significantly large dispersion warranting"
- [intro] Generate a score plot from mva results using plot_mva() with color_by='SampleType': "Generate a score plot from mva results using plot_mva() with color_by='SampleType' and components=(1,2)."
- [intro] Inspect the plot to confirm mild separation and visually identify outlier samples: "Inspect the plot to confirm mild separation between benign and cancer samples and visually identify outlier samples (samples 18 and 42)."
- [readme] lipidr implements PCA, PCoA and OPLS(DA) to reveal patterns in data and discover variables related to an outcome of interest: "lipidr implements PCA, PCoA and OPLS(DA) to reveal patterns in data and discover variables related to an outcome of interest."
- [intro] We can see mild separation between benign and cancer samples, but not between cancer and metastasis: "We can see mild separation between benign and cancer samples, but not between cancer and metastasis."
