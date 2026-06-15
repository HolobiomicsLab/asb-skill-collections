---
name: methylation-data-clustering
description: Use when after merging methylation call files across all samples into a unified methylBase object (via unite()), when you need to assess whether biological replicates cluster together, identify unexpected sample groupings, or visualize global methylation similarity relationships before proceeding.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3295
  - http://edamontology.org/topic_0654
  - http://edamontology.org/topic_3360
  tools:
  - R
  - knitr
  - methylKit
  - genomation
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

# methylation-data-clustering

## Summary

Hierarchical clustering and principal component analysis of methylation profiles across multiple samples to assess sample relationships and methylation-based similarity. This skill reveals grouping patterns and variance structure in DNA methylation data, enabling identification of sample subpopulations and quality assessment of methylation profiling.

## When to use

After merging methylation call files across all samples into a unified methylBase object (via unite()), when you need to assess whether biological replicates cluster together, identify unexpected sample groupings, or visualize global methylation similarity relationships before proceeding to differential methylation analysis.

## When NOT to use

- Input is a single sample or fewer than 2 samples — clustering requires multiple samples to show relationships.
- methylBase object has not been constructed via unite() with consistent coverage filtering — inconsistent base coverage across samples will distort distance metrics.
- Samples have extremely divergent methylation profiles (e.g., from different organisms or methylation assay types) — correlation-based distance may not be meaningful.

## Inputs

- methylBase object (unified methylation matrix from unite() with all samples merged at common coverage positions)
- Sample annotation table or experimental design metadata (optional, for color-coding clusters)

## Outputs

- Dendrogram object (hierarchical clustering tree with samples as leaves)
- Scree plot (variance explained by each principal component)
- PC1/PC2 scatter plot (sample positions in principal component space)
- Clustering and PCA visualizations suitable for publication or QC reporting

## How to apply

Load the methylBase object produced by unite() and apply clusterSamples() to perform hierarchical clustering on methylation profiles using correlation distance with Ward linkage, generating a dendrogram that visualizes sample relationships. Simultaneously apply PCASamples() to compute principal components and generate a scree plot showing variance explained by each PC. Extract and visualize the first two principal components (PC1 and PC2) as a scatter plot to assess sample grouping and methylation-based similarity. Interpret the dendrogram branch structure and PC1/PC2 loadings to confirm that biological/treatment replicates cluster together and that the methylation variance structure aligns with experimental design expectations.

## Related tools

- **methylKit** (Core R package providing clusterSamples() and PCASamples() functions for methylation clustering and PCA; also handles methylBase object creation and manipulation) — https://github.com/al2na/methylKit
- **R** (Programming environment for executing methylKit clustering and PCA functions and generating publication-quality visualizations)
- **knitr** (R package for embedding clustering and PCA code and outputs in reproducible documents (vignettes, reports))
- **genomation** (Optional downstream tool for annotating clusters with gene features after samples are grouped)

## Examples

```
clusterSamples(methylBase_object); PCASamples(methylBase_object)
```

## Evaluation signals

- Dendrogram visual inspection: biological replicates and samples from the same treatment group should cluster together with shorter branch heights; divergent samples should occupy separate clades.
- Scree plot monotonicity: variance explained by successive PCs should decrease smoothly; a sharp elbow typically identifies the informative number of dimensions (usually PC1 and PC2 should explain >50% of total variance).
- PC1/PC2 scatter plot separation: samples with similar methylation profiles should occupy nearby positions in PC space; batch effects or experimental artifacts would appear as unexpected sample segregation.
- Consistency with experimental design: cluster structure should align with known biological groups (e.g., test vs. control, treated vs. untreated); unexpected clusters suggest data quality issues or confounded factors.
- Reproducibility: rerunning clusterSamples() and PCASamples() on the same methylBase object should produce identical dendrograms and PC plots (deterministic functions).

## Limitations

- Clustering results depend on coverage filtering applied in unite() — bases with uneven coverage across samples will bias distance calculations; minimum coverage thresholds (default 10X per base) must be consistent.
- Ward linkage hierarchical clustering can be sensitive to outlier samples with extreme methylation profiles, potentially creating spurious long branches unrelated to biological signal.
- PCA assumes linear relationships between methylation levels; if methylation patterns are highly non-linear or driven by binary on/off switching in a subset of sites, PCA may not capture the dominant variance structure.
- Small sample sizes (n < 3–4 per group) may lead to unstable PC estimates and unreliable clustering; at least 2 replicates per condition are required for meaningful biological interpretation.
- The correlation distance metric used by clusterSamples() is sensitive to rank order and may obscure absolute methylation level differences; samples with identical methylation patterns but different baseline levels would cluster together despite biological differences.

## Evidence

- [other] clusterSamples() produces a dendrogram showing sample clustering by correlation distance with Ward linkage, and PCASamples() generates a scree plot and PC1/PC2 scatter plot revealing methylation profile relationships: "clusterSamples() produces a dendrogram showing sample clustering by correlation distance with Ward linkage, and PCASamples() generates a scree plot and PC1/PC2 scatter plot"
- [other] Load the methylBase object produced by unite() and apply clustering and PCA functions to assess sample grouping and methylation-based similarity: "Load the methylBase object produced by unite() from example CpG methylation files. 2. Apply clusterSamples() function to perform hierarchical clustering on methylation profiles"
- [readme] methylKit is an R package for DNA methylation analysis and annotation from high-throughput bisulfite sequencing: "methylKit is an R package for DNA methylation analysis and annotation from high-throughput bisulfite sequencing"
- [readme] By default methRead requires a minimum coverage of 10 reads per base to ensure good quality of the data and a high confidence methylation percentage: "By default methRead requires a minimum coverage of 10 reads per base to ensure good quality of the data"
- [intro] In order to do further analysis, we will need to get the bases covered in all samples. The following function will merge all samples to one object for base-pair locations that are covered in all: "In order to do further analysis, we will need to get the bases covered in all samples. The following function will merge all samples to one object"
