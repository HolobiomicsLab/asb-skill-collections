---
name: multiomics-data-integration
description: Use when when you have matched multiomics measurements across the same samples or cell lines (transcriptomics, proteomics, metabolomics, epigenomics, etc.) and need to train predictive models that learn regulatory relationships across biomolecular classes.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_3391
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_0625
  tools:
  - ML_function.ipynb
  - preprocessing_example.ipynb
  - recon_mapping
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

# multiomics-data-integration

## Summary

Integration of ten feature sets spanning eight biomolecular classes (genomic CNV, mutations, DNA methylation, histone PTMs, coding/non-coding transcriptomics, proteomics, and phosphoproteomics) into unified feature spaces for machine learning prediction of metabolic regulation. This skill enables construction of systems-level metabolic regulome networks by aligning and normalizing heterogeneous omics layers.

## When to use

When you have matched multiomics measurements across the same samples or cell lines (transcriptomics, proteomics, metabolomics, epigenomics, etc.) and need to train predictive models that learn regulatory relationships across biomolecular classes. Specifically applicable when your goal is to infer which molecular features at different omics levels best predict variation in a downstream phenotype (e.g., metabolite abundance) and you want confidence scores reflecting consistency across independent experiments or feature sets.

## When NOT to use

- Input datasets are unpaired or unmapped across omics layers (e.g., different samples in transcriptomics vs. proteomics).
- Only one omics layer is available; multiomics integration requires at least two distinct biomolecular classes.
- Target phenotype is binary or categorical without clear continuous variation; models trained here assume continuous phenotype prediction.

## Inputs

- multiomics feature matrices from eight biomolecular classes (genomic CNV, mutations, DNA methylation, histone PTMs, coding transcripts, RNA splicing, miRNA, lncRNA, proteomics, phosphoproteomics)
- matched phenotype measurements (e.g., metabolite abundance across cell lines)
- metadata linking samples across omics datasets
- optional: curated interaction databases or pathway annotations for validation

## Outputs

- normalized, aligned multiomics feature tables in compatible feature space
- trained machine learning models (one per feature set) with feature importance rankings
- confidence scores (0–8) for each feature based on cross-experiment recovery
- regulome network graph (edge list or adjacency format) linking omics features to predicted phenotypes
- model accuracy metrics and Pearson correlation coefficients with Bonferroni-corrected p-values per feature set

## How to apply

Load preprocessed datasets from each of the eight biomolecular classes into a common computational environment. Apply feature normalization (e.g., z-score normalization as shown in preprocessing_example.ipynb) and cross-dataset alignment to ensure compatible feature spaces across omics layers. Handle missing values via imputation methods (e.g., KNN imputation for omics data). Train machine learning models (random forests, XGBoost, ridge regression, lasso) independently on each feature set to predict the target phenotype (e.g., metabolite levels), computing feature importance scores and model accuracies for each. Assign confidence scores (0–8 scale) based on how many independent experiments or feature sets recovered each feature in their top-ranked predictions. Integrate high-confidence features with known pathway topology (via database mapping) to construct the final regulome network, prioritizing features with high confidence scores and no previously identified mechanistic relationship for downstream validation.

## Related tools

- **ML_function.ipynb** (Implements random forests, XGBoost, ridge regression, and lasso regression for feature importance extraction across independent feature sets) — https://github.com/sriram-lab/Metab8D
- **preprocessing_example.ipynb** (Demonstrates z-score normalization and KNN imputation for cross-omics feature alignment) — https://github.com/sriram-lab/Metab8D
- **recon_mapping** (Maps predicted features to metabolic network reactions and translates gene identifiers for validation against curated pathways) — https://github.com/sriram-lab/Metab8D

## Examples

```
python ML_function.ipynb  # Train ML models on each of nine feature sets; outputs feature importances and Pearson correlations (RF_results/) with confidence scores aggregated into Metab8D_network.xlsx
```

## Evaluation signals

- Feature normalization statistics (e.g., mean ≈ 0, std ≈ 1 for z-scored features) confirm successful cross-omics alignment.
- Model accuracy metrics (Pearson r, p-values) show statistical significance (Bonferroni-corrected p < 0.05) for each feature set's predictive power.
- Confidence scores (0–8) exhibit non-uniform distribution with a subset of features recovered across multiple independent experiments, indicating robust regulatory signals.
- Regulome network exhibits expected biological structure: features linked to metabolites are enriched in relevant pathways (validated against Recon3D or other metabolic databases).
- Features with high confidence and no prior mechanistic annotation are identified and flagged for experimental validation, confirming novelty.

## Limitations

- Mutations were excluded from random forest model results due to their binary structure, limiting full integration of genomic variation.
- The approach is dependent on the availability of matched, high-quality multiomics measurements; missing or misaligned data may degrade confidence scores.
- Feature importance rankings reflect only associations captured by the chosen machine learning models; causality is not inferred and requires independent validation.
- Confidence scoring relies on recovery consistency across a fixed set of experiments; generalization to independent cohorts requires external validation.

## Evidence

- [readme] Metab8D utilizes ten feature sets from eight biomolecular classes: 1. genomic copy number variation (CNV), 2. genomic mutations, 3. epigenomic DNA methylation, 4. epigenomic histone PTMs, transcriptomics – 5a. coding transcripts and 5b. RNA splicing, non-coding transcriptomics – 6a. miRNA and 6b. lncRNA, 7. proteomics, and 8. phosphoproteomics: "Metab8D utilizes ten feature sets from eight biomolecular classes: 1. genomic copy number variation (CNV), 2. genomic mutations, 3. epigenomic DNA methylation, 4. epigenomic histone PTMs,"
- [other] Apply feature normalization and cross-dataset alignment to ensure compatible feature spaces across omics layers.: "Apply feature normalization and cross-dataset alignment to ensure compatible feature spaces across omics layers."
- [readme] An example of model generation is provided at the bottom of the ML_function.ipynb file using the histone PTM data. A requirements.txt file is provided, specifying all necessary packages for running this code.: "An example of model generation is provided at the bottom of the ML_function.ipynb file using the histone PTM data."
- [readme] The resultant proposed regulome network can be found in the Metab8D_network.xlsx file, where the top 20 features for all 2,025 trained metabolite models (nine feature sets for 225 metabolites), along with their respective confidence scores, may be found.: "The resultant proposed regulome network can be found in the Metab8D_network.xlsx file, where the top 20 features for all 2,025 trained metabolite models (nine feature sets for 225 metabolites), along"
- [readme] confidence scores (0 through 8) based on the number of controls (out of 8 experiments) for which each feature appeared in the top 20 most important features.: "confidence scores (0 through 8) based on the number of controls (out of 8 experiments) for which each feature appeared in the top 20 most important features."
- [readme] Example code for preprocessing the original histone PTM data along with examples of z-score normalization and KNN imputation.: "Example code for preprocessing the original histone PTM data along with examples of z-score normalization and KNN imputation."
