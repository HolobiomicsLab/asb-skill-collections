---
name: transformation-method-comparison
description: Use when when you have paired microbiome (16S rRNA or functional) and metabolome (LC-MS/MS or similar) data and must decide between compositional transformations (CLR, RA, or others) before training a predictive model.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3174
  - http://edamontology.org/topic_3697
  - http://edamontology.org/topic_0621
  - http://edamontology.org/topic_0091
  tools:
  - Elastic Net
  - MiMeNet
  - TensorFlow or PyTorch
  - scikit-learn
  - Seaborn
  - Python
  - TensorFlow
  - SciPy
  - Seaborn / Matplotlib
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
---

# transformation-method-comparison

## Summary

Compare predictive performance and metabolite recovery between alternative data transformations (e.g., centered log-ratio vs. relative abundance) on paired microbiome-metabolome datasets to assess whether transformation choice materially affects downstream model performance and biological findings.

## When to use

When you have paired microbiome (16S rRNA or functional) and metabolome (LC-MS/MS or similar) data and must decide between compositional transformations (CLR, RA, or others) before training a predictive model. Use this skill when transformation choice could affect: (1) the count or identity of well-predicted metabolites, (2) predictive correlation distributions, (3) module membership, or (4) biomarker discovery outcomes. This is especially important in disease-associated cohorts where transformation could bias clinical inference.

## When NOT to use

- Input is already a derived feature table (e.g., KEGG pathway relative abundances or pre-clustered OTU abundance). Transformation comparison is most informative on raw taxonomic or functional profiles.
- Single dataset or single cohort only. The skill's value is strongest when consistency of transformation effects is assessed across independent datasets (IBD-PRISM vs. cystic fibrosis vs. soil in the source work).
- Metabolome data are already log-transformed or z-scored. This skill assumes raw or intensity-normalized metabolomic input; prior transformations may obscure the effect of the compositional transformation being tested.

## Inputs

- paired microbiome abundance table (samples × microbial features; count or rarefied)
- paired metabolome abundance table (samples × metabolite features; raw or intensity-normalized)
- sample metadata (disease labels, cohort membership, or other covariates)
- network hyperparameters (layer size, L2 penalty λ, dropout rate, early stopping patience)

## Outputs

- well-predicted metabolite sets (95th percentile SCC threshold) for each transformation
- Spearman correlation coefficient distributions (mean, SD, range) per transformation
- count comparison table (e.g., CLR: 366 vs. RA: 198 well-predicted metabolites)
- background SCC distributions from shuffled data (null model)
- feature attribution score matrices (microbe–metabolite interactions) per transformation
- microbial and metabolite consensus-clustered modules per transformation
- downstream prediction performance metrics (e.g., AUC) per transformation
- statistical comparison summary (magnitude of improvement, consistency across datasets)

## How to apply

Prepare two or more parallel input pipelines using different transformations (e.g., centered log-ratio with pseudocount +1 vs. relative abundance normalization). For each transformation, train the same predictive model (MiMeNet or alternative) using identical cross-validation folds (10 iterations of 10-fold CV recommended), identical hyperparameters (layer size, L2 regularization, dropout, early stopping patience), and identical feature filtering (e.g., remove features in <10% of samples). Generate empirical background distributions by shuffling microbiome and metabolome samples independently and retraining 100 models per condition to establish null Spearman correlation coefficients (SCC). Define well-predicted metabolites at the 95th percentile of background SCC for each transformation separately. Compare: (1) count of well-predicted metabolites between conditions, (2) mean and variance of prediction correlations, (3) module composition and size via consensus clustering, and (4) downstream classification performance (e.g., AUC for disease prediction). Report the magnitude of improvement and whether differences are consistent across independent datasets (internal validation set, external cohorts, or different body sites).

## Related tools

- **MiMeNet** (Multi-layer perceptron neural network for training parallel predictive models under different transformations and deriving feature attribution scores for module construction) — https://github.com/YDaiLab/MiMeNet
- **TensorFlow** (Deep learning framework for implementing MiMeNet neural network training and inference)
- **scikit-learn** (Provides consensus clustering, cross-validation utilities, and background shuffling infrastructure)
- **SciPy** (Spearman rank correlation (scipy.stats.spearmanr) for measuring prediction quality)
- **Seaborn / Matplotlib** (Visualization of SCC distributions, well-predicted metabolite counts, and module comparisons across transformations)

## Examples

```
python MiMeNet_train.py -micro data/IBD/microbiome_PRISM.csv -metab data/IBD/metabolome_PRISM.csv -micro_norm CLR -metab_norm None -net_params results/IBD/network_parameters.txt -num_run_cv 10 -output results/IBD_CLR && python MiMeNet_train.py -micro data/IBD/microbiome_PRISM.csv -metab data/IBD/metabolome_PRISM.csv -micro_norm RA -metab_norm None -net_params results/IBD/network_parameters.txt -num_run_cv 10 -output results/IBD_RA
```

## Evaluation signals

