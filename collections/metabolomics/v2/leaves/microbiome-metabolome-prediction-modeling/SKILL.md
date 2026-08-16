---
name: microbiome-metabolome-prediction-modeling
description: Use when you have paired microbiome (16S rRNA, metagenomic) and metabolomic
  (LC-MS, GC-MS) abundance tables from the same biosamples, and you want to predict
  which metabolites are recoverable from microbial composition alone and identify
  groups of microbes and metabolites with correlated.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3174
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0092
  tools:
  - ADAM optimizer
  - scikit-learn (Python)
  - MiMeNet
  - MelonnPan
  - Random Forest
  - Canonical Correlation Analysis (CCA)
  - scikit-learn
  - TensorFlow
  - scikit-bio
  techniques:
  - LC-MS
  - GC-MS
  license_tier: open
derived_from:
- doi: 10.1371/journal.pcbi.1009021
  title: MiMeNet
evidence_spans:
- MiMeNet was trained using the ADAM optimizer and the mean squared error (MSE) loss
  function.
- MiMeNet was trained using the ADAM optimizer and the mean squared error (MSE) loss
  function
- these models can predict the entire set of metabolites at once, and all models were
  evaluated using 10 iterations of 10-fold cross-validation. Random Forest, multivariate
  Elastic Net, and Canonical
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

# microbiome-metabolome-prediction-modeling

## Summary

Train and evaluate neural network models to predict metabolite abundances from microbiome composition data, with cross-validated performance assessment and identification of well-predicted metabolites above a background correlation threshold. This skill enables data-driven discovery of microbe-metabolite interaction structures without mechanistic prior knowledge.

## When to use

You have paired microbiome (16S rRNA, metagenomic) and metabolomic (LC-MS, GC-MS) abundance tables from the same biosamples, and you want to predict which metabolites are recoverable from microbial composition alone and identify groups of microbes and metabolites with correlated interaction patterns across multiple datasets or disease cohorts.

## When NOT to use

- Input metabolome data are not measured from the same biosamples as the microbiome data; paired designs are required to establish train-test relationships.
- You seek to infer mechanistic or biochemical pathways; MiMeNet is data-driven and does not incorporate stoichiometric or annotated reference models.
- Sample size is very small (<30) or unbalanced across conditions; nested cross-validation and background shuffling require sufficient replication to avoid spurious correlations.
- Metabolites of interest are rare or sparse (present in <10% of samples) — the preprocessing step will remove them before training.

## Inputs

- paired microbiome abundance table (samples × microbial features, CSV/TSV)
- paired metabolomic abundance table (samples × metabolite features, CSV/TSV)
- optional: external validation microbiome table
- optional: external validation metabolomic table
- optional: metabolite annotations (CSV)
- optional: sample labels/phenotypes (CSV)

## Outputs

- mean Spearman correlation coefficients per metabolite (SCC vector)
- count of well-predicted metabolites (integer, above 95th percentile threshold)
- microbe-metabolite feature attribution score matrix
- biclustered microbe and metabolite modules (interaction networks)
- background SCC distribution (empirical null from 100 shuffled iterations)
- module-based interaction network visualization

## How to apply

Preprocess microbiome and metabolomic data by removing features present in <10% of samples, then apply centered log-ratio (CLR) transformation with pseudocount of 1. Use nested 5-fold cross-validation to tune neural network hyperparameters (layer count, layer size, L2 regularization λ, dropout rate) on each dataset. Train multilayer perceptron networks with ReLU activation, ADAM optimizer, and MSE loss with early stopping (40 iterations without validation improvement). Evaluate over 10 iterations of 10-fold cross-validation (80/20 train-validation split) and calculate mean Spearman correlation coefficient (SCC) between predicted and observed metabolite abundances for each metabolite. Generate an empirical background distribution by retraining 100 shuffled models with randomized sample order, then define well-predicted metabolites as those with SCC above the 95th percentile of background correlations. Benchmark against appropriate baselines (Elastic Net, Random Forest, CCA) using identical cross-validation protocol, and aggregate results across datasets and iterations reporting mean ± standard deviation of SCC and well-predicted metabolite counts.

## Related tools

- **MiMeNet** (Primary neural network implementation for microbiome-metabolome prediction using multilayer perceptron with ReLU, ADAM optimizer, and feature attribution scoring) — https://github.com/YDaiLab/MiMeNet
- **MelonnPan** (Baseline method for comparison using Elastic Net linear regression to predict metabolite abundances from microbiome features) — https://github.com/biobakery/melonnpan
- **Random Forest** (Baseline regression model trained with 100 tree estimators for benchmarking predictive performance against neural network approach)
- **Canonical Correlation Analysis (CCA)** (Baseline method for identifying correlated dimensions across microbiome and metabolomic feature spaces using 10, 20, or 40 components)
- **scikit-learn** (Python library providing Elastic Net, Random Forest, CCA implementations, and cross-validation utilities for baseline model training and evaluation)
- **TensorFlow** (Deep learning framework (version 1.14+) for neural network construction, training with ADAM optimizer, and dropout regularization)
- **scikit-bio** (Bioinformatics library providing Spearman correlation coefficient calculation and microbiome data utilities)

## Examples

```
python MiMeNet_train.py -micro data/IBD/microbiome_PRISM.csv -metab data/IBD/metabolome_PRISM.csv -micro_norm None -metab_norm CLR -num_run_cv 10 -num_cv 10 -num_background 100 -output IBD_results
```

## Evaluation signals

