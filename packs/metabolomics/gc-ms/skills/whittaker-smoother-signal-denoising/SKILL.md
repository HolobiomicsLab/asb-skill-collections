---
name: whittaker-smoother-signal-denoising
description: Use when after baseline correction (e.g., via asymmetric least squares) when raw GCxGC-MS chromatograms still contain high-frequency noise that obscures true signal structure. Use it when you need to reduce noise before peak alignment or multivariate analysis (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3563
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
  tools:
  - RGCxGC
  - R
  - baseline_corr
  techniques:
  - LC-MS
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

# whittaker-smoother-signal-denoising

## Summary

Apply the Whittaker smoother algorithm to baseline-corrected GCxGC-MS chromatograms to reduce instrumental and chemical noise while preserving peak shapes. The algorithm uses a user-specified penalty order and smoothing factor (lambda) to balance fidelity to the observed signal against smoothness.

## When to use

Apply this skill after baseline correction (e.g., via asymmetric least squares) when raw GCxGC-MS chromatograms still contain high-frequency noise that obscures true signal structure. Use it when you need to reduce noise before peak alignment or multivariate analysis (e.g., MPCA) without distorting peak positions or intensities required for biomarker discovery.

## When NOT to use

- Input chromatogram has not yet undergone baseline correction; apply baseline_corr first.
- Chromatogram is already heavily preprocessed or has missing/corrupted intensity regions; verify data integrity before smoothing.
- Analysis requires peak intensity values to match raw detector signal exactly (e.g., for absolute quantification without calibration); smoothing introduces systematic bias in intensities.

## Inputs

- baseline-corrected chromatogram object (class chromatogram from RGCxGC, typically output from baseline_corr function)
- Whittaker smoother algorithm specification (penalty order: integer, e.g., 2 for quadratic)
- lambda smoothing parameter (numeric, e.g., 10)

## Outputs

- smoothed chromatogram object (class chromatogram, ready for peak alignment or MPCA)

## How to apply

Load a baseline-corrected chromatogram object (output from baseline_corr function) into R/RGCxGC. Call the wsmooth function, specifying the Whittaker smoother algorithm with penalty=2 (quadratic penalty) and an appropriate lambda value (e.g., lambda=10); larger lambda values produce stronger smoothing and more influence on the penalty term. The function iteratively minimizes a penalized least-squares criterion balancing fit to observed intensities against the roughness penalty. Examine the smoothed chromatogram visually to verify that peaks remain distinct and well-defined; if over-smoothing occurs (peaks flattened or merged), reduce lambda. Store the resulting smoothed chromatogram object for downstream peak alignment or feature extraction.

## Related tools

- **RGCxGC** (R package implementing wsmooth function for Whittaker smoothing of 2D chromatograms) — https://github.com/DanielQuiroz97/RGCxGC
- **R** (Programming environment and runtime for executing wsmooth and RGCxGC workflows)
- **baseline_corr** (RGCxGC function that must be run prior to smoothing to remove baseline drift) — https://github.com/DanielQuiroz97/RGCxGC

## Examples

```
library(RGCxGC); MTBLS08_bc <- baseline_corr(MTBLS08); MTBLS08_sm2 <- wsmooth(MTBLS08_bc, method='whittaker', penalty=2, lambda=10)
```

## Evaluation signals

- Smoothed chromatogram object is created and stored in memory without error; object class and structure match input chromatogram.
- Peak signal-to-noise ratio (SNR) visibly improves in the smoothed chromatogram compared to baseline-corrected input; high-frequency noise is attenuated while peak maxima and shapes are preserved.
- Downstream peak alignment (2DCOW) or MPCA runs successfully on the smoothed chromatogram without convergence warnings.
- Lambda parameter sensitivity check: reducing lambda should produce noisier output; increasing lambda should produce smoother output. Choice of lambda=10 (or user-specified value) should not over-smooth and merge adjacent peaks.
- Smoothed intensities remain physically plausible (non-negative, within observed detector range); no anomalies or artifacts introduced by the algorithm.

## Limitations

- Whittaker smoother performance depends critically on lambda selection; no automated method is provided in RGCxGC to choose lambda, and user must rely on visual inspection or cross-validation.
- Smoothing applies a global penalty across the entire chromatogram; regions with genuinely low signal may be over-smoothed, while high-noise regions may remain under-smoothed if a single lambda is used.
- Algorithm assumes underlying signal is smooth; very sharp, narrow peaks may be slightly broadened or attenuated depending on penalty order and lambda.
- Penalty order (e.g., penalty=2) is fixed by the user; the paper/README do not discuss how to choose penalty order for different chromatographic scenarios (e.g., GCxGC vs. liquid chromatography).

## Evidence

- [intro] Whittaker smoother algorithm application: "you can perform preprocessing routines like smoothing and/or baseline correction by using the function wsmooth and baseline_corr"
- [other] Penalty and lambda parameters: "Apply wsmooth function with Whittaker smoother algorithm, setting penalty parameter to 2 and lambda parameter to 10"
- [other] Lambda effect on smoothing strength: "greater lambda values have stronger influence on the smoothing process"
- [intro] Noise reduction role in preprocessing: "noise can be significantly reduced by using preprocessing algorithms, herein smoothing, baseline correction, and peak alignment"
- [readme] Algorithm citation and theoretical basis: "smoothing based on the Whittaker smoother. Furthermore, the multiway principal component analysis is implemented"
- [other] Downstream workflow context: "Store the resulting smoothed chromatogram object in memory for downstream peak alignment or multivariate analysis steps"
