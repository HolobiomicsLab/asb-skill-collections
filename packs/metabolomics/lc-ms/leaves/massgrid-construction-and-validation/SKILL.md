---
name: massgrid-construction-and-validation
description: 'Use when after individual mass tracks (EICs) have been extracted from each sample''s mzML file and you need to create a unified, cross-sample m/z reference structure. Triggered when: (1) you have ≥2 samples in a cohort; (2) mass tracks have been binned at 0.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3557
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - pymzml
  - mass_functions.nn_cluster_by_mz_seeds
  - chromatograms.get_thousandth_bins
  - chromatograms.extract_single_track_fullrt_length
  - ext_Experiment.get_reference_sample_id
  - MassGrid.build_grid_sample_wise
  - MassGrid.add_sample
  - MassGrid.build_grid_by_centroiding
  - MassGrid.bin_track_mzs
  techniques:
  - LC-MS
derived_from:
- doi: 10.1038/s41467-023-39889-1
  title: asari
evidence_spans:
- Trackable and scalable Python program for high-resolution LC-MS metabolomics data preprocessing
- Trackable and scalable Python program for high-resolution metabolomics data processing.
- The default method uses `pymzml` to parse mzML files.
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

# massgrid-construction-and-validation

## Summary

Construction and validation of a unified MassGrid by aligning mass tracks across multiple LC-MS samples using high mass resolution and anchor mass track detection. The MassGrid serves as the backbone for subsequent peak detection and feature extraction, ensuring reproducible tracking between raw mass tracks (EICs) and detected features across the study cohort.

## When to use

After individual mass tracks (EICs) have been extracted from each sample's mzML file and you need to create a unified, cross-sample m/z reference structure. Triggered when: (1) you have ≥2 samples in a cohort; (2) mass tracks have been binned at 0.001 amu resolution and nearest-neighbor clustered within each sample; (3) anchor mass tracks (isotopes, adducts) have been identified; and (4) you are preparing for composite-map peak detection rather than per-sample peak calling.

## When NOT to use

- Input is already a composite feature table or peak feature table (MassGrid is a pre-feature intermediate); construct it only during mass track alignment, before peak detection.
- Single-sample analysis where cross-sample alignment is not needed; MassGrid assumes multiple samples.
- Mass tracks have not yet been extracted or binned; first run chromatograms.extract_massTracks_ and bin at 0.001 amu resolution.

## Inputs

- mass_tracks_per_sample (list of EICs, binned at 0.001 amu resolution and nearest-neighbor clustered)
- sample_metadata (sample identifiers, file paths)
- anchor_track_catalog (detected 13C/12C isotopes and Na/H adducts per sample)
- reference_sample_id (optional; auto-selected if not provided)

## Outputs

- MassGrid (unified data structure with m/z rows, sample indices, and m/z values per row)
- mass_track_identifiers (mapping between MassGrid rows and original per-sample mass tracks)
- recalibration_report (m/z drift statistics and correction factors applied)

## How to apply

First, identify anchor mass tracks (e.g., 13C/12C isotope pairs, Na/H adducts) within each sample using characteristic m/z differences. Select a reference sample—typically the one with the highest number of anchor mass tracks unless user-specified. For studies ≤10 samples, perform pairwise alignment by comparing anchor mass tracks first, recalibrating all m/z values if systematic drift exceeds 1 ppm, then aligning remaining mass tracks using MassGrid.build_grid_sample_wise and MassGrid.add_sample. For larger studies, apply nearest-neighbor clustering across all mass tracks from all samples, binning and centroiding m/z values into a unified MassGrid using MassGrid.build_grid_by_centroiding and MassGrid.bin_track_mzs. Validate the output: confirm that each MassGrid row represents one unique mass track identifier, each row contains sample indices and their corresponding m/z values, and anchor tracks are marked with higher priority in the alignment structure.

## Related tools

