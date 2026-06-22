---
name: savitzky-golay-filter-application
description: Use when apply Savitzky-Golay smoothing when your mass spectra contain significant noise but you need to preserve sharp peaks and spectral fine structure (e.g., isotope patterns, peak asymmetry).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  tools:
  - Cardinal
  - R
  - CardinalIO
  - Cardinal 3.6
  - matter 2.4 / 2.6
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

# savitzky-golay-filter-application

## Summary

Apply Savitzky-Golay (sgolay) spectral smoothing to mass spectra in Cardinal 3.6 to reduce noise while preserving peak shape and intensity. This method is particularly valuable when fine spectral features and peak fidelity must be maintained during pre-processing of MSImagingArrays objects.

## When to use

Apply Savitzky-Golay smoothing when your mass spectra contain significant noise but you need to preserve sharp peaks and spectral fine structure (e.g., isotope patterns, peak asymmetry). Use this instead of Gaussian smoothing when peak preservation is critical and you want polynomial-weighted local averaging. Ideal for pre-processing continuous imzML mass spectrometry imaging data where spectral detail informs downstream statistical analysis.

## When NOT to use

- Spectra already heavily smoothed or baseline-corrected; re-smoothing risks loss of legitimate spectral features.
- Very sparse spectra or spectra with extremely isolated peaks where local polynomial fitting may distort peak shape.
- Data where you need to preserve all sub-peak structure unmodified (e.g., high-resolution isotope patterns requiring no pre-smoothing).

## Inputs

- MSImagingArrays object with spectral data
- mass spectra (continuous or discrete m/z values)
- imzML file (continuous format)

## Outputs

- Smoothed MSImagingArrays or MSImagingExperiment object
- Queued spectral processing operation (pre-execution)
- Visualization (spectrum plot with xlim and linewidth parameters)

## How to apply

Load the Cardinal library and construct or import an MSImagingArrays object containing raw spectral data. Queue the Savitzky-Golay smoothing operation using smooth(method="sgolay") with default window and polynomial parameters (typically a small window size like 5–11 points and polynomial order 2–3). Chain the operation with plot() and xlim parameters to visualize the smoothed spectrum on a specific mass range before execution. Compare results side-by-side with alternative smoothing (e.g., Gaussian via smooth(method="gaussian")) to confirm peak preservation. Execute the queued operation and validate that noise is reduced, peak heights and positions remain stable, and no artificial spectral features are introduced.

## Related tools

- **Cardinal** (Primary framework providing smooth() function with sgolay method for queuing and executing Savitzky-Golay spectral smoothing on MSImagingArrays and MSImagingExperiment objects.) — github.com/kuwisdelu/Cardinal
- **Cardinal 3.6** (Major update containing redesigned class hierarchy (MSImagingArrays, MSImagingExperiment) and new low-level signal processing functions including improved Savitzky-Golay filtering.) — github.com/kuwisdelu/Cardinal
- **matter 2.4 / 2.6** (Underlying low-level signal processing engine supporting efficient spectral operations in Cardinal 3.6, including Savitzky-Golay and other filtering methods.)
- **BiocParallel** (Optional package enabling parallel execution of smoothing operations across multiple spectra when BPPARAM option is supplied.)
- **CardinalIO** (Companion package providing readMSIData() and example imzML files for importing mass spectrometry imaging data before smoothing.)

## Examples

```
library(Cardinal); obj <- readMSIData(path_continuous); obj |> smooth(method="sgolay") |> plot(xlim=c(800, 1200), linewidth=1)
```

## Evaluation signals

- Smoothed spectra show reduced noise variance while preserving peak m/z positions (validate via comparison table or overlay plot with original).
- Peak heights and widths remain stable or change predictably with window size; no artificial peak splitting or migration.
- Side-by-side comparison with Gaussian smoothing shows superior peak sharpness and detail retention in sgolay output.
- Queued operation executes without errors and produces valid MSImagingArrays/Experiment object; downstream statistical analysis (PCA, clustering) runs unchanged.
- Visual inspection of smooth() preview (using plot() + xlim) confirms noise suppression across the mass range without introducing spurious spectral features.

## Limitations

- Savitzky-Golay smoothing is a local polynomial approximation; very large window sizes can over-smooth and lose spectral detail; window must be odd and smaller than spectrum length.
- Default polynomial order (typically 2–3) may be suboptimal for complex peak shapes or very noisy data; manual tuning may be required.
- Smoothing is queued (lazy evaluation) in Cardinal 3.6; actual computation deferred until execution, which may obscure parameter mistakes until runtime.
- No changelog provided for Cardinal 3.6; behavior differences from prior versions (e.g., 3.5) not formally documented in the vignette.

## Evidence

- [other] smooth() function queues smoothing operations and supports both Gaussian and Savitzky-Golay (sgolay) methods: "The smooth() function queues smoothing operations on MSImagingArrays objects and supports both Gaussian and Savitzky-Golay (sgolay) methods."
- [other] Parameters and chaining with plot() for preview before processing: "Both methods can be chained with plot() to preview results before processing, with parameters xlim to control the mass range and linewidth to adjust visualization."
- [intro] Savitzky-Golay method listed among new spectral processing methods: "New spectral processing methods in smooth(): Improved Gaussian filtering, Bilateral and adaptive bilateral filtering, Nonlinear diffusion filtering, Guided filtering, Peak-aware guided filtering,"
- [intro] MSImagingArrays class for representing raw spectra: "Updated MSImagingExperiment class with a new counterpart MSImagingArrays class for better representing raw spectra"
- [intro] Parallel processing support via BiocParallel for all pre-processing methods: "Parallel processing support via the BiocParallel package for all pre-processing methods and any statistical analysis methods with a BPPARAM option"
- [other] Comparison of Savitzky-Golay and Gaussian smoothing for peak preservation: "How does Savitzky-Golay smoothing differ from Gaussian smoothing when applied to mass spectra in Cardinal 3.6?"
