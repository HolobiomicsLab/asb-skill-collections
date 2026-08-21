---
name: quality-control-threshold-application
description: Use when when you have a raw feature abundance matrix with missing values
  (NAs or zeros) and need to remove features with excessive sparsity before imputation
  or reproducibility analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_0625
  tools:
  - R
  - MSPrep
  - Bioconductor
  - marr
  - MWASTools
  - ThermoRawFileParser
  - Python
  - PCPFM (Python-Centric Pipeline for Metabolomics)
  - Asari
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1186/s12859-021-04336-9
  title: marr
- doi: 10.1080/01621459.2017.1397521
  title: ''
- doi: 10.1093/bioinformatics/btx477
  title: ''
- doi: 10.1371/journal.pcbi.1011912
  title: ''
evidence_spans:
- 'marr: An R/Bioconductor package for Maximum Rank Reproducibility'
- The R-package **marr** can be installed from GitHub using the R package [devtools]
- The **msprepCOPD** data in the **marr** package was pre-processed using the MSPrep
  software
- '`marr`: An R/Bioconductor package for Maximum Rank Reproducibility'
- Assuming that R (>=3.3) and Bioconductor have been correctly installed
- Here, we present a package to perform MWAS using univariate hypothesis testing
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_marr_cq
    doi: 10.1186/s12859-021-04336-9
    title: marr
  - build: coll_mwastools_cq
    doi: 10.1093/bioinformatics/btx477
    title: MWASTools
  - build: coll_pcpfm
    doi: 10.1371/journal.pcbi.1011912
    title: pcpfm
  dedup_kept_from: coll_marr_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s12859-021-04336-9
  all_source_dois:
  - 10.1186/s12859-021-04336-9
  - 10.1080/01621459.2017.1397521
  - 10.1093/bioinformatics/btx477
  - 10.1371/journal.pcbi.1011912
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# quality-control-threshold-application

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Apply a quantitative missingness threshold to filter features (metabolites) from high-dimensional replicate experiments, retaining only those meeting a minimum presence criterion across samples. This skill removes low-quality features before downstream analysis and is essential for preparing metabolomics data for reproducibility assessment.

## When to use

When you have a raw feature abundance matrix with missing values (NAs or zeros) and need to remove features with excessive sparsity before imputation or reproducibility analysis. Apply this skill when the proportion of missing data per feature varies substantially and a biological or technical minimum presence threshold is justified (e.g., a metabolite must be quantifiable in at least 20% of replicates to be retained for analysis).

## When NOT to use

- Input data already consists of a pre-filtered feature table with documented minimum presence thresholds applied.
- Missingness is not random or informative; features with high missingness are biologically relevant (e.g., conditionally expressed markers) and removal would bias results.
- Sample size is very small (N < 5) such that a 20% presence threshold cannot be met for any feature; choose a lower threshold or alternative strategy.

## Inputs

- Raw feature abundance matrix (e.g., SummarizedExperiment object with metabolite rows × sample columns)
- Numeric threshold for maximum acceptable missingness as a proportion (e.g., 0.80 for 80%)
- Missing value convention (NA, zero, or software-specific representation)

## Outputs

- Filtered feature abundance matrix with features below missingness threshold retained
- Feature count before and after filtering (e.g., 662 → 645 metabolites)
- List of removed feature identifiers and their individual missingness proportions

## How to apply

Calculate the proportion of missing values (NA or zero, following MSPrep convention) for each feature across all samples. Define a missingness threshold (e.g., 80%) and retain only features with missingness at or below that threshold, equivalently ensuring each feature is present in at least the complementary percentage of samples (e.g., ≥20% presence in at least 4 of 20 samples). Remove features exceeding the threshold and output the filtered abundance matrix with feature identifiers and sample annotations preserved. The rationale is to exclude metabolites too sparsely measured to provide reliable signal in downstream reproducibility or statistical analyses, while minimizing feature loss (typically 2–5% of features).

## Related tools

- **MSPrep** (Pre-processing software that establishes the missing-value convention (NA/zero) and filtering methodology applied to raw metabolomics data)
- **marr** (R/Bioconductor package containing the msprepCOPD dataset and downstream reproducibility assessment; filtering is a preprocessing step before marr reproducibility calculations) — https://github.com/Ghoshlab/marr
- **R** (Programming language used to load SummarizedExperiment objects, compute missingness proportions, and apply filter logic)
- **Bioconductor** (Framework providing SummarizedExperiment data structures and standard methods for manipulating high-dimensional genomics/metabolomics assay data)

## Examples

```
# Load msprepCOPD from marr package; calculate missingness per metabolite; retain metabolites with ≤80% missingness
library(marr); data(msprepCOPD); miss_prop <- rowMeans(is.na(assay(msprepCOPD))); filtered <- msprepCOPD[miss_prop <= 0.80, ]; cat('Retained:', nrow(filtered), 'metabolites\n')
```

## Evaluation signals

- Feature count reduction is within expected range (2–5% loss typical for 80% threshold) and no features with ≥20% presence are incorrectly removed.
- Missingness proportion for every retained feature is ≤80% (or ≤ specified threshold); every removed feature has missingness >80%.
- Output matrix dimensions match expected filtered counts (e.g., 645 features × 20 samples) and all feature identifiers and sample annotations are preserved.
- No numerical or data-type errors during missingness calculation (check for proper handling of NA, zero, and mixed encodings across software).
- Downstream reproducibility or imputation analysis proceeds without failures, indicating data quality is sufficient for next step.

## Limitations

- Threshold choice (e.g., 80%) is somewhat arbitrary; sensitivity analysis on nearby thresholds (70%–90%) may reveal whether conclusions are robust to threshold variation.
- Applying a uniform threshold across all features may be suboptimal if different feature classes (e.g., lipids vs. amino acids) have intrinsically different missingness rates; stratified or adaptive thresholds are not addressed in this article.
- Missingness filtering does not account for the magnitude or quality of non-missing values; a feature present in 25% of samples may still have poor signal-to-noise or low dynamic range in those samples.

## Evidence

- [intro] The MSPrep filtering step removes metabolites exceeding 80% missingness, reducing the raw metabolite count from 662 to 645 (a loss of 17 metabolites or 2.6% of features).: "The MSPrep filtering step removes metabolites exceeding 80% missingness, reducing the raw metabolite count from 662 to 645 (a loss of 17 metabolites or 2.6% of features)."
- [intro] Filtering workflow specifies calculation and retention logic: identify and retain only metabolites with ≤80% missingness (i.e., present in ≥20% of samples, or equivalently ≥4 of 20 samples).: "Identify and retain only metabolites with ≤80% missingness (i.e., present in ≥20% of samples, or equivalently ≥4 of 20 samples)."
- [intro] Workflow step description from article enrichment: 'Filtering: Metabolites are removed if they are missing more than 80% of the samples': "Filtering: Metabolites are removed if they are missing more than 80% of the samples"
- [readme] The marr package README confirms the msprepCOPD dataset contains pre-processed data after filtering to 645 metabolites.: "The `marr` package contains a pre-processed data `SummarizedExperiment` assay object of 645 metabolites (features) measured in plasma and 20 biological replicates"
