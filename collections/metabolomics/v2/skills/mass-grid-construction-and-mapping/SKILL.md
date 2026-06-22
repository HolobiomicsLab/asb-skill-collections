---
name: mass-grid-construction-and-mapping
description: 'Use when after mass track extraction from individual LC-MS samples, when you need to align mass tracks across a cohort to produce a unified feature matrix. Specifically: when study size is ≤10 samples, use pairwise anchor-prioritized alignment;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3644
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - asari mass_functions module (nn_cluster_by_mz_seeds)
  - asari MassGrid class (build_grid_sample_wise, add_sample, build_grid_by_centroiding, bin_track_mzs)
  - asari.mass_functions.nn_cluster_by_mz_seeds
  - asari.MassGrid (build_grid_sample_wise, add_sample, build_grid_by_centroiding, bin_track_mzs)
  - asari.chromatograms.get_thousandth_bins
  - scipy.signal.detrend
derived_from:
- doi: 10.1038/s41467-023-39889-1
  title: asari
evidence_spans:
- Trackable and scalable Python program for high-resolution LC-MS metabolomics data preprocessing
- Trackable and scalable Python program for high-resolution metabolomics data processing.
- a nearest neighbor (NN) clustering is performed to establish the number of mass tracks. See [mass_functions.nn_cluster_by_mz_seeds](mass_functions.nn_cluster_by_mz_seeds).
- See [MassGrid.build_grid_sample_wise](MassGrid.build_grid_sample_wise), [MassGrid.add_sample](MassGrid.add_sample). See [MassGrid.build_grid_by_centroiding](MassGrid.build_grid_by_centroiding),
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_asari
    doi: 10.1038/s41467-023-39889-1
    title: asari
  dedup_kept_from: coll_asari
schema_version: 0.2.0
---

# mass-grid-construction-and-mapping

## Summary

Construct a unified mass-to-sample alignment map (MassGrid) by conditionally selecting between pairwise or clustering-based alignment strategies based on study size, establishing consensus m/z values across samples while tracking sample membership and mass track identifiers.

## When to use

After mass track extraction from individual LC-MS samples, when you need to align mass tracks across a cohort to produce a unified feature matrix. Specifically: when study size is ≤10 samples, use pairwise anchor-prioritized alignment; when >10 samples, switch to nearest-neighbor clustering to manage computational cost and memory use.

## When NOT to use

- Input is already a feature table or already-aligned consensus m/z list — skip to downstream statistical or annotation steps.
- Mass tracks have not been extracted and anchor masses have not been identified — first run mass track construction and anchor detection.
- Study contains samples with vastly different ionization efficiency or instrument calibration drift not correctable within 1 ppm — consider external calibration or sample-specific reference standards before MassGrid construction.

## Inputs

- mass_track_objects_per_sample (list of ExtractedMassTrack with m/z, intensity, RT, sample_id)
- anchor_mass_track_registry (identified 13C/12C isotopes and Na/H adducts per sample)
- mz_tolerance_ppm (default ~5 ppm for high-resolution LC-MS)
- sample_count (integer, determines algorithm selection)

## Outputs

- MassGrid_object (alignment structure with consensus m/z per bin, sample membership, mass track IDs)
- _mass_grid_mapping.csv (tabular export: aligned_mass_track_id, consensus_mz, samples_present)
- recalibrated_sample_mz_values (if systematic m/z drift >1 ppm detected and corrected)

## How to apply

First, determine study size (total sample count) to select alignment strategy: if ≤10 samples, identify the reference sample with the highest count of anchor mass tracks (13C/12C isotopes or Na/H adducts), then perform pairwise sample-wise alignment by aligning anchor mass tracks first between each sample and reference, recalibrating all m/z values if systematic difference exceeds 1 ppm tolerance, then aligning remaining mass tracks. For studies >10 samples, bin all mass tracks by m/z using nearest-neighbor clustering seeded by histogram-based m/z detection, requiring 2 peaks separated by at least mz_tolerance. For both strategies, construct consensus m/z for each aligned bin as the mean of the median m/z and m/z at highest intensity. Output a _mass_grid_mapping.csv documenting aligned mass track identifiers, consensus m/z values, and sample membership across the MassGrid.

## Related tools

