---
name: feature-abundance-pattern-matching
description: Use when after initial retention-time-based feature grouping when you have groups of multiple features at similar m/z and retention time but need to determine which features actually arise from the same compound.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - MsFeatures
  - xcms
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

# feature-abundance-pattern-matching

## Summary

Refine LC-MS feature groups by correlating abundance patterns across samples to identify features of the same compound. This skill groups features whose ion intensities co-vary in a similar pattern, distinguishing true co-eluting features from artifacts or unrelated ions at similar m/z and retention time.

## When to use

Apply this skill after initial retention-time-based feature grouping when you have groups of multiple features at similar m/z and retention time but need to determine which features actually arise from the same compound. Use it when you observe that retention-time-based grouping alone produces groups that are too broad or contain features with uncorrelated abundance patterns across samples.

## When NOT to use

- Input data contains only a single sample or very few replicates; abundance correlation is meaningless without within-group sample variance.
- Feature abundances are not measured on a comparable scale across samples (e.g., raw intensity counts without normalization or batch correction may produce spurious correlations).
- The research question focuses only on m/z and retention time similarity and does not require chemical compound identity validation.

## Inputs

- xcms XcmsExperiment object or preprocessed feature abundance matrix (rows: features, columns: samples)
- feature groups from SimilarRtimeParam grouping (FeatureGroupsParam object or equivalent)

## Outputs

- refined feature groups object (FeatureGroupsParam result after AbundanceSimilarityParam refinement)
- abundance-correlation-refined feature groups table with feature-to-group-ID mapping

## How to apply

Load the xcms-preprocessed LC-MS data and the feature groups output from a SimilarRtimeParam-based grouping step. Apply the groupFeatures() function with AbundanceSimilarityParam, which computes feature abundance correlation across all samples and uses a user-specified correlation threshold (commonly threshold=0.7 or similar) to subdivide existing feature groups. Features whose abundances across samples correlate above this threshold are kept together; those below the threshold are split into separate sub-groups. The rationale is that features from the same compound should show highly correlated intensity patterns across replicates and conditions, while unrelated ions should show uncorrelated abundances. Visualize the resulting refined groups using plotFeatureGroups() to verify that sub-groups are now more homogeneous.

## Related tools

- **xcms** (provides groupFeatures() method and AbundanceSimilarityParam class to perform abundance-correlation-based feature grouping and refinement) — https://github.com/sneumann/xcms
- **MsFeatures** (general MS feature grouping framework that integrates with xcms for modular grouping-parameter dispatch) — https://github.com/RforMassSpectrometry/MsFeatures

## Examples

```
groupFeatures(feature_groups, AbundanceSimilarityParam(threshold=0.7))
```

## Evaluation signals

- Verify that the number of feature groups increases (or group count remains stable) after abundance-based refinement, compared to retention-time-only grouping, indicating successful sub-grouping.
- Confirm that within each resulting sub-group, Pearson or Spearman correlation of feature abundances across samples is ≥ the specified threshold (e.g., ≥0.7).
- Check that features split into separate sub-groups show abundance correlation values below the threshold, confirming they were correctly separated.
- Overlay the m/z and retention time coordinates of sub-groups and visually inspect that features in different sub-groups are indeed distinct in m/z or RT, not just poorly correlated.
- Compare the refined groups against a reference standard or known compound co-elution patterns (if available) to validate biological or chemical plausibility.

## Limitations

- Abundance correlation requires sufficient sample replication and variance; groups with low signal intensity or high noise may produce unreliable correlations.
- The threshold parameter is user-specified and data-dependent; no automatic threshold selection is provided; threshold choice significantly affects the number of sub-groups produced.
- Features from different ionization products (e.g., [M+H]+ and [M+Na]+) of the same compound may have lower abundance correlation if their ionization efficiency varies across samples, potentially leading to incorrect splitting.
- Post-translational modifications, isobars, or contaminants that co-elute may show high abundance correlation by chance and remain falsely grouped together.

## Evidence

- [intro] AbundanceSimilarityParam: perform a feature grouping based on correlation of feature abundances (values) across samples.: "AbundanceSimilarityParam: perform a feature grouping based on correlation of feature abundances (values) across samples."
- [intro] The abundance of features (ions) of the same compound should have a similar pattern across samples.: "The abundance of features (ions) of the same compound should have a similar pattern across samples. The peak shape of"
- [intro] abundance correlation-based refinement further split groups: "Grouping by similar retention time grouped the in total features into feature groups. Many of the larger retention time-based feature groups have been splitted into two or more sub-groups based on"
- [other] Apply groupFeatures() function with AbundanceSimilarityParam specifying threshold=0.7 and n=2 to perform feature grouping based on EIC similarity correlation across the refined groups.: "Apply groupFeatures() function with AbundanceSimilarityParam specifying threshold=0.7 and n=2 to perform feature grouping based on EIC similarity correlation across the refined groups."
