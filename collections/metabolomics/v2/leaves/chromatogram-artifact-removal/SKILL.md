---
name: chromatogram-artifact-removal
description: Use when raw NetCDF-format GCxGC-MS chromatograms exhibit steady or increasing
  baseline intensity caused by instrumental contamination, column bleeding, or thermal
  drift;
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
  tools:
  - RGCxGC
  - R
  techniques:
  - GC-MS
  license_tier: restricted
derived_from:
- doi: 10.1016/j.microc.2020.104830
  title: RGCxGC
- doi: 10.1371/journal.pntd.0006215
  title: ''
evidence_spans:
- The goal of RGCxGC is to provide an easy-to-use platform to analyze two-dimensional
  gas chromatography data.
- This is the vignette to explain the implementation of RGCxGC package.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_rgcxgc_cq
    doi: 10.1016/j.microc.2020.104830
    title: RGCxGC
  dedup_kept_from: coll_rgcxgc_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1016/j.microc.2020.104830
  all_source_dois:
  - 10.1016/j.microc.2020.104830
  - 10.1371/journal.pntd.0006215
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# chromatogram-artifact-removal

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Remove instrumental noise and baseline drift from 2D-TIC (two-dimensional Total Intensity Chromatogram) GCxGC-MS data using asymmetric least squares baseline correction and Whittaker smoothing to enhance signal quality and reveal metabolite differences. This preprocessing step is essential before peak alignment and multivariate analysis.

## When to use

Raw NetCDF-format GCxGC-MS chromatograms exhibit steady or increasing baseline intensity caused by instrumental contamination, column bleeding, or thermal drift; smoothing and baseline correction are needed before peak alignment (2DCOW) to avoid alignment artifacts and to improve the signal-to-noise ratio for downstream multivariate analysis (MPCA).

## When NOT to use

- Input is already baseline-corrected or has been manually pre-processed by external software — applying baseline_corr redundantly may distort true metabolite signals.
- The 2D chromatogram is from a non-GCxGC instrument or is stored in a format other than NetCDF (e.g., vendor-specific binary formats not imported via read_chrom).
- Analysis goal is only qualitative identification of major peaks; baseline correction introduces algorithmic assumptions that may not be justified for single-sample exploratory work.

## Inputs

- 2D-TIC chromatogram object (output from read_chrom function, derived from NetCDF file)

## Outputs

- Baseline-corrected and smoothed 2D-TIC chromatogram object
- Preprocessed chromatogram ready for peak alignment and multivariate analysis

## How to apply

After importing and folding the raw chromatogram into 2D-TIC using read_chrom, apply smoothing first using the wsmooth function with the Whittaker smoother algorithm to attenuate high-frequency chemical and instrumental noise. Then apply baseline_corr using the asymmetric least squares algorithm to remove the slowly-varying baseline component. The asymmetric least squares method uses differential penalties for positive and negative residuals, allowing it to preserve sharp metabolite peaks while suppressing baseline undulation. Order matters: smoothing before baseline correction prevents the correction step from over-fitting to noise. Visually inspect the corrected 2D-TIC to confirm that baseline distortion is removed without peak attenuation and that the separation space now contains more intense, well-resolved signals.

## Related tools

- **RGCxGC** (Provides baseline_corr function (asymmetric least squares baseline correction) and wsmooth function (Whittaker smoothing) for 2D-TIC artifact removal) — https://github.com/DanielQuiroz97/RGCxGC
- **R** (Execution environment for RGCxGC package functions)

## Examples

```
baseline_corr(chrom_obj, lambda=100, p=0.001); wsmooth(chrom_obj, lambda=100)
```

## Evaluation signals

- Visual inspection of the baseline-corrected 2D chromatogram shows a flat, near-zero baseline with no increasing or oscillating drift.
- Peak intensities in the separation space are increased relative to the baseline (higher signal-to-noise ratio) compared to the raw chromatogram.
- Peaks remain sharp and well-resolved; no significant broadening or distortion is visible after smoothing and baseline correction.
- Downstream peak alignment (2DCOW) produces fewer alignment artifacts and higher alignment scores when applied to preprocessed chromatograms versus raw data.
- Multivariate analysis (MPCA) on corrected chromatograms reveals clearer group separation and higher explained variance in the first few components compared to unprocessed data.

## Limitations

- Asymmetric least squares baseline correction assumes baseline distortion is smooth and slowly-varying; sharp instrumental spikes or hot-spot contamination may not be fully removed.
- The choice of smoothing strength (lambda parameter in Whittaker smoother) and baseline correction asymmetry (p parameter in asymmetric least squares) can impact peak shape and quantification; no universal defaults are described in the article.
- Over-smoothing can eliminate low-intensity or poorly-resolved metabolite peaks; under-smoothing leaves residual noise that degrades alignment and multivariate analysis.
- Baseline correction is data-dependent and may not perform equally well across all retention time regions if baseline behavior varies locally.

## Evidence

- [other] baseline_corr function using asymmetric least squares remove baseline distortion from a 2D-TIC chromatogram: "The baseline_corr function applies the asymmetric least squares algorithm to remove steady and increasing intensity from 2D-TIC chromatograms caused by instrumental contamination or column bleeding"
- [intro] RGCxGC offers preprocessing algorithms including baseline correction and smoothing: "RGCxGC offers common pre-processing algorithms for signal enhancement, such as baseline correction based on asymetric least squares, smoothing based on the Whittaker smoother"
- [intro] Preprocessing steps reduce noise and enable multivariate analysis: "noise can be significantly reduced by using preprocessing algorithms, herein smoothing, baseline correction, and peak alignment. Then, in order to reveal differences between groups, multivariate"
- [intro] workflow order: first read_chrom, then apply wsmooth and baseline_corr: "you can perform preprocessing routines like smoothing and/or baseline correction by using the function wsmooth and baseline_corr"
- [readme] Raw chromatographic signals contain undesirable artifacts requiring preprocessing: "Raw chromatographic signals usually contains undesirable artifacts, such as chemical and"
