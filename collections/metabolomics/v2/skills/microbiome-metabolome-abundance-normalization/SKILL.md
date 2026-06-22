---
name: microbiome-metabolome-abundance-normalization
description: Use when when you have raw count matrices from paired microbiome (16S rRNA or metagenomic) and metabolomic (LC-MS/MS) profiling data that will be used to train or apply a predictive model (e.g., MiMeNet, MelonnPan, Random Forest) to predict metabolite abundances from microbial composition.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3174
  - http://edamontology.org/topic_0194
  - http://edamontology.org/topic_3520
  tools:
  - MiMeNet
  - ADAM optimizer
  - MelonnPan
  - Elastic Net
  - WGCNA
  - scikit-bio
  - HUMAnN2
  techniques:
  - LC-MS
  - tandem-MS
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

# microbiome-metabolome-abundance-normalization

## Summary

Compositional transformation of paired microbiome and metabolome count matrices into normalized abundance representations (relative abundance or centered log-ratio) prior to predictive modeling. This preprocessing step corrects for the compositional nature of sequencing data and removes features with low prevalence, enabling fair comparison across samples and reducing noise in downstream machine learning.

## When to use

When you have raw count matrices from paired microbiome (16S rRNA or metagenomic) and metabolomic (LC-MS/MS) profiling data that will be used to train or apply a predictive model (e.g., MiMeNet, MelonnPan, Random Forest) to predict metabolite abundances from microbial composition. Apply this skill before feature attribution analysis, cross-validation, or model evaluation to ensure data are on a comparable scale and low-signal features do not confound results.

## When NOT to use

- Input matrices are already normalized or CLR-transformed (e.g., from prior preprocessing); applying the skill twice will distort the data.
- Analyzing single (non-paired) microbiome or metabolome data without the paired partner; this skill is designed for joint microbiome-metabolome prediction and requires both data types.
- Data include negative values or continuous measurements that are not counts (e.g., ion intensity directly from MS); CLR and RA transformations assume count data with non-negative support.

## Inputs

- Microbiome count matrix (samples × microbial features; CSV format)
- Metabolome count matrix (samples × metabolite features; CSV format)
- External validation microbiome counts (optional; for hold-out evaluation)
- External validation metabolome counts (optional; for hold-out evaluation)

## Outputs

- Normalized microbiome abundance matrix (CLR or RA transformed; samples × features)
- Normalized metabolome abundance matrix (CLR or RA transformed; samples × features)
- Feature prevalence summary (count and percentage of samples per feature pre/post filtering)
- Filtered feature list (features retained after 10% prevalence threshold)

## How to apply

First, apply a compositional transformation to both the microbiome and metabolome count matrices using either relative abundance (RA) normalization or centered log-ratio (CLR) transformation. CLR is preferred when using neural networks or when the data include true zero abundances, as it handles compositionality without arbitrary pseudo-counts. Second, remove any input or output feature (microbial taxa or metabolite) present in less than 10% of samples to filter low-abundance or erratic signal. Apply these transformations identically to both training and external validation datasets to ensure consistency. If data are already normalized (e.g., from prior preprocessing), skip transformation by passing 'None' to the normalization parameter. Document the specific transformation and filtering thresholds applied so that external data can be preprocessed identically during model evaluation.

## Related tools

- **MiMeNet** (Primary neural network framework that accepts normalized CLR or RA transformed microbiome and metabolome matrices as input and trains predictive models) — https://github.com/YDaiLab/MiMeNet
- **MelonnPan** (Elastic Net regression baseline model for microbiome-metabolome prediction; accepts normalized feature tables) — https://github.com/biobakery/melonnpan
- **scikit-bio** (Python library providing compositional transformation functions (CLR) and feature filtering utilities)
- **HUMAnN2** (Metagenomic functional profiling tool that can generate UniRef90 gene family abundance tables as input to MelonnPan or other downstream models)

## Examples

```
python MiMeNet_train.py -micro data/IBD/microbiome_PRISM.csv -metab data/IBD/metabolome_PRISM.csv -external_micro data/IBD/microbiome_external.csv -external_metab data/IBD/metabolome_external.csv -micro_norm CLR -metab_norm CLR -num_run_cv 10 -output IBD
```

## Evaluation signals

- Verify that all feature abundance values in the normalized matrix are non-negative and do not contain NaN or infinite values; CLR-transformed data may contain small negative values due to log-ratio geometry.
- Confirm that the number of features retained post-filtering matches the 10% prevalence threshold: features present in fewer than 0.1 × (number of samples) should be removed.
- Check that the normalized microbiome and metabolome matrices have identical sample ordering and sample count before joint modeling.
- Validate that external validation datasets are transformed using identical parameters (RA or CLR, same filtering threshold) as the training set; compare the feature sets to ensure alignment.
- Inspect the distribution of normalized abundances: CLR-transformed data should be roughly symmetric around zero; RA-transformed data should sum to 1.0 (or constant) per sample.

## Limitations

- CLR transformation can introduce spurious correlations among features due to the closure constraint (all features sum to constant); use appropriate statistical methods downstream (e.g., SPIEC-EASI, CCPNA) if inferring associations.
- The 10% prevalence filter may be too lenient for rare microbial taxa or low-abundance metabolites in small cohorts; consider cohort size and biological relevance when setting the threshold.
- Not all metabolites may be predicted from microbiome data alone, as some metabolites derive from host diet or metabolism; even after normalization, prediction correlations may be low for non-microbial metabolites.
- Normalization does not account for technical variation (e.g., batch effects, sequencing depth biases); consider batch correction or technical covariate adjustment separately if present.
- The choice between RA and CLR normalization can affect downstream results; CLR is preferred for compositional methods but may not always be appropriate depending on the statistical model (e.g., MelonnPan uses Elastic Net and may accept RA).

## Evidence

- [methods] Any input or output feature that is present in less than 10% of samples was removed: "Any input or output feature that is present in less than 10% of samples was removed"
- [readme] Microbiome normalization (RA, CLR, or None): "Microbiome normalization (RA, CLR, or None)"
- [readme] MiMeNet will perform a compositional transformation to relative abundance or centered log-ratio and filter low abundant microbial: "MiMeNet will perform a compositional transformation to relative abundance or centered log-ratio and filter low abundant microbial"
- [other] Load and preprocess IBD (PRISM) microbiome (201 features) and metabolome (8848 features) data, applying centered log-ratio transformation and removing features present in <10% of samples.: "Load and preprocess IBD (PRISM) microbiome (201 features) and metabolome (8848 features) data, applying centered log-ratio transformation and removing features present in <10% of samples."
- [other] Load and preprocess IBD (External) microbiome and metabolome data using identical transformation and filtering procedures.: "Load and preprocess IBD (External) microbiome and metabolome data using identical transformation and filtering procedures."
- [readme] If the data is already transformed, apply 'None' to skip transformation.: "If the data is already transformed, apply 'None' to skip transformation."
