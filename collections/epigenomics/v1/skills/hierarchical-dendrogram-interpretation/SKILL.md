---
name: hierarchical-dendrogram-interpretation
description: Use when you have a methylBase object containing aligned methylation calls across multiple samples and need to verify whether samples cluster by expected experimental condition (e.g., test vs. control) or identify unexpected sample relationships.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3295
  - http://edamontology.org/topic_0654
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

# hierarchical-dendrogram-interpretation

## Summary

Interpret hierarchical clustering dendrograms from methylation profiles to assess sample relatedness and grouping patterns. This skill applies distance-based clustering to reveal whether samples cluster by expected biological groups (e.g., treatment vs. control) and infers methylation-based similarity relationships.

## When to use

You have a methylBase object containing aligned methylation calls across multiple samples and need to verify whether samples cluster by expected experimental condition (e.g., test vs. control) or identify unexpected sample relationships. Use this skill when sample relationships and data quality must be confirmed before downstream differential methylation analysis.

## When NOT to use

- Input is a single sample or fewer than two samples—dendrograms require at least two samples to show relationships.
- Samples have been pre-filtered to remove low-coverage bases and you need quantitative differential methylation statistics rather than exploratory sample clustering.
- You have already identified batch effects and corrected them; re-clustering may not reflect the corrected structure without re-running clusterSamples().

## Inputs

- methylBase object (output of unite() function containing merged methylation calls for all samples at positions covered in all samples)

## Outputs

- Dendrogram object showing hierarchical relationships among samples
- Visual dendrogram plot with branch structure and sample labels

## How to apply

Load a methylBase object from unite() containing base-pair coverage and methylation percentages across samples. Apply clusterSamples() to perform hierarchical clustering using correlation distance with Ward linkage, which produces a dendrogram showing pairwise sample relationships. Interpret the dendrogram by examining branch heights (reflecting correlation distance) and cluster membership—samples that cluster together have similar methylation profiles. Validate the dendrogram structure against expected biological groupings (e.g., test1 and test2 grouping separately from ctrl1 and ctrl2). Inspect outliers or unexpected groupings as indicators of batch effects, sample swaps, or biological heterogeneity that may require sample-level filtering via filterByCoverage() before proceeding to differential methylation testing.

## Related tools

- **methylKit** (Provides clusterSamples() function to perform hierarchical clustering on methylBase objects and generate dendrograms using correlation distance and Ward linkage) — https://github.com/al2na/methylKit
- **R** (Execution environment for methylKit functions and dendrogram visualization)

## Examples

```
clusterSamples(methylBase_object)
```

## Evaluation signals

- Dendrogram branch structure matches expected biological groupings (e.g., test samples cluster together, control samples cluster together, or known biological replicates are proximal in the tree).
- Branch heights (correlation distances) are consistent with sample similarity expectations—greater distances between treatment and control groups suggest robust methylation differences.
- No unexpected outliers or sample swaps are visible; all samples from the same experimental condition are more similar to each other than to samples from different conditions.
- Comparison with PCASamples() scatter plot (PC1 vs PC2) shows consistent clustering patterns—samples that cluster in the dendrogram should occupy similar regions in PC space.

## Limitations

- Dendrogram clustering depends on correlation distance computed from methylation percentages; samples with low coverage or high noise may produce misleading cluster patterns. Pre-filter using filterByCoverage() (default 10X minimum, removing >99.9th percentile) before clustering.
- Ward linkage emphasizes variance within clusters and may suppress detection of small, biologically important sample subgroups if their methylation profiles are globally similar.
- Dendrograms reflect only pairwise correlation structure; they do not quantify statistical significance of differences or distinguish samples with gradual methylation drift from those in discrete biological states.
- CpG methylation context only: methylKit's default clustering analyzes CpG dinucleotides; non-CpG methylation in embryonic stem cells and other tissues requires separate preprocessing and may not be captured in standard CpG-focused methylBase objects.

## Evidence

- [intro] clusterSamples() produces a dendrogram showing sample clustering by correlation distance with Ward linkage: "clusterSamples() produces a dendrogram showing sample clustering by correlation distance with Ward linkage"
- [intro] By default methRead requires a minimum coverage of 10 reads per base to ensure good quality of the data: "By default methRead requires a minimum coverage of 10 reads per base to ensure good quality of the data and a high confidence methylation percentage"
- [intro] Merge samples across all bases using unite() function to create methylBase objects for comparative analysis: "In order to do further analysis, we will need to get the bases covered in all samples. The following function will merge all samples to one object for base-pair locations that are covered in all"
- [readme] Sample correlation and clustering is a current feature for assessing sample relationships: "Sample correlation and clustering"
