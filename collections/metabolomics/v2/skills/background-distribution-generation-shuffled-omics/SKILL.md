---
name: background-distribution-generation-shuffled-omics
description: Use when when training a regression or neural-network model on paired microbiome and metabolome data, and you need to establish a statistically principled cutoff for identifying metabolites (or other features) whose prediction correlations are significantly better than random chance.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
  edam_topics:
  - http://edamontology.org/topic_3697
  - http://edamontology.org/topic_0610
  - http://edamontology.org/topic_3174
  tools:
  - MiMeNet
  - MelonnPan
  - Elastic Net
  - NED
  - scikit-learn
  - Python
  - TensorFlow
  - Scipy
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

# background-distribution-generation-shuffled-omics

## Summary

Generate an empirical null distribution of prediction performance metrics (e.g., Spearman correlation coefficients) by repeatedly shuffling paired omics datasets and performing cross-validated model evaluation. This establishes statistical thresholds for identifying well-predicted features and distinguishing signal from noise in microbiome–metabolome predictive models.

## When to use

When training a regression or neural-network model on paired microbiome and metabolome data, and you need to establish a statistically principled cutoff for identifying metabolites (or other features) whose prediction correlations are significantly better than random chance. Especially useful when the absolute correlation magnitude varies across datasets (e.g., due to measurement noise, longitudinal structure, or ecological heterogeneity) and a fixed threshold would be inappropriate.

## When NOT to use

- Input data are already filtered to contain only known predictable features (background distribution should be run on unfiltered data to be valid).
- Paired structure has already been intentionally broken or samples are unpaired.
- Sample size is very small (< 50 samples) such that 10-fold CV produces unreliable estimates of the null; consider a simpler permutation test or pooled external validation instead.

## Inputs

- paired microbiome feature table (samples × taxa/genes, relative abundance or CLR-transformed)
- paired metabolome feature table (samples × metabolites, relative abundance or CLR-transformed)
- trained model architecture and hyperparameters (e.g., layer size, regularization, dropout)
- cross-validation scheme (number of folds, iterations)

## Outputs

- background distribution of performance scores (e.g., Spearman correlation coefficients from 100+ shuffled CV runs)
- empirical significance threshold (e.g., 95th percentile SCC value, dataset-specific)
- list of well-predicted features (those with observed SCC ≥ threshold)

## How to apply

Perform multiple iterations (10 or more recommended) of 10-fold cross-validation on the shuffled dataset: for each iteration, independently shuffle the samples in both the microbiome and metabolome tables (breaking the pairing), then train and evaluate the model using the same cross-validation procedure and performance metric (e.g., Spearman correlation coefficient) as the real analysis. Collect the performance scores across all folds and iterations to construct an empirical distribution. Define the significance threshold as the 95th percentile (or another justifiable quantile) of this background distribution; only metabolites with observed cross-validated performance at or above this threshold are considered well-predicted. This approach accounts for the intrinsic variance in the data and model without assuming a parametric null.

## Related tools

- **MiMeNet** (neural-network model trained and evaluated on shuffled data to compute background performance distribution) — https://github.com/YDaiLab/MiMeNet
- **scikit-learn** (provides cross-validation splits and correlation/regression utilities)
- **TensorFlow** (backend for training neural network models during background CV iterations)
- **Scipy** (computes Spearman correlation coefficients and percentile statistics)

## Examples

```
python MiMeNet_train.py -micro data/IBD/microbiome_PRISM.csv -metab data/IBD/metabolome_PRISM.csv -micro_norm None -metab_norm CLR -num_run_cv 10 -num_cv 10 -num_background 100 -output results/IBD_background
```

## Evaluation signals

- Background distribution SCC values are centered near zero and symmetric (indicating true shuffling broke the microbe–metabolite association).
- 95th percentile threshold is dataset-specific and varies across IBD (PRISM) [0.136], cystic fibrosis [0.129], and soil [0.410] datasets, reflecting biological and technical heterogeneity.
- Number of well-predicted metabolites identified from observed data is substantially smaller than total metabolites tested, and typically 5–10× higher than would be expected from random chance alone (e.g., 351 / 8848 ≈ 4% for IBD PRISM, consistent with signal enrichment above the 95th percentile null).
- Observed (paired) cross-validated SCCs for well-predicted metabolites are visibly separated from the background distribution in a histogram or Q–Q plot.
- External validation on held-out cohorts shows that metabolites passing the threshold generalize better than random-expectation metabolites.

## Limitations

- Threshold estimation depends on the number of background iterations; ≥ 100 iterations are strongly recommended for stable 95th percentile estimates (the MiMeNet paper used 100 shuffles).
- Longitudinal structure in the data (e.g., multiple time points per subject) can inflate background correlations and artificially raise the significance threshold; the soil dataset exhibited higher threshold (0.410) than others, possibly due to temporal dependency.
- Shuffling assumes features are exchangeable within each table; if there are missing-data patterns, batch effects, or confounding variables, shuffling alone does not ensure a valid null.
- The method does not incorporate mechanistic or phylogenetic knowledge; some metabolites may be genuinely unpredictable from microbiome alone (not all metabolites are microbe-associated), leading to lower mean prediction correlations overall.

## Evidence

- [methods] MiMeNet then generates a background distribution of SCCs through multiple iterations of shuffling the dataset and performing a cross-validated evaluation on the shuffled set: "MiMeNet then generates a background distribution of SCCs through multiple iterations of shuffling the dataset and performing a cross-validated evaluation"
- [other] Generate background distribution by shuffling samples in both microbiome and metabolome 100 times and performing cross-validated evaluation; calculate 95th percentile SCC threshold (0.136 for IBD PRISM).: "shuffling samples in both microbiome and metabolome 100 times and performing cross-validated evaluation; calculate 95th percentile SCC threshold (0.136 for IBD PRISM)"
- [results] This background distribution of SCCs is then used to determine a cutoff for significantly well-predicted metabolites: "This background distribution of SCCs is then used to determine a cutoff for significantly well-predicted metabolites"
- [methods] We then defined a metabolite as well-predicted if its SCC is above the 95th percentile of the background correlations: "We then defined a metabolite as well-predicted if its SCC is above the 95th percentile of the background correlations"
- [discussion] We also observed a higher threshold value for the soil data (Fig 3A–3C), which may be due to the longitudinal observations.: "We also observed a higher threshold value for the soil data, which may be due to the longitudinal observations"
- [readme] num_background: Integer for number of iterations of 10-fold cross-validation to run on shuffled data in order to generate empirical background (Recommend at least 10): "Integer for number of iterations of 10-fold cross-validation to run on shuffled data in order to generate empirical background (Recommend at least 10)"
