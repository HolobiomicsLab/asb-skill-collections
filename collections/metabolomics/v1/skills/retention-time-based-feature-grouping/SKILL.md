---
name: retention-time-based-feature-grouping
description: Use when after chromatographic peak detection on preprocessed LC-MS data when you have an xcms result object (XcmsExperiment or xcmsSet) with detected peaks and need to collapse redundant m/z signals into feature groups.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0091
  tools:
  - MsFeatures
  - xcms
  - MsExperiment
derived_from:
- doi: 10.1021/acs.analchem.5c04338
  title: xcms
evidence_spans:
- General MS feature grouping functionality if defined by the `r Biocpkg("MsFeatures")` package
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

# retention-time-based-feature-grouping

## Summary

Initial grouping of LC-MS features by similar retention time using a sliding window (e.g., 20 seconds) to co-locate ions likely from the same metabolite, prior to refinement by abundance correlation or EIC similarity. This is the first step in a multi-stage feature correspondence workflow.

## When to use

Apply this skill after chromatographic peak detection on preprocessed LC-MS data when you have an xcms result object (XcmsExperiment or xcmsSet) with detected peaks and need to collapse redundant m/z signals into feature groups. Use it as the initial coarse grouping stage before abundance or EIC-based refinement, especially when ions of the same compound are expected to co-elute within a known retention time window (e.g., 20 s for standard HPLC methods).

## When NOT to use

- If peaks have already been grouped by a downstream method (e.g., abundance correlation or EIC similarity); this is a foundational grouping step, not a refinement.
- If your experiment uses a non-standard chromatographic method (e.g., very fast gradient, gas chromatography) where the 20 s window does not match expected co-elution behavior.
- If you need to group features across samples with different retention time calibrations; alignment should precede this skill.

## Inputs

- xcms result object (XcmsExperiment or xcmsSet) with detected chromatographic peaks
- SimilarRtimeParam parameter object specifying retention time window (in seconds)

## Outputs

- Feature groups (integer vector assigning each peak to a group ID)
- Summary statistics: total number of groups, count and distribution of features per group
- Grouped feature assignments suitable for downstream refinement or visualization

## How to apply

Load a preprocessed xcms result object containing detected chromatographic peaks. Define a SimilarRtimeParam object specifying the retention time window (e.g., window=20 for a 20-second tolerance). Pass this parameter to the groupFeatures() function, which clusters all detected peaks into groups where any two peaks within the same group differ by ≤ the window threshold in retention time. Extract the resulting feature group assignments and compute summary statistics (number of groups, distribution of group sizes). This coarse grouping exploits the principle that features of the same compound should have similar retention time; larger groups may be further refined by abundance correlation or EIC similarity in downstream steps.

## Related tools

- **xcms** (Core package providing groupFeatures() method and SimilarRtimeParam class for retention time-based feature clustering) — https://github.com/sneumann/xcms
- **MsFeatures** (General MS feature grouping functionality that defines or extends grouping parameter classes and methods)
- **MsExperiment** (Data container (alternative to XcmsExperiment) holding raw spectra and results for groupFeatures() input)

## Examples

```
groupFeatures(xcms_result, SimilarRtimeParam(window=20))
```

## Evaluation signals

- Reproducibility: re-running groupFeatures with identical SimilarRtimeParam(20) on the same xcms object yields identical feature group assignments
- Invariant: all features within a group differ by ≤ 20 seconds in retention time; no feature is assigned to multiple groups
- Distribution check: verify the reported number of groups and group size frequencies match expected biological constraints (e.g., no singleton groups if the window is too small)
- Downstream compatibility: grouped features are accepted by subsequent refinement methods (AbundanceSimilarityParam, EicSimilarityParam) without conversion errors
- Visual inspection: plotFeatureGroups() or equivalent visualization shows connected features in m/z–retention time space clustering as expected

## Limitations

- The choice of window size (e.g., 20 s) is arbitrary and must be tuned to match the chromatographic resolution and expected co-elution behavior of your method; no data-driven default is provided.
- Retention time-based grouping alone cannot distinguish isomers or compounds with identical m/z and retention time; it must be followed by abundance or spectral refinement.
- Groups can be large and heterogeneous (containing unrelated features) if the window is too wide, necessitating downstream filtering.
- This method assumes retention time is accurately measured and calibrated; uncalibrated or drifting retention times across a sample batch will produce spurious groupings.

## Evidence

- [intro] Initial retention time-based grouping: "SimilarRtimeParam: perform an initial grouping based on similar retention time."
- [intro] Feature co-elution principle: "Features (ions) of the same compound should have similar retention time."
- [intro] Multi-stage refinement workflow: "Retention time-based feature grouping with 20-second window grouped features into feature groups. Many of the larger retention time-based feature groups have been splitted into two or more sub-groups"
- [intro] Downstream refinement stages: "AbundanceSimilarityParam: perform a feature grouping based on correlation of feature abundances (values) across samples."
- [readme] xcms core functionality: "Version 4 adds native support for the Spectra package to xcms and allows to perform the pre-processing on MsExperiment objects"
