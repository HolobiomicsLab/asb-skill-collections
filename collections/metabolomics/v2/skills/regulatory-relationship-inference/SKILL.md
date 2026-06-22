---
name: regulatory-relationship-inference
description: Use when you have matched multiomics measurements (CNV, mutations, DNA methylation, histone PTMs, coding/noncoding transcripts, miRNA, lncRNA, proteomics, phosphoproteomics) across a cohort of cell lines or samples and want to identify which upstream omics features predict metabolite abundance.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0199
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0602
  tools:
  - Random Forest (scikit-learn)
  - XGBoost
  - Ridge Regression
  - Lasso Regression
  - ML_function.ipynb
  - preprocessing_example.ipynb
  - recon_mapping (MATLAB/Python scripts)
  - Recon3D
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

# regulatory-relationship-inference

## Summary

Infer metabolic regulatory relationships by training machine learning models on aligned multiomics feature sets (genomic, epigenomic, transcriptomic, proteomic) to predict metabolite levels and extract feature importance scores as confidence-ranked regulatory edges. This skill bridges omics layers to construct systems-level metabolic regulome networks suitable for hypothesis generation and mechanistic validation.

## When to use

You have matched multiomics measurements (CNV, mutations, DNA methylation, histone PTMs, coding/noncoding transcripts, miRNA, lncRNA, proteomics, phosphoproteomics) across a cohort of cell lines or samples and want to identify which upstream omics features best predict metabolite abundance. Use this skill when you need to propose and rank putative regulatory mechanisms linking molecular features to metabolic phenotypes, especially when mechanistic relationships are unknown and require prioritization for downstream validation.

## When NOT to use

- Input metabolomics or feature data are not aligned across samples (different sample sets or row orderings for metabolites and features); preprocessing must restore sample-level correspondence first.
- You have fewer than ~30 samples or cell lines; statistical power for feature importance ranking and multiple-testing correction becomes unreliable with very small cohorts.
- Your goal is to identify global metabolic pathways rather than rank individual feature–metabolite regulatory links; use pathway enrichment or flux balance analysis instead.

## Inputs

- Aligned multiomics feature matrix: genomic CNV (continuous)
- Genomic mutations (binary)
- Epigenomic DNA methylation (continuous, 0–1)
- Epigenomic histone PTM abundance (continuous)
- Transcriptomics: coding transcript expression (continuous, log-normalized)
- Transcriptomics: RNA splicing ratios (continuous, 0–1)
- Noncoding transcriptomics: miRNA abundance (continuous)
- Noncoding transcriptomics: lncRNA abundance (continuous)
- Proteomics: protein abundance (continuous, log-normalized)
- Phosphoproteomics: phosphosite abundance (continuous)
- Metabolomics measurements: metabolite abundance per sample (continuous, aligned to feature matrix rows)
- Metadata: sample identifiers, cell line annotations, batch information

## Outputs

- Metabolic regulome network edge list (TSV, JSON, GML, or Excel): metabolite ID, feature ID, feature set class, feature importance score, confidence score (0–8), regulatory annotation
- Top 20 features per metabolite per feature set (structured table with feature rank, importance, p-value, Bonferroni-corrected significance)
- Model performance metrics per metabolite–feature-set pair: Pearson correlation, R², accuracy or RMSE, significance threshold status
- Validated regulatory edges: subset of edge list after cross-reference with curated metabolic pathway and protein–metabolite databases

## How to apply

Preprocess and normalize each of the ten feature sets (CNV, mutations, DNA methylation, histone PTMs, coding transcripts, RNA splicing, miRNA, lncRNA, proteomics, phosphoproteomics) independently using z-score normalization and KNN imputation to handle missing values. Train parallel machine learning models (random forests, XGBoost, ridge regression, lasso regression) for each metabolite using each feature set as input, stratified by omics class to avoid confounding. Extract feature importance scores from each trained model and retain the top 20 features per metabolite–feature-set pair. Assign confidence scores (0–8) to each feature based on the number of control experiments (maximum 8) in which it appeared in the top 20, weighted toward features with reproducible, high importance across replicates. Validate high-confidence predicted regulatory edges (confidence ≥ 6) against known metabolic pathways and curated protein–metabolite interaction databases before export. Use Bonferroni-corrected P-values (p < 0.05) to filter model correlations by significance.

## Related tools

- **Random Forest (scikit-learn)** (Train feature importance–based ML models for metabolite prediction across each omics feature set)
- **XGBoost** (Alternative gradient boosting model for metabolite prediction and feature importance ranking)
- **Ridge Regression** (Regularized linear model for metabolite prediction to assess linear feature–metabolite relationships)
- **Lasso Regression** (Sparse linear model for metabolite prediction with automated feature selection)
- **ML_function.ipynb** (Reference implementation: Python Jupyter notebook containing model training, accuracy assessment, and feature importance extraction pipeline for all four ML algorithms) — https://github.com/sriram-lab/Metab8D
- **preprocessing_example.ipynb** (Reference implementation for z-score normalization and KNN imputation of multiomics feature sets) — https://github.com/sriram-lab/Metab8D
- **recon_mapping (MATLAB/Python scripts)** (Extract genes from Recon3D metabolic reactions and map predicted regulatory features to pathway context) — https://github.com/sriram-lab/Metab8D
- **Recon3D** (Reference metabolic network for validation of predicted metabolite–feature regulatory relationships) — https://github.com/sriram-lab/Recon8D

