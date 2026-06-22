---
name: mass-grid-index-traversal-and-retrieval
description: Use when when you have constructed a MassGrid (m/z-aligned mass tracks across multiple samples) and need to retrieve all sample-specific mass tracks for a given m/z value in order to sum their intensities, apply retention time calibration, or construct composite mass track objects for peak.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0625
  tools:
  - Python
  - numpy
  - asari CompositeMap
  - asari chromatograms module
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
---

# mass-grid-index-traversal-and-retrieval

## Summary

Retrieve aligned mass tracks from a MassGrid structure by m/z index and access their corresponding intensity vectors across samples. This skill enables efficient lookup and aggregation of sample-specific mass track data during composite map construction for peak detection.

## When to use

When you have constructed a MassGrid (m/z-aligned mass tracks across multiple samples) and need to retrieve all sample-specific mass tracks for a given m/z value in order to sum their intensities, apply retention time calibration, or construct composite mass track objects for peak detection.

## When NOT to use

- Input is already a composite map or feature table — retrieval and summing have already been performed.
- Mass tracks have not yet been aligned into a MassGrid — perform mass separation and alignment first.
- Retention time calibration has not been computed — apply RT alignment before index traversal.

## Inputs

- MassGrid structure (m/z-indexed aligned mass tracks across samples)
- Retention time calibration dictionaries (rt_cal_dict) for each sample
- Individual sample mass tracks with intensity vectors (np.array, full RT length)

## Outputs

- Composite mass track objects (consensus m/z + summed intensity vector)
- CompositeMap.composite_tracks data structure (indexed by m/z)

## How to apply

For each m/z index in the MassGrid, retrieve the corresponding set of aligned mass tracks from all samples. Extract the full retention time-length intensity vector (as np.array) for each sample's mass track. Apply the sample-specific retention time calibration dictionary (rt_cal_dict) by remapping scan indices to align all intensities to reference sample scan space. Sum the intensity values element-wise across all samples at each scan position to produce a unified composite intensity vector. Package the consensus m/z value and summed intensity vector into a composite mass track object, preserving the parent_masstrack_id link for downstream feature-to-EIC traceability.

## Related tools

- **numpy** (Element-wise intensity vector summation and array indexing during mass track retrieval)
- **asari CompositeMap** (Core data structure that stores and indexes composite mass tracks by m/z for peak detection) — https://github.com/shuzhao-li/asari
- **asari chromatograms module** (Provides mass track construction and intensity vector extraction for each sample) — https://github.com/shuzhao-li/asari

## Evaluation signals

- Composite intensity vectors have unified length matching the reference sample scan space after RT calibration
- Sum of composite intensity vector ≥ max individual sample intensity for each m/z (no data loss)
- parent_masstrack_id links are preserved and traceable back to original sample mass tracks
- CompositeMap.composite_tracks is fully indexed by m/z with no missing or duplicate entries
- Composite mass tracks are ordered by m/z and ready as input to peak detection (scipy.signal.find_peaks)

## Limitations

- Requires retention time calibration to have been computed prior; misaligned or absent rt_cal_dict will produce spurious intensity aggregation.
- Element-wise summation assumes all samples have been mapped to a common reference scan space; differential scan counts or uncalibrated offsets will yield incorrect composite vectors.
- Large MassGrids with many samples and high m/z density can consume significant memory during intensity vector concatenation; batch processing or disk-based indexing may be needed for very large projects.
- Parent mass track IDs must be consistently maintained through retrieval; loss or duplication of IDs breaks downstream feature-to-EIC backtracking.

## Evidence

- [other] Load the MassGrid (m/z-aligned mass tracks across samples) and retention time calibration dictionaries (rt_cal_dict) for each sample from the prior alignment steps.: "Load the MassGrid (m/z-aligned mass tracks across samples) and retention time calibration dictionaries (rt_cal_dict)"
- [other] For each mass track in the MassGrid, retrieve the corresponding aligned mass tracks from all samples and their intensity vectors (full RT length as np.array).: "retrieve the corresponding aligned mass tracks from all samples and their intensity vectors (full RT length as np.array)"
- [other] Apply retention time calibration to each sample's mass track by remapping scan indices using the sample-specific rt_cal_dict to align all intensities to reference sample scan space.: "Apply retention time calibration to each sample's mass track by remapping scan indices using the sample-specific rt_cal_dict to align all intensities to reference sample scan space"
- [other] Sum the intensity values element-wise across all samples at each scan position to create a composite intensity vector of unified length.: "Sum the intensity values element-wise across all samples at each scan position to create a composite intensity vector of unified length"
- [other] Construct composite mass track objects containing the consensus m/z value and summed intensity vector, retaining the parent_masstrack_id link for downstream feature mapping.: "Construct composite mass track objects containing the consensus m/z value and summed intensity vector, retaining the parent_masstrack_id link"
- [other] Store composite mass tracks in the CompositeMap.composite_tracks data structure indexed by m/z for access by peak detection.: "Store composite mass tracks in the CompositeMap.composite_tracks data structure indexed by m/z for access by peak detection"
- [intro] Reproducible, track and backtrack between features and mass tracks (EICs): "track and backtrack between features and mass tracks (EICs)"
- [other] Aignment of mass tracks across samples, resulting in the MassGrid; See [CompositeMap.construct_mass_grid](CompositeMap.construct_mass_grid).: "Alignment of mass tracks across samples, resulting in the MassGrid"
