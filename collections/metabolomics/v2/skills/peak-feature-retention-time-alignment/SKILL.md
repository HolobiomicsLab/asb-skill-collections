---
name: peak-feature-retention-time-alignment
description: Use when you have preprocessed (smoothed and baseline-corrected) 2D-GCxGC-MS chromatograms from multiple samples and need to align their peak positions to a common reference chromatogram before multivariate analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - RGCxGC
  - R
  - wsmooth
  - baseline_corr
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

# peak-feature-retention-time-alignment

## Summary

Align peak retention times across preprocessed 2D gas chromatography samples to a reference chromatogram using 2D correlation optimized warping (2DCOW), enabling accurate feature matching and downstream multivariate analysis. This skill corrects for instrumental and chemical drift that causes retention time shifts between chromatographic runs.

## When to use

Apply this skill when you have preprocessed (smoothed and baseline-corrected) 2D-GCxGC-MS chromatograms from multiple samples and need to align their peak positions to a common reference chromatogram before multivariate analysis. Use it specifically when retention time shifts between runs could obscure true metabolite differences between groups (e.g., disease vs. control samples in metabolomic biomarker discovery).

## When NOT to use

- Input chromatograms are raw, unsmoothed NetCDF data—apply wsmooth and baseline_corr first.
- Reference chromatogram is of poor quality or contains artifacts—select a high-quality reference representative of the study group.
- Chromatograms have fundamentally different peak profiles (e.g., different sample types or extraction protocols)—ensure samples and reference are comparable.

## Inputs

- preprocessed sample chromatogram (2D array, output from wsmooth + baseline_corr)
- preprocessed reference chromatogram (2D array, output from wsmooth + baseline_corr)
- segment parameters (integer vector, typical c(10, 40))
- maximum warping levels (integer vector, typical c(1, 8))

## Outputs

- aligned sample chromatogram (2D array, retention times warped to match reference)
- warping function metadata (segment-wise transformation parameters, if available)

## How to apply

Load a preprocessed sample chromatogram and a preprocessed reference chromatogram (both output from wsmooth and baseline_corr functions). Apply the twod_cow function with segment parameters c(10, 40)—dividing the chromatogram into segments of 10 and 40 bins in the first and second dimensions respectively—and maximum warping levels c(1, 8) to constrain warping flexibility and prevent over-correction. The function applies 2D correlation optimized warping iteratively across these segments to maximize correlation between sample and reference peaks. For batch alignment of multiple samples, use batch_2DCOW instead. Inspect the aligned chromatogram visually to confirm that major peaks overlay the reference peaks without artificial peak distortion, and verify that the warping did not collapse distinct peaks or introduce artifacts.

## Related tools

- **RGCxGC** (R package implementing twod_cow and batch_2DCOW functions for 2D correlation optimized warping alignment of GCxGC-MS chromatograms) — https://github.com/DanielQuiroz97/RGCxGC
- **wsmooth** (RGCxGC preprocessing function applying Whittaker smoother prior to alignment) — https://github.com/DanielQuiroz97/RGCxGC
- **baseline_corr** (RGCxGC preprocessing function applying asymmetric least squares baseline correction prior to alignment) — https://github.com/DanielQuiroz97/RGCxGC

## Examples

```
aligned_sample <- twod_cow(sample_chrom, reference_chrom, segments=c(10,40), max_warp=c(1,8))
```

## Evaluation signals

- Aligned chromatogram peak positions visually overlay reference peaks with minimal residual shift in both first and second chromatographic dimensions.
- Correlation coefficient between aligned sample and reference chromatograms increases compared to pre-alignment correlation.
- Peak intensity and shape are preserved after warping (no artificial peak widening, splitting, or collapse).
- Warping parameters (segment deformations) remain within physically plausible bounds (gradual, continuous shifts rather than sharp discontinuities).
- Multivariate analysis (MPCA) downstream shows improved group separation and reduced within-group variance after alignment compared to unaligned data.

## Limitations

- 2DCOW assumes the sample and reference have similar peak content and order; highly divergent chromatograms may fail to align correctly or produce artifactual warping.
- Segment and warping parameters (c(10, 40) and c(1, 8)) are empirically chosen and may require tuning for different chromatographic methods, column dimensions, or sample types.
- Alignment quality depends critically on preprocessed data quality; if baseline correction or smoothing introduces artifacts, downstream alignment will propagate or magnify them.
- The choice of reference chromatogram affects all aligned samples; a poor reference can bias the entire dataset.

## Evidence

- [other] twod_cow function definition and parameters: "The twod_cow function accepts four arguments: a sample chromatogram, a reference chromatogram, segment parameters (c(10, 40)), and maximum warping levels for both dimensions (c(1, 8))"
- [intro] 2DCOW algorithm purpose and role in preprocessing: "peak alignment of a single sample against a reference chromatogram can be performed based on the two-dimensional correlation optimized warping (2DCOW) algorithm"
- [intro] preprocessing requirements before alignment: "you can perform preprocessing routines like smoothing and/or baseline correction by using the function wsmooth and baseline_corr"
- [intro] 2DCOW role in reducing noise and revealing group differences: "Preprocessing steps including smoothing, baseline correction, and peak alignment can reduce noise and reveal differences between groups for multivariate analysis"
- [readme] Algorithmic basis and reference: "peak alignment [2D COW] based on asymetric least squares, smoothing based on the Whittaker smoother, and peak alignment 2D COW"
