---
name: isotope-adduct-anchor-identification
description: Use when when you have extracted mass tracks (EICs) from individual LC-MS
  samples and need to establish reliable landmarks for subsequent pairwise or global
  alignment across a cohort.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - pymzml
  - chromatograms.extract_single_track_fullrt_length
  - mass_functions.nn_cluster_by_mz_seeds
  - chromatograms.get_thousandth_bins
  - ext_Experiment.get_reference_sample_id
  - mass2chem
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1038/s41467-023-39889-1
  title: asari
evidence_spans:
- Trackable and scalable Python program for high-resolution LC-MS metabolomics data
  preprocessing
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

# isotope-adduct-anchor-identification

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Identify anchor mass tracks within individual LC-MS samples by detecting characteristic m/z differences corresponding to 13C/12C isotope patterns or common adducts (e.g., Na/H). These anchors serve as high-confidence reference points for cross-sample mass track alignment into a unified MassGrid.

## When to use

When you have extracted mass tracks (EICs) from individual LC-MS samples and need to establish reliable landmarks for subsequent pairwise or global alignment across a cohort. This skill is essential before attempting to construct a MassGrid, especially when systematic m/z drift or sample-to-sample m/z variation is suspected. Use it when you have high mass resolution data (0.001 amu binning tolerance or better) and want to leverage isotope/adduct relationships to prioritize alignment accuracy.

## When NOT to use

- Input is already a feature table or composite map (anchors must be identified on raw mass tracks before alignment).
- Mass resolution is insufficient to resolve isotope shifts reliably (e.g., low-resolution TOF or Orbitrap at <5 ppm accuracy).
- Sample cohort contains <2 samples, making cross-sample alignment unnecessary.

## Inputs

- mass tracks (EICs) extracted per sample from mzML files
- binned m/z values at 0.001 amu or finer resolution
- full retention time chromatogram data for each mass track
- sample metadata (sample identifiers, optional reference sample designation)

## Outputs

- anchor mass track identifiers and m/z values per sample
- isotope/adduct relationship annotations (delta m/z, type)
- reference sample ID and its anchor track set
- m/z recalibration parameters (if drift > 1 ppm detected)
- sample-wise anchor track counts and quality metrics

## How to apply

For each sample, scan all extracted mass tracks for pairs or clusters that exhibit m/z differences matching known isotope shifts (e.g., 13C-12C = 1.00335 amu, or Na-H adducts = 21.98194 amu) within the specified mass resolution tolerance (typically 0.001 amu or 1 ppm). Use nearest-neighbor clustering by m/z seeds to group co-eluting or overlapping tracks, then apply pattern matching (e.g., chromatograms.extract_single_track_fullrt_length) to identify isotope ladders or adduct families. Retain only those anchor mass tracks that meet a minimum signal-to-noise and peak shape criterion (SNR and Gaussian fit quality). The reference sample is selected as the one with the highest count of anchor mass tracks (unless user-specified), and its anchor tracks are used as calibration reference for downstream m/z recalibration if systematic drift exceeds 1 ppm across the cohort.

## Related tools

- **chromatograms.extract_single_track_fullrt_length** (Detects isotope and adduct m/z differences within a single sample's mass tracks) — https://github.com/shuzhao-li/asari
- **mass_functions.nn_cluster_by_mz_seeds** (Clusters overlapping m/z values by nearest-neighbor seeding to resolve co-eluting isotope/adduct families) — https://github.com/shuzhao-li/asari
- **chromatograms.get_thousandth_bins** (Bins and merges m/z values at 0.001 amu resolution for precise isotope/adduct detection) — https://github.com/shuzhao-li/asari
- **ext_Experiment.get_reference_sample_id** (Selects the reference sample based on highest count of anchor mass tracks) — https://github.com/shuzhao-li/asari
- **mass2chem** (Provides chemical formula utilities and adduct/isotope mass pattern lookup tables) — https://github.com/shuzhao-li/mass2chem

## Examples

```
from asari import chromatograms, mass_functions; anchors = chromatograms.extract_single_track_fullrt_length(mass_tracks, mz_tolerance=0.001, isotope_patterns=['13C', 'Na_H'])
```

## Evaluation signals

- Anchor track count per sample is >= 1 and consistent with expected compound complexity (typically 5–50 for metabolomics samples).
- Reference sample is correctly identified as the one with the maximum anchor track count, or matches user specification.
- All detected isotope/adduct m/z differences fall within expected ranges: 13C-12C ≈ 1.00335 ± tolerance, Na-H ≈ 21.98194 ± tolerance.
- m/z recalibration (if applied) reduces systematic drift below 1 ppm threshold across the sample cohort.
- Anchor tracks show high SNR and Gaussian-like peak shape (audit_mass_track metrics pass), indicating reliable signal.

## Limitations

- Requires high mass resolution (≥ 0.001 amu precision) to reliably distinguish isotope and adduct shifts; lower-resolution instruments may produce spurious or missed anchors.
- Assumes sufficient adduct/isotope diversity in the sample; samples with few compounds or minimal isotope enrichment may yield fewer or no anchors, weakening cross-sample calibration.
- m/z recalibration is triggered only if drift exceeds 1 ppm; systematic offsets < 1 ppm are not corrected and may accumulate in larger cohorts.
- Anchor identification is deterministic and depends on predefined m/z patterns; novel adducts or post-translational modifications not in the pattern library will be missed.
- Reference sample selection by anchor count alone may not be optimal if a sample has high anchor count but poor chromatographic separation or high background noise.

## Evidence

- [other] Identify anchor mass tracks by detecting m/z differences matching 13C/12C isotopes or Na/H adducts within each sample: "Identify anchor mass tracks by detecting m/z differences matching 13C/12C isotopes or Na/H adducts within each sample (chromatograms.extract_single_track_fullrt_length)."
- [other] Bin m/z values at 0.001 amu resolution, applying nearest-neighbor clustering by m/z seeds to resolve overlapping m/z values: "Extract mass tracks from each sample using pymzml and bin m/z values at 0.001 amu resolution, merging adjacent bins within tolerance and applying nearest-neighbor clustering by m/z seeds to resolve"
- [other] Select reference sample as the one with highest number of anchor mass tracks unless user-specified: "Select the reference sample as the one with the highest number of anchor mass tracks unless user-specified (ext_Experiment.get_reference_sample_id)."
- [other] Recalibrate all m/z values if systematic drift exceeds 1 ppm: "recalibrating all m/z values if systematic drift exceeds 1 ppm, then aligning remaining mass tracks (MassGrid.build_grid_sample_wise, MassGrid.add_sample)."
- [intro] High mass resolution leveraged to prioritize mass separation and alignment: "Taking advantage of high mass resolution to prioritize mass separation and alignment"
- [intro] Reproducible tracking and backtracking between features and mass tracks (EICs): "Reproducible, track and backtrack between features and mass tracks (EICs)"
