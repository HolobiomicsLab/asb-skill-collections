---
name: feature-abundance-correlation-analysis
description: Use when after initial retention-time-based feature grouping (e.g., using SimilarRtimeParam with a 20-second window), apply this skill when you need to split large feature groups into more homogeneous sub-groups.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
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

# feature-abundance-correlation-analysis

## Summary

Refine retention-time-based LC-MS feature groups by partitioning them into sub-groups based on pairwise abundance correlation across samples using a user-defined threshold. This skill identifies which co-eluting features (same m/z and retention time window) actually co-vary in intensity, separating true co-ionizations from instrumental or chemical artifacts.

## When to use

After initial retention-time-based feature grouping (e.g., using SimilarRtimeParam with a 20-second window), apply this skill when you need to split large feature groups into more homogeneous sub-groups. Use it when abundance patterns diverge within a retention-time window—for example, when 159 features initially group into 94 retention-time groups, but some of those groups contain features with weak or absent correlation (e.g., features within FG.040 showing correlation strengths below a 0.7 threshold between certain feature pairs).

## When NOT to use

- Input is already a final compound-level feature table (e.g., post-annotation, merged by chemical identity); abundance correlation grouping is a pre-annotation refinement step.
- Sample sizes are < 3 (correlation statistics are unreliable with insufficient degrees of freedom).
- Abundance data has not been normalized or processed for missing values; gap-filling should precede this step.

## Inputs

- Retention-time-based feature groups (output from SimilarRtimeParam)
- Feature abundance matrix (intensity values across samples)
- Sample metadata or grouping information

## Outputs

- Sub-grouped feature assignments (refined feature groups indexed by FG.XXX notation)
- Count of total sub-groups produced
- Pairwise correlation matrix for each group
- Correlation heatmap visualization

## How to apply

Load retention-time-based feature groups output from SimilarRtimeParam. Apply the groupFeatures() function from MsFeatures with AbundanceSimilarityParam, setting threshold=0.7 (or other domain-justified cutoff), transform=log2 (to handle skewed abundance distributions), and filled=TRUE (to include gap-filled intensities for samples where peaks were not detected). For each retention-time group, compute pairwise Pearson or Spearman correlations of log2-transformed abundances across all samples. Features with pairwise correlation exceeding the threshold are retained in the same sub-group; those falling below it spawn separate sub-groups. Extract sub-group assignments and generate a heatmap (using pheatmap) showing pairwise correlations within each group to validate sub-grouping coherence and identify which feature pairs drive the partitioning.

## Related tools

- **xcms** (Provides preprocessing and retention-time grouping infrastructure; groupFeatures() dispatches to MsFeatures for abundance-based refinement.) — https://github.com/sneumann/xcms
- **MsFeatures** (Implements AbundanceSimilarityParam and groupFeatures() core logic for abundance correlation-based feature partitioning.)
- **pheatmap** (Visualizes pairwise correlation matrices within and across feature sub-groups to validate grouping coherence.)

## Examples

```
groupFeatures(fg_rtime, AbundanceSimilarityParam(threshold=0.7, transform="log2", filled=TRUE))
```

## Evaluation signals

- Verify output sub-group count is lower or equal to the input retention-time group count (no expansion, only refinement).
- Check that all pairwise correlations within a sub-group are ≥ the threshold (0.7); correlations between features in different sub-groups should be < threshold.
- Confirm gap-filled abundances (filled=TRUE) do not artificially inflate correlation; compare with filled=FALSE to assess sensitivity.
- Inspect the correlation heatmap visually: sub-groups should form distinct blocks with high within-block correlation and low between-block correlation.
- Validate that feature pairs explicitly mentioned in findings (e.g., FT273–FT274 and FT143–FT273 in FG.040) match the heatmap and sub-group assignments.

## Limitations

- Not all features within a retention-time group will show pairwise correlation above the threshold; some weaker correlations are expected and drive further sub-partitioning.
- Log2 transformation assumes abundance values are positive; zero or missing intensities require prior gap-filling or pseudocount addition.
- Correlation-based grouping is sensitive to outlier samples; quality control and potential outlier removal should precede this step.
- Threshold selection (e.g., 0.7) is user-dependent and should be justified by domain knowledge or exploratory analysis; no universal cutoff is recommended in the article.

## Evidence

- [other] After applying AbundanceSimilarityParam(threshold=0.7, transform=log2, filled=TRUE), the 159 features were grouped into 94 feature groups.: "After applying AbundanceSimilarityParam(threshold=0.7, transform=log2, filled=TRUE), the 159 features were grouped into 94 feature groups."
- [other] Within FG.040, pairwise correlation analysis reveals that not all features show correlation above the 0.7 threshold—for example, clear correlation is present between FT273 and FT274, and between FT143 and FT273, but other features within this retention time group show weaker correlations.: "Within FG.040, pairwise correlation analysis reveals that not all features show correlation above the 0.7 threshold—for example, clear correlation is present between FT273 and FT274, and between"
- [intro] AbundanceSimilarityParam: perform a feature grouping based on correlation of feature abundances (values) across samples.: "AbundanceSimilarityParam: perform a feature grouping based on correlation of feature abundances (values) across samples."
- [intro] The abundance of features (ions) of the same compound should have a similar pattern across samples.: "The abundance of features (ions) of the same compound should have a similar pattern across samples."
- [intro] Many of the larger retention time-based feature groups have been splitted into two or more sub-groups based on abundance correlation-based refinement.: "Many of the larger retention time-based feature groups have been splitted into two or more sub-groups based on abundance correlation-based refinement."
- [intro] for samples in which no chromatographic peak for a feature was detected, all signal from the m/z - retention time range defined based on the detected chromatographic peaks was integrated.: "for samples in which no chromatographic peak for a feature was detected, all signal from the m/z - retention time range defined based on the detected chromatographic peaks was integrated."
