---
name: unwanted-variation-removal
description: Use when metabolomics featuredata exhibits unwanted variation from batch
  effects, matrix effects, or confounding factors;
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - NormalizeMets
  - RStudio
  - LogTransform
  - MissingValues
  - NormQcmets
  - RlaPlots
  license_tier: restricted
derived_from:
- doi: 10.1007/s11306-018-1347-7
  title: NormalizeMets
evidence_spans:
- The R software environment can be downloaded for free from the Comprehensive R Archive
  Network (CRAN)
- 'Install the NormalizeMets package by using the following function: `install.packages("NormalizeMets")`'
- The use of RStudio is also recommended. RStudio is an integrated development environment
  (IDE)
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

# unwanted-variation-removal

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Remove unwanted batch effects, matrix effects, and confounding biological variation from metabolomics feature matrices using statistical normalization methods. This skill selects and applies normalization methods (internal standards, RUV-based approaches, or combined methods) to produce normalized metabolite intensity data suitable for downstream biomarker analysis.

## When to use

Apply this skill when metabolomics featuredata exhibits unwanted variation from batch effects, matrix effects, or confounding factors; the decision to apply and which method to use depends on the availability of internal/external standards, negative controls, or quality control metabolites in your metabolitedata, and whether you have access to design factors or need unsupervised variance removal.

## When NOT to use

- Input featuredata is already normalized or does not exhibit batch or matrix effects (assessment via RlaPlots or PcaPlots should precede this skill).
- Metabolitedata lacks internal standards, negative controls, or QC designations and the analysis goal requires supervised (design-aware) normalization rather than unsupervised RUV.
- Featuredata is in non-intensity units (e.g., already scaled, z-scored, or in arbitrary units) without clear zero handling or log-scale justification.

## Inputs

- featuredata (metabolomics data matrix: samples × metabolites)
- metabolitedata (dataframe with IS, neg_control, or QC designation columns)
- sampledata (optional; sample metadata including batch, order of analysis, factors)
- log-transformed and imputed featuredata (output from LogTransform and MissingValues)
- indices or factor vectors identifying quality control metabolites or sample design

## Outputs

- normalized featuredata matrix (samples × metabolites)
- unwanted-variation component (uvdata; removed variation matrix)
- normalized object containing normalized featuredata, metadata, and method parameters

## How to apply

Load featuredata, sampledata, and metabolitedata into R using NormalizeMets. First, log-transform featuredata using LogTransform with base=exp(1) and zerotona=TRUE to handle zeros; optionally use MissingValues with feature.cutoff=0.8, sample.cutoff=0.8 to impute missing values. Identify quality control metabolites (internal standards, negative controls, or QC pools) from the metabolitedata using columns such as IS, neg_control, or QC designation. Select a normalization method based on available metadata: use 'is' or 'nomis' for internal standard-based normalization, 'ccmn' for combined correction, 'ruv2' or 'ruvrand' for RUV approaches with specified k parameter and design factors, or 'ruvrandclust' for unsupervised clustering-based unwanted variation removal. Call NormQcmets (or NormQcsamples for sample-level QC) with the log-transformed featuredata, pass QC metabolite indices via qcmets parameter, and provide method-specific parameters (isvec for 'is', k for RUV methods, factors for design-aware methods). Extract the normalized featuredata matrix from the output object.

## Related tools

- **NormalizeMets** (R package containing NormQcmets, NormQcsamples, LogTransform, and MissingValues functions for metabolomics normalization and preprocessing) — github.com/metabolomicstats/NormalizeMets
- **R** (Statistical computing environment in which NormalizeMets functions are executed)
- **RStudio** (IDE for interactive R-based normalization workflows and data exploration)
- **LogTransform** (NormalizeMets function to log-transform featuredata prior to normalization, handling zeros via zerotona parameter) — github.com/metabolomicstats/NormalizeMets
- **MissingValues** (NormalizeMets function to impute missing values in featuredata using feature.cutoff and sample.cutoff thresholds) — github.com/metabolomicstats/NormalizeMets
- **NormQcmets** (Core normalization function accepting featuredata and supporting six normalization methods (is, nomis, ccmn, ruv2, ruvrand, ruvrandclust)) — github.com/metabolomicstats/NormalizeMets
- **RlaPlots** (Visualization function to assess unwanted variation before and after normalization) — github.com/metabolomicstats/NormalizeMets

