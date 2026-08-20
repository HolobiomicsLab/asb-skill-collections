---
name: retention-time-alignment-mapping-application
description: Use when after mass tracks have been aligned across samples into a MassGrid structure and retention time calibration dictionaries (rt_cal_dict) have been computed for each sample, but before summing intensity vectors element-wise to construct the composite map.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - numpy
  - asari (CompositeMap module)
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# retention-time-alignment-mapping-application

## Summary

Apply retention time calibration mappings to mass tracks from individual samples, remapping scan indices to a unified reference sample space to enable valid intensity aggregation across samples into a composite map. This step ensures that intensity values at each retention time position are aligned before summation for peak detection.

## When to use

After mass tracks have been aligned across samples into a MassGrid structure and retention time calibration dictionaries (rt_cal_dict) have been computed for each sample, but before summing intensity vectors element-wise to construct the composite map. Use this skill when individual samples exhibit retention time drift or shifts that would cause intensities at the same m/z to be misaligned chronologically.

## When NOT to use

- Peak detection has already been performed independently on each sample (use composite map approach instead).
- Retention time calibration dictionaries have not yet been computed from the alignment step.
- Input mass tracks are not part of a MassGrid structure (single-sample analysis may not require cross-sample alignment).

## Inputs

- MassGrid (m/z-aligned mass tracks across samples)
- Sample-specific retention time calibration dictionaries (rt_cal_dict)
- Mass track intensity vectors (full RT length as numpy array) for each sample

## Outputs

- Retention time-aligned intensity vectors for each sample (remapped to reference scan space)
- Unified-length intensity vectors ready for element-wise summation

## How to apply

For each mass track in the MassGrid, retrieve the intensity vector (full RT length as np.array) from each sample along with its sample-specific rt_cal_dict. Apply the calibration by remapping the scan indices in each sample's intensity vector using the rt_cal_dict to transform them into reference sample scan space. This remapping ensures all intensity vectors are aligned to the same retention time grid before element-wise summation. The calibration is sample-specific because each sample may have experienced different chromatographic drift during the LC-MS run. After alignment, all intensity vectors will have unified length and temporal correspondence, enabling valid composite intensity construction.

## Related tools

- **Python** (Programming language for implementing retention time calibration remapping and scan index transformation)
- **numpy** (Array manipulation library for remapping scan indices and aligning intensity vectors)
- **asari (CompositeMap module)** (Orchestrates retention time alignment and composite map construction; calls rt_cal_dict application) — https://github.com/shuzhao-li/asari

## Evaluation signals

- All intensity vectors for a given mass track have equal length after alignment (unified to reference sample scan space)
- Scan indices in each sample's vector have been remapped according to their rt_cal_dict without data loss
- Element-wise summation of aligned intensity vectors produces a composite vector with expected dimensionality
- Retention time peaks in the composite map align spatially with peaks from individual samples when visualized together
- No NaN or out-of-bounds indices appear in remapped intensity vectors; index transformation is valid and invertible

## Limitations

- Accuracy of retention time alignment depends on quality of the rt_cal_dict computed in the preceding alignment step; poor calibration propagates into composite map errors.
- Assumes all samples share a common reference scan space; pathological cases where no samples are sufficiently similar may require manual reference selection.
- Remapping assumes monotonic or near-monotonic retention time drift; non-monotonic instrumental drift is not handled.
- Sample with extreme retention time shifts may introduce edge effects or gaps in the unified scan space if the calibration range does not fully overlap.

## Evidence

- [other] For each mass track in the MassGrid, retrieve the corresponding aligned mass tracks from all samples and their intensity vectors (full RT length as np.array). Apply retention time calibration to each sample's mass track by remapping scan indices using the sample-specific rt_cal_dict to align all intensities to reference sample scan space.: "For each mass track in the MassGrid, retrieve the corresponding aligned mass tracks from all samples and their intensity vectors (full RT length as np.array). 3. Apply retention time calibration to"
- [other] Sum the intensity values element-wise across all samples at each scan position to create a composite intensity vector of unified length.: "Sum the intensity values element-wise across all samples at each scan position to create a composite intensity vector of unified length."
- [intro] Peak detection on a composite map instead of repeated on individual samples: "Peak detection on a composite map instead of repeated on individual samples"
- [other] Alignment of mass tracks across samples, resulting in the MassGrid; See [CompositeMap.construct_mass_grid](CompositeMap.construct_mass_grid). Retention time alignment Building the composite map: "Alignment of mass tracks across samples, resulting in the MassGrid; See [CompositeMap.construct_mass_grid](CompositeMap.construct_mass_grid). Retention time alignment Building the composite map"
