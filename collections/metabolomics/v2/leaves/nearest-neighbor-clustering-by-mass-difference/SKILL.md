---
name: nearest-neighbor-clustering-by-mass-difference
description: Use when processing LC-MS metabolomics studies with >10 samples where
  sample count and memory constraints make pairwise mass alignment infeasible.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3198
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - asari mass_functions module (nn_cluster_by_mz_seeds)
  - asari mass_functions.nn_cluster_by_mz_seeds
  - asari MassGrid.build_grid_by_centroiding
  - asari chromatograms.get_thousandth_bins
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
- a nearest neighbor (NN) clustering is performed to establish the number of mass
  tracks. See [mass_functions.nn_cluster_by_mz_seeds](mass_functions.nn_cluster_by_mz_seeds).
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

# nearest-neighbor-clustering-by-mass-difference

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Groups mass tracks across LC-MS samples by clustering m/z values using nearest-neighbor methods seeded by histogram-based m/z detection, enabling scalable mass alignment for large studies (>10 samples) without pairwise computation. This approach trades exhaustive pairwise alignment for memory- and CPU-efficient binning that preserves high-resolution mass separation.

## When to use

Apply this skill when processing LC-MS metabolomics studies with >10 samples where sample count and memory constraints make pairwise mass alignment infeasible. Specifically, use it during the MassGrid construction phase after mass track extraction from individual samples, when you need to align heterogeneous m/z values across the cohort into consensus bins while maintaining mass resolution (typically <5 ppm tolerance).

## When NOT to use

- Input study has ≤10 samples — use pairwise anchor-mass-track alignment instead for higher sensitivity to systematic drift.
- Mass tracks are already binned or consensus m/z values already exist — this skill is for initial alignment, not refinement.
- Input does not include mass track intensity or m/z distribution information — clustering seeding requires histogram maxima detection.

## Inputs

- mass_tracks_per_sample (list of lists of {m/z, retention_time, intensity} tuples, one list per sample)
- mz_tolerance (float, typically 0.001 in m/z units or expressed in ppm)
- study_sample_count (integer)

## Outputs

- aligned_mass_bins (list of {consensus_m/z, [sample_track_ids], [sample_m/z_values]})
- _mass_grid_mapping.csv (tab- or comma-separated file documenting aligned mass track identifiers, consensus m/z, and sample membership)

## How to apply

After extracting mass tracks from all samples, bin all sample mass tracks by m/z using nearest-neighbor clustering seeded by histogram-based detection of local m/z maxima. For each m/z bin, require that 2 peaks be separated by at least mz_tolerance (typically 0.001 in m/z units or ~5 ppm at m/z 500) to prevent spurious merging. Construct a consensus m/z for each aligned bin as the mean of the median m/z and the m/z at highest intensity across all samples contributing to that bin. Document the aligned mass track identifiers, consensus m/z values, and sample membership in an output mapping file. This approach is chosen over pairwise alignment for studies >10 samples because it avoids O(n²) comparisons and reduces peak memory usage while still leveraging the high mass resolution of modern instruments to separate true mass differences from noise.

## Related tools

- **asari mass_functions.nn_cluster_by_mz_seeds** (Core implementation of nearest-neighbor m/z clustering with histogram-based seeding) — https://github.com/shuzhao-li/asari
- **asari MassGrid.build_grid_by_centroiding** (Constructs consensus m/z bins from clustered mass tracks and computes consensus m/z as mean of median m/z and intensity-weighted m/z) — https://github.com/shuzhao-li/asari
- **asari chromatograms.get_thousandth_bins** (Pre-bins mass tracks into m/z ranges (0.001 m/z width) for efficient histogram construction and seed detection) — https://github.com/shuzhao-li/asari

## Examples

```
from asari.mass_functions import nn_cluster_by_mz_seeds
from asari.MassGrid import MassGrid
mg = MassGrid()
mg.build_grid_by_centroiding(all_mass_tracks, mz_tolerance=0.001)
```

## Evaluation signals

- Consensus m/z values in output bins fall within mz_tolerance of all constituent sample m/z values (validate no spurious merging across tolerance boundaries).
- _mass_grid_mapping.csv is non-empty, with each row containing a unique consensus m/z, at least one sample track ID, and reproducible across re-runs on the same input.
- Number of aligned bins is consistent with the expected m/z distribution width (e.g., for a 50–1200 m/z range with 0.001 m/z bins, expect ~1.15M theoretical bins, fewer in practice due to gaps).
- Peak intensity distribution in aligned bins (e.g., median SNR per bin) is preserved relative to input; no systematic loss of weak peaks relative to strong peaks.
- Sample membership across bins shows expected sparsity: for a moderately sized cohort (N=50–100), most bins contain tracks from only a subset of samples.

## Limitations

- Method assumes that m/z drift across samples is minimal (<2× mz_tolerance per sample); if systematic drift >1 ppm exists, pre-calibration via pairwise anchor masses may be required.
- Histogram-based seeding depends on local maxima detection (scipy.signal.find_peaks prominence); if sample m/z distributions are very noisy or sparse, seed detection may miss true metabolite clusters.
- Consensus m/z computed as mean of median and intensity-weighted m/z is a heuristic; in regions with extreme intensity imbalance across samples, it may skew toward dominant samples.
- No built-in quality filtering; weak or artifact mass tracks (SNR <3 or unusual isotope patterns) are clustered identically to high-confidence tracks; filtering should precede clustering or follow post-hoc in downstream QC.
- For very large cohorts (N>1000), histogram resolution may need tuning; default 0.001 m/z bin width can become memory-constrained.

## Evidence

- [other] if ≤10 samples, use pairwise alignment with anchor mass track prioritization; else use nearest-neighbor clustering method: "if ≤10 samples, use pairwise alignment with anchor mass track prioritization; else use nearest-neighbor clustering method."
- [other] For large studies, bin all sample mass tracks by m/z using nearest-neighbor clustering with histogram-based m/z seed detection, ensuring 2 peaks separated by at least mz_tolerance.: "For large studies, bin all sample mass tracks by m/z using nearest-neighbor clustering with histogram-based m/z seed detection, ensuring 2 peaks separated by at least mz_tolerance."
- [other] Construct consensus m/z for each aligned bin as mean of median m/z and m/z at highest intensity.: "Construct consensus m/z for each aligned bin as mean of median m/z and m/z at highest intensity."
- [other] Generate _mass_grid_mapping.csv documenting aligned mass track identifiers, consensus m/z values, and sample membership across the MassGrid.: "Generate _mass_grid_mapping.csv documenting aligned mass track identifiers, consensus m/z values, and sample membership across the MassGrid."
- [other] Asari is designed as a scalable program that uses performance-conscious approaches, operating with disciplined memory and CPU use, enabling it to handle studies of varying sizes through conditional algorithm selection.: "Asari is designed as a scalable program that uses performance-conscious approaches, operating with disciplined memory and CPU use, enabling it to handle studies of varying sizes through conditional"
- [methods] See [mass_functions.nn_cluster_by_mz_seeds](mass_functions.nn_cluster_by_mz_seeds).: "See [mass_functions.nn_cluster_by_mz_seeds](mass_functions.nn_cluster_by_mz_seeds)."