- Background SCC distributions are reproducible and symmetric around zero for shuffled data; cutoff thresholds (95th percentile) are substantially higher than median background SCC in observed data, confirming statistical significance.
- Well-predicted metabolite counts differ between transformations and the direction of improvement (if any) is consistent within the same dataset but may vary across datasets (e.g., CLR > RA in cystic fibrosis and soil; comparable in IBD-PRISM), as documented in the source article.
- Cross-validation procedure is identical across transformations: same folds, same model architecture, same hyperparameters, and same feature filtering thresholds (e.g., <10% presence removal). Differences in counts/correlations are attributable to transformation only.
- Module membership and enrichment are reproducibly derived via the same consensus clustering algorithm and threshold (e.g., Δk=0.025) for each transformation; modules with significant enrichment (Wilcoxon p<0.05) are comparable or show systematic differences that can be traced to transformation-induced changes in feature attribution scores.
- Downstream classification performance (e.g., binary IBD classifier AUC) is evaluated on held-out samples using module feature values; AUC values are reported with confidence intervals or standard deviations across 100 iterations, and the magnitude of improvement between transformations is quantified.

## Limitations

- Transformation effects are context-dependent: CLR showed comparable performance to RA in IBD-PRISM but improved performance in cystic fibrosis and soil datasets. No universal recommendation emerges; dataset-specific benchmarking is necessary.
- Not all metabolites associate with microbes; some metabolites will have low prediction correlations regardless of transformation, leading to an overall lower mean correlation across all metabolites and inflating the well-predicted metabolite threshold cutoff.
- Longitudinal observations in time-series data (e.g., soil biocrust wetting) may inflate the background SCC threshold and reduce the count of well-predicted metabolites, as noted for the soil dataset (threshold 0.410 vs. 0.136 for IBD-PRISM). Cross-sectional and longitudinal designs may not be directly comparable.
- Feature attribution scores and module assignments are data-driven and do not incorporate mechanistic knowledge of metabolite biosynthesis or microbe–host interactions, limiting the biological interpretability of transformation-induced differences in module content.
- The skill assumes raw or minimally processed input (count or intensity data). If metabolome data have already undergone log transformation or other compositional adjustments prior to this comparison, the transformation effect will be confounded with prior preprocessing.

## Evidence

- [other] In the IBD (PRISM) dataset, prediction correlations were comparable between CLR and relative abundance transformations, while CLR showed increased correlations in cystic fibrosis and soil datasets.: "In the IBD (PRISM) dataset, prediction correlations were comparable between CLR and relative abundance transformations, while CLR showed increased correlations in cystic fibrosis and soil datasets."
- [other] Prepare two parallel input transformations: centered log-ratio (CLR) transformation with pseudocount +1, and relative abundance (RA) normalization.: "Prepare two parallel input transformations: centered log-ratio (CLR) transformation with pseudocount +1, and relative abundance (RA) normalization."
- [other] For each transformation, train MiMeNet (multi-layer perceptron with ReLU activation, L2 regularization λ=0.001, dropout=0.5, layer size=512, 1 hidden layer) using 10 iterations of 10-fold cross-validation (80/20 train/validation split during CV, early stopping at 40 epochs without validation improvement).: "For each transformation, train MiMeNet (multi-layer perceptron with ReLU activation, L2 regularization λ=0.001, dropout=0.5, layer size=512, 1 hidden layer) using 10 iterations of 10-fold"
- [other] Generate background distributions by shuffling microbiome and metabolome samples independently, training 100 models per condition, collecting Spearman correlation coefficients (SCC).: "Generate background distributions by shuffling microbiome and metabolome samples independently, training 100 models per condition, collecting Spearman correlation coefficients (SCC)."
- [other] Define well-predicted metabolites at the 95th percentile of background SCC; count and record well-predicted metabolite sets for CLR and RA conditions.: "Define well-predicted metabolites at the 95th percentile of background SCC; count and record well-predicted metabolite sets for CLR and RA conditions."
- [readme] MiMeNet generates a background of SCC values using a similar approach as in _Cross-Validated Evaluation_. However, to generate the background distribution of SCCs, the samples are randomly shuffled for each cross-validated iteration.: "MiMeNet generates a background of SCC values using a similar approach as in _Cross-Validated Evaluation_. However, to generate the background distribution of SCCs, the samples are randomly shuffled"
- [other] Compare counts of well-predicted metabolites and AUC scores between CLR and RA, documenting the magnitude of improvement for CLR.: "Compare counts of well-predicted metabolites and AUC scores between CLR and RA, documenting the magnitude of improvement for CLR."
- [discussion] since not all metabolites may be associated with microbes, some metabolites will have lower prediction correlations, which resulted in an overall lower mean correlation across all metabolites: "since not all metabolites may be associated with microbes, some metabolites will have lower prediction correlations, which resulted in an overall lower mean correlation across all metabolites"
- [discussion] We also observed a higher threshold value for the soil data (Fig 3A–3C), which may be due to the longitudinal observations.: "We also observed a higher threshold value for the soil data (Fig 3A–3C), which may be due to the longitudinal observations."
