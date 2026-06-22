---
name: signal-preprocessing-chain-normalization-smoothing-baseline
description: Use when apply this preprocessing chain when you have loaded raw or continuous imzML mass spectra into a Cardinal MSImagingArrays object and need to prepare them for peak picking, statistical analysis, or imaging.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Cardinal
  - BiocParallel
  - R
  - Cardinal 3.6
  - matter 2.4 / matter 2.6
  - CardinalIO
derived_from:
- doi: 10.1093/bioinformatics/btv146
  title: Cardinal
evidence_spans:
- library(Cardinal)
- '*Cardinal 3.6* is a major update with breaking changes. It bring support many of the new low-level signal processing functions'
- Parallel processing support via the *BiocParallel* package for all pre-processing methods
- Parallel processing support via the *BiocParallel* package for all pre-processing methods and any statistical analysis methods with a `BPPARAM` option
- 'Once installed, Cardinal can be loaded with library(): library(Cardinal)'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cardinal_cq
    doi: 10.1093/bioinformatics/btv146
    title: Cardinal
  dedup_kept_from: coll_cardinal_cq
schema_version: 0.2.0
---

# Signal preprocessing chain: normalization, smoothing, baseline reduction

## Summary

A sequential preprocessing pipeline for mass spectrometry imaging spectra that normalizes intensity variability, reduces noise via smoothing, and removes baseline drift before peak detection or statistical analysis. This chain prepares raw MSImagingArrays objects for downstream analysis by queuing normalize(), smooth(), and reduceBaseline() operations.

## When to use

Apply this preprocessing chain when you have loaded raw or continuous imzML mass spectra into a Cardinal MSImagingArrays object and need to prepare them for peak picking, statistical analysis, or imaging. Use it before peakPick() or any comparative analysis across multiple spectra, especially when spectra exhibit intensity normalization drift, spectral noise, or baseline offset that could confound downstream analyses.

## When NOT to use

- Input spectra are already peak-picked or feature-summarized (e.g., already reduced to m/z bins with intensities) — preprocessing is designed for raw or continuous spectra, not feature tables.
- Baseline and noise characteristics are scientifically important and must be preserved (e.g., in certain diagnostic or quality-control contexts where absolute baseline shape or noise floor carries signal).
- Computational resources are severely constrained and parallel execution via BiocParallel is unavailable — the full chain can be memory-intensive on very large imzML files.

## Inputs

- MSImagingArrays object (raw or continuous imzML-derived)
- Preprocessed mass spectra with m/z and intensity dimensions

## Outputs

- MSImagingArrays object with queued normalization, smoothing, and baseline reduction operations
- Processed spectra ready for peak picking or statistical analysis

## How to apply

Load a preprocessed MSImagingArrays object and queue the chain sequentially: (1) apply normalize() with a normalization method (TIC, RMS, or reference feature) to remove intensity scale differences across spectra; (2) apply smooth() with an appropriate method (e.g., Gaussian, bilateral, Savitzky-Golay, or moving average) to reduce high-frequency noise while preserving spectral features; (3) apply reduceBaseline() with a method such as local minima interpolation, convex hull estimation, SNIP clipping, or running medians to remove baseline drift. Each step is queued as a lazy operation and executed together on all spectra in the array. The order is critical: normalize first to standardize intensity, then smooth to denoise, then remove baseline. This pipeline integrates with Cardinal's BiocParallel support for efficient parallel execution across all spectra.

## Related tools

- **Cardinal 3.6** (Primary framework providing normalize(), smooth(), and reduceBaseline() methods; implements class hierarchy (MSImagingArrays, SpectralImagingArrays) for lazy queueing and execution of preprocessing steps.) — https://github.com/kuwisdelu/Cardinal
- **BiocParallel** (Enables parallel processing of preprocessing methods across all spectra via BPPARAM option; accelerates execution on multi-core systems.)
- **matter 2.4 / matter 2.6** (Low-level signal processing functions underlying the new preprocessing methods in Cardinal 3.6; handles out-of-memory array operations.)
- **CardinalIO** (Provides example imzML datasets for testing the preprocessing pipeline.)

## Examples

```
msi_preprocessed <- normalize(msi_raw, method='TIC') %>% smooth(method='Gaussian') %>% reduceBaseline(method='SNIP'); msi_preprocessed <- process(msi_preprocessed, BPPARAM=BiocParallel::MulticoreParam())
```

## Evaluation signals

- Verify that normalize() has been applied: check that spectra intensity scales are uniform across the imaging array (e.g., TIC or RMS normalization reduces inter-spectrum intensity variance).
- Verify that smooth() has been applied: confirm that high-frequency noise is attenuated while major spectral peaks remain sharp and at their original m/z positions.
- Verify that reduceBaseline() has been applied: inspect the preprocessed spectra and confirm that baseline drift has been removed (baseline should be near zero across the m/z range with no trend).
- Check that the queue contains all three operations in the correct order (normalize → smooth → baseline) by examining the MSImagingArrays processingQueue or equivalent metadata.
- Execute the queue and validate output dimensions: processed spectra should retain the same m/z vector and spatial dimensions as input, with only intensity values modified.

## Limitations

- The order of operations is strict and must be normalize → smooth → baseline; applying them in a different order may yield artifacts or fail to remove intended sources of variation.
- Smoothing strength and baseline removal aggressiveness must be tuned to the specific mass range, ionization mode, and instrument resolution; inappropriate parameters can obscure real peaks (over-smoothing) or leave residual baseline (under-removal).
- Parallel execution via BiocParallel requires sufficient memory and computational resources; very large imzML files may exhaust memory even with out-of-memory support in matter.
- The preprocessing chain is generic and does not account for instrument-specific calibration drift, charge-state heterogeneity, or spatial artifacts that may require custom pre-preprocessing steps.

## Evidence

- [intro] Normalization step: "Use normalize() to queue normalization on MSImagingArrays or MSImagingExperiment"
- [intro] Smoothing step: "New spectral processing methods in smooth(): Improved Gaussian filtering, Bilateral and adaptive bilateral filtering, Nonlinear diffusion filtering, Guided filtering, Peak-aware guided filtering,"
- [intro] Baseline reduction step: "New spectral baseline reduction methods in reduceBaseline(): Interpolation from local minima, Convex hull estimation, Sensitive nonlinear iterative peak (SNIP) clipping, Running medians"
- [intro] Parallel processing integration: "Parallel processing support via the BiocParallel package for all pre-processing methods and any statistical analysis methods with a BPPARAM option"
- [intro] Data structure support: "Updated MSImagingExperiment class with a new counterpart MSImagingArrays class for better representing raw spectra"
- [other] Method context in workflow: "1. Load the preprocessed MSImagingArrays object (normalized via normalize(), smoothed via smooth(), and baseline-reduced via reduceBaseline()). 2. Queue derivative-based peak picking using peakPick()"
