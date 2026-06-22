---
name: centered-log-ratio-normalization
description: Use when apply CLR normalization when you have count-based microbiome or metabolome compositional data (e.g., 16S rRNA gene abundances, LC-MS/MS metabolite abundances) that will be used as input to multivariate predictive models (neural networks, regression, correlation analysis).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3697
  - http://edamontology.org/topic_3174
  - http://edamontology.org/topic_0637
  tools:
  - Elastic Net
  - MiMeNet
  - TensorFlow or PyTorch
  - scikit-learn
  - Seaborn
  - Python
  - scikit-learn (MLPRegressor)
  - ADAM optimizer
  - ReLU activation
  - NumPy
  - SciPy
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

# centered-log-ratio-normalization

## Summary

Centered log-ratio (CLR) transformation is a compositional data normalization method that accounts for the constrained sum structure of microbiome count data by log-transforming the ratio of each feature to the geometric mean of all features. Applied as a preprocessing step before multivariate modeling of microbiome-metabolome relationships, CLR normalization improves prediction accuracy and correlation detection compared to relative abundance transformation, particularly in datasets with high feature counts.

## When to use

Apply CLR normalization when you have count-based microbiome or metabolome compositional data (e.g., 16S rRNA gene abundances, LC-MS/MS metabolite abundances) that will be used as input to multivariate predictive models (neural networks, regression, correlation analysis). CLR is particularly beneficial when comparing across multiple datasets or when feature correlations need to be preserved; the IBD (PRISM), cystic fibrosis, and soil datasets all showed improved mean Spearman correlations or well-predicted metabolite counts with CLR versus relative abundance, especially in datasets with larger metabolite feature spaces (8848 vs 168 metabolites).

## When NOT to use

- Data is already normalized or transformed (e.g., already relative abundance, already log-transformed, already z-scored). CLR should be applied to raw counts, not post-hoc to normalized data.
- Feature presence-absence (binary) data or already-aggregated ratios are the input. CLR requires actual count magnitudes to compute meaningful geometric means.
- Downstream analysis explicitly requires relative abundance interpretation (e.g., taxonomic composition plots, biomass-normalized statistics). CLR changes the scale to centered log space, which is less interpretable in those contexts.

## Inputs

- count matrix (samples × features) of microbiome taxa or metabolite abundances
- feature pseudocount offset (typically +1)
- geometric mean calculation method (typically log-space mean of all features per sample)

## Outputs

- CLR-transformed numeric matrix (samples × features), same dimensions as input
- centered log-ratio values (mean = 0 across features per sample)
- feature-to-geometric-mean ratio matrix (optional, for inspection)

## How to apply

Add a pseudocount (+1) to all count values to avoid log(0) errors. For each sample, calculate the geometric mean across all features. Then, for each feature, take the natural log of the feature count divided by the geometric mean. The result is a centered, log-scale matrix where feature sums are constrained to zero. This transformation preserves compositional relationships while enabling use of standard multivariate statistical methods that assume additive structure. Apply CLR before train-test splitting or cross-validation, using the same pseudocount and geometric mean calculation for all samples in the analysis. When comparing CLR to relative abundance transformations on the same data, note that CLR consistently produced higher prediction correlations (e.g., 0.309 vs ~0.108 baseline on IBD PRISM) and increased counts of well-predicted metabolites (6857 of 8848 vs 198 of 8848 on IBD PRISM).

## Related tools

- **MiMeNet** (Neural network framework that accepts CLR-normalized microbiome and metabolome matrices as input for microbe-metabolite prediction and module inference) — https://github.com/YDaiLab/MiMeNet
- **scikit-learn** (Used for MLPRegressor and general linear regression after CLR normalization)
- **SciPy** (Provides log and geometric mean functions for CLR calculation; also computes Spearman correlation on CLR-transformed outputs)
- **NumPy** (Efficient matrix operations for pseudocount addition, geometric mean computation, and element-wise log transformation)

