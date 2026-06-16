---
name: m-z-alignment-across-samples
description: Use when after mass track construction for individual samples, when you need to establish consensus m/z values across a cohort of LC-MS samples to build a unified feature table.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3645
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - asari mass_functions module (nn_cluster_by_mz_seeds)
  - asari MassGrid class (build_grid_sample_wise, add_sample, build_grid_by_centroiding, bin_track_mzs)
derived_from:
- doi: 10.1038/s41467-023-39889-1
  title: asari
evidence_spans:
- Trackable and scalable Python program for high-resolution LC-MS metabolomics data preprocessing
- Trackable and scalable Python program for high-resolution metabolomics data processing.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_asari
    doi: 10.1038/s41467-023-39889-1
    title: asari
  dedup_kept_from: coll_asari
schema_version: 0.2.0
---

# m/z-alignment-across-samples

## Summary

Conditional alignment of mass tracks (extracted ion chromatograms) across LC-MS samples using either pairwise anchor-based or nearest-neighbor clustering strategies, selected by study size to balance statistical power with computational efficiency. Produces a MassGrid mapping that links aligned m/z values and sample membership.

## When to use

After mass track construction for individual samples, when you need to establish consensus m/z values across a cohort of LC-MS samples to build a unified feature table. Apply this skill when sample count is known and you have extracted mass tracks with identified anchor mass tracks (13C/12C isotopes or Na/H adducts) for each sample.

## When NOT to use

- Input is already a feature table or consensus m/z list (alignment already performed).
- Mass tracks have not yet been extracted or anchor mass tracks have not been identified.
- Study contains only a single sample (no cross-sample alignment needed).

## Inputs

- Mass track list per sample (m/z, retention time, intensity values)
- Identified anchor mass tracks (13C/12C isotopes or Na/H adducts) per sample
- Sample count / study size metadata
- User-specified reference sample (optional)

## Outputs

- MassGrid: aligned m/z consensus values with sample membership
- _mass_grid_mapping.csv: table of aligned mass track IDs, consensus m/z, and sample membership
- Recalibrated sample m/z values (if pairwise strategy)

## How to apply

First, determine study size (sample count) to select alignment strategy: if ≤10 samples, use pairwise alignment with anchor mass track prioritization; otherwise use nearest-neighbor clustering. Identify the reference sample as the one with the highest number of anchor mass tracks, unless user-specified. For small studies, perform sample-wise pairwise alignment: align anchor mass tracks between each sample and reference list first, then recalibrate all sample m/z values if systematic difference exceeds 1 ppm, then align remaining mass tracks. For large studies, bin all sample mass tracks by m/z using nearest-neighbor clustering with histogram-based m/z seed detection, ensuring 2 peaks separated by at least mz_tolerance. Construct consensus m/z for each aligned bin as the mean of the median m/z and m/z at highest intensity. Generate _mass_grid_mapping.csv documenting aligned mass track identifiers, consensus m/z values, and sample membership.

## Related tools

- **asari mass_functions module (nn_cluster_by_mz_seeds)** (Performs nearest-neighbor clustering of mass tracks by m/z seeds for large studies (>10 samples)) — https://github.com/shuzhao-li/asari
- **asari MassGrid class (build_grid_sample_wise, add_sample, build_grid_by_centroiding, bin_track_mzs)** (Core classes for constructing and managing aligned mass track grid across samples) — https://github.com/shuzhao-li/asari
- **Python** (Implementation language for alignment algorithms)

## Examples

```
From Python: `from asari.mass_functions import nn_cluster_by_mz_seeds; from asari.workflow import MassGrid; grid = MassGrid(); grid.build_grid_sample_wise(samples, sample_count=5, mz_tolerance=5) if sample_count <= 10 else grid.build_grid_by_centroiding(samples, mz_tolerance=5)`
```

## Evaluation signals

- MassGrid contains no missing consensus m/z values for bins with ≥1 sample membership.
- _mass_grid_mapping.csv row count matches total unique aligned mass track identifiers.
- Pairwise strategy (≤10 samples): anchor mass tracks aligned first; verify no m/z recalibrations for differences <1 ppm.
- Nearest-neighbor strategy (>10 samples): verify histogram-based seed m/z separated by ≥mz_tolerance; consensus m/z is within expected range of input sample m/z values.
- Sample membership is complete: all original samples appear in at least one grid row.

## Limitations

- Small study threshold (≤10 samples) is fixed; studies near boundary may benefit from sensitivity analysis on strategy choice.
- Anchor mass track identification depends on presence of 13C/12C isotopes or Na/H adducts; samples without detectable anchors may have degraded alignment.
- Nearest-neighbor clustering sensitivity to mz_tolerance parameter; inappropriate tolerance values can merge distinct m/z or fragment bins.
- Systematic m/z differences >1 ppm in pairwise strategy trigger recalibration but may indicate instrument drift or data quality issues unaddressed by this step alone.

## Evidence

- [other] if ≤10 samples, use pairwise alignment with anchor mass track prioritization; else use nearest-neighbor clustering method: "if ≤10 samples, use pairwise alignment with anchor mass track prioritization; else use nearest-neighbor clustering method"
- [other] Identify reference sample as the one with highest number of anchor mass tracks (13C/12C isotopes or Na/H adducts) unless user-specified: "Identify reference sample as the one with highest number of anchor mass tracks (13C/12C isotopes or Na/H adducts) unless user-specified"
- [other] For small studies, perform pairwise sample-wise alignment: align anchor mass tracks first between each sample and reference list, recalibrate all sample m/z values if systematic difference exceeds 1 ppm, then align remaining mass tracks: "For small studies, perform pairwise sample-wise alignment: align anchor mass tracks first between each sample and reference list, recalibrate all sample m/z values if systematic difference exceeds 1"
- [other] For large studies, bin all sample mass tracks by m/z using nearest-neighbor clustering with histogram-based m/z seed detection, ensuring 2 peaks separated by at least mz_tolerance: "For large studies, bin all sample mass tracks by m/z using nearest-neighbor clustering with histogram-based m/z seed detection, ensuring 2 peaks separated by at least mz_tolerance"
- [other] Construct consensus m/z for each aligned bin as mean of median m/z and m/z at highest intensity: "Construct consensus m/z for each aligned bin as mean of median m/z and m/z at highest intensity"
- [other] Asari is designed as a scalable program that uses performance-conscious approaches, operating with disciplined memory and CPU use, enabling it to handle studies of varying sizes through conditional algorithm selection: "Asari is designed as a scalable program that uses performance-conscious approaches, operating with disciplined memory and CPU use, enabling it to handle studies of varying sizes through conditional"
- [readme] Taking advantage of high mass resolution to prioritize mass separation and alignment: "Taking advantage of high mass resolution to prioritize mass separation and alignment"
- [methods] Aignment of mass tracks across samples, resulting in the MassGrid: "Aignment of mass tracks across samples, resulting in the MassGrid"
