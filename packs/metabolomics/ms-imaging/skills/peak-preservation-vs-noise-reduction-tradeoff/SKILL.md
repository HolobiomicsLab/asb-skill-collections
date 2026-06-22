---
name: peak-preservation-vs-noise-reduction-tradeoff
description: Use when you have raw or baseline-corrected mass spectra from MSImagingArrays or MSImagingExperiment objects and need to decide between smoothing methods before peak picking or statistical analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Cardinal
  - R
  - CardinalIO
  - Cardinal 3.6
  - matter 2.4 / 2.6
  - BiocParallel
  techniques:
  - MS-imaging
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

# peak-preservation-vs-noise-reduction-tradeoff

## Summary

Evaluate and compare spectral smoothing methods (Savitzky-Golay vs. Gaussian) on mass spectra to understand their differential effects on peak sharpness, noise suppression, and signal fidelity. This skill is essential when preprocessing mass spectrometry imaging data where aggressive noise reduction risks obliterating narrow peaks or shifting peak positions.

## When to use

Use this skill when you have raw or baseline-corrected mass spectra from MSImagingArrays or MSImagingExperiment objects and need to decide between smoothing methods before peak picking or statistical analysis. Apply it when your spectrum contains both significant noise and narrow peaks of interest, or when you are uncertain whether peak broadening from smoothing will compromise downstream analysis (e.g., peak alignment, mass accuracy calibration, or spatial clustering).

## When NOT to use

- Spectra are already smoothed or heavily preprocessed and further smoothing would introduce artifacts.
- Analysis goal does not require noise reduction (e.g., exact mass measurement where any peak distortion is unacceptable).
- Peak picking method is robust to smoothing artifacts and no comparison is needed to justify method choice.

## Inputs

- MSImagingArrays object with raw or baseline-corrected mass spectra
- MSImagingExperiment object with spectral data
- Mass range (m/z) to evaluate via xlim parameter

## Outputs

- Smoothed spectral data (queued operations ready for processing)
- Overlaid comparison plots showing original and both smoothed spectra
- Visual and quantitative comparison of peak preservation and noise reduction
- Processed spectra ready for downstream peak picking or statistical analysis

## How to apply

Queue both Savitzky-Golay and Gaussian smoothing operations on the same MSImagingArrays object using smooth(method='sgolay') and smooth(method='gaussian'), adjusting window length and polynomial order for Savitzky-Golay, and kernel width for Gaussian. Preview or extract the smoothed spectra and generate overlaid plots with the original spectrum, examining peak height retention, baseline flatness, and noise floor reduction. Choose Savitzky-Golay if narrow peaks and edge preservation are critical; choose Gaussian if maximal noise suppression and smooth backgrounds are prioritized. Compare results using both visual inspection (peak shape, baseline noise) and quantitative metrics (signal-to-noise ratio, peak width, peak position shift) to validate the tradeoff choice for your downstream workflow.

## Related tools

- **Cardinal 3.6** (Provides smooth() function to queue Savitzky-Golay and Gaussian smoothing on MSImagingArrays and MSImagingExperiment objects, and plot() for side-by-side visualization of smoothed vs. original spectra.) — https://github.com/kuwisdelu/Cardinal
- **matter 2.4 / 2.6** (Underlying low-level signal processing functions that implement the Savitzky-Golay and Gaussian smoothing algorithms in Cardinal 3.6.)
- **BiocParallel** (Optional package for parallel processing of smoothing operations across multiple spectra to accelerate comparison workflow.)
- **R** (Programming environment for loading Cardinal library and executing smooth() and plot() commands.)

## Examples

```
library(Cardinal); msi <- readMSIData('data.imzML'); msi_sgolay <- smooth(msi, method='sgolay'); msi_gaussian <- smooth(msi, method='gaussian'); plot(msi, xlim=c(800, 1200)); plot(msi_sgolay, xlim=c(800, 1200)); plot(msi_gaussian, xlim=c(800, 1200))
```

## Evaluation signals

- Side-by-side plots show visually distinct peak shapes: Savitzky-Golay peaks retain sharp edges and fine structure; Gaussian peaks are broader but smoother.
- Baseline noise is reduced in both smoothed spectra relative to original, but Gaussian smoothing produces lower noise floor at cost of peak broadening.
- Peak positions (m/z values) remain stable under Savitzky-Golay smoothing; Gaussian smoothing may shift narrow peaks slightly depending on window width.
- Signal-to-noise ratio (SNR) improves after smoothing; verify no artificial peak splitting or merging artifacts are introduced by comparing peak count before and after.
- Downstream peak picking results differ predictably: more peaks detected in Savitzky-Golay output (sharper peaks easier to identify); fewer, broader peaks in Gaussian output due to smoothing artifacts.

## Limitations

- Savitzky-Golay smoothing quality depends critically on window length and polynomial order; suboptimal parameters can distort peak shape or amplify noise at spectrum edges.
- Gaussian smoothing always broadens peaks; if original spectrum has overlapping narrow peaks, Gaussian smoothing will merge them, rendering separation impossible.
- Both methods are queued operations in Cardinal 3.6 and must be processed (not just previewed) before the actual smoothed data is written to disk or returned for analysis.
- Comparison workflow requires manual visual inspection or custom code to compute SNR and peak metrics; no automated decision criterion is provided by the smooth() function.
- Smoothing parameters (window, polynomial order, kernel width) are not automatically optimized; user must test multiple parameter values to find the best tradeoff for their specific mass range and peak widths.

## Evidence

- [other] smooth() function queues smoothing and supports both Gaussian and sgolay methods: "The smooth() function queues smoothing operations on MSImagingArrays objects and supports both Gaussian and Savitzky-Golay (sgolay) methods."
- [other] Chaining and preview workflow: "Both methods can be chained with plot() to preview results before processing, with parameters xlim to control the mass range and linewidth to adjust visualization."
- [intro] Savitzky-Golay among new smoothing methods in Cardinal 3.6: "New spectral processing methods in smooth(): Improved Gaussian filtering, Bilateral and adaptive bilateral filtering, Nonlinear diffusion filtering, Guided filtering, Peak-aware guided filtering,"
- [other] Workflow for generating comparison figures: "Produce a figure or table showing the original spectrum overlaid with both Savitzky-Golay and Gaussian smoothed results to highlight differences in peak preservation and noise reduction."
- [readme] Cardinal installation and library loading: "Once installed, *Cardinal* can be loaded with `library()`: ```{r library, eval=FALSE} library(Cardinal) ```"
