---
name: microbiome-metabolome-data-preprocessing
description: Use when when starting with raw paired microbiome (16S rRNA, metagenomic taxonomic or functional features) and metabolome (LC-MS/MS, NMR) count tables from the same biospecimens, and planning to train prediction models or co-abundance networks.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3174
  - http://edamontology.org/topic_0637
  - http://edamontology.org/topic_3407
  tools:
  - MiMeNet
  - scikit-learn (MLPRegressor)
  - ADAM optimizer
  - ReLU activation
  - NumPy
  - Elastic Net
  - TensorFlow or PyTorch
  - scikit-learn
  - Seaborn
  - Python
  - SciPy
  - Pandas
  techniques:
  - LC-MS
  - tandem-MS
  - NMR
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# microbiome-metabolome-data-preprocessing

## Summary

Preparation and normalization of paired microbiome and metabolome feature tables for downstream prediction modeling, including low-abundance filtering, compositional transformations (CLR or relative abundance), and feature quality control. This skill ensures that heterogeneous omics measurements are made commensurable and that rare features do not dominate the learning signal.

## When to use

When starting with raw paired microbiome (16S rRNA, metagenomic taxonomic or functional features) and metabolome (LC-MS/MS, NMR) count tables from the same biospecimens, and planning to train prediction models or co-abundance networks. Apply this skill before neural network training, module clustering, or any cross-validated evaluation on microbiome-metabolome datasets.

## When NOT to use

- Input feature tables are already normalized and filtered (e.g., already CLR-transformed or rarefied)
- Microbiome and metabolome measurements come from different or unpaired biospecimens
- Analysis goal does not require training a predictive model; descriptive alpha/beta diversity analysis may not need CLR transformation

## Inputs

- raw microbiome count table (samples × microbes/features, integer or relative abundance format)
- raw metabolome count table (samples × metabolites/features, LC-MS/MS or NMR intensity format)
- optional: sample metadata (e.g., diagnosis labels, cohort identifiers)

## Outputs

- filtered microbiome feature table (samples × microbes, after <10% prevalence removal)
- filtered metabolome feature table (samples × metabolites, after <10% prevalence removal)
- transformation metadata (normalization type: CLR or RA, pseudocount value if CLR, any filtering thresholds applied)

## How to apply

Load raw paired microbiome and metabolome count tables (samples × features format). First, remove any feature (microbial or metabolite) present in fewer than 10% of samples to eliminate sparse, likely artifactual features. Second, apply compositional transformation: either centered log-ratio (CLR) with pseudocount +1, or relative abundance (RA) normalization. The choice between CLR and RA affects downstream correlation estimates; CLR is recommended for datasets with compositional structure (cystic fibrosis, soil), while RA may suffice for well-characterized cohorts like IBD PRISM. Document the transformation applied, as it influences background distribution generation and well-predicted metabolite thresholds. Return filtered and normalized feature tables (same row/column structure) and record preprocessing parameters for reproducibility in external validation.

## Related tools

- **scikit-learn** (Preprocessing and normalization of feature tables; feature selection and filtering utilities)
- **SciPy** (Centered log-ratio transformation via logarithmic and geometric mean operations)
- **Pandas** (Loading, filtering, and reshaping CSV/TSV count tables and metadata)
- **NumPy** (Array operations for prevalence filtering and composition-altering transformations)

## Examples

```
python MiMeNet_train.py -micro data/IBD/microbiome_PRISM.csv -metab data/IBD/metabolome_PRISM.csv -micro_norm None -metab_norm CLR
```

## Evaluation signals

- Verify that no feature in output tables has <10% prevalence (sample coverage check)
- Confirm that CLR-transformed features have mean ≈ 0 across samples; RA features sum to 1.0 per sample
- Check that row and column counts match between input and output (only features below threshold removed)
- If CLR applied, verify that log-transformed denominators (geometric mean) do not yield infinite or NaN values
- Reproduce output on held-out samples using the same transformation parameters; identical results confirm deterministic preprocessing

## Limitations

- The 10% prevalence threshold is heuristic and may remove true rare features; datasets with sparse, true low-abundance species may require lower cutoffs
- CLR transformation with pseudocount +1 can bias small counts; alternative pseudocounts (e.g., half-minimum nonzero, Laplace) may be preferable for sparse data
- Choice of CLR vs. RA normalization affects subsequent model performance and threshold cutoffs; no universal guidance provided; empirical comparison (task_005) is recommended
- Paired sample assumption is critical; if microbiome and metabolome are from different biospecimens or time-points, compositional methods may mislead
- For longitudinal or hierarchical study designs (e.g., repeated measures, biocrust time-series), batch effects and temporal autocorrelation are not addressed in this preprocessing step

## Evidence

- [methods] Remove features present in <10% of samples: "Any input or output feature that is present in less than 10% of samples was removed"
- [methods] CLR transformation with pseudocount +1: "centered log-ratio (CLR) transformation with pseudocount +1"
- [methods] Relative abundance normalization alternative: "relative abundance (RA) normalization"
- [abstract] CLR vs RA effects on downstream prediction: "prediction correlations were comparable between CLR and relative abundance transformations, while CLR showed increased correlations in cystic fibrosis and soil datasets"
- [methods] Dataset-specific preprocessing parameters: "centered log-ratio transformation (with pseudocount of 1; exception: IBD PRISM microbes in relative abundance)"
- [methods] Preprocessing prior to neural network training: "Load and preprocess the three paired microbiome-metabolome datasets"
