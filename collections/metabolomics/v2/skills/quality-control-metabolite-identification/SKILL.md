---
name: quality-control-metabolite-identification
description: Use when you have loaded a metabolomics dataset with a metabolitedata dataframe containing annotation columns (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - NormalizeMets
  - RStudio
derived_from:
- doi: 10.1007/s11306-018-1347-7
  title: NormalizeMets
evidence_spans:
- The R software environment can be downloaded for free from the Comprehensive R Archive Network (CRAN)
- 'Install the NormalizeMets package by using the following function: `install.packages("NormalizeMets")`'
- The use of RStudio is also recommended. RStudio is an integrated development environment (IDE)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_normalizemets_cq
    doi: 10.1007/s11306-018-1347-7
    title: NormalizeMets
  dedup_kept_from: coll_normalizemets_cq
schema_version: 0.2.0
---

# quality-control-metabolite-identification

## Summary

Identify and extract quality control metabolites (internal standards, negative controls, or external standards) from metabolomics datasets by querying metabolite-specific annotation columns. This step enables subsequent normalization and quality assessment by flagging metabolites whose behavior is known a priori and should be used to correct for unwanted variation.

## When to use

You have loaded a metabolomics dataset with a metabolitedata dataframe containing annotation columns (e.g., 'IS' for internal standards, 'neg_control' for negative controls, or equivalent QC designations) and need to extract the indices or names of these QC metabolites before applying normalization methods such as NormQcmets. This is required when the normalization method depends on known reference metabolites (e.g., 'is', 'nomis', 'ccmn', 'ruvrandclust') that must be passed explicitly via the qcmets parameter.

## When NOT to use

- The metabolitedata does not contain explicit QC annotation columns or the dataset lacks metadata about which metabolites are standards or controls.
- You intend to use a normalization method that does not require QC metabolites (e.g., scaling methods like 'median', 'mean', 'sum') and do not need to assess QC performance.
- Your dataset has already been pre-filtered to remove or separate QC metabolites from the feature matrix; re-identifying them may introduce duplicates or inconsistencies.

## Inputs

- metabolitedata: dataframe with QC annotation columns (IS, neg_control, or equivalent) and metabolite names as row names
- metabolomics dataset object (mixdata, Didata, UVdata, or alldata_eg) containing metabolitedata component

## Outputs

- qcmets: numeric or character vector of indices or names of quality control metabolites
- qcmets_subset: subset of metabolitedata filtered to QC metabolites only (optional, for validation)

## How to apply

Load the metabolitedata dataframe from your bundled dataset (mixdata, Didata, UVdata, or alldata_eg). Query the appropriate annotation column using logical indexing (e.g., which(metabolitedata$IS==1) for internal standards or which(metabolitedata$neg_control==1) for negative controls) to retrieve the row indices or names of QC metabolites. Verify that the returned indices are not empty and correspond to metabolites present in the featuredata matrix. Pass these indices to the qcmets parameter of NormQcmets or store them for downstream QC visualization. The rationale is that QC metabolites serve as known anchors for estimating and removing unwanted variation; their identification must precede normalization to ensure the correct reference set is used.

## Related tools

- **NormalizeMets** (R package providing metabolitedata structure, QC annotation columns, and NormQcmets function that consumes qcmets indices; identified QC metabolites are passed via qcmets parameter to drive normalization.) — https://github.com/metabolomicstats/NormalizeMets
- **R** (statistical environment for executing logical indexing queries (which()) and dataframe operations to identify QC metabolites from metabolitedata.)
- **RStudio** (integrated development environment (IDE) for interactively querying metabolitedata and validating QC metabolite identification.)

## Examples

```
qcmets <- which(UVdata$metabolitedata$neg_control==1); normalized <- NormQcmets(featuredata=UVdata$featuredata, method='ruvrandclust', k=1, qcmets=qcmets)
```

## Evaluation signals

- Returned qcmets indices are non-empty and all values fall within the range [1, ncol(featuredata)].
- Each identified QC metabolite name appears in both metabolitedata row names and featuredata column names with no mismatches.
- Logical query (e.g., which(metabolitedata$IS==1)) returns consistent indices across repeated runs on the same dataset.
- When qcmets indices are passed to NormQcmets, the function executes without errors related to out-of-bounds or missing metabolite references.
- Visual inspection or summary of the qcmets_subset shows that selected metabolites have expected IS, neg_control, or other QC annotations set to 1 (or TRUE).

## Limitations

- QC annotation columns must exist and be populated correctly in metabolitedata; missing or misspelled column names will return empty results without warning.
- If multiple QC annotations exist (e.g., both 'IS' and 'neg_control'), the user must decide which to use or combine; the skill does not automate prioritization.
- Quality of downstream normalization depends on the accuracy and completeness of QC annotations; mislabeled or irrelevant metabolites in the QC set will bias normalization results.
- The skill assumes metabolite row names in metabolitedata match column names in featuredata; name mismatches will cause failures during NormQcmets execution.

## Evidence

- [other] Identify negative control metabolites from metabolitedata using the neg_control column (which(UVdata$metabolitedata$neg_control==1)).: "Identify negative control metabolites from metabolitedata using the neg_control column (which(UVdata$metabolitedata$neg_control==1))."
- [other] Identify quality control metabolites (internal standards) from the metabolitedata using the IS column.: "Identify quality control metabolites (internal standards) from the metabolitedata using the IS column."
- [readme] metabolitedata contains metabolite-specific information in a separate dataframe. These information can include, but is not limited to, designation of metabolites as internal/external standards, or positive/negative controls.: "metabolitedata contains metabolite-specific information in a separate dataframe. These information can include, but is not limited to, designation of metabolites as internal/external standards, or"
- [other] pass the indices of QC metabolites via qcmets parameter, and provide additional parameters as required: "pass the indices of QC metabolites via qcmets parameter, and provide additional parameters as required"
