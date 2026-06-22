---
name: intensity-vector-manipulation-numpy
description: Use when you have extracted mass tracks (EICs) from multiple LC-MS samples aligned into a MassGrid structure, and you need to combine their intensity vectors into a single composite intensity vector for peak detection on the aggregate signal rather than per-sample.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - numpy
  - asari
  techniques:
  - LC-MS
derived_from:
- doi: 10.1038/s41467-023-39889-1
  title: asari
evidence_spans:
- Trackable and scalable Python program for high-resolution LC-MS metabolomics data preprocessing
- Trackable and scalable Python program for high-resolution metabolomics data processing.
- intensity_track is np.array(full RT length).
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

# Intensity vector manipulation with NumPy

## Summary

Aggregate and align intensity vectors from multiple mass tracks across LC-MS samples using NumPy array operations to construct a composite intensity profile for peak detection. This skill applies retention time calibration, element-wise summation, and vector consolidation to create unified composite mass tracks suitable for statistics-guided peak detection.

## When to use

You have extracted mass tracks (EICs) from multiple LC-MS samples aligned into a MassGrid structure, and you need to combine their intensity vectors into a single composite intensity vector for peak detection on the aggregate signal rather than per-sample. Specifically, when you have sample-specific retention time calibration dictionaries (rt_cal_dict) and need to project all intensities onto a reference sample's scan space before summing.

## When NOT to use

- Input is already a composite feature table or detected peak list; this skill is for pre-detection aggregation only.
- Mass tracks have not yet been aligned into a MassGrid; perform mass alignment first.
- Retention time calibration has not been performed; apply rt_cal_dict mapping before summation to avoid scan misalignment.

## Inputs

- MassGrid (m/z-aligned mass tracks across samples)
- Sample-specific retention time calibration dictionaries (rt_cal_dict)
- Aligned mass track intensity vectors (NumPy arrays, one per sample per m/z)

## Outputs

- CompositeMap.composite_tracks (indexed by m/z)
- Composite mass track objects (consensus m/z, summed intensity vector, parent_masstrack_id)

## How to apply

For each mass track in the MassGrid, retrieve the aligned mass track intensity vectors from all samples as NumPy arrays of full retention time length. Apply retention time calibration to each sample's intensity vector by remapping its scan indices using the sample-specific rt_cal_dict, aligning all vectors to the reference sample's scan space. Sum the calibrated intensity vectors element-wise across all samples at each scan position using NumPy to produce a single composite intensity vector of unified length. Construct composite mass track objects that retain both the consensus m/z value and the summed intensity vector, maintaining the parent_masstrack_id link for traceability. Store these composite tracks in the CompositeMap.composite_tracks data structure indexed by m/z for downstream peak detection.

## Related tools

- **numpy** (Element-wise intensity vector summation and array index remapping for retention time calibration) — https://numpy.org/
- **asari** (LC-MS workflow framework that orchestrates MassGrid construction and CompositeMap building) — https://github.com/shuzhao-li/asari

## Examples

```
# Pseudo-code from asari workflow:
for m_z in mass_grid.keys():
    aligned_tracks = mass_grid[m_z]
    composite_intensity = np.zeros(ref_sample_scan_length)
    for sample_id, track in aligned_tracks.items():
        calibrated = track.intensity[rt_cal_dict[sample_id]]
        composite_intensity += calibrated
    composite_map.add_track(m_z, composite_intensity, parent_id=track.id)
```

## Evaluation signals

- Composite intensity vectors have length equal to reference sample scan space (after rt_cal_dict remapping)
- Sum of composite intensity vector is greater than or equal to any individual sample's intensity vector at each m/z
- Composite tracks are indexed by consensus m/z and retrievable from CompositeMap.composite_tracks
- Parent_masstrack_id links are preserved and traceable back to original sample mass tracks
- No NaN or inf values in composite intensity vectors (exception: masked/missing scans should be handled consistently)

## Limitations

- Retention time calibration must be accurate; systematic rt_cal_dict errors will cause intensity misalignment across samples and spurious summed peaks.
- Composite map approach assumes that true metabolites produce co-eluting signals across samples; co-elution is prerequisite for valid summation.
- Element-wise summation can be dominated by high-intensity outlier samples; pre-processing filters (rescaling under ceiling, low-intensity track identification) should be applied first.
- Memory scales with number of samples and m/z resolution; large projects may require chunking or out-of-core processing.

## Evidence

- [other] For each mass track in the MassGrid, retrieve the corresponding aligned mass tracks from all samples and their intensity vectors (full RT length as np.array).: "For each mass track in the MassGrid, retrieve the corresponding aligned mass tracks from all samples and their intensity vectors (full RT length as np.array)."
- [other] Apply retention time calibration to each sample's mass track by remapping scan indices using the sample-specific rt_cal_dict to align all intensities to reference sample scan space.: "Apply retention time calibration to each sample's mass track by remapping scan indices using the sample-specific rt_cal_dict to align all intensities to reference sample scan space."
- [other] Sum the intensity values element-wise across all samples at each scan position to create a composite intensity vector of unified length.: "Sum the intensity values element-wise across all samples at each scan position to create a composite intensity vector of unified length."
- [other] Construct composite mass track objects containing the consensus m/z value and summed intensity vector, retaining the parent_masstrack_id link for downstream feature mapping.: "Construct composite mass track objects containing the consensus m/z value and summed intensity vector, retaining the parent_masstrack_id link for downstream feature mapping."
- [intro] Peak detection on a composite map instead of repeated on individual samples: "Peak detection on a composite map instead of repeated on individual samples"
