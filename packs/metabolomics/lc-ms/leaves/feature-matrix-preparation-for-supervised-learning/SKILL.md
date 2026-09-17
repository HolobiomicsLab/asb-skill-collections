---
name: feature-matrix-preparation-for-supervised-learning
description: Use when you have preprocessed metabolomics feature abundance data and
  want to train multiple classifiers (traditional ML or deep learning) to predict
  sample phenotype or disease status.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_3520
  tools:
  - Lilikoi v2.0
  - R
  - h2o
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1093/gigascience/giaa162
  title: Lilikoi V2.0
evidence_spans:
- The new Lilikoi v2.0 R package has implemented a deep-learning method for classification,
  in addition to popular machine learning methods.
- Lilikoi v2.0 is a modern, comprehensive package to enable metabolomics analysis
  in R programming environment.
- DL via h2o
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lilikoi_v2_0_cq
    doi: 10.1093/gigascience/giaa162
    title: Lilikoi V2.0
  dedup_kept_from: coll_lilikoi_v2_0_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/gigascience/giaa162
  all_source_dois:
  - 10.1093/gigascience/giaa162
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# feature-matrix-preparation-for-supervised-learning

## Summary

Prepare a preprocessed metabolomics feature matrix with corresponding sample labels for input to supervised machine learning and deep learning classifiers. This skill transforms raw or intermediate metabolomics data into the structured matrix and label format required by the Lilikoi v2.0 machine_learning module.

## When to use

You have preprocessed metabolomics feature abundance data and want to train multiple classifiers (traditional ML or deep learning) to predict sample phenotype or disease status. Specifically, when you need to format an expression matrix and phenotype labels for cross-validated, multi-algorithm comparison using Lilikoi v2.0.

## When NOT to use

- Input data is already a pre-trained classifier object or model weights — use skill only for data preparation, not model inference.
- Metabolomics matrix contains missing values or requires imputation — this skill assumes preprocessing is complete; apply imputation before this skill.
- You are performing unsupervised learning (e.g., clustering, PCA) — this skill is specific to supervised classification workflows.

## Inputs

- preprocessed metabolomics feature matrix (numeric; rows=metabolites, columns=samples)
- sample phenotype labels (factor or character vector; length=ncol(matrix))
- optional: metabolite-to-pathway mapping table (from lilikoi.MetaTOpathway())
- optional: pathway feature selection results (from lilikoi.featuresSelection())

## Outputs

- formatted input matrix ready for lilikoi.machine_learning() (MLmatrix parameter)
- aligned sample label vector (measurementLabels parameter)
- pathway-aggregated abundance matrix (PDSmatrix) if pathway engineering applied
- filtered pathway list if feature selection applied

## How to apply

Load the preprocessed metabolomics feature matrix (rows = metabolites, columns = samples) and corresponding sample labels (e.g., disease/control phenotypes) into R using lilikoi.Loaddata() or equivalent. Ensure the matrix is numeric, with metabolite identifiers as row names and sample identifiers as column names; labels should be a factor or character vector aligned to matrix columns. Perform pathway-level feature engineering if needed using lilikoi.MetaTOpathway() to convert metabolite names to HMDB identifiers and lilikoi.PDSfun() to aggregate metabolites into pathway abundance scores (PDSmatrix). Optionally filter pathways using lilikoi.featuresSelection() with a threshold (e.g., 0.50) to reduce feature dimensionality and improve classifier stability. Pass the final matrix (metabolite-level or pathway-aggregated) and labels to lilikoi.machine_learning() with configurable parameters: trainportion (0.8), cvnum (10 folds), dlround (50 rounds), nrun (10 iterations), and classifier flags (Rpart, LDA, SVM, RF, GBM, PAM, LOG, DL). This structure enables direct comparison of multiple algorithms on the same training/validation splits.

## Related tools

- **Lilikoi v2.0** (R package implementing machine_learning module that accepts the prepared matrix and labels; integrates h2o for deep learning and supports Rpart, LDA, SVM, RF, GBM, PAM, LOG classifiers) — https://github.com/lanagarmire/lilikoi2
- **R** (Programming environment for loading data, executing lilikoi functions, and managing matrices and labels)
- **h2o** (Deep learning backend integrated into Lilikoi v2.0 for training the DL classifier on the prepared matrix)

## Examples

```
dt <- lilikoi.Loaddata(file="plasma_breast_cancer.csv"); PDSmatrix <- lilikoi.PDSfun(lilikoi.MetaTOpathway('name')$table); lilikoi.machine_learning(MLmatrix = PDSmatrix, measurementLabels = dt$Metadata$Label, trainportion = 0.8, cvnum = 10, dlround = 50, nrun = 10, DL = TRUE, SVM = TRUE, RF = TRUE)
```

## Evaluation signals

- Matrix dimensions match expected input: nrow(matrix) ≥ 1, ncol(matrix) = length(labels), no NA or NaN values in numeric matrix.
- Labels are properly aligned: each column of the matrix corresponds to exactly one entry in the labels vector; label values are discrete/categorical (factor levels or unique character strings).
- If pathway aggregation applied: pathway abundance scores (PDSmatrix) have fewer rows than original metabolite matrix; row names correspond to pathway identifiers; values are numeric and in expected ranges for the metabolomics platform.
- If feature selection applied: filtered pathway list is a subset of full pathway list; selection threshold and method (gain, etc.) are recorded and reproducible.
- Lilikoi.machine_learning() executes without errors on the prepared matrix and labels; cross-validation splits are created correctly (trainportion=0.8 produces ~80% training set per fold).

## Limitations

- Lilikoi v2.0 assumes balanced or manageable class distributions; highly imbalanced phenotypes may require additional weighting or stratification not covered by this skill.
- Pathway aggregation using lilikoi.PDSfun() requires a complete metabolite-to-pathway mapping; metabolites without pathway assignments will be excluded, potentially losing information.
- Feature selection threshold (e.g., 0.50 in lilikoi.featuresSelection) is user-specified; no guidance is provided in the README on optimal threshold selection for different metabolomics datasets.
- The skill does not address batch correction, normalization beyond preprocessing, or integration of multi-modal data; assumes input matrix is already quality-controlled.

## Evidence

- [readme] Load and align feature matrix with labels: "dt <- lilikoi.Loaddata(file=system.file("extdata", "plasma_breast_cancer.csv", package = "lilikoi")); Metadata <- dt$Metadata; dataSet <- dt$dataSet"
- [readme] Apply pathway transformation and feature engineering: "convertResults=lilikoi.MetaTOpathway('name'); Metabolite_pathway_table = convertResults$table; PDSmatrix=lilikoi.PDSfun(Metabolite_pathway_table); selected_Pathways_Weka="
- [other] Module accepts expression matrix, labels, and configurable parameters: "The Lilikoi v2.0 machine_learning module accepts an expression matrix and labels, supports multiple classifiers (Rpart, LDA, SVM, RF, GBM, PAM, LOG, and DL), and provides configurable parameters"
- [readme] Machine learning function invocation with prepared matrix and labels: "lilikoi.machine_learning(MLmatrix = Metadata, measurementLabels = Metadata$Label, significantPathways = 0, trainportion = 0.8, cvnum = 10, dlround=50,nrun=10, Rpart=TRUE,"
- [intro] Workflow includes preprocessing and pathway-level aggregation: "Lilikoi v2.0 supports data preprocessing, exploratory analysis, pathway visualization and metabolite-pathway regression"
