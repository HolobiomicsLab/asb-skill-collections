---
name: percentile-threshold-determination-scc
description: 'Use when when you have paired microbiome and metabolome data and need to identify which metabolites are significantly well-predicted by microbes, but the relationship between prediction accuracy and biological relevance is unknown or varies across datasets (e.g., IBD PRISM: 0.136;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3174
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3336
  tools:
  - MiMeNet
  - MelonnPan
  - Elastic Net
  - NED
  - scikit-learn
  - Python
  - TensorFlow
  - SciPy
  - TensorFlow / Keras
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
---

# Percentile-Threshold Determination for Spearman Correlation Coefficients

## Summary

Establishes a data-driven statistical cutoff for identifying well-predicted metabolites by computing the empirical 95th percentile of Spearman correlation coefficients (SCC) from a background distribution of shuffled microbiome-metabolome pairs. This threshold allows separation of genuinely predictive features from noise across heterogeneous datasets.

## When to use

When you have paired microbiome and metabolome data and need to identify which metabolites are significantly well-predicted by microbes, but the relationship between prediction accuracy and biological relevance is unknown or varies across datasets (e.g., IBD PRISM: 0.136; cystic fibrosis: 0.129; soil biocrust: 0.410). Use this skill when domain-specific thresholds are unavailable and you want a principled, dataset-adaptive cutoff.

## When NOT to use

- Input data is already pre-filtered by a fixed correlation threshold (e.g., |r| > 0.3) — percentile determination assumes you are working with the full, unfiltered prediction output.
- You have fewer than ~50 samples in your cohort, as the cross-validation folds and shuffling iterations may not generate stable null distributions.
- Metabolites have been pre-selected or annotated as 'biologically important' via independent means; percentile thresholding is hypothesis-free and may conflict with prior knowledge.

## Inputs

- Paired microbiome abundance table (samples × microbial features, centered log-ratio or relative abundance transformed)
- Paired metabolome abundance table (samples × metabolite features, centered log-ratio or relative abundance transformed, features present in <10% of samples removed)
- Trained predictive model or model training pipeline (MiMeNet or equivalent) with cross-validation framework
- Shuffled microbiome-metabolome sample pairs (100 iterations recommended)

## Outputs

- 95th percentile SCC threshold value (scalar, e.g., 0.136 for IBD PRISM dataset)
- List of well-predicted metabolites (binary classification: SCC ≥ threshold vs. SCC < threshold)
- Count of well-predicted metabolites (e.g., 351 for IBD PRISM using MiMeNet)
- Background SCC distribution (vector of null correlations for quality control and visualization)

## How to apply

First, train your predictive model (e.g., MiMeNet, MelonnPan) on the observed paired data using k-fold cross-validation, recording Spearman correlation coefficients for each metabolite. Next, generate an empirical null distribution by shuffling samples in both the microbiome and metabolome independently (typically 100 iterations recommended in literature), re-training and evaluating the model on the shuffled data each time to accumulate SCCs under the null hypothesis. Finally, compute the 95th percentile of this null SCC distribution as your significance threshold; metabolites with observed SCC ≥ this percentile are classified as well-predicted. The rationale is that this approach accounts for dataset-specific noise structure and model characteristics without assuming a fixed cutoff, ensuring reproducibility across different environments and sample sizes.

## Related tools

- **MiMeNet** (Multilayer perceptron neural network that predicts metabolite abundances from microbiome data; training loop generates SCC values for threshold computation) — https://github.com/YDaiLab/MiMeNet
- **MelonnPan** (Elastic Net linear regression baseline for metabolite prediction; alternative model architecture for generating SCC distribution) — https://github.com/biobakery/melonnpan
- **scikit-learn** (Provides cross-validation folds (e.g., KFold) and statistical utilities for shuffling and percentile calculation)
- **SciPy** (Computes Spearman correlation coefficients (scipy.stats.spearmanr) and percentile functions (numpy.percentile))
- **TensorFlow / Keras** (Neural network training backend for MiMeNet cross-validation loops that generate SCC values)

