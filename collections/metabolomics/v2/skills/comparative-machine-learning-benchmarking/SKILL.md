---
name: comparative-machine-learning-benchmarking
description: Use when you have developed a new machine learning model for predicting metabolomic profiles from microbiome data and need to quantify its performance improvement over existing methods.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3659
  edam_topics:
  - http://edamontology.org/topic_3174
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3673
  tools:
  - MiMeNet
  - ADAM optimizer
  - MelonnPan
  - Elastic Net
  - WGCNA
  - Random Forest
  - scikit-learn
derived_from:
- doi: 10.1371/journal.pcbi.1009021
  title: MiMeNet
evidence_spans:
- An MLPNN model is composed of multiple fully connected hidden layers composed of perceptrons
- MiMeNet is an integrative MLPNN, which trains models to accurately predict the metabolome based on a microbiome
- MiMeNet was trained using the ADAM optimizer and the mean squared error (MSE) loss function.
- MiMeNet was trained using the ADAM optimizer and the mean squared error (MSE) loss function
- MelonnPan was downloaded from https://github.com/biobakery/melonnpan and executed using the given instructions
- Multivariate Elastic Net models were implemented using ElasticNet and GridSearchCV using 5-fold internal cross-validation
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# comparative-machine-learning-benchmarking

## Summary

Systematic evaluation of a novel machine learning model (MiMeNet) against established baselines (MelonnPan, Random Forest, Elastic Net, NED) on paired microbiome-metabolome datasets using consistent train-test splits, cross-validation protocols, and correlation-based performance metrics. This skill enables assessment of whether a new predictive approach offers genuine improvements in metabolite prediction accuracy and discovery capacity.

## When to use

You have developed a new machine learning model for predicting metabolomic profiles from microbiome data and need to quantify its performance improvement over existing methods. Apply this skill when you have access to paired microbiome (16S or metagenomic) and metabolome (LC-MS or other) data from multiple cohorts, and you want to compare prediction accuracy, count of well-predicted features, and generalizability across independent validation sets.

## When NOT to use

- Unpaired microbiome and metabolome data: benchmarking requires the same biological samples measured in both omics modalities.
- Datasets with <50 samples in any training fold: cross-validation performance estimates become unreliable; consider pooled evaluation instead.
- Single cohort with no external validation set: inability to assess generalization; task_id=task_002 explicitly validates on a separate external IBD cohort.

## Inputs

- Paired microbiome abundance table (samples × microbial features, e.g., 201 features after filtering)
- Paired metabolome abundance table (samples × metabolomic features, e.g., 8848 features after filtering)
- External validation microbiome table (independent cohort, same feature space)
- External validation metabolome table (independent cohort, same feature space)
- Trained model weights or hyperparameter specification (JSON or text file)

## Outputs

- Cross-validated Spearman correlation coefficients per metabolite per fold
- Mean Spearman correlation coefficient across all metabolites (aggregated)
- Count of well-predicted metabolites (above 95th percentile threshold)
- Background distribution of correlations from shuffled cross-validation
- External validation performance metrics (mean SCC, well-predicted count on held-out data)
- Comparison table: proposed model vs. baseline models (MelonnPan, Random Forest, etc.) for each metric

## How to apply

Train your proposed model (e.g., MiMeNet multilayer perceptron) on the same preprocessed input data (centered log-ratio transformed, features filtered at 10% prevalence threshold) using identical hyperparameter tuning procedures (e.g., layer size 512, L2 penalty 0.001, dropout 0.5, ADAM optimizer with early stopping). Run ten iterations of 10-fold cross-validation to obtain stable performance estimates. Measure predictive accuracy using Spearman correlation coefficients between predicted and observed metabolite abundances for each feature. Generate a background distribution by shuffling the dataset and repeating cross-validation, then use the 95th percentile of shuffled correlations as a threshold to identify well-predicted metabolites. Train the same baseline models (MelonnPan with Elastic Net, Random Forest regressors, and any published comparators) on identical training data with their established protocols. Report: (1) mean Spearman correlation coefficient across all metabolites, (2) count of metabolites exceeding the 95th percentile threshold, and (3) performance on held-out external validation cohorts if available. This ensures fair comparison because all models see the same training distribution, normalization, and feature filtering.

## Related tools

- **MiMeNet** (Proposed neural network model for microbe-metabolite prediction under evaluation) — https://github.com/YDaiLab/MiMeNet
- **MelonnPan** (Baseline linear model (Elastic Net) for comparative benchmarking) — https://github.com/biobakery/melonnpan
- **Random Forest** (Baseline non-linear regressor for comparative benchmarking)
- **ADAM optimizer** (Gradient descent optimizer for training neural network models)
- **scikit-learn** (Implementation of cross-validation and baseline regression models)

## Examples

```
python MiMeNet_train.py -micro data/IBD/microbiome_PRISM.csv -metab data/IBD/metabolome_PRISM.csv -external_micro data/IBD/microbiome_external.csv -external_metab data/IBD/metabolome_external.csv -micro_norm None -metab_norm CLR -net_params results/IBD/network_parameters.txt -num_run_cv 10 -num_cv 10 -threshold 0.95 -output IBD
```

## Evaluation signals

