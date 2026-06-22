---
name: variance-stabilization-normalization
description: Use when after k-nearest neighbor imputation (cutoff ≥0.6 data retention) and outlier sample removal have been completed on your MultiAssayExperiment object.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - MetaboDiff
  - R
  - MultiAssayExperiment
derived_from:
- doi: 10.1093/bioinformatics/bty344
  title: MetaboDiff
- doi: 10.1158/0008-5472.can-14-1490
  title: ''
evidence_spans:
- '`MetaboDiff` is available for all operating systems and can be installed via Github'
- met = knn_impute(met,cutoff=0.4)
- The `MetaboDiff` R package requires R version 4.0.2 or higher.
- The `MetaboDiff` R package requires R version 4.0.2 or higher
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metabodiff_cq
    doi: 10.1093/bioinformatics/bty344
    title: MetaboDiff
  dedup_kept_from: coll_metabodiff_cq
schema_version: 0.2.0
---

# Variance-Stabilization Normalization

## Summary

Variance-stabilizing normalization (vsn) is a post-imputation normalization step that ensures constant variance across the full range of metabolite measurements, preventing heteroscedasticity that would violate assumptions of downstream statistical tests. Apply this skill after kNN imputation and outlier removal to prepare metabolite assay data for differential analysis.

## When to use

After k-nearest neighbor imputation (cutoff ≥0.6 data retention) and outlier sample removal have been completed on your MultiAssayExperiment object. Specifically, use this when metabolite measurements exhibit variance that scales with measurement intensity (heteroscedasticity), which violates constant-variance assumptions required for valid p-value calculations in differential metabolomic analysis.

## When NOT to use

- Input assay is already log-transformed or known to have constant variance across the measurement range
- You are working with count data (e.g., microbiome reads) rather than continuous metabolite measurements
- Downstream analysis explicitly requires raw (non-normalized) measurements, such as when deriving abundance-based network weights

## Inputs

- MultiAssayExperiment object (post-kNN imputation, post-outlier removal)
- assay slot containing metabolite measurements (rows = metabolites, columns = samples)
- colData slot containing sample metadata including group labels for QC visualization

## Outputs

- MultiAssayExperiment object with normalized assay values
- Variance-stabilized metabolite measurement matrix (constant variance across measurement range)
- Quality control plots showing normalized measurement distributions by sample and group

## How to apply

Apply the normalize_met function to your post-imputation, post-outlier-removal MultiAssayExperiment object. The vsn method stabilizes variance by log-transforming and rescaling measurements so that variance becomes approximately constant across the measured spectrum, rather than growing with signal intensity. This ensures that downstream statistical tests (e.g., t-tests, linear models) maintain valid Type I error rates. After normalization, verify success by generating quality control plots with quality_plot to confirm that normalized measurements show comparable distributions across samples and groups, and that no systematic group effects remain in the residuals.

## Related tools

- **MetaboDiff** (R package providing normalize_met function to apply vsn normalization to MultiAssayExperiment metabolomics objects) — https://github.com/andreasmock/MetaboDiff
- **MultiAssayExperiment** (Bioconductor class used to represent normalized metabolite assay data alongside sample metadata and feature annotations)
- **R** (Statistical computing environment required (version ≥4.0.2) for executing vsn normalization and QC visualization)

## Examples

```
met <- normalize_met(met); quality_plot(met, group_factor="tumor_normal", label_colors=c("darkseagreen","dodgerblue"))
```

## Evaluation signals

- Post-normalization quality_plot shows comparable measurement distributions across samples and groups (no systematic group shifts in central tendency or spread)
- Variance is approximately constant across the full range of metabolite intensities (inspect plot of residuals vs. fitted values — should show flat trend, not funnel shape)
- pca_plot and tsne_plot after normalization do not reveal artificial clustering driven by measurement intensity alone; biological group structure (e.g., tumor vs. normal) is preserved or enhanced
- Normalized assay values are log-scale or log-like (typically in range 0–15 for metabolomics after vsn), indicating successful transformation
- No systematic batch or technical artifacts appear in post-normalization visualizations that were not present in the original assay

## Limitations

- vsn performance degrades when >40% of data are imputed (high missingness rate); validate that knn_impute cutoff is ≥0.6 to retain only metabolites with ≥60% non-missing data before normalization
- vsn assumes a smooth, continuous relationship between mean and variance; it may not work well for metabolites with bimodal distributions or extreme outliers that survived outlier_heatmap filtering
- Normalization is applied globally across all samples; if strong batch effects exist (e.g., samples from different instruments or acquisition dates), batch correction should precede vsn or be applied jointly
- vsn is not designed for categorical or ordinal metabolite data; only apply to continuous abundance measurements

## Evidence

- [methods] Variance stabilizing normalization (vsn) is used to ensure that the variance remains nearly constant over the measured spectrum: "Variance stabilizing normalization (vsn) is used to ensure that the variance remains nearly constant over the measured spectrum"
- [methods] kNN imputation with cutoff=0.4 retains metabolites with ≥60% non-missing data; normalization follows imputation: "imputation is performed by k-nearest neighbor imputation, which could be shown to minimize the effects on the normality and variance of the data as long as the number of missing data does not exceed"
- [methods] normalize_met function is applied to MultiAssayExperiment object after outlier removal: "met <- normalize_met(met)"
- [methods] Quality control via quality_plot verifies normalized measurements show comparable distributions across samples and groups: "quality_plot(met, group_factor="tumor_normal", label_colors=c("darkseagreen","dodgerblue"))"
- [intro] MetaboDiff provides low-level entry to differential metabolomic analysis via normalization of metabolite measurement tables: "The MetaboDiff packages aims to provide a low-level entry to differential metabolomic analysis with R by starting off with the table of metabolite measurements."