- Mean Spearman correlation coefficients increase meaningfully over baselines (e.g., MiMeNet SCC 0.309 vs. MelonnPan 0.108 on IBD PRISM; 0.457 vs. 0.276 on Cystic Fibrosis; 0.264 vs. −0.272 on Soil dataset)
- Well-predicted metabolite counts substantially exceed baseline (e.g., 366 vs. 198 for IBD, 143 vs. 104 for CF, 29 vs. 4 for Soil)
- Background SCC distribution (from 100 shuffled iterations) exhibits lower mean correlation than observed dataset, and 95th percentile threshold is clearly separated from the bulk of null distribution
- Biclustered modules show coherent grouping: annotated metabolites co-cluster with unannotated ones sharing similar microbe interaction patterns; microbe modules associate with known ecological or functional groups
- External validation dataset (if available) produces SCC and well-predicted metabolite counts consistent with internal 10-fold cross-validation performance (within ±2 standard deviations)
- Feature attribution score matrix is sparse and interpretable: only microbes with at least one significant attribution score (e.g., ≥97.5th percentile) are retained in network visualization

## Limitations

- Not all metabolites are necessarily associated with microbes, resulting in lower prediction correlations and lower overall mean SCC across all metabolites; this limitation is inherent to the biological system, not the model
- MiMeNet analysis is data-driven and does not incorporate mechanistic knowledge (e.g., enzyme catalysis, stoichiometric models, or annotated metabolic references), so inferred interactions are associations, not causal mechanisms
- Lower threshold values observed for soil data compared to host-associated cohorts may reflect longitudinal sampling structure; generalizability across environmental contexts is not fully characterized
- Comparison with NED (Network Embedding Dimensionality) model is limited; reproducibility artifacts for external validation datasets are not provided in public repository
- Performance depends on feature filtering (10% presence threshold) and CLR transformation choices, which may remove rare but biologically relevant metabolites or microbes

## Evidence

- [results] MiMeNet achieves mean Spearman correlation coefficients that increase from 0.108 to 0.309 (IBD PRISM), 0.276 to 0.457 (Cystic Fibrosis), and -0.272 to 0.264 (Soil) compared to MelonnPan: "MiMeNet achieves mean Spearman correlation coefficients that increase from 0.108 to 0.309 (IBD PRISM), 0.276 to 0.457 (Cystic Fibrosis), and -0.272 to 0.264 (Soil) compared to MelonnPan"
- [results] Load and preprocess microbiome and metabolomic data from IBD (PRISM), Cystic Fibrosis, and Soil datasets, removing features present in <10% of samples and applying centered log-ratio (CLR) transformation with pseudocount of 1: "removing features present in <10% of samples and applying centered log-ratio (CLR) transformation with pseudocount of 1"
- [results] Perform hyperparameter tuning using nested 5-fold cross-validation to select optimal layer size, number of layers, L2 regularization (λ), and dropout rates for MiMeNet MLPNN architecture on each dataset.: "Perform hyperparameter tuning using nested 5-fold cross-validation to select optimal layer size, number of layers, L2 regularization (λ), and dropout rates for MiMeNet MLPNN architecture"
- [results] Train MiMeNet using ADAM optimizer with mean squared error loss function and L2 regularization, applying ReLU activation and dropout at each hidden layer, with early stopping when validation loss does not improve within 40 iterations.: "Train MiMeNet using ADAM optimizer with mean squared error loss function and L2 regularization, applying ReLU activation and dropout at each hidden layer, with early stopping when validation loss"
- [results] Generate background SCC distribution by training 100 shuffled models with random sample reordering and define well-predicted metabolites as those with SCC above the 95th percentile of background correlations.: "Generate background SCC distribution by training 100 shuffled models with random sample reordering and define well-predicted metabolites as those with SCC above the 95th percentile of background"
- [results] Evaluate MiMeNet over 10 iterations of 10-fold cross-validation (90% training, 10% test; 80/20 train-validation split) and calculate mean Spearman correlation coefficient (SCC) between predicted and observed metabolite abundances.: "Evaluate MiMeNet over 10 iterations of 10-fold cross-validation (90% training, 10% test; 80/20 train-validation split) and calculate mean Spearman correlation coefficient (SCC)"
- [discussion] Although the MiMeNet analysis is data-driven without incorporating mechanistic knowledge, these types of evidence obtained from the integrative analysis: "Although the MiMeNet analysis is data-driven without incorporating mechanistic knowledge"
- [discussion] since not all metabolites may be associated with microbes, some metabolites will have lower prediction correlations, which resulted in an overall lower mean correlation across all metabolites: "since not all metabolites may be associated with microbes, some metabolites will have lower prediction correlations"
- [readme] python MiMeNet_train.py -micro data/IBD/microbiome_PRISM.csv -metab data/IBD/metabolome_PRISM.csv -external_micro data/IBD/microbiome_external.csv -external_metab data/IBD/metabolome_external.csv -micro_norm None -metab_norm CLR -net_params results/IBD/network_parameters.txt -annotation data/IBD/metabolome_annotation.csv -labels data/IBD/diagnosis_PRISM.csv -num_run_cv 10 -output IBD: "python MiMeNet_train.py -micro data/IBD/microbiome_PRISM.csv -metab data/IBD/metabolome_PRISM.csv -external_micro data/IBD/microbiome_external.csv -external_metab data/IBD/metabolome_external.csv"
- [results] MiMeNet constructs a score matrix of microbe-metabolite feature attributions between the microbes and well-predicted metabolites, then biclusters the score matrix into microbial and metabolomic modules: "MiMeNet constructs a score matrix of microbe-metabolite feature attributions between the microbes and well-predicted metabolites, then biclusters the score matrix into microbial and metabolomic"
