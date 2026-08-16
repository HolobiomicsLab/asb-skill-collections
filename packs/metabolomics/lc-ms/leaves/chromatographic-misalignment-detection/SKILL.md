---
name: chromatographic-misalignment-detection
description: Use when after running XCMS-based alignment on LC-MS datasets with hundreds of samples or data acquisition periods longer than a week, when the assumption that all m/z bins in the same sample share a single warping function is likely to fail.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3173
  - http://edamontology.org/topic_0091
  tools:
  - ncGTW
  - R
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

# chromatographic-misalignment-detection

## Summary

Detect and identify misaligned feature groups in LC-MS data that result from overly simplistic alignment assumptions in XCMS, using higher-resolution alignment results and statistical p-value thresholding to flag features with inconsistent sample subset patterns.

## When to use

After running XCMS-based alignment on LC-MS datasets with hundreds of samples or data acquisition periods longer than a week, when the assumption that all m/z bins in the same sample share a single warping function is likely to fail. Use this skill when you suspect XCMS has produced misaligned features due to retention time drift structures or parameter misconfiguration, and you need to identify which features require realignment before peak-filling or peak-regrouping.

## When NOT to use

- Input dataset contains fewer than ~20–30 samples or acquisition time spans only hours, where single warping functions per sample are often sufficient.
- XCMS alignment has already been visually validated or independently confirmed by reference standards; misalignment detection assumes prior alignment may be unreliable.
- Your analysis goal does not require peak-filling or peak-regrouping; misalignment detection adds computational cost only if downstream steps depend on accurate feature alignment.

## Inputs

- XCMS-aligned LC-MS feature group table (xcmsSet object)
- Raw LC-MS data in mzXML, mzML, or netCDF format
- XCMS warping functions and group metadata

## Outputs

- List of flagged misaligned feature group indices
- P-value assignments per feature
- Sample subset patterns indicating misalignment signature
- Candidate features for ncGTW realignment

## How to apply

First, perform XCMS alignment at default resolution to establish baseline warping functions. Then run ncGTW's misalignment detection algorithm, which operates in two steps: (1) estimate a p-value for each feature using a higher-resolution alignment result under the null hypothesis of accurate alignment; (2) identify all features with sufficiently small p-values and disjoint sample subsets, flagging these as misaligned candidates. The algorithm does not immediately realign — it only surfaces misalignment signals. Compare the flagged features against the XCMS output to determine which require compound-specific, individualized warping functions. The decision to proceed to realignment depends on the severity of CV increase or the magnitude of retention time drift within flagged feature groups.

## Related tools

- **ncGTW** (Performs misalignment detection via higher-resolution alignment and p-value assignment; identifies feature groups with disjoint sample subsets) — https://github.com/ChiungTingWu/ncGTW
- **xcms** (Produces baseline warping functions and initial alignment that ncGTW evaluates for misalignment)
- **R** (Execution environment for ncGTW as a plug-in package)

## Examples

```
# After XCMS alignment in R:
xcmsSet_obj <- xcmsSet(...)  # standard XCMS workflow
ncgtw_obj <- ncGTW(xcmsSet_obj)  # initialize ncGTW
misaligned_features <- detectMisalignments(ncgtw_obj, pvalue_threshold=0.05)  # detect misaligned feature indices
```

## Evaluation signals

- Flagged features have p-values below the chosen significance threshold (typically < 0.05) and show disjoint sample subsets in the misalignment signature, confirming they fail the single-warping-function assumption.
- Coefficient of variation (CV) for flagged features is elevated (e.g., > 0.30) before realignment, and improvement after ncGTW realignment and peak-filling is substantial (e.g., CV reduction from 0.369 to 0.229).
- Retention time distributions of flagged features across samples show multi-modal or discontinuous patterns inconsistent with a single smooth warping function.
- The number and identity of flagged features are stable across repeated runs with the same hyperparameters, indicating reproducible detection.
- After realignment, flagged feature groups no longer exhibit disjoint sample subset patterns and show continuous, unimodal retention time distributions.

## Limitations

- Misalignment detection relies on the assumption that higher-resolution alignment produces more accurate results; if the higher-resolution alignment itself is biased or uses inappropriate parameters, detection may fail or produce false positives.
- The algorithm requires a sufficient number of samples and diverse retention time drift patterns to estimate p-values reliably; small datasets (< 20 samples) may yield unreliable p-value assignments.
- Detection does not account for true biological variation in retention time across samples; features with genuine compound-specific drift may be flagged as misaligned and incorrectly realigned.
- Performance and memory requirements scale with dataset size (number of samples and features); very large datasets may face computational bottlenecks.
- The choice of p-value threshold and the definition of 'disjoint sample subsets' are user-configurable but not fully detailed in the provided documentation, leaving room for operator-dependent bias.

## Evidence

- [readme] Misalignment detection rationale: "ncGTW detects the misaligned features with two criterions. First, ncGTW algorithm estimates the p-value of each feature using higher resolution alignment result, where the p-value is given by the"
- [intro] Core problem statement: "ncGTW uses individualized warping functions for different compounds and assigns constraint edges on warping functions of neighboring samples. That is, ncGTW avoids the popular but not accurate"
- [intro] Downstream utility: "xcms may have some misaligned features, and there is a function in ncGTW to identify such misalignments. After identifying"
- [other] Quantitative performance measure: "ncGTW realignment reduced CV after peak-filling from 0.369 to 0.229 for feature 1 and from 0.351 to 0.119 for feature 2, compared to XCMS warping functions."
- [readme] Installation and integration: "The purpose of ncGTW is to detect and fix the bad alignments in the LC-MS data. Currently, ncGTW is implemented in a R-package as a plug-in for XCMS."
