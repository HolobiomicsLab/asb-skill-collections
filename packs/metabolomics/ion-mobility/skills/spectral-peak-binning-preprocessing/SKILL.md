---
name: spectral-peak-binning-preprocessing
description: Use when when you have raw high-resolution tandem mass spectra (mzML, mzXML, or MGF format) that you intend to cluster or compare at scale, and you need to convert continuous m/z and intensity measurements into discrete bins suitable for feature hashing or similarity searching.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - falcon
  - spectrum-utils
  - Python 3.8+
  techniques:
  - LC-MS
  - ion-mobility-MS
derived_from:
- doi: 10.1002/rcm.9153
  title: falcon
evidence_spans:
- The _falcon_ spectrum clustering tool uses advanced algorithmic techniques for highly efficient processing of millions of MS/MS spectra.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_falcon_cq
    doi: 10.1002/rcm.9153
    title: falcon
  dedup_kept_from: coll_falcon_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1002/rcm.9153
  all_source_dois:
  - 10.1002/rcm.9153
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-peak-binning-preprocessing

## Summary

Discretize high-resolution MS/MS spectra by binning m/z and intensity dimensions into small mass bins, preparing them for dimensionality reduction via feature hashing. This preprocessing step conserves spectral information while enabling efficient vectorization for large-scale clustering.

## When to use

When you have raw high-resolution tandem mass spectra (mzML, mzXML, or MGF format) that you intend to cluster or compare at scale, and you need to convert continuous m/z and intensity measurements into discrete bins suitable for feature hashing or similarity searching. Apply this before constructing nearest-neighbor indexes or computing pairwise distance matrices.

## When NOT to use

- Spectra are already in a low-dimensional feature vector format (e.g., already hashed or pre-computed feature tables)
- Analysis requires interpretation of exact fragment mass values; binning loses sub-bin resolution
- Input data are ion mobility or drift time spectra without clear m/z dimension

## Inputs

- high-resolution MS/MS spectra in mzML, mzXML, or MGF format
- raw spectrum objects with m/z and intensity arrays

## Outputs

- binned spectrum representations (sparse vectors with discretized m/z bins)
- quality-filtered spectrum set (spectra passing min_peaks and m/z_range thresholds)
- spectrum objects prepared for feature hashing input

## How to apply

Load raw MS/MS spectra using spectrum-utils or equivalent tool. Discretize each spectrum by assigning m/z values to small mass bins (bin width typically 0.1 Da or smaller) and optionally scaling intensities (square root or logarithm scaling often improve downstream clustering). Discard spectra failing quality filters: fewer than minimum peaks (default 5), m/z range smaller than threshold (default 250 Da), or peaks outside the m/z window (default 101–500 m/z). The binned spectra are then input to feature hashing, which maps sparse, high-dimensional bin vectors to low-dimensional dense or sparse vectors using a hash function such as MurmurHash3. This binning step is critical because it converts sparse, high-dimensional representations into a form amenable to efficient nearest-neighbor indexing without exhaustive all-pairs comparison.

## Related tools

- **spectrum-utils** (Load and parse raw MS/MS spectra in mzML, mzXML, MGF formats; handle spectrum metadata and peak arrays)
- **falcon** (Orchestrate binning, feature hashing, and downstream nearest-neighbor indexing and clustering pipeline) — https://github.com/bittremieux/falcon
- **Python 3.8+** (Runtime environment for spectrum-utils and falcon binning routines)

## Examples

```
falcon peak/*.mzml falcon --export_representatives --precursor_tol 20 ppm --fragment_tol 0.05 --eps 0.10
```

## Evaluation signals

- All output spectra have peaks within the configured m/z range (min_mz to max_mz); verify no peaks fall outside [101, 500] m/z by default
- Spectra passing quality filters have ≥ min_peaks peaks (default 5) and m/z span ≥ min_mz_range (default 250 Da)
- Binned representations are sparse vectors with keys corresponding to m/z bin indices and values representing summed or max intensity in each bin
- Downstream feature hashing preserves cosine similarity between binned vectors; verify by sampling spectrum pairs and comparing hashed vs. original binned cosine distances
- Output file format is compatible with nearest-neighbor index construction (e.g., dense or sparse vector serialization accepted by falcon's indexing stage)

## Limitations

- Binning width and intensity scaling method are user-configurable and can significantly influence downstream clustering purity; values between eps=0.05–0.15 typically yield pure results, but parameter tuning may be needed for metabolomics or top-down data
- Small mass bins tightly capture fragment masses but increase dimensionality before hashing; feature hashing must follow to reduce to feasible memory and compute
- Default min_peaks and min_mz_range thresholds (5 peaks, 250 m/z) are tuned for bottom-up proteomics; metabolomics and top-down analyses require adjustment
- Spectra with very few peaks or narrow m/z ranges are discarded; loss of rare or low-abundance peptides may occur

## Evidence

- [readme] Binning discretizes m/z and intensity; feature hashing follows: "spectra are converted to sparse vectors using small mass bins to tightly capture their fragment masses"
- [readme] Feature hashing conserves cosine similarity for downstream clustering: "feature hashing conserves the cosine similarity between hashed vectors and can be used to approximate the similarity between the original spectra"
- [readme] Quality filtering applied during preprocessing: "Discard spectra with fewer than the specified number of peaks, or peaks spanning a smaller m/z range between the minimum and maximum m/z value. Default values are minimum 5 peaks and 250 m/z range."
- [readme] Intensity scaling options during preprocessing: "Scale the peak intensities by their square root, logarithm, rank, or no scaling. Default is no scaling, with square root scaling often giving good results as well."
- [intro] High-resolution spectra converted via binning and feature hashing: "First, high-resolution spectra are binned and converted to low-dimensional vectors using feature hashing."
- [readme] Binning supports m/z range filtering: "min_mz and max_mz: The minimum and maximum peak m/z value, respectively. Peaks outside these values will be discarded. Default values are 101 m/z and 500 m/z, respectively."
