---
name: epigenetic-sample-stratification
description: Use when after merging methylation call files into a unified methylBase object (covering all samples at common base positions), apply this skill to assess whether biological replicates cluster together, whether case/control or treatment groups separate as expected, and to identify potential sample.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3295
  - http://edamontology.org/topic_3674
  - http://edamontology.org/topic_0625
  tools:
  - R
  - knitr
  - methylKit
  - Bismark
  - MethylDackel
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

# epigenetic-sample-stratification

## Summary

Stratify and visualize biological samples by their methylation profiles using unsupervised clustering and principal component analysis on base-pair resolution methylation data. This skill reveals sample relationships and groupings driven by DNA methylation similarity, enabling detection of batch effects, tissue/phenotype separation, and quality assessment of bisulfite sequencing experiments.

## When to use

After merging methylation call files into a unified methylBase object (covering all samples at common base positions), apply this skill to assess whether biological replicates cluster together, whether case/control or treatment groups separate as expected, and to identify potential sample contamination or mislabeling before proceeding to differential methylation analysis.

## When NOT to use

- Input methylation files have not been merged to a common set of covered positions (use unite() first)
- Sample number is very small (< 3 samples total); clustering and PCA require sufficient replication to reveal meaningful structure
- Methylation data come from highly heterogeneous tissues or cell types where within-group heterogeneity dominates; the skill may show dispersed rather than informative clustering

## Inputs

- methylBase object (unified methylation matrix across all samples)
- sample metadata or grouping information (phenotype/treatment assignments)

## Outputs

- dendrogram object from hierarchical clustering
- scree plot showing variance explained by principal components
- PC1 vs PC2 scatter plot with sample labels/colors

## How to apply

Load a methylBase object produced by unite() function from methRead output files. Apply clusterSamples() to perform hierarchical clustering on methylation profiles using correlation distance with Ward linkage, generating a dendrogram that reveals sample grouping. Then apply PCASamples() to compute principal components and generate a scree plot showing the proportion of variance explained by each PC. Extract and visualize PC1 and PC2 as a 2D scatter plot to assess sample separation in methylation space. Interpret the dendrogram branch distances and PC scatter plot positioning to evaluate whether biological replicates show high similarity and whether experimental groups separate as hypothesized. High within-group correlation and clear between-group separation indicate good data quality and expected biological structure.

## Related tools

- **methylKit** (R package providing clusterSamples() and PCASamples() functions to perform hierarchical clustering and PCA on methylBase objects; primary tool for this skill) — https://github.com/al2na/methylKit
- **R** (Statistical programming language used to run methylKit functions and manipulate clustering/PCA outputs)
- **Bismark** (Upstream tool that produces methylation call files (input to methRead); generates the raw methylation metrics aggregated by methylKit) — https://github.com/FelixKrueger/Bismark
- **MethylDackel** (Alternative upstream tool for extracting per-base methylation metrics from BAM alignments; can produce methylation call files compatible with methylKit methRead) — https://github.com/dpryan79/MethylDackel

## Examples

```
library(methylKit); clusterSamples(methylBase.obj, dist='correlation', method='ward', plot=TRUE); PCASamples(methylBase.obj, scree=TRUE, comp=c(1,2))
```

## Evaluation signals

- Biological replicates (e.g., test1 and test2) cluster together with short branch distances in the dendrogram, indicating high methylation similarity
- Different experimental groups (e.g., test samples vs. ctrl samples) separate into distinct clades or show clear separation in the PC1 vs PC2 scatter plot
- Scree plot shows that the first two principal components capture a substantial fraction of total variance (typically > 50% combined for n=4 samples), indicating that major methylation variation aligns with experimental structure
- No unexpected samples appear as outliers in the scatter plot; all samples map to expected regions based on their phenotype/treatment labels
- Correlation-based dendrogram distances are stable and reproducible across subsets of the data (e.g., re-clustering after removing one sample changes neighbor relationships minimally)

## Limitations

- Clustering and PCA assume that methylation variation is normally distributed and that correlation distance is appropriate; heavily skewed or bimodal methylation distributions may yield misleading results
- Results depend critically on coverage filtering: bases with low or inconsistent coverage are included by default (minimum 10X coverage in methRead), which can introduce noise; applying stricter thresholds via filterByCoverage() before clustering is recommended
- The skill is unsupervised and does not test statistical significance of sample separation; apparent clustering may reflect batch effects or confounding variables rather than biological differences
- Very large numbers of differentially methylated bases can dominate PCA; tissue-specific or cell-type-specific methylation patterns may obscure the effect of the primary experimental variable
- Sample size of < 3 samples per group limits interpretability of clustering; dendrogram topology and PC scatter plot become unstable with very small sample counts

## Evidence

- [intro] clusterSamples() produces a dendrogram showing sample clustering by correlation distance with Ward linkage, and PCASamples() generates a scree plot and PC1/PC2 scatter plot revealing methylation profile relationships among the four samples: "clusterSamples() produces a dendrogram showing sample clustering by correlation distance with Ward linkage, and PCASamples() generates a scree plot and PC1/PC2 scatter plot revealing methylation"
- [intro] We start by reading in the methylation call data from bisulfite sequencing with methRead function. Reading in the data this way will return a methylRawList object, and then uses unite() to merge samples to one object: "In order to do further analysis, we will need to get the bases covered in all samples. The following function will merge all samples to one object for base-pair locations that are covered in all"
- [intro] By default methRead requires a minimum coverage of 10 reads per base to ensure good quality of the data and a high confidence methylation percentage: "By default methRead requires a minimum coverage of 10 reads per base to ensure good quality of the data and a high confidence methylation percentage"
- [readme] methylKit is an R package for DNA methylation analysis and annotation from high-throughput bisulfite sequencing and is designed to deal with sequencing data from RRBS and its variants, but also target-capture methods: "*methylKit* is an [R](http://en.wikipedia.org/wiki/R_%28programming_language%29) package for DNA methylation analysis and annotation from high-throughput bisulfite sequencing. The package is designed"
- [readme] Sample correlation and clustering are current features of methylKit enabling researchers to assess sample relationships and grouping: "Sample correlation and clustering"
