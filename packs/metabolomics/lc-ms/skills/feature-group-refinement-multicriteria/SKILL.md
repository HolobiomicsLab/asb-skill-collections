---
name: feature-group-refinement-multicriteria
description: 'Use when after initial retention-time-based feature grouping (e.g., ±20 s window) when you need to separate co-eluting features that are chemically distinct. Triggers include: (1) large feature groups (>2–3 members) suspected to contain multiple compounds;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - MsFeatures
  - xcms
  - MSnbase
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# feature-group-refinement-multicriteria

## Summary

Iteratively refine LC-MS feature groups using complementary similarity metrics—retention time, abundance correlation, and extracted ion chromatogram (EIC) shape—to resolve co-eluting ions and distinguish true adducts or fragments from spectral noise. This multi-criterion approach progressively splits initial retention-time-based groups into increasingly homogeneous sub-groups, each validated by orthogonal chemical properties.

## When to use

Apply this skill after initial retention-time-based feature grouping (e.g., ±20 s window) when you need to separate co-eluting features that are chemically distinct. Triggers include: (1) large feature groups (>2–3 members) suspected to contain multiple compounds; (2) need to validate that grouped features truly belong to the same metabolite; (3) presence of abundance patterns or EIC shapes that contradict co-identity; (4) requirement to distinguish adducts, in-source fragments, or isotopologues from true co-elutants.

## When NOT to use

- Input is already a consensus feature table or already has been refined by EIC similarity; re-running risks redundant splits and loss of chemical coherence.
- Sample count is <2; abundance correlation and EIC-to-sample overlap are undefined.
- All features in the input groups co-elute with identical abundance patterns and peak shapes; no orthogonal refinement is possible.

## Inputs

- Pre-processed LC-MS XcmsExperiment or xcmsSet object with detected chromatographic peaks
- Abundance-correlation-refined feature groups (output from AbundanceSimilarityParam refinement)
- Sample metadata with ≥2 samples (required for abundance correlation and EIC overlap)

## Outputs

- Hierarchically refined feature group object (XcmsExperiment or xcmsSet) with sub-groups indexed by EIC similarity
- Tabulated feature group count and membership (features per sub-group)
- Overlay EIC plots showing peak shape and retention-time alignment within and between sub-groups

## How to apply

Begin with pre-processed LC-MS data and retention-time-grouped feature groups (e.g., output from SimilarRtimeParam with 20 s window). Apply a three-stage refinement pipeline: (1) Filter by abundance correlation using AbundanceSimilarityParam to group features whose abundance vectors across samples are highly correlated (typical threshold ≥0.7); split groups whose members show discordant abundance patterns, as these indicate different metabolites. (2) Further refine using EicSimilarityParam with correlation threshold=0.7 and n=2 (top 2 samples) to measure EIC peak shape similarity; features with shifted retention times or distinct peak morphologies will separate into distinct sub-groups. (3) Inspect the final sub-groups: count the number of feature groups produced; overlay EIC plots for suspected groups (e.g., FG.013.001, FG.045.001) to visually confirm that sub-groups exhibit homogeneous retention time and peak shape. The rationale: abundance correlation captures co-regulation across the sample matrix (a hallmark of the same metabolite); EIC similarity adds instrumental evidence (peak shape and elution profile) that is independent of sample composition, catching cases where correlated abundance masks spectral heterogeneity.

## Related tools

- **xcms** (Core preprocessing and feature grouping engine; provides groupFeatures() function, SimilarRtimeParam, AbundanceSimilarityParam, and EicSimilarityParam classes) — https://github.com/sneumann/xcms
- **MsFeatures** (General MS feature grouping abstraction layer; encapsulates grouping parameter classes and dispatch logic)
- **MSnbase** (Provides XcmsExperiment and Spectra container classes for input data and chromatographic peak objects)

## Examples

```
groupFeatures(abundance_refined_groups, EicSimilarityParam(threshold=0.7, n=2))
```

## Evaluation signals

- Final feature group count is smaller than input count; at least one input group is split into ≥2 sub-groups (evidence of refinement occurred).
- Each sub-group exhibits abundance correlation ≥0.7 (threshold parameter); members with r < 0.7 are in separate groups.
- Overlay EIC plots for validation groups (e.g., FG.013.001, FG.045.001) show visually distinct retention-time clusters or peak morphologies between sub-groups; within-group EICs are congruent in shape and timing.
- For features assigned to the same sub-group, pairwise EIC correlation (computed on overlapping m/z–time windows in ≥2 samples) is ≥0.7.
- No further splits are observed when re-running the pipeline on the output groups with the same thresholds (convergence criterion).

## Limitations

- Requires ≥2 samples with detected signal at the feature location; gap-filling does not recover EIC morphology, only integrated abundance. If a feature is absent (chromatographic peak not detected) in >50% of samples, EIC correlation estimates become unreliable.
- EicSimilarityParam with n=2 uses only the top 2 samples by some criterion (likely highest total ion intensity or sample abundance rank); results may be sensitive to sample ordering or outliers. In very small cohorts or highly imbalanced designs, this can inflate or deflate apparent similarity.
- Abundance correlation is sensitive to batch effects, missing values, and non-linear relationships; two chemically distinct features may appear correlated if they are co-regulated by an unobserved confounder (e.g., sample preparation order).
- The threshold parameters (correlation ≥0.7) are heuristic and article-derived; different metabolite classes, ionization modes, or instruments may benefit from tuning. No principled method for selecting thresholds is provided in the article.

## Evidence

- [intro] Features (ions) of the same compound should have similar retention time. The abundance of features (ions) of the same compound should have a similar pattern across samples. The peak shape of EICs of features of the same compound should be similar: "Features (ions) of the same compound should have similar retention time. The abundance of features (ions) of the same compound should have a similar pattern across samples. The peak shape of"
- [intro] Retention time-based feature grouping with 20-second window grouped features into feature groups; abundance correlation-based refinement further split groups; EIC similarity analysis provided additional sub-grouping: "Grouping by similar retention time grouped the in total features into feature groups. Many of the larger retention time-based feature groups have been splitted into two or more sub-groups based on"
- [other] Apply groupFeatures() function with EicSimilarityParam specifying threshold=0.7 and n=2 to perform feature grouping based on EIC similarity correlation across the refined groups.: "Apply groupFeatures() function with EicSimilarityParam specifying threshold=0.7 and n=2 to perform feature grouping based on EIC similarity correlation across the refined groups."
- [other] After EIC similarity analysis with threshold 0.7 and n=2, features within feature groups FG.013.001 and FG.045.001 were subdivided into separate sub-groups, with one feature in FG.013.001 showing a shifted retention time in EIC plots that distinguished it from co-eluting features: "After EIC similarity analysis with threshold 0.7 and n=2, features within feature groups FG.013.001 and FG.045.001 were subdivided into separate sub-groups, with one feature in FG.013.001 showing a"
- [intro] AbundanceSimilarityParam: perform a feature grouping based on correlation of feature abundances (values) across samples.: "AbundanceSimilarityParam: perform a feature grouping based on correlation of feature abundances (values) across samples."
- [intro] EicSimilarityParam: perform a feature grouping based on correlation of EICs.: "EicSimilarityParam: perform a feature grouping based on correlation of EICs."
- [readme] The *xcms* R package provides functionality to efficiently preprocess LC-MS (as well as GC-MS and LC-MS/MS) data.: "The *xcms* R package provides functionality to efficiently preprocess LC-MS (as well as GC-MS and LC-MS/MS) data."
