---
name: metabolite-abundance-standardization
description: Use when you have a metabolomics featuredata matrix with known batch effects, matrix effects, or unwanted technical variation, and you have identified a set of negative control metabolites (e.g., spiked internal standards or blank-derived features) that are expected to show no biological signal.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - NormalizeMets
  - RStudio
  - Microsoft Excel
derived_from:
- doi: 10.1007/s11306-018-1347-7
  title: NormalizeMets
evidence_spans:
- The R software environment can be downloaded for free from the Comprehensive R Archive Network (CRAN)
- 'Install the NormalizeMets package by using the following function: `install.packages("NormalizeMets")`'
- The use of RStudio is also recommended. RStudio is an integrated development environment (IDE)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_normalizemets_cq
    doi: 10.1007/s11306-018-1347-7
    title: NormalizeMets
  dedup_kept_from: coll_normalizemets_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1007/s11306-018-1347-7
  all_source_dois:
  - 10.1007/s11306-018-1347-7
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-abundance-standardization

## Summary

Standardize metabolite peak intensities or concentrations across a featuredata matrix using remove-unwanted-variation (RUV) normalization with clustering and negative control metabolites. This skill corrects for batch effects, matrix effects, and other systematic variation in metabolomics data before downstream biomarker analysis.

## When to use

Apply this skill when you have a metabolomics featuredata matrix with known batch effects, matrix effects, or unwanted technical variation, and you have identified a set of negative control metabolites (e.g., spiked internal standards or blank-derived features) that are expected to show no biological signal. Use ruvrandclust specifically when you want to leverage negative control information with clustering (k parameter) to remove unwanted variation while preserving biological differences.

## When NOT to use

- Featuredata is already normalized or does not exhibit batch or matrix effects.
- Negative control metabolites cannot be reliably identified or are absent from the study design.
- The featuredata contains missing values that have not been handled by MissingValues() or log-transformation preprocessing.

## Inputs

- featuredata: metabolomics data matrix (samples × metabolites) with numeric peak intensities or concentrations
- metabolitedata: dataframe with metabolite identifiers as row names and neg_control column (0/1 indicator)
- sampledata: optional dataframe with sample identifiers as row names

## Outputs

- normalized featuredata: corrected metabolomics matrix (same dimensions as input)
- uvdata: matrix of estimated unwanted-variation components removed from each sample
- metadata: normalization parameters and control information

## How to apply

Load the featuredata, sampledata, and metabolitedata into R using NormalizeMets. Identify negative control metabolites by filtering metabolitedata on the neg_control column (e.g., which(UVdata$metabolitedata$neg_control==1)). Call NormQcmets() with method='ruvrandclust', k=1 (or higher for stronger clustering), and qcmets set to the indices of negative control metabolites. Extract the normalized featuredata and the uvdata component (the removed unwanted-variation matrix) from the returned object. The k parameter controls the number of factors of unwanted variation to estimate; k=1 removes a single underlying unwanted-variation component. Verify that the normalized output has the same dimensions as the input and that negative control metabolites show reduced intensity variance across samples.

## Related tools

- **NormalizeMets** (Primary R package providing NormQcmets() function for ruvrandclust normalization) — https://github.com/metabolomicstats/NormalizeMets
- **R** (Scientific computing environment required to install and run NormalizeMets)
- **RStudio** (Integrated development environment for interactive R workflow and debugging)
- **Microsoft Excel** (Graphical user interface wrapper for NormalizeMets functions (optional))

## Examples

```
neg_controls <- which(UVdata$metabolitedata$neg_control==1); uv_ruvrandclust <- NormQcmets(UVdata$featuredata, method='ruvrandclust', k=1, qcmets=neg_controls)
```

## Evaluation signals

- Output featuredata has identical dimensions (rows, columns) to input featuredata.
- Negative control metabolites show reduced variance or intensity range in the normalized matrix compared to the input.
- uvdata matrix has the same number of rows as featuredata (one unwanted-variation estimate per sample).
- Distribution of normalized intensities is reasonable (not collapsed to zero or extreme values); compare via histogram or summary statistics before/after.
- Biological samples cluster according to expected groupings (verified via PCA or RLA plots) after normalization, indicating biological signal is preserved.

## Limitations

- Requires valid identification of negative control metabolites; misidentification compromises accuracy.
- Method assumes negative control metabolites truly contain no biological signal; if controls are correlated with sample biology, unwanted variation removal may bias results.
- Missing values in featuredata must be pre-handled (via MissingValues() function) before normalization.
- RUV methods may underperform if the number of negative controls is very small relative to the number of metabolites.
- Choice of k parameter affects strength of unwanted-variation removal; no universal default applies to all studies.

## Evidence

- [other] NormQcmets with method='ruvrandclust', k=1, and qcmets set to the negative control indices to perform remove-unwanted-variation normalization with clustering: "Apply NormQcmets with method='ruvrandclust', k=1, and qcmets set to the negative control indices to perform remove-unwanted-variation normalization with clustering on the UVdata featuredata."
- [other] The NormQcmets function accepts featuredata as input and supports ruvrandclust as one of its normalization methods, enabling removal of unwanted variation from metabolomics data matrices.: "The NormQcmets function accepts featuredata as input and supports ruvrandclust as one of its normalization methods, enabling removal of unwanted variation from metabolomics data matrices."
- [other] Identify negative control metabolites from metabolitedata using the neg_control column: "Identify negative control metabolites from metabolitedata using the neg_control column (which(UVdata$metabolitedata$neg_control==1))."
- [readme] Metabolomics data are inevitably subject to a component of unwanted variation, due to factors such as batch effects, matrix effects, and confounding biological variation.: "Metabolomics data are inevitably subject to a component of unwanted variation, due to factors such as batch effects, matrix effects, and confounding biological variation."
- [readme] The input data format consists of three parts: (i) 'featuredata' which is the metabolomics data matrix containing all metabolite peak intensities (or concentrations). Unique sample names must be provided as row names and unique metabolite names as column names, (ii) 'metabolitedata' contains metabolite-specific information in a separate dataframe.: "The input data format consists of three parts: (i) 'featuredata' which is the metabolomics data matrix containing all metabolite peak intensities (or concentrations). Unique sample names must be"
