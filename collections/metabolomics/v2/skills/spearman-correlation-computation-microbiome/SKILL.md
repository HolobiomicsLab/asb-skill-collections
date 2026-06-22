---
name: spearman-correlation-computation-microbiome
description: 'Use when you have cross-validated predictions of metabolite abundances from a microbiome-metabolome model and need to: (1) measure predictive accuracy at the individual metabolite level; (2) aggregate performance across all metabolites to report mean SCC;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3697
  - http://edamontology.org/topic_3174
  - http://edamontology.org/topic_0602
  tools:
  - MiMeNet
  - MelonnPan
  - Elastic Net
  - NED
  - scikit-learn
  - Python
  - TensorFlow
  - scipy
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Spearman Correlation Computation for Microbiome-Metabolome Prediction

## Summary

Compute Spearman correlation coefficients (SCCs) between predicted and observed metabolite abundances to quantify prediction accuracy in microbiome-metabolome models. This metric is used to identify well-predicted metabolites and compare the predictive performance of competing methods across paired microbiome and metabolomic datasets.

## When to use

Apply this skill when you have cross-validated predictions of metabolite abundances from a microbiome-metabolome model and need to: (1) measure predictive accuracy at the individual metabolite level; (2) aggregate performance across all metabolites to report mean SCC; (3) generate a distribution of SCCs under a null model (shuffled data) to establish a significance threshold; or (4) compare the performance of multiple competing prediction methods (e.g., MiMeNet vs. MelonnPan) on the same dataset.

## When NOT to use

- When the metabolite or microbiome data has not been normalized (e.g., still in raw counts); apply centered log-ratio or relative abundance transformation first.
- When comparing predictions across datasets with very different distributions (e.g., IBD cohort vs. soil samples) without first checking that the background distribution threshold is computed independently for each dataset.
- When metabolite abundances are binary or categorical rather than continuous; Spearman correlation assumes ranked or continuous data.
- When sample sizes are very small (<20 samples per fold), as SCC estimates become unstable and the background distribution may not be robust.

## Inputs

- Predicted metabolite abundance matrix (samples × metabolites, from cross-validated model predictions)
- Observed metabolite abundance matrix (samples × metabolites, ground truth from test set)
- Microbiome abundance matrix (samples × microbial features, for null model shuffling)
- Metabolomic abundance matrix (samples × metabolites, for null model shuffling)

## Outputs

- Per-metabolite Spearman correlation coefficients (vector or table)
- Mean SCC across all metabolites (scalar summary statistic)
- Background distribution of SCCs from shuffled null model (vector of length = num_background × num_cv)
- 95th percentile SCC threshold for well-predicted metabolites (scalar)
- Count of well-predicted metabolites (scalar)
- Metabolite prediction quality table (metabolite ID, SCC, significance flag)

## How to apply

For each metabolite in the test set, compute the Spearman rank correlation coefficient between its predicted abundance (from cross-validated model output) and its observed abundance (ground truth). Aggregate these per-metabolite SCCs by taking the mean across all metabolites to obtain a dataset-level performance summary. To establish a significance cutoff, generate a background distribution by shuffling the microbiome and metabolomic samples independently, performing the same cross-validated prediction and SCC computation on the shuffled data across multiple iterations (e.g., 100 times), then defining the 95th percentile of this null distribution as the threshold for 'well-predicted' metabolites. Metabolites with SCC ≥ this threshold are retained for downstream analysis (network analysis, module detection, biomarker discovery); those below are considered poorly predicted and may reflect metabolites not mechanistically linked to the microbiome or features with low signal-to-noise. Report both the count of well-predicted metabolites and the mean SCC across all metabolites to fully characterize model performance.

## Related tools

- **MiMeNet** (Neural network model that generates predicted metabolite abundances; SCC is used to evaluate its cross-validated predictions) — https://github.com/YDaiLab/MiMeNet
- **MelonnPan** (Elastic Net-based baseline method whose predictions are compared to MiMeNet using SCC as the performance metric) — https://github.com/biobakery/melonnpan
- **scikit-learn** (Python library providing scipy.stats.spearmanr for computing Spearman correlation coefficients)
- **scipy** (Python library with scipy.stats.spearmanr function for rank correlation computation)

