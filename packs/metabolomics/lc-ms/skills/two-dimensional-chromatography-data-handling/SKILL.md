---
name: two-dimensional-chromatography-data-handling
description: Use when you have raw GCxGC-MS chromatogram data in NetCDF format from multiple samples (e.g., case and control groups) and need to prepare them for multivariate analysis such as multiway principal component analysis (MPCA).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - RGCxGC
  - R
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# two-dimensional-chromatography-data-handling

## Summary

Import, preprocess, and align two-dimensional gas chromatography-mass spectrometry (GCxGC-MS) data from NetCDF files into a unified matrix suitable for multivariate analysis. This skill handles the complete signal enhancement pipeline—smoothing, baseline correction, and peak alignment—to reduce instrumental and chemical noise and reveal metabolite differences between sample groups.

## When to use

You have raw GCxGC-MS chromatogram data in NetCDF format from multiple samples (e.g., case and control groups) and need to prepare them for multivariate analysis such as multiway principal component analysis (MPCA). Apply this skill when raw signals contain baseline drift, high-frequency noise, or retention-time shifts that would obscure meaningful metabolite differences between groups.

## When NOT to use

- Input is already a preprocessed feature matrix or intensity table (not raw NetCDF chromatograms)—proceed directly to MPCA.
- Chromatograms are from a single technique that does not produce two-dimensional separation (e.g., 1D GC or LC-MS)—use univariate preprocessing instead.
- Data are already aligned and baseline-corrected by the instrument vendor software and you only need to combine them—use join_chromatograms alone without rerunning wsmooth or baseline_corr.

## Inputs

- Raw GCxGC-MS NetCDF file(s) containing two-dimensional chromatogram data (m/z vs. retention time)
- Multiple sample chromatograms from case and control groups
- Reference chromatogram for 2DCOW peak alignment

## Outputs

- Preprocessed 2D-TIC (two-dimensional Total Intensity Chromatogram) for each sample
- Baseline-corrected and smoothed chromatogram matrix
- Peak-aligned chromatograms
- Joined three-way array (m/z × retention time × samples) suitable for MPCA

## How to apply

Begin by importing each raw NetCDF chromatogram and folding it into a two-dimensional Total Intensity Chromatogram (2D-TIC) using the read_chrom function. Apply smoothing using the Whittaker smoother algorithm via wsmooth to reduce high-frequency instrumental noise, then perform baseline correction using the asymmetric least squares algorithm via baseline_corr to remove baseline drift. Next, align all preprocessed chromatograms to a reference sample using the 2D correlation optimized warping (2DCOW) algorithm via twod_cow or batch_2DCOW to correct retention-time shifts across the sample set. Finally, join all aligned chromatograms into a single stacked matrix using join_chromatograms, which produces a three-way array (m/z × retention time × samples) ready for MPCA. The choice of reference sample and smoother parameters (e.g., smoothness penalty in Whittaker) should be informed by visual inspection of raw signals and the magnitude of baseline variation observed.

## Related tools

- **RGCxGC** (Primary R package for reading NetCDF chromatograms, applying smoothing (wsmooth), baseline correction (baseline_corr), peak alignment (twod_cow/batch_2DCOW), and joining preprocessed chromatograms into a unified matrix.) — https://github.com/DanielQuiroz97/RGCxGC
- **R** (Statistical programming environment in which RGCxGC functions are executed.)

## Examples

```
# Load preprocessed MTBLS579 data and join into unified matrix
library(RGCxGC)
data(MTBLS579)
preprocessed_chrom <- join_chromatograms(list(chrom1_smooth_baseline, chrom2_smooth_baseline, chrom3_smooth_baseline, chrom4_smooth_baseline, chrom5_smooth_baseline, chrom6_smooth_baseline))
```

## Evaluation signals

- Successfully read and folded raw NetCDF files into 2D-TIC objects without file I/O errors; visual inspection confirms 2D chromatogram structure (m/z vs. retention time).
- After smoothing and baseline correction, baseline artefacts are visually reduced and peak signal-to-noise ratio is improved relative to raw chromatogram.
- After 2DCOW alignment, retention-time shifts are corrected and peaks from the same metabolite appear at nearly identical coordinates across samples; alignment quality can be assessed by overlay or correlation of aligned chromatograms.
- Joined output is a three-way array with dimensions matching (m/z bins × retention-time bins × number of samples); all sample chromatograms are stacked without missing values or dimension mismatches.
- The joined matrix is compatible with m_prcomp function in RGCxGC; MPCA scores can be extracted without dimension or data-type errors.

## Limitations

- The choice of reference chromatogram for 2DCOW alignment can influence downstream results; a poor reference (e.g., very noisy or atypical sample) may lead to suboptimal alignment. The article does not specify criteria for reference selection.
- Smoothing and baseline correction parameters (e.g., Whittaker smoothness penalty) are not explicitly optimized in the article; practitioners must tune these based on visual inspection or cross-validation.
- Peak alignment using 2DCOW assumes that metabolites shift retention time in a spatially smooth manner; severe localized distortions or instrument failures may not be fully corrected.
- The method is demonstrated on six chromatograms (MTBLS579 dataset); scalability to very large sample sets or highly diverse metabolite profiles is not explicitly addressed.

## Evidence

- [intro] Import and preprocessing steps: "first, the raw chromatogram is importing from a NetCDF file and is folded into the two-dimensional Total Intensity Chromatogram (2D-TIC)."
- [intro] Smoothing and baseline correction methods: "you can perform preprocessing routines like smoothing and/or baseline correction by using the function wsmooth and baseline_corr"
- [intro] Peak alignment algorithm: "peak alignment of a single sample against a reference chromatogram can be performed based on the two-dimensional correlation optimized warping (2DCOW) algorithm."
- [intro] Joining chromatograms into unified matrix: "Once the chromatograms are already preprocessed, it has to be in a single R object. To meet this requirement, the join_chromatograms functions does it."
- [readme] RGCxGC preprocessing capabilities and algorithms: "RGCxGC offers common pre-processing algorithms for signal enhancement, such as baseline correction based on asymetric least squares, smoothing based on the Whittaker smoother, and peak alignment 2D"
