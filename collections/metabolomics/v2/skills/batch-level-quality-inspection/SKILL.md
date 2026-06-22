---
name: batch-level-quality-inspection
description: Use when after loading a raw metabolomics data matrix (samples × features in CSV format, log2-normalized with batch labels in the first column) and before selecting a batch correction model.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - dbnorm
  - R
  - sva
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

# batch-level-quality-inspection

## Summary

Inspect the structure and quality of metabolomics datasets at sample batch level and metabolic feature level to detect batch effects and technical heterogeneity before applying normalization. This diagnostic step uses advanced statistical tools and visualization to identify whether batch correction is needed and which statistical model best fits the data structure.

## When to use

After loading a raw metabolomics data matrix (samples × features in CSV format, log2-normalized with batch labels in the first column) and before selecting a batch correction model. Apply this skill when you need to assess whether technical drift or batch effects are present, evaluate dissimilarity between quality control replicates across batches, and compare the performance of candidate correction models (ber, ber-bagging, parametric ComBat, non-parametric ComBat) on your specific data structure.

## When NOT to use

- Input data is not yet log2-normalized or missing values have not been estimated — complete preprocessing with emvd() or emvf() first.
- Feature count exceeds 2000 — both Visodbnorm() and dbnormSCORE() are documented as less suitable for >2000 features due to computational speed and visualization clarity.
- Batch structure is unknown or batch labels are not provided in the first column of the input matrix — batch-level inspection requires explicit batch annotation.

## Inputs

- Metabolomics data matrix (CSV): rows=samples, columns=metabolic features, first column=batch identifier
- Data must be log2-normalized and scaled to account for high-abundance features
- Missing values must be estimated/imputed prior to inspection

## Outputs

- PDF file: PCA plots, Scree plots, RLA (Relative Log Abundance) plots, correlation plots, density profile plots (PDF saved to working directory)
- CSV files: Adjusted R² values for each feature under each model, comparative score table for model performance, hierarchical clustering distance matrices (saved to temporary Rtmpe folder)
- RLA visualization plots (displayed in RStudio Viewer panel)

## How to apply

Load the preprocessed and imputed metabolomics matrix (CSV format, rows=samples, columns=features, batch identifier in first column). Call the diagnostic functions in sequence: (1) Visodbnorm() to generate PCA plots, Scree plots, and RLA plots for visual inspection of batch separation and feature distributions in raw vs. adjusted data across all implemented models; (2) dbnormSCORE() to compute adjusted R² for each feature's dependence on batch level and produce a comparative score table showing which model maximizes variance explained by batch, facilitating selection of the most appropriate correction approach; (3) hclustdbnorm() to evaluate dissimilarity between replicate samples across batches using hierarchical clustering with Pearson distance and average linkage before and after correction. Use the graphical outputs (PDF files with PCA, correlation, and density plots) and CSV score matrices to judge model fit. Select the model showing the highest adjusted R² score reduction and clearest batch-level separation elimination in PCA space.

## Related tools

- **dbnorm** (Implements Visodbnorm(), dbnormSCORE(), hclustdbnorm(), and diagnostic plot functions for batch-level and feature-level quality inspection using PCA, correlation, RLA, and hierarchical clustering visualization.) — https://github.com/NBDZ/dbnorm
- **R** (Execution environment; required for calling dbnorm functions and generating diagnostic plots.)
- **sva** (Provides ComBat parametric and non-parametric batch correction models that are evaluated during quality inspection.)

## Examples

```
data <- read.csv('path/to/mydata.csv', sep = ',', header = T, row.names = 1)
library(dbnorm)
Visodbnorm(data)
dbnormSCORE(data)
hclustdbnorm(data)
```

## Evaluation signals

- PCA plot shows clear spatial separation of batch clusters in raw data that is reduced or eliminated after correction, indicating batch effect was present and successfully detected.
- Adjusted R² values decrease substantially after correction for each model; the selected model shows the largest reduction in batch-level variance explained (closest to zero in adjusted R² for corrected data).
- Score table indicates consistent performance across features (low variance in adjusted R² across the feature matrix after correction), signaling the model fits the data structure well.
- Hierarchical clustering dendrogram shows quality control replicates analyzed in different batches cluster together after correction, demonstrating batch effect removal improved replicate consistency.
- Density profile plots (PDF) show shifted probability density functions in raw data aligned or overlapping in corrected data across batches, visually confirming drift correction.

## Limitations

- Recommended for metabolomics datasets with <2000 features; computational performance and visualization clarity degrade for larger feature sets.
- Inspection functions rely on graphical interpretation (PCA, RLA plots, density plots); subjective judgment required to select among candidate models when score metrics are similar.
- RLA plots only display in RStudio Viewer panel; may not be accessible in non-interactive or headless R environments.
- Requires complete batch labeling and preprocessing; cannot inspect data with missing or ambiguous batch assignments.

## Evidence

- [readme] By including advanced statistical tools, the *dbnorm* package allows user to inspect the structure and quality of large metabolomics datasets both in macroscopic and microscopic scales at the sample batch level and metabolic feature level: "By including advanced statistical tools, the *dbnorm* package allows user to inspect the structure and quality of large metabolomics datasets both in macroscopic and microscopic scales at the sample"
- [intro] dbnorm includes advanced statistical tools to inspect structure and quality of metabolomics datasets at sample batch level and metabolic feature level: "includes advanced statistical tools to inspect structure and quality of metabolomics datasets at sample batch level and metabolic feature level"
- [readme] This function is suggested for less than 2000 features (variables).: "This function is suggested for less than 2000 features (variables)."
- [readme] This function allows users to evaluate dissimilarity between identical samples (quality control replicates or analytical replicates) analyzed in different batches, prior and after correction: "This function allows users to evaluate dissimilarity between identical samples (quality control replicates or analytical replicates) analyzed in different batches, prior and after correction"
- [readme] the adjusted coefficient of determination or Adjusted R-Squared is calculated for each variable estimated in a regression model for its dependency to the batch level in the raw data and treated data: "the adjusted coefficient of determination or Adjusted R-Squared is calculated for each variable estimated in a regression model for its dependency to the batch level in the raw data and treated data"
