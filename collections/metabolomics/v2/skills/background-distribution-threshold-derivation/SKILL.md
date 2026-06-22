---
name: background-distribution-threshold-derivation
description: Use when when you have trained predictive models (e.g., neural networks) on paired microbiome-metabolome data and need to identify which metabolites are genuinely well-predicted above chance.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_3174
  - http://edamontology.org/topic_3697
  - http://edamontology.org/topic_0622
  tools:
  - Elastic Net
  - MiMeNet
  - TensorFlow or PyTorch
  - scikit-learn
  - Seaborn
  - Python
  - scipy
  - NumPy
  techniques:
  - LC-MS
derived_from:
- doi: 10.1371/journal.pcbi.1009021
  title: MiMeNet
evidence_spans:
- we benchmarked MiMeNet against other general regression models, i.e., Random Forest (RF), multivariate Elastic Net, and canonical correlation analysis (CCA) models
- MiMeNet (Microbiome-Metabolome Network), a multi-layer perceptron (MLPNN)
- MiMeNet uses paired microbiome and metabolome data for model training. Microbiome abundance features (green) are used to train a neural network to predict metabolite abundance features (blue).
- MiMeNet was trained using the ADAM optimizer and the mean squared error (MSE) loss function
- MiMeNet was trained using the ADAM optimizer and the mean squared error (MSE) loss function.
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

# Background-Distribution Threshold Derivation

## Summary

Derive empirical significance thresholds for metabolite prediction quality by generating null distributions through repeated shuffling and cross-validation, then define well-predicted metabolites at a high percentile (e.g., 95th) of the background distribution. This guards against false discoveries and enables data-driven cutoff selection without prior assumptions.

## When to use

When you have trained predictive models (e.g., neural networks) on paired microbiome-metabolome data and need to identify which metabolites are genuinely well-predicted above chance. Use this skill when: (1) you want to distinguish signal from noise in high-dimensional prediction tasks, (2) your prediction metric (e.g., Spearman correlation) varies naturally across metabolites, and (3) you lack external biological validation or literature cutoffs. It is particularly valuable for metabolomic and metagenomic studies where most features may be weakly associated with the microbiome.

## When NOT to use

- You already have validated external test sets or literature-based cutoffs for your metabolites; threshold derivation is most useful when such references are unavailable.
- Your prediction metric is already corrected for multiple testing (e.g., FDR-adjusted p-values); background shuffling adds redundant conservatism.
- Your datasets are very small (n < 20 samples); the null distribution may be unstable and the 95th percentile unreliable.

## Inputs

- Paired microbiome (16S rRNA or metagenomic) and metabolome (LC-MS/MS or similar) feature tables (samples × features)
- Trained predictive models from cross-validated training on real data
- Prediction quality metrics (Spearman correlation coefficients per metabolite) from real cross-validation
- Sample size and feature filtering parameters (e.g., minimum prevalence threshold)

## Outputs

- Empirical background distribution of prediction metrics (e.g., list of SCC values from shuffled CV runs)
- Percentile-based significance threshold (e.g., 95th percentile SCC value)
- Binary classification of metabolites as well-predicted vs. not well-predicted
- Well-predicted metabolite counts and sets for downstream module construction and validation

## How to apply

Train your predictive model on the real data using cross-validation (e.g., 10 iterations of 10-fold CV), recording a prediction quality metric (Spearman correlation coefficient) for each metabolite. Then independently shuffle the microbiome and metabolome sample labels while keeping feature counts intact, re-train the model on shuffled data using the same cross-validation scheme, and record the same metric. Repeat this shuffling procedure for many iterations (e.g., 100 background iterations) to build an empirical null distribution of metrics. Finally, compute the 95th percentile of this background distribution and use it as the cutoff: metabolites with real-data metrics above this threshold are designated well-predicted. This approach controls for multiple testing and dataset-specific noise structure without assuming a parametric distribution.

## Related tools

