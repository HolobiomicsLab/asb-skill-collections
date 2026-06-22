---
name: sample-to-reference-retention-time-remapping
description: Use when after mass tracks have been aligned across samples into a MassGrid structure and retention time calibration dictionaries (rt_cal_dict) have been computed for each sample during prior alignment steps.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0637
  tools:
  - Python
  - numpy
  - asari.CompositeMap
  - asari.chromatograms
  techniques:
  - LC-MS
derived_from:
- doi: 10.1038/s41467-023-39889-1
  title: asari
evidence_spans:
- Trackable and scalable Python program for high-resolution LC-MS metabolomics data preprocessing
- Trackable and scalable Python program for high-resolution metabolomics data processing.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_asari_cq
    doi: 10.1038/s41467-023-39889-1
    title: asari
  dedup_kept_from: coll_asari_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-023-39889-1
  all_source_dois:
  - 10.1038/s41467-023-39889-1
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# sample-to-reference-retention-time-remapping

## Summary

Apply sample-specific retention time calibration dictionaries to remap scan indices from individual samples into a unified reference sample retention time space, enabling intensity vectors of different lengths to be aggregated into a composite map for peak detection. This is a prerequisite for cross-sample composite intensity summation in high-resolution LC-MS metabolomics.

## When to use

After mass tracks have been aligned across samples into a MassGrid structure and retention time calibration dictionaries (rt_cal_dict) have been computed for each sample during prior alignment steps. Use this skill immediately before summing aligned mass track intensities across samples, when individual samples have different scan lengths or retention time drifts that must be harmonized onto a reference sample timeline.

## When NOT to use

- Input is already a feature table or finalized peak detection output; retention time remapping is only needed during intermediate composite map construction, not downstream.
- Samples are already known to have identical retention time axes and no drift; skip remapping if all rt_cal_dict entries are identity mappings.
- Individual sample peak detection is the goal, not composite analysis; remapping is only necessary when aggregating intensities across multiple samples for a single composite map.

## Inputs

- MassGrid (m/z-aligned mass tracks across samples)
- retention time calibration dictionaries (rt_cal_dict) per sample
- intensity vectors as np.array (full RT length) from each sample's mass track

## Outputs

- retention-time-remapped intensity vectors (unified scan length per sample)
- composite intensity vectors (element-wise sum across all remapped samples)
- CompositeMap.composite_tracks data structure indexed by m/z

## How to apply

For each mass track in the MassGrid, retrieve the corresponding aligned mass tracks and intensity vectors (stored as np.array of full retention time length) from all samples. Apply the sample-specific rt_cal_dict to each sample's mass track by remapping its scan indices into the reference sample's scan space. The remapping function translates source sample scan positions to target reference positions using the calibration dictionary entries. After remapping, all intensity vectors are now aligned to the same reference scan space and unified length. This calibrated, length-matched intensity data then flows directly into element-wise summation to construct composite intensity vectors for the CompositeMap data structure.

## Related tools

- **numpy** (Element-wise array operations for intensity vector manipulation and remapping during calibration application)
- **asari.CompositeMap** (Data structure that stores composite_tracks indexed by m/z, receives remapped and summed intensity vectors as input) — https://github.com/shuzhao-li/asari
- **asari.chromatograms** (Extracts and manages mass tracks and retention time information prior to remapping) — https://github.com/shuzhao-li/asari

## Evaluation signals

- All remapped intensity vectors for a given m/z have identical length equal to the reference sample scan count
- Intensity values remain non-negative and within expected dynamic range after remapping (no out-of-bounds access or interpolation artifacts)
- Composite intensity vector (element-wise sum) shows expected increase in signal-to-noise ratio relative to individual sample mass tracks
- Retention time coordinates of peaks detected on the composite map are consistent with observed retention times in source samples after inverse remapping
- parent_masstrack_id links in composite mass track objects correctly trace back to original sample mass track identifiers

## Limitations

- Remapping accuracy depends on the quality and completeness of rt_cal_dict entries; sparse or poorly calibrated dictionaries will introduce systematic errors in intensity alignment.
- Intensity interpolation or extrapolation beyond the calibration dictionary's range may be required for edge scans; behavior at boundaries is not detailed in the article.
- The method assumes a single reference sample; multi-reference or sample-independent reference space workflows are not addressed.
- Extreme retention time drifts or non-linear drift patterns may exceed the expressiveness of a simple scan-index mapping and degrade alignment fidelity.

## Evidence

- [other] For each mass track in the MassGrid, retrieve the corresponding aligned mass tracks from all samples and their intensity vectors (full RT length as np.array).: "For each mass track in the MassGrid, retrieve the corresponding aligned mass tracks from all samples and their intensity vectors (full RT length as np.array)."
- [other] Apply retention time calibration to each sample's mass track by remapping scan indices using the sample-specific rt_cal_dict to align all intensities to reference sample scan space.: "Apply retention time calibration to each sample's mass track by remapping scan indices using the sample-specific rt_cal_dict to align all intensities to reference sample scan space."
- [other] Sum the intensity values element-wise across all samples at each scan position to create a composite intensity vector of unified length.: "Sum the intensity values element-wise across all samples at each scan position to create a composite intensity vector of unified length."
- [other] Load the MassGrid (m/z-aligned mass tracks across samples) and retention time calibration dictionaries (rt_cal_dict) for each sample from the prior alignment steps.: "Load the MassGrid (m/z-aligned mass tracks across samples) and retention time calibration dictionaries (rt_cal_dict) for each sample from the prior alignment steps."
- [other] Retention time alignment; Building the composite map: "Retention time alignment"
