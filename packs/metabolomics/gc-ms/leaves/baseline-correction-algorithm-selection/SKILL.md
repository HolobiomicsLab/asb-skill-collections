---
name: baseline-correction-algorithm-selection
description: Use when when you have imported a raw GCxGC-MS chromatogram as a 2D-TIC (2D Total Intensity Chromatogram) object from a NetCDF file and observe steady or increasing baseline intensity caused by instrumental contamination, column bleeding, or thermal drift.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - RGCxGC
  - R
  techniques:
  - GC-MS
derived_from:
- doi: 10.1016/j.microc.2020.104830
  title: RGCxGC
- doi: 10.1371/journal.pntd.0006215
  title: ''
evidence_spans:
- The goal of RGCxGC is to provide an easy-to-use platform to analyze two-dimensional gas chromatography data.
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

# Baseline Correction Algorithm Selection

## Summary

Selecting and applying an appropriate baseline correction algorithm to remove instrumental drift, column bleeding, and chemical noise from raw GCxGC-MS chromatographic signals. This skill determines which baseline correction approach (e.g., asymmetric least squares) best suits the noise characteristics and intensity profile of the 2D-TIC chromatogram before downstream preprocessing and multivariate analysis.

## When to use

When you have imported a raw GCxGC-MS chromatogram as a 2D-TIC (2D Total Intensity Chromatogram) object from a NetCDF file and observe steady or increasing baseline intensity caused by instrumental contamination, column bleeding, or thermal drift. Apply this skill before smoothing and peak alignment when baseline distortion would otherwise obscure weak metabolite signals needed for biomarker discovery or diagnostic classification.

## When NOT to use

- Input chromatogram has already been baseline-corrected by the instrument software or a prior preprocessing step; re-correction risks signal loss or artifact introduction.
- Baseline distortion is highly localized (e.g., single large contaminant peak) rather than systematic drift; targeted peak removal or manual artifact annotation may be more appropriate.
- Analysis goal requires absolute intensity quantification where baseline shape and height carry chemical meaning; baseline flattening would destroy that information.

## Inputs

- 2D-TIC chromatogram object (output from read_chrom function; imported from NetCDF raw data)
- Raw GCxGC-MS signal with baseline distortion (steady, increasing, or drifting intensity)

## Outputs

- Baseline-corrected 2D-TIC chromatogram object (flatter baseline, preserved peak intensity)
- Signal-to-noise improved chromatographic image ready for smoothing and alignment

## How to apply

First, inspect the raw 2D-TIC chromatogram for visual signatures of baseline distortion: steady background intensity, monotonic intensity increase along the first or second dimension, or elevated signal at column or detector edges. For GCxGC-MS metabolomics data with steady or increasing baseline, apply the asymmetric least squares algorithm via the baseline_corr function in RGCxGC. Asymmetric least squares is preferred because it penalizes positive deviations (signal peaks) more heavily than negative deviations (baseline), preserving peak shape and intensity while flattening the baseline. The algorithm iteratively re-weights residuals to separate baseline from signal. Verify correction by comparing the baseline-corrected 2D-TIC histogram or intensity profile to the raw chromatogram: the corrected chromatogram should show a flatter, near-zero baseline with retained or enhanced peak definition. Baseline correction is necessary before smoothing and peak alignment because these downstream steps assume a stable baseline.

## Related tools

- **RGCxGC** (Provides baseline_corr function implementing asymmetric least squares algorithm for 2D-TIC baseline correction) — https://github.com/DanielQuiroz97/RGCxGC
- **R** (Runtime environment and package management for executing RGCxGC baseline correction workflow)

## Examples

```
baseline_corr(chromatogram_object, method = 'als', lambda = 1e5, p = 0.01)
```

## Evaluation signals

- Baseline intensity in the corrected 2D-TIC is visibly flattened and near zero across the retention time space, compared to the raw chromatogram.
- Peak heights and widths are preserved or enhanced in the baseline-corrected chromatogram; no spurious peak shrinkage or broadening.
- Histogram or intensity profile of the baseline-corrected 2D-TIC shows a left-skewed (noise-dominated) distribution rather than the right-skewed (baseline-dominated) distribution of the raw chromatogram.
- Downstream smoothing (Whittaker) and peak alignment (2DCOW) operations produce cleaner, more reproducible results when applied to baseline-corrected vs. raw chromatograms.
- Multivariate analysis (MPCA) of baseline-corrected chromatograms reveals stronger separation between diagnostic groups (e.g., chronic typhoid carriers vs. controls) than analysis of raw or inadequately corrected data.

## Limitations

- Asymmetric least squares assumes baseline distortion is smooth and monotonic; highly nonlinear or multi-modal baseline artifacts may require parameter tuning (asymmetry factor) or alternative algorithms.
- Correction quality depends on choosing appropriate regularization and asymmetry parameters; no universal default exists across all GCxGC-MS instruments or sample types.
- Over-correction can remove weak, broad signal components (e.g., low-abundance metabolites with extended elution profiles) if the algorithm misclassifies them as baseline.
- The algorithm is computationally intensive for large 2D chromatographic matrices; processing time scales with chromatogram resolution and number of samples.

## Evidence

- [intro] Raw chromatographic signals usually contains undesirable artifacts, such as chemical and instrumental noise: "Raw chromatographic signals usually contains undesirable artifacts, such as chemical and"
- [other] Baseline correction based on asymmetric least squares removes steady and increasing intensity from 2D-TIC chromatograms: "The baseline_corr function applies the asymmetric least squares algorithm to remove steady and increasing intensity from 2D-TIC chromatograms caused by instrumental contamination or column bleeding"
- [intro] Baseline correction is applied after import and folding of raw chromatogram into 2D-TIC: "first, the raw chromatogram is importing from a NetCDF file and is folded into the two-dimensional Total Intensity Chromatogram (2D-TIC)."
- [intro] Preprocessing with baseline correction and smoothing reduces noise and reveals differences between groups: "noise can be significantly reduced by using preprocessing algorithms, herein smoothing, baseline correction, and peak alignment. Then, in order to reveal differences between groups, multivariate"
- [readme] Asymmetric least squares is a validated algorithm for baseline correction in GCxGC-MS: "RGCxGC offers common pre-processing algorithms for signal enhancement, such as baseline correction based on asymetric least squares"
