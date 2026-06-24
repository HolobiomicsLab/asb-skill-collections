---
name: cross-validation-workflow-execution
description: Use when you have paired microbiome (16S rRNA/metagenomic) and metabolome
  (LC-MS/MS or similar) count data and need to evaluate how well a predictive model
  (e.g., neural network, Elastic Net) generalizes across samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3697
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0199
  tools:
  - Elastic Net
  - MiMeNet
  - TensorFlow or PyTorch
  - scikit-learn
  - Seaborn
  - Python
  - SciPy
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1371/journal.pcbi.1009021
  title: MiMeNet
evidence_spans:
- we benchmarked MiMeNet against other general regression models, i.e., Random Forest
  (RF), multivariate Elastic Net, and canonical correlation analysis (CCA) models
- MiMeNet (Microbiome-Metabolome Network), a multi-layer perceptron (MLPNN)
- MiMeNet uses paired microbiome and metabolome data for model training. Microbiome
  abundance features (green) are used to train a neural network to predict metabolite
  abundance features (blue).
- MiMeNet was trained using the ADAM optimizer and the mean squared error (MSE) loss
  function
- MiMeNet was trained using the ADAM optimizer and the mean squared error (MSE) loss
  function.
- MelonnPan and NED models were obtained from their respective GitHub repositories
  and executed using default parameters as according to their tutorials. Random Forest,
  multivariate Elastic Net, and
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

# cross-validation-workflow-execution

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Execute multiple iterations of k-fold cross-validation on paired microbiome-metabolome datasets to obtain empirical performance distributions (Spearman correlation coefficients) and establish statistical thresholds for identifying well-predicted metabolites. This workflow trains neural network models repeatedly on held-out folds to measure predictive robustness and generate background distributions for significance testing.

## When to use

Apply this skill when you have paired microbiome (16S rRNA/metagenomic) and metabolome (LC-MS/MS or similar) count data and need to evaluate how well a predictive model (e.g., neural network, Elastic Net) generalizes across samples. Use it specifically when you must distinguish true metabolite prediction signals from noise by comparing observed performance to a shuffled background distribution, or when you need to estimate model stability across multiple random train-test partitions.

## When NOT to use

- Input feature tables are not paired or samples cannot be stratified consistently (e.g., longitudinal samples from same subject where randomization violates independence assumption).
- Sample size is very small (<30 samples total), in which case k-fold CV with k>3 may lead to underpowered folds and unreliable threshold estimation.
- You only have a single static model you wish to evaluate once; cross-validation is designed for repeated training and threshold calibration, not single-pass evaluation.
- Metabolites are already annotated and validated by external standards such that no empirical threshold discovery is needed.

## Inputs

- Paired microbiome abundance table (samples × microbes; count or compositional format)
- Paired metabolome abundance table (samples × metabolites; count or relative abundance format)
- Neural network hyperparameter configuration (JSON or dict: layers, layer size, L2 penalty, dropout rate, early stopping criteria)
- Optional: sample labels or phenotype vector for module enrichment testing
- Optional: external test set (separate microbiome and metabolome tables for validation)

## Outputs

- Cross-validated Spearman correlation coefficient (SCC) distribution per metabolite (mean ± SD or full per-fold values)
- Background SCC distribution from shuffled cross-validation (used to compute 95th percentile threshold)
- Well-predicted metabolite set (those with observed SCC > 95th percentile of background)
- Trained neural network weights from each fold (for feature attribution extraction)
- Feature attribution score matrix (microbes × metabolites; normalized and clipped to [−1, 1])
- Optional: module membership assignments (microbes and metabolites clustered by interaction patterns)

## How to apply

