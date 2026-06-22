---
name: lc-ms-feature-grouping-by-retention-time
description: Use when immediately after chromatographic peak detection (findChromPeaks) when you have detected peaks across multiple samples and need to identify which peaks represent the same feature across the sample cohort.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - MsFeatures
  - xcms
  techniques:
  - LC-MS
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

# LC-MS feature grouping by retention time

## Summary

Groups chromatographic peaks detected across LC-MS samples into feature groups based on similarity of retention time within a specified time window. This is the first dimensionality-reduction step in the xcms preprocessing workflow, consolidating ions that likely derive from the same compound eluting at similar times.

## When to use

Apply this skill immediately after chromatographic peak detection (findChromPeaks) when you have detected peaks across multiple samples and need to identify which peaks represent the same feature across the sample cohort. Use it when you have a pre-processed XcmsExperiment or xcmsSet object with detected peaks but peaks have not yet been grouped or compared across samples.

## When NOT to use

- Input is already feature-grouped by retention time or beyond (e.g., already passed through abundance-correlation grouping); apply only once per workflow
- Chromatographic peaks have not yet been detected in raw data; run findChromPeaks first
- Retention time calibration across samples is severely misaligned (>RT window); recalibrate retention times before grouping

## Inputs

- XcmsExperiment or xcmsSet object with detected chromatographic peaks (output from findChromPeaks)
- SimilarRtimeParam object specifying retention time window threshold (e.g., 10 seconds)

## Outputs

- XcmsExperiment or xcmsSet object with features grouped by retention time similarity
- Feature group membership table mapping peaks to group IDs

## How to apply

Call groupFeatures() on your peak-detected xmse object with a SimilarRtimeParam parameter specifying a retention time window (typically 10 seconds based on the article workflow). The algorithm groups peaks whose retention times fall within this window across all samples, assuming features of the same compound co-elute. Choose the time window based on your chromatographic resolution and instrument stability; tighter windows require better RT reproducibility but reduce false grouping of co-eluting compounds. This output serves as input to downstream abundance-correlation or EIC-similarity refinement steps to progressively separate co-eluting ions of different compounds.

## Related tools

- **xcms** (Provides groupFeatures() function and SimilarRtimeParam class; implements retention time-based grouping algorithm) — https://github.com/sneumann/xcms
- **MsFeatures** (Defines general MS feature grouping functionality; xcms extends with LC-MS-specific implementations)

## Examples

```
groupFeatures(xmse, param = SimilarRtimeParam(10))
```

## Evaluation signals

- Output object contains a valid featureDefinitions data frame with column 'npeaks' reflecting number of peaks per group and 'rtmed' showing median retention time per group
- Total number of groups is less than the initial number of detected peaks (dimensionality reduction achieved)
- Retention time range within each group does not exceed the specified window threshold (e.g., max RT – min RT ≤ 10 seconds)
- Peaks within a group span multiple samples (indicating cross-sample consolidation), not just single-sample replicates
- Downstream abundance-correlation or EIC-similarity grouping produces monotonically decreasing or stable feature group counts, not artificial inflation

## Limitations

- Requires good retention time reproducibility across samples; poor calibration or batch effects can create false groups
- Does not use m/z or peak shape information; co-eluting ions of different compounds will be incorrectly grouped together unless refined by later steps (abundance correlation, EIC similarity)
- Fixed retention time window may be suboptimal for complex samples with variable ionization efficiency or for metabolites with very similar RT; manual tuning recommended
- Assumes linear or monotonic retention time behavior; non-linear RT drift across a large run batch may require per-sample or sliding-window approaches not captured by single global window

## Evidence

- [intro] Features (ions) of the same compound should have similar retention time.: "Features (ions) of the same compound should have similar retention time."
- [intro] Group features by similar retention time within specified time window: "Group features by similar retention time within specified time window"
- [intro] groupFeatures(xmse, param = SimilarRtimeParam(10)): "groupFeatures(xmse, param = SimilarRtimeParam(10))"
- [intro] The feature grouping functions base on the following assumptions/properties of LC-MS data: - Features (ions) of the same compound should have similar retention time.: "The feature grouping functions base on the following assumptions/properties of LC-MS data: - Features (ions) of the same compound should have similar retention time."
