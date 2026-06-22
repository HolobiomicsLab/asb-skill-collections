---
name: spearman-correlation-background-distribution-analysis
description: Use when after cross-validated neural network or regression models have generated predicted metabolite abundances and you need to distinguish genuinely predictable metabolites from those with spuriously high correlations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3463
  edam_topics:
  - http://edamontology.org/topic_3697
  - http://edamontology.org/topic_3174
  tools:
  - MiMeNet
  - scikit-learn (MLPRegressor)
  - ADAM optimizer
  - ReLU activation
  - SciPy (Spearman correlation)
  - NumPy
  - SciPy Spearman correlation
  - scikit-learn
derived_from:
- doi: 10.1371/journal.pcbi.1009021
  title: MiMeNet
evidence_spans:
- MiMeNet (Microbiome-Metabolome Network), a multi-layer perceptron (MLPNN)
- MiMeNet uses paired microbiome and metabolome data for model training. Microbiome abundance features (green) are used to train a neural network to predict metabolite abundance features (blue).
- An MLPNN model is composed of multiple fully connected hidden layers composed of perceptrons
- Canonical correlation analysis models were implemented using Python's scikit-learn package.
- MiMeNet was trained using the ADAM optimizer and the mean squared error (MSE) loss function.
- In MiMeNet, φ is set as the rectified linear unit (ReLU). We selected this activation function since previous studies have shown that it is resilient to the problems of exploding and vanishing
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
---

# Spearman correlation background distribution analysis

## Summary

A statistical validation technique that establishes significance thresholds for metabolite prediction by generating an empirical null distribution through shuffled cross-validation, enabling distinction between genuine metabolite-microbe relationships and random correlations. This skill is essential for determining which metabolites have been predicted with confidence above background noise.

## When to use

Apply this skill after cross-validated neural network or regression models have generated predicted metabolite abundances and you need to distinguish genuinely predictable metabolites from those with spuriously high correlations. Specifically, use when you have paired microbiome-metabolome datasets where not all metabolites are expected to correlate with microbial composition, and you want to avoid inflated performance claims by establishing what correlation magnitude constitutes 'well-predicted' rather than chance agreement.

## When NOT to use

- When the metabolome and microbiome are known to be in near-perfect correspondence (e.g., highly constrained laboratory conditions or synthetic data); background distribution thresholding assumes substantial unmappable variance.
- When sample size is very small (<20 samples) such that 10-fold cross-validation partitions become unreliable and shuffled background distributions become sparse and unstable.
- When metabolites have been pre-filtered to only those with known mechanistic associations to microbes; the method assumes many metabolites are a priori independent of the microbiota.

## Inputs

- Paired microbiome abundance matrix (samples × microbes, after preprocessing/normalization)
- Paired metabolome abundance matrix (samples × metabolites, after preprocessing/normalization)
- Predicted metabolite abundances from trained neural network or regression model(s) across all test folds and cross-validation iterations
- Cross-validation fold assignments (e.g., 10-fold partitions)

## Outputs

- Background SCC distribution (empirical null distribution of Spearman correlation coefficients from shuffled data)
- 95th percentile SCC threshold per dataset (e.g., scalar cutoff value)
- Binary classification of metabolites: well-predicted vs. background-level
- Count and percentage of well-predicted metabolites per dataset
- Mean SCC range per dataset (min → max observed correlation across well-predicted metabolites)

## How to apply

Generate a background distribution by performing 100 iterations of 10-fold cross-validation on independently shuffled microbiome and metabolome samples (shuffling breaks the true association structure while preserving feature distributions). Compute Spearman correlation coefficients (SCCs) between predicted and observed metabolite abundances for each shuffled iteration and fold, collecting all SCC values across the shuffled dataset. Define a significance threshold at the 95th percentile of this background SCC distribution. Classify a metabolite as 'well-predicted' only if its observed-data SCC exceeds this percentile-derived cutoff. This approach yields dataset-specific thresholds (e.g., 0.136 for IBD PRISM, 0.129 for cystic fibrosis, 0.410 for soil) that account for inherent differences in feature dimensionality, sample size, and biological signal strength.

## Related tools

- **SciPy Spearman correlation** (Compute rank-based correlation coefficients between predicted and observed metabolite abundances for both observed and shuffled data) — https://scipy.org
- **NumPy** (Efficient matrix shuffling, percentile calculation, and aggregation of SCC values across cross-validation iterations) — https://numpy.org
- **scikit-learn** (Cross-validation fold generation (KFold) and model training infrastructure for both observed and shuffled datasets) — https://scikit-learn.org
- **MiMeNet** (Reference implementation that generates background distributions via 100 iterations of 10-fold cross-validation on shuffled data and defines well-predicted metabolites at the 95th percentile) — https://github.com/YDaiLab/MiMeNet

