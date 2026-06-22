---
name: metabolite-feature-flagging
description: Use when after drift correction and before imputation, when you have a MetaboSet object with LC-MS peak abundances and need to remove features with insufficient detection consistency across QC samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3520
  tools:
  - notame
  - R
  - Biobase
  - ExpressionSet
  techniques:
  - LC-MS
derived_from:
- doi: 10.3390/metabo10040135
  title: notame
- doi: 10.1093/bioinformatics/btr597
  title: ''
evidence_spans:
- This package can be used to analyze preprocessed LC-MS data in non-targeted metabolomics
- library(notame)
- reads them to R, conducts additional preprocessing and statistical analyses
- '```MetaboSet``` is built upon the ```ExpressionSet``` class from the Biobase package by Bioconductor'
- '```MetaboSet``` objects are the primary data structure of this package. ```MetaboSet``` is built upon the ```ExpressionSet``` class'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_notame_cq
    doi: 10.3390/metabo10040135
    title: notame
  dedup_kept_from: coll_notame_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3390/metabo10040135
  all_source_dois:
  - 10.3390/metabo10040135
  - 10.1093/bioinformatics/btr597
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-feature-flagging

## Summary

A quality-control filtering step that identifies and marks LC-MS metabolite features failing to meet minimum detection-rate thresholds across QC samples, preventing low-confidence features from downstream multivariate analysis. This skill operationalizes the flag_detection function in the notame workflow to enforce reproducibility criteria on feature abundance data.

## When to use

After drift correction and before imputation, when you have a MetaboSet object with LC-MS peak abundances and need to remove features with insufficient detection consistency across QC samples. Apply this when QC sample labels are present in the fData metadata and you want to enforce a minimum reproducibility cutoff (e.g., 70% QC detection rate) to filter out noise-prone or poorly ionizing compounds before statistical analysis.

## When NOT to use

- Input data lacks QC sample replicates or QC column in fData—flag_detection requires labeled QC samples to compute detection rates.
- Feature detection has already been filtered by upstream peak-picking software—applying redundant flagging may over-filter genuine low-abundance metabolites.
- Analysis goal requires retention of all detected features regardless of reproducibility (e.g., exploratory hypothesis generation from rare features)—flagging is irreversible without manual intervention.

## Inputs

- MetaboSet object (Biobase ExpressionSet subclass) with exprs (feature × sample abundance matrix), pData (sample metadata including QC labels), and fData (feature metadata with QC column)

## Outputs

- MetaboSet object with updated Flag column in fData marking features with detection rate < qc_limit threshold
- Filtered feature set (implicitly excluded from subsequent analyses when all_features=FALSE)

## How to apply

Load the MetaboSet object containing feature abundances (exprs), sample metadata (pData), and feature metadata (fData) with a QC column marking quality-control samples. Call flag_detection with qc_limit=0.7 to identify features observed in fewer than 70% of QC samples; this function computes detection rates per feature and updates the Flag column in fData with non-NA values for features below threshold. The rationale is that features consistently detected across replicate QC injections are more likely to be true signals than sporadic detections. Verify that flagged features are excluded from downstream multivariate analyses by setting all_features=FALSE; the Flag column acts as a persistent mask for the workflow.

## Related tools

- **notame** (Implements flag_detection function and coordinates QC-based feature flagging within the LC-MS preprocessing workflow) — https://github.com/hanhineva-lab/notame
- **Biobase** (Provides ExpressionSet class foundation for MetaboSet objects, enabling structured storage of feature flags in fData slots)
- **R** (Execution environment for flag_detection and MetaboSet manipulation)

## Examples

```
mset_flagged <- flag_detection(mset, qc_limit = 0.7); mset_filtered <- filter_by_flag(mset_flagged, all_features = FALSE)
```

## Evaluation signals

- Flag column in fData contains non-NA values (e.g., 'low_detection') for features with QC detection rate < qc_limit; unflagged features have NA.
- Number of flagged features matches manual count of features observed in < 70% of QC samples when qc_limit=0.7.
- Multivariate analysis outputs (PCA, OPLS-DA) exclude flagged features when all_features=FALSE, reducing dimensionality and noise compared to all_features=TRUE.
- Flagged features correspond to those with sporadic or absent peaks in QC abundance matrix (exprs) across QC sample columns.
- Reproducibility improves post-filtering: QC sample clustering tightness or inter-QC correlation increases after flagging applied.

## Limitations

- qc_limit threshold (0.7) is arbitrary; no universal consensus exists for optimal detection-rate cutoff across metabolite classes—tissue types, ionization modes, or compound chemistry may require empirical tuning.
- Flags permanently mark features in fData but do not remove them; downstream functions must respect all_features parameter to enforce exclusion—silent retention is possible if parameter is misset.
- Requires sufficient QC replicates to estimate reliable detection rates; sparse QC sampling (n < 3–5) produces unstable thresholds.
- Does not account for biology-driven variability (e.g., metabolites genuinely absent in some QC pools); detection rate alone cannot distinguish instrumental noise from true metabolite absence.

## Evidence

- [other] flag_detection is used to flag features based on detection: "flag_detection``` is used to flag features based on detection"
- [methods] Apply flag_detection with qc_limit parameter to identify features below acceptance threshold: "Apply flag_detection with qc_limit=0.7 to identify features not observed in at least 70% of QC samples"
- [methods] Flagging updates Flag column in feature metadata: "Update the Flag column in fData to record flagged features with non-NA values"
- [methods] Flagged features excluded from downstream analysis by default: "Verify that flagged features are excluded from subsequent multivariate analyses by default (all_features=FALSE)"
- [readme] MetaboSet is built on Biobase ExpressionSet: "MetaboSet``` is built upon the ```ExpressionSet``` class from the Biobase package"
- [other] Next, flag all the features with extensive amounts of missing values: "Next, flag all the features with extensive amounts of missing values"
