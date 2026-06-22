---
name: multi-sample-abundance-pattern-detection
description: Use when after initial retention-time-based feature grouping (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - MsFeatures
  - pheatmap
  - xcms
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/ac051437y
  title: XCMS
evidence_spans:
- General MS feature grouping functionality if defined by the `r Biocpkg("MsFeatures")` package
- library(pheatmap)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_xcms
    doi: 10.1021/ac051437y
    title: XCMS
  dedup_kept_from: coll_xcms
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/ac051437y
  all_source_dois:
  - 10.1021/ac051437y
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Multi-sample abundance pattern detection

## Summary

Refine feature groups by detecting correlated abundance patterns across samples using abundance-similarity parameters. This skill identifies which features within a retention-time-based group co-vary in intensity across replicates, splitting groups where abundance correlation falls below a threshold.

## When to use

After initial retention-time-based feature grouping (e.g., via SimilarRtimeParam with a 20-second window), when you have LC-MS data from multiple samples and need to distinguish co-eluting features of the same compound (which should have correlated abundances) from unrelated ions at similar m/z and retention time. Apply this skill when retention-time clustering alone groups chemically unrelated features together.

## When NOT to use

- Input is already a finalized feature table or compound annotation (abundance refinement will not improve chemical identity).
- Study has only one or two samples; correlation-based grouping requires multiple replicates to detect meaningful patterns.
- Features are known to be authentic adducts or isotopic variants that may have genuinely lower correlations due to ionization bias (e.g., [M+H]+ vs. [M+Na]+).

## Inputs

- retention-time-based feature groups (output from SimilarRtimeParam grouping)
- feature abundance matrix (features × samples) with missing values allowed
- LC-MS XcmsExperiment or feature table with sample replicates

## Outputs

- refined feature sub-groups with abundance-correlation-based assignments
- pairwise correlation matrix for each parent feature group
- sub-group count and feature-to-subgroup mapping table
- correlation heatmap visualization

## How to apply

Load retention-time-based feature groups and apply the groupFeatures() function with AbundanceSimilarityParam, specifying a correlation threshold (e.g., 0.7), a log2 abundance transformation to stabilize variance, and filled=TRUE to impute missing peaks before correlation calculation. The algorithm computes pairwise Pearson correlations of log2-transformed abundances across all samples for each feature pair within a retention-time group. Feature pairs with correlation below the threshold are split into separate sub-groups. Generate pairwise correlation heatmaps to visualize which features cluster together and verify that the refinement does not over-split genuine co-eluting adducts or isotopologues.

## Related tools

- **xcms** (Provides groupFeatures() method and AbundanceSimilarityParam class for abundance-correlation-based refinement of feature groups) — https://github.com/sneumann/xcms
- **MsFeatures** (Defines general MS feature grouping functionality and parameter classes for refinement strategies)
- **pheatmap** (Generates pairwise correlation heatmaps to visualize abundance patterns within feature groups)

## Examples

```
groupFeatures(feature_groups, AbundanceSimilarityParam(threshold=0.7, transform="log2", filled=TRUE))
```

## Evaluation signals

- Sub-group count from refinement is less than or equal to the input retention-time group count (no merging, only splitting).
- Pairwise correlation plot confirms that features within each sub-group have correlations ≥ threshold (default 0.7), and cross-sub-group correlations fall below the threshold.
- No sub-group contains a single feature (degenerate groups indicate over-splitting).
- Abundance patterns in log2-transformed space are visually coherent within sub-groups (heatmap rows cluster together).
- Parameter sensitivity check: vary threshold (e.g., 0.6, 0.7, 0.8) and verify that sub-group assignments are stable in the 0.65–0.75 range for robust grouping.

## Limitations

- Correlation-based grouping assumes linear abundance relationships; non-linear co-variation (e.g., post-translational modifications with unequal ionization) may be missed.
- Missing peak detection (filled=TRUE) relies on imputation; if imputation method is biased, spurious correlations can arise.
- Threshold choice (e.g., 0.7) is empirical and data-dependent; no universal value suits all compounds or instrument types.
- Does not directly recover chemical identity or distinguish adducts from isobars; abundance correlation is a necessary but not sufficient condition for compound assignment.
- Performance degrades with very high feature density (e.g., >5000 features) due to O(n²) pairwise correlation computation.

## Evidence

- [intro] AbundanceSimilarityParam: perform a feature grouping based on correlation of feature abundances (values) across samples.: "AbundanceSimilarityParam: perform a feature grouping based on correlation of feature abundances (values) across samples."
- [other] After applying AbundanceSimilarityParam(threshold=0.7, transform=log2, filled=TRUE), the 159 features were grouped into 94 feature groups. Within FG.040, pairwise correlation analysis reveals that not all features show correlation above the 0.7 threshold—for example, clear correlation is present between FT273 and FT274, and between FT143 and FT273, but other features within this retention time group show weaker correlations.: "After applying AbundanceSimilarityParam(threshold=0.7, transform=log2, filled=TRUE), the 159 features were grouped into 94 feature groups. Within FG.040, pairwise correlation analysis reveals that"
- [intro] Abundance of features of the same compound should have a similar pattern across samples.: "The abundance of features (ions) of the same compound should have a similar pattern across samples."
- [intro] Many of the larger retention time-based feature groups have been splitted into two or more sub-groups based on abundance correlation: "Many of the larger retention time-based feature groups have been splitted into two or more sub-groups based on"
- [other] Apply groupFeatures function with AbundanceSimilarityParam specifying threshold=0.7, transform=log2, and filled=TRUE to perform abundance-correlation-based refinement.: "Apply groupFeatures function with AbundanceSimilarityParam specifying threshold=0.7, transform=log2, and filled=TRUE to perform abundance-correlation-based refinement."
