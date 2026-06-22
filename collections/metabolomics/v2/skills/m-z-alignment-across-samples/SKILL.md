---
name: m-z-alignment-across-samples
description: Use when you have extracted mass tracks (EICs) from multiple LC-MS samples at 0.001 amu resolution and need to construct a sample-agnostic m/z reference frame.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - pymzml
  - mass_functions.nn_cluster_by_mz_seeds
  - chromatograms.get_thousandth_bins
  - chromatograms.extract_single_track_fullrt_length
  - MassGrid.build_grid_sample_wise
  - MassGrid.build_grid_by_centroiding
  - MassGrid.bin_track_mzs
  - ext_Experiment.get_reference_sample_id
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
  - build: coll_asari
    doi: 10.1038/s41467-023-39889-1
    title: asari
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

# m-z-alignment-across-samples

## Summary

Align mass tracks (EICs) detected in individual LC-MS samples into a unified MassGrid structure by leveraging high mass resolution to detect and resolve m/z differences corresponding to isotopes and adducts, then bin and centroid m/z values across the cohort. This enables reproducible tracking between detected features and their underlying chromatographic traces.

## When to use

You have extracted mass tracks (EICs) from multiple LC-MS samples at 0.001 amu resolution and need to construct a sample-agnostic m/z reference frame. Apply this skill when you have ≥2 samples with overlapping mass tracks and systematic m/z drift between instruments or scan modes, or when you want to consolidate features across a cohort into a single feature table indexed by m/z.

## When NOT to use

- Input mass tracks have already been merged or consolidated into a feature table—apply this skill during intermediate processing, not post-hoc.
- Mass resolution is <0.001 amu (e.g., low-resolution quadrupole or TOF instruments)—the skill depends on high mass resolution to prioritize mass separation.
- You are aligning only a single sample—the skill is designed for cross-sample alignment; intra-sample mass tracking uses different functions.

## Inputs

- Mass tracks (EICs) extracted from each sample
- Binned m/z values at 0.001 amu resolution per sample
- Retention time-aligned chromatographic intensity traces
- Sample metadata (instrument, acquisition mode, optional reference sample designation)

## Outputs

- MassGrid: unified m/z reference frame with one row per unique mass track
- MassGrid row content: m/z identifier, sample indices, sample-specific m/z values, anchor track flags
- Recalibration function (if systematic drift >1 ppm detected)
- Mass track-to-sample mapping (_mass_grid_mapping.csv)

## How to apply

First, bin all m/z values within each sample at 0.001 amu resolution and merge adjacent bins within tolerance using nearest-neighbor clustering by m/z seeds to resolve overlapping m/z values (chromatograms.get_thousandth_bins, mass_functions.nn_cluster_by_mz_seeds). Identify anchor mass tracks in each sample by detecting m/z differences matching 13C/12C isotopes or Na/H adducts; select the reference sample as the one with the highest number of anchor tracks unless user-specified. For small studies (≤10 samples), perform pairwise alignment by comparing anchor mass tracks first and recalibrating all m/z values if systematic drift exceeds 1 ppm, then align remaining mass tracks. For larger studies (>10 samples), apply nearest-neighbor clustering on all mass tracks across samples to bin and centroid m/z values into a unified MassGrid. Validate that the MassGrid contains one m/z row per unique mass track identifier, each row lists sample indices and their corresponding m/z values, and anchor tracks are marked with higher priority.

## Related tools

- **pymzml** (Parse mzML centroid spectra files to extract m/z and intensity data) — https://github.com/shuzhao-li/asari
- **mass_functions.nn_cluster_by_mz_seeds** (Perform nearest-neighbor clustering on m/z values by seeds to bin and resolve overlapping m/z) — https://github.com/shuzhao-li/asari
- **chromatograms.get_thousandth_bins** (Bin m/z values at 0.001 amu resolution and merge adjacent bins within tolerance) — https://github.com/shuzhao-li/asari
- **chromatograms.extract_single_track_fullrt_length** (Identify anchor mass tracks by detecting characteristic m/z differences (isotopes, adducts)) — https://github.com/shuzhao-li/asari
- **MassGrid.build_grid_sample_wise** (Perform pairwise sample-by-sample alignment for small studies (≤10 samples)) — https://github.com/shuzhao-li/asari
- **MassGrid.build_grid_by_centroiding** (Apply nearest-neighbor clustering for large studies to bin and centroid m/z across all samples) — https://github.com/shuzhao-li/asari
- **MassGrid.bin_track_mzs** (Bin sample-specific m/z values into unified MassGrid rows) — https://github.com/shuzhao-li/asari
- **ext_Experiment.get_reference_sample_id** (Identify or designate the reference sample with highest anchor mass track count) — https://github.com/shuzhao-li/asari

