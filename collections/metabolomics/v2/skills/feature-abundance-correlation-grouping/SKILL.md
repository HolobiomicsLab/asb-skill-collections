---
name: feature-abundance-correlation-grouping
description: Use when after performing retention-time-based feature grouping (e.g., 10–20 second windows), when you observe large feature groups that may conflate multiple independent compounds with coincidentally similar retention times.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - MsFeatures
  - xcms
derived_from:
- doi: 10.1021/ac051437y
  title: XCMS
evidence_spans:
- General MS feature grouping functionality if defined by the `r Biocpkg("MsFeatures")` package with additional functionality being implemented
- VignetteDepends{xcms,BiocStyle,faahKO,pheatmap,MsFeatures}
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_xcms_cq
    doi: 10.1021/ac051437y
    title: XCMS
  dedup_kept_from: coll_xcms_cq
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

# feature-abundance-correlation-grouping

## Summary

Refine retention-time-based feature groups by applying correlation-based abundance similarity thresholds to split groups with dissimilar abundance patterns across samples. This post-hoc grouping step reduces false positive co-grouping of features with similar retention times but uncorrelated ion intensities.

## When to use

After performing retention-time-based feature grouping (e.g., 10–20 second windows), when you observe large feature groups that may conflate multiple independent compounds with coincidentally similar retention times. Apply this step if you have filled chromatographic peak data across samples and want to decompose retention-time groups into more chemically coherent sub-groups based on quantitative abundance co-variation.

## When NOT to use

- Input features have not been grouped by retention time first — apply SimilarRtimeParam grouping before abundance correlation refinement.
- Filled chromatographic peak data is unavailable or sparse (many zero/missing values) — abundance correlation is unreliable without complete quantitative matrices.
- You are working with a single-sample dataset or samples with no shared features — correlation requires multi-sample abundance variation.

## Inputs

- XcmsExperiment object with pre-existing retention-time-based feature groups
- Filled chromatographic peak intensity matrix (samples × features, all non-zero)

## Outputs

- XcmsExperiment object with refined (post-split) feature groups
- Integer: total count of feature groups after abundance correlation refinement
- Feature group membership assignments (feature → group ID mapping)

## How to apply

Load a pre-grouped XcmsExperiment object (from SimilarRtimeParam grouping). Apply groupFeatures() with AbundanceSimilarityParam, specifying: threshold (typically 0.7 for Pearson correlation), transform function (log2 recommended for abundance data to handle skew), and filled=TRUE to ensure all features have abundance values across all samples. The function will compute pairwise correlations of log2-transformed feature abundances, then split original retention-time groups into sub-groups when correlations fall below the threshold. Extract the resulting feature group count and membership assignments to assess splitting effectiveness.

## Related tools

- **xcms** (Provides groupFeatures() function, AbundanceSimilarityParam class, and XcmsExperiment data container for retention-time and abundance-correlation grouping workflows.) — https://github.com/sneumann/xcms
- **MsFeatures** (Defines general MS feature grouping interface and complementary grouping parameter classes used by xcms.)

## Examples

```
groupFeatures(xmse, param = AbundanceSimilarityParam(threshold = 0.7, transform = log2), filled = TRUE)
```

## Evaluation signals

- Feature group count increases substantially compared to retention-time-only grouping, indicating large retention-time groups were split.
- Intra-group Pearson correlation of log2-transformed abundances is ≥ threshold (0.7); inter-group correlation is < threshold.
- Verify that features within each post-refinement group have similar retention time (within original 10–20 s window) AND similar abundance patterns across samples.
- Spot-check a sample of split groups: confirm that sub-groups represent chemically distinct features (e.g., different m/z values or significantly different ion abundance ranks across samples).

## Limitations

- Abundance correlation thresholds are data-dependent; a fixed threshold (e.g., 0.7) may over-split or under-split in datasets with high inter-sample variability or few replicates.
- Log2 transformation assumes positive abundances; zero or missing values in unfilled data will cause correlation to fail or be undefined.
- Correlation-based grouping assumes that co-eluting features from the same compound have abundant collinear abundances; isomers or in-source fragments may correlate poorly despite sharing a precursor.
- The article does not specify how ties (correlations exactly equal to threshold) are handled or performance on very large feature groups (>100 features per retention-time bin).

## Evidence

- [other] After applying AbundanceSimilarityParam(threshold = 0.7, transform = log2, filled = TRUE) to the rt-20s grouped xmse object, many of the larger retention time-based feature groups were split into two or more sub-groups based on correlation of feature abundances.: "After applying AbundanceSimilarityParam(threshold = 0.7, transform = log2, filled = TRUE) to the rt-20s grouped xmse object, many of the larger retention time-based feature groups were split into two"
- [intro] Features (ions) of the same compound should have similar retention time and abundance patterns across samples and peak shapes of extracted ion chromatograms.: "Features (ions) of the same compound should have similar retention time. The abundance of features"
- [intro] groupFeatures(xmse, AbundanceSimilarityParam(threshold = 0.7, transform = log2), filled = TRUE) refines feature groups based on correlation of feature abundances across samples.: "groupFeatures(xmse, AbundanceSimilarityParam(threshold = 0.7, transform = log2), filled = TRUE)"
- [intro] For samples in which no chromatographic peak for a feature was detected, all signal from the m/z - retention time range defined based on the detected chromatographic peaks was integrated.: "for samples in which no chromatographic peak for a feature was detected, all signal from the m/z - retention time range defined based on the detected chromatographic peaks was integrated"
