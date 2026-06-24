---
name: cross-dataset-model-generalization-assessment
description: Use when you have trained a neural network or regression model on one
  paired microbiome-metabolome dataset and wish to test whether it can predict metabolite
  abundances in an independent, externally-sourced dataset collected from different
  patient cohorts or study populations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3174
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0625
  tools:
  - MiMeNet
  - ADAM optimizer
  - MelonnPan
  - Elastic Net
  - WGCNA
  - Random Forest
  - Spearman correlation
  license_tier: restricted
derived_from:
- doi: 10.1371/journal.pcbi.1009021
  title: MiMeNet
evidence_spans:
- An MLPNN model is composed of multiple fully connected hidden layers composed of
  perceptrons
- MiMeNet is an integrative MLPNN, which trains models to accurately predict the metabolome
  based on a microbiome
- MiMeNet was trained using the ADAM optimizer and the mean squared error (MSE) loss
  function.
- MiMeNet was trained using the ADAM optimizer and the mean squared error (MSE) loss
  function
- MelonnPan was downloaded from https://github.com/biobakery/melonnpan and executed
  using the given instructions
- Multivariate Elastic Net models were implemented using ElasticNet and GridSearchCV
  using 5-fold internal cross-validation
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

# cross-dataset-model-generalization-assessment

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Evaluate whether a predictive model trained on one microbiome-metabolome dataset maintains prediction accuracy when applied to an independent held-out dataset from different cohorts or clinical sources. This skill assesses generalization capacity by comparing correlation metrics and well-predicted metabolite counts across datasets.

## When to use

You have trained a neural network or regression model on one paired microbiome-metabolome dataset and wish to test whether it can predict metabolite abundances in an independent, externally-sourced dataset collected from different patient cohorts or study populations. Apply this skill when you need to validate that model performance is not an artifact of training-set overfitting and to quantify the degree of generalization loss.

## When NOT to use

- The external dataset uses a fundamentally different feature taxonomy or gene family annotation system (e.g., training used 16S taxonomy but external data uses shotgun metagenomics UniRef90) without a consistent mapping
- The training dataset and external dataset measure metabolites via different analytical platforms (e.g., different MS instruments, chromatography methods) without prior platform harmonization or batch correction
- You have no held-out external dataset and are only performing internal cross-validation within a single cohort

## Inputs

- trained neural network model (e.g., MiMeNet multilayer perceptron with fixed weights and architecture)
- external microbiome feature table (samples × microbial taxa/features, CSV or matrix format)
- external metabolome feature table (samples × metabolite compounds, CSV or matrix format)
- data transformation specification (e.g., CLR, relative abundance) used during training
- feature filtering thresholds applied to training set (e.g., minimum prevalence cutoff)

## Outputs

- Spearman correlation coefficient (SCC) for each metabolite (predicted vs. observed)
- mean SCC across all metabolites or annotated subset
- count of well-predicted metabolites (above 95th percentile threshold)
- background distribution of SCCs from shuffled cross-validation
- comparison metrics relative to baseline methods (e.g., MelonnPan, Random Forest)

## How to apply

Load and preprocess the external validation dataset using identical data transformations (e.g., centered log-ratio transformation) and feature filtering thresholds (e.g., ≥10% prevalence) as the training set to ensure consistent feature spaces. Apply the trained model to the external test set without further training or hyperparameter adjustment. Compute Spearman correlation coefficients (SCCs) between predicted and observed metabolite abundances for each metabolite. Generate a background distribution of SCCs by performing cross-validation on shuffled versions of the external dataset to establish a null expectation. Identify well-predicted metabolites in the external set using the 95th percentile threshold of the background correlations. Report mean SCC, the count of well-predicted metabolites, and comparative metrics (e.g., change in mean correlation, increase in metabolite counts) relative to baseline methods to quantify generalization performance.

## Related tools

- **MiMeNet** (trained neural network model applied to external validation data to predict metabolome from microbiome) — https://github.com/YDaiLab/MiMeNet
- **MelonnPan** (baseline method for comparative assessment of generalization performance (Elastic Net linear regression)) — https://github.com/biobakery/melonnpan
- **Random Forest** (baseline regression method for comparison of predictive accuracy on external data)
- **Spearman correlation** (statistical metric for measuring agreement between predicted and observed metabolite abundances)

