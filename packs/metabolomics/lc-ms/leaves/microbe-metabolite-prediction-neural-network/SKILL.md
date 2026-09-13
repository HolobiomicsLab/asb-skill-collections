---
name: microbe-metabolite-prediction-neural-network
description: 'Use when you have paired microbiome (16S or metagenomic taxonomy/functions
  at genus or finer level) and metabolome (LC-MS or similar profiled metabolites)
  data from the same samples and want to: (1) predict unobserved metabolite abundances
  from microbiome composition;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_3174
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0080
  tools:
  - MiMeNet
  - MelonnPan
  - Elastic Net
  - NED
  - scikit-learn
  - Python
  - TensorFlow
  - NED (Non-negative Embedding)
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1371/journal.pcbi.1009021
  title: MiMeNet
evidence_spans:
- MiMeNet (Microbiome-Metabolome Network), a multi-layer perceptron (MLPNN)
- MiMeNet uses paired microbiome and metabolome data for model training. Microbiome
  abundance features (green) are used to train a neural network to predict metabolite
  abundance features (blue).
- we first compared MiMeNet to MelonnPan, a recent model that uses Elastic Net linear
  regression
- we benchmarked MiMeNet against other general regression models, i.e., Random Forest
  (RF), multivariate Elastic Net, and canonical correlation analysis (CCA) models
- The NED model was trained using code downloaded from https://github.com/vuongle2/BiomeNED
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

# microbe-metabolite-prediction-neural-network

## Summary

Train a multilayer perceptron neural network to predict metabolomic profiles from microbiome taxonomic or functional abundance data, leveraging shared information across metabolomic features to improve prediction accuracy over independent linear regression methods. This skill identifies well-predicted metabolites and extracts feature attribution scores to illuminate microbe-metabolite interaction networks.

## When to use

You have paired microbiome (16S or metagenomic taxonomy/functions at genus or finer level) and metabolome (LC-MS or similar profiled metabolites) data from the same samples and want to: (1) predict unobserved metabolite abundances from microbiome composition; (2) identify which metabolites can be reliably predicted from microbial taxa; or (3) discover structured microbe-metabolite interaction modules rather than treating each metabolite as an independent prediction target. This is especially valuable when you suspect metabolite predictions benefit from learning shared patterns across the entire metabolomic profile rather than modeling each metabolite separately.

## When NOT to use

- Microbiome and metabolome samples are unpaired or from different individuals—this skill requires matched microbe and metabolite measurements from the same biospecimen.
- Metabolite data is not already profiled (i.e., you have untargeted MS data but no annotated compound identities); feature attribution will lack biological interpretability.
- You seek to predict metabolite presence/absence (binary outcome) rather than continuous abundance; this skill models continuous predictions via MSE loss.

## Inputs

- Paired microbiome abundance table (samples × taxa/KOs; CSV format; genus-level 16S or metagenomic functional features acceptable)
- Paired metabolome abundance table (samples × metabolites; CSV format; LC-MS or similar profiled metabolites)
- Optional: external validation microbiome and metabolome tables (same format, independent samples)
- Optional: metabolite annotation table (CSV; metabolite IDs × annotation fields)
- Optional: sample label table (CSV; sample IDs × phenotype or cohort labels for enrichment testing)
- Network hyperparameter JSON file (layer size, num_layers, L2 penalty, dropout rate)

## Outputs

- Well-predicted metabolites list (metabolite IDs with SCC ≥ 95th percentile threshold)
- Feature attribution score matrix (microbes × metabolites; indicates strength and direction of prediction contribution)
- Microbe-metabolite interaction modules (biclustered microbial and metabolomic clusters with similar interaction patterns)
- Mean Spearman correlation coefficients per method (summary prediction accuracy)
- Background distribution of SCCs from permuted data (used to establish significance threshold)
- Module enrichment statistics (e.g., Wilcoxon rank-sum p-values comparing module feature values between phenotype groups)

## How to apply

Apply centered log-ratio (CLR) transformation to metabolite features and remove features present in <10% of samples. Configure a multilayer perceptron with optimized hyperparameters (e.g., layer size 512, 1 hidden layer, L2 penalty 0.001, dropout 0.5) and train using 10 iterations of k-fold cross-validation (typically k=10) with ADAM optimizer, MSE loss, and early stopping (e.g., 40 epoch patience). Generate a background distribution by shuffling samples in both microbiome and metabolome 100 times and performing the same cross-validated evaluation to establish an empirical null distribution. Calculate the 95th percentile Spearman correlation coefficient (SCC) threshold from this background; metabolites meeting or exceeding this threshold are classified as well-predicted. Construct a feature attribution score matrix from learned network weights to identify significant microbe-metabolite associations (typically at the 97.5th percentile threshold). Cluster the score matrix into microbial and metabolomic modules to reveal functional interaction structure. The rationale is that neural networks can capture nonlinear relationships and learn shared representations across metabolites, while the permutation-based background controls for false discoveries.

## Related tools

- **MiMeNet** (Primary neural network implementation for microbe-metabolite prediction; trains multilayer perceptron with cross-validation and generates background distributions) — https://github.com/YDaiLab/MiMeNet
- **MelonnPan** (Benchmark linear regression baseline (Elastic Net) for comparison; models each metabolite independently to highlight advantage of joint neural network modeling) — https://github.com/biobakery/melonnpan
- **Elastic Net** (Linear regression regularization method used by MelonnPan baseline for independent per-metabolite prediction)
- **TensorFlow** (Deep learning framework for building and training the multilayer perceptron neural network)
- **scikit-learn** (Provides cross-validation splitting, correlation coefficient computation, and statistical utilities)
- **NED (Non-negative Embedding)** (Alternative neural embedding baseline for comparison against MiMeNet prediction performance) — https://github.com/vuongle2/BiomeNED

