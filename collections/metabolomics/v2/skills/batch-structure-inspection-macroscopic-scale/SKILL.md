---
name: batch-structure-inspection-macroscopic-scale
description: Use when after loading log-transformed, pre-processed metabolomics feature abundance tables (samples × features, with batch identifiers in the first column) and prior to selecting a batch-effect correction model.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3935
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0091
  tools:
  - dbnorm
  - R
  - sva
  - R graphics libraries (ggplot2, lattice)
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

# batch-structure-inspection-macroscopic-scale

## Summary

Visually inspect the macroscopic structure of metabolomics datasets across analytical batches using unsupervised learning algorithms (PCA, hierarchical clustering) to identify spatial separation of sample sets and batch drift patterns before and after correction. This skill helps users evaluate whether batch effects are present and whether correction models have successfully removed technical heterogeneity.

## When to use

After loading log-transformed, pre-processed metabolomics feature abundance tables (samples × features, with batch identifiers in the first column) and prior to selecting a batch-effect correction model. Use this skill when you need to assess the overall structure of your data across batches, detect the presence of drift or batch-induced clustering, and visualize the impact of different correction models on sample-level batch separation.

## When NOT to use

- Input data has >2000 features (computational inefficiency for visualization functions; use decomposed dbnormBer, dbnormBagging, etc. instead)
- Data has not been normalized and log-transformed; raw count or intensity data will obscure batch structure due to high-abundance feature dominance
- Batch identifiers are missing or not properly encoded in the first column of the input matrix

## Inputs

- Log2-normalized metabolomics feature abundance matrix (.csv format)
- Batch identifiers (first column of data matrix)
- Samples as rows, metabolic features as columns
- Pre-processed data with missing values imputed

## Outputs

- PDF file containing PCA plots, Scree plots, Correlation plots, and Score plots
- RLA plots displayed in RStudio Viewer panel
- .csv files with Adjusted R-squared values for each feature and model comparison
- Score table indicating maximum Adjusted R-squared for each correction model

## How to apply

Load your .csv metabolomics data (log2-normalized, with batch levels in the first column and features in subsequent columns) into R and call the dbnorm visualization functions. The Visodbnorm function generates PCA and Scree plots to reveal sample clustering and batch-driven variance patterns at the macroscopic level. For computational efficiency with datasets <2000 features, run dbnormSCORE alongside Visodbnorm to obtain Adjusted R-squared metrics that quantify how well each correction model (ber, ber-bagging, parametric ComBat, non-parametric ComBat) removes batch-dependent variance. Compare the raw data visualization against the corrected datasets to assess which model best separates biological samples while removing batch-induced spatial clustering. The RLA (Relative Log Abundance) plots in the RStudio Viewer and the output PDF files provide graphical evidence of batch structure before and after correction.

## Related tools

- **dbnorm** (Core R package providing Visodbnorm, dbnormSCORE, and related visualization functions for macroscopic batch structure inspection) — https://github.com/NBDZ/dbnorm
- **sva** (Provides ComBat (parametric and non-parametric) batch-effect correction models integrated into dbnorm for comparative visualization)
- **R graphics libraries (ggplot2, lattice)** (Backend for rendering PCA, Scree, and Correlation plots in dbnorm visualizations)

## Examples

```
library(dbnorm); data<-read.csv("path/to/metabolomics_data.csv", sep=",", header=T, row.names=1); Visodbnorm(data); dbnormSCORE(data)
```

## Evaluation signals

- PCA plot shows distinct spatial clustering by batch in raw data; after correction, sample clusters should align with biological treatment/phenotype rather than batch identity
- Scree plot variance explained: batch-driven PC1/PC2 variance should decrease substantially after applying a successful correction model
- Adjusted R-squared values (dbnormSCORE output) show improvement from raw to corrected data; model with highest mean Adjusted R-squared across features is most effective
- RLA plots display shifted probability density functions across batches in raw data; after correction, feature distributions should converge across batches
- PDF output files are generated without errors and contain all four plot types; .csv files contain numeric scores with one row per feature and one column per model

## Limitations

- Visualization functions recommended for <2000 features due to computational and visual complexity; larger datasets should use decomposed functions (dbnormBer, dbnormBagging, etc.)
- PCA-based macroscopic inspection assumes that batch effects dominate lower-dimensional variance; strong biological signal may mask subtle batch structure
- Data must be pre-normalized and log2-transformed; raw abundances will obscure batch structure due to high-abundance feature dominance
- Hierarchical clustering analysis (hclustdbnorm) uses Pearson distance and average linkage; results depend on these distance metric choices and may not reveal non-Euclidean batch patterns

## Evidence

- [readme] By including advanced statistical tools, the *dbnorm* package allows user to inspect the structure and quality of large metabolomics datasets both in macroscopic and microscopic scales at the sample batch level: "allows user to inspect the structure and quality of large metabolomics datasets both in macroscopic and microscopic scales at the sample batch level"
- [other] functions using advanced statistical tools to generate several diagnosis plots to help users to choose the statistical model which better fits to their data structure: "generate several diagnosis plots to help users to choose the statistical model which better fits to their data structure"
- [readme] Graphical inferences in the context of unsupervised learning algorithms create visual inspection to inform users about the spatial separation of the sample sets analyzed in the different analytical runs: "Graphical inferences in the context of unsupervised learning algorithms create visual inspection to inform users about the spatial separation of the sample sets analyzed in the different analytical"
- [readme] This function is suggested for less than 2000 features (variables) for better computational speed.: "This function is suggested for less than 2000 features (variables) for better computational speed"
- [readme] Data to be uploaded must be normalized and scaled on the log2 to account for the high abundance features (variables) by which technical heterogeneity might be overlooked.: "Data to be uploaded must be normalized and scaled on the log2 to account for the high abundance features"
