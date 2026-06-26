---
name: metabolite-missingness-threshold-filtering
description: Use when when you have a metabolite measurement matrix with missing values
  across samples and need to decide which metabolites to retain before applying k-nearest
  neighbor imputation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - MetaboDiff
  - MultiAssayExperiment
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1093/bioinformatics/bty344
  title: MetaboDiff
- doi: 10.1158/0008-5472.can-14-1490
  title: ''
evidence_spans:
- The `MetaboDiff` R package requires R version 4.0.2 or higher.
- The `MetaboDiff` R package requires R version 4.0.2 or higher
- '`MetaboDiff` is available for all operating systems and can be installed via Github'
- met = knn_impute(met,cutoff=0.4)
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/bty344
  all_source_dois:
  - 10.1093/bioinformatics/bty344
  - 10.1158/0008-5472.can-14-1490
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-missingness-threshold-filtering

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Apply a missingness cutoff threshold to filter out metabolites with excessive missing values before imputation, retaining only metabolites measured in a sufficient fraction of samples. This ensures that imputation algorithms operate on data with acceptable completeness and minimizes bias from over-imputation.

## When to use

When you have a metabolite measurement matrix with missing values across samples and need to decide which metabolites to retain before applying k-nearest neighbor imputation. Specifically, use this skill when the fraction of missing values per metabolite varies widely and you want to exclude metabolites that lack sufficient data support (e.g., missing in >40% of samples) to enable reliable imputation and downstream statistical analysis.

## When NOT to use

- Input assay matrix has no missing values or negligible missingness—filtering will have minimal effect and may discard useful metabolites unnecessarily.
- Metabolites are already known to be biologically informative despite high missingness in specific sample groups; domain knowledge should override automatic filtering.
- Analysis goal requires imputation of all measured metabolites regardless of missingness pattern for sample-level or pathway-level inference that does not depend on per-metabolite reliability.

## Inputs

- assay matrix: rows are metabolites, columns are samples, entries are metabolite abundance measurements with missing values encoded (e.g., NA)
- missingness cutoff parameter (numeric, 0–1): maximum allowable fraction of missing values per metabolite

## Outputs

- filtered assay matrix: subset of original metabolites meeting the non-missingness threshold
- count of excluded metabolites: integer tally of metabolites removed by the filter
- list of retained metabolite identifiers: rownames or indices of metabolites passing the filter

## How to apply

Define a missingness cutoff threshold (e.g., cutoff=0.4) that specifies the maximum proportion of samples in which a metabolite can be missing and still be retained. For each metabolite in the assay matrix, calculate the fraction of missing values across all samples. Retain only metabolites where the fraction of non-missing measurements meets or exceeds the complementary threshold (e.g., ≥60% of samples for cutoff=0.4). This filtering is typically applied before imputation to reduce the computational burden and avoid imputing metabolites with sparse coverage. The rationale is that k-nearest neighbor imputation performs more reliably when metabolites have sufficient observed data points to anchor the similarity calculations, and excessive imputation can distort the variance structure of the data.

## Related tools

- **MetaboDiff** (R package providing knn_impute function with built-in cutoff parameter for missingness-based filtering prior to imputation) — https://github.com/andreasmock/MetaboDiff
- **R** (Programming environment for loading data, computing missingness fractions, and applying the threshold filter)
- **MultiAssayExperiment** (Data container class used by MetaboDiff to organize assay matrices, rowData, and colData for efficient subsetting and filtering)

## Examples

```
met = knn_impute(met, cutoff=0.4)
```

## Evaluation signals

- Verify that the number of excluded metabolites equals the count of metabolites with missing-value fraction exceeding the cutoff (e.g., 69 metabolites excluded for cutoff=0.4 on the Priolo et al. prostate cancer dataset).
- Check that all retained metabolites have a non-missing-value fraction ≥ (1 - cutoff) across samples; spot-check a sample of retained and excluded metabolites to confirm correct classification.
- Confirm that the filtered assay matrix has fewer rows (metabolites) than the original matrix but retains all original columns (samples).
- Inspect the distribution of missingness across retained metabolites and confirm it is bounded by the cutoff threshold.
- Verify that downstream imputation (e.g., knn_impute) completes successfully on the filtered matrix without errors due to all-missing rows.

## Limitations

- The choice of cutoff threshold is somewhat arbitrary and should be justified by the experimental design and biological context; too stringent a cutoff may discard metabolites with structured missingness (e.g., true absences in a particular sample group), while too lenient a cutoff retains metabolites with sparse coverage unsuitable for imputation.
- Filtering is applied uniformly across all samples and does not account for sample-specific missingness patterns; a metabolite might be excluded globally even if it is well-measured in a subset of samples relevant to the analysis.
- Post-filtering imputation (e.g., k-nearest neighbor) assumes that patterns of missingness are not informative; if missingness is related to metabolite abundance or sample phenotype, filtering followed by imputation may introduce bias.
- No guidance is provided in the article for sensitivity analysis or cross-validation of the cutoff choice; practitioners should consider running the pipeline with multiple cutoff values to assess robustness of downstream findings.

## Evidence

- [methods] knn_impute function call with cutoff parameter: "met = knn_impute(met,cutoff=0.4)"
- [methods] definition of cutoff effect on metabolite retention: "retain only metabolites with non-missing measurements in ≥60% of samples (i.e., missing in ≤40%)"
- [methods] imputation performance rationale: "imputation is performed by k-nearest neighbor imputation, which could be shown to minimize the effects on the normality and variance of the data as long as the number of missing data does not exceed"
- [methods] reference to met_example tumor-vs-normal dataset: "example data for the tutorial is derived from a study by Priolo and colleagues in which the authors used the service of Metabolon to compare the tissue metabolome of 61 prostate cancers with 25"
- [readme] rationale for pre-imputation filtering: "The MetaboDiff packages aims to provide a low-level entry to differential metabolomic analysis with R by starting off with the table of metabolite measurements."
