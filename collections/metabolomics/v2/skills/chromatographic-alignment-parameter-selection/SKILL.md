---
name: chromatographic-alignment-parameter-selection
description: Use when after chromatographic peak detection (e.g. centWave) has been performed on LC-MS data and you need to group features that likely originate from the same compound.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - MsFeatures
  - xcms
  - MsExperiment
  techniques:
  - LC-MS
  - tandem-MS
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

# chromatographic-alignment-parameter-selection

## Summary

Select and apply retention time-based feature grouping parameters to align chromatographic peaks across LC-MS samples. This skill clusters features detected at similar retention times into feature groups, reducing data complexity and preparing for downstream compound annotation.

## When to use

After chromatographic peak detection (e.g. centWave) has been performed on LC-MS data and you need to group features that likely originate from the same compound. Apply this skill when your analysis requires features with similar retention times to be consolidated into feature groups before abundance correlation or peak shape refinement steps. The decision hinges on whether compounds in your experiment are expected to elute within predictable retention time windows — typical for reverse-phase LC-MS/MS data.

## When NOT to use

- Input is already a feature table or matrix (peaks have already been grouped or summarized).
- Chromatographic peaks have not yet been detected — first apply centWave or equivalent peak detection.
- Your LC-MS data lacks reliable retention time information or uses highly variable retention time across runs due to poor chromatographic control.

## Inputs

- XcmsExperiment object with detected chromatographic peaks (from findChromPeaks)
- SimilarRtimeParam object with user-defined retention time window

## Outputs

- XcmsExperiment object with assigned feature groups (featureGroups column populated)
- Integer count of resulting feature groups

## How to apply

Load the preprocessed XcmsExperiment object (xmse) containing detected chromatographic peaks. Choose a retention time window parameter (e.g., SimilarRtimeParam(20) for a 20-second window) based on your chromatographic resolution and expected peak width; narrower windows (10–20 s) suit high-resolution separations, while wider windows (30+ s) accommodate drift or gradient variations. Call groupFeatures(xmse, param = SimilarRtimeParam(window_in_seconds)) to group features by similar retention time. Extract and count the resulting feature groups using featureGroups() to verify clustering. The rationale is that features of the same compound should have similar retention time; this initial grouping reduces false feature multiplicity before refining with abundance similarity or EIC peak shape metrics.

## Related tools

- **xcms** (Primary package providing groupFeatures() method, SimilarRtimeParam class, and XcmsExperiment container for retention time-based feature grouping) — https://github.com/sneumann/xcms
- **MsFeatures** (Provides general MS feature grouping functionality and parameter classes extended by xcms)
- **MsExperiment** (Container class for multi-modal MS data; XcmsExperiment extends this to hold preprocessed peak and grouping results)

## Examples

```
groupFeatures(xmse, param = SimilarRtimeParam(20))
featureGroups(xmse)
```

## Evaluation signals

- featureGroups() returns non-zero number of groups; verify count matches expected clustering density for your sample complexity.
- Retention time range within each feature group does not exceed the specified window parameter (e.g., max_rt_diff ≤ 20 s for SimilarRtimeParam(20)).
- Downstream abundance similarity or EIC similarity refinement (groupFeatures with AbundanceSimilarityParam or EicSimilarityParam) reduces the initial feature group count further, indicating the retention-time grouping captured true feature co-elution patterns.
- Manual inspection of a subset of grouped features confirms that grouped features have similar m/z and plausible isotope or adduct relationships consistent with the same compound.

## Limitations

- Retention time drift or batch effects across runs can cause features from the same compound to fall outside the window, resulting in false negatives (fragmented grouping). Pre-alignment or run correction may be needed for high-drift datasets.
- The window parameter is a fixed threshold; no adaptive tuning is performed based on actual peak width distribution. Users must set it manually or iterate empirically.
- Retention time alone does not distinguish isobaric compounds or overlapping peaks. Subsequent refinement with AbundanceSimilarityParam or EicSimilarityParam is strongly recommended to reduce false positives.
- This skill groups features; it does not impute missing peaks in samples where a feature is not detected. Missing signal recovery requires separate fillChromPeaks() step.

## Evidence

- [intro] Features of the same compound should have similar retention time: "Features (ions) of the same compound should have similar retention time."
- [intro] groupFeatures with SimilarRtimeParam is used to group features by retention time within a window: "groupFeatures(xmse, param = SimilarRtimeParam(10))"
- [intro] Feature grouping reduces data set complexity and aids annotation: "*Compounding* aims now at grouping such features presumably representing signal from the same originating compound to reduce data set complexity (and to aid in subsequent annotation steps)."
- [other] featureGroups() function is used to extract and count resulting feature groups: "Extract and count the resulting feature groups using featureGroups() to obtain the number of grouped features."
- [readme] XcmsExperiment is the recommended container for retention time-based grouping: "Version 4 adds native support for the [Spectra](https://github.com/RforMassSpectrometry/Spectra) package to `xcms` and allows to perform the pre-processing on `MsExperiment` objects"
