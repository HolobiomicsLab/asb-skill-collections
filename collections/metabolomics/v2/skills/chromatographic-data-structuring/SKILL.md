---
name: chromatographic-data-structuring
description: Use when after parsing a centroid mzML file into (m/z, scan_number, intensity) tuples, when you need to organize sparse MS1 data for efficient peak detection and cross-sample alignment. Apply this skill when high mass resolution (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_3520
  tools:
  - pymzml
  - Python
  - asari (chromatograms.extract_massTracks_)
  - scipy.signal.find_peaks
  - mass2chem
  - metDataModel
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

# chromatographic-data-structuring

## Summary

Organize and index raw MS1 spectra into mass-indexed data structures (mzTree) and construct mass track objects (consensus m/z, intensity vector) that serve as the foundation for peak detection and feature alignment. This skill bridges raw mzML parsing and composite map construction by imposing m/z-based spatial organization on temporal (scan-number and retention-time) intensity measurements.

## When to use

After parsing a centroid mzML file into (m/z, scan_number, intensity) tuples, when you need to organize sparse MS1 data for efficient peak detection and cross-sample alignment. Apply this skill when high mass resolution (e.g., Orbitrap data at <5 ppm tolerance) permits m/z-driven binning rather than sample-wise peak detection, and when you intend to detect features on a composite map across multiple samples rather than individually.

## When NOT to use

- Input is already a feature table or aligned matrix of peak intensities — this skill operates on raw spectra, not post-detection features.
- Data are from low-resolution instruments (e.g., quadrupole, <20 ppm) where m/z-driven binning may merge chemically distinct ions; consider sample-wise peak detection instead.
- Retention time has not yet been calibrated or aligned across samples — apply retention time alignment before or after mass track construction, depending on your workflow design.

## Inputs

- mzML file (centroid spectra)
- list of (m/z, scan_number, intensity) tuples from MS1 spectra
- ppm mass tolerance (e.g., 5 ppm for Orbitrap)
- minimal scan count threshold (e.g., 3 scans per bin)

## Outputs

- mzTree dictionary indexed by int(mz × 1000)
- data bins with merged adjacent m/z ranges
- mass tracks: tuples of (consensus_mz, intensity_vector)
- anchor mass tracks linking isotopes or adducts
- sample registry with file metadata and mass track assignments

## How to apply

Parse the mzML file using pymzml to extract all MS1 spectra as (m/z, scan_number, intensity) tuples. Index the data points into an mzTree dictionary keyed by int(mz × 1000) for rapid m/z-range queries. Create data bins from mzTree using get_thousandth_bins, filtering for a minimal required scan count (e.g., ≥3 scans) and merging adjacent bins if separated by ≤0.001 amu or within your specified ppm tolerance. For each data bin, determine the number of mass tracks by checking whether the m/z range spans more than 2× your ppm tolerance; if so, apply nearest-neighbor clustering (nn_cluster_by_mz_seeds) using m/z histogram peaks. Construct each mass track as a (consensus_mz, intensity_vector) pair: set consensus_mz = mean(median_mz, mz_at_highest_intensity), take the maximum intensity when multiple points occupy the same scan, and insert zeros for scans with no data points across the full RT range. Finally, identify anchor mass tracks by detecting m/z differences matching known isotopes (13C/12C) or adducts (Na/H) to link related ion species.

## Related tools

- **pymzml** (Parse mzML files to extract MS1 spectra as (m/z, scan_number, intensity) tuples for indexing into mzTree)
- **asari (chromatograms.extract_massTracks_)** (Core implementation of mzTree indexing, data binning, mass track construction, and consensus m/z calculation) — https://github.com/shuzhao-li/asari
- **scipy.signal.find_peaks** (Local maxima detection used during nearest-neighbor clustering of m/z histogram peaks within data bins)
- **mass2chem** (Library of isotope and adduct mass differences for identifying anchor mass tracks (13C/12C, Na/H)) — https://github.com/shuzhao-li/mass2chem
- **metDataModel** (Provides reusable data structure definitions for mass tracks, spectra, and sample metadata) — https://github.com/shuzhao-li-lab/metDataModel

## Examples

```
from asari.chromatograms import extract_massTracks_; mass_tracks = extract_massTracks_(mzTree, data_bins, ppm_tolerance=5, mz_seed_separation=0.001)
```

## Evaluation signals

- mzTree dictionary is non-empty and all keys are integers in range [1000 × min_mz, 1000 × max_mz], with no gaps >1000 between consecutive keys
- Data bins are contiguous (no gaps), merged bins respect ≤0.001 amu or ppm tolerance thresholds, and each bin contains ≥ minimum scan count
- Each mass track's intensity_vector has length equal to total number of scans, with values ≥0 and zeros only where no data exist
- Consensus m/z for each mass track lies within the m/z range of its data bin and equals the stated formula mean(median_mz, mz_at_highest_intensity)
- Anchor mass tracks are identified with m/z differences matching known 13C/12C (1.003355 ± ppm tolerance) or Na/H (22.98977 ± ppm tolerance) mass shifts

## Limitations

- mzTree indexing by int(mz × 1000) introduces quantization at the 0.001 amu level; higher-precision m/z data may be degraded if ppm tolerance is tighter than ±0.5 ppm at low m/z
- Nearest-neighbor clustering of m/z histogram peaks assumes separable local maxima; overlapping or poorly resolved isotopic patterns may incorrectly merge or split mass tracks
- Consensus m/z calculation using mean(median_mz, mz_at_highest_intensity) can be biased if the highest-intensity scan occurs at the tail of a chromatographic peak; median m/z alone may be more robust for skewed distributions
- Anchor mass track identification requires reference mass differences (isotope, adduct library); missing or incorrect library entries will fail to link related ion species, leading to redundant or orphaned mass tracks

## Evidence

- [other] Parse the mzML file using pymzml to retrieve all MS1 spectra as a list of (m/z, scan_number, intensity) tuples.: "Parse the mzML file using pymzml to retrieve all MS1 spectra as a list of (m/z, scan_number, intensity) tuples."
- [other] Index data points into an mzTree dictionary keyed by int(mz × 1000) for efficient retrieval.: "Index data points into an mzTree dictionary keyed by int(mz × 1000) for efficient retrieval."
- [other] Create data bins from mzTree using get_thousandth_bins, filtering for minimal required scan count and merging adjacent bins separated by ≤0.001 amu or within ppm tolerance.: "Create data bins from mzTree using get_thousandth_bins, filtering for minimal required scan count and merging adjacent bins separated by ≤0.001 amu or within ppm tolerance."
- [other] For each data bin, determine the number of mass tracks: if m/z range is within 2 × ppm tolerance, create one track; otherwise apply nearest-neighbor clustering via nn_cluster_by_mz_seeds using m/z histogram peaks separated by mz tolerance minimum.: "For each data bin, determine the number of mass tracks: if m/z range is within 2 × ppm tolerance, create one track; otherwise apply nearest-neighbor clustering via nn_cluster_by_mz_seeds using m/z"
- [other] Build each mass track as (consensus_mz, intensity_vector) where consensus_mz = mean(median_mz, mz_at_highest_intensity), maximum intensity is used when multiple points exist in the same scan, and zeros are inserted for missing intensity values across full RT range.: "Build each mass track as (consensus_mz, intensity_vector) where consensus_mz = mean(median_mz, mz_at_highest_intensity), maximum intensity is used when multiple points exist in the same scan, and"
- [other] Establish anchor mass tracks by identifying m/z differences matching 13C/12C isotopes or Na/H adducts.: "Establish anchor mass tracks by identifying m/z differences matching 13C/12C isotopes or Na/H adducts."
- [intro] Taking advantage of high mass resolution to prioritize mass separation and alignment: "Taking advantage of high mass resolution to prioritize mass separation and alignment"
- [readme] Trackable and scalable Python program for high-resolution metabolomics data processing.: "Trackable and scalable Python program for high-resolution metabolomics data processing."
