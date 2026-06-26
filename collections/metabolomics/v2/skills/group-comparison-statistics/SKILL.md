---
name: group-comparison-statistics
description: Use when after data integration, batch correction, and sample separation
  when you have a feature-by-sample abundance matrix (finalData) and corresponding
  sample group labels (finalLabel), and your research goal is to identify which metabolites
  significantly differ between experimental groups for.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - LargeMetabo
  - Marker_Identify
  - e1071
  - FSelector
  - mixOmics
  - siggenes
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1093/bib/bbac455
  title: LargeMetabo
evidence_spans:
- install_github("LargeMetabo/LargeMetabo", force = TRUE, build_vignettes = TRUE)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_largemetabo_cq
    doi: 10.1093/bib/bbac455
    title: LargeMetabo
  dedup_kept_from: coll_largemetabo_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bib/bbac455
  all_source_dois:
  - 10.1093/bib/bbac455
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# group-comparison-statistics

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Apply statistical tests to identify metabolic markers that differentiate between sample groups in large-scale metabolomic datasets. This skill encompasses 13 strategies including fold-change (FC), t-test, Wilcoxon rank sum (WRS), and machine-learning-based methods to rank and select features by their discriminatory power.

## When to use

Apply this skill after data integration, batch correction, and sample separation when you have a feature-by-sample abundance matrix (finalData) and corresponding sample group labels (finalLabel), and your research goal is to identify which metabolites significantly differ between experimental groups for downstream marker annotation or pathway enrichment.

## When NOT to use

- Do not use when input data is already a filtered set of pre-selected markers or when sample group labels are missing or ambiguous.
- Do not apply if data has not undergone batch effect removal, as unwanted variations across analytical experiments will confound statistical comparisons.
- Do not use univariate methods (t-test, FC) when the number of features far exceeds the number of samples and multicollinearity is suspected; prefer machine-learning-based feature selection in such high-dimensional scenarios.

## Inputs

- finalData: feature-by-sample abundance matrix (rows=metabolites, columns=samples)
- finalLabel: vector of sample group assignments (e.g., disease/control labels)

## Outputs

- MarkerResult object containing ranked metabolite table (e.g., FC_table)
- Table with metabolite identifiers, statistical scores/fold-change values, and rankings

## How to apply

Load the MarkerData object containing finalData (metabolite abundance matrix) and finalLabel (sample group assignments) into R. Select an appropriate statistical method from the 13 available strategies based on your data distribution and experimental design: fold-change (FC) for simple ranking by magnitude; t-test or Wilcoxon rank sum for univariate statistical significance; PLS-DA or OPLS-DA for multivariate group separation; or machine-learning methods (RF-RFE, SVM-RFE, Relief) for feature importance ranking when dealing with high-dimensional data. Call Marker_Identify(finalData, finalLabel, method='<method_name>') to compute rankings and extract the resulting ranked table (e.g., FC_table for fold-change). The output MarkerResult object contains ranked metabolite identifiers with their statistical scores or feature importance values, which can be filtered by p-value threshold or ranking cutoff before downstream annotation.

## Related tools

- **Marker_Identify** (Core LargeMetabo function that computes statistical rankings across 13 marker identification strategies) — https://github.com/LargeMetabo/LargeMetabo
- **e1071** (Provides SVM-based classification and feature elimination for SVM-RFE method)
- **FSelector** (Implements correlation-based feature selection (CFS) and entropy-based filter methods)
- **mixOmics** (Provides PLS-DA and OPLS-DA multivariate discrimination analysis)
- **siggenes** (Implements Significance Analysis for Microarrays (SAM) statistical method)

## Examples

```
finalData <- MarkerData$finalData
finalLabel <- MarkerData$finalLabel
MarkerResult <- Marker_Identify(finalData, finalLabel, method = "FC")
MarkerResult$FC_table[1:5,]
```

## Evaluation signals

- MarkerResult object successfully returns a ranked table with metabolite identifiers, statistical scores (p-values, fold-change values, or feature importance ranks), and ordering consistent with the chosen method's criteria.
- For fold-change method: FC_table contains ranked metabolites with fold-change magnitudes and directionality (upregulated vs. downregulated) relative to sample groups.
- For statistical tests: output includes p-values or adjusted p-values; check that at least some features show p < 0.05 or meet the expected significance threshold.
- For machine-learning methods: feature importance or ranking scores are inversely correlated with method-specific error metrics (e.g., out-of-bag error for random forest).
- Ranked marker list is reproducible when applied with the same input data and parameters, and top-ranked metabolites are biologically interpretable in the context of the experimental design.

## Limitations

- Fold-change method ranks by magnitude alone and does not incorporate statistical significance, potentially inflating small but highly variable changes.
- Univariate methods (t-test, WRS) do not account for correlations among metabolites and may identify spurious markers in high-dimensional data.
- Machine-learning methods (RF-RFE, SVM-RFE) require careful cross-validation and hyperparameter tuning to avoid overfitting; performance depends on sample size and class balance.
- All methods assume that sample group labels are correctly assigned and representative; mislabeled or contaminated samples will bias marker rankings.
- The choice of method significantly impacts results; no single method is universally optimal across all metabolomic datasets and experimental designs.

## Evidence

- [readme] In the marker identification step, there are 13 popular strategies to identify metabolic markers for the given dataset: "In the marker identification step, there are 13 popular strategies to identify metabolic markers for the given dataset"
- [other] Marker_Identify() function with method='FC' accepts a data matrix (finalData) and sample labels (finalLabel), returning a MarkerResult object containing FC_table with ranked metabolic markers: "The Marker_Identify() function with method='FC' accepts a data matrix (finalData) and corresponding sample labels (finalLabel), and returns a MarkerResult object containing an FC_table with ranked"
- [readme] The 13 strategies include fold change, t-test, Chi-squared test, CFS, entropy-based filter, linear models with empirical Bayes, Relief, RF-RFE, SAM, SVM-RFE, and Wilcoxon rank sum: "These strategies include fold change (FC), partial least squares discrimination analysis (PLS-DA), orthogonal PLS-DA (OPLS-DA), Student's t-test, Chi-squared test, correlation-based feature selection"
- [readme] After data integration, batch effects removal is essential before marker identification to remove unwanted variations among different batches: "After data integration, it was essential to remove the unwanted variations among different batches"
- [readme] Example invocation showing extraction of FC_table from MarkerResult: "MarkerResult <- Marker_Identify(finalData, finalLabel, method = "FC")
    MarkerResult$FC_table[1:5,]"
