---
name: feature-sub-group-refinement-and-validation
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
  - tandem-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# feature-sub-group-refinement-and-validation

## Summary

Refine retention-time-based feature groups using abundance correlation thresholds and validate sub-grouping patterns through pairwise correlation analysis. This skill applies post-hoc grouping refinement to LC-MS feature data, splitting larger groups into smaller, more homogeneous sub-groups based on abundance similarity across samples.

## When to use

After initial retention-time-based feature grouping (e.g., using SimilarRtimeParam with a 20-second window) has produced feature groups, but you suspect that features within a single retention-time group may represent distinct compounds or adducts with different abundance patterns across samples. Apply this skill when you need to validate whether all features in a group truly co-vary in intensity, especially when the group size is large (e.g., >5 features) or when visual inspection or prior knowledge suggests heterogeneous correlation structure.

## When NOT to use

- Input feature groups are already very small (≤2 features per group); abundance-based refinement will have minimal effect.
- Samples have highly variable or missing abundance data without effective gap-filling; correlation estimates become unreliable.
- The analysis goal requires grouping only by m/z and retention time, with no need to validate co-abundance patterns.

## Inputs

- Retention-time-based feature groups (output from SimilarRtimeParam grouping)
- Feature abundance matrix (log-transformed intensity values across samples)
- Gap-filled abundance values for missing features

## Outputs

- Sub-group assignments (integer vector mapping each feature to a refined sub-group ID)
- Count of refined sub-groups produced
- Pairwise correlation matrix for features within target groups
- Correlation heatmap visualization (pheatmap object or exported image)

## How to apply

Load the output of retention-time-based grouping (e.g., from SimilarRtimeParam) into the MsFeatures groupFeatures function. Apply AbundanceSimilarityParam with a correlation threshold (e.g., 0.7), specifying transform=log2 to stabilize variance across the abundance range, and filled=TRUE to include gap-filled intensities for samples where peaks were not detected. This step splits retention-time groups into sub-groups where all pairwise feature correlations exceed the threshold. Extract the resulting sub-group assignments, count the total number of sub-groups produced, and generate pairwise correlation heatmaps (using pheatmap or equivalent) to visualize clustering patterns and identify features that do not meet the correlation criterion. Compare the sub-group count and structure to the original retention-time grouping to assess the magnitude of refinement.

## Related tools

- **xcms** (Core package providing groupFeatures() and feature group data structures) — https://github.com/sneumann/xcms
- **MsFeatures** (Provides AbundanceSimilarityParam class and grouping algorithm implementation) — https://github.com/RforMassSpectrometry/MsFeatures
- **pheatmap** (Generates heatmap visualizations of pairwise feature correlations)

## Examples

```
groupFeatures(fg, AbundanceSimilarityParam(threshold=0.7, transform='log2', filled=TRUE))
```

## Evaluation signals

- Sub-group count is greater than or equal to the number of retention-time-based groups, confirming that refinement did not merge groups.
- Pairwise correlation matrix within each sub-group shows all off-diagonal correlations ≥ the specified threshold (e.g., ≥0.7), confirming internal homogeneity.
- Features that failed to meet the correlation threshold within the original group are assigned to different sub-groups, validating separation.
- Heatmap dendrogram or cluster structure visually matches the computed sub-group assignments, indicating consistent clustering.
- Gap-filled samples do not distort correlation estimates; comparison of correlations computed with and without gap-filled values shows minor differences in threshold classification.

## Limitations

- Correlation estimates are sensitive to the choice of transform (log2 vs. no transform vs. other) and the presence of zero or near-zero abundances; log2 transform with pseudocount adjustment is recommended but not always sufficient for sparse data.
- The threshold value (e.g., 0.7) is user-defined and must be calibrated per dataset; no universally optimal threshold exists across different instrument types, metabolite classes, or sample types.
- Gap-filling for missing chromatographic peaks can artificially inflate or suppress correlations if the filling algorithm is biased; validation against raw signal is advised.
- Sub-groups derived from abundance correlation may not correspond to chemical structures or true biological co-regulation; additional validation via MS/MS, isotope patterns, or reference standards is often needed to confirm sub-group identity.

## Evidence

- [other] After applying AbundanceSimilarityParam(threshold=0.7, transform=log2, filled=TRUE), the 159 features were grouped into 94 feature groups.: "After applying AbundanceSimilarityParam(threshold=0.7, transform=log2, filled=TRUE), the 159 features were grouped into 94 feature groups."
- [other] Apply groupFeatures function with AbundanceSimilarityParam specifying threshold=0.7, transform=log2, and filled=TRUE to perform abundance-correlation-based refinement.: "Apply groupFeatures function with AbundanceSimilarityParam specifying threshold=0.7, transform=log2, and filled=TRUE to perform abundance-correlation-based refinement."
- [other] Within FG.040, pairwise correlation analysis reveals that not all features show correlation above the 0.7 threshold—for example, clear correlation is present between FT273 and FT274, and between FT143 and FT273, but other features within this retention time group show weaker correlations.: "Within FG.040, pairwise correlation analysis reveals that not all features show correlation above the 0.7 threshold—for example, clear correlation is present between FT273 and FT274, and between"
- [intro] The abundance of features (ions) of the same compound should have a similar pattern across samples.: "The abundance of features (ions) of the same compound should have a similar pattern across samples."
- [intro] AbundanceSimilarityParam: perform a feature grouping based on correlation of feature abundances (values) across samples.: "AbundanceSimilarityParam: perform a feature grouping based on correlation of feature abundances (values) across samples."
- [intro] for samples in which no chromatographic peak for a feature was detected, all signal from the m/z - retention time range defined based on the detected chromatographic peaks was integrated.: "for samples in which no chromatographic peak for a feature was detected, all signal from the m/z - retention time range defined based on the detected chromatographic peaks was integrated."
