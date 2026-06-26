---
name: machine-learning-regulatory-prediction
description: Use when you have matched multiomics data (CNV, mutations, DNA methylation,
  histone PTMs, transcriptomics, miRNA, lncRNA, proteomics, phosphoproteomics) and
  metabolomics measurements across a cell line panel or cohort, and you want to infer
  which molecular features (genes, regulatory marks, splice.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2945
  edam_topics:
  - http://edamontology.org/topic_3673
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3572
  - http://edamontology.org/topic_3407
  tools:
  - Recon8D / Metab8D pipeline
  - ML_function.ipynb
  - preprocessing_example.ipynb
  - recon_mapping (MATLAB/Python scripts)
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1101/2024.08.17.608400v2
  title: Recon8D
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_recon8d_cq
    doi: 10.1101/2024.08.17.608400v2
    title: Recon8D
  dedup_kept_from: coll_recon8d_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2024.08.17.608400v2
  all_source_dois:
  - 10.1101/2024.08.17.608400v2
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# machine-learning-regulatory-prediction

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Train ensemble and regression machine learning models on multiomics feature sets to predict metabolite levels and infer regulatory relationships in a metabolic regulome network. This skill integrates transcriptomics, proteomics, epigenomics, and metabolomics data to rank feature importance and surface novel regulatory associations.

## When to use

You have matched multiomics data (CNV, mutations, DNA methylation, histone PTMs, transcriptomics, miRNA, lncRNA, proteomics, phosphoproteomics) and metabolomics measurements across a cell line panel or cohort, and you want to infer which molecular features (genes, regulatory marks, splice variants, protein modifications) most strongly predict metabolite abundance and thus likely regulate metabolism.

## When NOT to use

- Input data are already aggregated into a single feature matrix; the skill requires independent preprocessing and model training per feature set (omics class) to enable cross-feature-set confidence scoring.
- Metabolomics or multiomics data lack sufficient sample size (< 30 cell lines recommended for robust model training) or are not well-matched across modalities.
- You are seeking to identify dysregulated metabolites in a single disease sample or small cohort without a reference cell line panel for supervised training.

## Inputs

- multiomics feature sets: genomic copy number variation, genomic mutations, DNA methylation, histone post-translational modifications, coding transcripts, RNA splicing, miRNA, lncRNA, proteomics, phosphoproteomics (each as numeric matrix: samples × features)
- matched metabolomics data (samples × metabolites, quantified across CCLE or similar cell line panel)
- metabolic network topology (e.g., Recon3D reactions and metabolite annotations)

## Outputs

- ranked feature importance table (metabolite × feature set × top 20 features with confidence scores 0–8)
- predicted metabolic regulome network (edge list: metabolite–feature pairs with confidence scores and model type annotations)
- model accuracy metrics (Pearson correlation and Bonferroni-corrected p-values per metabolite–feature set pair)
- structured network file (e.g., Metab8D_network.xlsx with cross-feature-set rankings)

## How to apply

Preprocess and normalize each of the nine feature sets independently using z-score normalization and imputation (e.g., KNN for missing values in histone PTM data). Train four model types—random forests, XGBoost, ridge regression, and lasso regression—on each feature set to predict metabolite levels across the cell line panel. For each metabolite-feature set pair, extract feature importance scores and rank the top 20 features. Assign a confidence score (0–8) based on how many independent experimental replicates or cross-validation folds ranked each feature in the top 20. Exclude binary features (e.g., mutation presence/absence) from random forest analysis due to their discrete structure. Validate predicted regulatory edges by checking intersection with known metabolic pathways (e.g., Recon3D) and curated interaction databases.

## Related tools

- **Recon8D / Metab8D pipeline** (Complete machine learning workflow for training random forests, XGBoost, ridge regression, and lasso models; generating feature importances; and producing regulome network output) — https://github.com/sriram-lab/Metab8D
- **ML_function.ipynb** (Jupyter notebook implementing model training, accuracy assessment, and feature importance extraction for each feature set) — https://github.com/sriram-lab/Metab8D
- **preprocessing_example.ipynb** (Example code for z-score normalization and KNN imputation of multiomics features prior to model training) — https://github.com/sriram-lab/Metab8D
- **recon_mapping (MATLAB/Python scripts)** (Extract genes from metabolic reactions and map them to top feature lists for pathway integration and validation) — https://github.com/sriram-lab/Metab8D

## Examples

```
python ML_function.ipynb --input example_datasets/histone_PTM_data.csv --metabolites example_datasets/metabolomics_data.csv --models random_forest xgboost ridge lasso --output Metab8D_network.xlsx
```

## Evaluation signals

- Feature importance ranks are reproducible across cross-validation folds or independent experiments (confidence score ≥ 5 out of 8 indicates robust prediction).
- Model accuracies (Pearson correlation per metabolite) pass Bonferroni-corrected significance threshold (p < 0.05 / number of tests), indicating non-random prediction.
- Top-ranked features for each metabolite show known mechanistic overlap with metabolic pathways in Recon3D or curated interaction databases (e.g., genes encoding enzymes in the same pathway).
- Features with high confidence scores but no previously identified mechanistic link are prioritized for experimental validation, indicating the model surface genuine novel associations.
- Output files (Metab8D_network.xlsx, RF_results correlation tables) are well-formed, contain exactly 2,025 metabolite models (9 feature sets × 225 metabolites), and confidence scores range 0–8 as specified.

## Limitations

- Binary features such as genomic mutations were excluded from random forest models in the Metab8D study due to their discrete structure, which can bias importance scores; alternative encoding or model adjustment may be needed if mutation–metabolite relationships are critical.
- Model predictions are specific to the Cancer Cell Line Encyclopedia (CCLE) panel used for training; generalization to primary tissues, different cell types, or disease contexts requires independent validation.
- Feature importance rankings reflect correlation or predictive power, not causal regulatory relationships; high-confidence features require downstream functional validation (e.g., CRISPR knockdown, metabolic flux assays) to confirm causality.
- Accuracy and confidence scores depend on data quality, sample size, and the degree of multiomics data alignment; mismatched or sparse datasets reduce model robustness.

## Evidence

- [readme] Metab8D utilizes ten feature sets from eight biomolecular classes: 1. genomic copy number variation (CNV), 2. genomic mutations, 3. epigenomic DNA methylation, 4. epigenomic histone PTMs, transcriptomics – 5a. coding transcripts and 5b. RNA splicing, non-coding transcriptomics – 6a. miRNA and 6b. lncRNA, 7. proteomics, and 8. phosphoproteomics: "Metab8D utilizes ten feature sets from eight biomolecular classes: 1. genomic copy number variation (CNV), 2. genomic mutations, 3. epigenomic DNA methylation, 4. epigenomic histone PTMs,"
- [readme] train machine learning (ML) models for predicting relative levels of each metabolite across matched cell lines from the Cancer Cell Line Encyclopedia: "train machine learning (ML) models for predicting relative levels of each metabolite across matched cell lines from the Cancer Cell Line Encyclopedia"
- [readme] Mutations were excluded from random forest model results due to their binary structure: "Mutations were excluded from random forest model results due to their binary structure"
- [readme] Metab8D network generation involves training ML models, assessing their accuracy, and obtaining feature importances thereof. This process is repeated for each individual feature set.: "Metab8D network generation involves training ML models, assessing their accuracy, and obtaining feature importances thereof. This process is repeated for each individual feature set."
- [readme] top 20 features for all 2,025 trained metabolite models (nine feature sets for 225 metabolites), along with their respective confidence scores: "top 20 features for all 2,025 trained metabolite models (nine feature sets for 225 metabolites), along with their respective confidence scores"
- [readme] confidence scores (0 through 8) based on the number of controls (out of 8 experiments) for which each feature appeared in the top 20 most imoprtant features: "confidence scores (0 through 8) based on the number of controls (out of 8 experiments) for which each feature appeared in the top 20 most imoprtant features"
- [other] Apply feature normalization and cross-dataset alignment to ensure compatible feature spaces across omics layers. Train machine learning models to predict metabolic regulatory relationships from multiomics features using supervised learning.: "Apply feature normalization and cross-dataset alignment to ensure compatible feature spaces across omics layers. Train machine learning models to predict metabolic regulatory relationships from"
- [other] Validate predicted regulatory edges against known metabolic pathways and curated interaction databases.: "Validate predicted regulatory edges against known metabolic pathways and curated interaction databases."
- [readme] Example code for preprocessing the original histone PTM data along with examples of z-score normalization and KNN imputation.: "Example code for preprocessing the original histone PTM data along with examples of z-score normalization and KNN imputation."
