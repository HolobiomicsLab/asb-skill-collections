---
name: sample-similarity-assessment-from-methylation
description: Use when after merging methylation calls across all samples using unite() to create a methylBase object, apply this skill to characterize whether replicate samples cluster together and to visualize methylation-driven separation between biological groups (e.g., test vs. control).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2238
  edam_topics:
  - http://edamontology.org/topic_3295
  - http://edamontology.org/topic_3674
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

# Sample similarity assessment from methylation

## Summary

Assess methylation-based relationships among samples by computing hierarchical clustering and principal component analysis (PCA) on methylation profiles. This skill reveals sample grouping patterns and similarity structures that reflect methylation heterogeneity across treatment or control conditions.

## When to use

After merging methylation calls across all samples using unite() to create a methylBase object, apply this skill to characterize whether replicate samples cluster together and to visualize methylation-driven separation between biological groups (e.g., test vs. control). Use it as an exploratory quality-control step before differential methylation analysis.

## When NOT to use

- Sample methylation calls have not yet been merged across all samples (unite() has not been run); use methRead() and filtering steps first.
- Only single-sample or unpaired data is available; clustering and PCA require ≥2 samples for meaningful comparison.
- Samples have extremely low or unequal coverage after filtering; low-depth regions introduce noise into correlation and PC estimates.

## Inputs

- methylBase object (unified methylation calls across all samples, produced by unite())

## Outputs

- Dendrogram (hierarchical clustering tree with sample labels and correlation distances)
- Scree plot (variance explained by each principal component)
- PC1/PC2 scatter plot (2D sample projection with methylation-based similarity geometry)

## How to apply

Load the merged methylBase object from unite() into methylKit. Apply clusterSamples() to perform hierarchical clustering using correlation distance with Ward linkage, which groups samples by methylation profile similarity and produces a dendrogram. Simultaneously apply PCASamples() to compute principal components and generate a scree plot showing variance explained by each component. Extract and scatter-plot the first two principal components (PC1 and PC2) to assess sample grouping in reduced dimensionality space. Samples that cluster together or occupy the same region in PC space indicate methylation-level agreement; separation indicates distinct methylation profiles. Examine both outputs together: the dendrogram confirms hierarchical relationships, while the PCA scatter plot validates separation in the top variance axes.

## Related tools

- **methylKit** (R package providing clusterSamples() and PCASamples() functions for correlation-based hierarchical clustering and PCA on methylBase objects) — https://github.com/al2na/methylKit
- **R** (Statistical programming environment in which methylKit functions are executed)
- **knitr** (Markdown rendering for reproducible analysis and documentation of clustering and PCA outputs)

## Examples

```
clusterSamples(methylBase_object); PCASamples(methylBase_object)
```

## Evaluation signals

- Dendrogram branch heights and topology are consistent with known sample relationships (replicates cluster closer than biological groups, if expected)
- Scree plot shows monotonic decrease in variance explained; first two components typically capture >50% of total variance for well-separated sample groups
- PC1/PC2 scatter plot shows biological groups (e.g., test vs. control) in distinct regions and replicates within the same group cluster tightly
- Correlation distance values in dendrogram are in expected range (0–1 for Pearson correlation distance); all pairwise distances are symmetric
- No unexpected sample inversions or outliers; extreme outliers suggest quality issues or contamination requiring review of raw methylation calls

## Limitations

- Clustering and PCA are sensitive to batch effects and coverage bias; filterByCoverage() should be applied before unite() to remove PCR-biased bases with extreme coverage (default: < 10X or > 99.9th percentile).
- PCA assumes linear relationships between methylation values; non-linear structures (e.g., clusters separated by multiple methylation contexts) may not be fully captured in the first two components.
- Dendrogram and PCA reflect methylation patterns at all covered bases; regional or context-specific (CpG vs. CHG vs. CHH) relationships are obscured unless subset before analysis.
- Sample relationships are unstable with very few (< 100) high-quality covered bases across all samples; coverage threshold and base filtering become critical.
- Ward linkage in hierarchical clustering can be sensitive to initial sample order and outlier samples; always examine the dendrogram visually for consistency with biological expectations.

## Evidence

- [other] clusterSamples() produces a dendrogram showing sample clustering by correlation distance with Ward linkage: "clusterSamples() produces a dendrogram showing sample clustering by correlation distance with Ward linkage"
- [other] PCASamples() generates a scree plot and PC1/PC2 scatter plot: "PCASamples() generates a scree plot and PC1/PC2 scatter plot revealing methylation profile relationships among the four samples"
- [other] Load methylBase object and apply clustering/PCA functions: "Load the methylBase object produced by unite() from example CpG methylation files. Apply clusterSamples() function to perform hierarchical clustering on methylation profiles and generate a dendrogram"
- [intro] Filter samples based on coverage to remove PCR bias: "The code below filters a methylRawList and discards bases that have coverage below 10X and also discards the bases that have more than 99.9th percentile of coverage in each sample"
- [readme] methylKit is an R package for DNA methylation analysis: "methylKit is an R package for DNA methylation analysis and annotation from high-throughput bisulfite sequencing"
- [readme] Sample correlation and clustering is a current feature: "Sample correlation and clustering"
