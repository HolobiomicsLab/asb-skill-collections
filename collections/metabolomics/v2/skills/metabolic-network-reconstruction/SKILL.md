---
name: metabolic-network-reconstruction
description: Use when you have matched multiomics data (genomics, epigenomics, transcriptomics, proteomics, metabolomics) across a cohort of cell lines or samples and want to infer which molecular features (genes, transcripts, proteins, methylation sites) regulate metabolite abundance.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3660
  edam_topics:
  - http://edamontology.org/topic_2275
  - http://edamontology.org/topic_0199
  - http://edamontology.org/topic_3517
  tools:
  - Metab8D
  - Recon8D / Recon3D
  - scikit-learn RandomForest / XGBoost / Ridge / Lasso
  - Cancer Cell Line Encyclopedia (CCLE)
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolic-network-reconstruction

## Summary

Reconstruct a multiomic metabolic regulatory network by training machine learning models on aligned multiomics features (CNV, mutations, epigenomics, transcriptomics, proteomics) to predict metabolite levels and infer regulatory relationships across a reference cell line panel. This skill integrates diverse biomolecular layers to propose systems-level metabolic regulation mechanisms.

## When to use

You have matched multiomics data (genomics, epigenomics, transcriptomics, proteomics, metabolomics) across a cohort of cell lines or samples and want to infer which molecular features (genes, transcripts, proteins, methylation sites) regulate metabolite abundance. Use this skill when you seek to move beyond single-layer correlation analysis to a predictive, feature-importance-ranked regulome.

## When NOT to use

- Input is single-layer data (e.g., transcriptomics only); this skill requires matched multiomics across ≥3 biomolecular classes.
- Metabolomics or multiomics samples are not paired or aligned across individuals/cell lines; model training requires consistent feature and metabolite coverage across the cohort.
- Metabolite or feature data are already highly sparse (>80% zeros/missing) after imputation; random forest and regression models require sufficient variance and overlap to learn regulatory signals.

## Inputs

- Multiomics feature matrix: genomic copy number variation (CNV) table
- Genomic mutation calls (binary or VCF format)
- Epigenomic DNA methylation matrix
- Histone post-translational modification (PTM) abundance table
- Transcriptomics: coding transcript expression and RNA splicing ratios
- Non-coding transcriptomics: miRNA and lncRNA expression
- Proteomics abundance matrix
- Phosphoproteomics abundance matrix
- Metabolomics: metabolite abundance or relative level matrix
- Cell line sample metadata linking omics layers
- Metabolic network topology (e.g., Recon3D reactions and metabolite–gene associations)

## Outputs

- Regulome network edge list: metabolite × feature pairs with confidence scores (0–8)
- Top 20 features per metabolite per feature set (e.g., Metab8D_network.xlsx format)
- Feature importance scores (e.g., Gini impurity, SHAP, or permutation importance)
- Model accuracy metrics (Pearson correlation, p-values) per metabolite per feature set
- Validated regulatory annotations mapped to metabolic pathways and reaction genes

## How to apply

Preprocess and normalize each of the ten feature sets (CNV, mutations, DNA methylation, histone PTMs, coding & non-coding transcripts, miRNA, lncRNA, proteomics, phosphoproteomics) separately, ensuring z-score normalization and handling missing values via KNN imputation. Train random forest, XGBoost, ridge regression, and lasso regression models independently for each metabolite using each feature set as predictors. Extract feature importance scores from all models and aggregate them across replicates or cross-validation folds. For each metabolite–feature set pair, rank the top 20 most important features and assign a confidence score (0–8) based on how many control experiments included that feature in their top 20 rankings. Validate predicted regulatory edges by mapping features to genes involved in reactions linked to the target metabolites, then cross-reference against known pathway databases and curated interaction resources. Export the final regulome as a structured edge list (metabolite–feature pairs) with confidence scores and feature importances.

## Related tools

- **Metab8D** (End-to-end ML workflow for training feature importance models across multiomics layers and generating the metabolic regulome network) — https://github.com/sriram-lab/Metab8D
- **Recon8D / Recon3D** (Source metabolic network topology for mapping predicted features to metabolite-linked genes and reactions for validation) — https://github.com/sriram-lab/Recon8D
- **scikit-learn RandomForest / XGBoost / Ridge / Lasso** (Machine learning models for training per-metabolite predictors and extracting feature importances)
- **Cancer Cell Line Encyclopedia (CCLE)** (Reference multiomics cohort (transcriptomics, proteomics, metabolomics) used to train and validate models)

