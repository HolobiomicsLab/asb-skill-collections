---
name: nearest-neighbor-clustering-for-mass-spectrometry
description: Use when you have extracted mass tracks (EICs) from individual samples
  at 0.001 amu m/z resolution and need to align them into a composite mass grid for
  feature detection.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - pymzml
  - mass_functions.nn_cluster_by_mz_seeds
  - MassGrid.bin_track_mzs
  - MassGrid.build_grid_by_centroiding
  - MassGrid.build_grid_sample_wise
  - chromatograms.extract_single_track_fullrt_length
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
- The default method uses `pymzml` to parse mzML files.
- nearest neighbor (NN) clustering is performed to establish the number of mass tracks.
  The NN clustering assigns each data point to its nearest 'peak mz value'.
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

# nearest-neighbor-clustering-for-mass-spectrometry

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Cluster and bin m/z values from mass tracks across multiple LC-MS samples using nearest-neighbor methods to resolve overlapping chromatograms and construct a unified mass grid. This skill leverages high mass resolution to group chemically equivalent ions and align them reproducibly across the cohort.

## When to use

Apply this skill when you have extracted mass tracks (EICs) from individual samples at 0.001 amu m/z resolution and need to align them into a composite mass grid for feature detection. Specifically, use it when: (1) you have overlapping m/z values from different samples that represent the same chemical species, (2) you need to resolve degeneracy caused by adjacent bins or mass measurement drift, or (3) you are processing studies with >10 samples where pairwise alignment becomes computationally expensive.

## When NOT to use

- Input is already a feature table or composite peak list (clustering is applied at the mass track stage, before feature detection)
- Mass resolution is <0.1 amu or m/z measurement error is >5 ppm; nearest-neighbor clustering depends on sub-ppm precision
- Single sample or no cross-sample overlap; clustering is most valuable when cohort-level alignment is needed

## Inputs

- mass tracks (EICs) extracted from individual mzML samples
- m/z values binned at 0.001 amu resolution per sample
- isotope or adduct difference patterns (e.g., 13C/12C, Na/H) for anchor detection
- sample count and reference sample designation

## Outputs

- MassGrid structure: a table with one row per unique mass track, columns listing sample indices and their m/z values
- centroided m/z values for each mass track cluster
- anchor track annotations with alignment priority flags
- m/z recalibration parameters if drift >1 ppm detected

## How to apply

First, bin all m/z values from mass tracks across samples at 0.001 amu resolution, merging adjacent bins within tolerance. Apply nearest-neighbor clustering by m/z seeds (using `mass_functions.nn_cluster_by_mz_seeds`) to group overlapping m/z values into clusters. For small studies (≤10 samples), perform pairwise alignment on anchor mass tracks first and recalibrate if systematic drift exceeds 1 ppm, then align remaining tracks. For larger studies, centroid m/z values within each cluster and construct the MassGrid by binning all tracks across samples (using `MassGrid.bin_track_mzs` and `MassGrid.build_grid_by_centroiding`). The output is a MassGrid where each row represents a unique mass track identifier and contains sample indices mapped to their corresponding m/z values, with anchor tracks marked for higher priority.

## Related tools

- **mass_functions.nn_cluster_by_mz_seeds** (Performs nearest-neighbor clustering on m/z values using seed-based assignment to resolve overlapping mass tracks) — https://github.com/shuzhao-li/asari
- **MassGrid.bin_track_mzs** (Bins m/z values from all mass tracks across samples into discrete m/z bins for grouping) — https://github.com/shuzhao-li/asari
- **MassGrid.build_grid_by_centroiding** (Constructs MassGrid by centroiding m/z values within bins for large studies (>10 samples)) — https://github.com/shuzhao-li/asari
- **MassGrid.build_grid_sample_wise** (Performs pairwise sample-by-sample alignment for small studies (≤10 samples) with recalibration) — https://github.com/shuzhao-li/asari
- **chromatograms.extract_single_track_fullrt_length** (Identifies anchor mass tracks (isotopes, adducts) within each sample for priority alignment) — https://github.com/shuzhao-li/asari
- **pymzml** (Parses mzML files to extract raw m/z and intensity data for mass track construction) — https://github.com/shuzhao-li/asari

## Examples

```
from asari.mass_functions import nn_cluster_by_mz_seeds; from asari.chromatograms import get_thousandth_bins; mz_bins = get_thousandth_bins(mass_tracks); clusters = nn_cluster_by_mz_seeds(mz_bins, tolerance=0.001)
```

## Evaluation signals

- MassGrid contains exactly one row per unique mass track identifier with no duplicates
- Each MassGrid row lists all sample indices with measured m/z values and no missing values for samples where the track was detected
- Centroided m/z values per cluster are within ±0.001 amu of the input bin resolution
- Anchor mass tracks are marked with elevated priority flags and appear first in alignment order
- For samples with systematic m/z drift >1 ppm, recalibration parameters are applied and post-correction pairwise m/z differences are <0.5 ppm
- Mass tracks representing the same chemical species across samples cluster together; verify by comparing expected isotope offsets (1.003 amu for 13C/12C) to actual m/z differences in aligned rows

## Limitations

- Clustering precision depends on high mass resolution (sub-ppm accuracy); data with >1 ppm uncalibrated drift may produce spurious clusters or misalignments
- Nearest-neighbor methods are sensitive to seed selection and bin width; suboptimal choices of 0.001 amu binning may either over-merge genuine distinct masses or fail to consolidate isotopologue series
- For studies with very large numbers of samples (>>100), centroiding-based clustering may smooth out real biological variation in m/z if samples exhibit systematic within-cohort calibration differences
- Anchor track detection (isotope/adduct patterns) requires presence of abundant ions; low-abundance or singleton mass tracks may not be detected as anchors and could be misaligned

## Evidence

- [other] bin m/z values at 0.001 amu resolution, merging adjacent bins within tolerance and applying nearest-neighbor clustering by m/z seeds: "Extract mass tracks from each sample using pymzml and bin m/z values at 0.001 amu resolution, merging adjacent bins within tolerance and applying nearest-neighbor clustering by m/z seeds to resolve"
- [other] For small studies (≤10 samples), perform pairwise alignment by comparing anchor mass tracks first, recalibrating if drift exceeds 1 ppm, then aligning remaining mass tracks: "For small studies (≤10 samples), perform pairwise alignment by comparing anchor mass tracks first, recalibrating all m/z values if systematic drift exceeds 1 ppm, then aligning remaining mass tracks"
- [other] For larger studies, apply nearest-neighbor clustering on all mass tracks across samples to bin and centroid m/z values into a unified MassGrid: "For larger studies, apply nearest-neighbor clustering on all mass tracks across samples to bin and centroid m/z values into a unified MassGrid"
- [other] MassGrid contains one m/z row per unique mass track identifier, each row lists sample indices and their corresponding m/z values, and anchor tracks are marked with higher priority: "MassGrid contains one m/z row per unique mass track identifier, each row lists sample indices and their corresponding m/z values, and anchor tracks are marked with higher priority in the alignment"
- [other] Asari aligns mass tracks across samples by constructing a MassGrid, leveraging high mass resolution to prioritize mass separation and alignment, enabling reproducible tracking: "Asari aligns mass tracks across samples by constructing a MassGrid, a process that leverages high mass resolution to prioritize mass separation and alignment, enabling reproducible tracking and"
