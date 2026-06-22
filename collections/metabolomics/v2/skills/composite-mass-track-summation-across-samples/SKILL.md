---
name: composite-mass-track-summation-across-samples
description: Use when after mass tracks have been aligned across samples into a MassGrid structure (m/z-aligned, same mass-to-charge ratio) and retention time calibration dictionaries have been computed for each sample.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3674
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - Python
  - numpy
  - asari.CompositeMap.construct_mass_grid
  - asari.chromatograms.extract_massTracks_
  - asari.peaks.stats_detect_elution_peaks
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

# Reconstruct the composite map by summing aligned mass track intensities

## Summary

Aggregate intensity vectors from retention-time-aligned mass tracks across all samples into a composite map by element-wise summation at each scan position. This unified composite representation replaces independent peak detection on each sample, enabling statistics-guided peak detection on aggregated signal.

## When to use

After mass tracks have been aligned across samples into a MassGrid structure (m/z-aligned, same mass-to-charge ratio) and retention time calibration dictionaries have been computed for each sample. Apply this skill when you need to pool signal from multiple samples for improved peak detection sensitivity and reproducibility, rather than detecting peaks independently on each sample.

## When NOT to use

- Input is already a feature table or set of detected peaks (composite map construction precedes peak detection, not follows it).
- Mass tracks have not yet been aligned across samples into a MassGrid structure (perform mass alignment first).
- Retention time calibration has not been computed for all samples (rt_cal_dict must be available before intensity summation).

## Inputs

- MassGrid: m/z-aligned mass tracks across samples
- rt_cal_dict: sample-specific retention time calibration dictionaries
- intensity vectors (np.array): full RT-length intensity arrays per sample per mass track
- parent_masstrack_id links for traceability

## Outputs

- CompositeMap: collection of composite mass tracks indexed by m/z
- composite intensity vectors: element-wise sum of aligned, RT-calibrated intensities
- composite mass track objects: (consensus m/z, summed intensity vector, parent_masstrack_id)

## How to apply

Load the MassGrid (m/z-aligned mass tracks from all samples) and sample-specific retention time calibration dictionaries (rt_cal_dict) from prior alignment steps. For each mass track in the MassGrid, retrieve the corresponding intensity vectors (as np.array, full RT length) from all samples. Apply retention time calibration to each sample's mass track by remapping scan indices using the sample-specific rt_cal_dict to align all intensities to reference sample scan space, ensuring uniform length. Sum the intensity values element-wise across all samples at each scan position to create a single composite intensity vector. Construct composite mass track objects containing the consensus m/z value and summed intensity vector, and store them in the CompositeMap.composite_tracks data structure indexed by m/z for downstream peak detection.

## Related tools

- **numpy** (Element-wise array summation and intensity vector manipulation)
- **asari.CompositeMap.construct_mass_grid** (Constructs the MassGrid from aligned mass tracks prior to composite map building) — https://github.com/shuzhao-li/asari
- **asari.chromatograms.extract_massTracks_** (Extracts individual mass tracks from each sample before alignment and summation) — https://github.com/shuzhao-li/asari
- **asari.peaks.stats_detect_elution_peaks** (Peak detection performed on the composite map output from this skill) — https://github.com/shuzhao-li/asari

## Evaluation signals

- All composite mass tracks have consistent m/z values matching the MassGrid index.
- Composite intensity vectors have uniform length equal to the reference sample scan space after RT calibration.
- Sum of composite intensities at each scan position equals the sum of corresponding aligned intensities from all samples.
- parent_masstrack_id links are retained in composite mass track objects for traceability back to individual sample tracks.
- Composite intensity values are non-negative and magnitude is increased by factor proportional to number of samples (assuming additive signal).

## Limitations

- Assumes retention time calibration has been correctly computed; errors in rt_cal_dict propagate to misaligned intensity summation.
- Element-wise summation treats all samples equally; samples with extreme baseline or noise dominate composite signal.
- Requires all samples to have mass tracks at the same m/z; missing mass tracks in some samples contribute zero intensity.
- No per-sample weighting or robust aggregation (e.g., median, trimmed mean) is applied; outlier samples can inflate composite signal.

## Evidence

- [other] The asari workflow constructs a composite map by aligning mass tracks across samples into a MassGrid structure, which serves as the input for subsequent peak detection operations rather than performing peak detection independently on each sample.: "constructs a composite map by aligning mass tracks across samples into a MassGrid structure, which serves as the input for subsequent peak detection operations"
- [other] For each mass track in the MassGrid, retrieve the corresponding aligned mass tracks from all samples and their intensity vectors (full RT length as np.array). Apply retention time calibration to each sample's mass track by remapping scan indices using the sample-specific rt_cal_dict to align all intensities to reference sample scan space. Sum the intensity values element-wise across all samples at each scan position to create a composite intensity vector of unified length.: "retrieve the corresponding aligned mass tracks from all samples and their intensity vectors (full RT length as np.array). Apply retention time calibration to each sample's mass track by remapping"
- [intro] Peak detection on a composite map instead of repeated on individual samples: "Peak detection on a composite map instead of repeated on individual samples"
- [other] Construct composite mass track objects containing the consensus m/z value and summed intensity vector, retaining the parent_masstrack_id link for downstream feature mapping. Store composite mass tracks in the CompositeMap.composite_tracks data structure indexed by m/z for access by peak detection.: "Construct composite mass track objects containing the consensus m/z value and summed intensity vector, retaining the parent_masstrack_id link for downstream feature mapping. Store composite mass"
