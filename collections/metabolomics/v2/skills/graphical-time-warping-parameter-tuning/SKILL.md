---
name: graphical-time-warping-parameter-tuning
description: Use when your XCMS-processed LC-MS dataset exhibits retention-time drift
  or misalignment artifacts—particularly when analyzing hundreds of samples, data
  acquisition spans longer than one week, or you observe feature groups with inconsistent
  m/z or RT that XCMS grouped under a single global warping.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0218
  - http://edamontology.org/topic_3375
  tools:
  - ncGTW
  - R
  - graphical time warping (GTW)
  - dynamic time warping (DTW)
  - xcms
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1093/bioinformatics/btaa037
  title: ncGTW
evidence_spans:
- Neighbor-wise Compound-specific Graphical Time Warping (ncGTW) [@ncgtw19] is an
  alignment algorithm
- '`ncGTW` is an R package developed as a plug-in of `xcms`'
- ncGTW is an R package developed as a plug-in of xcms
- This algorithm is improved from graphical time warping (GTW) [@gtw16], a popular
  dynamic time warping (DTW)
- graphical time warping (GTW) [@gtw16], a popular dynamic time warping (DTW) based
  alignment method
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ncgtw_cq
    doi: 10.1093/bioinformatics/btaa037
    title: ncGTW
  dedup_kept_from: coll_ncgtw_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btaa037
  all_source_dois:
  - 10.1093/bioinformatics/btaa037
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# graphical-time-warping-parameter-tuning

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Optimize ncGTW alignment parameters (parSamp for parallel sample grouping and bpParam for worker configuration) to generate compound-specific retention-time warping functions that replace XCMS global warping assumptions. This skill addresses LC-MS feature misalignment caused by XCMS's single warping function per m/z bin, especially in large cohorts or long acquisition runs.

## When to use

Your XCMS-processed LC-MS dataset exhibits retention-time drift or misalignment artifacts—particularly when analyzing hundreds of samples, data acquisition spans longer than one week, or you observe feature groups with inconsistent m/z or RT that XCMS grouped under a single global warping function. Use this skill when you need to detect and correct misalignments before peak-regrouping or peak-filling.

## When NOT to use

- Your input is already a finalized feature intensity table or peak-picked matrix; use this skill on raw or profile-aligned LC-MS data before quantitation.
- XCMS alignment appears adequate (no evidence of RT drift, feature group fragmentation, or multi-week acquisition); parameter tuning adds computational cost without benefit.
- You lack a valid xcmsSet object or preprocessed ncGTWinputs; the skill requires both XCMS and ncGTW-compatible data structures.

## Inputs

- ncGTWinputs object (preprocessed LC-MS profiles with XCMS alignment metadata)
- xcmsSet object (XCMS-aligned feature groups and RT corrections)
- parallel execution backend configuration (bpParam)

## Outputs

- ncGTW-derived warping functions (compound-specific, neighbor-constrained)
- adjusted retention-time coefficients (replaces xcmsLargeWin@rt$corrected)
- realigned feature groups ready for XCMS peak-filling and regrouping

## How to apply

Load a preprocessed ncGTWinputs object (containing XCMS-aligned features and metadata) and an xcmsSet object into ncGTWalign(). Configure the parSamp parameter to control how samples are grouped for neighbor-wise pairwise alignment—smaller values impose tighter structural constraints on warping functions between adjacent samples. Set bpParam to specify parallel worker backends (e.g., bplapply with MulticoreParam or SnowParam) to distribute the dynamic time warping computation across cores. Execute ncGTWalign() to compute compound-specific graphical time warping (GTW) functions that respect RT drift structure and neighboring-sample constraints. Pass the output through adjustRT() to refine and extract warping coefficients, which then replace the original xcmsLargeWin@rt$corrected slot for downstream XCMS peak-filling and regrouping operations. Validate that the new warping functions resolve previously misaligned feature groups by comparing p-values and sample membership before and after realignment.

## Related tools

- **ncGTW** (Primary alignment engine; applies neighbor-wise compound-specific graphical time warping with configurable parallel sample grouping (parSamp) and worker backends (bpParam) to detect and correct XCMS misalignments) — https://github.com/ChiungTingWu/ncGTW
- **xcms** (Upstream LC-MS feature detection and initial alignment; ncGTW operates as a plug-in to detect and realign misaligned features from xcmsSet objects)
- **R** (Execution environment for ncGTW and xcms packages; supports parallel backends via BiocParallel)
- **dynamic time warping (DTW)** (Underlying alignment algorithm; ncGTW constrains DTW-based warping functions using neighboring-sample structure)

## Examples

```
ncGTW_result <- ncGTWalign(ncGTWinputs, xcmsSet_obj, parSamp=c(1,2), bpParam=BiocParallel::MulticoreParam(workers=4)); xcmsSet_obj@rt$corrected <- adjustRT(ncGTW_result)
```

## Evaluation signals

- ncGTW realignment resolves previously misaligned features: compare feature group p-values and sample membership before and after adjustRT() replacement; p-values should decrease and samples should consolidate into single coherent groups.
- Warping function coefficients successfully replace xcmsLargeWin@rt$corrected: verify that the ncGTW-derived RT warping functions are inserted into the xcmsSet object and downstream XCMS peak-filling/regrouping steps accept the new corrections without error.
- Neighbor-wise constraints are respected: confirm that adjacent samples in the ncGTW alignment exhibit similar warping functions (validated by inspecting the constraint edges or by visual inspection of aligned chromatograms).
- Parallel execution efficiency improves with worker count scaling: measure total alignment runtime as a function of bpParam worker count; runtime should decrease sublinearly with increasing workers up to sample count.
- No feature loss or spurious grouping: verify that the total number of detected features and their m/z ranges remain stable after realignment, and that peak-filling and regrouping steps produce valid intensity matrices with no NaN or Inf values.

## Limitations

- ncGTW assumes that RT drift structure is consistent across neighboring samples; highly erratic or non-monotonic RT shifts may not be well-modeled by the constraint-edge approach.
- Parameter selection for parSamp and bpParam is not fully automated; practitioners must choose grouping granularity and parallelization strategy based on sample size, acquisition duration, and hardware resources; no guidance on optimal values is provided in the manual.
- Computational cost scales with sample count and m/z resolution; large cohorts (>500 samples) may require substantial wall-clock time and memory even with parallel workers.
- ncGTW detects misalignments using higher-resolution alignment results and p-value thresholds, but the threshold selection and false-positive/false-negative rates are not quantified in the provided documentation.

## Evidence

- [other] ncGTWalign() applies alignment with configurable parallel sample grouping and workers: "applies alignment with configurable parallel sample grouping (parSamp parameter) and workers (bpParam parameter)"
- [other] adjustRT() generates new RT warping functions that replace XCMS corrections: "adjustRT() generates new RT warping functions that replace xcmsLargeWin@rt$corrected for downstream peak-filling and regrouping"
- [readme] ncGTW detects misaligned features from XCMS using individualized warping functions: "ncGTW uses individualized warping functions for different compounds and assigns constraint edges on warping functions of neighboring samples"
- [intro] XCMS single warping function assumption causes misalignment in large cohorts: "all m/z bins in the same sample share the same warping function, which often fails with hundreds of samples or data acquisition longer than a week"
- [intro] ncGTW considers RT drift structure in addition to warping functions: "by considering the RT drifts structure, ncGTW can align RT more accurately"
- [readme] ncGTW is implemented as an R package plug-in for XCMS: "ncGTW is implemented in a R-package as a plug-in for XCMS. That is, ncGTW can detect the misaligned feature groups from XCMS and realign them"