## Examples

```
python MiMeNet_train.py -micro data/IBD/microbiome_PRISM.csv -metab data/IBD/metabolome_PRISM.csv -micro_norm None -metab_norm CLR -num_run_cv 10 -output IBD
```

## Evaluation signals

- CLR matrix sums to zero (or near-zero within numerical precision) across features within each sample; validate by computing row sums and confirming they are close to 0.
- Comparison of prediction performance (mean Spearman correlation coefficient) between CLR-normalized and relative-abundance-normalized inputs on the same dataset should show equal or improved performance for CLR; on IBD (PRISM) dataset, expect mean SCC ~0.309 with CLR vs. ~0.108 baseline.
- Well-predicted metabolite counts (metabolites above 95th percentile of background correlation distribution) should be equal or higher under CLR; on IBD (PRISM), CLR-based predictions identified 6857 well-predicted metabolites vs. 198 at baseline.
- Feature attribution score matrices derived from CLR-trained models should yield stable, interpretable microbe-metabolite modules when biclustered; cluster robustness can be evaluated by consensus clustering k* selection using area-under-CDF with Δk threshold.
- Visualization of module-level features (e.g., boxplots of normalized CLR module scores stratified by phenotype) should show enriched distributions for known phenotype-associated taxa/metabolites and validate against external cohort predictions (e.g., external IBD cohort AUC).

## Limitations

- CLR assumes all features are measured in the same units and from the same compositional pool. Combining data from different platforms (e.g., 16S and WGS, or different metabolomics methods) requires careful batch correction before CLR.
- CLR is sensitive to rare or zero-inflated features; pseudocount choice (typically +1) can affect results on very sparse datasets. The article uses pseudocount +1 uniformly but does not explore sensitivity to this parameter.
- CLR transformation loses information about absolute microbial or metabolite abundances; it is only meaningful for relative comparisons within samples. Interpretation of CLR coefficients does not directly translate back to fold-change in absolute concentration.
- Higher threshold for well-predicted metabolites was observed in soil dataset (0.410 vs. 0.136 for IBD), which the authors attribute to longitudinal structure; CLR may not fully account for temporal dependencies or repeated measures in microbiome time series.
- CLR does not handle missing data or features that are entirely absent in some samples; features must be present in ≥10% of samples prior to CLR transformation (as applied in the MiMeNet pipeline).

## Evidence

- [methods] centered log-ratio (CLR) transformation with pseudocount +1: "centered log-ratio (CLR) transformation with pseudocount +1"
- [other] In the IBD (PRISM) dataset, prediction correlations were comparable between CLR and relative abundance transformations, while CLR showed increased correlations in cystic fibrosis and soil datasets.: "In the IBD (PRISM) dataset, prediction correlations were comparable between CLR and relative abundance transformations, while CLR showed increased correlations in cystic fibrosis and soil datasets."
- [other] For each transformation, train MiMeNet... 3. Prepare two parallel input transformations: centered log-ratio (CLR) transformation with pseudocount +1, and relative abundance (RA) normalization.: "Prepare two parallel input transformations: centered log-ratio (CLR) transformation with pseudocount +1, and relative abundance (RA) normalization."
- [abstract] MiMeNet more accurately predicts metabolite abundances (mean Spearman correlation coefficients increase from 0.108 to 0.309, 0.276 to 0.457, and -0.272 to 0.264): "MiMeNet more accurately predicts metabolite abundances (mean Spearman correlation coefficients increase from 0.108 to 0.309, 0.276 to 0.457, and -0.272 to 0.264)"
- [readme] Transform the microbial features into relative abundance (RA) or center log-ratio (CLR). If the data is already transformed, apply 'None' to skip transformation.: "Transform the microbial features into relative abundance (RA) or center log-ratio (CLR). If the data is already transformed, apply 'None' to skip transformation."
