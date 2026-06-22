---
name: pairwise-similarity-matrix-construction
description: Use when after XCMS feature detection and retention time correction, when you have a feature abundance table aligned across samples and need to group features that likely arise from the same compound before downstream annotation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_1812
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - XCMS
  - dynamicTreeCut
  - RAMClustR
derived_from:
- doi: 10.1021/ac501530d
  title: RAMClust
evidence_spans:
- ramclustR function is built to use xcms data
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ramclust_cq
    doi: 10.1021/ac501530d
    title: RAMClust
  dedup_kept_from: coll_ramclust_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/ac501530d
  all_source_dois:
  - 10.1021/ac501530d
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# pairwise-similarity-matrix-construction

## Summary

Construct a symmetric pairwise similarity matrix by multiplying retention time similarity and correlational similarity scores for all feature pairs in metabolomics data. This matrix serves as input to hierarchical clustering to group features derived from the same compound.

## When to use

After XCMS feature detection and retention time correction, when you have a feature abundance table aligned across samples and need to group features that likely arise from the same compound before downstream annotation. Apply this skill when your data contains multiple features per compound due to isotopic peaks and adduction phenomena, and you need an unsupervised, platform-agnostic grouping approach.

## When NOT to use

- Input data has not undergone XCMS retention time correction and regrouping (retcor and group steps required)
- Missing values remain in the feature abundance table (fillPeaks must be run first)
- Features are from targeted or supervised analysis where feature grouping is already predefined by curated rules

## Inputs

- XCMS feature table with retention time-corrected and regrouped features
- Feature abundance matrix (samples × features) with no missing values (post-fillPeaks)
- Retention time values for all detected features

## Outputs

- Symmetric pairwise similarity matrix (features × features)
- Feature cluster assignments from hierarchical clustering

## How to apply

Extract retention time values and Pearson correlation coefficients for all feature pairs from your XCMS-processed feature table. Normalize retention time differences into a similarity score on a 0–1 scale (e.g., using inverse distance or Gaussian kernel). Compute pairwise Pearson correlation coefficients between quantitative feature profiles across all samples. Multiply the retention time similarity score and correlational similarity score element-wise for each feature pair; a product of 1×1=1 indicates features likely derive from the same compound, while 0×1 or 1×0 indicates different compounds. Output the resulting symmetric similarity matrix in a format suitable for hierarchical clustering (e.g., distance or similarity matrix) and pass it to dynamicTreeCut for dendrogram cutting.

## Related tools

- **XCMS** (Detects all signals from metabolomics dataset and generates aligned features; provides retention time and feature abundance data as input to similarity calculation)
- **dynamicTreeCut** (Performs hierarchical clustering on the similarity matrix and cuts the resulting dendrogram into feature clusters)
- **RAMClustR** (Wrapper function that orchestrates similarity matrix construction, hierarchical clustering, and feature annotation for metabolomics data) — https://github.com/cbroeckl/RAMClustR
- **R** (Statistical computing environment for correlation computation and matrix operations)

## Examples

```
RC <- ramclustR(xcmsObj = xset, ExpDes = experiment); # constructs similarity matrix internally and performs clustering
```

## Evaluation signals

- Similarity matrix is symmetric (matrix[i,j] == matrix[j,i]) and diagonal values equal 1 (self-similarity)
- All similarity values fall within [0, 1] range (product of two 0–1 scores)
- Features with similar retention times and correlated abundance profiles across samples produce high similarity scores (close to 1)
- Features with dissimilar retention times or uncorrelated profiles produce low similarity scores (close to 0)
- Hierarchical clustering of the matrix produces clusters where member features share approximately the same retention time within expected chromatographic window

## Limitations

- Approach assumes features from the same compound have approximately equal retention times; compounds with severe co-elution or overlapping peaks may not be properly resolved
- Pearson correlation can mask non-linear relationships between feature abundances
- Similarity matrix construction requires complete feature abundance data; sparse or highly missing data will produce unreliable correlations
- Method is unsupervised and platform-agnostic but depends critically on quality of prior XCMS retention time correction; drift in RT can cause false grouping or splitting

## Evidence

- [other] RAMClustR calculates a pairwise total similarity score as the product of retention time similarity and correlational similarity scores.: "RAMClustR calculates a pairwise total similarity score as the product of retention time similarity and correlational similarity scores"
- [other] A score of 1×1=1 indicates features likely derive from one compound, while scores like 1×0=0 or 0×1=0 indicate features represent different compounds.: "A score of 1×1=1 indicates features likely derive from one compound, while scores like 1×0=0 or 0×1=0 indicate features represent different compounds"
- [intro] Since both conditions must be met, the product of the two similarity scores provides the best approximation of the total similarity score: "Since both conditions must be met, the product of the two similarity scores provides the best approximatio of the total similarity score"
- [intro] two features derived from the same compound will have (approximately) the same retention time and quantitative trend across samples: "two features derived from the same compound with have (approximately) the same retention time. The second is that two features derived from the same compound will have (approximately) the same"
- [intro] submitting this score matrix for hierarchical clustering, and then cutting the resulting dendrogram into neat chunks using the dynamicTreeCut package: "submitting this score matrix for heirarchical clustering, and then cutting the resulting dendrogram into neat chunks using the dynamicTreeCut package"
- [other] Compute Pearson correlation coefficients between quantitative feature profiles across all samples to obtain correlational similarity scores.: "Compute Pearson correlation coefficients between quantitative feature profiles across all samples to obtain correlational similarity scores"
- [other] Normalize retention time differences into a similarity score (e.g., inverse distance or Gaussian kernel) on a scale of 0–1.: "Normalize retention time differences into a similarity score (e.g., inverse distance or Gaussian kernel) on a scale of 0–1"
- [intro] xset <- fillPeaks(xset)  # 'fillPeaks' to remove missing values in final dataset: "xset <- fillPeaks(xset)  # 'fillPeaks' to remove missing values in final dataset"
