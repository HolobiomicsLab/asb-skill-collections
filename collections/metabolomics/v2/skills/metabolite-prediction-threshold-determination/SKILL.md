---
name: metabolite-prediction-threshold-determination
description: Use when after training and cross-validating a regression model (e.g., neural network or Elastic Net) that predicts metabolite abundances from microbiome features, you have Spearman correlation coefficients (SCCs) for each metabolite between predicted and observed values.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3697
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - MiMeNet
  - scikit-learn (MLPRegressor)
  - ADAM optimizer
  - ReLU activation
  - NumPy
  - SciPy (Spearman correlation)
  - MelonnPan
derived_from:
- doi: 10.1371/journal.pcbi.1009021
  title: MiMeNet
evidence_spans:
- MiMeNet (Microbiome-Metabolome Network), a multi-layer perceptron (MLPNN)
- MiMeNet uses paired microbiome and metabolome data for model training. Microbiome abundance features (green) are used to train a neural network to predict metabolite abundance features (blue).
- An MLPNN model is composed of multiple fully connected hidden layers composed of perceptrons
- Canonical correlation analysis models were implemented using Python's scikit-learn package.
- MiMeNet was trained using the ADAM optimizer and the mean squared error (MSE) loss function.
- In MiMeNet, φ is set as the rectified linear unit (ReLU). We selected this activation function since previous studies have shown that it is resilient to the problems of exploding and vanishing
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

# metabolite-prediction-threshold-determination

## Summary

Determine which metabolites are reliably predicted by a microbiome-to-metabolome model by establishing a statistical cutoff threshold from an empirical background distribution of correlations on shuffled data. This separates signal from noise and identifies metabolites suitable for downstream biological interpretation.

## When to use

After training and cross-validating a regression model (e.g., neural network or Elastic Net) that predicts metabolite abundances from microbiome features, you have Spearman correlation coefficients (SCCs) for each metabolite between predicted and observed values. You need to distinguish metabolites with genuine predictive signal from those that appear predictive by chance. Apply this skill when you have paired microbiome-metabolome data from multiple samples and want to classify metabolites as 'well-predicted' for module discovery, functional interpretation, or biomarker nomination.

## When NOT to use

- When you have only a single train–test split or no cross-validation structure; background distribution requires repeated shuffled cross-validation runs.
- When the input is already a hand-curated list of metabolites or a pre-filtered feature table; thresholding is needed at the model evaluation stage, not downstream.
- When metabolite annotations or mechanistic relationships are the primary goal and you do not need statistical validation of prediction accuracy.

## Inputs

- Spearman correlation coefficient (SCC) values for each metabolite from cross-validated predictions on observed data
- Paired microbiome abundance table (samples × microbial features)
- Paired metabolome abundance table (samples × metabolite features)
- Pre-defined network hyperparameters (layer size, number of layers, L2 penalty, dropout rate)
- Number of background iterations and cross-validation fold structure

## Outputs

- 95th percentile SCC threshold cutoff value (one per dataset)
- Binary classification: well-predicted vs. not well-predicted metabolites
- Count of well-predicted metabolites and percentage relative to total
- Filtered feature attribution score matrix containing only well-predicted metabolites

## How to apply

Generate a null (background) distribution of Spearman correlation coefficients by performing multiple iterations (typically ≥10) of cross-validated model training on randomly shuffled microbiome-metabolome data (shuffle samples independently for both modalities). Collect all SCC values across all metabolites and iterations from the shuffled runs. Compute the 95th percentile of this background SCC distribution—this becomes your significance threshold. Apply the threshold to the observed (real data) cross-validation results: classify any metabolite with SCC above the 95th percentile background cutoff as 'well-predicted'. Use this classification to filter the feature attribution score matrix before subsequent analyses such as biclustering or module enrichment testing. The rationale is that correlations exceeding the shuffled background represent signal unlikely due to random association.

## Related tools

