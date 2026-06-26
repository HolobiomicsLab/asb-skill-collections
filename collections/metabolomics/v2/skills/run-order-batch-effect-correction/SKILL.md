---
name: run-order-batch-effect-correction
description: Use when metabolomics featuredata exhibits run-order-dependent signal
  drift, matrix effects, or batch effects that correlate with the order in which samples
  were analyzed.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - R
  - NormalizeMets
  - RStudio
  - Microsoft Excel
  license_tier: open
  provenance_tier: literature
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

# run-order-batch-effect-correction

## Summary

Corrects unwanted variation in metabolomics feature data caused by run-order-dependent batch effects using RLSC (reference linear-based signal correction) normalization applied to quality-control samples. This skill removes systematic drift and instrumental variation that accumulates across the analytical sequence.

## When to use

Apply this skill when metabolomics featuredata exhibits run-order-dependent signal drift, matrix effects, or batch effects that correlate with the order in which samples were analyzed. Specifically, when your dataset includes dedicated QC (quality-control) samples interspersed throughout the analytical run and you need to normalize all feature intensities relative to these stable reference samples before downstream statistical analysis.

## When NOT to use

- Your dataset lacks quality-control (QC) samples or standard reference materials interspersed throughout the analytical run; RLSC depends on stable QC reference points to estimate drift.
- Run order is not a relevant source of variation (e.g., samples were randomized and instrumental drift is negligible); normalization may introduce noise rather than remove it.
- Input featuredata is already normalized by another method or is already a concentration-normalized feature table; applying RLSC sequentially may over-correct.

## Inputs

- featuredata: metabolomics data matrix with samples as rows and metabolites as columns (peak intensities or concentrations)
- sampledata: dataframe with samples as rows and sample-specific metadata as columns, including an 'order' column denoting run sequence
- metabolitedata (optional): dataframe with metabolite-specific annotations (internal/external standards, controls)

## Outputs

- Normalized featuredata matrix: log-transformed and run-order-corrected metabolite intensities with same dimensions as input

## How to apply

Sort both featuredata and sampledata by the run order column (sampledata$order) to arrange samples and QC samples chronologically. Call NormQcsamples() with the sorted featuredata and sampledata, specifying method='rlsc' to invoke reference linear-based signal correction. Set polynomial degree deg=2 to fit a smooth trend across the run, span=0 to allow automatic bandwidth selection, and lg=TRUE to log-transform the output, which stabilizes variance and improves normalization performance. The function uses QC samples to estimate and remove the time-dependent systematic bias from all metabolite features. Return the normalized featuredata matrix for subsequent quality assessment and biomarker analysis.

## Related tools

- **NormalizeMets** (R package containing NormQcsamples() function and supporting functions for assessing, selecting, and implementing normalization methods on metabolomics data) — https://github.com/metabolomicstats/NormalizeMets
- **R** (Statistical computing environment required to install and run NormalizeMets package functions)
- **RStudio** (Integrated development environment (IDE) recommended for interactive R scripting and debugging of normalization workflows)
- **Microsoft Excel** (Optional graphical user interface to NormalizeMets functions for users preferring point-and-click normalization workflow) — https://github.com/metabolomicstats/ExNormalizeMets

## Examples

```
library(NormalizeMets); data(Didata); featuredata_sorted <- Didata$featuredata[order(Didata$sampledata$order), ]; sampledata_sorted <- Didata$sampledata[order(Didata$sampledata$order), ]; normalized_features <- NormQcsamples(featuredata_sorted, sampledata_sorted, method='rlsc', span=0, deg=2, lg=TRUE)
```

## Evaluation signals

- Verify output featuredata has identical dimensions (rows = samples, columns = metabolites) and row/column names match input; no samples or features dropped.
- Confirm all output values are log-transformed (span multiple orders of magnitude) and positive; check for NaN, Inf, or missing values introduced by transformation or correction.
- Generate RLA (Relative Log Abundance) plots before and after normalization; run-order-corrected data should show centered, symmetrical boxplots per sample with reduced trend across run order.
- Apply PCA plots to normalized data; QC samples should cluster tightly together regardless of run position, indicating successful removal of run-order-dependent drift.
- Verify polynomial fit deg=2 is appropriate by examining loess smoothing diagnostics; inspect whether fitted trend captures instrumental drift without over-fitting noise.

## Limitations

- RLSC effectiveness depends critically on the number, distribution, and measurement stability of QC samples; sparse or unevenly distributed QC samples may yield poor drift estimation.
- The method assumes run-order effects follow a smooth, low-degree polynomial trend; abrupt batch breaks, instrument recalibration events, or non-monotonic drift may not be corrected adequately.
- Log transformation (lg=TRUE) requires all input feature intensities to be positive; zero or negative values (missing/imputed data) must be handled prior to normalization.
- RLSC is designed for metabolomics data with QC reference samples; application to other omics data types (genomics, proteomics) without adapting the QC sample concept is not recommended.
- No changelog documented; version compatibility and historical changes between releases of NormalizeMets are not formally tracked, limiting reproducibility across different package versions.

## Evidence

- [other] NormQcsamples is a function that accepts featuredata and sampledata as inputs, applies RLSC normalization with configurable parameters (method, span, deg, lg), and outputs a normalized feature data matrix.: "NormQcsamples is a function that accepts featuredata and sampledata as inputs, applies RLSC normalization with configurable parameters (method, span, deg, lg), and outputs a normalized feature data"
- [other] Sort featuredata and sampledata by run order (sampledata$order column). Call NormQcsamples with the sorted featuredata and sampledata, specifying method='rlsc', span=0, deg=2 (polynomial degree), and lg=TRUE (to log-transform output).: "Sort featuredata and sampledata by run order (sampledata$order column). Call NormQcsamples with the sorted featuredata and sampledata, specifying method='rlsc', span=0, deg=2 (polynomial degree), and"
- [readme] Metabolomics data are inevitably subject to a component of unwanted variation, due to factors such as batch effects, matrix effects, and confounding biological variation.: "Metabolomics data are inevitably subject to a component of unwanted variation, due to factors such as batch effects, matrix effects, and confounding biological variation."
- [readme] (i) 'featuredata' which is the metabolomics data matrix containing all metabolite peak intensities (or concentrations). Unique sample names must be provided as row names and unique metabolite names as column names, (ii) 'metabolitedata' contains metabolite-specific information in a separate dataframe.: "'featuredata' which is the metabolomics data matrix containing all metabolite peak intensities (or concentrations). Unique sample names must be provided as row names and unique metabolite names as"
- [readme] 'sampledata' is a dataframe that contains sample-specific information. These information can include sample type, order of analysis, factors of interest and other sample-specific data relevant to the analysis.: "'sampledata' is a dataframe that contains sample-specific information. These information can include sample type, order of analysis, factors of interest and other sample-specific data relevant to the"
