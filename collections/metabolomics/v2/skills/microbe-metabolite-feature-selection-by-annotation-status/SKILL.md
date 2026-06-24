---
name: microbe-metabolite-feature-selection-by-annotation-status
description: Use when when you have paired microbiome-metabolome datasets where only
  a subset of metabolites carry curated biochemical annotations (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3697
  - http://edamontology.org/topic_0160
  - http://edamontology.org/topic_3674
  tools:
  - MiMeNet
  - ADAM optimizer
  - TensorFlow
  - scikit-learn
  - Seaborn/Matplotlib
  license_tier: restricted
derived_from:
- doi: 10.1371/journal.pcbi.1009021
  title: MiMeNet
evidence_spans:
- An MLPNN model is composed of multiple fully connected hidden layers composed of
  perceptrons
- MiMeNet is an integrative MLPNN, which trains models to accurately predict the metabolome
  based on a microbiome
- MiMeNet was trained using the ADAM optimizer and the mean squared error (MSE) loss
  function.
- MiMeNet was trained using the ADAM optimizer and the mean squared error (MSE) loss
  function
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

# Microbe-Metabolite Feature Selection by Annotation Status

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Stratify metabolite prediction models by whether metabolites carry curated biochemical annotations, enabling separate evaluation of annotated versus unannotated features to measure the impact of annotation availability on prediction accuracy. This skill surfaces latent predictive signal in unannotated metabolites that can improve overall model performance when trained jointly.

## When to use

When you have paired microbiome-metabolome datasets where only a subset of metabolites carry curated biochemical annotations (e.g., from metabolomic reference databases), and you want to quantify whether including unannotated metabolites as training outputs improves prediction accuracy for the annotated subset. This is particularly relevant when evaluating whether integrative multi-output neural network models can leverage shared structure across annotated and unannotated features to enhance annotation-driven downstream applications.

## When NOT to use

- Input contains only annotated metabolites with no unannotated counterparts — this skill requires a meaningful pool of unannotated features to measure the benefit of multi-output learning.
- Annotation status is uncertain or not reliably distinguishable in your metabolomic data — annotation label noise will confound the comparison.
- Sample size is very small (< 40 samples) — reliable 10-fold cross-validation and background permutation distributions require adequate data to estimate model variance.
- Your downstream use case requires high interpretability per feature — this skill optimizes aggregate prediction gain, not individual feature importance or mechanistic insights.

## Inputs

- Paired microbiome feature table (samples × microbial features, relative abundance or CLR-transformed)
- Paired metabolome feature table (samples × metabolite features, CLR-normalized with pseudocount of 1)
- Metabolite annotation file (mapping subset of metabolites to curated biochemical identities)
- Train-test split indices (80% training, 20% validation, consistent across both model configurations)
- Network hyperparameter configuration (JSON: hidden layer count, node count, L2 penalty, dropout rate)

## Outputs

- Spearman correlation coefficient matrix (annotated metabolites × 100 cross-validation folds, two model conditions)
- Per-metabolite improvement deltas and statistical significance (delta_SCC, p-value)
- Count of well-predicted metabolites for each condition (threshold: 95th percentile of background SCC distribution)
- Comparative scatterplot (SCC_all vs. SCC_annotated_only) for each annotated metabolite
- Mean SCC improvement across all annotated metabolites and confidence intervals

## How to apply

Prepare two parallel neural network training regimes on identical input microbial features and train-test splits: (1) Train a model using all metabolites (annotated + unannotated) as outputs; (2) Train an identically configured model using only annotated metabolites as outputs. For each regime, perform 10 iterations of 10-fold cross-validation with the same network hyperparameters (e.g., single hidden layer, L2 regularization λ=0.001, dropout=0.5) and identical ADAM optimizer settings. Evaluate both models on held-out test folds and compute Spearman correlation coefficients (SCC) for each annotated metabolite across all 100 model runs. Calculate per-metabolite improvement delta (SCC_all − SCC_annotated_only) and report mean delta and count of well-predicted metabolites (those above the 95th percentile threshold) for each condition. Statistical significance is assessed via permutation testing or bootstrapped confidence intervals.

## Related tools

- **MiMeNet** (Neural network framework for multi-output microbe-to-metabolite prediction; enables joint training on annotated and unannotated metabolites as separate experimental conditions) — https://github.com/YDaiLab/MiMeNet
- **TensorFlow** (Deep learning backend for training MLPNN models with configurable regularization, dropout, and early stopping)
- **scikit-learn** (Provides cross-validation utilities (KFold, StratifiedKFold) and performance metrics (Spearman correlation via scipy.stats))
- **ADAM optimizer** (Adaptive learning rate optimizer used for training both model variants with identical convergence settings)
- **Seaborn/Matplotlib** (Visualization of comparative scatterplots and improvement distributions across annotated metabolites)

## Examples

```
python MiMeNet_train.py -micro data/IBD/microbiome_PRISM.csv -metab data/IBD/metabolome_PRISM.csv -annotation data/IBD/metabolome_annotation.csv -num_run_cv 10 -num_cv 10 -net_params results/IBD/network_parameters.txt -output results/IBD_annotated_vs_all && python MiMeNet_train.py -micro data/IBD/microbiome_PRISM.csv -metab data/IBD/metabolome_PRISM.csv -annotation data/IBD/metabolome_annotation.csv -num_run_cv 10 -num_cv 10 -net_params results/IBD/network_parameters.txt -output results/IBD_annotated_only --annotated_only
```

## Evaluation signals

- Mean Spearman correlation coefficient for annotated metabolites improves in the multi-output (all metabolites) condition relative to annotated-only baseline (e.g., Δ SCC ≥ 0.05, p < 0.05).
- Count of well-predicted annotated metabolites (SCC > 95th percentile of background) increases when unannotated metabolites are included in training (e.g., 333 → 366 out of 466 in IBD dataset).
- Per-metabolite improvement deltas (SCC_all − SCC_annotated_only) are distributed such that majority of annotated metabolites show positive or neutral delta, not systematic degradation.
- Cross-validation is reproducible: identical hyperparameters, random seed, and train-test split indices yield same mean SCC and delta across repeated runs.
- Statistical test (e.g., paired t-test, Wilcoxon signed-rank) on per-metabolite deltas confirms significance of improvement, with effect size (Cohen's d) consistent with biological plausibility.

## Limitations

- Not all metabolites may be microbiome-associated, causing lower prediction correlations for some features even in the all-metabolites condition; this may obscure the true benefit for microbially-linked metabolites.
- Annotation quality and completeness vary across metabolomic platforms and reference databases; sparse or incorrect annotations in the input file will weaken the annotation-only baseline, artificially inflating the measured improvement.
- The comparison assumes identical network architecture and hyperparameters for both conditions; if hyperparameters are separately tuned per condition, the comparison conflates the benefit of annotation-aware multi-output learning with the benefit of condition-specific regularization.
- Cross-validation split strategy (e.g., 10-fold vs. stratified by phenotype) can affect results; stratification by disease state or other covariates may yield different deltas than random folds, complicating generalization.
- External validation on independent cohorts may reveal that the improvement is dataset- or platform-specific and does not generalize to new metabolomic profiles.
- The 95th percentile threshold for 'well-predicted' is empirical and not mechanistically justified; changes in threshold choice can alter the count of well-predicted metabolites and mask or inflate improvements.

## Evidence

- [other] Training MiMeNet on all metabolites improved mean Spearman correlation coefficients for annotated metabolites from 0.259 to 0.309 (P < 10−47), with well-predicted metabolites increasing from 333 to 366 out of 466 annotated metabolites in the IBD (PRISM) dataset.: "Training MiMeNet on all metabolites improved mean Spearman correlation coefficients for annotated metabolites from 0.259 to 0.309 (P < 10−47), with well-predicted metabolites increasing from 333 to"
- [other] For each iteration-fold, train a separate MiMeNet MLPNN model (using optimal hyperparameters: 512-node single hidden layer, L2 penalty λ=0.001, dropout=0.5, ReLU activation) on the complete feature set (all metabolites), using ADAM optimizer and mean squared error loss with early stopping (patience=40 epochs). In parallel, train an identically configured MiMeNet model using only annotated metabolites as outputs.: "train a separate MiMeNet MLPNN model (using optimal hyperparameters: 512-node single hidden layer, L2 penalty λ=0.001, dropout=0.5, ReLU activation) on the complete feature set (all metabolites),"
- [other] Evaluate both models on the held-out test fold; calculate Spearman correlation coefficient (SCC) between predicted and observed abundance for each annotated metabolite across all 100 model runs (10 iterations × 10 folds). Compute mean SCC per annotated metabolite for each training regime and generate scatterplot comparing the two conditions; calculate per-metabolite delta (SCC_all − SCC_annotated_only) and overall mean delta.: "Evaluate both models on the held-out test fold; calculate Spearman correlation coefficient (SCC) between predicted and observed abundance for each annotated metabolite across all 100 model runs (10"
- [discussion] since not all metabolites may be associated with microbes, some metabolites will have lower prediction correlations, which resulted in an overall lower mean correlation across all metabolites: "since not all metabolites may be associated with microbes, some metabolites will have lower prediction correlations, which resulted in an overall lower mean correlation across all metabolites"
- [other] We then defined a metabolite as well-predicted if its SCC is above the 95th percentile of the background correlations: "We then defined a metabolite as well-predicted if its SCC is above the 95th percentile of the background correlations"
- [other] Any input or output feature that is present in less than 10% of samples was removed: "Any input or output feature that is present in less than 10% of samples was removed"
- [other] Split data into training (80%) and validation (20%) sets, then perform 10 iterations of 10-fold cross-validation.: "Split data into training (80%) and validation (20%) sets, then perform 10 iterations of 10-fold cross-validation"
- [other] Load IBD (PRISM) microbiome and metabolomic data, apply centered log-ratio transformation with pseudocount of 1, and filter features present in <10% of samples.: "Load IBD (PRISM) microbiome and metabolomic data, apply centered log-ratio transformation with pseudocount of 1, and filter features present in <10% of samples"
