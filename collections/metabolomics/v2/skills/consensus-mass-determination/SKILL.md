---
name: consensus-mass-determination
description: Use when after constructing individual mass tracks from mzTree data bins and before alignment across samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0769
  tools:
  - pymzml
  - Python
  - asari
  - scipy.signal.find_peaks
derived_from:
- doi: 10.1038/s41467-023-39889-1
  title: asari
evidence_spans:
- The default method uses `pymzml` to parse mzML files.
- Trackable and scalable Python program for high-resolution LC-MS metabolomics data preprocessing
- Trackable and scalable Python program for high-resolution metabolomics data processing.
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
---

# consensus-mass-determination

## Summary

Determines a representative m/z value for each mass track by combining the median m/z across the track with the m/z at maximum intensity, weighted by the peak's signal characteristics. This step ensures robust mass assignment that resists outliers while preserving the mass shift information from the most intense part of the elution profile.

## When to use

After constructing individual mass tracks from mzTree data bins and before alignment across samples. Apply this skill when you have extracted a set of (m/z, scan_number, intensity) tuples for a single m/z region and need a single representative mass value that balances accuracy across the full chromatographic range with sensitivity to the most informative (highest-intensity) region of the peak.

## When NOT to use

- Input is already a feature table with assigned consensus m/z values; consensus determination should not be reapplied.
- Mass tracks have fewer than the minimum required scan count for the data bin; filter before consensus calculation.
- m/z range within a bin is already resolved as multiple distinct isotope or adduct species; assign separate mass tracks first, then apply consensus per track.

## Inputs

- mass track (list of (m/z, scan_number, intensity) tuples for a single m/z region)
- intensity vector aligned to full retention time range with zeros for missing scans
- mzTree bin (indexed dictionary of data points keyed by int(mz × 1000))

## Outputs

- consensus_mz (float, representative m/z for the mass track)
- mass track with finalized (consensus_mz, intensity_vector) tuple

## How to apply

For each mass track, calculate consensus_mz as the mean of two components: (1) the median m/z observed across all scans in the track, and (2) the m/z at the scan where intensity is maximum. This dual-component average mitigates the risk that outlier m/z values in low-intensity tails distort the mass assignment, while still leveraging the highest-signal region where mass resolution is best. The rationale is that the median resists skew from the track's full span, whereas the maximum-intensity m/z captures the peak's most reliable mass measurement. When multiple intensity points exist in the same scan (due to data binning granularity), use the maximum intensity to break ties, then propagate that m/z value into the consensus calculation.

## Related tools

- **pymzml** (Parses mzML files to extract raw MS1 spectra as (m/z, scan_number, intensity) tuples for indexing into mzTree)
- **asari** (Orchestrates mass track construction and consensus m/z determination as part of the composite map building workflow) — https://github.com/shuzhao-li/asari
- **scipy.signal.find_peaks** (Supports peak detection and intensity maximum identification on processed mass tracks after consensus m/z is assigned)

## Examples

```
consensus_mz = (np.median(mz_values) + mz_at_max_intensity) / 2; mass_track = (consensus_mz, intensity_vector)
```

## Evaluation signals

- consensus_mz values fall within the original m/z range spanned by the mass track (min ≤ consensus_mz ≤ max)
- consensus_mz is closer to the median m/z than to isolated outliers in the track's m/z distribution
- consensus_mz aligns with high-intensity regions of the mass track (vicinity of maximum intensity)
- consensus_mz is stable across repeated calculations (deterministic, not sensitive to minor perturbations in input scan order)
- Consensus masses for isotopically related tracks (e.g., ¹²C vs. ¹³C) differ by the expected mass shift (≈1.003 amu for ¹³C, within instrument ppm tolerance)

## Limitations

- If the intensity vector is heavily skewed with most signal in a few scans, median m/z may underweight the most reliable mass region; median + max approach mitigates but does not eliminate this bias.
- In presence of mass calibration drift across the retention time range, median m/z may not reflect true neutral mass; requires prior retention-time-aware mass alignment or calibration correction.
- If a mass track spans multiple poorly resolved co-eluting peaks, consensus_mz represents an artificial average; resolve using nearest-neighbor clustering (nn_cluster_by_mz_seeds) before consensus determination.
- Low-intensity mass tracks with baseline noise may yield unstable median or maximum-intensity m/z; apply intensity thresholding (min_intensity_threshold, default 1e3) before consensus calculation.

## Evidence

- [other] Build each mass track as (consensus_mz, intensity_vector) where consensus_mz = mean(median_mz, mz_at_highest_intensity), maximum intensity is used when multiple points exist in the same scan, and zeros are inserted for missing intensity values across full RT range.: "consensus_mz = mean(median_mz, mz_at_highest_intensity)"
- [intro] Taking advantage of high mass resolution to prioritize mass separation and alignment during the initial processing of MS1 spectra.: "high mass resolution to prioritize mass separation and alignment"
- [other] For each data bin, determine the number of mass tracks: if m/z range is within 2 × ppm tolerance, create one track; otherwise apply nearest-neighbor clustering via nn_cluster_by_mz_seeds using m/z histogram peaks separated by mz tolerance minimum.: "m/z range is within 2 × ppm tolerance, create one track"
- [other] Establish anchor mass tracks by identifying m/z differences matching 13C/12C isotopes or Na/H adducts.: "m/z differences matching 13C/12C isotopes or Na/H adducts"
