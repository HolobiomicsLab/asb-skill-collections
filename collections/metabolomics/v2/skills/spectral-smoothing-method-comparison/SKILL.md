---
name: spectral-smoothing-method-comparison
description: Use when when you have raw mass spectra in an MSImagingArrays object and need to decide between Savitzky-Golay and Gaussian smoothing methods based on their effects on peak shape fidelity and baseline noise. Apply this skill when peak preservation is a priority (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - Cardinal
  - R
  - CardinalIO
  - Cardinal 3.6
  - matter 2.4/2.6
  - BiocParallel
derived_from:
- doi: 10.1093/bioinformatics/btv146
  title: Cardinal
evidence_spans:
- library(Cardinal)
- '*Cardinal 3.6* is a major update with breaking changes. It bring support many of the new low-level signal processing functions'
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-smoothing-method-comparison

## Summary

Compare Savitzky-Golay and Gaussian smoothing methods applied to mass spectra in Cardinal 3.6 to evaluate differences in peak preservation and noise reduction. This skill is essential when choosing between smoothing algorithms for MSImagingArrays objects where preserving spectral features while reducing noise is critical.

## When to use

When you have raw mass spectra in an MSImagingArrays object and need to decide between Savitzky-Golay and Gaussian smoothing methods based on their effects on peak shape fidelity and baseline noise. Apply this skill when peak preservation is a priority (e.g., quantitative analysis) or when noise reduction must be balanced against spectral detail loss.

## When NOT to use

- Input spectra are already pre-smoothed or have been heavily averaged—re-smoothing may over-blur features.
- Peak picking has already been performed on raw spectra—apply smoothing before peak detection, not after.
- Data are already baseline-corrected and normalized—smoothing order matters; apply smooth() before reduceBaseline() or normalize().

## Inputs

- MSImagingArrays object with spectral data
- mass spectra with noise and peaks
- mass range (xlim parameter for visualization)

## Outputs

- Savitzky-Golay smoothed spectrum (queued operation)
- Gaussian smoothed spectrum (queued operation)
- comparative visualization (plot overlay with original)

## How to apply

Load Cardinal 3.6 and create or import an MSImagingArrays object with spectral data. Queue Savitzky-Golay smoothing using smooth(method="sgolay") with default polynomial window parameters on a copy of the spectra. Queue Gaussian smoothing using smooth(method="gaussian") on another copy. Use plot() with xlim to preview both operations on the same mass range before processing. Overlay the original spectrum with both smoothed results to visually assess peak preservation (how well Savitzky-Golay maintains peak heights and widths) versus noise reduction efficacy (how well Gaussian suppresses low-amplitude noise). Produce a side-by-side figure comparing all three traces to guide method selection for your downstream statistical analysis.

## Related tools

- **Cardinal 3.6** (provides smooth() method with sgolay and gaussian parameters for queuing smoothing operations on MSImagingArrays) — https://github.com/kuwisdelu/Cardinal
- **matter 2.4/2.6** (low-level signal processing functions underlying Cardinal 3.6 smoothing methods)
- **BiocParallel** (enables parallel processing of smoothing operations across multiple spectra)
- **R** (host language for Cardinal library execution and visualization)

## Examples

```
library(Cardinal); data <- readMSIData(path); data_smooth_sg <- smooth(data, method='sgolay'); data_smooth_g <- smooth(data, method='gaussian'); plot(data, xlim=c(400, 800), linewidth=1); plot(data_smooth_sg, add=TRUE, linewidth=1, col='red'); plot(data_smooth_g, add=TRUE, linewidth=1, col='blue')
```

## Evaluation signals

- Visual inspection: Savitzky-Golay peaks maintain sharper edges and higher amplitude fidelity compared to Gaussian; Gaussian produces smoother, wider peaks with lower tails.
- Noise floor comparison: both methods should reduce high-frequency noise; quantify via standard deviation of baseline regions—expect Gaussian to reduce noise more uniformly across frequency.
- Peak height preservation: measure m/z positions and intensities of known reference peaks in both smoothed spectra—Savitzky-Golay should preserve original heights better (typically within 5–10% of raw), Gaussian may reduce them by 15–25%.
- Plot overlay reproducibility: re-run smooth() operations on the same MSImagingArrays object and confirm overlay results are identical—verifies parameter stability.
- Parameter sensitivity: test window size (polyorder, winsize for sgolay; sigma for gaussian) and confirm smoothing effect scales monotonically—larger windows = more smoothing; verify this is visible in overlay.

## Limitations

- Savitzky-Golay performance degrades near spectrum edges where polynomial window cannot be centered—use with xlim to avoid endpoints.
- Gaussian smoothing is slower for very large spectral datasets; Cardinal 3.6 mitigates this via BiocParallel, but single-spectrum preview may still lag.
- Method choice does not address systematic issues (e.g., chemical noise, instrument drift)—smoothing is a pre-processing step; if noise is not random or is correlated with sample features, neither method will preserve true signal.
- Queued operations in Cardinal do not process in-place; memory overhead increases with object size; for very large out-of-memory MSImagingExperiment objects, preview on a subset first.

## Evidence

- [intro] smooth() queues smoothing operations and supports Savitzky-Golay method: "The smooth() function queues smoothing operations on MSImagingArrays objects and supports both Gaussian and Savitzky-Golay (sgolay) methods."
- [intro] Both methods can be chained with plot() for preview before processing: "Both methods can be chained with plot() to preview results before processing, with parameters xlim to control the mass range and linewidth to adjust visualization."
- [intro] Workflow produces comparative figure showing original and smoothed spectra: "Produce a figure or table showing the original spectrum overlaid with both Savitzky-Golay and Gaussian smoothed results to highlight differences in peak preservation and noise reduction."
- [intro] Cardinal 3.6 includes new smoothing methods in smooth() function: "New spectral processing methods in smooth(): Improved Gaussian filtering, Bilateral and adaptive bilateral filtering, Nonlinear diffusion filtering, Guided filtering, Peak-aware guided filtering,"
- [intro] Parallel processing available for pre-processing methods: "Parallel processing support via the BiocParallel package for all pre-processing methods and any statistical analysis methods with a BPPARAM option"
