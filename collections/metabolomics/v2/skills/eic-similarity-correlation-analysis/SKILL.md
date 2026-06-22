---
name: eic-similarity-correlation-analysis
description: Use when after abundance-correlation-based feature group refinement when you observe that larger feature groups (particularly those with 3+ features in the same m/z–retention-time window) may contain features with different peak shapes or retention-time shifts in their EICs, or when abundance.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - MsFeatures
  - xcms
  techniques:
  - LC-MS
  - GC-MS
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

# EIC-similarity-correlation-analysis

## Summary

Refine feature groups by correlating extracted ion chromatogram (EIC) peak shapes across samples using EicSimilarityParam, subdividing co-eluting or poorly correlated features into distinct sub-groups. This skill applies after retention-time and abundance-based grouping to resolve features that share m/z and retention time but have divergent chromatographic profiles.

## When to use

Apply this skill after abundance-correlation-based feature group refinement when you observe that larger feature groups (particularly those with 3+ features in the same m/z–retention-time window) may contain features with different peak shapes or retention-time shifts in their EICs, or when abundance correlation alone leaves chemically distinct features grouped together.

## When NOT to use

- Input feature groups are already well-separated by retention time (e.g., no co-eluting features); EIC refinement would add no new information.
- Sample count is very low (n < 2), making EIC correlation unreliable across the top n samples.
- Features have noisy or irregular peak shapes that produce unstable EIC correlations independent of true chemical similarity.

## Inputs

- XcmsExperiment object or xcms feature groups (output from AbundanceSimilarityParam refinement)
- EicSimilarityParam object with threshold and n parameters

## Outputs

- Feature groups subdivided by EIC similarity (new feature group count)
- Overlay EIC plots showing sub-group distinctions within feature groups

## How to apply

Load pre-processed LC-MS data and abundance-refined feature groups into R using xcms. Apply the groupFeatures() function with EicSimilarityParam, specifying a correlation threshold (e.g., threshold=0.7) and the number of top samples to use for EIC correlation calculation (e.g., n=2). The function calculates pairwise EIC similarities by correlating peak shapes across the specified samples and subdivides groups where features fail to meet the threshold. Extract the final feature group count and generate overlay EIC plots using plotEICs() to visualize whether sub-groups show distinct peak shapes or retention-time shifts that justify the subdivision.

## Related tools

- **xcms** (Primary tool providing groupFeatures() method with EicSimilarityParam class and plotEICs() visualization function for LC-MS feature grouping and EIC correlation analysis) — https://github.com/sneumann/xcms
- **MsFeatures** (Provides general MS feature grouping functionality framework integrated with xcms for EIC-based sub-grouping)

## Examples

```
groupFeatures(xcms_obj, param = EicSimilarityParam(threshold = 0.7, n = 2))
```

## Evaluation signals

- Final feature group count increases (subdivisions are created) compared to abundance-refined input; document the change in number of groups.
- Sub-divided feature groups within FG.013.001 or similar show measurable retention-time offset (e.g., >0.5 s) in overlay EIC plots, visually justifying the split.
- Correlation coefficients among features within newly created sub-groups exceed the specified threshold (e.g., >0.7), while correlations between sub-groups fall below it.
- EIC peak shapes within sub-groups are visually congruent (same apex time, width, and skew), whereas features assigned to different sub-groups exhibit divergent peak morphologies.

## Limitations

- EIC similarity refinement depends on reliable peak shape; noisy or poorly detected chromatographic peaks produce unreliable correlations.
- The threshold and n parameters are user-specified; their choice significantly affects sub-grouping outcome and must be validated empirically (e.g., via visual inspection of EIC plots for features like FG.013.001 and FG.045.001).
- If all features in a group pass the correlation threshold, no sub-grouping occurs; the skill does not subdivide groups when features are genuinely co-eluting and similarly shaped.
- EIC correlation is computed across the top n samples; choice of n affects stability and may miss weaker signals or features only abundant in minor samples.

## Evidence

- [other] After EIC similarity analysis with threshold 0.7 and n=2, features within feature groups FG.013.001 and FG.045.001 were subdivided into separate sub-groups, with one feature in FG.013.001 showing a shifted retention time in EIC plots that distinguished it from co-eluting features, and FG.045.001 being grouped into two distinct sub-groups based on EIC correlation patterns.: "After EIC similarity analysis with threshold 0.7 and n=2, features within feature groups FG.013.001 and FG.045.001 were subdivided into separate sub-groups, with one feature in FG.013.001 showing a"
- [other] Apply groupFeatures() function with EicSimilarityParam specifying threshold=0.7 and n=2 to perform feature grouping based on EIC similarity correlation: "Apply groupFeatures() function with EicSimilarityParam specifying threshold=0.7 and n=2 to perform feature grouping based on EIC similarity correlation across the refined groups."
- [intro] Features (ions) of the same compound should have similar retention time. The abundance of features (ions) of the same compound should have a similar pattern across samples. The peak shape of EICs of features of the same compound should be similar: "Features (ions) of the same compound should have similar retention time. The abundance of features (ions) of the same compound should have a similar pattern across samples. The peak shape of"
- [intro] EicSimilarityParam: perform a feature grouping based on correlation of EICs.: "EicSimilarityParam: perform a feature grouping based on correlation of EICs."
- [readme] The *xcms* R package provides functionality to efficiently preprocess LC-MS (as well as GC-MS and LC-MS/MS) data.: "The *xcms* R package provides functionality to efficiently preprocess LC-MS (as well as GC-MS and LC-MS/MS) data."