- **MiMeNet** (End-to-end workflow that trains neural network models on paired microbiome-metabolome data and implements background-distribution threshold derivation for well-predicted metabolite identification) — https://github.com/YDaiLab/MiMeNet
- **scikit-learn** (Provides cross-validation splitting (KFold) and model evaluation utilities used in threshold derivation)
- **scipy** (Computes Spearman correlation coefficients (scipy.stats.spearmanr) for prediction quality metrics)
- **NumPy** (Enables efficient shuffling and percentile computation on background distribution arrays)

## Examples

```
python MiMeNet_train.py -micro data/IBD/microbiome_PRISM.csv -metab data/IBD/metabolome_PRISM.csv -micro_norm None -metab_norm CLR -num_run_cv 10 -num_background 100 -threshold 0.95 -output IBD
```

## Evaluation signals

- Background distribution shape and stability: histograms of shuffled metrics should be unimodal and centered near zero (for unassociated features); verify that increasing num_background iterations does not substantially shift the percentile threshold (convergence check).
- Percentile cutoff is higher than the median background metric but lower than the maximum; for IBD (PRISM) data, the 95th percentile SCC threshold should be approximately 0.136 (a concrete reference value).
- Well-predicted metabolite count is substantially smaller than total metabolites; the skill correctly filters the majority of weakly-associated features (e.g., 366 well-predicted out of 8848 metabolites in IBD PRISM).
- Real-data prediction metrics are right-shifted relative to background distribution; visual inspection (histogram overlay) should show clear separation between the two, confirming that real associations exceed chance.
- Downstream analyses (e.g., module enrichment, classifier performance) using well-predicted metabolites show statistical significance (e.g., Wilcoxon p < 0.05 for module enrichment) and biological interpretability; poor threshold derivation will either retain too much noise or lose signal.

## Limitations

- Threshold robustness depends on sample size; small datasets (n < 20) may produce unstable null distributions and unreliable percentile estimates.
- The 95th percentile cutoff is arbitrary and dataset-specific; longitudinal or time-series data (e.g., soil biocrust samples) may require higher thresholds due to natural autocorrelation, as observed in the MiMeNet soil cohort (threshold 0.410 vs. 0.136 for IBD PRISM).
- Shuffling assumes that metabolites are independent of the microbiome under the null; if true biological structure exists at very weak effect sizes, shuffling may overestimate the null and reject genuinely weak but meaningful metabolites.
- The method does not account for metabolite measurement quality or annotation confidence; poorly annotated or noisy metabolite features may have artificially high or low background metrics.
- Computational cost scales with num_background iterations (100+ recommended); generating null distributions for large metabolite sets (8000+) can be slow without parallel processing.

## Evidence

- [results] MiMeNet then generates a background distribution of SCCs through multiple iterations of shuffling the dataset and performing a cross-validated evaluation on the shuffled set: "generates a background distribution of SCCs through multiple iterations of shuffling the dataset and performing a cross-validated evaluation on the shuffled set"
- [results] This background distribution of SCCs is then used to determine a cutoff for significantly well-predicted metabolites: "This background distribution of SCCs is then used to determine a cutoff for significantly well-predicted metabolites"
- [methods] We then defined a metabolite as well-predicted if its SCC is above the 95th percentile of the background correlations: "We then defined a metabolite as well-predicted if its SCC is above the 95th percentile of the background correlations"
- [results] the cutoffs for SCCs between the predicted and observed abundances of metabolites were found to be 0.136, 0.129, and 0.410 for the IBD (PRISM), cystic fibrosis, and soil datasets, respectively: "the cutoffs for SCCs between the predicted and observed abundances of metabolites were found to be 0.136, 0.129, and 0.410 for the IBD (PRISM), cystic fibrosis, and soil datasets, respectively"
- [readme] MiMeNet generates a background of SCC values using a similar approach as in Cross-Validated Evaluation. However, to generate the background distribution of SCCs, the samples are randomly shuffled for each cross-validated iteration.: "MiMeNet generates a background of SCC values using a similar approach as in Cross-Validated Evaluation. However, to generate the background distribution of SCCs, the samples are randomly shuffled for"
- [discussion] We also observed a higher threshold value for the soil data (Fig 3A–3C), which may be due to the longitudinal observations.: "We also observed a higher threshold value for the soil data (Fig 3A–3C), which may be due to the longitudinal observations."
