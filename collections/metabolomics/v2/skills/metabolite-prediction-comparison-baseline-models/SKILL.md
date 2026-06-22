---
name: metabolite-prediction-comparison-baseline-models
description: Use when you have paired microbiome (genus-level 16S or functional profiles) and metabolome datasets (e.g., mass spectrometry or metabolomics panels) with 100+ samples, and you want to demonstrate that a new prediction method outperforms prior work.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3445
  edam_topics:
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_3174
  - http://edamontology.org/topic_0091
  tools:
  - MiMeNet
  - MelonnPan
  - Elastic Net
  - NED
  - scikit-learn
  - Python
  - TensorFlow
  - Random Forest
  - Canonical Correlation Analysis (CCA)
  - NED (Non-negative Embedding)
derived_from:
- doi: 10.1371/journal.pcbi.1009021
  title: MiMeNet
evidence_spans:
- MiMeNet (Microbiome-Metabolome Network), a multi-layer perceptron (MLPNN)
- MiMeNet uses paired microbiome and metabolome data for model training. Microbiome abundance features (green) are used to train a neural network to predict metabolite abundance features (blue).
- we first compared MiMeNet to MelonnPan, a recent model that uses Elastic Net linear regression
- we benchmarked MiMeNet against other general regression models, i.e., Random Forest (RF), multivariate Elastic Net, and canonical correlation analysis (CCA) models
- The NED model was trained using code downloaded from https://github.com/vuongle2/BiomeNED
- MelonnPan and NED models were obtained from their respective GitHub repositories and executed using default parameters as according to their tutorials. Random Forest, multivariate Elastic Net, and
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mimenet_cq
    doi: 10.1371/journal.pcbi.1009021
    title: MiMeNet
  dedup_kept_from: coll_mimenet_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pcbi.1009021
  all_source_dois:
  - 10.1371/journal.pcbi.1009021
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-prediction-comparison-baseline-models

## Summary

Benchmark a neural network-based metabolite prediction model against established linear regression and other baseline methods using cross-validated Spearman correlation coefficients and counts of well-predicted metabolites. This skill enables empirical assessment of whether a candidate method identifies more metabolites above a statistically derived threshold than existing approaches.

## When to use

You have paired microbiome (genus-level 16S or functional profiles) and metabolome datasets (e.g., mass spectrometry or metabolomics panels) with 100+ samples, and you want to demonstrate that a new prediction method outperforms prior work. Specifically, when you need to show improvement in (1) mean prediction accuracy across all metabolites, (2) count of 'well-predicted' metabolites meeting a correlation threshold, or (3) both, on identical datasets using identical evaluation protocols.

## When NOT to use

- Your dataset has <50 paired samples; the 10-fold cross-validation and background shuffling will be unreliable.
- Microbiome and metabolome samples are not paired or do not share identical sample IDs and ordering; the comparison assumes matched observations.
- You have already selected a single 'best' baseline method; the skill requires parallel training of multiple established baselines under identical conditions to isolate the candidate model's advantage.

## Inputs

- Paired microbiome abundance table (samples × taxa/features, centered log-ratio transformed or raw counts)
- Paired metabolome abundance table (samples × metabolites, centered log-ratio transformed, features filtered to ≥10% presence)
- Hyperparameter specification for candidate model (JSON or text file: layer size, hidden layers, L2 penalty, dropout, optimizer, loss, early stopping patience)
- Optional: external validation microbiome and metabolome tables for out-of-sample assessment

## Outputs

- Mean Spearman correlation coefficient (SCC) per method (scalar per model)
- Count of well-predicted metabolites per method (integer, metabolites with SCC ≥ 95th percentile threshold)
- Background distribution of SCCs (vector from shuffled cross-validation iterations)
- 95th percentile SCC threshold (scalar, dataset-specific)
- Scatter plot comparing candidate model vs. baseline model prediction correlations (with summary statistics overlay)
- Improvement ratio: (candidate well-predicted count − baseline count) / baseline count or similar metric