- Consistency check: all models trained on identical preprocessed data (centered log-ratio normalized, <10% prevalence features removed) with no data leakage between cross-validation folds.
- Metric stability: mean Spearman correlation reported with standard deviation or confidence intervals across ten CV iterations and ten folds per iteration (100 estimates total).
- External validity: proposed model shows consistent improvement (e.g., mean SCC increase from 0.168 to 0.275 for annotated metabolites) when evaluated on held-out external cohort data without retraining.
- Well-predicted metabolite counts match threshold definition: count reports metabolites with SCC > 95th percentile of background shuffled distribution, with explicit background statistics reported.
- Baseline agreement: baseline models (MelonnPan, Random Forest) reproduce or closely match previously published performance on same data, confirming fair implementation.

## Limitations

- Not all metabolites may be associated with microbes in vivo, resulting in inherently low prediction correlations for non-microbial metabolites and biasing overall mean correlation downward (acknowledged in MiMeNet discussion).
- MiMeNet analysis is data-driven without incorporating mechanistic knowledge of metabolic pathways; improvements in correlation do not necessarily indicate causal or functional microbe-metabolite relationships.
- Generalizability across body sites and sample types remains unclear: threshold values differ across datasets (e.g., higher for soil data with longitudinal structure), suggesting dataset-specific empirical background generation may be necessary.
- External validation performance depends critically on similarity between training and external cohorts in microbiome composition, sequencing depth, and metabolomic platform; large distributional shifts may invalidate the 95th percentile threshold.

## Evidence

- [other] When training using the entire IBD (PRISM) dataset to predict the IBD (External) test set, MiMeNet identified 308 well-predicted metabolites while MelonnPan identified 186, with mean correlation increased from 0.168 to 0.275 for annotated metabolites.: "When training using the entire IBD (PRISM) dataset to predict the IBD (External) test set, MiMeNet identified 308 well-predicted metabolites while MelonnPan identified 186, with mean correlation"
- [other] Train a single MiMeNet multilayer perceptron neural network on the full IBD (PRISM) dataset using optimal hyperparameters (layer size 512, single hidden layer, L2 penalty 0.001, dropout 0.5) with ADAM optimizer and mean squared error loss, applying early stopping when validation loss does not improve within 40 iterations.: "Train a single MiMeNet multilayer perceptron neural network on the full IBD (PRISM) dataset using optimal hyperparameters (layer size 512, single hidden layer, L2 penalty 0.001, dropout 0.5) with"
- [other] Evaluate the trained model on IBD (External) test data by computing Spearman correlation coefficients between predicted and observed metabolite abundances for each metabolite.: "Evaluate the trained model on IBD (External) test data by computing Spearman correlation coefficients between predicted and observed metabolite abundances for each metabolite."
- [other] Identify well-predicted metabolites in the IBD (External) dataset using the 95th percentile threshold of background correlations from shuffled cross-validation.: "Identify well-predicted metabolites in the IBD (External) dataset using the 95th percentile threshold of background correlations from shuffled cross-validation."
- [results] We identified 163 microbes that had at least one significant attribution score with a well-predicted metabolite: "We identified 163 microbes that had at least one significant attribution score with a well-predicted metabolite"
- [results] compared MiMeNet to MelonnPan, a recent model that uses Elastic Net linear regression: "compared MiMeNet to MelonnPan, a recent model that uses Elastic Net linear regression"
- [results] we benchmarked MiMeNet against other general regression models, i.e., Random Forest (RF): "we benchmarked MiMeNet against other general regression models, i.e., Random Forest (RF)"
- [discussion] since not all metabolites may be associated with microbes, some metabolites will have lower prediction correlations, which resulted in an overall lower mean correlation across all metabolites: "since not all metabolites may be associated with microbes, some metabolites will have lower prediction correlations, which resulted in an overall lower mean correlation across all metabolites"
- [discussion] Although the MiMeNet analysis is data-driven without incorporating mechanistic knowledge, these types of evidence obtained from the integrative analysis: "Although the MiMeNet analysis is data-driven without incorporating mechanistic knowledge, these types of evidence obtained from the integrative analysis"
- [methods] Any input or output feature that is present in less than 10% of samples was removed: "Any input or output feature that is present in less than 10% of samples was removed"
- [methods] We then defined a metabolite as well-predicted if its SCC is above the 95th percentile of the background correlations: "We then defined a metabolite as well-predicted if its SCC is above the 95th percentile of the background correlations"
- [results] the predictive performance of a model is measured by the average Spearman correlation coefficients (SCCs) between the predicted and the observed abundances: "the predictive performance of a model is measured by the average Spearman correlation coefficients (SCCs) between the predicted and the observed abundances"
- [results] MiMeNet then generates a background distribution of SCCs through multiple iterations of shuffling the dataset and performing a cross-validation on the shuffled set: "MiMeNet then generates a background distribution of SCCs through multiple iterations of shuffling the dataset and performing a cross-validation on the shuffled set"
- [results] MiMeNet then trains multiple network models using 10-fold cross-validation: "MiMeNet then trains multiple network models using 10-fold cross-validation"
- [abstract] Using ten iterations of 10-fold cross-validation on three paired microbiome-metabolome datasets: "Using ten iterations of 10-fold cross-validation on three paired microbiome-metabolome datasets"
