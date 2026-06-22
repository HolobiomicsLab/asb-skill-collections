---
name: queued-spectrum-preview-generation
description: Use when when you have queued one or more spectral processing operations (e.g., smooth(), normalize(), reduceBaseline()) on an MSImagingArrays object and need to inspect the effect on representative spectra before processing the full dataset.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  tools:
  - Cardinal
  - R
  - CardinalIO
  - Cardinal 3.6
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

# queued-spectrum-preview-generation

## Summary

Generate previews of queued spectral processing operations on MSImagingArrays objects in Cardinal 3.6 before committing them to disk. This skill enables side-by-side comparison of different smoothing or preprocessing methods to validate parameter choices and assess peak preservation and noise reduction before applying operations to large imaging datasets.

## When to use

When you have queued one or more spectral processing operations (e.g., smooth(), normalize(), reduceBaseline()) on an MSImagingArrays object and need to inspect the effect on representative spectra before processing the full dataset. This is especially useful when comparing competing preprocessing strategies (e.g., Savitzky-Golay vs. Gaussian smoothing) or tuning algorithm parameters (window size, polynomial degree, noise thresholds) to assess peak preservation and noise reduction.

## When NOT to use

- Spectra have already been processed and extracted; queuing and preview are only meaningful on unprocessed MSImagingArrays objects.
- Dataset is too small to benefit from non-destructive preview (i.e., when reprocessing is fast enough that immediate application is preferable).
- Preprocessing parameters are already validated and fixed by protocol; preview adds no decision value.

## Inputs

- MSImagingArrays object with spectral data loaded
- One or more queued spectral processing operations (e.g., from smooth(), normalize(), reduceBaseline())

## Outputs

- Preview plot or static visualization overlaying original and processed spectra
- Visual assessment of peak morphology, noise levels, and parameter effect
- Confidence in queued operation parameters prior to full-dataset processing

## How to apply

After queuing one or more preprocessing operations on an MSImagingArrays object using methods like smooth(method='sgolay') or smooth(method='gaussian'), chain the plot() function to generate an interactive or static preview of the result. Use the xlim parameter to focus on a mass range of interest and linewidth to adjust visualization clarity. Generate overlaid plots of the original spectrum and each queued operation to compare morphological differences. Inspect the preview to evaluate whether peaks are preserved, noise is adequately reduced, and parameter choices are appropriate before calling process() or $ to commit operations. If the preview reveals inadequate results (e.g., excessive peak broadening or insufficient noise suppression), modify the queued operation parameters and regenerate the preview without reprocessing the full dataset.

## Related tools

- **Cardinal 3.6** (MSI preprocessing framework providing smooth(), normalize(), reduceBaseline() methods and queuing architecture; plot() method for preview generation) — https://github.com/kuwisdelu/Cardinal
- **R** (Runtime environment for Cardinal library and visualization (plot))
- **BiocParallel** (Optional: enables parallel processing of preview or full-dataset processing via BPPARAM option)

## Examples

```
library(Cardinal); msi <- readMSIData('data.imzML'); msi_sgolay <- smooth(msi, method='sgolay'); msi_gaussian <- smooth(msi, method='gaussian'); plot(msi_sgolay, xlim=c(800, 1200), linewidth=1.5); plot(msi_gaussian, xlim=c(800, 1200), linewidth=1.5)
```

## Evaluation signals

- Preview plot is generated without error and displays both original and processed spectra on the same axes.
- Visual inspection confirms that peaks are preserved or appropriately broadened/sharpened depending on the smoothing method and parameters.
- Noise level reduction is visually apparent in the preview (e.g., baseline fluctuations reduced) relative to the original spectrum.
- Xlim and linewidth parameters correctly constrain the mass range displayed and improve readability of critical features.
- Queued operations can be modified and replotted iteratively without triggering full reprocessing of the dataset, confirming the non-destructive nature of the preview.

## Limitations

- Preview is generated on a subset of spectra or a representative spectrum; behavior on rare or edge-case spectra may differ from full-dataset results.
- Preview does not account for spatial preprocessing (e.g., image-level contrast enhancement via CLAHE or spatial smoothing), which may interact with spectral preprocessing in ways not visible in isolated spectrum plots.
- No automatic validation or recommendation system for parameter tuning; user must visually interpret and judge the preview quality, which is subjective and may require domain expertise.

## Evidence

- [intro] Queuing and preview workflow demonstrated in task_002: "Queue Gaussian smoothing on the same object using smooth(method="gaussian") for comparison. 4. Generate a preview or extract smoothed spectra from both queued operations to visualize side-by-side"
- [intro] smooth() queuing architecture in Cardinal 3.6: "The smooth() function queues smoothing operations on MSImagingArrays objects and supports both Gaussian and Savitzky-Golay (sgolay) methods."
- [intro] Chaining plot() to preview results before processing: "Both methods can be chained with plot() to preview results before processing, with parameters xlim to control the mass range and linewidth to adjust visualization."
- [intro] Spectrum comparison as evaluation metric: "Produce a figure or table showing the original spectrum overlaid with both Savitzky-Golay and Gaussian smoothed results to highlight differences in peak preservation and noise reduction."