## How to apply

Prepare paired microbiome and metabolome data with identical sample ordering. Apply centered log-ratio transformation to metabolite features and filter features present in <10% of samples. Train your candidate model (e.g., neural network) using 10 iterations of 10-fold cross-validation with documented hyperparameters. In parallel, train baseline models (Elastic Net for MelonnPan, Random Forest, CCA, or others) using the same cross-validation scheme and default parameters. Generate a background distribution by shuffling both the microbiome and metabolome 100 times and computing cross-validated correlations; derive the 95th percentile Spearman correlation coefficient (SCC) threshold from this distribution (e.g., 0.136 for IBD PRISM). Define well-predicted metabolites as those with SCC ≥ the 95th percentile threshold. For each method, report (1) mean SCC across all metabolites, (2) count of well-predicted metabolites, and (3) scatter plots with summary statistics comparing candidate vs. baseline predictions. This protocol isolates the model architecture effect by controlling for data preprocessing, cross-validation strategy, and statistical threshold derivation.

## Related tools

- **MiMeNet** (Candidate multi-layer perceptron neural network model for microbiome-to-metabolome prediction; trained with optimized hyperparameters (layer size, dropout, L2 penalty) via 10 iterations of 10-fold cross-validation) — https://github.com/YDaiLab/MiMeNet
- **MelonnPan** (Baseline Elastic Net linear regression method applied independently to each metabolite; establishes prior prediction accuracy for comparison) — https://github.com/biobakery/melonnpan
- **Elastic Net** (Regularized linear regression algorithm underlying MelonnPan baseline; used for per-metabolite independent prediction)
- **Random Forest** (General regression baseline method benchmarked against MiMeNet; models metabolite prediction from microbiome features)
- **Canonical Correlation Analysis (CCA)** (Multivariate baseline method for joint modeling of microbiome-metabolome relationships; alternative to independent per-metabolite regression)
- **scikit-learn** (Python library providing Elastic Net, Random Forest, and cross-validation utilities for implementing and evaluating baseline models)
- **TensorFlow** (Deep learning framework used to implement and train the candidate multi-layer perceptron neural network with ADAM optimizer and early stopping)
- **NED (Non-negative Embedding)** (Optional alternative baseline method for metabolite prediction; provides additional comparison point beyond Elastic Net and Random Forest) — https://github.com/vuongle2/BiomeNED

## Examples

```
python MiMeNet_train.py -micro data/IBD/microbiome_PRISM.csv -metab data/IBD/metabolome_PRISM.csv -micro_norm None -metab_norm CLR -num_run_cv 10 -num_background 100 -output IBD_comparison && compare_correlations.py --mimemet_output IBD/correlations.txt --melonnpan_output melonnpan_trained_weights.txt --threshold 0.136 --plot scatter_comparison.pdf
```

## Evaluation signals

- Background distribution from shuffled cross-validation spans a lower range (e.g., 0.1–0.2 SCC) than observed correlations from real data; 95th percentile threshold is well-separated from median background SCC.
- Candidate model mean SCC is substantially higher than all baseline models across the same dataset (e.g., MiMeNet 0.309 vs. MelonnPan 0.108 on IBD PRISM).
- Count of well-predicted metabolites (SCC ≥ 95th percentile) for candidate model exceeds all baseline counts by ≥50% or shows clear rank-ordering (e.g., MiMeNet 351 > MelonnPan 198).
- Scatter plot of candidate vs. baseline correlations shows candidate predictions clustering above the identity line (y=x), indicating systematic improvement, not just noise.
- Improvement metrics (ratio, absolute count difference) are consistent across multiple datasets (e.g., IBD, Cystic Fibrosis, soil biocrust), suggesting generalizability of the candidate model advantage.

## Limitations

