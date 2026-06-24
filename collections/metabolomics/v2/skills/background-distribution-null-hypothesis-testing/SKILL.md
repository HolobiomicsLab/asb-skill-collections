---
name: background-distribution-null-hypothesis-testing
description: Use when when predicting one data modality (e.g., metabolite abundances)
  from another (e.g., microbiome composition) and you need to distinguish genuine
  microbe–metabolite associations from false positives driven by data compositionality,
  sample size artifacts, or confounding variation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
  edam_topics:
  - http://edamontology.org/topic_3174
  - http://edamontology.org/topic_3697
  - http://edamontology.org/topic_0621
  tools:
  - MiMeNet
  - scikit-learn
  - scipy.stats
  license_tier: restricted
derived_from:
- doi: 10.1371/journal.pcbi.1009021
  title: MiMeNet
evidence_spans:
- An MLPNN model is composed of multiple fully connected hidden layers composed of
  perceptrons
- MiMeNet is an integrative MLPNN, which trains models to accurately predict the metabolome
  based on a microbiome
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

# background-distribution-null-hypothesis-testing

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Generate an empirical null distribution by shuffling paired input features independently and re-running cross-validation, then use percentile thresholds from this background to identify statistically significant predictions. This skill decouples true signal from spurious correlations arising from compositional data or batch effects.

## When to use

When predicting one data modality (e.g., metabolite abundances) from another (e.g., microbiome composition) and you need to distinguish genuine microbe–metabolite associations from false positives driven by data compositionality, sample size artifacts, or confounding variation. Essential when the input and output are measured on the same samples but may have spurious correlations by chance.

## When NOT to use

- Input microbiome and metabolome are from different cohorts or samples — background shuffling assumes paired measurements on identical sample sets.
- Sample size is very small (n < 20) — percentile estimation from background becomes unstable; consider parametric null models instead.
- You have a priori mechanistic knowledge linking specific taxa to metabolites and wish to test directed hypotheses rather than genome-wide association.

## Inputs

- paired microbiome abundance table (samples × microbial features; CLR-transformed or relative abundance)
- paired metabolomic abundance table (samples × metabolites; CLR-transformed or relative abundance)
- trained cross-validated prediction model(s) with fixed hyperparameters
- number of background iterations (n, recommended ≥10)

## Outputs

- background distribution of prediction metrics (e.g., SCC values across all shuffled CV folds)
- 95th percentile threshold from background distribution
- binary classification of metabolites as 'well-predicted' (observed metric > 95th percentile background) vs. not
- count of significantly well-predicted metabolites per condition

## How to apply

Execute k-fold cross-validation on your paired microbiome and metabolomic datasets (e.g., 10-fold CV over n iterations, such as 100), but in parallel shuffle the microbiome and metabolome data independently before each fold to eliminate true biological associations while preserving the statistical structure of each modality. For each shuffled fold, train the same prediction model (e.g., MLPNN with identical hyperparameters) and record the prediction metric (e.g., Spearman correlation coefficient, SCC) for each output feature. Aggregate these background metrics across all shuffled folds to build an empirical null distribution. Compare observed metrics from unshuffled cross-validation against this background: features with observed metrics above a high percentile (e.g., 95th percentile of the background distribution) are classified as significantly well-predicted. This approach accounts for the compositional nature of microbiome data and the multiple-comparison problem inherent in metabolomic prediction.

## Related tools

- **MiMeNet** (neural network framework that trains MLPNN models on paired microbiome–metabolome data and applies background-distribution-based thresholding to identify well-predicted metabolites) — https://github.com/YDaiLab/MiMeNet
- **scikit-learn** (provides cross-validation iterators (cross_val_score, KFold) and model selection utilities used in background distribution generation)
- **scipy.stats** (computes Spearman correlation coefficients and percentile calculations on shuffled and observed distributions)

## Examples

```
python MiMeNet_train.py -micro data/IBD/microbiome_PRISM.csv -metab data/IBD/metabolome_PRISM.csv -micro_norm None -metab_norm CLR -num_background 100 -num_run_cv 10 -num_cv 10 -threshold 0.95 -output results/IBD
```

## Evaluation signals

- Background distribution shape: empirical null should be approximately symmetric or centered near zero correlation; high variance or bimodality may indicate improper shuffling or model instability.
- Percentile cutoff validity: the 95th percentile of the background should lie below mean observed SCC of true well-predicted metabolites; if not, the cutoff is too lenient.
- Reproducibility: background distribution from multiple runs (e.g., 10 iterations of 100-fold shuffled CV) should yield stable percentile thresholds (±<5% variation).
- Comparative metric: count of well-predicted metabolites should be substantially higher in unshuffled CV than in background; if counts are similar, signal-to-noise ratio is poor.
- External validation: well-predicted metabolites from one cohort should maintain SCC > background threshold when evaluated on held-out external samples.

## Limitations

- Shuffling destroys all dependencies between microbiome and metabolome; this is a strength for null hypothesis construction but assumes microbes and metabolites are exchangeable units (violated if temporal or phylogenetic structure is informative).
- Percentile threshold (e.g., 95th) is arbitrary and may not reflect domain-specific significance; consider Bonferroni or FDR-corrected thresholds for large metabolite panels.
- Assumes paired samples; mismatched cohorts or technical batch effects not represented in shuffling can inflate false positives.
- Computationally expensive: 100 iterations of 10-fold CV with shuffled data requires 1,000 model trainings; MiMeNet recommends ≥10 background iterations as practical minimum.
- Not all metabolites may be associated with microbes, resulting in lower prediction correlations; background distribution will reflect this non-specific signal, raising the threshold.

## Evidence

- [methods] Generate a background SCC distribution by shuffling microbiome and metabolome data independently, re-running 10-fold cross-validation 100 times, and identifying metabolites with SCC >95th percentile as well-predicted.: "Generate a background SCC distribution by shuffling microbiome and metabolome data independently, re-running 10-fold cross-validation 100 times, and identifying metabolites with SCC >95th percentile"
- [readme] MiMeNet generates a background of SCC values using a similar approach as in _Cross-Validated Evaluation_. However, to generate the background distribution of SCCs, the samples are randomly shuffled for each cross-validated iteration.: "MiMeNet generates a background of SCC values using a similar approach as in _Cross-Validated Evaluation_. However, to generate the background distribution of SCCs, the samples are randomly shuffled"
- [results] MiMeNet then generates a background distribution of SCCs through multiple iterations of shuffling the dataset and performing a cross-validation on the shuffled set: "MiMeNet then generates a background distribution of SCCs through multiple iterations of shuffling the dataset and performing a cross-validation on the shuffled set"
- [results] This background distribution of SCCs is then used to determine a cutoff for significantly well-predicted metabolites: "This background distribution of SCCs is then used to determine a cutoff for significantly well-predicted metabolites"
- [methods] We then defined a metabolite as well-predicted if its SCC is above the 95th percentile of the background correlations: "We then defined a metabolite as well-predicted if its SCC is above the 95th percentile of the background correlations"
