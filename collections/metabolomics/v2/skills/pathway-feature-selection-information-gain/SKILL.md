---
name: pathway-feature-selection-information-gain
description: Use when after computing a pathway dysregulation score matrix (PDSmatrix)
  from metabolite-to-pathway mappings, apply this skill when you need to reduce the
  dimensionality of pathway features and select only those pathways with sufficient
  information content to discriminate between phenotype classes.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3407
  tools:
  - Lilikoi v2.0
  - R
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1093/gigascience/giaa162
  title: Lilikoi V2.0
evidence_spans:
- The new Lilikoi v2.0 R package has implemented a deep-learning method for classification,
  in addition to popular machine learning methods.
- Lilikoi v2.0 is a modern, comprehensive package to enable metabolomics analysis
  in R programming environment.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lilikoi_v2_0_cq
    doi: 10.1093/gigascience/giaa162
    title: Lilikoi V2.0
  dedup_kept_from: coll_lilikoi_v2_0_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/gigascience/giaa162
  all_source_dois:
  - 10.1093/gigascience/giaa162
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Reconstruct significant-pathway feature selection with lilikoi.featuresSelection

## Summary

Uses information-gain-based feature selection to rank and filter pathways from a pathway dysregulation score (PDS) matrix by their relevance to phenotype, identifying the most discriminative metabolic pathways for downstream classification or regression analysis.

## When to use

After computing a pathway dysregulation score matrix (PDSmatrix) from metabolite-to-pathway mappings, apply this skill when you need to reduce the dimensionality of pathway features and select only those pathways with sufficient information content to discriminate between phenotype classes or predict a continuous outcome. Use it before machine learning or prognosis modeling to avoid overfitting and improve interpretability.

## When NOT to use

- Input is already a pre-filtered or manually curated set of pathways; feature selection is redundant.
- Phenotype data contains missing or misaligned sample labels that do not correspond row-wise to PDSmatrix columns.
- PDSmatrix contains only a small number of pathways (< 10); information-gain ranking may be unstable or uninformative.

## Inputs

- PDSmatrix (pathway-by-sample matrix of dysregulation scores, numeric)
- phenotype labels (vector of class labels or continuous outcome values)

## Outputs

- selected_Pathways_Weka (vector of selected pathway names and their information-gain scores)

## How to apply

Load the PDSmatrix (pathway-by-sample feature matrix) and phenotype labels into R. Apply the lilikoi.featuresSelection function with the information-gain method and a threshold of 0.50 to rank pathways by their mutual information with the phenotype and filter those meeting the threshold. The function outputs selected_Pathways_Weka, a vector of pathway names and their information-gain scores. Information-gain scores quantify how much knowing a pathway's dysregulation reduces uncertainty about the phenotype; pathways exceeding 0.50 are retained for subsequent analysis. This threshold balances feature reduction with retention of phenotype-relevant signal.

## Related tools

- **Lilikoi v2.0** (R package implementing lilikoi.featuresSelection function with information-gain method for pathway feature selection) — https://github.com/lanagarmire/lilikoi2
- **R** (Programming environment and runtime for Lilikoi v2.0)

## Examples

```
selected_Pathways_Weka <- lilikoi.featuresSelection(PDSmatrix, threshold=0.50, method="gain")
```

## Evaluation signals

- selected_Pathways_Weka contains non-empty vector of pathway names with numeric information-gain scores all ≥ 0.50.
- Number of selected pathways is substantially smaller than input PDSmatrix rows, confirming dimensionality reduction.
- Selected pathways show improved discriminative power in downstream classification (e.g., higher cross-validation accuracy or AUC) compared to using all pathways.
- Information-gain scores are ranked monotonically; no duplicates or missing values in output.
- Pathways in selected_Pathways_Weka are a strict subset of the row names in the input PDSmatrix.

## Limitations

- Information-gain threshold of 0.50 is data-dependent and may require tuning for datasets with different phenotype distributions or pathway counts.
- Feature selection based on univariate information-gain does not account for pathway-pathway interactions or collinearity; selected pathways may be redundant.
- Method assumes discrete or discretized phenotype values; continuous outcomes may require prior binning, which can lose information.
- Selection is performed independently on the training set; without proper cross-validation during feature selection, performance may be overestimated.

## Evidence

- [other] The lilikoi.featuresSelection function operates on the PDSmatrix using the information-gain method with a threshold of 0.50 to select pathways significantly related to phenotype.: "The lilikoi.featuresSelection function operates on the PDSmatrix using the information-gain method with a threshold of 0.50 to select pathways significantly related to phenotype"
- [other] Apply the information-gain method for feature selection with threshold 0.50 in Lilikoi v2.0 to rank and filter pathways by their relevance to the phenotype.: "Apply the information-gain method for feature selection with threshold 0.50 in Lilikoi v2.0 to rank and filter pathways by their relevance to the phenotype"
- [readme] Lilikoi v2.0 is a modern, comprehensive package to enable metabolomics analysis in R programming environment.: "Lilikoi v2.0 is a modern, comprehensive package to enable metabolomics analysis in R programming environment"
- [readme] Select the most signficant pathway related to phenotype. selected_Pathways_Weka= lilikoi.featuresSelection(PDSmatrix,threshold= 0.50,method="gain"): "selected_Pathways_Weka= lilikoi.featuresSelection(PDSmatrix,threshold= 0.50,method="gain")"
