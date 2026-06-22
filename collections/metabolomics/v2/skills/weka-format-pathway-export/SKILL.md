---
name: weka-format-pathway-export
description: Use when you have computed a pathway dysregulation score matrix (PDSmatrix) from metabolomics data and need to rank pathways by their relevance to a binary or multi-class phenotype label using information-gain scoring, then export the ranked set for use in machine learning classifiers (SVM, Random.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - Lilikoi v2.0
  - R
  - Weka
derived_from:
- doi: 10.1093/gigascience/giaa162
  title: Lilikoi V2.0
evidence_spans:
- The new Lilikoi v2.0 R package has implemented a deep-learning method for classification, in addition to popular machine learning methods.
- Lilikoi v2.0 is a modern, comprehensive package to enable metabolomics analysis in R programming environment.
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

# weka-format-pathway-export

## Summary

Export information-gain ranked pathways from a pathway dysregulation score (PDS) matrix into Weka-compatible format for downstream machine learning classification. This skill bridges personalized pathway analysis with standardized feature selection output suitable for phenotype prediction.

## When to use

You have computed a pathway dysregulation score matrix (PDSmatrix) from metabolomics data and need to rank pathways by their relevance to a binary or multi-class phenotype label using information-gain scoring, then export the ranked set for use in machine learning classifiers (SVM, Random Forest, LDA, etc.). Apply this when your input is metabolite-pathway associations and phenotype labels, and your goal is phenotype prediction via pathway features.

## When NOT to use

- PDSmatrix has not yet been computed from metabolite-pathway associations (use lilikoi.PDSfun first).
- Phenotype labels are continuous (e.g., survival time, biomarker concentration) rather than categorical; use regression-based feature selection instead.
- You are performing unsupervised pathway discovery with no phenotype annotation; information-gain requires labeled data.

## Inputs

- PDSmatrix (numeric matrix: pathways × samples with dysregulation scores)
- phenotype labels (factor or character vector: class labels per sample)
- information-gain threshold (numeric, typical range 0.30–0.70)

## Outputs

- selected_Pathways_Weka (data frame or text file: ranked pathway names with information-gain scores)
- information-gain scores per pathway (numeric vector)

## How to apply

Load the PDSmatrix (pathway-by-sample feature matrix) and corresponding phenotype labels into R. Apply the lilikoi.featuresSelection function with method='gain' (information-gain) and a threshold (typically 0.50) to rank pathways by their mutual information with the phenotype and filter to only those exceeding the threshold. The function returns selected_Pathways_Weka, a ranked list of pathway names and their information-gain scores in a format compatible with Weka machine learning workflows. The threshold acts as a specificity control: higher thresholds (e.g., 0.70) retain only the most discriminative pathways, while lower thresholds (e.g., 0.30) retain more candidate pathways at the risk of including noise. The information-gain metric quantifies how much knowing a pathway's activity reduces uncertainty about the phenotype class.

## Related tools

- **Lilikoi v2.0** (R package hosting lilikoi.featuresSelection function for information-gain pathway ranking and Weka export) — https://github.com/lanagarmire/lilikoi2
- **R** (Programming environment for executing lilikoi.featuresSelection and managing PDSmatrix objects)
- **Weka** (Target machine learning framework for which the selected_Pathways_Weka output is formatted)

## Examples

```
selected_Pathways_Weka <- lilikoi.featuresSelection(PDSmatrix, threshold=0.50, method="gain")
```

## Evaluation signals

- selected_Pathways_Weka contains only pathways with information-gain scores ≥ threshold; verify no scores fall below the specified cutoff.
- Pathway list is ranked in descending order by information-gain score; top pathways are more discriminative for the phenotype.
- Output file format is compatible with Weka (tab- or comma-delimited; pathway name and score columns are present and parseable).
- Number of selected pathways is substantially smaller than input PDSmatrix row count, indicating effective filtering (typical: 5–50 pathways selected from thousands).
- Information-gain scores are bounded in [0, log₂(number of classes)]; for binary phenotypes, max score ≤ 1.0.

## Limitations

- Information-gain assumes categorical phenotype; continuous outcomes require alternative feature selection methods (e.g., correlation, regression coefficient ranking).
- Threshold selection (0.50 in the reference workflow) is heuristic; no data-driven method for optimizing it is described; requires domain knowledge or cross-validation tuning.
- Pathways with rare or zero information-gain scores in small sample sets may be filtered out, potentially missing rare but clinically relevant signals.
- No correction for multiple comparisons applied; information-gain scoring does not account for multiple testing burden across pathways.

## Evidence

- [other] Apply information-gain method for feature selection: "Apply the information-gain method for feature selection with threshold 0.50 in Lilikoi v2.0 to rank and filter pathways by their relevance to the phenotype."
- [other] PDSmatrix is the pathway dysregulation score matrix: "Load the PDSmatrix (pathway-by-sample feature matrix) and phenotype labels into R."
- [other] Output is selected_Pathways_Weka: "producing selected_Pathways_Weka as output."
- [other] Information-gain scores rank pathway relevance: "to rank and filter pathways by their relevance to the phenotype."
- [readme] Lilikoi.featuresSelection implementation in readme: "selected_Pathways_Weka= lilikoi.featuresSelection(PDSmatrix,threshold= 0.50,method="gain")"
