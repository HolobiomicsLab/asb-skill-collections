---
name: diagnostic-plot-generation-for-batch-effects
description: Use when after loading log-transformed metabolomics feature abundance tables (samples as rows, metabolic features as columns) with batch identifiers, and before committing to a single batch-correction model.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3673
  tools:
  - dbnorm
  - R
  - sva
  - ggplot2
  - ber
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# diagnostic-plot-generation-for-batch-effects

## Summary

Generate and compare diagnostic visualizations (PCA, RLA, correlation, and probability density function plots) before and after batch-effect correction to evaluate which statistical model (parametric vs. non-parametric ComBat, or two-stage ber procedure) best fits the structure and quality of metabolomics datasets.

## When to use

After loading log-transformed metabolomics feature abundance tables (samples as rows, metabolic features as columns) with batch identifiers, and before committing to a single batch-correction model. Use this skill when you need to inspect batch structure, drift patterns, and data quality at both sample-batch and metabolic-feature levels to select the correction method that minimizes technical heterogeneity without obscuring biological signal.

## When NOT to use

- When input data is already in count-per-million (CPM) or compositional form — dbnorm expects log2-normalized abundance values
- When datasets contain >2,000 features and real-time visualization is required — use decomposed functions (dbnormBer, dbnormPcom, etc.) instead of Visodbnorm() for computational efficiency
- When batch structure is unknown or not recorded in the input file — batch levels must be explicitly specified in the first column

## Inputs

- CSV file: log2-normalized metabolomics feature abundance matrix (samples × features, with batch column)
- Batch factor vector (first column of input CSV)
- Raw metabolomics data matrix (uncorrected counts or intensities, log-transformed)

## Outputs

- PDF file: compiled diagnostic plots (PCA, Scree, RLA, Correlation, Score plots)
- CSV files: Adjusted R-squared values per feature and per model
- CSV files: corrected metabolomics datasets for each applied statistical model
- RLA plots (visualized in RStudio Viewer panel)
- Model performance score table (maximum Adjusted R-squared per model)

## How to apply

Load CSV metabolomics data normalized and log2-scaled, with batch levels in the first column and features in remaining columns. Apply the dbnorm package functions Visodbnorm() or dbnormSCORE() to generate diagnostic plots comparing raw versus corrected data across three statistical models: two-stage procedure (ber), ber-bagging, parametric ComBat, and non-parametric ComBat. Inspect the resulting PCA plots (to assess sample cluster separation by batch before/after correction), RLA plots (relative log abundance to detect drift), correlation plots, and probability density function plots of feature distributions. Calculate Adjusted R-squared values for each model to quantify the maximum variability explained by batch in both raw and corrected data; select the model with the lowest residual batch signal and highest consistency across all features. For datasets with fewer than 2,000 features, use Visodbnorm() for faster computation; for larger datasets, decompose into separate dbnormBer(), dbnormBagging(), dbnormPcom(), and dbnormNPcom() functions.

## Related tools

- **dbnorm** (Primary package providing Visodbnorm(), dbnormSCORE(), and individual correction functions (dbnormBer, dbnormPcom, dbnormNPcom) that generate diagnostic plots and apply batch-correction models) — https://github.com/NBDZ/dbnorm
- **sva** (Provides ComBat parametric and non-parametric empirical Bayes methods for batch correction, called within dbnorm functions)
- **ggplot2** (R graphics library used by dbnorm to render PCA, RLA, correlation, and distribution plots)
- **ber** (Two-stage batch effect removal procedure (Giordan 2013) implemented in dbnorm as alternative to ComBat) — https://cran.r-project.org/src/contrib/Archive/

## Examples

```
library(dbnorm)
data <- read.csv("path/to/metabolomics_log2_normalized.csv", sep=",", header=TRUE, row.names=1)
Visodbnorm(data)
dbnormSCORE(data)
```

## Evaluation signals

- PCA plots show reduced batch clustering and improved sample-type separation after correction compared to raw data
- RLA (Relative Log Abundance) plots exhibit centered, symmetric distributions around zero after correction, indicating removal of across-batch signal drift
- Adjusted R-squared values are substantially lower (closer to 0) after correction than in raw data, confirming reduced dependence of features on batch level
- Probability density function plots of feature distributions align across batches in corrected data but remain shifted in raw data
- Model performance score identifies one statistical model with consistently lower Adjusted R-squared across all features, indicating best fit to the data structure

## Limitations

- Computational speed degrades for datasets with >2,000 features; README recommends using decomposed individual functions (dbnormBer, dbnormPcom, etc.) instead of Visodbnorm() for large feature sets
- Input data must be pre-normalized to log2 scale; high-abundance features not log-transformed may mask technical heterogeneity and invalidate model selection
- Diagnostic plots assume batch structure is known and correctly recorded in the first column; missing, mislabeled, or implicit batch information will produce misleading visualizations
- No changelog provided for dbnorm package versions, limiting reproducibility across version changes
- RLA plots are rendered in RStudio Viewer panel only; batch structure must be inspected interactively and cannot be exported as static PDF without manual intervention

## Evidence

- [readme] functions using advanced statistical tools to generate several diagnosis plots to help users to choose the statistical model which better fits to their data structure: "functions using advanced statistical tools to generate several diagnosis plots to help users to choose the statistical model which better fits to their data structure"
- [other] dbnorm includes functions that use advanced statistical tools to generate several diagnosis plots that help users choose the statistical model which better fits their data structure: "dbnorm includes functions that use advanced statistical tools to generate several diagnosis plots that help users choose the statistical model which better fits their data structure"
- [readme] Data to be uploaded must be normalized and scaled on the log2 to account for the high abundance features (variables) by which technical heterogeneity might be overlooked: "Data to be uploaded must be normalized and scaled on the log2 to account for the high abundance features (variables)"
- [readme] Graphical check such as *PCA* plot and *Scree* plot compiled into a **PDF** (saved in the working directory) and three **.csv** files (saved in a folder, intiate with *Rtmpe*, in Users's Temporary directory): "Graphical check such as *PCA* plot and *Scree* plot compiled into a **PDF** (saved in the working directory) and three **.csv** files"
- [readme] the adjusted coefficient of determination or Adjusted R-Squared is calculated for each variable estimated in a regression model for its dependency to the batch level in the raw data and treated data: "adjusted coefficient of determination or Adjusted R-Squared is calculated for each variable estimated in a regression model for its dependency to the batch level"
- [readme] The *RLA* plots are visualized in the **Viewer** panel in the **rstudio** console.: "The *RLA* plots are visualized in the **Viewer** panel in the **rstudio** console"
- [readme] This function is suggested for less than 2000 features (variables) for better computational speed.: "This function is suggested for less than 2000 features (variables) for better computational speed"
- [readme] the graphical inferences in the context of unsupervised learning algorithms create visual inspection to inform users about the spatial separation of the sample sets analyzed in the different analytical runs alongside the distribution of features (variables) in the raw and treated datasets: "visual inspection to inform users about the spatial separation of the sample sets analyzed in the different analytical runs alongside the distribution of features"
