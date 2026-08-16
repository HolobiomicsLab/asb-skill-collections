---
name: composite-map-data-structure-construction
description: Use when after mass track extraction and alignment across samples, when you have a MassGrid structure (m/z-aligned mass tracks) and corresponding retention time calibration dictionaries for each sample, and need to prepare input for composite peak detection rather than per-sample peak detection.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - numpy
  - asari CompositeMap module
  - metDataModel
  techniques:
  - mass-spectrometry
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

# composite-map-data-structure-construction

## Summary

Constructs a CompositeMap data structure by aligning mass tracks across samples into a unified MassGrid, applying retention time calibration, and summing intensity vectors element-wise to create consensus m/z-indexed composite mass tracks for unified peak detection. This enables peak detection on aggregated signal rather than repeated independently on each sample.

## When to use

After mass track extraction and alignment across samples, when you have a MassGrid structure (m/z-aligned mass tracks) and corresponding retention time calibration dictionaries for each sample, and need to prepare input for composite peak detection rather than per-sample peak detection.

## When NOT to use

- When mass tracks have not yet been aligned across samples into a MassGrid structure
- When retention time calibration has not been computed or is unavailable for samples
- When peak detection should be performed independently on individual sample mass tracks rather than on aggregated composite signal

## Inputs

- MassGrid (m/z-aligned mass tracks across samples)
- Sample-specific retention time calibration dictionaries (rt_cal_dict)
- Aligned mass track intensity vectors (numpy arrays, full RT length per sample)

## Outputs

- CompositeMap data structure with composite_tracks
- Composite mass track objects indexed by m/z
- Summed intensity vectors (unified scan length)
- Parent mass track ID mappings for traceability

## How to apply

Load the MassGrid containing aligned mass tracks across all samples along with sample-specific retention time calibration dictionaries (rt_cal_dict). For each mass track in the MassGrid, retrieve the aligned mass track intensity vectors (full RT length as numpy arrays) from all samples. Apply retention time calibration to each sample's intensity vector by remapping scan indices using the sample-specific rt_cal_dict to align all intensities to reference sample scan space. Sum the calibrated intensity values element-wise across all samples at each scan position to generate a composite intensity vector of unified length. Construct composite mass track objects containing the consensus m/z value and the summed intensity vector, retaining parent_masstrack_id links for downstream traceability. Store the composite mass tracks in CompositeMap.composite_tracks indexed by m/z for access by subsequent peak detection operations.

## Related tools

- **numpy** (Element-wise summation and array manipulation of intensity vectors across aligned samples)
- **asari CompositeMap module** (Data structure container and orchestration for composite mass track construction) — https://github.com/shuzhao-li/asari
- **metDataModel** (Defines core data structures for composite mass tracks and metabolomic data models) — https://github.com/shuzhao-li-lab/metDataModel

## Examples

```
# Python snippet using asari workflow
from asari.workflows import CompositeMap
cmap = CompositeMap()
cmap.construct_composite_tracks(mass_grid=mgrid, rt_calibration_dicts=rt_cal_dicts)
composite_tracks = cmap.composite_tracks  # indexed by m/z for peak detection
```

## Evaluation signals

- Composite intensity vectors have unified length matching the reference sample scan space after retention time calibration
- All parent_masstrack_id links are preserved and traceable to original sample mass tracks
- Composite mass tracks are indexed by m/z and retrievable from CompositeMap.composite_tracks
- Sum of composite intensities reflects aggregation logic: no intensity values are duplicated or lost during element-wise summation
- Retention time calibration was correctly applied: scan index remapping aligns all samples to reference scan space before summation

## Limitations

- Composite map construction requires prior successful mass track alignment and RT calibration; misalignment will propagate incorrect intensity aggregation
- Element-wise summation assumes all intensity vectors have been correctly remapped to identical scan indices; any residual RT drift will skew composite signal
- Large sample numbers may inflate composite intensity values, potentially affecting subsequent peak detection thresholds and requiring intensity normalization or scaling in downstream steps
- The method does not account for differential sample abundance or batch effects; equal weighting in summation may mask or amplify sample-specific artifacts

## Evidence

- [other] Load the MassGrid (m/z-aligned mass tracks across samples) and retention time calibration dictionaries (rt_cal_dict) for each sample from the prior alignment steps.: "Load the MassGrid (m/z-aligned mass tracks across samples) and retention time calibration dictionaries (rt_cal_dict) for each sample from the prior alignment steps."
- [other] Apply retention time calibration to each sample's mass track by remapping scan indices using the sample-specific rt_cal_dict to align all intensities to reference sample scan space.: "Apply retention time calibration to each sample's mass track by remapping scan indices using the sample-specific rt_cal_dict to align all intensities to reference sample scan space."
- [other] Sum the intensity values element-wise across all samples at each scan position to create a composite intensity vector of unified length.: "Sum the intensity values element-wise across all samples at each scan position to create a composite intensity vector of unified length."
- [intro] Peak detection on a composite map instead of repeated on individual samples: "Peak detection on a composite map instead of repeated on individual samples"
- [other] Construct composite mass track objects containing the consensus m/z value and summed intensity vector, retaining the parent_masstrack_id link for downstream feature mapping.: "Construct composite mass track objects containing the consensus m/z value and summed intensity vector, retaining the parent_masstrack_id link for downstream feature mapping."
- [other] Store composite mass tracks in the CompositeMap.composite_tracks data structure indexed by m/z for access by peak detection.: "Store composite mass tracks in the CompositeMap.composite_tracks data structure indexed by m/z for access by peak detection."
- [readme] Our goal is to define a minimal set of data models to promote interoperability in computational metabolomics.: "Our goal is to define a minimal set of data models to promote interoperability in computational metabolomics."
