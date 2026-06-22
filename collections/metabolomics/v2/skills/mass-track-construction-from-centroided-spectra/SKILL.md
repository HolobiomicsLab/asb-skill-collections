---
name: mass-track-construction-from-centroided-spectra
description: Use when when you have centroided mzML files from LC-MS metabolomics and need to construct high-mass-resolution mass tracks for each sample before alignment. Apply this skill at the start of an untargeted metabolomics workflow, before building a cross-sample MassGrid.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - Python
  - pymzml
  - khipu
  - JMS
  - HMDB 4
  - chromatograms.get_thousandth_bins
  - mass_functions.nn_cluster_by_mz_seeds
  - chromatograms.extract_single_track_fullrt_length
  - asari
derived_from:
- doi: 10.1038/s41467-023-39889-1
  title: asari
evidence_spans:
- Trackable and scalable Python program for high-resolution LC-MS metabolomics data preprocessing
- Trackable and scalable Python program for high-resolution metabolomics data processing.
- The default method uses `pymzml` to parse mzML files.
- The preannotaion is done via another package khipu (https://github.com/shuzhao-li-lab/khipu)
- The empirical compounds are searched against known compound database (default HMDB 4) via another package JMS (https://github.com/shuzhao-li/JMS).
- known compound database (default HMDB 4)
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

# mass-track-construction-from-centroided-spectra

## Summary

Extract and organize ion chromatograms (mass tracks) from individual LC-MS samples by parsing centroided mzML spectra, binning m/z values at 0.001 amu resolution, and clustering nearby m/z values to establish anchor tracks for isotopologues and adducts. This step precedes cross-sample alignment and is essential for tracking reproducibility between features and their underlying extracted ion currents (EICs).

## When to use

When you have centroided mzML files from LC-MS metabolomics and need to construct high-mass-resolution mass tracks for each sample before alignment. Apply this skill at the start of an untargeted metabolomics workflow, before building a cross-sample MassGrid. The skill is most effective when dealing with high-resolution instruments (e.g., Orbitrap, Q-TOF) where m/z separation is prioritized and mass deviation typically remains below 1 ppm.

## When NOT to use

- Input data is already profile (continuous) mzML rather than centroided — apply centroiding first (e.g. via ProteoWizard or vendor-supplied tools) before this skill.
- You have only MS/MS spectra without MS1 data — mass-track construction requires full-scan (MS1) chromatographic traces.
- Mass resolution is very low (< 10,000 FWHM) or multiple unresolved ions are expected within a single m/z bin — clustering and isotope anchoring may produce false splits or missed coelutions.

## Inputs

- centroided mzML file(s) from a single LC-MS sample
- instrument-specific mass tolerance parameter (ppm; default 5 ppm)
- expected m/z binning resolution (0.001 amu default)

## Outputs

- per-sample mass_tracks dictionary: {m/z → [(scan, intensity), ...]
- mzTree (indexed m/z spectra data structure)
- anchor_mass_tracks (isotopologue and adduct relationships)
- mass_track JSON for downstream chromatographic calibration

## How to apply

Parse all MS1 spectra from each mzML file using pymzml to extract (m/z, scan number, intensity) tuples and index them into an mzTree (dictionary keyed by int(m/z × 1000)) for efficient retrieval. Bin the mzTree values at 0.001 amu boundaries using chromatograms.get_thousandth_bins; each bin becomes a candidate mass track if its m/z range remains within 2× the tolerance ppm (default 5 ppm, ~0.005 m/z units). For bins whose m/z ranges exceed this threshold, apply nearest-neighbor clustering via mass_functions.nn_cluster_by_mz_seeds to split the bin into multiple tracks. Establish anchor mass tracks by identifying m/z differences matching 13C/12C isotope shift (1.003 Da) or common adducts (e.g., Na–H, 22.99 Da); these anchors enable later confirmation of empirical compound relationships. Intensity values at each scan are extracted per mass track to create the full chromatographic profile. Output per-sample mass tracks are JSON-serializable and maintain m/z, scan-number, and intensity mappings needed for subsequent RT calibration and cross-sample alignment.

## Related tools

- **pymzml** (Parse mzML files to extract and index MS1 spectra (m/z, scan, intensity) as mzTree data structure)
- **chromatograms.get_thousandth_bins** (Bin mzTree into 0.001 amu windows and create candidate mass track seeds) — https://github.com/shuzhao-li/asari
- **mass_functions.nn_cluster_by_mz_seeds** (Apply nearest-neighbor clustering to split m/z bins exceeding 2× tolerance ppm into distinct mass tracks) — https://github.com/shuzhao-li/asari
- **chromatograms.extract_single_track_fullrt_length** (Extract full-retention-time intensity profile for a single mass track across all scans in a sample) — https://github.com/shuzhao-li/asari
- **asari** (Orchestrates mass-track construction as part of the end-to-end LC-MS feature extraction pipeline) — https://github.com/shuzhao-li/asari

## Examples

```
python3 -m asari.main process -i mydir/projectx_dir --mode pos
```

## Evaluation signals

- All MS1 scans are represented in at least one mass track (no missing m/z signals)
- m/z deviation within each mass track is ≤ 1 ppm (expected from high-resolution instruments after binning and clustering)
- Anchor mass tracks for 13C and Na/H adducts are correctly identified and linked to parent tracks (validated by m/z difference within isotope/adduct mass tolerance)
- No duplicate intensity assignments (each scan's intensity for a given m/z bin appears in exactly one mass track)
- RT chromatographic profiles are continuous (no unexpected scan gaps) and intensity values are non-negative integers or floats

## Limitations

- Assumes centroided input; profile-mode spectra must be centroided upstream, which may introduce artifacts or data loss.
- Clustering threshold (2× tolerance ppm) may not resolve very close isobars or high-complexity m/z regions in some biological matrices.
- Anchor mass-track identification relies on exact isotope/adduct mass shifts; modifications, non-standard adducts, or ion losses are not automatically detected and may remain unlinked.
- Performance scales with spectral complexity and number of scans; very high-resolution or long chromatographic runs may increase memory and compute time.
- Does not account for spectral artifacts, contamination, or instrument calibration drift; downstream QC and calibration (RT_lowess_calibration) are required to mitigate.

## Evidence

- [other] Extract mass tracks for each sample by parsing MS1 spectra with pymzml, binning m/z values to 0.001 amu using chromatograms.get_thousandth_bins, clustering with mass_functions.nn_cluster_by_mz_seeds where m/z ranges exceed 2× tolerance ppm (default 5 ppm), and establishing anchor mass tracks for 13C/12C isotopes and Na/H adducts.: "Extract mass tracks for each sample by parsing MS1 spectra with pymzml, binning m/z values to 0.001 amu using chromatograms.get_thousandth_bins, clustering with mass_functions.nn_cluster_by_mz_seeds"
- [methods] Get all MS1 spectra from a data file, as a list of [(m/z, scan number, intensity), ...]. Index to a dictionary by int(mz * 1000) for efficiency retrieval. This is an mzTree.: "Get all MS1 spectra from a data file, as a list of [(m/z, scan number, intensity), ...]. Index to a dictionary by int(mz * 1000) for efficienty retrieval. This is an mzTree."
- [methods] Create a list of data bins from mzTree. Each bin starts with a value in the mzTree, which has a m/z range around 0.001: "Create a list of data bins from mzTree. Each bin starts with a value in the mzTree, which has a m/z range around 0.001"
- [methods] Build mass tracks per data bin. If the m/z range in a data bin is within 2 x tolerance ppm, the bin leads to a single mass track.: "Build mass tracks per data bin. If the m/z range in a data bin is within 2 x tolerance ppm, the bin leads to a single mass track."
- [intro] Reproducible, track and backtrack between features and mass tracks (EICs): "Reproducible, track and backtrack between features and mass tracks (EICs)"
- [readme] Input data are centroid mzML files from LC, GC or DI-MS metabolomics.: "Input data are centroid mzML files from LC, GC or DI-MS metabolomics."