## Examples

```
from scipy.stats import spearmanr; import numpy as np; scc_per_metabolite = [spearmanr(predicted[:, i], observed[:, i])[0] for i in range(predicted.shape[1])]; mean_scc = np.mean(scc_per_metabolite); well_predicted = np.sum(np.array(scc_per_metabolite) >= 0.136)
```

## Evaluation signals

- Mean SCC should increase relative to the null model (shuffled background); if mean SCC ≈ mean of background distribution, the model has no predictive power.
- The count of well-predicted metabolites (SCC ≥ 95th percentile threshold) should be substantially greater than the count expected by random chance (e.g., ~5% of total metabolites if threshold is set at 95th percentile of a uniform null distribution).
- The 95th percentile threshold computed from the background distribution should be notably lower than the observed SCCs for well-predicted metabolites; thresholds for IBD (PRISM) typically range 0.13–0.14, while well-predicted metabolites often have SCC > 0.3.
- When comparing two methods (e.g., MiMeNet vs. MelonnPan), the method with higher mean SCC and larger count of well-predicted metabolites should be reproducible across multiple cross-validation runs; report 95% confidence intervals or standard deviations.
- SCC distributions should be approximately normal or at least unimodal when plotted; bimodal or heavily skewed distributions may indicate data quality issues or the presence of two populations of metabolites with very different predictability.

## Limitations

- Not all metabolites may be mechanistically associated with the microbiome, so some metabolites will have lower prediction correlations by design; this results in an overall lower mean SCC across all metabolites and should not be interpreted as model failure.
- The 95th percentile threshold is dataset-specific and must be recomputed for each new dataset using its own shuffled background distribution; thresholds computed from one dataset (e.g., IBD PRISM) cannot be directly applied to another (e.g., soil biocrust).
- SCC is sensitive to outliers in the predicted or observed abundance values; data with extreme values or measurement errors can inflate or deflate correlations; centered log-ratio or other compositional transformations should be applied before computing SCC.
- Small sample sizes (N < 20) lead to unstable SCC estimates; confidence intervals widen and rank-based correlation becomes less reliable.
- The computational cost of generating the background distribution (multiple iterations of shuffling + cross-validation) scales linearly with the number of samples and metabolites; for very large datasets, subsampling or parallel computation may be needed.

## Evidence

- [results] the predictive performance of a model is measured by the average Spearman correlation coefficients (SCCs) between the predicted and the observed abundance of the metabolites: "the predictive performance of a model is measured by the average Spearman correlation coefficients (SCCs) between the predicted and the observed abundance of the metabolites"
- [results] MiMeNet then generates a background distribution of SCCs through multiple iterations of shuffling the dataset and performing a cross-validated evaluation on the shuffled set: "MiMeNet then generates a background distribution of SCCs through multiple iterations of shuffling the dataset and performing a cross-validated evaluation on the shuffled set"
- [methods] We then defined a metabolite as well-predicted if its SCC is above the 95th percentile of the background correlations: "We then defined a metabolite as well-predicted if its SCC is above the 95th percentile of the background correlations"
- [results] the cutoffs for SCCs between the predicted and observed abundances of metabolites were found to be 0.136, 0.129, and 0.410 for the IBD (PRISM), cystic fibrosis, and soil datasets, respectively: "the cutoffs for SCCs between the predicted and observed abundances of metabolites were found to be 0.136, 0.129, and 0.410 for the IBD (PRISM), cystic fibrosis, and soil datasets, respectively"
- [other] MiMeNet identified 351 well-predicted metabolites from 8848 total metabolites, whereas MelonnPan identified 198 well-predicted metabolites using the same correlation cutoff of 0.3: "MiMeNet identified 351 well-predicted metabolites from 8848 total metabolites, whereas MelonnPan identified 198 well-predicted metabolites using the same correlation cutoff of 0.3"
- [discussion] since not all metabolites may be associated with microbes, some metabolites will have lower prediction correlations, which resulted in an overall lower mean correlation across all metabolites: "since not all metabolites may be associated with microbes, some metabolites will have lower prediction correlations, which resulted in an overall lower mean correlation across all metabolites"
