---
name: batch-effect-correction-metabolomics
description: Use when your metabolomics dataset exhibits samples analyzed across multiple
  batches or analytical runs with suspected technical drift or batch-to-batch signal
  shift visible as systematic separation in unsupervised clustering (PCA, hierarchical
  clustering).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - dbnorm
  - R
  - sva
  - ber
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1038/s41598-021-84824-3
  title: Dbnorm
- doi: 10.1007/s12561-013-9081-1
  title: ''
evidence_spans:
- dbnorm (V-0.2.2) A package for drift across batches normalization and visualization
- dbnorm contains R functions which allow visualization and removal of technical heterogeneity
- '*dbnorm* contains R functions which allow visualization and removal of technical
  heterogeneity'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_dbnorm_cq
    doi: 10.1038/s41598-021-84824-3
    title: Dbnorm
  dedup_kept_from: coll_dbnorm_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41598-021-84824-3
  all_source_dois:
  - 10.1038/s41598-021-84824-3
  - 10.1007/s12561-013-9081-1
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# batch-effect-correction-metabolomics

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Correct technical batch effects and drift across analytical runs in preprocessed, log2-scaled metabolomics datasets using statistical models (ber, ComBat parametric/non-parametric) implemented in the dbnorm package. This skill removes systematic technical heterogeneity while preserving biological signal, enabling robust downstream analysis of disease mechanisms.

## When to use

Your metabolomics dataset exhibits samples analyzed across multiple batches or analytical runs with suspected technical drift or batch-to-batch signal shift visible as systematic separation in unsupervised clustering (PCA, hierarchical clustering). Data must be normalized, log2-scaled, in CSV format with batch identifiers in the first column, and contain fewer than 2000 features for computational efficiency with visualization functions.

## When NOT to use

- Input metabolomics data is not yet normalized or log2-scaled; apply preprocessing normalization first
- Dataset contains >2000 features; visualization-intensive functions (Visodbnorm, dbnormSCORE) will be computationally slow; use individual model functions (dbnormBer, etc.) instead
- Batch effects are intentional experimental design factors you wish to preserve for biological inference; use blocking or stratified analysis instead

## Inputs

- CSV file: metabolomics abundance matrix (log2-scaled, samples in rows, features/metabolites in columns, batch identifier in first column)
- batch annotation metadata (factor or character vector indicating batch/analytical run assignment)

## Outputs

- Corrected metabolomics abundance matrix (CSV) with batch effects removed
- Diagnostic PDF (PCA plots, scree plots, correlation plots, RLA plots, profile density plots)
- Adjusted R-squared scores (CSV) quantifying model performance per feature
- Quality assessment summary table (CSV) with maximum adjusted R-squared per model

## How to apply

First, preprocess the metabolomics matrix to handle missing values (NA or zero) using emvd (global minimum) or emvf (per-feature minimum) imputation functions. Load the batch-annotated matrix into R and call the appropriate batch correction function (dbnormBer, dbnormBagging, dbnormPcom, or dbnormNPcom) based on your data structure. Before committing to a single model, run dbnormSCORE to compute adjusted R-squared values quantifying how well each model explains batch variance; select the model with highest consistency across features. Apply your chosen model and inspect diagnostic outputs (PCA plots, RLA plots, profile density plots) to confirm spatial separation of batches is resolved and feature distributions show convergence across batches. Extract the corrected CSV matrix from the temporary R output folder for downstream analysis.

## Related tools

- **dbnorm** (R package implementing ber, ber-bagging, parametric ComBat, and non-parametric ComBat batch correction models with diagnostic and imputation functions) — https://github.com/NBDZ/dbnorm
- **sva** (Bioconductor package providing ComBat parametric and non-parametric empirical Bayes batch effect correction methods; dependency of dbnorm)
- **ber** (R package implementing the two-stage ber function (originally for microarray gene expression) adapted in dbnorm for metabolomics drift correction)

## Examples

```
data <- read.csv('path/to/metabolomics.csv', sep=',', header=TRUE, row.names=1); library(dbnorm); df <- emvd(data[-1]); dbnormSCORE(cbind(data[1], df)); corrected <- dbnormBer(cbind(data[1], df))
```

## Evaluation signals

- Adjusted R-squared values for batch effect in corrected data are substantially lower (>0.3 difference) than in raw data for majority of features
- PCA plot shows substantial reduction in visual clustering/separation by batch after correction; biological groups (if present) remain resolved
- RLA (Relative Log Abundance) plots show centered distributions around zero post-correction across all batches (raw data shows systematic shift)
- Profile density plots of features show convergence of probability density functions across batches post-correction (raw data shows shifted PDFs)
- Hierarchical clustering distance between technical replicates (QC samples) analyzed in different batches decreases after correction

## Limitations

- Requires input data to be normalized and log2-scaled; high-abundance features can obscure technical heterogeneity if not log-transformed
- Computational speed degrades substantially for datasets >2000 features; visualization functions (Visodbnorm, dbnormSCORE) not recommended for large feature sets
- No changelog available in repository; version tracking and backward compatibility not documented
- ber function assumes linear drift patterns across batches; non-linear batch effects may not be fully corrected
- Model selection via dbnormSCORE depends on adjusted R-squared; biological domain knowledge needed to validate that chosen model does not over-correct and remove real biological signal

## Evidence

- [intro] dbnorm allows visualization and removal of technical heterogeneity from large metabolomics datasets: "*dbnorm* contains R functions which allow visualization and removal of technical heterogeneity from large metabolomics dataset"
- [readme] Data preprocessing requires log2 scaling and CSV format with batch in first column: "Data to be uploaded must be normalized and scaled on the log2 to account for the high abundance features (variables) by which technical heterogeneity might be overlooked. The input data must be in"
- [readme] dbnorm includes multiple statistical models for batch correction: ber, ber-bagging, parametric ComBat, non-parametric ComBat: "*dbnorm* includes several statistical models such as, ComBat(parametric and non-parametric)-model [PMID:16632515]  from sva package [PMID:22257669] ,that was already in use for metabolomics data"
- [readme] dbnormSCORE evaluates model performance via adjusted coefficient of determination: "the  adjusted coefficient of determination or Adjusted R-Squared is calculated for each variable estimated in a regression model for its dependency to the batch level in the raw data and treated data"
- [readme] Visualization functions recommended for datasets with fewer than 2000 features: "This function is suggested for less than 2000 features (variables)."
- [readme] Missing value imputation via global or per-feature minimum detection: "This function allows you to estimate missing values (Zero or/and NA values) by the lowest detected value in the entire experiment."
- [readme] Profile density plots show batch effects across corrected and raw data: "These functions allow users to adjust the data for batch effect using either of models implemented in the package described earlier, and inform about the presence of across batch signal drift or"
