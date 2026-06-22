---
name: spectrum-binning-and-normalization
description: Use when you have raw, high-resolution MS/MS spectra in mzML, mzXML, or MGF format that need to be prepared for fast similarity searching or clustering.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - falcon
  - spectrum-utils==0.3.5
  - spectrum-utils
derived_from:
- doi: 10.1002/rcm.9153
  title: falcon
evidence_spans:
- The _falcon_ spectrum clustering tool uses advanced algorithmic techniques for highly efficient processing of millions of MS/MS spectra.
- pip install falcon-ms spectrum-utils==0.3.5
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_falcon
    doi: 10.1002/rcm.9153
    title: falcon
  dedup_kept_from: coll_falcon
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

# spectrum-binning-and-normalization

## Summary

Transform high-resolution tandem MS/MS spectra into binned, normalized representations that preserve mass accuracy while enabling efficient downstream feature hashing and nearest-neighbor indexing. This preprocessing step is essential for large-scale spectrum clustering workflows.

## When to use

Apply this skill when you have raw, high-resolution MS/MS spectra in mzML, mzXML, or MGF format that need to be prepared for fast similarity searching or clustering. Use it as the first transformation step before feature hashing and nearest-neighbor indexing, particularly when processing millions of spectra where computational efficiency is critical.

## When NOT to use

- Do not use if spectra are already converted to low-dimensional hashed vectors or feature tables; binning is an upstream step.
- Do not apply if you require preservation of exact peak masses or isotopic fine structure; binning sacrifices mass resolution for computational efficiency.
- Do not use if your input spectra are already preprocessed (e.g., centroided with peak picking completed); binning expects raw or lightly processed peak lists.

## Inputs

- High-resolution MS/MS spectra in mzML, mzXML, or MGF format
- Peak intensity arrays with corresponding m/z values
- Precursor mass tolerance (ppm or Dalton)
- Fragment mass tolerance (Dalton)

## Outputs

- Binned, normalized sparse vectors (high-dimensional representation of spectra)
- Peak-filtered spectra meeting quality thresholds (≥5 peaks, ≥250 m/z range)
- Scaled intensity matrices ready for feature hashing

## How to apply

Load high-resolution MS/MS spectra and bin them across the m/z range using fixed-width mass bins (typically small bins to tightly capture fragment masses). Normalize peak intensities within each bin—commonly using square root or logarithmic scaling, or rank-based scaling depending on your spectral characteristics. For bottom-up proteomics, apply default preprocessing: discard spectra with fewer than 5 peaks or spanning less than 250 m/z range, and trim peaks outside the 101–500 m/z window. The binned, normalized vectors preserve cosine similarity and serve as the sparse, high-dimensional input to feature hashing. Adjust scaling and m/z filters if analyzing metabolomics or top-down data, as defaults are tuned for peptide spectra.

## Related tools

- **falcon** (Implements spectrum binning and normalization as the first step in the full clustering pipeline; accepts mzML/mzXML/MGF input and applies configurable preprocessing.) — https://github.com/bittremieux/falcon
- **spectrum-utils** (Provides utility functions for spectrum I/O, filtering, and transformation; version 0.3.5 is a dependency of falcon.)

## Examples

```
falcon peak/*.mzml falcon --export_representatives --precursor_tol 20 ppm --fragment_tol 0.05 --eps 0.10
```

## Evaluation signals

- Verify that all output bins have consistent width across the m/z range and that no peaks are lost due to bin boundaries.
- Check that intensity scaling (square root, logarithm, or rank) is consistently applied across all spectra and produces non-negative values.
- Confirm that spectra failing quality thresholds (< 5 peaks or < 250 m/z span) are correctly excluded from downstream analysis.
- Validate that cosine similarity between pairs of binned vectors approximates the cosine similarity of the original high-resolution spectra.
- Ensure output vectors are in sparse format (e.g., SciPy sparse matrix) when input is sparse, preserving memory efficiency for millions of spectra.

## Limitations

- Bin width must be chosen carefully: too coarse bins lose mass resolution; too fine bins increase vector dimensionality and memory overhead.
- Default preprocessing settings (5 peaks, 250 m/z range, 101–500 m/z window) are tuned for bottom-up proteomics; metabolomics and top-down data require parameter adjustment.
- Intensity scaling method influences the subsequent cosine distance threshold (eps parameter); changing scaling may require recalibration of clustering cutoffs.
- Binning is irreversible; exact peak masses and fine structure are lost. If high mass accuracy is required downstream, preserve original spectra separately.

## Evidence

- [intro] High-resolution spectra are binned and converted to low-dimensional vectors using feature hashing: "First, high-resolution spectra are binned and converted to low-dimensional vectors using feature hashing."
- [other] Bin spectra across the m/z range and normalize intensities as part of workflow: "2. Bin spectra across the m/z range and normalize intensities."
- [readme] Spectra are converted to sparse vectors using small mass bins to tightly capture their fragment masses: "First, spectra are converted to sparse vectors using small mass bins to tightly capture their fragment masses."
- [readme] Default preprocessing settings for bottom-up proteomics: "Default values are minimum 5 peaks and 250 m/z range. It is recommended to reduce these values when clustering metabolomics data."
- [readme] Scaling options and their effects: "Scale the peak intensities by their square root, logarithm, rank, or no scaling. Default is no scaling, with square root scaling often giving good results as well."
- [readme] M/z range filtering defaults: "Default values are 101 m/z and 500 m/z, respectively. Peaks outside these values will be discarded."
