---
name: chromatogram-alignment-warping
description: Use when you have baseline-corrected and smoothed 2D-TIC chromatogram objects from individual GCxGC-MS samples that exhibit retention-time variations relative to a reference chromatogram, and you need to align peak positions across both dimensions before joining multiple samples for multiway PCA or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3365
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# chromatogram-alignment-warping

## Summary

Aligns preprocessed 2D gas chromatography samples to a reference chromatogram using 2D correlation optimized warping (2DCOW), which corrects for retention-time drift and nonlinear distortion across both chromatographic dimensions. This skill is essential after baseline correction and smoothing to enable accurate multivariate comparison of GCxGC-MS profiles.

## When to use

Apply this skill when you have baseline-corrected and smoothed 2D-TIC chromatogram objects from individual GCxGC-MS samples that exhibit retention-time variations relative to a reference chromatogram, and you need to align peak positions across both dimensions before joining multiple samples for multiway PCA or metabolite comparison.

## When NOT to use

- Raw, unsmoothed chromatograms or chromatograms that have not undergone baseline correction, as alignment quality depends on signal-to-noise enhancement
- Single chromatogram without a reference standard; 2DCOW requires a stable, high-quality reference for alignment guidance
- Already-aligned or pre-warped chromatograms; applying 2DCOW twice will introduce cumulative distortion

## Inputs

- preprocessed sample chromatogram (2D-TIC object, smoothed and baseline-corrected)
- preprocessed reference chromatogram (2D-TIC object, smoothed and baseline-corrected)

## Outputs

- aligned chromatogram object (2D-TIC with warped retention times)
- warping function parameters (segment and warping level metadata)

## How to apply

Load a preprocessed sample chromatogram and a preprocessed reference chromatogram (both smoothed via Whittaker filter and baseline-corrected via asymmetric least squares). Apply the twod_cow function with segment parameters c(10, 40) to partition the chromatogram into manageable 10×40 blocks, and set maximum warping levels c(1, 8) to constrain deformation in the first and second dimensions respectively. The function iteratively optimizes 2D correlation within each segment, warping the sample chromatogram to maximize alignment with the reference. Retrieve the aligned chromatogram object, which will have corrected retention times and can then be joined with other preprocessed samples for downstream multivariate analysis.

## Related tools

- **RGCxGC** (R package providing twod_cow and batch_2DCOW functions for single-sample and batch 2D correlation optimized warping alignment) — https://github.com/DanielQuiroz97/RGCxGC
- **R** (programming environment executing the 2DCOW alignment via RGCxGC functions)

## Examples

```
aligned_sample <- twod_cow(sample_chrom, reference_chrom, segments=c(10, 40), max_warp=c(1, 8))
```

## Evaluation signals

- Aligned chromatogram object is returned without errors and has the same dimensions as the input sample chromatogram
- Peak positions in the aligned chromatogram are closer (in retention time) to corresponding peaks in the reference chromatogram compared to the unaligned sample
- Warping displacement is within the specified maximum warping levels c(1, 8) for each dimension, indicating controlled, biologically plausible deformation
- Multiway PCA scores and loadings computed after alignment show reduced inter-sample variance in stable metabolite regions compared to pre-alignment data
- Multiple samples aligned to the same reference chromatogram can be successfully joined into a single 3D array via join_chromatograms without dimension mismatches

## Limitations

- 2DCOW assumes the reference chromatogram is representative and stable; poor reference choice will propagate misalignment across all samples
- Segment parameters c(10, 40) and maximum warping c(1, 8) are heuristic and may require optimization for different chromatographic methods or column configurations
- Extreme retention-time shifts beyond the maximum warping threshold cannot be corrected; samples with very large drift relative to the reference may fail to align appropriately
- Alignment quality depends critically on prior smoothing and baseline correction; residual noise or baseline artifacts can degrade warping accuracy

## Evidence

- [other] task_004 finding and workflow: "The twod_cow function accepts four arguments: a sample chromatogram, a reference chromatogram, segment parameters (c(10, 40)), and maximum warping levels for both dimensions (c(1, 8)), and produces"
- [intro] preprocessing prerequisite: "noise can be significantly reduced by using preprocessing algorithms, herein smoothing, baseline correction, and peak alignment. Then, in order to reveal differences between groups, multivariate"
- [intro] 2DCOW algorithm implementation: "peak alignment of a single sample against a reference chromatogram can be performed based on the two-dimensional correlation optimized warping (2DCOW) algorithm. Alternatively, multiple sample"
- [readme] algorithm theoretical foundation: "peak alignment 2D COW based on asymetric least squares, smoothing based on the Whittaker smoother, and peak alignment 2D COW. Furthermore, the multiway principal component analysis is implemented"