- Not all metabolites are associated with microbes, so some metabolites will have lower prediction correlations, reducing overall mean SCC across all metabolites even for well-performing methods.
- The 95th percentile threshold is dataset-specific and data-dependent; a higher threshold for longitudinal data (e.g., soil biocrust, threshold 0.410) may reflect temporal dependencies rather than model quality, complicating cross-dataset comparison.
- Comparison is sensitive to choice of normalization (CLR vs. relative abundance) and filtering (e.g., ≥10% presence cutoff); applying different preprocessing to candidate vs. baseline methods will confound the model-level comparison.
- External validation performance may differ substantially from cross-validated performance; demonstrating improvement on held-out cohorts is important but not always performed.
- Interpretability of neural network models is limited to data-driven feature attribution scores without mechanistic knowledge integration; baseline methods like Elastic Net provide explicit regression coefficients that may be more clinically actionable.

## Evidence

- [other] On the IBD (PRISM) dataset, MiMeNet identified 351 well-predicted metabolites from 8848 total metabolites, whereas MelonnPan identified 198 well-predicted metabolites using the same correlation cutoff of 0.3.: "MiMeNet identified 351 well-predicted metabolites from 8848 total metabolites, whereas MelonnPan identified 198 well-predicted metabolites using the same correlation cutoff"
- [other] Train MiMeNet using 10 iterations of 10-fold cross-validation with optimized hyperparameters (layer size 512, 1 hidden layer, L2 penalty 0.001, dropout 0.5), using ADAM optimizer and MSE loss with early stopping (40 epoch patience). Train MelonnPan using default parameters with Elastic Net linear regression for each metabolite independently.: "Train MiMeNet using 10 iterations of 10-fold cross-validation with optimized hyperparameters (layer size 512, 1 hidden layer, L2 penalty 0.001, dropout 0.5), using ADAM optimizer and MSE loss with"
- [other] Generate background distribution by shuffling samples in both microbiome and metabolome 100 times and performing cross-validated evaluation; calculate 95th percentile SCC threshold (0.136 for IBD PRISM).: "Generate background distribution by shuffling samples in both microbiome and metabolome 100 times and performing cross-validated evaluation; calculate 95th percentile SCC threshold (0.136 for IBD"
- [other] Identify well-predicted metabolites for each method as those with SCC ≥ 95th percentile threshold; count total well-predicted metabolites.: "Identify well-predicted metabolites for each method as those with SCC ≥ 95th percentile threshold; count total well-predicted metabolites"
- [results] the predictive performance of a model is measured by the average Spearman correlation coefficients (SCCs) between the predicted and the observed abundance of the metabolites: "the predictive performance of a model is measured by the average Spearman correlation coefficients (SCCs) between the predicted and the observed abundance of the metabolites"
- [results] we benchmarked MiMeNet against other general regression models, i.e., Random Forest (RF), multivariate Elastic Net, and canonical correlation analysis (CCA) models: "we benchmarked MiMeNet against other general regression models, i.e., Random Forest (RF), multivariate Elastic Net, and canonical correlation analysis (CCA) models"
- [intro] MelonnPan models each metabolite individually, missing the opportunity to use shared information across metabolomic features to boost prediction: "MelonnPan models each metabolite individually, missing the opportunity to use shared information across metabolomic features to boost prediction"
- [methods] Any input or output feature that is present in less than 10% of samples was removed: "Any input or output feature that is present in less than 10% of samples was removed"
- [methods] We then defined a metabolite as well-predicted if its SCC is above the 95th percentile of the background correlations: "We then defined a metabolite as well-predicted if its SCC is above the 95th percentile of the background correlations"
- [results] MiMeNet then generates a background distribution of SCCs through multiple iterations of shuffling the dataset and performing a cross-validated evaluation on the shuffled set: "MiMeNet then generates a background distribution of SCCs through multiple iterations of shuffling the dataset and performing a cross-validated evaluation on the shuffled set"
