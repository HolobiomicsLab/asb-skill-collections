---
name: chromatogram-baseline-correction-preprocessing
description: Use when you have raw or folded 2D-TIC chromatogram data (typically imported
  from NetCDF files into RGCxGC chromatogram objects) that exhibits baseline drift,
  chemical noise, or instrumental artifacts that would obscure true metabolite peaks.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
  tools:
  - RGCxGC
  - R
  techniques:
  - GC-MS
  license_tier: restricted
  provenance_tier: literature
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

# chromatogram-baseline-correction-preprocessing

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Remove instrumental baseline drift and chemical noise from GCxGC-MS chromatograms using asymmetric least squares (ALS) algorithm to enhance signal clarity and enable downstream peak alignment and multivariate analysis. This is a critical preprocessing step that must precede smoothing and peak alignment in comprehensive two-dimensional gas chromatography workflows.

## When to use

Apply this skill when you have raw or folded 2D-TIC chromatogram data (typically imported from NetCDF files into RGCxGC chromatogram objects) that exhibits baseline drift, chemical noise, or instrumental artifacts that would obscure true metabolite peaks. Use it before smoothing and peak alignment, and when your downstream analysis requires clean peak detection or multiway principal component analysis (MPCA) on GCxGC-MS data.

## When NOT to use

- Input chromatogram is already baseline-corrected (e.g., by instrument software or a prior preprocessing step); reapplication may remove true signal.
- Analysis goal is peak detection on already-processed feature tables or extracted peak lists; baseline correction applies only to raw chromatographic intensity matrices.
- Data is 1D chromatography or mass spectra without a 2D structure; this skill is specific to comprehensive 2D chromatography (GCxGC) workflows.

## Inputs

- raw chromatogram object imported from NetCDF file (2D-TIC format)
- baseline-uncorrected chromatogram R object (MTBLS08 or similar GCxGC-MS data)

## Outputs

- baseline-corrected chromatogram object (MTBLS08_bc or equivalent)
- cleaned 2D-TIC with reduced instrumental and chemical noise

## How to apply

Load the baseline-corrected chromatogram object (typically output from read_chrom or a prior import step) into the baseline_corr function, which applies the asymmetric least squares (ALS) algorithm to adaptively estimate and subtract the baseline while preserving true peaks. The ALS algorithm uses an iterative weighted least squares fit with asymmetric penalties—penalizing deviations above the fitted curve more heavily than below—to distinguish instrumental drift from authentic signal. After baseline correction, the resulting cleaned chromatogram object can be used for downstream smoothing with wsmooth, peak alignment with 2DCOW, or direct multiway PCA. Monitor correction quality by visual inspection of the 2D chromatogram before and after, ensuring peaks remain sharp while background is flattened.

## Related tools

- **RGCxGC** (R package providing baseline_corr function that implements asymmetric least squares baseline correction for 2D-TIC chromatogram objects) — https://github.com/DanielQuiroz97/RGCxGC
- **R** (Programming environment in which baseline_corr function is executed and chromatogram objects are manipulated)

## Examples

```
MTBLS08_bc <- baseline_corr(MTBLS08)
```

## Evaluation signals

- Visual inspection: baseline-corrected 2D chromatogram shows flattened background while peak intensities and shapes are preserved compared to raw input
- Peak signal-to-noise ratio increases post-correction (measurable via peak height or area relative to background variance)
- Downstream peak alignment (2DCOW) produces higher correlation scores between corrected sample chromatograms and reference
- MPCA loadings and scores are more interpretable and show stronger metabolite discrimination after baseline correction than on uncorrected data
- No systematic offset or positive baseline remains in the corrected chromatogram; minimum intensity values should be near zero

## Limitations

- ALS algorithm parameters (iterations, penalty weights) may require tuning for different chromatography conditions or metabolite classes; no universal default provided in the article
- Baseline correction assumes the majority of the chromatogram is baseline (not peaks); if sample is extremely complex or densely populated with peaks, the algorithm may remove true signal
- Quality depends on the folding method used to construct the 2D-TIC from raw 1D traces; poor folding leads to artefactual baseline features that ALS cannot fully correct

## Evidence

- [intro] RGCxGC offers common pre-processing algorithms for signal enhancement, such as baseline correction: "RGCxGC offers common pre-processing algorithms for signal enhancement, such as baseline correction based on asymetric least squares"
- [intro] Baseline correction must precede smoothing in the workflow: "you can perform preprocessing routines like smoothing and/or baseline correction by using the function wsmooth and baseline_corr"
- [intro] Baseline correction removes undesirable artifacts from raw chromatographic signals: "Raw chromatographic signals usually contains undesirable artifacts, such as chemical and noise can be significantly reduced by using preprocessing algorithms"
- [intro] Baseline correction and smoothing reduce noise to enable group differentiation in downstream multivariate analysis: "Preprocessing steps including smoothing, baseline correction, and peak alignment can reduce noise and reveal differences between groups for multivariate analysis"
- [readme] ALS is the named algorithm used in RGCxGC for baseline correction: "baseline correction based on asymetric least squares"