## Examples

```
from asari.mass_functions import nn_cluster_by_mz_seeds; from asari.chromatograms import get_thousandth_bins; grid = MassGrid(samples, mass_tracks); grid.build_grid_by_centroiding() if len(samples) > 10 else grid.build_grid_sample_wise()
```

## Evaluation signals

- MassGrid schema invariant: exactly one m/z row per unique mass track identifier; no duplicate rows.
- Each MassGrid row contains sample indices and corresponding m/z values for all samples contributing mass tracks to that m/z bin; samples not contributing that mass track are marked or absent.
- Anchor mass tracks are correctly flagged and have priority in alignment; verify by comparing 13C/12C and Na/H m/z offsets against theoretical values (1.003 amu for 13C/12C, 22.990 amu for Na/H adduct mass difference).
- Systematic m/z drift between samples (before recalibration) is ≤1 ppm post-alignment; drift >1 ppm triggers recalibration logic and should be corrected in output m/z values.
- Feature reproducibility: mass tracks within ±1 ppm of the MassGrid m/z row centroid are correctly backtracked to the same feature; inspect _mass_grid_mapping.csv for correct sample-to-feature assignments.

## Limitations

- For studies >10 samples, centroiding-based alignment may reduce fine m/z precision if samples have large systematic drifts; recalibration is applied but assumes drift is uniform across m/z range.
- Anchor mass track identification depends on sufficient signal-to-noise and presence of isotope or adduct patterns; low-intensity or single-ion mass tracks may not have detectable anchors and alignment quality degrades.
- The 1 ppm drift threshold is empirically set for high-resolution Orbitrap data; different instrument types (Q-TOF, quadrupole) may require parameter adjustment.
- MassGrid does not retroactively align retention times; cross-sample retention time drift must be addressed in a separate alignment step before or after MassGrid construction.

## Evidence

- [other] Asari aligns mass tracks across samples by constructing a MassGrid, a process that leverages high mass resolution to prioritize mass separation and alignment, enabling reproducible tracking and backtracking between features and mass tracks (EICs).: "Asari aligns mass tracks across samples by constructing a MassGrid, a process that leverages high mass resolution to prioritize mass separation and alignment, enabling reproducible tracking and"
- [other] Extract mass tracks from each sample using pymzml and bin m/z values at 0.001 amu resolution, merging adjacent bins within tolerance and applying nearest-neighbor clustering by m/z seeds to resolve overlapping m/z values: "Extract mass tracks from each sample using pymzml and bin m/z values at 0.001 amu resolution, merging adjacent bins within tolerance and applying nearest-neighbor clustering by m/z seeds to resolve"
- [other] Identify anchor mass tracks by detecting m/z differences matching 13C/12C isotopes or Na/H adducts within each sample: "Identify anchor mass tracks by detecting m/z differences matching 13C/12C isotopes or Na/H adducts within each sample"
- [other] For small studies (≤10 samples), perform pairwise alignment by comparing anchor mass tracks first, recalibrating all m/z values if systematic drift exceeds 1 ppm, then aligning remaining mass tracks: "For small studies (≤10 samples), perform pairwise alignment by comparing anchor mass tracks first, recalibrating all m/z values if systematic drift exceeds 1 ppm, then aligning remaining mass tracks"
- [other] For larger studies, apply nearest-neighbor clustering on all mass tracks across samples to bin and centroid m/z values into a unified MassGrid: "For larger studies, apply nearest-neighbor clustering on all mass tracks across samples to bin and centroid m/z values into a unified MassGrid"
- [other] MassGrid contains one m/z row per unique mass track identifier, each row lists sample indices and their corresponding m/z values, and anchor tracks are marked with higher priority in the alignment structure.: "MassGrid contains one m/z row per unique mass track identifier, each row lists sample indices and their corresponding m/z values, and anchor tracks are marked with higher priority in the alignment"
- [intro] Taking advantage of high mass resolution to prioritize mass separation and alignment: "Taking advantage of high mass resolution to prioritize mass separation and alignment"