- **MiMeNet** (Multi-layer perceptron neural network that predicts metabolite abundances from microbiome features; generates cross-validated SCCs and implements threshold determination) — https://github.com/YDaiLab/MiMeNet
- **SciPy (Spearman correlation)** (Computes Spearman rank correlation coefficients between predicted and observed metabolite abundances)
- **scikit-learn (MLPRegressor)** (Implements multi-layer perceptron regression; used to train models on shuffled and real data)
- **NumPy** (Shuffles microbiome and metabolome arrays independently; computes percentile of background SCC distribution)
- **MelonnPan** (Elastic Net–based baseline for metabolite prediction; used for comparative benchmarking of threshold performance) — https://github.com/biobakery/melonnpan

## Examples

```
python MiMeNet_train.py -micro data/IBD/microbiome_PRISM.csv -metab data/IBD/metabolome_PRISM.csv -num_run_cv 10 -num_background 100 -output IBD
```

## Evaluation signals

- 95th percentile cutoff values are dataset-specific and reflect background noise; for IBD (PRISM), cystic fibrosis, and soil datasets, expect cutoffs of 0.136, 0.129, and 0.410 respectively (higher thresholds in soil may indicate longitudinal structure or lower microbe–metabolite coupling).
- Well-predicted metabolite count is reproducible across repeated threshold calculations from independently shuffled backgrounds; the article reports consistent counts (198→366, 104→143, 4→29 across datasets).
- Mean SCC for well-predicted metabolites is substantially higher than the mean across all metabolites; mean SCC ranges from observed data (0.108→0.309, 0.276→0.457, −0.272→0.264) should show improvement over baseline linear models.
- Shuffled background SCC distribution shows no systematic correlation with observed metabolite SCC; overlap between background and observed distributions confirms the threshold is empirically justified.
- Feature attribution scores derived from well-predicted metabolites yield meaningful functional modules with significant enrichment patterns (tested by Wilcoxon rank-sum, p<0.05) between phenotypic groups.

## Limitations

- Threshold cutoff is sensitive to the quality and size of the training data; datasets with fewer samples or metabolites (e.g., soil: 85 metabolites total, only 29 well-predicted) may yield higher percentile thresholds and fewer reliable predictions.
- The 95th percentile is empirically chosen but not theoretically justified; alternative percentiles (90th, 97.5th) may be appropriate depending on stringency requirements.
- Not all metabolites may be genuinely associated with microbes in the ecosystem; some well-predicted metabolites may reflect indirect or compositional artifacts rather than causal microbe–metabolite relationships.
- Background distribution generation requires substantial computational cost (100 or more iterations of cross-validation on shuffled data); the article does not detail sensitivity to the number of background iterations.
- Threshold determination assumes independence of shuffled microbiome and metabolome samples; longitudinal or paired sampling designs (noted in soil data) may violate this assumption and inflate apparent SCC values.

## Evidence

- [results] MiMeNet then generates a background distribution of SCCs through multiple iterations of shuffling the dataset and performing a cross-validated evaluation on the shuffled set: "MiMeNet then generates a background distribution of SCCs through multiple iterations of shuffling the dataset and performing a cross-validated evaluation on the shuffled set"
- [methods] We then defined a metabolite as well-predicted if its SCC is above the 95th percentile of the background correlations: "We then defined a metabolite as well-predicted if its SCC is above the 95th percentile of the background correlations"
- [results] the cutoffs for SCCs between the predicted and observed abundances of metabolites were found to be 0.136, 0.129, and 0.410 for the IBD (PRISM), cystic fibrosis, and soil datasets, respectively: "the cutoffs for SCCs between the predicted and observed abundances of metabolites were found to be 0.136, 0.129, and 0.410 for the IBD (PRISM), cystic fibrosis, and soil datasets, respectively"
- [results] This background distribution of SCCs is then used to determine a cutoff for significantly well-predicted metabolites: "This background distribution of SCCs is then used to determine a cutoff for significantly well-predicted metabolites"
- [readme] Generate background distribution by shuffling dataset and cross-validation: "Generate background distribution by shuffling the dataset and performing a cross-validated evaluation on the shuffled set"
- [discussion] We also observed a higher threshold value for the soil data (Fig 3A–3C), which may be due to the longitudinal observations.: "We also observed a higher threshold value for the soil data (Fig 3A–3C), which may be due to the longitudinal observations."