## Evaluation signals

- Feature importance scores are non-negative, ranked in descending order within each metabolite–feature-set model, and tied to model performance metrics (correlation p-value, R²) that meet Bonferroni-corrected significance threshold (p < 0.05).
- Confidence scores (0–8) are consistent with reproducibility: features ranked in top 20 across multiple random forest seeds / cross-validation folds receive higher confidence; confidence distribution is not uniform (should show clustering near 0, 4, or 8).
- Top-ranked edges validated against curated databases show prior mechanistic support (e.g., feature encodes enzyme, transporter, or allosteric regulator of top-ranked metabolite); unexpected high-confidence edges without known mechanism are flagged as hypothesis-generating candidates.
- Model predictions on independent validation cohorts (e.g., external cell line panel) show similar feature rankings and confidence scores for the same metabolites, indicating generalization.
- Output edge list is valid structured format (JSON parseable, TSV tab-delimited with no embedded tabs in values, Excel with consistent schema per sheet); all metabolite and feature IDs are resolvable to reference databases (BiggID for metabolites, gene symbols / transcript IDs for features).

## Limitations

- Binary features (genomic mutations) are excluded from random forest results due to incompatibility with feature importance ranking; consider alternative encoding (e.g., mutation burden per pathway) or separate handling.
- Feature importance scores reflect correlation with metabolite levels in the training cohort (Cancer Cell Line Encyclopedia); causality is not inferred and must be validated experimentally or in independent datasets.
- Confidence scores are computed from a fixed number of control experiments (≤8); cohorts with fewer replicates or controls will have reduced confidence score resolution.
- Cross-omics feature coupling (e.g., high CNV and high transcript abundance for the same gene) can inflate importance for upstream features and obscure direct regulatory mechanisms; validation against mechanistic databases is essential.
- Missing data imputation (KNN) may bias importance scores for sparse features; comparison against models trained on complete-case subsets recommended for sensitivity analysis.

## Evidence

- [readme] Metab8D utilizes ten feature sets from eight biomolecular classes: 1. genomic copy number variation (CNV), 2. genomic mutations, 3. epigenomic DNA methylation, 4. epigenomic histone PTMs, transcriptomics – 5a. coding transcripts and 5b. RNA splicing, non-coding transcriptomics – 6a. miRNA and 6b. lncRNA, 7. proteomics, and 8. phosphoproteomics to train machine learning (ML) models for predicting relative levels of each metabolite: "Metab8D utilizes ten feature sets from eight biomolecular classes: 1. genomic copy number variation (CNV), 2. genomic mutations, 3. epigenomic DNA methylation, 4. epigenomic histone PTMs,"
- [readme] Mutations were excluded from random forest model results due to their binary structure: "Mutations were excluded from random forest model results due to their binary structure"
- [readme] ML_function.ipynb file, Metab8D network generation involves training ML models, assessing their accuracy, and obtaining feature importances thereof. This process is repeated for each individual feature set.: "Metab8D network generation involves training ML models, assessing their accuracy, and obtaining feature importances thereof. This process is repeated for each individual feature set."
- [readme] The top 20 features for all 2,025 trained metabolite models (nine feature sets for 225 metabolites), along with their respective confidence scores, may be found. Features with high confidence scores and no previously identified mechanistic relationship should be prioritized for further study.: "The top 20 features for all 2,025 trained metabolite models (nine feature sets for 225 metabolites), along with their respective confidence scores, may be found."
- [readme] Confidence scores (0 through 8) based on the number of controls (out of 8 experiments) for which each feature appeared in the top 20 most important features.: "Confidence scores (0 through 8) based on the number of controls (out of 8 experiments) for which each feature appeared in the top 20"
- [readme] Example code for preprocessing the original histone PTM data along with examples of z-score normalization and KNN imputation.: "Example code for preprocessing the original histone PTM data along with examples of z-score normalization and KNN imputation."
- [readme] RF_results: Pearson's correlations and P values for all metabolite models from each of nine feature sets. Significance is determined by Bonferroni-corrected P value.: "RF_results: Pearson's correlations and P values for all metabolite models from each of nine feature sets. Significance is determined by Bonferroni-corrected P value."
- [other] Train machine learning models to predict metabolic regulatory relationships from multiomics features using supervised learning: "Train machine learning models to predict metabolic regulatory relationships from multiomics features using supervised learning"