## Examples

```
# After training MiMeNet on IBD PRISM data with 10-fold CV, shuffle samples 100 times and compute 95th percentile threshold:
threshold_95 = np.percentile(background_scc_array, 95)
well_predicted = metabolites[observed_scc >= threshold_95]
print(f'Threshold: {threshold_95:.3f}, Well-predicted metabolites: {len(well_predicted)}')
```

## Evaluation signals

- The 95th percentile threshold must be computed from shuffled data, not observed data; verify that background distribution SCC values are substantially lower than observed SCC values for true biological signals.
- Count of well-predicted metabolites should show a substantial increase when comparing observed predictions to shuffle baseline (e.g., 351 vs. ~0 expected by chance on IBD PRISM).
- The threshold value should be dataset-specific and reflect biological signal-to-noise ratio; compare thresholds across datasets (IBD: 0.136, CF: 0.129, soil: 0.410) and confirm that soil's higher threshold correlates with longitudinal structure noted in the paper.
- Well-predicted metabolites identified at the 95th percentile cutoff should show stable functional annotation clustering and enrichment for biological pathways when subjected to downstream module analysis (biclustering and network construction).
- External validation cohort should show similar SCC distributions and well-predicted metabolite counts when applying the same threshold derived from the training cohort, confirming generalization.

## Limitations

- Threshold derivation assumes that shuffling samples breaks microbe-metabolite associations while preserving marginal distributions; this may fail if compositional confounders or batch effects dominate.
- The 95th percentile is a fixed statistical choice; datasets with very weak overall predictive signal (e.g., few metabolites genuinely associated with microbes) may yield thresholds too stringent or lenient for biological interpretation.
- Longitudinal or temporally correlated samples (e.g., soil biocrust data) violate the independence assumption of random shuffling, potentially inflating null SCCs and raising the threshold artificially; the paper notes this phenomenon but does not fully explain the mechanistic impact.
- Not all metabolites are necessarily associated with microbes; prediction correlations for microbe-independent metabolites will cluster near zero, diluting the overall mean correlation and lowering the percentile threshold relative to the subset of truly associated compounds.
- The method is sensitive to data normalization (centered log-ratio vs. relative abundance) and feature filtering (removal of <10% prevalence features); applying different preprocessing pipelines will alter the background distribution and threshold.

## Evidence

- [other] Generate background distribution by shuffling samples in both microbiome and metabolome 100 times and performing cross-validated evaluation; calculate 95th percentile SCC threshold: "Generate background distribution by shuffling samples in both microbiome and metabolome 100 times and performing cross-validated evaluation; calculate 95th percentile SCC threshold (0.136 for IBD"
- [results] MiMeNet then generates a background distribution of SCCs through multiple iterations of shuffling the dataset and performing a cross-validated evaluation on the shuffled set: "MiMeNet then generates a background distribution of SCCs through multiple iterations of shuffling the dataset and performing a cross-validated evaluation on the shuffled set"
- [results] This background distribution of SCCs is then used to determine a cutoff for significantly well-predicted metabolites: "This background distribution of SCCs is then used to determine a cutoff for significantly well-predicted metabolites"
- [methods] We defined a metabolite as well-predicted if its SCC is above the 95th percentile of the background correlations: "We defined a metabolite as well-predicted if its SCC is above the 95th percentile of the background correlations"
- [results] the cutoffs for SCCs between the predicted and observed abundances of metabolites were found to be 0.136, 0.129, and 0.410 for the IBD (PRISM), cystic fibrosis, and soil datasets, respectively: "the cutoffs for SCCs between the predicted and observed abundances of metabolites were found to be 0.136, 0.129, and 0.410 for the IBD (PRISM), cystic fibrosis, and soil datasets, respectively"
- [discussion] We also observed a higher threshold value for the soil data (Fig 3A–3C), which may be due to the longitudinal observations.: "We also observed a higher threshold value for the soil data (Fig 3A–3C), which may be due to the longitudinal observations."
