---
name: retention-time-abundance-correlation-visualization
description: Use when after applying AbundanceSimilarityParam (with threshold ≥0.7 and log2 transform) to retention-time-based feature groups from SimilarRtimeParam, when you need to examine the internal correlation structure of specific feature sub-groups (e.g., FG.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - MsFeatures
  - pheatmap
  - xcms
derived_from:
- doi: 10.1021/acs.analchem.5c04338
  title: xcms
evidence_spans:
- General MS feature grouping functionality if defined by the `r Biocpkg("MsFeatures")` package
- library(pheatmap)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_xcms
    doi: 10.1021/acs.analchem.5c04338
    title: xcms
  dedup_kept_from: coll_xcms
schema_version: 0.2.0
---

# retention-time-abundance-correlation-visualization

## Summary

Visualize pairwise abundance correlations across samples within retention-time-based feature groups after abundance-similarity refinement, to assess which co-eluting features exhibit correlated ion abundance patterns and therefore likely derive from the same chemical compound. This skill bridges peak grouping and annotation by confirming that features grouped by retention time AND abundance correlation are genuinely co-variant.

## When to use

After applying AbundanceSimilarityParam (with threshold ≥0.7 and log2 transform) to retention-time-based feature groups from SimilarRtimeParam, when you need to examine the internal correlation structure of specific feature sub-groups (e.g., FG.040) to validate that the refined grouping accurately reflects sample-to-sample abundance co-variation. Use this skill especially when retention-time-based groups are large and may contain heterogeneous features that require sub-grouping confirmation.

## When NOT to use

- When input feature groups have been refined using EicSimilarityParam only (without abundance correlation refinement), as the grouping already incorporates EIC shape rather than abundance patterns.
- When the feature abundance matrix is too sparse or contains too many missing values even after gap-filling, rendering correlation estimates unreliable.
- When only a single sample or very few samples (< 3–4) are available, as correlation estimates require sufficient degrees of freedom.

## Inputs

- Retention-time-based feature groups (output from SimilarRtimeParam grouping)
- Refined feature sub-groups (output from groupFeatures with AbundanceSimilarityParam, threshold=0.7, transform=log2, filled=TRUE)
- Feature abundance matrix (features × samples, log2-transformed and gap-filled)

## Outputs

- Pairwise correlation matrix (features × features) for selected feature group
- Hierarchically-clustered correlation heatmap visualization
- Correlation statistics (e.g., Pearson r, p-values) for feature pairs within the group

## How to apply

Load the refined feature groups (output from groupFeatures with AbundanceSimilarityParam applied). Select a feature sub-group of interest (e.g., FG.040) and extract the abundance matrix (feature-by-sample intensities) for all features within that group, preferably after log2 transformation and any missing-value filling (filled=TRUE). Compute pairwise Pearson or Spearman correlation coefficients across all feature pairs using the sample-wise abundance vectors. Visualize the resulting correlation matrix as a heatmap (e.g., using pheatmap) with features as rows and columns, clustering them hierarchically to reveal which features co-vary strongly (correlation ≥0.7 threshold) and which show weaker correlations. The rationale is that true co-metabolites or multiply-charged/adducted ions from the same precursor should show high abundance correlation across all samples; features with weak correlations despite similar retention time may represent contaminants, false peaks, or unrelated compounds and warrant further investigation or removal.

## Related tools

- **xcms** (Provides groupFeatures() function and AbundanceSimilarityParam class to perform abundance-correlation-based feature refinement on retention-time groups; also handles log2 transformation and gap-filling.) — https://github.com/sneumann/xcms
- **MsFeatures** (Defines and implements the AbundanceSimilarityParam and grouping interface used to refine feature groups by abundance correlation.)
- **pheatmap** (Generates hierarchically-clustered heatmap visualizations of the pairwise feature correlation matrix to reveal sub-group structure and co-variance patterns.)

## Examples

```
# Load refined feature groups and extract FG.040 abundance matrix; compute pairwise correlations and visualize with pheatmap
fg_sub <- featureGroups[featureGroups$fg_id == "FG.040", ]
cor_matrix <- cor(t(fea_abundance[fg_sub$feature_id, ]), method="pearson")
pheatmap(cor_matrix, clustering_distance_cols="pearson", clustering_distance_rows="pearson", main="FG.040 Pairwise Abundance Correlation")
```

## Evaluation signals

- Correlation heatmap displays clear block structure: features within the refined sub-group (e.g., FG.040) should cluster into one or more cohesive blocks with high pairwise correlations (r ≥ 0.7), while uncorrelated features should appear isolated or in separate clusters.
- Majority of pairwise correlations within the refined sub-group exceed the 0.7 threshold used in AbundanceSimilarityParam; any feature pairs with r < 0.7 should be visually distinct from the main correlated cluster and may indicate sub-group misassignment.
- Hierarchical clustering dendrogram groups features that are known to co-metabolites or isotope/adduct pairs at short branch distances, and separates unrelated features at greater distances.
- Gap-filling status is reflected: features with higher proportions of filled (estimated) vs. observed abundances should be identifiable and may show slightly lower correlations; this is expected and should not invalidate the overall grouping if the trend is mild.
- Comparison with EIC similarity (from EicSimilarityParam) shows concordance: features with high abundance correlation should also display similar peak shapes and retention time clustering in EIC plots.

## Limitations

- Not all features within a retention-time-based feature group will show pairwise correlations above the 0.7 threshold, even after AbundanceSimilarityParam refinement, as noted in the faahKO example (FG.040 contains features with both strong and weak correlations). This indicates that retention time alone is insufficient to group all co-metabolites and that multiple refinement steps (abundance similarity + EIC similarity) may be needed.
- Correlation estimates depend heavily on the quality and completeness of the abundance matrix; extensive gap-filling (filled=TRUE) can artificially inflate correlations if the imputation method does not accurately reflect true co-variation.
- Log2 transformation may not be optimal for all datasets; zero or near-zero abundances in some samples can cause numerical issues or distort correlation estimates. The choice of transformation should be validated empirically.
- Hierarchical clustering in heatmap visualizations can be sensitive to distance metric (Euclidean, Pearson, etc.) and linkage method (complete, average, ward); different choices may produce visually different dendrograms even for the same correlation data.
- Correlation-based grouping is sample-dependent: features that appear correlated in the given cohort may not co-vary in other studies, ecosystems, or disease states, limiting generalizability of sub-group assignments.

## Evidence

- [other] After applying AbundanceSimilarityParam(threshold=0.7, transform=log2, filled=TRUE), the 159 features were grouped into 94 feature groups.: "After applying AbundanceSimilarityParam(threshold=0.7, transform=log2, filled=TRUE), the 159 features were grouped into 94 feature groups."
- [other] Within FG.040, pairwise correlation analysis reveals that not all features show correlation above the 0.7 threshold—for example, clear correlation is present between FT273 and FT274, and between FT143 and FT273, but other features within this retention time group show weaker correlations.: "Within FG.040, pairwise correlation analysis reveals that not all features show correlation above the 0.7 threshold—for example, clear correlation is present between FT273 and FT274, and between"
- [other] Generate a pairwise correlation plot showing abundance correlations across samples for all features in FG.040, visualizing which features cluster together under the abundance similarity criterion.: "Generate a pairwise correlation plot showing abundance correlations across samples for all features in FG.040, visualizing which features cluster together under the abundance similarity criterion."
- [intro] Features (ions) of the same compound should have similar retention time. The abundance of features (ions) of the same compound should have a similar pattern across samples.: "Features (ions) of the same compound should have similar retention time. The abundance of features (ions) of the same compound should have a similar pattern across samples."
- [intro] Grouping by similar retention time grouped the in total features into feature groups. Many of the larger retention time-based feature groups have been splitted into two or more sub-groups based on: "Grouping by similar retention time grouped the in total features into feature groups. Many of the larger retention time-based feature groups have been splitted into two or more sub-groups based on"
- [intro] AbundanceSimilarityParam: perform a feature grouping based on correlation of feature abundances (values) across samples.: "AbundanceSimilarityParam: perform a feature grouping based on correlation of feature abundances (values) across samples."
