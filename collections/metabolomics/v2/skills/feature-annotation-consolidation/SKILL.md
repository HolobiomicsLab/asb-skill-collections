---
name: feature-annotation-consolidation
description: Use when after chromatographic peak detection and feature detection in LC-MS preprocessing, when you have a set of detected features (m/z, retention time, intensity) and need to consolidate redundant or related ion signals into compound-level feature groups before downstream statistical or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - MsFeatures
  - xcms
  - faahKO
derived_from:
- doi: 10.1021/ac051437y
  title: XCMS
evidence_spans:
- General MS feature grouping functionality if defined by the `r Biocpkg("MsFeatures")` package
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

# feature-annotation-consolidation

## Summary

Consolidate multiple feature annotations (ions of the same compound) by applying a multi-stage filtering pipeline: initial retention-time-based grouping, followed by abundance correlation refinement and EIC similarity analysis. This skill identifies which features across m/z and retention time space belong to the same molecular entity.

## When to use

After chromatographic peak detection and feature detection in LC-MS preprocessing, when you have a set of detected features (m/z, retention time, intensity) and need to consolidate redundant or related ion signals into compound-level feature groups before downstream statistical or annotation analysis. Triggers include: (1) raw feature table contains many features with similar retention times but different m/z values; (2) you expect isotope adducts or in-source fragments; (3) abundance patterns or EIC shapes suggest multiple features derive from the same molecular entity.

## When NOT to use

- Input is already a consolidated compound-level feature table or pre-grouped feature set; re-grouping will overwrite existing annotations.
- Raw MS data has not yet undergone peak detection or alignment; features have not been extracted.
- Retention time calibration is severely poor (large systematic drift); grouping window will be unreliable.

## Inputs

- XcmsExperiment or xcmsSet object (preprocessed with chromatographic peaks detected via findChromPeaks)
- Feature m/z and retention time coordinates (from chromPeaks)
- Feature intensity matrix across samples

## Outputs

- Feature group assignments (mapping each feature to a group ID)
- Table of group sizes and distribution
- Annotated feature groups with retention time and m/z ranges

## How to apply

Begin with retention-time-based grouping using SimilarRtimeParam with a 20-second window—this coarse-grained step groups features that co-elute, exploiting the principle that ions of the same compound should have similar retention time. Refine these groups using AbundanceSimilarityParam, which splits larger retention-time groups based on feature abundance correlation patterns across samples: ions from the same compound should share similar relative abundance profiles. Further resolve sub-groups using EicSimilarityParam to compare extracted ion chromatogram (EIC) peak shapes and correlation. Apply filters at each stage to exclude outlier features and improve group cohesion. Visualize results in m/z–retention time space using plotFeatureGroups to inspect whether grouped features are spatially and temporally coherent. Success is indicated by tight clustering of grouped features and absence of spatially distant or temporally disjoint features within the same group.

## Related tools

- **xcms** (Provides groupFeatures() method and parameter classes (SimilarRtimeParam, AbundanceSimilarityParam, EicSimilarityParam) for multi-stage feature consolidation) — https://github.com/sneumann/xcms
- **MsFeatures** (General MS feature grouping functionality and parameter interface)
- **faahKO** (Reference dataset for benchmarking feature grouping workflows)

## Examples

```
groupFeatures(xcms_result, SimilarRtimeParam(window=20)); # followed by AbundanceSimilarityParam and EicSimilarityParam refining steps
```

## Evaluation signals

- Total count of feature groups produced matches reference values reported for the dataset (e.g., faahKO with SimilarRtimeParam(20)).
- Distribution of group sizes is unimodal or expected based on compound diversity; no pathologically large groups (>100 features per group unless expected from isotope clusters).
- Features within each group cluster tightly in m/z–retention time space (no spatially distant outliers when visualized with plotFeatureGroups).
- Abundance correlation within groups is significantly higher than between groups (measured via Pearson or Spearman correlation).
- EIC peak shapes within groups exhibit high similarity; cross-correlation scores between grouped EICs are above threshold (e.g., >0.7).

## Limitations

- Retention-time-based grouping assumes features of the same compound co-elute; early-eluting impurities or late-phase isomers may be misclustered.
- Abundance correlation refinement can fail if feature ion abundances are decoupled (e.g., selective ion suppression or different ionization efficiency); very weak features may show noisy correlation patterns.
- EIC similarity analysis is sensitive to peak shape distortion from overlap or noise; features with poor chromatographic resolution will yield unreliable similarity scores.
- Multi-stage filtering may remove valid features if window parameters (retention-time window, correlation threshold, EIC similarity threshold) are too stringent.
- For samples with missing chromatographic peaks (gap-filling required), feature abundance patterns may be incomplete, degrading correlation-based grouping.

## Evidence

- [intro] Features (ions) of the same compound should have similar retention time. The abundance of features (ions) of the same compound should have a similar pattern across samples. The peak shape of [EICs] of features of the same compound should be similar.: "Features (ions) of the same compound should have similar retention time. The abundance of features (ions) of the same compound should have a similar pattern across samples. The peak shape of"
- [intro] SimilarRtimeParam: perform an initial grouping based on similar retention time.: "SimilarRtimeParam: perform an initial grouping based on similar retention time."
- [intro] AbundanceSimilarityParam: perform a feature grouping based on correlation of feature abundances (values) across samples.: "AbundanceSimilarityParam: perform a feature grouping based on correlation of feature abundances (values) across samples."
- [intro] EicSimilarityParam: perform a feature grouping based on correlation of EICs.: "EicSimilarityParam: perform a feature grouping based on correlation of EICs."
- [intro] Grouping by similar retention time grouped the in total features into feature groups. Many of the larger retention time-based feature groups have been splitted into two or more sub-groups based on: "Grouping by similar retention time grouped the in total features into feature groups. Many of the larger retention time-based feature groups have been splitted into two or more sub-groups based on"
- [intro] plotFeatureGroups function which shows all features in the m/z - retention time space with grouped features being connected with a line.: "plotFeatureGroups function which shows all features in the m/z - retention time space with grouped features being connected with a line."
- [other] When applying SimilarRtimeParam(20) to group features by retention time, the faahKO dataset features were grouped into a specific number of feature groups with varying sizes, as shown by the table of group sizes produced by the grouping operation.: "When applying SimilarRtimeParam(20) to group features by retention time, the faahKO dataset features were grouped into a specific number of feature groups with varying sizes, as shown by the table of"
- [intro] General MS feature grouping functionality if defined by the `r Biocpkg("MsFeatures")` package: "General MS feature grouping functionality if defined by the `r Biocpkg("MsFeatures")` package"
