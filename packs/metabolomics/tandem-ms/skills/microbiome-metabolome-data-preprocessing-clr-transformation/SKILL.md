---
name: microbiome-metabolome-data-preprocessing-clr-transformation
description: Use when you have paired microbiome and metabolomic abundance tables (samples × features) with relative abundance or raw count values, and you are preparing data for downstream regression or neural network modeling of microbe-metabolite relationships.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3697
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0625
  tools:
  - MiMeNet
  - MelonnPan
  - scikit-bio
  - Pandas
  techniques:
  - LC-MS
  - tandem-MS
derived_from:
- doi: 10.1371/journal.pcbi.1009021
  title: MiMeNet
evidence_spans:
- An MLPNN model is composed of multiple fully connected hidden layers composed of perceptrons
- MiMeNet is an integrative MLPNN, which trains models to accurately predict the metabolome based on a microbiome
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

# microbiome-metabolome-data-preprocessing-clr-transformation

## Summary

Apply center log-ratio (CLR) transformation to microbiome relative abundance data and metabolomic abundance data to convert compositional count matrices into log-scale representations suitable for neural network training. This preprocessing step addresses the compositional nature of both data types and enables fair feature scaling before cross-validated model training.

## When to use

Apply this skill when you have paired microbiome and metabolomic abundance tables (samples × features) with relative abundance or raw count values, and you are preparing data for downstream regression or neural network modeling of microbe-metabolite relationships. Use CLR transformation specifically when the data are compositional (parts-of-a-whole, i.e., row sums to a constant) and you need to remove the bias introduced by the unit-sum constraint before fitting predictive models.

## When NOT to use

- Data are already CLR-transformed or otherwise log-normalized; applying CLR again will double-transform and distort relationships.
- Microbiome or metabolomic data are counts from non-compositional platforms (e.g., absolute quantification, QPCR); CLR is designed for relative-abundance or sequencing data.
- The analysis goal is to preserve original abundance scales for biomarker discovery or threshold-based clinical cutoffs; CLR removes absolute scale information.

## Inputs

- Microbiome abundance matrix (samples × microbial features; CSV format; raw counts or relative abundance)
- Metabolomic abundance matrix (samples × metabolite features; CSV format; raw counts or relative abundance)
- Optional: feature annotation table (metabolite IDs or functional labels)

## Outputs

- CLR-transformed microbiome abundance matrix (samples × microbial features; ready for modeling)
- CLR-transformed metabolomic abundance matrix (samples × metabolite features; ready for modeling)
- Feature presence/absence report (feature filtering summary: features retained after <10% threshold filtering)

## How to apply

Load paired microbiome (e.g., 16S rRNA-derived or taxonomic abundance) and metabolomic (e.g., LC-MS/MS or spectral abundance) count or relative abundance matrices with samples in rows and features in columns. Remove any features present in fewer than 10% of samples to eliminate sparse, uninformative signals. Apply center log-ratio (CLR) transformation: for each feature in each sample, compute (log of sample's feature abundance) − (mean log abundance across all features in that sample). This centers the log-transformed data and makes feature correlations more interpretable in high-dimensional space. Verify that output matrices have the same dimensions as input (after feature filtering) and that no NaN or infinite values are present (these indicate zero-abundance features that should have been filtered). The transformed data is then ready for cross-validation, neural network hyperparameter tuning, and model training.

## Related tools

- **MiMeNet** (Framework that applies CLR transformation as part of its data preprocessing pipeline before neural network training and metabolite prediction) — https://github.com/YDaiLab/MiMeNet
- **MelonnPan** (Elastic Net–based metabolite prediction tool that accepts both relative abundance (RA) and CLR-transformed input; used as a comparative baseline for MiMeNet) — https://github.com/biobakery/melonnpan
- **scikit-bio** (Python library providing CLR and other compositional data transformations; used by MiMeNet for preprocessing)
- **Pandas** (Python library for loading, filtering, and manipulating abundance matrices (CSV I/O and feature filtering by presence threshold))

## Examples

```
python MiMeNet_train.py -micro data/IBD/microbiome_PRISM.csv -metab data/IBD/metabolome_PRISM.csv -micro_norm None -metab_norm CLR -num_cv 10 -output results/
```

## Evaluation signals

- Output matrices have identical dimensions to input (after feature filtering by 10% presence threshold) and preserve sample order.
- CLR-transformed values are centered around zero (mean of log-transformed features per sample should be ~0); no NaN or infinite values are present in the output.
- Feature filtering correctly removes all features present in <10% of samples; feature count decreases or remains constant after filtering.
- Downstream neural network training converges without overflow/underflow errors and produces meaningful Spearman correlation coefficients (SCCs) between predicted and observed metabolite abundances (e.g., mean SCC > 0.1 on test folds).
- External validation on held-out samples shows consistent SCC distributions and well-predicted metabolite counts similar to internal cross-validation, indicating the transformation did not introduce data leakage or bias.

## Limitations

- CLR transformation requires all features to be positive (non-zero); zero abundances in the input must be handled (e.g., by pseudocount addition before transformation), which can bias rare features.
- The transformation is sample-wise (each sample's log-abundances are centered independently), so it does not account for inter-sample batch effects or sample-level covariates; external batch correction may be needed before CLR.
- CLR is reversible only up to an additive constant; absolute abundance information is lost, limiting downstream interpretation of metabolite or microbe absolute concentrations.
- Applying CLR to already-aggregated or heavily filtered data (e.g., only dominant taxa) may distort the relative abundance relationships compared to CLR applied to the full feature set.

## Evidence

- [other] Load raw microbiome (relative or CLR-transformed abundance) and metabolomic data (LC-MS/MS or 16S rRNA-derived, CLR-transformed) from the IBD (PRISM) or cystic fibrosis dataset, filtering out features present in <10% of samples.: "Load raw microbiome (relative or CLR-transformed abundance) and metabolomic data (LC-MS/MS or 16S rRNA-derived, CLR-transformed) from the IBD (PRISM) or cystic fibrosis dataset, filtering out"
- [methods] Any input or output feature that is present in less than 10% of samples was removed.: "Any input or output feature that is present in less than 10% of samples was removed"
- [readme] MiMeNet will perform a compositional transformation to relative abundance or centered log-ratio and filter low abundant microbial and metabolite features.: "MiMeNet will perform a compositional transformation to relative abundance or centered log-ratio and filter low abundant microbial and metabolite features."
- [readme] Transform the microbial features into relative abundance (RA) or center log-ratio (CLR). If the data is already transformed, apply 'None' to skip transformation.: "Transform the microbial features into relative abundance (RA) or center log-ratio (CLR). If the data is already transformed, apply 'None' to skip transformation."
- [readme] python MiMeNet_train.py -micro data/IBD/microbiome_PRISM.csv -metab data/IBD/metabolome_PRISM.csv -external_micro data/IBD/microbiome_external.csv -external_metab data/IBD/metabolome_external.csv -micro_norm None -metab_norm CLR: "python MiMeNet_train.py -micro data/IBD/microbiome_PRISM.csv -metab data/IBD/metabolome_PRISM.csv -external_micro data/IBD/microbiome_external.csv -external_metab data/IBD/metabolome_external.csv"
