---
name: centered-log-ratio-transformation-application
description: Use when apply CLR transformation when working with microbiome or metabolomic relative abundance tables that will be input to multivariate regression or neural network models.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3174
  - http://edamontology.org/topic_3697
  - http://edamontology.org/topic_0091
  tools:
  - MiMeNet
  - ADAM optimizer
  - MelonnPan
  - Elastic Net
  - WGCNA
  - scikit-bio
derived_from:
- doi: 10.1371/journal.pcbi.1009021
  title: MiMeNet
evidence_spans:
- An MLPNN model is composed of multiple fully connected hidden layers composed of perceptrons
- MiMeNet is an integrative MLPNN, which trains models to accurately predict the metabolome based on a microbiome
- MiMeNet was trained using the ADAM optimizer and the mean squared error (MSE) loss function.
- MiMeNet was trained using the ADAM optimizer and the mean squared error (MSE) loss function
- MelonnPan was downloaded from https://github.com/biobakery/melonnpan and executed using the given instructions
- Multivariate Elastic Net models were implemented using ElasticNet and GridSearchCV using 5-fold internal cross-validation
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mimenet
    doi: 10.1371/journal.pcbi.1009021
    title: MiMeNet
  dedup_kept_from: coll_mimenet
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pcbi.1009021
  all_source_dois:
  - 10.1371/journal.pcbi.1009021
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Centered-Log-Ratio Transformation Application

## Summary

Centered-log-ratio (CLR) transformation is a compositional data normalization technique applied to microbiome and metabolomic abundance tables to handle the closure constraint inherent in relative abundance data. It converts counts to log-scale, centered values that preserve compositional relationships while enabling standard statistical and machine learning methods to be applied appropriately.

## When to use

Apply CLR transformation when working with microbiome or metabolomic relative abundance tables that will be input to multivariate regression or neural network models. CLR is specifically indicated when the input features are compositional (sum-to-constant), before downstream prediction modeling or correlation analysis, and particularly when comparing performance across multiple datasets or validating models on external cohorts.

## When NOT to use

- When input data is already transformed (e.g., already log-normalized or z-scored); applying CLR twice will distort relationships.
- When working with non-compositional data (e.g., absolute counts from qPCR, gene expression normalized to housekeeping genes, or already-normalized abundance values); CLR assumes relative abundance with a closure constraint.
- When the input table contains zero or negative values that cannot be meaningfully log-transformed; zero-handling strategies (pseudocounts, zero-inflated models) must be applied first.

## Inputs

- Microbiome relative abundance table (samples × microbial features, CSV format)
- Metabolomic relative abundance table (samples × metabolite features, CSV format)
- Count matrix or abundance matrix with compositional structure (rows = samples, columns = features)

## Outputs

- CLR-transformed microbiome abundance table (samples × microbial features, log-scale centered values)
- CLR-transformed metabolomic abundance table (samples × metabolite features, log-scale centered values)
- Transformed feature matrix suitable for neural network or regression model training

## How to apply

CLR transformation is performed as a preprocessing step after loading microbiome and metabolomic count matrices but before feature filtering and model training. For each sample, compute the geometric mean of all features (across both samples and features), then divide each feature abundance by this geometric mean and take the natural logarithm. In MiMeNet's workflow, CLR is applied to metabolomic features (specified via the `-metab_norm CLR` parameter) while microbiome features may use relative abundance or CLR depending on the analysis. Apply identical CLR transformations to both training and external validation datasets using the same preprocessing pipeline to ensure consistency. The transformation is applied after removing low-abundance features (those present in <10% of samples) to avoid division-by-zero or log(0) errors. This normalization enables neural network models to learn relationships between microbial and metabolomic features without bias from the compositional constraint.

## Related tools

- **MiMeNet** (Neural network framework that accepts CLR-transformed microbiome and metabolomic data as preprocessed inputs for predicting metabolomic profiles) — https://github.com/YDaiLab/MiMeNet
- **scikit-bio** (Python library providing compositional data transformation utilities including CLR normalization)
- **MelonnPan** (Baseline elastic net regression method for metabolite prediction that also accepts preprocessed abundance data (with or without CLR)) — https://github.com/biobakery/melonnpan

## Examples

```
python MiMeNet_train.py -micro data/IBD/microbiome_PRISM.csv -metab data/IBD/metabolome_PRISM.csv -external_micro data/IBD/microbiome_external.csv -external_metab data/IBD/metabolome_external.csv -micro_norm None -metab_norm CLR -net_params results/IBD/network_parameters.txt
```

## Evaluation signals

- Verify that transformed values are centered around zero (mean ≈ 0 across all features in each sample) and span negative to positive log-scale values (not bounded [0, 1]).
- Confirm that no NaN, Inf, or undefined values appear in the transformed table after log transformation (indicates unhandled zeros in the original data).
- Check that downstream model performance (mean Spearman correlation coefficient for metabolite prediction) on external validation data is consistent with or improves over untransformed baselines, demonstrating that the compositional preprocessing was appropriate.
- Ensure that the same CLR transformation pipeline (geometric mean calculation, log operation, feature filtering order) is applied identically to both training and external validation datasets to avoid batch effects.
- Validate that well-predicted metabolites identified post-model training (using the 95th percentile correlation threshold) show meaningful biological associations by comparing to known microbe-metabolite interactions in the literature or functional databases.

## Limitations

- CLR transformation is sensitive to zero values in the original data; features with zero abundance in any sample require pseudocount addition or zero-inflated handling before transformation, and the choice of pseudocount strategy can affect downstream inference.
- The geometric mean calculation in CLR can be unstable when applied to sparse data (many zero values), leading to extreme log-ratio values that may dominate the learned model; aggressive feature filtering (e.g., presence in >10% of samples) is recommended to mitigate this.
- CLR transformation loses information about absolute abundance (converts to relative ratios only); if absolute quantification is important for mechanistic interpretation, alternative normalization strategies should be considered.
- Not all metabolites may be associated with microbes, resulting in lower prediction correlations and lower overall mean correlation across all metabolites even after CLR preprocessing, potentially masking true relationships in metabolites that are microbiome-independent.

## Evidence

- [other] Load and preprocess IBD (PRISM) microbiome (201 features) and metabolome (8848 features) data, applying centered log-ratio transformation and removing features present in <10% of samples.: "applying centered log-ratio transformation and removing features present in <10% of samples"
- [other] Load and preprocess IBD (External) microbiome and metabolome data using identical transformation and filtering procedures.: "Load and preprocess IBD (External) microbiome and metabolome data using identical transformation and filtering procedures"
- [readme] Transform the microbial features into relative abundance (RA) or center log-ratio (CLR). If the data is already transformed, apply 'None' to skip transformation.: "Transform the microbial features into relative abundance (RA) or center log-ratio (CLR). If the data is already transformed, apply 'None' to skip transformation."
- [readme] Transform the metabolomic features into relative abundance (RA) or center log-ratio (CLR). If the data is already transformed, apply 'None' to skip transformation.: "Transform the metabolomic features into relative abundance (RA) or center log-ratio (CLR). If the data is already transformed, apply 'None' to skip transformation."
- [readme] MiMeNet will perform a compositional transformation to relative abundance or centered log-ratio and filter low abundant microbial: "MiMeNet will perform a compositional transformation to relative abundance or centered log-ratio and filter low abundant microbial"