- **asari.mass_functions.nn_cluster_by_mz_seeds** (Performs nearest-neighbor clustering of mass tracks by m/z for large studies (>10 samples)) — https://github.com/shuzhao-li/asari
- **asari.MassGrid (build_grid_sample_wise, add_sample, build_grid_by_centroiding, bin_track_mzs)** (Core class implementing MassGrid construction logic, consensus m/z calculation, and sample membership tracking) — https://github.com/shuzhao-li/asari
- **asari.chromatograms.get_thousandth_bins** (Creates initial m/z bins from extracted MS1 spectra for mass track binning) — https://github.com/shuzhao-li/asari
- **scipy.signal.detrend** (Optional preprocessing of mass track intensity profiles before consensus m/z calculation)

## Examples

```
from asari.mass_functions import nn_cluster_by_mz_seeds; from asari.MassGrid import MassGrid; grid = MassGrid(); grid.build_grid_sample_wise(samples, reference_idx) if len(samples) <= 10 else grid.build_grid_by_centroiding(samples, mz_tolerance=5e-6)
```

## Evaluation signals

- Verify _mass_grid_mapping.csv contains one row per aligned mass bin with non-null consensus_mz (numeric) and comma-separated sample_id list.
- Check that consensus m/z values fall within mz_tolerance of the input mass track m/z values (e.g., <5 ppm deviation for high-resolution data).
- Confirm that pairwise alignment strategy was used for ≤10 samples and nearest-neighbor clustering for >10 samples (verify algorithm selection in project.json or logs).
- For pairwise alignments, validate that anchor mass track recalibration was applied if m/z drift exceeded 1 ppm (check for recalibration delta in output or logs).
- Ensure no mass tracks are lost or duplicated: sum of unique mass_track_ids in mapping should equal original count per sample; each bin membership is mutually exclusive.

## Limitations

- Pairwise strategy scales poorly for >10 samples; CPU and memory use grows quadratically with sample count — use nearest-neighbor clustering for larger cohorts.
- Anchor mass track identification (13C/12C, Na/H adducts) depends on prior detection of isotope patterns and adduct masses — sparse or missing isotope signals may degrade reference sample selection.
- Consensus m/z calculation (mean of median m/z and intensity-weighted m/z) assumes relatively symmetric m/z distributions within bins; extreme outliers or multimodal distributions may skew consensus.
- The 1 ppm systematic m/z drift threshold is tuned for high-resolution LC-MS (e.g., Orbitrap); lower-resolution instruments or uncalibrated data may require recalibration even below 1 ppm or may exceed tolerance.
- No explicit handling of samples with dramatically different dynamic range or signal saturation — alignment may be distorted if one sample dominates intensity in a bin.

## Evidence

- [other] Determine study size (sample count) to select alignment strategy: if ≤10 samples, use pairwise alignment with anchor mass track prioritization; else use nearest-neighbor clustering method.: "if ≤10 samples, use pairwise alignment with anchor mass track prioritization; else use nearest-neighbor clustering method"
- [other] For small studies, perform pairwise sample-wise alignment: align anchor mass tracks first between each sample and reference list, recalibrate all sample m/z values if systematic difference exceeds 1 ppm, then align remaining mass tracks.: "align anchor mass tracks first between each sample and reference list, recalibrate all sample m/z values if systematic difference exceeds 1 ppm, then align remaining mass tracks"
- [other] For large studies, bin all sample mass tracks by m/z using nearest-neighbor clustering with histogram-based m/z seed detection, ensuring 2 peaks separated by at least mz_tolerance.: "bin all sample mass tracks by m/z using nearest-neighbor clustering with histogram-based m/z seed detection, ensuring 2 peaks separated by at least mz_tolerance"
- [other] Construct consensus m/z for each aligned bin as mean of median m/z and m/z at highest intensity.: "Construct consensus m/z for each aligned bin as mean of median m/z and m/z at highest intensity"
- [intro] Taking advantage of high mass resolution to prioritize mass separation and alignment: "Taking advantage of high mass resolution to prioritize mass separation and alignment"
- [other] Asari is designed as a scalable program that uses performance-conscious approaches, operating with disciplined memory and CPU use, enabling it to handle studies of varying sizes through conditional algorithm selection.: "scalable program that uses performance-conscious approaches, operating with disciplined memory and CPU use, enabling it to handle studies of varying sizes through conditional algorithm selection"
