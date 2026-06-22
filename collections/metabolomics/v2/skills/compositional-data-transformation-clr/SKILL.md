---
name: compositional-data-transformation-clr
description: Use when apply CLR transformation when you have microbiome or metabolomic count data that sums to a constant across samples (relative abundance or compositional data) and intend to train supervised or unsupervised machine learning models (especially neural networks) that assume unbounded, linear.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3174
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3697
  tools:
  - ADAM optimizer
  - scikit-learn (Python)
  - MiMeNet
  - scikit-learn
  - TensorFlow / Keras
derived_from:
- doi: 10.1371/journal.pcbi.1009021
  title: MiMeNet
evidence_spans:
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Compositional Data Transformation (CLR)

## Summary

Center log-ratio (CLR) transformation converts compositional microbiome and metabolomic abundance data into a form suitable for neural network training by addressing the constant-sum constraint inherent in relative abundance data. This normalization is essential when modeling microbe-metabolite relationships to prevent spurious correlations and ensure the network learns true ecological associations rather than artifacts of compositional closure.

## When to use

Apply CLR transformation when you have microbiome or metabolomic count data that sums to a constant across samples (relative abundance or compositional data) and intend to train supervised or unsupervised machine learning models (especially neural networks) that assume unbounded, linear relationships between features. Specifically use this when predicting metabolite abundances from microbial features, as raw relative abundances violate the independence assumptions of regression-based methods.

## When NOT to use

- Do not apply CLR if the input data is already log-transformed or normalized (e.g., already in log₂ scale or quantile-normalized) — double transformation will distort relationships.
- Do not apply CLR if the input is not compositional (e.g., RNA-seq counts, absolute cell counts, or non-relative-abundance measurements) — CLR is designed for data constrained to a constant sum.
- Do not apply CLR if you are using constraint-based stoichiometric models (e.g., constraint-based metabolic reconstruction) that explicitly model relative abundances; these methods assume compositional structure rather than transformed linear space.

## Inputs

- Microbiome feature abundance table (samples × microbial features, raw or relative abundance counts)
- Metabolomic feature abundance table (samples × metabolite features, raw or relative abundance counts)

## Outputs

- CLR-transformed microbiome feature table (samples × microbial features, log-scale centered composition)
- CLR-transformed metabolomic feature table (samples × metabolite features, log-scale centered composition)

## How to apply

Add a pseudocount (e.g., 1) to all abundance values to handle zero counts, then divide each feature by the geometric mean of all features in the sample, and take the natural logarithm of the result. In practice: for each sample, compute the geometric mean of all feature abundances (including the pseudocount), then for each feature, compute log(feature_abundance / geometric_mean). Apply this transformation separately to microbiome and metabolome feature tables before downstream modeling. The pseudocount prevents undefined logarithms and stabilizes estimates for rare features. Document which features were transformed and which normalization (CLR vs. relative abundance) was applied to each data type, as this choice affects model interpretation and reproducibility.

## Related tools

- **MiMeNet** (Applies CLR transformation as a preprocessing step before neural network training; user specifies CLR normalization parameter to transform microbiome/metabolome tables) — https://github.com/YDaiLab/MiMeNet
- **scikit-learn** (Provides StandardScaler and other preprocessing utilities compatible with CLR-transformed compositional data)
- **TensorFlow / Keras** (Ingests CLR-transformed feature tables and trains neural network models assuming transformed, unbounded features)

## Examples

```
python MiMeNet_train.py -micro data/IBD/microbiome_PRISM.csv -metab data/IBD/metabolome_PRISM.csv -micro_norm None -metab_norm CLR -net_params results/IBD/network_parameters.txt -output IBD
```

## Evaluation signals

- Verify that all transformed values are real numbers (no NaN or Inf); NaN indicates zero counts without pseudocount or log(0) errors.
- Confirm that each sample's CLR-transformed features sum to zero (within floating-point tolerance ±1e-10); deviation indicates incorrect pseudocount application or geometric mean calculation.
- Check that the distribution of transformed values is approximately centered around zero with no strong skew; systematic deviation suggests pseudocount was too small or too large.
- Compare Spearman correlation coefficients of predicted vs. observed metabolite abundances before and after CLR transformation; CLR should yield higher correlations than untransformed relative abundance (as reported: 0.108→0.309 for IBD, 0.276→0.457 for CF, -0.272→0.264 for Soil).
- Verify that the number of well-predicted metabolites (SCC > 95th percentile of background) increases after CLR transformation relative to non-transformed baselines.

## Limitations

- CLR transformation requires a pseudocount to handle zero abundance values; the choice of pseudocount (default 1 in MiMeNet) is arbitrary and can affect downstream predictions, especially for rare features.
- CLR transformation assumes all features in a sample share the same absolute scale, which may not hold if microbiome and metabolomic data are measured on different instruments or from different biospecimens.
- The constant-sum constraint is relaxed but not eliminated after CLR; features remain linearly dependent, and some downstream methods may still require additional compositional corrections (e.g., principal component analysis on CLR data).
- CLR transformation does not account for different normalization needs across datasets; the article applied CLR with pseudocount 1 except for IBD microbes in relative abundance, indicating dataset-specific decisions are necessary.
- Interpretation of CLR-transformed coefficients is less intuitive than raw abundance or log-fold-change; feature attribution scores derived from CLR-transformed networks reflect log-ratio relationships, not absolute abundance changes.

## Evidence

- [other] Load and preprocess microbiome and metabolomic data from IBD (PRISM), Cystic Fibrosis, and Soil datasets, removing features present in <10% of samples and applying centered log-ratio (CLR) transformation with pseudocount of 1 (except IBD microbes in relative abundance).: "applying centered log-ratio (CLR) transformation with pseudocount of 1 (except IBD microbes in relative abundance)"
- [readme] Transform the microbial features into relative abundance (RA) or center log-ratio (CLR). If the data is already transformed, apply 'None' to skip transformation.: "Transform the microbial features into relative abundance (RA) or center log-ratio (CLR). If the data is already transformed, apply 'None' to skip transformation."
- [readme] MiMeNet will perform a compositional transformation to relative abundance or centered log-ratio and filter low abundant microbial and metabolite features.: "MiMeNet will perform a compositional transformation to relative abundance or centered log-ratio and filter low abundant"
- [abstract] MiMeNet more accurately predicts metabolite abundances (mean Spearman correlation coefficients increase from 0.108 to 0.309, 0.276 to 0.457, and -0.272 to 0.264): "MiMeNet more accurately predicts metabolite abundances (mean Spearman correlation coefficients increase from 0.108 to 0.309, 0.276 to 0.457, and -0.272 to 0.264)"
