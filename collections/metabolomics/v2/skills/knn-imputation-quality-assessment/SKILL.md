---
name: knn-imputation-quality-assessment
description: 'Use when after deciding to use KNN imputation on a metabolomic assay
  matrix with missing values, but before proceeding to normalization and statistical
  testing. Trigger conditions include: (1) your metabolomic dataset contains metabolites
  with varying degrees of missingness across samples;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3557
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - MetaboDiff
  - MultiAssayExperiment
  license_tier: restricted
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

# knn-imputation-quality-assessment

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Assess the quality and appropriateness of k-nearest neighbor (KNN) imputation for metabolomic data by evaluating how many metabolites are excluded by the missingness cutoff and verifying that imputation minimizes distortion of data normality and variance. This skill ensures that the imputation strategy preserves data integrity before downstream differential analysis.

## When to use

Apply this skill after deciding to use KNN imputation on a metabolomic assay matrix with missing values, but before proceeding to normalization and statistical testing. Trigger conditions include: (1) your metabolomic dataset contains metabolites with varying degrees of missingness across samples; (2) you have chosen a missingness cutoff (e.g., cutoff=0.4 to retain metabolites missing in ≤40% of samples); (3) you need to quantify how many features are lost by this filtering step and verify the imputation does not artificially inflate correlations or violate normality assumptions.

## When NOT to use

- Your metabolomic assay already has no missing values or uses a different imputation strategy (e.g., zero-filling, simple mean imputation) that you wish to preserve.
- You lack sufficient sample size or biological replicates within groups to support KNN neighbor selection (KNN requires enough samples to find stable k neighbors).
- Your dataset contains extreme missingness patterns where entire metabolite classes or sample cohorts are uniformly absent, rendering the cutoff strategy ineffective at balancing retention and reliability.

## Inputs

- MetaboDiff object or MultiAssayExperiment object containing an assay matrix of metabolite measurements (rows = metabolites, columns = samples) with missing values (NA)
- Sample metadata (colData) indicating biological groups (e.g., tumor vs. normal)
- Missingness cutoff parameter (scalar, 0–1, e.g., 0.4)

## Outputs

- Imputed metabolomic assay matrix with KNN-filled values replacing NAs for retained metabolites
- Count of excluded metabolites (those exceeding the missingness cutoff)
- Count of retained metabolites post-imputation
- Visual summary of missing-value patterns (via na_heatmap before and after imputation)
- Outlier heatmap and dendrogram showing impact of imputation on sample clustering

## How to apply

After loading your metabolomic dataset into MetaboDiff (e.g., the met_example tumor-vs-normal dataset with 61 prostate cancer + 25 normal samples), inspect the raw assay matrix dimensions and document the original metabolite count and missing-value patterns using na_heatmap. Call knn_impute(met, cutoff=0.4) to retain only metabolites with non-missing measurements in ≥60% of samples (i.e., missing in ≤40% of cases). Extract and count the metabolites in the imputed assay slot and compare to the raw count to identify the number excluded (e.g., 69 metabolites removed). The rationale is that KNN imputation with a defined missingness threshold balances statistical power (retaining sufficient features) against imputation reliability—features exceeding the threshold risk biased estimates when too many neighbors lack valid values. Verify quality by checking that post-imputation sample dendrograms and k-means clustering results remain interpretable and that no artificial outlier clusters are introduced by imputation artifacts.

## Related tools

- **MetaboDiff** (R package providing knn_impute function and downstream visualization/filtering workflows (na_heatmap, outlier_heatmap, normalize_met) to assess and apply imputation) — https://github.com/andreasmock/MetaboDiff
- **R** (Statistical computing environment required to load MetaboDiff and execute imputation pipeline)
- **MultiAssayExperiment** (Data container class (via create_mae) that organizes assay, rowData, and colData for streamlined imputation and annotation)

## Examples

```
met = knn_impute(met, cutoff=0.4); nrow(assay(met))
```

## Evaluation signals

- Metabolite count before and after imputation matches expected exclusions: raw count minus retained count equals reported excluded count (e.g., 69 metabolites).
- All retained metabolites have ≤cutoff proportion of missing values (e.g., ≤40% missing when cutoff=0.4); all excluded metabolites exceed this threshold.
- Post-imputation assay matrix contains no remaining NA values in retained metabolites; imputed values are numeric and within plausible biological ranges (compare to raw value distributions).
- na_heatmap visual inspection shows clear before/after pattern: raw heatmap displays sparse NAs across metabolites; post-imputation heatmap is dense (NAs replaced by KNN estimates).
- Outlier heatmap and sample dendrogram remain biologically interpretable post-imputation (e.g., tumor samples cluster distinctly from normal samples, without artificial k-means clusters driven by imputation noise); sample annotation lists missingness counts per sample to track imputation impact.

## Limitations

- KNN imputation reliability depends critically on the choice of missingness cutoff and the underlying assumption that k nearest neighbors in the full metabolomic space provide valid estimates for missing values. If metabolites are missing not at random (MNAR) but systematically absent due to instrument failure or sample preparation, KNN estimates may be biased.
- The method requires sufficient sample size and biological replicability to select stable neighbors; small cohorts or highly imbalanced designs may yield unstable imputation.
- KNN imputation can artificially inflate correlation coefficients among metabolites if many values are imputed, potentially biasing downstream network analysis. The article notes this occurs when missingness exceeds recommended thresholds but does not quantify the exact point of distortion.
- The choice of k (number of neighbors) in KNN is not explicitly detailed in the article; default or package-specific settings may differ across analyses, affecting reproducibility.

## Evidence

- [other] Application of knn_impute with cutoff=0.4 to the met_example tumor-vs-normal dataset results in exclusion of 69 metabolites that exceed the missingness threshold.: "Application of knn_impute with cutoff=0.4 to the met_example tumor-vs-normal dataset results in exclusion of 69 metabolites that exceed the missingness threshold."
- [methods] KNN imputation is chosen because it minimizes distortion of data normality and variance when missingness is moderate.: "imputation is performed by k-nearest neighbor imputation, which could be shown to minimize the effects on the normality and variance of the data as long as the number of missing data does not exceed"
- [methods] The na_heatmap function visualizes missing metabolite patterns to guide cutoff selection and assess imputation impact.: "The function `na_heatmap` visualizes the missing metabolite measurements across the samples."
- [methods] Outlier detection via outlier_heatmap after imputation confirms whether imputation introduced artifacts or preserved biological signal.: "the function `outlier_heatmap` is provided. The sample annotation shows the number of missing metabolites per sample as a proxy of the impact of imputation on clustering."
- [readme] MetaboDiff provides a low-level workflow for metabolomic analysis starting from raw measurement tables, with imputation as a core preprocessing step.: "The MetaboDiff packages aims to provide a low-level entry to differential metabolomic analysis with R by starting off with the table of metabolite measurements."