## Evaluation signals

- Model accuracy (Pearson correlation and Bonferroni-corrected p-values) is statistically significant (p < 0.05 after multiple-testing correction) for the majority of metabolite models per feature set.
- Top 20 features per metabolite include known genes or proteins involved in relevant metabolic reactions or pathways (validated against Recon3D and curated databases).
- Confidence scores (0–8) are reproducible across independent control experiments; features appearing consistently in top 20 across replicates receive high confidence.
- Predicted regulatory edges show biological coherence: e.g., transcription factors or kinases appear as top features for metabolites in their cognate pathways; phosphoproteomics features link to proteins with known metabolic roles.
- Regulome network exhibits expected scale-free or modular topology consistent with known metabolic regulation (e.g., hub metabolites like ATP or acetyl-CoA show broad regulatory connectivity; pathway-specific metabolites show local clustering).

## Limitations

- Mutations were excluded from random forest results due to their binary structure, reducing coverage of genetic regulation; alternative mutation encoding or separate binary classifiers may be needed to include genetic effects.
- Feature importance scores reflect correlation and predictive power in the training cohort (CCLE cell lines); transferability to other tissues, organisms, or disease contexts is not validated and should be treated with caution.
- KNN imputation of missing metabolomics or omics values can introduce bias if missingness is not random; heavily imputed features may produce spurious regulatory predictions.
- Top 20 feature lists per metabolite are a heuristic threshold; the true number of regulatory inputs varies and may exceed or fall below 20 for specific metabolites.
- Confidence scoring (0–8 based on appearance in top 20 across controls) is sensitive to model hyperparameter tuning and feature set composition; no formal FDR control is applied, and discovered edges should be validated experimentally.

## Evidence

- [readme] Metab8D utilizes ten feature sets from eight biomolecular classes: 1. genomic copy number variation (CNV), 2. genomic mutations, 3. epigenomic DNA methylation, 4. epigenomic histone PTMs, transcriptomics – 5a. coding transcripts and 5b. RNA splicing, non-coding transcriptomics – 6a. miRNA and 6b. lncRNA, 7. proteomics, and 8. phosphoproteomics: "Metab8D utilizes ten feature sets from eight biomolecular classes: 1. genomic copy number variation (CNV), 2. genomic mutations, 3. epigenomic DNA methylation, 4. epigenomic histone PTMs,"
- [readme] train machine learning (ML) models for predicting relative levels of each metabolite across matched cell lines from the Cancer Cell Line Encyclopedia, thereby inferring a multiomic metabolic regulatory network: "train machine learning (ML) models for predicting relative levels of each metabolite across matched cell lines from the Cancer Cell Line Encyclopedia, thereby inferring a multiomic metabolic"
- [readme] Mutations were excluded from random forest model results due to their binary structure: "Mutations were excluded from random forest model results due to their binary structure"
- [readme] Metab8D network generation involves training ML models, assessing their accuracy, and obtaining feature importances thereof. This process is repeated for each individual feature set.: "Metab8D network generation involves training ML models, assessing their accuracy, and obtaining feature importances thereof. This process is repeated for each individual feature set."
- [readme] The resultant proposed regulome network can be found in the Metab8D_network.xlsx file, where the top 20 features for all 2,025 trained metabolite models (nine feature sets for 225 metabolites), along with their respective confidence scores, may be found.: "The resultant proposed regulome network can be found in the Metab8D_network.xlsx file, where the top 20 features for all 2,025 trained metabolite models (nine feature sets for 225 metabolites), along"
- [readme] confidence scores (0 through 8) based on the number of controls (out of 8 experiments) for which each feature appeared in the top 20 most imoprtant features: "confidence scores (0 through 8) based on the number of controls (out of 8 experiments) for which each feature appeared in the top 20 most imoprtant features"
- [other] Apply feature normalization and cross-dataset alignment to ensure compatible feature spaces across omics layers: "Apply feature normalization and cross-dataset alignment to ensure compatible feature spaces across omics layers"
- [other] Validate predicted regulatory edges against known metabolic pathways and curated interaction databases: "Validate predicted regulatory edges against known metabolic pathways and curated interaction databases"
