---
name: principal-component-analysis-visualization
description: Use when after merging methylation call files from multiple samples using unite() to create a methylBase object, apply PCA when you need to visualize sample-level relationships based on overall methylation similarity across all covered bases, or when you want to determine which principal components.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3935
  edam_topics:
  - http://edamontology.org/topic_3674
  - http://edamontology.org/topic_3168
  tools:
  - R
  - knitr
  - methylKit
derived_from:
- doi: 10.1186/gb-2012-13-10-r87
  title: methylkit
evidence_spans:
- packageVersion('methylKit')
- '%\VignetteEngine{knitr::rmarkdown}'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/epigenomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_methylkit
    doi: 10.1186/gb-2012-13-10-r87
    title: methylkit
  dedup_kept_from: coll_methylkit
schema_version: 0.2.0
---

# principal-component-analysis-visualization

## Summary

Apply PCA to methylation profiles from a unified methylBase object to reveal sample relationships and variance structure in principal component space. Generates a scree plot showing variance explained by each PC and a biplot of the first two principal components to assess methylation-based sample grouping.

## When to use

After merging methylation call files from multiple samples using unite() to create a methylBase object, apply PCA when you need to visualize sample-level relationships based on overall methylation similarity across all covered bases, or when you want to determine which principal components explain the most variance in methylation profiles among your samples.

## When NOT to use

- Input is a raw methylRawList (unmunged per-sample files) — must first run unite() to create methylBase.
- You need to perform clustering by correlation distance with Ward linkage — use clusterSamples() instead, which produces a dendrogram.
- Sample count is very small (n < 3) — PCA is unstable with fewer samples than dimensions.

## Inputs

- methylBase object (unified methylation data from unite() across all samples and bases)
- sample metadata (optional, for labeling and coloring scatter plot points)

## Outputs

- scree plot (variance explained by each principal component)
- PC1 vs PC2 scatter plot (sample coordinates in first two principal components)
- principal component scores matrix (numeric coordinates for all samples and PCs)

## How to apply

Load the methylBase object produced by unite() from merged methylation calls. Apply the PCASamples() function from methylKit to compute principal components of the methylation profile matrix. Extract the scree plot showing variance explained by each PC to determine the number of informative components. Then visualize the first two principal components (PC1 and PC2) as a scatter plot with samples as points, colored or labeled by experimental group (e.g., test1, test2, ctrl1, ctrl2). The function performs centering and scaling on the methylation data before eigenvalue decomposition. Interpret clustering patterns in PC space: samples that cluster together have similar methylation profiles, while separation along PC1 and PC2 indicates major sources of methylation variation between experimental groups.

## Related tools

- **methylKit** (R package providing PCASamples() function to compute PCA on methylation profiles and generate scree and scatter plots) — https://github.com/al2na/methylKit
- **R** (Statistical computing environment in which PCASamples() and plotting functions are executed)

## Examples

```
PCASamples(methylBase_obj)
```

## Evaluation signals

- Scree plot shows monotonically decreasing variance explained with cumulative sum approaching 100% across PCs
- PC1 and PC2 scatter plot displays sample points with no overlapping labels and clear visual separation if groups differ in methylation
- Principal component scores matrix has dimensions (n_samples × n_components) with numeric values suitable for downstream analysis
- Samples cluster according to known experimental condition (e.g., test and control groups separate) indicating the PCA captured true biological structure
- Total variance explained by first two PCs is ≥ 50% (heuristic for effective dimensionality reduction)

## Limitations

- PCA assumes linear relationships between methylation and the principal components; complex or non-linear patterns may not be well-captured.
- Results depend on the choice of bases included in methylBase (coverage threshold, q-value filtering applied before PCA may alter conclusions).
- With very small sample sizes (n < 5), the variance estimates are unstable and the scatter plot may be misleading.
- PCA is sensitive to outlier samples (e.g., one sample with extremely different methylation); outliers can dominate PC1, obscuring subtler structure.

## Evidence

- [intro] PCASamples() generates a scree plot showing variance explained by each PC and PC1/PC2 scatter plot revealing methylation profile relationships: "PCASamples() function to compute principal components and generate a scree plot showing variance explained by each PC. 4. Extract and visualize the first two principal components (PC1 and PC2) as a"
- [intro] methylBase object is the input container created by uniting multiple samples: "In order to do further analysis, we will need to get the bases covered in all samples. The following function will merge all samples to one object for base-pair locations that are covered in all"
- [other] PCA visualization assesses sample relationships in principal component space: "How do the four samples (test1, test2, ctrl1, ctrl2) cluster based on methylation similarity, and what are their relationships in principal component space?"
- [readme] methylKit supports multiple visualization options including PCA: "Multiple visualization options"
- [readme] Sample correlation and clustering is a core feature of methylKit: "Sample correlation and clustering"
