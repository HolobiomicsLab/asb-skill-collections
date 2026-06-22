---
name: cross-omics-feature-alignment
description: Use when you have preprocessed multiomics datasets from distinct biomolecular classes (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3673
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3308
  tools:
  - ML_function.ipynb
  - preprocessing_example.ipynb
  - scikit-learn
  - XGBoost
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
---

# cross-omics-feature-alignment

## Summary

Normalize and align feature spaces across heterogeneous omics layers (transcriptomics, proteomics, metabolomics, epigenomics) to enable joint machine learning modeling of metabolic regulation. This skill ensures that features from different biomolecular classes are comparable in scale and distribution before multi-omics integration.

## When to use

You have preprocessed multiomics datasets from distinct biomolecular classes (e.g., CNV, mutations, DNA methylation, histone PTMs, coding/non-coding transcriptomics, proteomics, phosphoproteomics) and need to train unified machine learning models to predict metabolite levels or regulatory relationships. Alignment is required when features from different omics layers have incompatible scales, distributions, or missing-value patterns that would bias downstream model training.

## When NOT to use

- Input datasets are already harmonized or from a single omics platform (e.g., transcriptomics only); cross-omics alignment is unnecessary.
- Features have been manually curated or pre-filtered to remove platform-specific noise; re-alignment may reintroduce batch effects.
- Sample sizes are very small (<10 matched samples); KNN imputation and z-score normalization may amplify noise instead of reducing it.

## Inputs

- Raw multiomics datasets from eight biomolecular classes: genomic CNV, genomic mutations, DNA methylation, histone PTMs, coding transcripts, RNA splicing, miRNA, lncRNA, proteomics, phosphoproteomics
- Matched sample labels (e.g., Cancer Cell Line Encyclopedia cell line identifiers)
- Target outcome matrix (e.g., metabolite abundances for 225 metabolites across matched cell lines)

## Outputs

- Aligned feature matrix (samples × features) with z-score normalized values
- Imputed feature matrix with missing values replaced (KNN method)
- Per-omics-layer summary statistics (mean, std deviation) confirming alignment
- Feature importance scores and confidence scores (0–8 range based on control replicates)
- Top 20 features per metabolite per feature set with associated confidence annotations

## How to apply

Apply feature normalization (e.g., z-score standardization) and missing-value imputation (e.g., KNN imputation) separately within each omics feature set to stabilize variance and remove bias introduced by measurement platform differences. Then verify cross-dataset alignment by checking that normalized features across all omics layers share compatible mean (≈0) and standard deviation (≈1) distributions. The rationale is that machine learning models (random forests, XGBoost, ridge regression, lasso) are sensitive to feature scale and missingness; misaligned features inflate weights toward high-variance layers or sparse features, reducing interpretability of true regulatory relationships. After alignment, train models on the pooled, normalized feature matrix to extract feature importances and confidence scores (e.g., the number of experimental replicates, out of 8 controls, in which each feature appeared in the top 20 most important).

## Related tools

- **ML_function.ipynb** (Implements feature normalization, imputation, and machine learning model training (random forests, XGBoost, ridge, lasso) on aligned multiomics features) — https://github.com/sriram-lab/Metab8D
- **preprocessing_example.ipynb** (Demonstrates z-score normalization and KNN imputation workflows applied to histone PTM and metabolomics data as a template for cross-omics alignment) — https://github.com/sriram-lab/Metab8D
- **scikit-learn** (Provides preprocessing utilities (StandardScaler, KNNImputer) and machine learning model implementations (RandomForestRegressor, Ridge, Lasso))
- **XGBoost** (Gradient boosting model trained on aligned feature matrices for metabolite prediction)

## Examples

```
from sklearn.preprocessing import StandardScaler; from sklearn.impute import KNNImputer; import pandas as pd; df_aligned = pd.concat([StandardScaler().fit_transform(df_omics_layer) for df_omics_layer in [df_cnv, df_methylation, df_histone_ptm, df_transcripts, df_proteomics]], axis=1); imputer = KNNImputer(n_neighbors=5); df_imputed = pd.DataFrame(imputer.fit_transform(df_aligned))
```

## Evaluation signals

- Normalized features from all omics layers have mean ≈ 0 and standard deviation ≈ 1 across the full sample population.
- Cross-layer Pearson correlations between randomly selected features from different omics classes show no systematic bias toward any single platform.
- Missing-value imputation completeness: 100% of features have no remaining NaN values after KNN imputation; imputed values lie within ±3σ of the mean for their respective feature set.
- Machine learning model cross-validation accuracy (R² or Pearson correlation) is stable and reproducible across multiple random seeds, indicating alignment did not introduce artificial structure.
- Feature importance scores are distributed across all nine feature sets (excluding mutations) rather than concentrated in one or two omics layers; dominance by a single layer suggests misalignment.
- Top 20 features per metabolite show confidence scores (0–8) that reflect reproducibility across control replicates; features appearing in <2 controls should be treated as low-confidence.

## Limitations

- Binary or categorical features (e.g., genomic mutations encoded as 0/1) may not align well with continuous z-score normalization; Metab8D excluded mutations from random forest results due to this structural incompatibility.
- KNN imputation assumes missing values are missing at random (MCAR); if missingness is systematic to a particular omics layer or cell line, imputation may introduce bias.
- Alignment is sample-wise (across cell lines); features are normalized within each omics class separately, so cross-layer feature correlation structure is not explicitly constrained and may retain platform-specific biases.
- Confidence scores (0–8) depend on the number of experimental controls; datasets with fewer replicates will have lower maximum confidence and reduced ability to distinguish true signal from noise.

## Evidence

- [other] Apply feature normalization and cross-dataset alignment to ensure compatible feature spaces across omics layers.: "Apply feature normalization and cross-dataset alignment to ensure compatible feature spaces across omics layers."
- [readme] Metab8D utilizes ten feature sets from eight biomolecular classes: 1. genomic copy number variation (CNV), 2. genomic mutations, 3. epigenomic DNA methylation, 4. epigenomic histone PTMs, transcriptomics – 5a. coding transcripts and 5b. RNA splicing, non-coding transcriptomics – 6a. miRNA and 6b. lncRNA, 7. proteomics, and 8. phosphoproteomics to train machine learning (ML) models: "Metab8D utilizes ten feature sets from eight biomolecular classes: 1. genomic copy number variation (CNV), 2. genomic mutations, 3. epigenomic DNA methylation, 4. epigenomic histone PTMs,"
- [readme] Example code for preprocessing the original histone PTM data along with examples of z-score normalization and KNN imputation.: "Example code for preprocessing the original histone PTM data along with examples of z-score normalization and KNN imputation."
- [readme] Mutations were excluded from random forest model results due to their binary structure: "Mutations were excluded from random forest model results due to their binary structure (as discussed in the associated Metab8D manuscript referenced here)."
- [readme] The top 20 features for all 2,025 trained metabolite models (nine feature sets for 225 metabolites), along with their respective confidence scores, may be found.: "The top 20 features for all 2,025 trained metabolite models (nine feature sets for 225 metabolites), along with their respective confidence scores, may be found."
