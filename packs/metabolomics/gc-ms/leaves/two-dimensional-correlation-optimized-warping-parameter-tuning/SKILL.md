---
name: two-dimensional-correlation-optimized-warping-parameter-tuning
description: Use when when you have a preprocessed sample chromatogram (smoothed and baseline-corrected) and a preprocessed reference chromatogram, and need to align them using 2D COW.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
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

# two-dimensional-correlation-optimized-warping-parameter-tuning

## Summary

Tune segment and maximum warping parameters for the 2D correlation optimized warping (2D COW) algorithm to align preprocessed GCxGC-MS chromatograms. This skill addresses the critical decision of parameter selection that controls both the granularity of alignment segments and the allowed deformation in first and second dimensions, balancing alignment fidelity against overfitting.

## When to use

When you have a preprocessed sample chromatogram (smoothed and baseline-corrected) and a preprocessed reference chromatogram, and need to align them using 2D COW. Apply this skill when default or literature parameters may not be appropriate for your specific GCxGC-MS instrumentation, sample complexity, or chromatographic resolution. The choice of segments (number and length) and maximum warping levels (first and second dimension constraints) directly affects whether subtle metabolite shifts are captured without introducing spurious peak distortions.

## When NOT to use

- Input chromatograms have not been preprocessed (smoothed and baseline-corrected); apply smoothing and baseline correction first.
- Sample and reference chromatograms come from substantially different experimental conditions or instrument platforms; 2D COW assumes structural similarity in peak layout.
- Alignment goal is to merge multiple samples into a consensus feature table; use batch_2DCOW or join_chromatograms post-alignment instead.

## Inputs

- preprocessed sample chromatogram object (smoothed and baseline-corrected)
- preprocessed reference chromatogram object (smoothed and baseline-corrected)

## Outputs

- aligned sample chromatogram object (2D COW warped)

## How to apply

Prepare two preprocessed chromatogram objects (sample and reference) as R objects. Call the twod_cow function with four arguments: the sample chromatogram, reference chromatogram, a segments vector defining the number of segments and maximum segment length (e.g., c(10, 40)), and a max_warp vector specifying maximum warping levels for the first and second chromatographic dimensions (e.g., c(1, 8)). The segments parameter controls alignment granularity—smaller first values increase the number of alignment segments, capturing finer retention-time shifts but risking overfitting; the second value caps maximum segment length. The max_warp parameter constrains deformation: higher values permit more aggressive warping and are suitable for larger expected misalignments between sample and reference, while lower values enforce stricter structural conservation. Inspect the resulting aligned chromatogram object by visualizing overlay plots and examining peak position differences before and after alignment to verify the warping did not introduce artificial distortions or collapse genuine metabolite signals.

## Related tools

- **RGCxGC** (R package containing twod_cow function and 2D COW implementation; handles chromatogram import, preprocessing, and alignment workflow) — https://github.com/DanielQuiroz97/RGCxGC
- **R** (Language and runtime environment for executing twod_cow and RGCxGC functions)

## Examples

```
twod_cow(sample_chrom, reference_chrom, segments=c(10, 40), max_warp=c(1, 8))
```

## Evaluation signals

- Aligned chromatogram retains peak count and identities present in both sample and reference; no peaks are spuriously removed or merged.
- Peak retention times in aligned sample shift toward reference retention times; magnitude of shift is consistent with known inter-sample variation and instrumental drift tolerance.
- Visual overlay of aligned sample and reference chromatograms shows concordant peak positions (within ±0.1–0.2 min in first dimension, ±0.5–1.0 s in second dimension for typical GCxGC protocols).
- Intensity distribution and peak shape are preserved post-alignment; no artificial peak broadening or height attenuation is introduced by warping.
- Downstream multivariate analysis (e.g., MPCA) after alignment shows improved group separation and reduced inter-sample noise compared to unaligned data, indicating successful removal of systematic retention-time misalignment.

## Limitations

- Parameter selection (segments and max_warp) requires domain knowledge or empirical tuning; no automated parameter optimization algorithm is described in the article.
- 2D COW assumes the sample and reference share the same peak order and approximate retention times; severe instrumental drift or sample degradation may cause algorithm failure.
- Computational cost scales with chromatogram resolution and warping parameter magnitude; very large datasets or aggressive warping may be slow.
- The algorithm does not identify or annotate individual peaks; it aligns the entire chromatographic space, so misalignment in one region can propagate to others.

## Evidence

- [other] The twod_cow function accepts four arguments: a sample chromatogram, a reference chromatogram, segment parameters (c(10, 40)), and maximum warping levels for both dimensions (c(1, 8)): "The twod_cow function accepts four arguments: a sample chromatogram, a reference chromatogram, segment parameters (c(10, 40)), and maximum warping levels for both dimensions (c(1, 8))"
- [readme] RGCxGC offers common pre-processing algorithms for signal enhancement, such as baseline correction based on asymetric least squares, smoothing based on the Whittaker smoother, and peak alignment 2D COW: "RGCxGC offers common pre-processing algorithms for signal enhancement, such as baseline correction based on asymetric least squares, smoothing based on the Whittaker smoother, and peak alignment 2D"
- [intro] peak alignment of a single sample against a reference chromatogram can be performed based on the two-dimensional correlation optimized warping (2DCOW) algorithm: "peak alignment of a single sample against a reference chromatogram can be performed based on the two-dimensional correlation optimized warping (2DCOW) algorithm"
- [intro] noise can be significantly reduced by using preprocessing algorithms, herein smoothing, baseline correction, and peak alignment. Then, in order to reveal differences between groups, multivariate: "noise can be significantly reduced by using preprocessing algorithms, herein smoothing, baseline correction, and peak alignment"
- [readme] Zhang, D., Huang, X., Regnier, F. E., & Zhang, M. (2008). Two-Dimensional Correlation Optimized Warping Algorithm for Aligning GC×GC−MS Data. Analytical Chemistry, 80(8), 2664-2671.: "Two-Dimensional Correlation Optimized Warping Algorithm for Aligning GC×GC−MS Data. Analytical Chemistry, 80(8), 2664-2671"
