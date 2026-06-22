---
name: metabolite-feature-visualization-across-batches
description: Use when after applying batch-effect correction methods (parametric ComBat, non-parametric ComBat, ber, or ber-bagging) to log-transformed metabolomics abundance matrices, use this skill when you need to visually inspect whether technical heterogeneity (drift across batch, signal shift) has been.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - dbnorm
  - R
  - sva
  - ber
  - R graphics
derived_from:
- doi: 10.1038/s41598-021-84824-3
  title: Dbnorm
- doi: 10.1007/s12561-013-9081-1
  title: ''
evidence_spans:
- dbnorm (V-0.2.2) A package for drift across batches normalization and visualization
- dbnorm contains R functions which allow visualization and removal of technical heterogeneity
- '*dbnorm* contains R functions which allow visualization and removal of technical heterogeneity'
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

# metabolite-feature-visualization-across-batches

## Summary

Generate diagnostic visualizations that compare corrected versus uncorrected metabolomics feature distributions across batches to assess batch-effect correction model performance and select the statistical model that best fits the data structure.

## When to use

After applying batch-effect correction methods (parametric ComBat, non-parametric ComBat, ber, or ber-bagging) to log-transformed metabolomics abundance matrices, use this skill when you need to visually inspect whether technical heterogeneity (drift across batch, signal shift) has been adequately removed and to compare the effectiveness of competing correction models on individual metabolic features.

## When NOT to use

- Input data has not been log-transformed or is in raw (non-normalized) scale; profile plots may be dominated by high-abundance features and obscure batch-related drift
- Dataset contains >2000 metabolic features; computational speed degrades significantly for dbnormSCORE and profile plot generation
- Batch structure is not documented or batch labels are missing from the data matrix; visualization cannot stratify samples by analytical run

## Inputs

- log-transformed metabolomics abundance matrix (CSV format: samples × features, batch labels in first column)
- batch assignment vector (levels or group identifiers for each sample)

## Outputs

- PDF report containing probability density function (PDF) profile plots for raw and corrected features
- PDF report with correlation plots and adjusted R-squared score comparison across models
- CSV files with adjusted R-squared values for each feature and model performance scores
- RLA (Relative Log Abundance) plots visualized in RStudio Viewer panel

## How to apply

Load log-transformed metabolomics data (samples as rows, metabolic features as columns, batch labels in the first column) into R and invoke visualization functions that generate probability density function (PDF) profile plots for features in both raw and corrected datasets. Use ProfPlotraw to visualize uncorrected feature distributions, then apply model-specific profile plot functions (ProfPlotBer, ProfPlotComPara, ProfPlotComNPara) to inspect the shifted distributions after correction. Compile these graphical outputs into PDF reports showing side-by-side raw versus corrected density curves, which reveal whether batch-related signal drift has been successfully attenuated. For datasets with <2000 features, also generate correlation plots and adjusted R-squared score plots (dbnormSCORE function) to quantify which model explains the least variance attributable to batch, enabling model selection based on both visual inspection and performance metrics.

## Related tools

- **dbnorm** (R package providing ProfPlotraw, ProfPlotBer, ProfPlotComPara, ProfPlotComNPara, dbnormSCORE, and Visodbnorm functions to generate feature-level diagnostic visualizations comparing raw and batch-corrected metabolomics data) — https://github.com/NBDZ/dbnorm
- **sva** (R/Bioconductor package providing parametric and non-parametric ComBat batch-effect correction models whose performance is evaluated via dbnorm profile plots)
- **ber** (R package implementing two-stage batch-effect removal procedure; wrapped in dbnorm for model comparison via feature profile visualization)
- **R graphics** (Base R plotting infrastructure used to render PDF and PNG diagnostic visualizations of batch structure and feature distributions)

## Examples

```
library(dbnorm); data <- read.csv('path/to/metabolomics.csv', sep=',', header=T, row.names=1); ProfPlotraw(data); ProfPlotComPara(data); dbnormSCORE(data)
```

## Evaluation signals

- PDF profile plots show reduced overlap and signal shift between batch groups in corrected data compared to raw data; batch-stratified density curves converge toward a single distribution
- Adjusted R-squared values for corrected data are substantially lower than raw data across all features, indicating reduced batch-dependent variance
- dbnormSCORE output identifies a single model with maximum adjusted R-squared and consistent performance across features, signaling robust model selection
- RLA (Relative Log Abundance) plots in RStudio Viewer show symmetric, centered distributions around zero in corrected data rather than systematic drift patterns visible in raw data
- Correlation plots compiled in PDF show high correlation between biological replicates (quality control samples) analyzed in different batches after correction but not before

## Limitations

- Profile plot visualization is computationally expensive for >2000 features; dbnorm documentation recommends this skill for <2000 features for acceptable speed
- Visualization quality depends on adequate batch sample size; sparse or highly imbalanced batch designs may produce uninformative density plots
- Probability density function plots are univariate and do not capture batch effects in multivariate feature space or correlations between features; PCA-based visualization (Visodbnorm) recommended as complementary assessment
- Model selection via profile plots and adjusted R-squared is data-driven but not hypothesis-driven; no statistical significance testing is performed; final model choice should incorporate domain knowledge

## Evidence

- [intro] functions using advanced statistical tools to generate several diagnosis plots to help users to choose the statistical model which better fits to their data structure: "functions using advanced statistical tools to generate several diagnosis plots to help users to choose the statistical model which better fits to their data structure"
- [readme] Graphical check such as the plots compiled into a PDF file (saved in the working directory) and a .csv file: "Graphical check such as the plots compiled into a PDF file (saved in the working directory) and a .csv file"
- [readme] These functions allow users to adjust the data for batch effect using either of models implemented in the package described earlier, and inform about the presence of across batch signal drift or batch effect in the raw and treated data represented via the shifted probability density function (PDF) plots of the features: "the shifted probability density function (PDF) plots of the features (variables) detected in an experiment"
- [readme] This function is suggested for less than 2000 features (variables) for better computational speed: "This function is suggested for less than 2000 features (variables) for better computational speed"
- [readme] By including advanced statistical tools, the *dbnorm* package allows user to inspect the structure and quality of large metabolomics datasets both in macroscopic and microscopic scales at the sample batch level and metabolic feature level: "inspect the structure and quality of large metabolomics datasets both in macroscopic and microscopic scales at the sample batch level and metabolic feature level"