## Examples

```
python MiMeNet_train.py -micro data/IBD/microbiome_PRISM.csv -metab data/IBD/metabolome_PRISM.csv -micro_norm None -metab_norm CLR -num_run_cv 10 -num_background 100 -output IBD
```

## Evaluation signals

- Background SCC distribution shape and range should reflect random correlations: for IBD PRISM, CF, and soil datasets respectively, observed mean SCCs should increase substantially from background (0.108→0.309, 0.276→0.457, −0.272→0.264), demonstrating that true signal is distinguishable from noise.
- Well-predicted metabolite counts should be consistent with stated percentile threshold: ~5% of total metabolites would be expected at the 95th percentile if all metabolites were independent; observed counts (6857/8848=77.5% for IBD PRISM, 143/168=94.1% for CF, 29/85=34.1% for soil) indicate varying degrees of microbiome-metabolome coupling, validating the threshold's sensitivity to dataset structure.
- 95th percentile threshold values must be dataset-specific and responsive to feature dimensionality and feature rarity: higher thresholds for sparse datasets (soil: 0.410 with only 85 metabolites) and lower thresholds for metabolome-rich datasets (IBD PRISM: 0.136 with 8848 metabolites) confirms appropriate background calibration.
- Shuffled background SCCs should cluster near zero mean with tight distribution, while observed SCCs for well-predicted metabolites should show clear separation from background: visual inspection of SCC histograms (observed vs. shuffled) should show minimal overlap beyond the 95th percentile cutoff.
- Well-predicted metabolite sets should be reproducible across independent cross-validation runs: metabolites consistently above threshold across 10 iterations of 10-fold CV indicate robust predictions, whereas metabolites fluctuating near the threshold boundary suggest marginal or unstable predictability.

## Limitations

- The 95th percentile threshold is a statistical convenience and does not guarantee biological significance; a metabolite above threshold may still have low absolute correlation (e.g., SCC=0.15) and weak explanatory power for host biology.
- Method assumes that shuffling microbiome and metabolome independently produces a valid null hypothesis; if there are unmeasured confounders (e.g., host genotype, diet, medication) affecting both, the background distribution may not truly represent chance correlation.
- Performance is sensitive to preprocessing choices (CLR transformation, pseudocount, feature filtering at <10% prevalence): different normalization or filtering thresholds will shift both observed SCCs and background distributions, potentially altering metabolite classification.
- Longitudinal or time-series data (e.g., soil dataset with five time-points across successional stages) may inflate background correlations if temporal autocorrelation is not accounted for, leading to higher threshold values and fewer well-predicted metabolites identified.
- Not all metabolites may have microbial sources; the method cannot distinguish metabolites truly decoupled from microbes from those with weak but genuine associations, resulting in lower overall mean correlation across all metabolites.

## Evidence

- [other] Generate background distribution by shuffling microbiome and metabolome samples independently, performing 100 models of 10-fold cross-validation on shuffled data, collecting SCC values for all metabolites.: "Generate background distribution by shuffling microbiome and metabolome samples independently, performing 100 models of 10-fold cross-validation on shuffled data, collecting SCC values for all"
- [other] Define well-predicted metabolites as those with SCC above 95th percentile of background correlations, identifying cutoffs of 0.136 (IBD PRISM), 0.129 (cystic fibrosis), and 0.410 (soil).: "Define well-predicted metabolites as those with SCC above 95th percentile of background correlations, identifying cutoffs of 0.136 (IBD PRISM), 0.129 (cystic fibrosis), and 0.410 (soil)."
- [readme] MiMeNet generates a background of SCC values using a similar approach as in Cross-Validated Evaluation. However, to generate the background distribution of SCCs, the samples are randomly shuffled for each cross-validated iteration.: "MiMeNet generates a background of SCC values using a similar approach. To generate the background distribution of SCCs, the samples are randomly shuffled for each cross-validated iteration."
- [other] Calculate Spearman correlation coefficient (SCC) between predicted and observed metabolite abundances for each metabolite across all test folds and iterations, averaging to obtain mean SCC per metabolite.: "Calculate Spearman correlation coefficient (SCC) between predicted and observed metabolite abundances for each metabolite across all test folds and iterations, averaging to obtain mean SCC per"
- [methods] We then defined a metabolite as well-predicted if its SCC is above the 95th percentile of the background correlations: "We then defined a metabolite as well-predicted if its SCC is above the 95th percentile of the background correlations"
- [discussion] since not all metabolites may be associated with microbes, some metabolites will have lower prediction correlations, which resulted in an overall lower mean correlation across all metabolites: "since not all metabolites may be associated with microbes, some metabolites will have lower prediction correlations, which resulted in an overall lower mean correlation across all metabolites"
