---
name: mass-track-consensus-computation
description: Use when after mass tracks have been aligned across all samples (either
  via pairwise alignment for ≤10 samples or nearest-neighbor clustering for larger
  cohorts), and you need to generate a single representative m/z per aligned bin for
  downstream feature extraction and annotation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  tools:
  - Python
  - asari mass_functions module (nn_cluster_by_mz_seeds)
  - asari MassGrid class (build_grid_sample_wise, add_sample, build_grid_by_centroiding,
    bin_track_mzs)
  - asari MassGrid class
  - asari mass_functions module
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
- a nearest neighbor (NN) clustering is performed to establish the number of mass
  tracks. See [mass_functions.nn_cluster_by_mz_seeds](mass_functions.nn_cluster_by_mz_seeds).
- See [MassGrid.build_grid_sample_wise](MassGrid.build_grid_sample_wise), [MassGrid.add_sample](MassGrid.add_sample).
  See [MassGrid.build_grid_by_centroiding](MassGrid.build_grid_by_centroiding),
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

# mass-track-consensus-computation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Compute consensus m/z values for aligned mass tracks across LC-MS samples by combining median and intensity-weighted estimates. This step finalizes MassGrid construction after pairwise or nearest-neighbor alignment, ensuring reproducible mass calibration across study cohorts.

## When to use

After mass tracks have been aligned across all samples (either via pairwise alignment for ≤10 samples or nearest-neighbor clustering for larger cohorts), and you need to generate a single representative m/z per aligned bin for downstream feature extraction and annotation.

## When NOT to use

- Input is already a finalized feature table; consensus m/z computation is part of the alignment phase, not post-alignment QC.
- Mass tracks have not yet been aligned across samples; compute alignment first using build_grid_sample_wise or build_grid_by_centroiding.
- Study contains only a single sample; consensus m/z is meaningful only when aggregating across multiple samples.

## Inputs

- aligned_mass_track_bins (list of grouped mass tracks per consensus m/z bin)
- sample_membership_map (mapping of track IDs to sample origins)
- median_mz_per_bin (pre-computed median m/z for each aligned bin)
- intensity_mz_per_bin (m/z value at highest intensity for each bin)

## Outputs

- consensus_mz_values (single representative m/z per aligned bin)
- mass_grid_mapping.csv (table of aligned track IDs, consensus m/z, sample membership)

## How to apply

For each aligned bin of mass tracks (representing the same analyte m/z across samples), compute the consensus m/z as the mean of two quantities: (1) the median m/z of all tracks in that bin, and (2) the m/z value at the highest intensity within the bin. This dual-estimate approach balances robustness (median) against signal strength (intensity-weighted), reducing bias from outlier tracks or low-intensity measurements. The resulting consensus m/z is recorded alongside the sample membership and original track identifiers in the MassGrid output. This step is performed after systematic m/z recalibration (if pairwise differences exceed 1 ppm), ensuring the consensus is built on already-corrected m/z values.

## Related tools

- **asari MassGrid class** (Provides build_grid_sample_wise and build_grid_by_centroiding methods to construct aligned bins; consensus computation integrates into add_sample and grid finalization) — https://github.com/shuzhao-li/asari
- **asari mass_functions module** (Supplies nn_cluster_by_mz_seeds for large-study clustering and utility functions for bin aggregation prior to consensus calculation) — https://github.com/shuzhao-li/asari
- **Python** (Execution environment; numpy/scipy used for median and intensity indexing operations)

## Examples

```
from asari.mass_functions import build_grid_by_centroiding; mgrid = build_grid_by_centroiding(samples, parameters); mgrid.generate_output(outputdir)
```

## Evaluation signals

- Consensus m/z values fall within 1 ppm of the median m/z in the corresponding bin (validates balance between the two estimates).
- All sample identifiers listed in mass_grid_mapping.csv match the input sample registry; no orphaned or duplicate entries.
- Consensus m/z values are monotonically increasing across bins (no inversions due to sorting or aggregation errors).
- Each aligned bin contains at least one track; isolated bins with single tracks should have consensus m/z equal to that track's (calibrated) m/z.
- mass_grid_mapping.csv has matching row count to the number of aligned bins; output is complete and non-redundant.

## Limitations

- Consensus m/z is sensitive to outlier tracks with very high intensity or misaligned m/z; prior recalibration (if systematic difference > 1 ppm) is critical to avoid skewing the intensity-weighted component.
- For small aligned bins (e.g., present in only 1–2 samples), the consensus may not be stable; consider supplementary confidence intervals or sample-coverage thresholds.
- Method assumes high mass resolution (typically <5 ppm instrument error); low-resolution instruments may produce overlapping bins and artificially merged consensus m/z values.
- Bins generated by nearest-neighbor clustering (large studies) may vary in granularity depending on mz_tolerance and histogram-seed detection; consensus computation does not re-validate bin validity.

## Evidence

- [methods] Construct consensus m/z for each aligned bin as mean of median m/z and m/z at highest intensity: "Construct consensus m/z for each aligned bin as mean of median m/z and m/z at highest intensity."
- [methods] Generate _mass_grid_mapping.csv documenting aligned mass track identifiers, consensus m/z values, and sample membership across the MassGrid: "Generate _mass_grid_mapping.csv documenting aligned mass track identifiers, consensus m/z values, and sample membership across the MassGrid."
- [intro] Taking advantage of high mass resolution to prioritize mass separation and alignment: "Taking advantage of high mass resolution to prioritize mass separation and alignment"
- [methods] recalibrate all sample m/z values if systematic difference exceeds 1 ppm: "recalibrate all sample m/z values if systematic difference exceeds 1 ppm"
