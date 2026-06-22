---
name: spearman-correlation-statistical-analysis
description: Use when you have paired predicted and observed metabolite abundance vectors from a predictive model (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3445
  edam_topics:
  - http://edamontology.org/topic_3697
  - http://edamontology.org/topic_0625
  tools:
  - Canonical Correlation Analysis (CCA)
  - ADAM optimizer
  - scikit-learn (Python)
  - MiMeNet
  - MelonnPan
  - scikit-learn
derived_from:
- doi: 10.1371/journal.pcbi.1009021
  title: MiMeNet
evidence_spans:
- Canonical correlation analyses were implemented using CCA with 10, 20, and 40 components.
- MiMeNet was trained using the ADAM optimizer and the mean squared error (MSE) loss function.
- MiMeNet was trained using the ADAM optimizer and the mean squared error (MSE) loss function
- these models can predict the entire set of metabolites at once, and all models were evaluated using 10 iterations of 10-fold cross-validation. Random Forest, multivariate Elastic Net, and Canonical
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Spearman-Correlation Statistical Analysis

## Summary

Compute Spearman rank correlation coefficients (SCC) between predicted and observed metabolite abundances to quantify prediction accuracy across cross-validated folds. This non-parametric correlation metric is essential for evaluating microbiome-metabolome prediction models when the underlying relationship may be monotonic but not necessarily linear.

## When to use

You have paired predicted and observed metabolite abundance vectors from a predictive model (e.g., neural network, Elastic Net, Random Forest) evaluated over multiple cross-validation folds, and you need to measure how well the model's predictions rank-correlate with ground truth, accounting for potential non-linearity and robustness to outliers in compositional data.

## When NOT to use

- Input is qualitative (presence/absence) rather than quantitative relative abundance; use rank-based association measures instead.
- Sample size is extremely small (n < 10) and cross-validation folds cannot be meaningfully stratified.
- Metabolite abundances are already log-ratio transformed and you require raw correlation interpretation (document the transformation in results).

## Inputs

- Predicted metabolite abundance matrix (samples × metabolites)
- Observed metabolite abundance matrix (samples × metabolites)
- Cross-validation fold assignments or iteration metadata

## Outputs

- Mean Spearman correlation coefficient (SCC) per model ± standard deviation
- Per-metabolite SCC values across all cross-validation iterations
- Background SCC distribution (from shuffled data, ≥100 iterations)
- 95th percentile threshold from background distribution
- Binary classification of well-predicted metabolites (SCC > 95th percentile)

## How to apply

For each metabolite across all cross-validation iterations, calculate the Spearman rank correlation coefficient between predicted and observed relative abundances. Aggregate SCC values across metabolites and iterations to compute mean ± standard deviation. Use the mean SCC as the primary performance metric to compare models. Additionally, generate a background SCC distribution by training models on shuffled samples (with randomly reordered sample labels) across the same cross-validation protocol, then define well-predicted metabolites as those with SCC above the 95th percentile of background correlations. This empirical threshold distinguishes truly predictable features from noise-driven spurious correlations.

## Related tools

- **MiMeNet** (Neural network framework that trains models to predict metabolomic profiles from microbiome data and applies SCC evaluation across 10-fold cross-validation iterations) — https://github.com/YDaiLab/MiMeNet
- **MelonnPan** (Elastic Net linear regression baseline model evaluated using identical Spearman correlation and cross-validation protocol for benchmarking) — https://github.com/biobakery/melonnpan
- **scikit-learn** (Provides random forest regression and cross-validation utilities; SCC can be computed via scipy.stats.spearmanr)

## Examples

```
from scipy.stats import spearmanr; scc_per_metabolite = [spearmanr(predicted[:, i], observed[:, i])[0] for i in range(predicted.shape[1])]; mean_scc = np.mean(scc_per_metabolite); bg_scc_threshold = np.percentile(background_correlations, 95); well_predicted = [scc > bg_scc_threshold for scc in scc_per_metabolite]
```

## Evaluation signals

- SCC values range from −1 to +1; mean SCC for well-performing models on real data should be substantially higher than the 95th percentile of the background distribution generated from shuffled samples.
- Standard deviation of SCC across iterations should be reasonable relative to mean (coefficient of variation typically <50% for stable predictions).
- The number of well-predicted metabolites (SCC > 95th percentile threshold) should be substantially higher than expected by chance; compare to random baseline.
- External validation datasets (held-out cohorts) should show similar or slightly lower mean SCC compared to internal cross-validation, indicating generalizability.
- Model comparison (e.g., MiMeNet vs. MelonnPan) should show statistically meaningful differences in mean SCC; report effect sizes and confidence intervals across iterations.

## Limitations

- Not all metabolites are biologically associated with the microbiome, so some will inherently have low SCC even in well-performing models, lowering the overall mean correlation across all features.
- SCC is rank-based and may mask absolute prediction error magnitude; two models with different error distributions can yield identical correlations.
- The 95th percentile background threshold is empirically derived and may be sensitive to sample size, number of background iterations, and the degree of data shuffling; recommend at least 100 background iterations.
- Centered log-ratio (CLR) or relative abundance transformations alter the correlation landscape compared to raw counts; results are not directly comparable across different normalization strategies.
- The method assumes that shuffled-sample correlations reflect true noise, but strong compositional structure (e.g., spike taxa) can inflate background correlations.

## Evidence

- [methods] the predictive performance of a model is measured by the average Spearman correlation coefficients (SCCs) between the predicted and the observed abundances: "the predictive performance of a model is measured by the average Spearman correlation coefficients (SCCs) between the predicted and the observed abundances"
- [results] MiMeNet achieves mean Spearman correlation coefficients that increase from 0.108 to 0.309 (IBD PRISM), 0.276 to 0.457 (Cystic Fibrosis), and -0.272 to 0.264 (Soil) compared to MelonnPan: "MiMeNet achieves mean Spearman correlation coefficients that increase from 0.108 to 0.309 (IBD PRISM), 0.276 to 0.457 (Cystic Fibrosis), and -0.272 to 0.264 (Soil) compared to MelonnPan"
- [methods] We then defined a metabolite as well-predicted if its SCC is above the 95th percentile of the background correlations: "We then defined a metabolite as well-predicted if its SCC is above the 95th percentile of the background correlations"
- [results] MiMeNet then generates a background distribution of SCCs through multiple iterations of shuffling the dataset and performing a cross-validation on the shuffled set: "MiMeNet then generates a background distribution of SCCs through multiple iterations of shuffling the dataset and performing a cross-validation on the shuffled set"
- [abstract] Using ten iterations of 10-fold cross-validation on three paired microbiome-metabolome datasets: "Using ten iterations of 10-fold cross-validation on three paired microbiome-metabolome datasets"
- [discussion] since not all metabolites may be associated with microbes, some metabolites will have lower prediction correlations, which resulted in an overall lower mean correlation across all metabolites: "since not all metabolites may be associated with microbes, some metabolites will have lower prediction correlations, which resulted in an overall lower mean correlation across all metabolites"