Perform 10–100 iterations of k-fold cross-validation (typically 10 folds) on your paired microbiome-metabolome feature tables. For each iteration: (1) partition samples into k stratified folds; (2) train the model (e.g., MiMeNet neural network with specified hyperparameters: L2 regularization λ=0.001, dropout=0.5, layer size=512, 1 hidden layer) on k−1 folds; (3) evaluate on the held-out fold, recording Spearman correlation coefficients (SCC) between predicted and observed metabolite abundances; (4) aggregate SCCs across all folds and iterations to obtain a mean performance distribution. In parallel, generate a background distribution by shuffling microbiome and metabolome samples independently while repeating the same cross-validation procedure 100 times, collecting shuffled SCCs. Define metabolites as well-predicted if their observed SCC exceeds the 95th percentile of the background distribution. Use the trained models from the full CV run to extract feature attribution scores (e.g., via Olden's method) for subsequent module clustering and downstream analysis.

## Related tools

- **MiMeNet** (Multilayer perceptron neural network model trained and evaluated within cross-validation workflow to predict metabolite abundances from microbiome features and extract feature attribution scores.) — https://github.com/YDaiLab/MiMeNet
- **TensorFlow or PyTorch** (Deep learning framework used to implement and train the neural network model across cross-validation folds.)
- **scikit-learn** (Provides cross-validation utilities (KFold, StratifiedKFold), model evaluation metrics, and preprocessing functions for train-test splitting.)
- **SciPy** (Computes Spearman correlation coefficients between predicted and observed metabolite abundances for each fold.)
- **Seaborn** (Visualization of cross-validation performance distributions and background threshold comparisons.)

## Examples

```
python MiMeNet_train.py -micro data/IBD/microbiome_PRISM.csv -metab data/IBD/metabolome_PRISM.csv -micro_norm None -metab_norm CLR -net_params results/IBD/network_parameters.txt -num_run_cv 10 -num_cv 10 -num_background 100 -output IBD_CV_results
```

## Evaluation signals

- Mean Spearman correlation coefficients reported for each metabolite; observed SCC values should be roughly normally distributed and span a plausible range (e.g., −0.5 to 0.8 for real data) rather than all near zero or saturated.
- Background SCC distribution (from shuffled CV) should be centered near zero with lower variance than observed SCCs; 95th percentile threshold should be strictly positive and separated from observed metabolite SCCs to ensure meaningful discrimination.
- Well-predicted metabolite count should increase monotonically or remain stable across CV iterations (not oscillate wildly), and should be substantially lower than total metabolite count (typically 5–10% of features), indicating genuine signal recovery rather than overfitting.
- Feature attribution score matrices should be sparse after thresholding at the 97.5th percentile; microbes with zero significant attribution scores should be filtered out, and remaining microbes should co-cluster with metabolites in a consistent module structure across replicate CV runs.
- External validation (if available) on held-out cohort or time-split should show SCC values and well-predicted metabolite counts comparable to or slightly lower than CV performance, validating generalization.

## Limitations

- Cross-validation performance does not guarantee external generalization, especially if the external dataset comes from a different body site, disease state, or sequencing platform with different microbial or metabolic distributions.
- The 95th percentile threshold for well-predicted metabolites is arbitrary; in datasets where few metabolites truly associate with microbes, this threshold may yield false positives; conversely, in highly structured datasets (e.g., soil with strong temporal signals), the threshold may be too conservative and exclude real signals.
- Longitudinal or repeated-measures data within samples violates the independence assumption required for random k-fold CV; special handling (e.g., stratifying by subject, using GroupKFold) is required but is not detailed in the MiMeNet workflow.
- Computational cost scales poorly with feature count: training 100+ models on large microbiome tables (>1000 features) and metabolome tables (>5000 features) can be prohibitively slow; feature filtering (e.g., removing features present in <10% of samples) is essential.
- The workflow assumes that true metabolite-microbe relationships are captured by the neural network architecture and hyperparameters used; if the network is misspecified (e.g., wrong layer count, insufficient capacity), performance may be artificially depressed and thresholds become unreliable.

## Evidence

- [abstract] Using ten iterations of 10-fold cross-validation on three paired microbiome-metabolome datasets: "Using ten iterations of 10-fold cross-validation on three paired microbiome-metabolome datasets"
- [other] Train MiMeNet (multi-layer perceptron with ReLU activation, L2 regularization λ=0.001, dropout=0.5, layer size=512, 1 hidden layer) using 10 iterations of 10-fold cross-validation (80/20 train/validation split during CV, early stopping at 40 epochs without validation improvement).: "Train MiMeNet (multi-layer perceptron with ReLU activation, L2 regularization λ=0.001, dropout=0.5, layer size=512, 1 hidden layer) using 10 iterations of 10-fold cross-validation (80/20"
- [other] Generate background distributions by shuffling microbiome and metabolome samples independently, training 100 models per condition, collecting Spearman correlation coefficients (SCC).: "Generate background distributions by shuffling microbiome and metabolome samples independently, training 100 models per condition, collecting Spearman correlation coefficients (SCC)."
- [other] Define well-predicted metabolites at the 95th percentile of background SCC; count and record well-predicted metabolite sets for CLR and RA conditions.: "Define well-predicted metabolites at the 95th percentile of background SCC; count and record well-predicted metabolite sets for CLR and RA conditions."
- [other] Extract feature attribution score matrices using Olden's method for significant microbe-metabolite interactions (97.5th percentile threshold).: "Extract feature attribution score matrices using Olden's method for significant microbe-metabolite interactions (97.5th percentile threshold)."
- [readme] MiMeNet generates a background of SCC values using a similar approach as in Cross-Validated Evaluation. However, to generate the background distribution of SCCs, the samples are randomly shuffled for each cross-validated iteration.: "MiMeNet generates a background of SCC values using a similar approach as in Cross-Validated Evaluation. However, to generate the background distribution of SCCs, the samples are randomly shuffled for"
- [readme] MiMeNet will then take any metabolite with a SCC evaluation value above the 95th percentile to be well-predicted.: "MiMeNet will then take any metabolite with a SCC evaluation value above the 95th percentile to be well-predicted."
- [results] the predictive performance of a model is measured by the average Spearman correlation coefficients (SCCs) between the predicted and the observed abundance of the metabolites: "the predictive performance of a model is measured by the average Spearman correlation coefficients (SCCs) between the predicted and the observed abundance of the metabolites"
- [results] MiMeNet then trains multiple network models using 10-fold cross-validation: "MiMeNet then trains multiple network models using 10-fold cross-validation"
