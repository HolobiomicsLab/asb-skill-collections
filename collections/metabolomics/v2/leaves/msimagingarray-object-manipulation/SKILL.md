---
name: msimagingarray-object-manipulation
description: Use when when you have loaded mass spectrometry imaging data into a MSImagingArrays
  object in Cardinal 3.6 and need to explore the effects of multiple preprocessing
  steps (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Cardinal
  - R
  - CardinalIO
  - Cardinal 3.6
  - BiocParallel
  - matter 2.4 / 2.6
  techniques:
  - MS-imaging
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1093/bioinformatics/btv146
  title: Cardinal
evidence_spans:
- library(Cardinal)
- '*Cardinal 3.6* is a major update with breaking changes. It bring support many of
  the new low-level signal processing functions'
- 'Once installed, Cardinal can be loaded with library(): library(Cardinal)'
- 'We can read an example of a "continuous" imzML file from the `CardinalIO` package:'
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btv146
  all_source_dois:
  - 10.1093/bioinformatics/btv146
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# msimagingarray-object-manipulation

## Summary

Queuing and chaining spectral processing operations on MSImagingArrays objects in Cardinal 3.6 to preview and apply multiple signal processing methods (smoothing, baseline reduction, recalibration, peak picking) without immediate computation. This skill enables efficient exploration of preprocessing parameter combinations before committing to full dataset processing.

## When to use

When you have loaded mass spectrometry imaging data into a MSImagingArrays object in Cardinal 3.6 and need to explore the effects of multiple preprocessing steps (e.g., comparing Savitzky-Golay vs. Gaussian smoothing, or chaining normalization → smoothing → baseline reduction) before applying them to the full dataset. Use this skill when you want to preview results on individual spectra or subsets via plot() before processing all spectra in memory.

## When NOT to use

- Data is already in peak-picked or feature-summarized form (e.g., a feature matrix or m/z bin table) — MSImagingArrays is designed for raw spectra.
- You need immediate results and cannot tolerate the overhead of queuing operations; use direct function calls on small subsets instead.
- Your data is stored in a format other than imzML or Analyze 7.5 and has not yet been imported via readMSIData().

## Inputs

- MSImagingArrays object (with spectral data from imzML or Analyze 7.5 format)
- Raw mass spectra (m/z and intensity pairs)
- Preprocessing method name (string: 'gaussian', 'sgolay', 'bilateral', etc.)
- Method-specific parameters (window size, polynomial order, noise threshold)

## Outputs

- Queued MSImagingArrays object (preprocessing operations staged for execution)
- Smoothed spectra (Gaussian, Savitzky-Golay, bilateral, nonlinear diffusion, guided, peak-aware guided, or moving average)
- Preview plot(s) showing original vs. preprocessed spectrum overlay
- Comparison figure or table highlighting differences in peak preservation and noise reduction

## How to apply

Load your MSImagingArrays object (created from imzML, Analyze 7.5, or simulated data) and chain preprocessing operations using the smooth(), reduceBaseline(), recalibrate(), and peakPick() methods. Each operation is queued on the object without immediate execution. Preview the effect of a queued operation by extracting or plotting a single spectrum using plot() with parameters such as xlim (mass range) and linewidth to visualize the original spectrum overlaid with the queued result. This deferred-execution model allows you to compare multiple parameter sets (e.g., different window sizes for Savitzky-Golay, different polynomial orders, or different noise estimation methods) on a small subset before committing to processing the entire dataset. Rationale: Cardinal 3.6's redesigned MSImagingArrays class and queue-based operations support out-of-memory datasets and parallel processing via BiocParallel, making interactive preview crucial for tuning parameters on large imzML files.

## Related tools

- **Cardinal 3.6** (Provides MSImagingArrays class and queue-based preprocessing methods (smooth, reduceBaseline, recalibrate, peakPick) with plot() preview capability) — https://github.com/kuwisdelu/Cardinal
- **CardinalIO** (Supplies example imzML files and I/O support for reading continuous and processed imzML formats)
- **BiocParallel** (Enables parallel execution of queued preprocessing operations via BPPARAM option)
- **matter 2.4 / 2.6** (Provides low-level signal processing functions underlying Cardinal 3.6's preprocessing methods)

## Examples

```
library(Cardinal); path_continuous <- CardinalIO::exampleImzMLFile('continuous'); data <- readMSIData(path_continuous); smoothed_sgolay <- smooth(data, method='sgolay'); plot(smoothed_sgolay, xlim=c(500, 1500))
```

## Evaluation signals

- Plot overlay shows original spectrum and queued smoothed result with peak positions preserved or attenuated as expected for the chosen method (e.g., Savitzky-Golay preserves narrow peaks better than Gaussian).
- Smoothed spectrum has reduced noise (lower baseline fluctuation, cleaner minor peaks) without artificial peak shift or broadening.
- Queued operations are chainable without error; multiple methods can be sequentially applied to the same MSImagingArrays object.
- xlim and linewidth parameters on plot() correctly restrict the mass range and control line thickness as specified, allowing detailed inspection of specific m/z regions.
- Queued operations do not consume full memory until explicitly processed (verify by checking object size or memory profile before/after preview).

## Limitations

- Preview works on individual or small subsets of spectra; full-dataset processing still requires execution (via implicit or explicit realize/compute step).
- Parameter tuning is manual; no automated method selection or cross-validation is built into the queuing interface.
- Savitzky-Golay and other methods assume regularly spaced m/z bins; spectra from processed (binned) imzML are required; continuous format must be binned first.
- No changelog available in the provided documentation, so breaking changes between Cardinal 3.6 and earlier versions are not fully documented.

## Evidence

- [intro] Queue operations and preview before processing: "The smooth() function queues smoothing operations on MSImagingArrays objects and supports both Gaussian and Savitzky-Golay (sgolay) methods. Both methods can be chained with plot() to preview results"
- [intro] Savitzky-Golay and Gaussian smoothing methods are available: "New spectral processing methods in smooth(): Improved Gaussian filtering, Bilateral and adaptive bilateral filtering, Nonlinear diffusion filtering, Guided filtering, Peak-aware guided filtering"
- [intro] MSImagingArrays is designed for representing raw spectra: "Updated MSImagingExperiment class with a new counterpart MSImagingArrays class for better representing raw spectra"
- [intro] Parallel processing support for all preprocessing methods: "Parallel processing support via the BiocParallel package for all pre-processing methods and any statistical analysis methods with a BPPARAM option"
- [intro] readMSIData supports imzML and Analyze 7.5 formats: "Cardinal natively supports reading and writing imzML (both 'continuous' and 'processed' types) and Analyze 7.5 formats via the readMSIData() and writeMSIData() functions"
- [intro] Can chain multiple preprocessing methods: "Use normalize() to queue normalization on MSImagingArrays or MSImagingExperiment"
