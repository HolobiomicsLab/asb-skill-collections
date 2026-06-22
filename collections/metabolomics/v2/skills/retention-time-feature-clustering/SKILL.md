---
name: retention-time-feature-clustering
description: Use when after chromatographic peak detection (findChromPeaks) when you have a processed XcmsExperiment object with detected peaks and need to perform initial feature grouping. Use it when features of the same compound are expected to co-elute within a narrow retention-time window (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_0630
  - http://edamontology.org/topic_3370
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# retention-time-feature-clustering

## Summary

Group LC-MS features by similar retention time within a specified time window to create preliminary feature groups representing potential ions from the same compound. This is typically the first step in multi-stage feature grouping, reducing data complexity before applying abundance- or peak-shape-based refinement.

## When to use

Apply this skill after chromatographic peak detection (findChromPeaks) when you have a processed XcmsExperiment object with detected peaks and need to perform initial feature grouping. Use it when features of the same compound are expected to co-elute within a narrow retention-time window (e.g., 10–20 seconds in typical LC-MS), and before applying more sophisticated grouping methods based on abundance correlation or EIC similarity.

## When NOT to use

- Input data has not undergone chromatographic peak detection; call findChromPeaks() first.
- Retention-time information is missing or unreliable (e.g., drift exceeds tolerance window size).
- Feature groups should be based solely on MS/MS spectral similarity or external compound lists without chromatographic information.

## Inputs

- XcmsExperiment object with detected chromatographic peaks (result of findChromPeaks with centWave or similar)
- SimilarRtimeParam object specifying retention-time window (in seconds)

## Outputs

- XcmsExperiment object with featureGroups() populated by retention-time-based clustering
- Integer vector of feature group identifiers

## How to apply

Load a pre-processed XcmsExperiment object (xmse) and invoke the groupFeatures() function with SimilarRtimeParam(window_size_seconds) as the parameter. The window size (e.g., 20 seconds) defines the maximum retention-time tolerance within which features are clustered together. Features whose retention times fall within this window are assigned to the same feature group. The resulting grouped xmse object will have featureGroups() populated with integer group identifiers. This approach is fast and requires no sample-level information, making it suitable as a first-pass grouping step that can be followed by abundance-correlation or EIC-similarity refinement to split groups with low within-group coherence.

## Related tools

- **xcms** (Provides groupFeatures() function and SimilarRtimeParam class for retention-time-based feature grouping; implements the core peak detection and grouping workflow.) — https://github.com/sneumann/xcms
- **MsFeatures** (Supplies general MS feature grouping functionality and parameter classes used by xcms for modular grouping strategies.)

## Examples

```
groupFeatures(xmse, param = SimilarRtimeParam(20))
```

## Evaluation signals

- Verify that featureGroups() returns a non-empty integer vector with unique group IDs after grouping.
- Confirm that all features within a single group have retention times within the specified window (e.g., ±10 s for SimilarRtimeParam(20)).
- Check that the total number of feature groups is substantially smaller than the total number of individual features detected, indicating successful clustering.
- Validate that no features are unassigned (no NA values in featureGroups()).
- Compare the resulting group count to published benchmarks or expected ranges from prior experiments on the same dataset (e.g., faahKO).

## Limitations

- Retention-time-only grouping cannot distinguish features of different compounds that co-elute; subsequent refinement by abundance correlation or EIC similarity is often necessary to split such groups.
- The method is sensitive to retention-time calibration and reproducibility across runs; systematic drift can cause misalignment.
- Window size choice is heuristic and data-dependent; no automated parameter optimization is provided by the tool.
- Features with identical m/z and retention time but from different compounds (isomers, isobars) will be grouped together and require post-hoc disambiguation.

## Evidence

- [intro] Group features by similar retention time within specified time window: "groupFeatures(xmse, param = SimilarRtimeParam(10))"
- [other] Retention-time grouping clusters features into distinct feature groups: "When features are grouped using SimilarRtimeParam(20), the initial retention time-based grouping clusters features into distinct feature groups identified by the featureGroups() function."
- [intro] Features of the same compound should have similar retention time: "Features (ions) of the same compound should have similar retention time."
- [other] Retention-time grouping is a first step followed by abundance-based refinement: "After applying retention-time-based grouping with a 20-second window on the faahKO dataset, how many feature groups result from applying abundance correlation-based refinement"
- [readme] Tool provides efficient preprocessing for LC-MS data: "The *xcms* R package provides functionality to efficiently preprocess LC-MS (as well as GC-MS and LC-MS/MS) data."