- **pymzml** (Parse centroid mzML files to extract mass tracks and retention time data) — https://github.com/shuzhao-li-lab/asari
- **mass_functions.nn_cluster_by_mz_seeds** (Perform nearest-neighbor clustering of mass tracks by m/z seeds to resolve overlapping m/z values within and across samples) — https://github.com/shuzhao-li-lab/asari
- **chromatograms.get_thousandth_bins** (Bin mass tracks at 0.001 amu resolution and merge adjacent bins within tolerance) — https://github.com/shuzhao-li-lab/asari
- **chromatograms.extract_single_track_fullrt_length** (Identify anchor mass tracks by detecting m/z differences matching 13C/12C isotopes or Na/H adducts) — https://github.com/shuzhao-li-lab/asari
- **ext_Experiment.get_reference_sample_id** (Automatically select reference sample (highest anchor track count) unless user-specified) — https://github.com/shuzhao-li-lab/asari
- **MassGrid.build_grid_sample_wise** (Construct MassGrid for small studies (≤10 samples) by pairwise anchor-track-guided alignment) — https://github.com/shuzhao-li-lab/asari
- **MassGrid.add_sample** (Add aligned mass tracks from each sample to the MassGrid during pairwise alignment) — https://github.com/shuzhao-li-lab/asari
- **MassGrid.build_grid_by_centroiding** (Construct MassGrid for larger studies by clustering all mass tracks across samples and centroiding m/z) — https://github.com/shuzhao-li-lab/asari
- **MassGrid.bin_track_mzs** (Bin and centroid m/z values from all samples into unified MassGrid rows) — https://github.com/shuzhao-li-lab/asari

## Evaluation signals

- MassGrid contains exactly one row per unique mass track identifier; no duplicates or missing rows.
- Each MassGrid row lists all sample indices that contain a mass track at that m/z, with corresponding m/z values for each sample recorded.
- Anchor tracks are marked with higher priority in the alignment structure; verify via presence of isotope/adduct flags in output metadata.
- m/z recalibration report shows systematic drift corrections; if drift >1 ppm detected, verify recalibration was applied and post-correction drift is <1 ppm.
- Trackability validation: confirm that each MassGrid row m/z value maps back to the original per-sample mass track(s) via the mass_track_identifiers mapping.

## Limitations

- For studies >10 samples, pairwise alignment becomes computationally expensive; asari switches to nearest-neighbor clustering by centroiding, which may sacrifice fine m/z precision if clusters are too broad.
- Anchor track detection depends on correct identification of isotope and adduct m/z differences; if the compound library or adduct list is incomplete, some samples may be misclassified or poorly aligned.
- High mass resolution (e.g., Orbitrap) is required to enable the m/z separation and 0.001 amu binning strategy; lower-resolution instruments (e.g., quadrupole) may not support the same alignment precision.
- Systematic m/z drift is corrected only if it exceeds 1 ppm; smaller drifts (<1 ppm) are not recalibrated, and may accumulate across large studies.

## Evidence

- [other] Asari aligns mass tracks across samples by constructing a MassGrid, a process that leverages high mass resolution to prioritize mass separation and alignment, enabling reproducible tracking and backtracking between features and mass tracks (EICs).: "Asari aligns mass tracks across samples by constructing a MassGrid, a process that leverages high mass resolution to prioritize mass separation and alignment, enabling reproducible tracking and"
- [other] Extract mass tracks from each sample using pymzml and bin m/z values at 0.001 amu resolution, merging adjacent bins within tolerance and applying nearest-neighbor clustering by m/z seeds to resolve overlapping m/z values (chromatograms.get_thousandth_bins, mass_functions.nn_cluster_by_mz_seeds).: "Extract mass tracks from each sample using pymzml and bin m/z values at 0.001 amu resolution, merging adjacent bins within tolerance and applying nearest-neighbor clustering by m/z seeds to resolve"
- [other] Identify anchor mass tracks by detecting m/z differences matching 13C/12C isotopes or Na/H adducts within each sample (chromatograms.extract_single_track_fullrt_length).: "Identify anchor mass tracks by detecting m/z differences matching 13C/12C isotopes or Na/H adducts within each sample"
- [other] For small studies (≤10 samples), perform pairwise alignment by comparing anchor mass tracks first, recalibrating all m/z values if systematic drift exceeds 1 ppm, then aligning remaining mass tracks (MassGrid.build_grid_sample_wise, MassGrid.add_sample).: "For small studies (≤10 samples), perform pairwise alignment by comparing anchor mass tracks first, recalibrating all m/z values if systematic drift exceeds 1 ppm, then aligning remaining mass tracks"
- [other] For larger studies, apply nearest-neighbor clustering on all mass tracks across samples to bin and centroid m/z values into a unified MassGrid (MassGrid.build_grid_by_centroiding, MassGrid.bin_track_mzs).: "For larger studies, apply nearest-neighbor clustering on all mass tracks across samples to bin and centroid m/z values into a unified MassGrid"
- [other] MassGrid contains one m/z row per unique mass track identifier, each row lists sample indices and their corresponding m/z values, and anchor tracks are marked with higher priority in the alignment structure.: "MassGrid contains one m/z row per unique mass track identifier, each row lists sample indices and their corresponding m/z values, and anchor tracks are marked with higher priority"
- [readme] Taking advantage of high mass resolution to prioritize mass separation and alignment: "Taking advantage of high mass resolution to prioritize mass separation and alignment"
