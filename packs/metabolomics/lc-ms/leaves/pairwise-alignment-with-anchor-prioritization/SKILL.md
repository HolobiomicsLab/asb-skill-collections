---
name: pairwise-alignment-with-anchor-prioritization
description: Use when when processing LC-MS metabolomics datasets with 10 or fewer
  samples and requiring reproducible mass track alignment across the cohort.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3644
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0769
  tools:
  - Python
  - asari MassGrid class (build_grid_sample_wise, add_sample)
  - asari mass_functions module (anchor track identification)
  - scipy.signal.find_peaks
  - Python (3.8+)
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1038/s41467-023-39889-1
  title: asari
evidence_spans:
- Trackable and scalable Python program for high-resolution LC-MS metabolomics data
  preprocessing
- Trackable and scalable Python program for high-resolution metabolomics data processing.
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

# pairwise-alignment-with-anchor-prioritization

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

A mass track alignment strategy for small LC-MS metabolomics studies (≤10 samples) that prioritizes alignment of anchor mass tracks (isotopes and adducts) before aligning remaining tracks, with optional m/z recalibration if systematic differences exceed 1 ppm. This approach exploits high-confidence anchor features to establish a robust reference frame before handling ambiguous mass tracks.

## When to use

When processing LC-MS metabolomics datasets with 10 or fewer samples and requiring reproducible mass track alignment across the cohort. Use this strategy when memory and CPU resources are not severely constrained and when anchor mass tracks (13C/12C isotopes or Na/H adducts) can be reliably identified in the reference sample to guide the alignment of all remaining mass tracks.

## When NOT to use

- Study contains >10 samples: use nearest-neighbor clustering (nn_cluster_by_mz_seeds) instead for computational efficiency.
- Samples lack detectable anchor mass tracks: pairwise anchor-based alignment will fail; fall back to histogram-based seed detection or centroiding.
- Input is already a feature table or consensus mass list: skip mass track alignment entirely; proceed directly to feature detection.

## Inputs

- sample mass tracks per sample (list of m/z and intensity values)
- anchor mass track definitions (m/z differences for 13C/12C isotopes and Na/H adducts)
- reference sample identifier or auto-selected sample with maximum anchor tracks
- m/z tolerance threshold (default or user-specified in ppm)

## Outputs

- aligned MassGrid with consensus m/z values and sample membership
- _mass_grid_mapping.csv file documenting aligned mass track identifiers, consensus m/z, and sample presence
- recalibration offsets applied to each sample (if systematic drift detected)

## How to apply

First, identify the reference sample by selecting the one with the highest number of anchor mass tracks (isotopic or adduct pairs), or accept a user-specified reference. Extract anchor mass tracks from the reference sample based on predefined isotope and adduct mass differences. For each other sample, align its anchor mass tracks to the reference list first, computing m/z differences for each pair. If the systematic m/z difference (calculated as median across anchor pairs) exceeds 1 ppm, apply a global recalibration to all m/z values in that sample. After anchor tracks are aligned and recalibrated, proceed to align the remaining non-anchor mass tracks using the recalibrated m/z values, creating a unified MassGrid. This two-stage approach leverages high-confidence features to correct for instrumental drift before aligning lower-confidence tracks.

## Related tools

- **asari MassGrid class (build_grid_sample_wise, add_sample)** (Constructs and manages the aligned MassGrid for pairwise sample-wise alignment) — https://github.com/shuzhao-li/asari
- **asari mass_functions module (anchor track identification)** (Identifies 13C/12C isotope and Na/H adduct mass tracks for anchor-based alignment) — https://github.com/shuzhao-li/asari
- **scipy.signal.find_peaks** (Detects local maxima in chromatographic traces to identify mass tracks)
- **Python (3.8+)** (Primary runtime environment for alignment computations)

## Examples

```
from asari.mass_functions import identify_anchor_tracks; from asari import MassGrid; ref_sample = samples_by_anchor_count[0]; massgrid = MassGrid(); massgrid.build_grid_sample_wise(samples, ref_sample, mz_tolerance=5)
```

## Evaluation signals

- All anchor mass tracks from the reference sample are present in the aligned MassGrid with consensus m/z within expected tolerance (±1 ppm of reference).
- Recalibration offsets computed for each sample are consistent in direction and magnitude with known instrumental drift patterns (systematic vs. random).
- Non-anchor mass tracks cluster correctly around consensus m/z values derived from sample-wise anchor alignment; no spurious mass track fragmentation across different consensus bins.
- The _mass_grid_mapping.csv output contains complete mapping of original sample mass track identifiers to consensus m/z and shows expected sample membership patterns (all samples present for true compounds, subset for rare features).
- Cross-sample mass track correspondence is reproducible when the same reference sample is used; switching reference samples yields only minor shifts in consensus m/z (within calibration tolerance).

## Limitations

- Requires at least one sample with reliably detectable anchor mass tracks; studies lacking isotopic or adduct signals will experience anchor detection failure.
- Pairwise approach scales linearly with sample count; for >10 samples, computational cost becomes prohibitive relative to nearest-neighbor clustering alternatives.
- 1 ppm recalibration threshold is fixed in the article; studies with systematically larger instrumental drift (e.g., older instruments or extreme pH conditions) may require empirical adjustment.
- Alignment quality depends critically on anchor track signal-to-noise ratio; low-abundance isotopologues or adducts may be missed, degrading the reference frame.

## Evidence

- [methods] if ≤10 samples, use pairwise alignment with anchor mass track prioritization: "if ≤10 samples, use pairwise alignment with anchor mass track prioritization; else use nearest-neighbor clustering method"
- [methods] Identify reference sample as the one with highest number of anchor mass tracks: "Identify reference sample as the one with highest number of anchor mass tracks (13C/12C isotopes or Na/H adducts) unless user-specified."
- [methods] perform pairwise sample-wise alignment: align anchor mass tracks first: "For small studies, perform pairwise sample-wise alignment: align anchor mass tracks first between each sample and reference list, recalibrate all sample m/z values if systematic difference exceeds 1"
- [methods] Establish anchor mass tracks by finding m/z differences: "Establish anchor mass tracks by finding m/z differences that match to either 13C/12C isotopes or Na/H adducts."
- [other] Asari is designed as a scalable program that uses performance-conscious approaches: "Asari is designed as a scalable program that uses performance-conscious approaches, operating with disciplined memory and CPU use, enabling it to handle studies of varying sizes through conditional"
- [methods] Generate _mass_grid_mapping.csv documenting aligned mass track identifiers: "Generate _mass_grid_mapping.csv documenting aligned mass track identifiers, consensus m/z values, and sample membership across the MassGrid."
