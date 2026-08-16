---
name: compound-specific-warping-function-generation
description: Use when xCMS alignment produces suspected misaligned feature groups across hundreds of samples or long acquisition runs (>1 week), particularly when global XCMS warping functions fail to account for compound-specific or sample-neighborhood retention-time drift structures.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3365
  - http://edamontology.org/topic_0091
  tools:
  - ncGTW
  - R
  - graphical time warping (GTW)
  - dynamic time warping (DTW)
  - xcms
  techniques:
  - LC-MS
derived_from:
- doi: 10.1093/bioinformatics/btaa037
  title: ncGTW
evidence_spans:
- Neighbor-wise Compound-specific Graphical Time Warping (ncGTW) [@ncgtw19] is an alignment algorithm
- '`ncGTW` is an R package developed as a plug-in of `xcms`'
- ncGTW is an R package developed as a plug-in of xcms
- This algorithm is improved from graphical time warping (GTW) [@gtw16], a popular dynamic time warping (DTW)
- graphical time warping (GTW) [@gtw16], a popular dynamic time warping (DTW) based alignment method
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

# compound-specific-warping-function-generation

## Summary

This skill detects and corrects misaligned LC-MS features produced by XCMS by generating individualized, compound-specific retention-time warping functions using neighbor-wise graphical time warping (ncGTW). It replaces global XCMS warping coefficients with RT-drift-aware, sample-neighbor-constrained warping functions to improve downstream peak grouping and filling accuracy.

## When to use

Apply this skill when XCMS alignment produces suspected misaligned feature groups across hundreds of samples or long acquisition runs (>1 week), particularly when global XCMS warping functions fail to account for compound-specific or sample-neighborhood retention-time drift structures. Use it if post-XCMS peak grouping or filling shows inconsistent retention-time patterns across replicates or if some features appear to belong to the same compound but are split across multiple m/z groups.

## When NOT to use

- Input data contains fewer than ~50 samples or acquisition time <1 week; global XCMS warping may be sufficient and ncGTW adds computational overhead without benefit.
- Features are already individually verified and realigned by manual inspection or orthogonal reference standards; ncGTW is designed for systematic misalignment detection, not spot-correction.
- Input is already a finalized feature abundance table (e.g., peak heights or areas); ncGTW operates on raw or grouped LC-MS profiles and cannot retroactively improve collapsed abundance data.

## Inputs

- xcmsSet object (XCMS-aligned LC-MS profile data with feature groups and global RT corrections)
- ncGTWinputs object (loaded preprocessed feature metadata and RT structure)

## Outputs

- ncGTWalign() output object (pairwise warping functions and alignment scores)
- adjustRT() output (refined RT warping coefficients)
- Modified xcmsSet object with @rt$corrected replaced by ncGTW-derived warping functions

## How to apply

First, load preprocessed XCMS output (an xcmsSet object) along with its corresponding ncGTWinputs object containing feature metadata and RT structure. Execute ncGTWalign() on the loaded data, configuring the parSamp parameter to control parallel sample grouping and bpParam to set parallel workers; this computes dynamic time warping with constraint edges on neighboring samples to estimate pairwise warping functions. Next, pass the ncGTWalign() output through adjustRT() to refine and finalize the warping coefficients. Replace the original xcmsSet@rt$corrected slots with the ncGTW-derived warping functions, then proceed with XCMS peak-regrouping and peak-filling using the new RT coordinates. The key rationale is that ncGTW avoids the inaccurate assumption that all m/z bins in the same sample share one global warping function; instead it fits individual warping functions per compound while constraining them to align with neighboring samples' RT drift patterns.

## Related tools

- **ncGTW** (Core R package implementing neighbor-wise compound-specific graphical time warping alignment and misalignment detection; used to generate and refine warping functions.) — https://github.com/ChiungTingWu/ncGTW
- **xcms** (Upstream LC-MS preprocessing and initial global alignment; ncGTW acts as a plug-in to detect and correct XCMS misalignments via individualized warping functions.)
- **R** (Programming environment for running ncGTW functions (ncGTWalign(), adjustRT()) and orchestrating workflow steps.)

## Examples

```
ncGTWalign(ncGTWinputs, xcmsSet_object, parSamp=10, bpParam=BiocParallel::MulticoreParam(4)); adjustRT(ncGTWalign_output) -> new_rt_functions
```

## Evaluation signals

- RT correction quality: verify that ncGTW-corrected RT values reduce within-compound RT variance across replicates compared to XCMS-only corrections; plot RT distributions before and after adjustRT().
- Alignment accuracy: confirm that previously split features (same compound, different m/z groups) now co-align; check feature abundance correlation across replicates improves post-realignment.
- Misalignment detection consistency: confirm that ncGTWalign() p-values flag known problematic features (e.g., features with disjoint sample subsets or drift artifacts) consistently.
- Downstream peak-grouping improvement: re-run xcms grouping and peak-filling on ncGTW-corrected data and verify that the number of spurious feature groups decreases and group coherence (e.g., mass accuracy, RT clustering) improves.
- Parameter stability: verify that parSamp and bpParam settings produce consistent warping functions across runs and that constraint edges on neighboring samples are properly enforced (inspect alignment graph structure).

## Limitations

- ncGTW assumes that misaligned features can be identified via p-value testing and disjoint sample subsets; features with continuous low-level misalignment across all samples may not be flagged or corrected.
- Computational cost scales with sample count and feature complexity; the reference-free pairwise alignment strategy requires all-to-all sample comparisons, which becomes expensive for very large cohorts (>1000 samples).
- ncGTW requires that upstream XCMS grouping is reasonably accurate; if XCMS grouping is severely miscalibrated, ncGTW's neighbor-based constraint strategy may propagate or amplify those errors rather than correct them.
- No official changelog provided; version compatibility with recent XCMS releases and Bioconductor versions is not explicitly documented, requiring users to verify installation on their system.

## Evidence

- [intro] ncGTW avoids the inaccurate assumption that all m/z bins share one global warping function: "ncGTW uses individualized warping functions for different compounds and assigns constraint edges on warping functions of neighboring samples. That is, ncGTW avoids the popular but not accurate"
- [intro] ncGTW improves accuracy by considering RT drift structures in addition to warping functions: "by considering the RT drifts structure, ncGTW can align RT more accurately"
- [other] ncGTWalign() computes alignment with configurable parallel grouping and worker parameters: "applies alignment with configurable parallel sample grouping (parSamp parameter) and workers (bpParam parameter)"
- [other] adjustRT() generates refined warping functions that replace XCMS RT corrections: "adjustRT() generates new RT warping functions that replace xcmsLargeWin@rt$corrected for downstream peak-filling and regrouping"
- [readme] ncGTW is implemented as an XCMS plug-in to detect and fix misaligned features: "ncGTW can detect the misaligned feature groups from XCMS and realign them. After that, XCMS can use the realigned data from XCMS for more accurate grouping and peak-filling."
- [readme] ncGTW uses dynamic time warping with constraint edges on neighboring samples: "ncGTW performs all possible pairwise alignments between each two sample with the structure information in the dataset"
