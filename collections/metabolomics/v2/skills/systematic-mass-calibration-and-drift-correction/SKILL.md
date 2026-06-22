---
name: systematic-mass-calibration-and-drift-correction
description: Use when when processing multiple LC-MS samples in a cohort study and MassGrid construction reveals that anchor mass tracks (13C/12C isotope or Na/H adduct pairs) in non-reference samples deviate systematically from the reference sample's m/z values by >1 ppm.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - pymzml
  - mass_functions.nn_cluster_by_mz_seeds
  - chromatograms.extract_single_track_fullrt_length
  - ext_Experiment.get_reference_sample_id
  - MassGrid.build_grid_sample_wise
derived_from:
- doi: 10.1038/s41467-023-39889-1
  title: asari
evidence_spans:
- Trackable and scalable Python program for high-resolution LC-MS metabolomics data preprocessing
- Trackable and scalable Python program for high-resolution metabolomics data processing.
- The default method uses `pymzml` to parse mzML files.
- nearest neighbor (NN) clustering is performed to establish the number of mass tracks. The NN clustering assigns each data point to its nearest 'peak mz value'.
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

# Systematic Mass Calibration and Drift Correction

## Summary

Detect and correct systematic m/z drift across multiple LC-MS samples by comparing anchor mass tracks (isotopes and adducts) between a reference sample and other samples, recalibrating all m/z values when drift exceeds 1 ppm. This ensures reproducible mass track alignment and prevents false feature misalignment in cross-sample metabolomics studies.

## When to use

When processing multiple LC-MS samples in a cohort study and MassGrid construction reveals that anchor mass tracks (13C/12C isotope or Na/H adduct pairs) in non-reference samples deviate systematically from the reference sample's m/z values by >1 ppm. This indicates time-dependent instrument drift that, if uncorrected, will cause mass tracks from the same metabolite to align at different m/z values across samples, producing false feature splits.

## When NOT to use

- When processing a single sample or when all samples were acquired in a short time window with minimal instrument drift (<0.5 ppm observed).
- When anchor mass tracks cannot be confidently identified (e.g., very low-complexity samples with few isotope pairs or adducts).
- When drift appears non-linear or sample-dependent (e.g., temperature ramping during acquisition); linear correction assumes uniform systematic drift across the m/z range.

## Inputs

- Raw mass tracks extracted from each sample (EICs with m/z and intensity arrays)
- Identified anchor mass tracks (isotope pairs and adduct doublets) from each sample
- Reference sample index (sample with highest anchor track count or user-specified)
- Mass track metadata including sample ID, m/z centroid, and detected isotope/adduct relationships

## Outputs

- Recalibrated m/z values for all mass tracks in drifting samples
- Drift correction metadata (m/z offset per sample, ppm deviation, correction applied flag)
- Aligned MassGrid with corrected m/z rows, ready for retention time alignment and feature detection

## How to apply

After extracting anchor mass tracks from each sample (isotope pairs and common adducts) and selecting a reference sample (the one with the highest number of anchor tracks, or user-specified), perform pairwise comparison of anchor tracks between the reference and each other sample. Calculate the systematic m/z offset by measuring the difference in anchor track m/z values. If the offset exceeds 1 ppm, apply a linear recalibration function to all m/z values in that sample to shift them back into alignment with the reference. The recalibration should be based on the median or robust fit of anchor track offsets to avoid bias from outliers. Validate by confirming that recalibrated anchor tracks now overlap with reference anchors within mass resolution tolerance (typically 0.001 amu for high-resolution Orbitrap data).

## Related tools

- **pymzml** (Parse mzML files and extract mass track (EIC) data with m/z and retention time coordinates)
- **mass_functions.nn_cluster_by_mz_seeds** (Cluster and identify anchor mass tracks (isotope pairs, adducts) by m/z similarity within tolerance) — https://github.com/shuzhao-li/asari
- **chromatograms.extract_single_track_fullrt_length** (Extract full retention-time-length mass tracks and quantify anchor relationships (13C offset, Na/H adduct mass difference)) — https://github.com/shuzhao-li/asari
- **ext_Experiment.get_reference_sample_id** (Identify or confirm the reference sample (highest number of anchor tracks) for drift comparison) — https://github.com/shuzhao-li/asari
- **MassGrid.build_grid_sample_wise** (Build MassGrid with pairwise sample alignment, applying m/z recalibration when drift is detected) — https://github.com/shuzhao-li/asari

## Examples

```
# Python example within asari processing workflow:
# After extracting mass tracks and anchor pairs, recalibrate before MassGrid construction:
mass_grid = MassGrid()
mass_grid.build_grid_sample_wise(samples, reference_sample_id, drift_threshold_ppm=1.0)
```

## Evaluation signals

- After recalibration, the m/z offset between anchor tracks in a corrected sample and the reference sample should be <0.3 ppm (well within high-resolution mass accuracy).
- The distribution of anchor track m/z differences should show a single tight peak (mean ~0, std <0.2 ppm) after correction, rather than a systematic shift.
- Retention-time alignment and subsequent feature detection should show fewer spurious feature splits caused by m/z misalignment across samples.
- The MassGrid m/z rows should contain consistent m/z values for the same metabolite across samples, with no systematic drift-induced spreading visible in the feature table.
- Recalibration metadata should log the ppm offset per sample and confirm all samples exceeded or fell below the 1 ppm threshold before applying correction.

## Limitations

- Assumes systematic (linear or constant) drift across the m/z range; non-linear or m/z-dependent drift requires more complex models.
- Relies on the presence of sufficient, confidently identified anchor mass tracks; samples with very few isotope pairs or adducts may lack statistical power for robust drift estimation.
- A 1 ppm threshold may be too strict or too lenient depending on the instrument and sample complexity; threshold should be validated against downstream feature overlap and false positive rates.
- Does not account for time-varying drift during a single acquisition; assumes each sample's drift is constant across its acquisition window.
- Recalibration is performed before retention-time alignment, so retention-time drift is not corrected at this stage.

## Evidence

- [other] Identify anchor mass tracks by detecting m/z differences matching 13C/12C isotopes or Na/H adducts within each sample: "Identify anchor mass tracks by detecting m/z differences matching 13C/12C isotopes or Na/H adducts within each sample (chromatograms.extract_single_track_fullrt_length)."
- [other] Select the reference sample as the one with the highest number of anchor mass tracks unless user-specified: "Select the reference sample as the one with the highest number of anchor mass tracks unless user-specified (ext_Experiment.get_reference_sample_id)."
- [other] For small studies (≤10 samples), perform pairwise alignment by comparing anchor mass tracks first, recalibrating all m/z values if systematic drift exceeds 1 ppm: "For small studies (≤10 samples), perform pairwise alignment by comparing anchor mass tracks first, recalibrating all m/z values if systematic drift exceeds 1 ppm, then aligning remaining mass tracks"
- [other] Asari aligns mass tracks across samples by constructing a MassGrid, a process that leverages high mass resolution to prioritize mass separation and alignment: "Asari aligns mass tracks across samples by constructing a MassGrid, a process that leverages high mass resolution to prioritize mass separation and alignment, enabling reproducible tracking and"
- [intro] Taking advantage of high mass resolution to prioritize mass separation and alignment: "Taking advantage of high mass resolution to prioritize mass separation and alignment"
