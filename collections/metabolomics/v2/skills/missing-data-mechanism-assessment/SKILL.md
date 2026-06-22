---
name: missing-data-mechanism-assessment
description: Use when when you have a filtered metabolite abundance matrix with remaining missing values after feature-level filtering (e.g., removal of metabolites with >80% missingness), and you need to decide whether missingness is concentrated in specific features or sample pairs, or distributed randomly.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - R
  - Bioconductor
  - marr
derived_from:
- doi: 10.1186/s12859-021-04336-9
  title: marr
- doi: 10.1080/01621459.2017.1397521
  title: ''
evidence_spans:
- 'marr: An R/Bioconductor package for Maximum Rank Reproducibility'
- The R-package **marr** can be installed from GitHub using the R package [devtools]
- '`marr`: An R/Bioconductor package for Maximum Rank Reproducibility'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_marr_cq
    doi: 10.1186/s12859-021-04336-9
    title: marr
  dedup_kept_from: coll_marr_cq
schema_version: 0.2.0
---

# missing-data-mechanism-assessment

## Summary

Assessment of missingness patterns in high-dimensional biological replicate data to determine whether missing values are systematic (feature-level or sample-pair-level) or random, informing choice of imputation strategy. This skill is critical before applying Bayesian Principal Component Analysis (BPCA) or other missing-value handlers in metabolomics preprocessing pipelines.

## When to use

When you have a filtered metabolite abundance matrix with remaining missing values after feature-level filtering (e.g., removal of metabolites with >80% missingness), and you need to decide whether missingness is concentrated in specific features or sample pairs, or distributed randomly. This assessment guides imputation method selection and validates assumptions of the chosen imputation technique.

## When NOT to use

- Input matrix has already been imputed or has no remaining missing values.
- Missing values are known a priori to be missing-completely-at-random (MCAR) from study design (e.g., planned incomplete block design); assessment adds no new information.
- Missingness is known to be non-ignorable (e.g., missing-not-at-random driven by unmeasured confounders), requiring sensitivity analysis rather than standard pattern assessment.

## Inputs

- Filtered metabolite abundance matrix (CSV or R data frame; features × samples; with metabolites already removed if >80% missing)
- Sample metadata indicating replicate structure (for pairing analysis)

## Outputs

- Missingness pattern summary (feature-level and sample-pair-level missingness percentages)
- Visualization of missingness distribution (e.g., histogram or heatmap)
- Classification of missingness mechanism (random vs. systematic)
- Decision record documenting imputation method justification

## How to apply

Compute the distribution of missingness across (1) features (rows)—the percentage of samples in which each metabolite is missing—and (2) sample pairs (columns)—the percentage of features missing in each sample. Examine whether missing values cluster in a small subset of metabolites or samples (systematic missingness) or are broadly distributed (random missingness). If missingness is predominantly random and limited to <20% of values after filtering, BPCA-based imputation is appropriate; if missingness is highly structured or concentrated in certain features/samples, consider whether those features/samples should be excluded or handled separately. Document missingness patterns as a preprocessing quality-control metric prior to imputation.

## Related tools

- **marr** (Provides msprepCOPD metabolomics dataset with documented preprocessing stages (filtering, BPCA imputation, normalization) and the Marr() function for assessing reproducibility patterns in replicate samples, which can reveal missingness structure) — https://github.com/Ghoshlab/marr
- **R** (Host language for implementing missingness assessment functions (e.g., colSums(is.na()), rowSums(is.na())) and visualization (base plot, ggplot2, heatmap))
- **Bioconductor** (Source of SummarizedExperiment object class used to represent and manipulate filtered metabolite matrices) — https://bioconductor.org

## Examples

```
# R: Assess missingness patterns in filtered metabolite matrix
filtered_mat <- read.csv('metabolites_filtered.csv', row.names=1)
missing_by_feature <- rowSums(is.na(filtered_mat)) / ncol(filtered_mat) * 100
missing_by_sample <- colSums(is.na(filtered_mat)) / nrow(filtered_mat) * 100
cat('Mean feature missingness:', mean(missing_by_feature), '%\n')
cat('Mean sample missingness:', mean(missing_by_sample), '%\n')
hist(missing_by_feature, main='Missingness by Metabolite', xlab='% Missing')
```

## Evaluation signals

- Verify that missingness percentages sum correctly: mean(feature-level missingness) ≈ overall sparsity, and mean(sample-pair-level missingness) yields same overall percentage.
- Check that post-filtering missingness is ≤20% of total cells (articles and MSPrep pipeline assume BPCA is practical for sparse matrices below this threshold).
- Confirm no feature has >95% missing values after initial filtering (indicates filtering step may have been incomplete).
- Validate that replicate sample pairs are balanced in missingness (e.g., no technical replicate pair differs by >10 percentage points in missing-data rate, which would flag instrumental or procedural anomalies).
- Document that classification (random vs. systematic) was made explicit before imputation method selection; verify BPCA was chosen only if missingness is not highly concentrated in a few problematic features/samples.

## Limitations

- This skill assesses mechanisms but does not enforce missing-data assumptions (e.g., MCAR vs. MAR); practitioners must apply domain knowledge to validate whether mechanisms are plausible.
- Missingness patterns in cross-replicate metabolomics are often driven by instrument sensitivity thresholds, which may appear random at the level of individual features but are systematic at the instrument level—assessment does not detect or characterize this source.
- High-dimensional assessments (645+ metabolites) can be computationally light but difficult to visualize; summary statistics may mask localized, small-sample-size patterns important for specific biological subgroups.
- Assessment assumes replicate structure (e.g., paired samples) is known; if replicates are mislabeled or undocumented, pattern assessment will be unreliable.

## Evidence

- [intro] Filtering: Metabolites are removed if they are missing more than 80% of the samples: "Filtering: Metabolites are removed if they are missing more than 80% of the samples"
- [intro] BPCA applied after filtering and before median normalization in three-step MSPrep pipeline: "Missing value imputation technique: We apply Bayesian Principal Component Analysis (BPCA) to impute missing values"
- [intro] marr package contains msprepCOPD metabolomics dataset with 645 metabolites and 20 biological replicates: "The **marr** package contains a pre-processed data `SummarizedExperiment` assay object of 645 metabolites (features) measured in plasma and 20 biological replicates"
- [intro] Reproducibility depends on technical and biological variables in high-throughput experiments: "The reproducibility of a high-throughput experiment primarily depends on the technical variables, such as run time, technical replicates, laboratory operators and biological variables"
- [intro] marr procedure assesses reproducibility across replicate samples in MS-Metabolomics: "the (ma)ximum (r)ank (r)eproducibility (marr) procedure can be adapted to high-throughput MS-Metabolomics experiments across (biological or technical) replicate samples"
