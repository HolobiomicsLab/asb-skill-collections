---
name: gcxgc-chromatogram-object-manipulation
description: Use when you have raw GCxGC-MS data in NetCDF format that contains instrumental
  and chemical noise (baseline drift, high-frequency signal artifacts) and you need
  to prepare multiple preprocessed chromatogram objects for downstream multiway PCA
  or biomarker discovery.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3173
  tools:
  - RGCxGC
  - R
  - mixOmics
  - colorRamps
  techniques:
  - LC-MS
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

# GCxGC Chromatogram Object Manipulation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Load, preprocess, and transform two-dimensional gas chromatography-mass spectrometry (GCxGC-MS) chromatogram objects through a sequence of signal enhancement and alignment operations in R using the RGCxGC package. This skill chains baseline correction, smoothing, peak alignment, and object joining to prepare raw NetCDF chromatogram data for multivariate analysis.

## When to use

Apply this skill when you have raw GCxGC-MS data in NetCDF format that contains instrumental and chemical noise (baseline drift, high-frequency signal artifacts) and you need to prepare multiple preprocessed chromatogram objects for downstream multiway PCA or biomarker discovery. Use it when samples require both noise reduction (via smoothing and baseline correction) and inter-sample alignment before group-level multivariate analysis.

## When NOT to use

- Input is already a feature matrix or peak table; chromatogram object manipulation is for signal preprocessing, not post-extraction analysis.
- Data is from a different chromatography modality (e.g., 1D GC-MS, HPLC) without 2D structure; RGCxGC is designed for two-dimensional GC data.
- Raw data is not in NetCDF format or cannot be folded into a 2D-TIC object; read_chrom requires compatible structured chromatogram input.

## Inputs

- Raw chromatogram NetCDF file
- Chromatogram object (folded 2D-TIC from read_chrom)
- Baseline-corrected chromatogram object (output from baseline_corr)

## Outputs

- Smoothed chromatogram object (output from wsmooth)
- Baseline-corrected chromatogram object (output from baseline_corr)
- Aligned chromatogram object (output from twod_cow or batch_2DCOW)
- Joined multi-sample chromatogram container (output from join_chromatograms)

## How to apply

Begin by importing the raw NetCDF chromatogram and folding it into a two-dimensional Total Intensity Chromatogram (2D-TIC) object using read_chrom. Apply baseline correction using the asymmetric least squares algorithm via baseline_corr to remove baseline drift and low-frequency artifacts. Next, apply the Whittaker smoother algorithm via wsmooth with a quadratic penalty (penalty=2) and user-specified lambda smoothing factor (e.g., lambda=10); larger lambda values increase smoothing strength. Align preprocessed chromatograms against a reference sample using the 2D correlation optimized warping (2DCOW) algorithm via twod_cow or batch_2DCOW for multiple samples. Finally, combine all aligned chromatogram objects into a single R container using join_chromatograms to prepare for multiway PCA. The rationale is that each preprocessing step (baseline removal, then smoothing, then alignment) progressively reduces noise while preserving metabolite signal intensity differences needed to reveal biological group differences.

## Related tools

- **RGCxGC** (R package providing read_chrom, baseline_corr, wsmooth, twod_cow, batch_2DCOW, join_chromatograms, and m_prcomp functions for complete GCxGC preprocessing and multiway PCA pipeline) — https://github.com/DanielQuiroz97/RGCxGC
- **mixOmics** (Provides supervised multivariate model functions for downstream analysis after chromatogram preprocessing and MPCA)
- **colorRamps** (Supplies color palettes (matlab.like, matlab.like2) for visualization of preprocessed chromatogram matrices and MPCA results)

## Examples

```
MTBLS08_bc <- baseline_corr(MTBLS08_tic); MTBLS08_sm2 <- wsmooth(MTBLS08_bc, penalty=2, lambda=10); MTBLS08_aligned <- batch_2DCOW(MTBLS08_sm2, reference=ref_sample); MTBLS08_joined <- join_chromatograms(MTBLS08_aligned)
```

## Evaluation signals

- Baseline-corrected chromatogram object shows reduced baseline drift while retaining peak signal intensity; compare raw vs. corrected 2D-TIC visually or by examining intensity distributions.
- Smoothed chromatogram exhibits reduced high-frequency noise without over-smoothing metabolite peaks; verify by checking that peak maxima are preserved and signal-to-noise ratio improves.
- Aligned chromatograms from batch_2DCOW show consistent peak positions across samples (minimal warping artifacts) and reduced inter-sample retention time drift.
- Joined chromatogram container structure is compatible with m_prcomp input; confirm by successfully invoking m_prcomp on the joined object without dimension or schema errors.
- Lambda and penalty parameters are recorded with preprocessed objects; confirm that wsmooth parameters (penalty=2, lambda value) are documented or retrievable from the output object metadata.

## Limitations

- The Whittaker smoother strength is controlled by lambda; very high lambda values (e.g., >100) may over-smooth and attenuate true metabolite peaks, while very low lambda values (<1) may leave residual noise.
- 2D COW alignment requires selection of a reference chromatogram; poor reference choice (e.g., noisy or atypical sample) can misalign the entire cohort and degrade downstream multivariate analysis.
- Preprocessing order matters: baseline correction should precede smoothing; reversing this order may introduce artifacts or fail to remove baseline properly.
- RGCxGC is optimized for GCxGC-MS data in NetCDF format; compatibility with other chromatography formats or file types is not guaranteed.

## Evidence

- [intro] Read chromatogram import and folding: "first, the raw chromatogram is importing from a NetCDF file and is folded into the two-dimensional Total Intensity Chromatogram (2D-TIC)."
- [intro] Whittaker smoother algorithm application: "you can perform preprocessing routines like smoothing and/or baseline correction by using the function wsmooth and baseline_corr"
- [other] Lambda parameter effect on smoothing: "The wsmooth function applies the Whittaker smoother algorithm with user-specified penalty order (2 for quadratic) and lambda smoothing factor (10) to a baseline-corrected chromatogram object"
- [intro] Peak alignment using 2D COW: "peak alignment of a single sample against a reference chromatogram can be performed based on the two-dimensional correlation optimized warping (2DCOW) algorithm. Alternatively, multiple sample"
- [intro] Joining preprocessed chromatograms: "Once the chromatograms are already preprocessed, it has to be in a single R object. To meet this requirement, the join_chromatograms functions does it."
- [intro] Baseline correction and smoothing reduce noise: "noise can be significantly reduced by using preprocessing algorithms, herein smoothing, baseline correction, and peak alignment. Then, in order to reveal differences between groups, multivariate"
- [readme] RGCxGC README baseline and smoothing algorithms: "RGCxGC offers common pre-processing algorithms for signal enhancement, such as baseline correction based on asymetric least squares, smoothing based on the Whittaker smoother, and peak alignment 2D"
