---
name: neighbor-wise-constraint-propagation-in-dtw
description: Use when when XCMS or other DTW-based aligners have produced misaligned LC-MS feature groups across hundreds of samples or long acquisition periods (>1 week), particularly when individual m/z bins or compounds show inconsistent retention-time drift patterns across neighboring samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3644
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - ncGTW
  - R
  - xcms
  - graphical time warping (GTW)
  - dynamic time warping (DTW)
  techniques:
  - LC-MS
derived_from:
- doi: 10.1093/bioinformatics/btaa037
  title: ncGTW
evidence_spans:
- Neighbor-wise Compound-specific Graphical Time Warping (ncGTW) [@ncgtw19] is an alignment algorithm
- '`ncGTW` is an R package developed as a plug-in of `xcms`'
- ncGTW is an R package developed as a plug-in of xcms
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Neighbor-wise constraint propagation in dynamic time warping

## Summary

Apply neighbor-wise constraint edges during dynamic time warping alignment to enforce consistency of retention-time warping functions across adjacent LC-MS samples, improving alignment accuracy for compound-specific features that would otherwise diverge under sample-independent warping assumptions.

## When to use

When XCMS or other DTW-based aligners have produced misaligned LC-MS feature groups across hundreds of samples or long acquisition periods (>1 week), particularly when individual m/z bins or compounds show inconsistent retention-time drift patterns across neighboring samples. The skill is triggered by detection of features with sufficiently small p-values under higher-resolution alignment that have disjoint sample subsets, indicating localized misalignment.

## When NOT to use

- Input is a single LC-MS sample or very small cohort (<3 samples) where neighbor constraints cannot propagate meaningfully.
- XCMS alignment is already accurate and misalignment detection yields no features with sufficiently small p-values (i.e., no misalignment present).
- Input data has already been realigned by another reference-based method; neighbor-wise constraints assume reference-free pairwise structure that may conflict with fixed anchors.

## Inputs

- ncGTWinputs object (loaded LC-MS profile data with XCMS-aligned features and metadata)
- xcmsSet object (XCMS alignment results including corrected retention times)

## Outputs

- ncGTW warping functions (neighbor-constrained, compound-specific retention-time correction coefficients)
- Adjusted RT values (output of adjustRT() replacing xcmsLargeWin@rt$corrected for downstream peak-filling and regrouping)

## How to apply

Within the ncGTWalign() function, construct constraint edges on warping functions between neighboring samples to enforce smooth, sample-adjacent consistency of compound-specific retention-time warping. The algorithm: (1) accepts loaded ncGTWinputs (XCMS-preprocessed LC-MS profiles with metadata) and an xcmsSet object; (2) performs all possible pairwise alignments between sample pairs while propagating neighbor constraints as structural information; (3) uses these pairwise alignments as constraints to estimate aggregate warping functions for each sample that satisfy neighbor-wise consistency; (4) applies configurable parallel grouping (parSamp parameter) and worker threads (bpParam parameter) to scale across large cohorts. The rationale is that individual compounds often have localized, sample-dependent RT drift structures that violate the global single-warping-function assumption of XCMS, so constraining neighbors prevents spurious divergence while allowing compound-specificity.

## Related tools

- **ncGTW** (Primary R package implementing neighbor-wise compound-specific graphical time warping with constraint edges on neighboring samples) — https://github.com/ChiungTingWu/ncGTW
- **xcms** (Upstream LC-MS feature detection and global alignment whose misaligned features ncGTW detects and realigns)
- **graphical time warping (GTW)** (Parent algorithm improved by ncGTW to incorporate neighbor-wise constraints and compound-specificity)
- **dynamic time warping (DTW)** (Core distance metric underlying GTW and ncGTW pairwise alignment)

## Examples

```
ncGTWalign(object = xcmsSet_obj, input = ncGTWinputs_obj, parSamp = 10, bpParam = BiocParallel::bplapply); adjustRT(ncGTWalign_output)
```

## Evaluation signals

- Neighbor-constrained warping functions should show smooth, continuous drift across adjacent samples for the same compound (no sharp discontinuities in RT correction between samples i and i+1).
- p-values for realigned features should be elevated (weaker significance of misalignment) compared to pre-realignment p-values, indicating correction has reduced spurious separation.
- Downstream XCMS peak-regrouping and peak-filling operations should converge to fewer, larger feature groups with consistent m/z and RT ranges across samples.
- Compound-specific warping functions should vary between different m/z bins, confirming that the method does not revert to a single global warping function.
- Pairwise alignment consistency: constraint-satisfaction check that each sample's warping function to the common coordinate satisfies edges to neighbors within a specified tolerance.

## Limitations

- Misalignment detection relies on p-value significance under higher-resolution alignment; features with low signal-to-noise ratio may not generate reliable p-values.
- Neighbor-wise constraints assume spatial proximity in sample order (e.g., temporal or batch adjacency); if samples are randomly ordered or from disparate acquisition blocks, constraint edges may not encode meaningful structure.
- Reference-free, all-pairwise-alignment approach scales quadratically with sample count; for >1000 samples, computational cost and memory may become prohibitive unless parallelization is tuned.
- The algorithm requires that XCMS has already been run; it cannot recover from XCMS parameter misconfiguration if the entire feature set is misaligned uniformly rather than in localized subsets.

## Evidence

- [intro] ncGTW uses individualized warping functions for different compounds and assigns constraint edges on warping functions of neighboring samples: "ncGTW uses individualized warping functions for different compounds and assigns constraint edges on warping functions of neighboring samples."
- [other] ncGTWalign() accepts loaded profile data and xcmsSet, applies alignment with configurable parallel sample grouping and workers: "ncGTWalign() accepts loaded profile data (ncGTWinputs) and an xcmsSet object, applies alignment with configurable parallel sample grouping (parSamp parameter) and workers (bpParam parameter)"
- [other] adjustRT() generates new RT warping functions that replace XCMS-derived corrections for downstream peak-filling: "adjustRT() generates new RT warping functions that replace xcmsLargeWin@rt$corrected for downstream peak-filling and regrouping."
- [readme] ncGTW detects misalignment via p-value and disjoint sample subsets, then realigns using pairwise alignments as constraints: "ncGTW algorithm estimates the p-value of each feature using higher resolution alignment result, where the p-value is given by the null hypothesis with accurate alignment. Second, we identifies all"
- [readme] ncGTW performs all possible pairwise alignments with structure information, then estimates warping functions for all samples to a coordinate: "ncGTW performs all possible pairwise alignments between each two sample with the structure information in the dataset. Second, with all the pairwise alignment as constraints, ncGTW estimates the"
- [intro] XCMS assumes all m/z bins in the same sample share one warping function, which fails with hundreds of samples or week-long acquisition: "ncGTW can detect misaligned features produced by xcms due to the assumption that all m/z bins in the same sample share the same warping function, which often fails with hundreds of samples or data"