## Examples

```
python MiMeNet_train.py -micro data/IBD/microbiome_PRISM.csv -metab data/IBD/metabolome_PRISM.csv -external_micro data/IBD/microbiome_external.csv -external_metab data/IBD/metabolome_external.csv -micro_norm None -metab_norm CLR -net_params results/IBD/network_parameters.txt -num_run_cv 10 -output IBD
```

## Evaluation signals

- Mean Spearman correlation coefficient on external data is substantially higher than baseline methods (e.g., increase from 0.168 to 0.275 for MelonnPan comparison), indicating genuine model superiority rather than overfitting
- Count of well-predicted metabolites (above 95th percentile of background) is consistent with or exceeds training-set performance; significant decline suggests poor generalization
- Background distribution of SCCs from shuffled external cross-validation shows clear separation from observed SCC values, confirming statistical significance of well-predicted metabolites
- External dataset feature space (after preprocessing) matches training set dimensionality and composition; mismatch in filtered feature counts indicates preprocessing inconsistency
- No model retraining or hyperparameter adjustment occurs between training and external evaluation; model weights remain frozen

## Limitations

- Not all metabolites may be associated with microbes, resulting in lower prediction correlations and lower overall mean correlation across the full metabolite set, obscuring true model capacity
- External dataset must be collected from independent cohorts; if external samples derive from the same study population as training data, generalization assessment is invalid
- MiMeNet analysis is data-driven without incorporating mechanistic knowledge, so well-predicted metabolites may reflect statistical associations rather than causal microbe-metabolite interactions
- Higher or lower well-predicted metabolite thresholds may be needed for datasets with different temporal structures (e.g., longitudinal soil samples vs. cross-sectional human studies), but implications for threshold generalization are not fully explored
- Model performance depends on consistency of microbiome feature annotations and metabolite measurement platforms; platform-specific bias or missing annotations in external data can degrade predictions

## Evidence

- [other] When training using the entire IBD (PRISM) dataset to predict the IBD (External) test set, MiMeNet identified 308 well-predicted metabolites while MelonnPan identified 186, with mean correlation increased from 0.168 to 0.275 for annotated metabolites.: "When training using the entire IBD (PRISM) dataset to predict the IBD (External) test set, MiMeNet identified 308 well-predicted metabolites while MelonnPan identified 186, with mean correlation"
- [other] Load and preprocess IBD (External) microbiome and metabolome data using identical transformation and filtering procedures.: "Load and preprocess IBD (External) microbiome and metabolome data using identical transformation and filtering procedures."
- [other] Evaluate the trained model on IBD (External) test data by computing Spearman correlation coefficients between predicted and observed metabolite abundances for each metabolite.: "Evaluate the trained model on IBD (External) test data by computing Spearman correlation coefficients between predicted and observed metabolite abundances for each metabolite."
- [other] Identify well-predicted metabolites in the IBD (External) dataset using the 95th percentile threshold of background correlations from shuffled cross-validation.: "Identify well-predicted metabolites in the IBD (External) dataset using the 95th percentile threshold of background correlations from shuffled cross-validation."
- [methods] Any feature attribution score in the observed dataset with an absolute value above the threshold was considered significant: "Any feature attribution score in the observed dataset with an absolute value above the threshold was considered significant"
- [methods] We then defined a metabolite as well-predicted if its SCC is above the 95th percentile of the background correlations: "We then defined a metabolite as well-predicted if its SCC is above the 95th percentile of the background correlations"
- [discussion] since not all metabolites may be associated with microbes, some metabolites will have lower prediction correlations, which resulted in an overall lower mean correlation across all metabolites: "since not all metabolites may be associated with microbes, some metabolites will have lower prediction correlations, which resulted in an overall lower mean correlation across all metabolites"
- [discussion] Although the MiMeNet analysis is data-driven without incorporating mechanistic knowledge, these types of evidence obtained from the integrative analysis: "Although the MiMeNet analysis is data-driven without incorporating mechanistic knowledge, these types of evidence obtained from the integrative analysis"