## Examples

```
# Load data, log-transform, identify QC metabolites, and normalize using ruvrandclust
data(UVdata); qcmets <- which(UVdata$metabolitedata$neg_control==1); ft_log <- LogTransform(UVdata$featuredata, base=exp(1), zerotona=TRUE); norm_obj <- NormQcmets(ft_log, method='ruvrandclust', k=1, qcmets=qcmets); uv_ruvrandclust <- norm_obj$featuredata
```

## Evaluation signals

- Normalized featuredata dimensions match input featuredata (same samples and metabolites); no rows or columns lost.
- RlaPlots or PcaPlots applied to normalized featuredata show reduced batch clustering compared to raw featuredata; unwanted-variation component (uvdata) has visibly smaller variance than input.
- Method-specific parameters are correctly passed and documented in output object metadata (e.g., k value for RUV methods, method name, QC metabolite indices used).
- Normalized featuredata contains no NaN, Inf, or unexpected zero inflation after log-transformation and normalization (schema validation).
- Downstream biomarker identification or statistical tests on normalized featuredata produce effect sizes or p-values consistent with removal of confounding factors (e.g., reduced variance explained by batch, increased signal in factors of interest).

## Limitations

- Normalization method effectiveness depends critically on correct identification and availability of quality control metabolites; if IS/QC designations are incorrect or missing, normalization will fail or produce biased results.
- RUV methods (ruv2, ruvrand, ruvrandclust) assume that unwanted variation can be learned from negative control metabolites or replicate measurements; if controls are contaminated or sparse, performance degrades.
- Log-transformation with zerotona=TRUE and missing value imputation (knn, replace) require careful parameter selection (feature.cutoff, sample.cutoff); excessive filtering can discard valid metabolites, while lenient thresholds retain noise.
- Combined normalization (NormCombined) and multi-method comparison are not automated; practitioner must assess and choose normalization method manually using RlaPlots, PcaPlots, or HeatMap.
- Metabolomics-specific data structures (featuredata, sampledata, metabolitedata) must be strictly formatted with unique row/column names; violations cause function failures or silent errors.

## Evidence

- [readme] Metabolomics data are inevitably subject to a component of unwanted variation, due to factors such as batch effects, matrix effects, and confounding biological variation.: "Metabolomics data are inevitably subject to a component of unwanted variation, due to factors such as batch effects, matrix effects, and confounding biological variation."
- [other] The NormQcmets function accepts featuredata as input and supports multiple normalization methods including is, nomis, ccmn, ruv2, ruvrand, and ruvrandclust.: "NormQcmets <- function(featuredata, factors = NULL, method = c("is", "nomis", "ccmn", "ruv2", "ruvrand", "ruvrandclust")"
- [other] Log-transform the featuredata using LogTransform with base=exp(1) and zerotona=TRUE to handle zeros.: "Log-transform the featuredata using LogTransform with base=exp(1) and zerotona=TRUE to handle zeros."
- [other] Identify quality control metabolites (internal standards) from the metabolitedata using the IS column.: "Identify quality control metabolites (internal standards) from the metabolitedata using the IS column."
- [other] Apply NormQcmets with method='ruvrandclust', k=1, and qcmets set to the negative control indices to perform remove-unwanted-variation normalization with clustering.: "Apply NormQcmets with method='ruvrandclust', k=1, and qcmets set to the negative control indices to perform remove-unwanted-variation normalization with clustering on the UVdata featuredata."
- [readme] The input data format consists of featuredata (metabolomics data matrix with samples as rows and metabolites as columns), metabolitedata (metabolite-specific information), and sampledata (sample-specific information).: "The input data format consists of three parts: (i) "featuredata" which is the metabolomics data matrix containing all metabolite peak intensities (or concentrations). Unique sample names must be"
