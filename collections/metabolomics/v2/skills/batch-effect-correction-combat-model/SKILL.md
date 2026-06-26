---
name: batch-effect-correction-combat-model
description: Use when your metabolomics matrix shows evidence of systematic variation
  correlated with batch/run assignment (detectable via PCA separation by batch, elevated
  batch-dependent variance, or RLA plots showing non-zero median log-ratios).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - dbnorm
  - sva
  - R
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1038/s41598-021-84824-3
  title: Dbnorm
- doi: 10.1007/s12561-013-9081-1
  title: ''
evidence_spans:
- dbnorm (V-0.2.2) A package for drift across batches normalization and visualization
- ComBat(parametric and non-parametric)-model [PMID:16632515] from sva package [PMID:22257669]
- dbnorm contains R functions which allow visualization and removal of technical heterogeneity
- '*dbnorm* contains R functions which allow visualization and removal of technical
  heterogeneity'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_dbnorm_cq
    doi: 10.1038/s41598-021-84824-3
    title: Dbnorm
  dedup_kept_from: coll_dbnorm_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41598-021-84824-3
  all_source_dois:
  - 10.1038/s41598-021-84824-3
  - 10.1007/s12561-013-9081-1
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# batch-effect-correction-combat-model

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Apply parametric or non-parametric ComBat models from the sva package via dbnorm to remove batch effects and technical heterogeneity from metabolomics datasets. This skill uses empirical Bayes methods to adjust feature intensities for known batch assignments, preserving biological signal while standardizing technical variation across analytical runs.

## When to use

Your metabolomics matrix shows evidence of systematic variation correlated with batch/run assignment (detectable via PCA separation by batch, elevated batch-dependent variance, or RLA plots showing non-zero median log-ratios). Input must be log2-scaled, in CSV format with samples in rows and metabolic features in columns, and you must have an explicit batch assignment vector labeling each sample's analytical batch.

## When NOT to use

- Input data is not log2-scaled or contains zero/missing values without imputation (use emvd or emvf first)
- No explicit batch variable is available or batches cannot be clearly assigned to samples
- Dataset has fewer than ~20 samples per batch or extreme batch size imbalance (ComBat parameter estimation may be unstable; consider ber or ber-bagging instead)
- Batch effect is confounded with biological grouping of interest (correction will remove signal of interest; use design matrix or other covariate adjustment methods)

## Inputs

- log2-normalized metabolomics matrix (CSV format; samples × features)
- batch assignment vector (sample-to-batch mapping)
- preprocessed metabolomics data in dbnorm-compatible format

## Outputs

- batch-corrected metabolomics matrix (same dimensions and format as input)
- PCA and Scree plots (PDF) showing batch effect removal
- RLA (Relative Log Abundance) plots (HTML/Viewer panel)
- Correlation plots and Adjusted R-squared comparison (PDF and CSV)
- Diagnostic CSV files quantifying residual batch variance per feature

## How to apply

Load the log2-normalized metabolomics matrix (rows=samples, columns=features) and batch assignment vector into R. Call either dbnormPcom() for parametric ComBat (assumes normal error distribution within batches) or dbnormNPcom() for non-parametric ComBat (makes no distributional assumption) via dbnorm. Parametric is recommended when batch sample sizes are large and roughly balanced; non-parametric is safer for small or imbalanced batches. Both functions internally call sva::ComBat and output corrected data, PCA/RLA diagnostic plots, and an Adjusted R-squared matrix showing batch variance explained before and after correction. Verify success by confirming Adjusted R-squared decreases substantially post-correction and that PCA plots show reduced batch clustering while preserving sample-level biological structure.

## Related tools

- **dbnorm** (Primary R package wrapping ComBat functions (dbnormPcom, dbnormNPcom) and providing visualization and diagnostic functions for batch effect correction in metabolomics) — https://github.com/NBDZ/dbnorm
- **sva** (Bioconductor package providing the underlying ComBat parametric and non-parametric empirical Bayes algorithms called by dbnorm) — https://bioconductor.org/packages/sva
- **R** (Statistical computing environment required to execute dbnorm and sva functions)

## Examples

```
dbnormPcom(data)
OR
dbnormNPcom(data)
```

## Evaluation signals

- Adjusted R-squared for batch effect decreases substantially (by >50%) on the majority of features post-correction compared to raw data
- PCA plot shows reduced clustering by batch assignment after correction, while sample replicates (QC or biological replicates) remain proximal
- RLA (Relative Log Abundance) median log-ratios per batch shift toward zero post-correction; inter-quartile ranges should narrow
- Corrected data retains expected biological groupings (e.g., case vs. control, tissue type) visible in unsupervised clustering or PCA, indicating preservation of true signal
- Output CSV files contain no NaN or Inf values and have identical dimensions to input matrix

## Limitations

- ComBat assumes a linear batch effect model; non-linear batch drifts or interactions with biological variables may not be fully corrected
- Parametric ComBat requires sufficient samples per batch (~20+) for stable shrinkage parameter estimation; small or severely imbalanced batch designs may fail or produce unreliable corrections
- The method cannot distinguish batch effects from biological effects when batches are perfectly confounded with a phenotype; use design matrices or post-hoc covariate adjustment if available
- dbnormPcom and dbnormNPcom are computationally intensive for datasets with >2000 features; README recommends Visodbnorm function for visualization with <2000 features
- Imputation of missing values (zero or NA) must precede ComBat application; dbnorm provides emvd and emvf functions but imputation strategy choice affects downstream results and is not decided by the model

## Evidence

- [other] dbnorm implements ComBat (parametric and non-parametric) models from the sva package as conventional functions for batch effect correction based on statistical models to remove technical heterogeneity from metabolomics datasets.: "dbnorm implements ComBat (parametric and non-parametric) models from the sva package as conventional functions for batch effect correction based on statistical models"
- [readme] ComBat(parametric and non-parametric)-model [PMID:16632515] from sva package [PMID:22257669]: "ComBat(parametric and non-parametric)-model [PMID:16632515] from sva package [PMID:22257669]"
- [readme] The *dbnorm* package allows user to inspect the structure and quality of large metabolomics datasets both in macroscopic and microscopic scales at the sample batch level and metabolic feature level: "the *dbnorm* package allows user to inspect the structure and quality of large metabolomics datasets both in macroscopic and microscopic scales at the sample batch level and metabolic feature level"
- [readme] Data to be uploaded must be normalized and scaled on the log2 to account for the high abundance features (variables) by which technical heterogeneity might be overlooked.: "Data to be uploaded must be normalized and scaled on the log2 to account for the high abundance features"
- [readme] This function is suggested for less than 2000 features (variables) for better computational speed.: "This function is suggested for less than 2000 features (variables) for better computational speed"
- [readme] Graphical check such as *PCA* plot, *Scree* plot and *Correlation* plot compiled into a **PDF** (saved in the working directory) and the **.csv** (saved in a folder, intiate with *Rtmpe*, in Users's Temporary directory) for corrected dataset based on either of applied model: "Graphical check such as *PCA* plot, *Scree* plot and *Correlation* plot compiled into a **PDF** for corrected dataset"
- [readme] Bagging model is performed using partial bagging with n=150 bootstrap samples: "Bagging model is performed using partial bagging with n=150 bootstrap samples"