## Examples

```
python MiMeNet_train.py -micro data/IBD/microbiome_PRISM.csv -metab data/IBD/metabolome_PRISM.csv -external_micro data/IBD/microbiome_external.csv -external_metab data/IBD/metabolome_external.csv -micro_norm None -metab_norm CLR -net_params results/IBD/network_parameters.txt -annotation data/IBD/metabolome_annotation.csv -labels data/IBD/diagnosis_PRISM.csv -num_run_cv 10 -output IBD
```

## Evaluation signals

- Well-predicted metabolites count on held-out test set exceeds that of Elastic Net linear regression baseline by at least 50% (e.g., 351 vs 198 on IBD PRISM), indicating neural network leverages shared information across metabolites.
- Mean Spearman correlation coefficient (SCC) for neural network predictions is substantially higher than baseline (e.g., 0.309 vs 0.108 for MelonnPan on IBD PRISM), confirming improved prediction accuracy.
- 95th percentile SCC threshold derived from permuted background is well-separated from observed SCC distribution (i.e., clear elbow or bimodality), validating statistical significance of well-predicted metabolites.
- Feature attribution scores cluster metabolites and microbes into interpretable modules with statistically significant enrichment for phenotype groups (Wilcoxon p < 0.05), demonstrating biological coherence.
- External validation cohort achieves comparable or higher SCCs to training set, indicating generalization rather than overfitting.

## Limitations

- Not all metabolites may be associated with microbes, resulting in lower prediction correlations and reduced overall mean SCC; requires interpretation that some metabolites are host-derived or environmentally determined.
- Model interpretability is data-driven and does not explicitly incorporate mechanistic or biochemical knowledge; feature attributions reflect statistical associations rather than causal metabolic pathways.
- Longitudinal or temporally dependent samples (e.g., soil wetting time series) may inflate background correlation thresholds, reducing sensitivity to detect well-predicted metabolites in such datasets.
- Hyperparameter optimization (layer size, L2 penalty, dropout, patience) is dataset-specific and may require tuning; no automated hyperparameter search algorithm is provided in the original implementation.
- Requires substantial computational resources (GPU recommended) and memory for large metabolome profiles (>10,000 metabolites); training time scales with number of features and cross-validation iterations.

## Evidence

- [intro] MiMeNet uses multilayer perceptron neural networks to model metagenomic taxonomic or functional features to predict metabolomic features while learning underlying metabolite relationships: "MiMeNet, a multilayer perceptron neural network (MLPNN) that maps metagenomic taxonomic or functional features to metabolomic features. The use of MLPNN allows MiMeNet to"
- [results] MiMeNet identified more well-predicted metabolites on IBD PRISM (351 vs 198) compared to MelonnPan, demonstrating superiority of joint neural modeling over independent linear regression: "MiMeNet identified 351 well-predicted metabolites from 8848 total metabolites, whereas MelonnPan identified 198 well-predicted metabolites using the same correlation cutoff of 0.3."
- [methods] Training procedure uses 10 iterations of 10-fold cross-validation with optimized neural network hyperparameters, ADAM optimizer, MSE loss, and early stopping: "Train MiMeNet using 10 iterations of 10-fold cross-validation with optimized hyperparameters (layer size 512, 1 hidden layer, L2 penalty 0.001, dropout 0.5), using ADAM optimizer and MSE loss with"
- [methods] Background distribution generated by shuffling samples 100 times and performing cross-validated evaluation; 95th percentile SCC threshold used to identify well-predicted metabolites: "Generate background distribution by shuffling samples in both microbiome and metabolome 100 times and performing cross-validated evaluation; calculate 95th percentile SCC threshold (0.136 for IBD"
- [abstract] Feature attribution score matrix derived from network weights is used for clustering microbes and metabolites into functional modules: "trained models are then used to derive microbe-metabolite feature scores, which are used for clustering microbes and metabolites into functional modules"
- [methods] Centered log-ratio transformation applied to metabolite features; features present in <10% of samples are removed prior to modeling: "apply centered log-ratio transformation to metabolite features and remove features present in <10% of samples."
- [intro] MelonnPan models each metabolite individually using Elastic Net, missing shared information across metabolomic features: "MelonnPan displayed promising performance, however, it models each metabolite individually, missing the opportunity to use shared information across metabolomic features to boost prediction"
- [results] Spearman correlation coefficient (SCC) used as primary metric to measure prediction performance between predicted and observed metabolite abundances: "the predictive performance of a model is measured by the average Spearman correlation coefficients (SCCs) between the predicted and the observed abundance of the metabolites"
- [methods] Significant microbe-metabolite attributions identified at 97.5th percentile of background distribution; normalized and clipped to [-1, 1] range: "a threshold was set at the 97.5 percentile. Any feature attribution score in the observed dataset with an absolute value above the threshold was considered significant"
- [abstract] MiMeNet can group microbes and metabolites with similar interaction patterns and functions into modules to illuminate the underlying structure of the microbe-metabolite interaction network: "MiMeNet can group microbes and metabolites with similar interaction patterns and functions to illuminate the underlying structure of the microbe-metabolite interaction network"
