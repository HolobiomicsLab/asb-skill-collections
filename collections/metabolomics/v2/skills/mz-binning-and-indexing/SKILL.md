---
name: mz-binning-and-indexing
description: Use when immediately after parsing mzML files into (m/z, scan_number, intensity) tuples when you need to build mass tracks from raw MS1 spectra. Use it when working with high-resolution instruments (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - pymzml
  - Python
  - asari.chromatograms.get_thousandth_bins
  - asari.chromatograms.extract_massTracks_
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

# mz-binning-and-indexing

## Summary

Organize high-resolution MS1 spectra into m/z-indexed data structures and merge adjacent bins to enable efficient mass track construction and alignment. This skill leverages integer-keyed indexing and proximity-based merging to separate and align masses prior to feature detection.

## When to use

Apply this skill immediately after parsing mzML files into (m/z, scan_number, intensity) tuples when you need to build mass tracks from raw MS1 spectra. Use it when working with high-resolution instruments (e.g. Orbitrap) where mass separation and alignment must be prioritized over individual sample peak detection, and when you have ≥1 sample requiring reproducible mass track construction.

## When NOT to use

- Input is already a feature table or pre-processed consensus feature matrix; binning is a preprocessing step, not a post-hoc refinement.
- Profile-mode (non-centroid) mzML files; binning assumes discrete m/z centroids, not continuous spectral profiles.
- Very low mass resolution data (e.g., nominal mass Orbitrap or nominal-mass quadrupole); the skill exploits high mass resolution to separate isobars and requires ≥5 ppm relative accuracy.

## Inputs

- mzML file (centroid mode, MS1 spectra)
- List of (m/z, scan_number, intensity) tuples extracted from mzML
- Parameters: minimal required scan count per bin, absolute distance threshold (≤0.001 amu), ppm tolerance (instrument-specific)

## Outputs

- mzTree dictionary: keys = int(mz × 1000), values = lists of (m/z, scan_number, intensity)
- Data bins: consolidated m/z intervals with merged adjacent bins
- Bin metadata: m/z range, number of contributing scans, scan count distribution

## How to apply

Parse centroid mzML files using pymzml to extract all MS1 spectra as (m/z, scan_number, intensity) tuples. Index these points into an mzTree dictionary keyed by int(mz × 1000) for fast lookup. Apply get_thousandth_bins to create initial data bins from the mzTree, filtering bins that fail to meet a minimal required scan count threshold. Merge adjacent bins that are separated by ≤0.001 amu (0.001 Da) or fall within the ppm tolerance window (instrument-dependent, typically 5 ppm for Orbitrap). This two-stage merging—first by absolute distance, then by relative ppm—ensures that genuine isobars within the mass resolution are separated while noise and low-abundance spurious peaks are consolidated. The result is a set of consolidated mass bins, each representing a distinct m/z locus across the retention time range.

## Related tools

- **pymzml** (Parse mzML files and extract MS1 spectra as (m/z, scan_number, intensity) tuples) — https://github.com/shuzhao-li/asari
- **asari.chromatograms.get_thousandth_bins** (Create initial data bins from mzTree using scan count filtering and adjacency-based merging) — https://github.com/shuzhao-li/asari
- **asari.chromatograms.extract_massTracks_** (Construct mass tracks from consolidated bins for each sample) — https://github.com/shuzhao-li/asari

## Examples

```
from asari.chromatograms import get_thousandth_bins; import pymzml; spectra = [(m, scan, intensity) for m, scan, intensity in pymzml.run('sample.mzML')]; mzTree = {int(m*1000): [] for m, s, i in spectra}; [mzTree[int(m*1000)].append((m, s, i)) for m, s, i in spectra]; bins = get_thousandth_bins(mzTree, min_scan_count=5, ppm_tolerance=5)
```

## Evaluation signals

- Bins are non-overlapping and monotonically ordered by m/z; no bin spans >0.001 amu or exceeds ppm tolerance.
- Each bin contains ≥ minimum required scan count; low-abundance singleton m/z points are merged into adjacent bins.
- Mass separation is preserved: isobars separated by >ppm tolerance remain in distinct bins; spurious points within tolerance are consolidated.
- mzTree keys are integers in range [min(int(mz × 1000)), max(int(mz × 1000))]; lookup time is O(1) for a given m/z.
- Downstream mass track construction produces one track per bin (or multiple tracks per bin if the m/z range within a bin exceeds 2 × ppm tolerance, triggering nearest-neighbor clustering); track consensus m/z matches the bin's observed m/z distribution.

## Limitations

- Binning is sensitive to the choice of minimal scan count threshold; too low a threshold will retain noise spikes; too high will merge genuine low-abundance peaks.
- The 0.001 amu and ppm-based merging rules assume Orbitrap-class high-resolution instruments; results on lower-resolution instruments (e.g., nominal-mass TOF) may be unpredictable.
- Isotopic fine structure (e.g., 13C satellites) may be binned separately or together depending on ppm tolerance; the article notes that anchor mass tracks are identified post-hoc to resolve isotopic relationships.
- Very high dynamic range (>1E8 intensity) may require rescaling before or after binning; the article mentions a preset ceiling of 1E8 for mass track intensity.

## Evidence

- [other] Parse the mzML file using pymzml to retrieve all MS1 spectra as a list of (m/z, scan number, intensity) tuples.: "Parse the mzML file using pymzml to retrieve all MS1 spectra as a list of (m/z, scan_number, intensity) tuples."
- [other] Index data points into an mzTree dictionary keyed by int(mz × 1000) for efficient retrieval.: "Index data points into an mzTree dictionary keyed by int(mz × 1000) for efficient retrieval."
- [other] Create data bins from mzTree using get_thousandth_bins, filtering for minimal required scan count and merging adjacent bins separated by ≤0.001 amu or within ppm tolerance.: "Create data bins from mzTree using get_thousandth_bins, filtering for minimal required scan count and merging adjacent bins separated by ≤0.001 amu or within ppm tolerance."
- [intro] Taking advantage of high mass resolution to prioritize mass separation and alignment: "Taking advantage of high mass resolution to prioritize mass separation and alignment"
- [other] The default method uses `pymzml` to parse mzML files.: "The default method uses `pymzml` to parse mzML files."
