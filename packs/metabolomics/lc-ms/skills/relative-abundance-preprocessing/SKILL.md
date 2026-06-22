---
name: relative-abundance-preprocessing
description: Use when when you have raw count tables from 16S rRNA sequencing (microbiome) or LC-MS/MS metabolomics (metabolome) and need to train neural network or regression models for microbe-metabolite relationship prediction.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3174
  - http://edamontology.org/topic_3697
  - http://edamontology.org/topic_0622
  tools:
  - Elastic Net
  - MiMeNet
  - TensorFlow or PyTorch
  - scikit-learn
  - Seaborn
  - Python
  - MelonnPan
  - pandas
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

# relative-abundance-preprocessing

## Summary

Normalize microbiome and metabolome count tables to relative abundance (RA) or centered log-ratio (CLR) transformed compositions before predictive modeling. This preprocessing step standardizes feature scales and handles zero-inflation in compositional microbiome data, enabling fair comparison of transformation effects on downstream prediction performance.

## When to use

When you have raw count tables from 16S rRNA sequencing (microbiome) or LC-MS/MS metabolomics (metabolome) and need to train neural network or regression models for microbe-metabolite relationship prediction. Use this skill when comparing whether CLR or RA normalization produces better-predicted metabolite counts or prediction correlations in a specific disease cohort (e.g., IBD vs. controls).

## When NOT to use

- Input data is already normalized or transformed (e.g., already CLR, relative abundance, or log-scaled). Check data descriptors and apply 'None' normalization flag in tools like MiMeNet.
- Metabolite data lacks sufficient compositional structure (e.g., proteomics absolute abundance, single-metabolite standards rather than untargeted profiles). CLR is designed for compositional data where features sum to a constant per sample.
- Microbiome data consists of functional profiles or pathways that are not compositional in nature. RA/CLR transformations assume zero-sum constraints; independent abundance measurements should not be transformed.

## Inputs

- Raw microbiome count table (16S rRNA, taxonomic or functional features; samples × microbes)
- Raw metabolome count table (LC-MS/MS; samples × metabolites)
- Sample metadata (optional: disease status, cohort labels for downstream enrichment)

## Outputs

- CLR-transformed microbiome matrix (samples × microbes, log-centered compositions)
- CLR-transformed metabolome matrix (samples × metabolites, log-centered compositions)
- Relative-abundance microbiome matrix (samples × microbes, proportions ≤1)
- Relative-abundance metabolome matrix (samples × metabolites, proportions ≤1)
- Feature-retention report (count of features removed at 10% prevalence threshold)

## How to apply

Load paired microbiome and metabolome count matrices (samples × features). Apply one or both transformations in parallel: (1) relative abundance (RA): divide each feature by sample total and scale to proportions; (2) centered log-ratio (CLR): add pseudocount +1, log-transform, and center by subtracting the geometric mean of log-transformed features. Remove features present in <10% of samples before transformation to reduce sparsity. Train identical downstream models (e.g., MiMeNet neural networks with fixed hyperparameters: ReLU, L2=0.001, dropout=0.5, layer size=512, 1 hidden layer) on each transformed dataset using identical cross-validation folds (10 iterations of 10-fold CV). Compare prediction performance using mean Spearman correlation coefficients (SCCs) and counts of well-predicted metabolites at the 95th percentile of background SCC distribution. Document whether CLR or RA produces higher correlations and more well-predicted metabolites in your specific cohort (e.g., IBD PRISM showed comparable CLR/RA correlations, but CLR improved cystic fibrosis and soil).

## Related tools

- **MiMeNet** (accepts normalized microbiome and metabolome inputs (RA, CLR, or None) via -micro_norm and -metab_norm flags; outputs prediction correlations and module assignments stratified by transformation type) — https://github.com/YDaiLab/MiMeNet
- **MelonnPan** (linear regression-based metabolite prediction tool that can be trained on transformed microbial features; uses Elastic Net with relative-abundance or other normalized inputs) — https://github.com/biobakery/melonnpan
- **scikit-learn** (preprocessing utilities for log-transformation, scaling, and feature filtering in Python pipelines)
- **pandas** (data frame manipulation for feature filtering, composition normalization, and pseudocount addition in Python)

## Examples

```
python MiMeNet_train.py -micro data/IBD/microbiome_PRISM.csv -metab data/IBD/metabolome_PRISM.csv -micro_norm CLR -metab_norm CLR -num_run_cv 10 -num_cv 10 -output IBD_CLR_normalized
```

## Evaluation signals

- Feature prevalence: verify that all retained features are present in ≥10% of samples; count removed features and confirm <10% prevalence cutoff was applied
- Composition constraint: for CLR, verify that log-transformed, centered feature values sum to ~0 per sample (within floating-point tolerance); for RA, verify all feature rows sum to ~1.0 per sample
- Pseudocount addition: confirm pseudocount +1 was added to all counts before log-transformation to handle zeros; raw count tables must not contain exact zeros after transformation
- Spearman correlation improvement: compare mean SCC between CLR and RA across identical CV folds; CLR should show equal or improved correlations vs. RA in most datasets; document dataset-specific differences (e.g., IBD comparable, CF improved, soil improved)
- Well-predicted metabolite count consistency: verify that well-predicted metabolite counts are reproducible across repeated CV iterations; higher counts for CLR would indicate stronger metabolite predictability

## Limitations

- CLR transformation is undefined for samples with all-zero features; pseudocount +1 is a heuristic choice and may not be optimal for all microbiome compositionality profiles.
- Relative abundance normalization discards absolute abundance information; rare but biologically important features may be downweighted relative to highly abundant taxa even after RA scaling.
- No universally optimal transformation: IBD (PRISM) showed comparable CLR and RA correlations, while cystic fibrosis and soil showed CLR advantage; transformation choice may be dataset- or disease-context dependent. Prior benchmarking on similar cohorts is recommended.
- The 10% prevalence filter is arbitrary and may remove biologically relevant rare features; tune this threshold based on study design and statistical power.
- External validation datasets (e.g., LifeLines-DEEP for IBD) may have different baseline feature prevalence, requiring re-filtering or tolerance adjustment to maintain consistency.

## Evidence

- [methods] Remove features present in <10% of samples: "Any input or output feature that is present in less than 10% of samples was removed"
- [methods] CLR transformation with pseudocount +1: "centered log-ratio (CLR) transformation with pseudocount +1, and relative abundance (RA) normalization"
- [methods] Parallel transformation comparison approach: "Prepare two parallel input transformations: centered log-ratio (CLR) transformation with pseudocount +1, and relative abundance (RA) normalization"
- [readme] MiMeNet tool configuration for RA vs CLR: "Transform the microbial features into relative abundance (RA) or center log-ratio (CLR). If the data is already transformed, apply 'None' to skip transformation."
- [other] Dataset-specific transformation performance findings: "In the IBD (PRISM) dataset, prediction correlations were comparable between CLR and relative abundance transformations, while CLR showed increased correlations in cystic fibrosis and soil datasets"
