---
name: xcms-output-replacement-workflow
description: Use when xCMS has produced aligned LC-MS features but alignment quality is suspected to be poor—especially when analyzing hundreds of samples, data acquired over extended periods (>1 week), or when individual m/z bins show inconsistent RT shifts.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - ncGTW
  - xcms
  - R
derived_from:
- doi: 10.1093/bioinformatics/btaa037
  title: ncGTW
evidence_spans:
- Neighbor-wise Compound-specific Graphical Time Warping (ncGTW) [@ncgtw19] is an alignment algorithm
- '`ncGTW` is an R package developed as a plug-in of `xcms`, a popular LC-MS data analysis R package'
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
---

# xcms-output-replacement-workflow

## Summary

Replace XCMS-derived retention time (RT) corrections with ncGTW-computed warping functions to improve alignment accuracy for LC-MS feature groups affected by RT drift or misalignment. This workflow detects XCMS alignment failures and substitutes individualized, compound-specific warping functions that better capture RT structure across sample cohorts.

## When to use

XCMS has produced aligned LC-MS features but alignment quality is suspected to be poor—especially when analyzing hundreds of samples, data acquired over extended periods (>1 week), or when individual m/z bins show inconsistent RT shifts. Use this skill after XCMS alignment if feature groups show scatter in extracted ion chromatograms or if p-value-based misalignment detection (applied by ncGTW) identifies features with sufficiently small p-values and disjoint sample subsets.

## When NOT to use

- XCMS alignment has not yet been performed or xcmsSet object is not available.
- Sample cohort is small (<10 samples) or data acquisition time is short (<1 day), where XCMS single global warping function is usually sufficient.
- Input is already a finalized feature intensity matrix or quantification table; use ncGTW only on raw or profile data during alignment refinement.

## Inputs

- ncGTWinputs object (preprocessed XCMS-aligned profile data with metadata)
- xcmsSet object (XCMS alignment result with @rt$corrected slot)
- Raw or profile LC-MS data in formats supported by xcms (mzML, mzXML, NetCDF)

## Outputs

- Adjusted xcmsSet object with @rt$corrected replaced by ncGTW warping functions
- Refined retention time warping coefficients (from adjustRT())
- Re-grouped and re-filled feature table with improved peak alignment

## How to apply

Load the preprocessed ncGTWinputs object (containing XCMS-aligned features and metadata) alongside the xcmsSet object. Execute ncGTWalign() with configurable parallel sample grouping (parSamp parameter) and worker specification (bpParam parameter) to compute neighbor-wise, compound-specific graphical time warping (GTW) functions using dynamic time warping (DTW) with constraint edges on neighboring samples. This generates pairwise alignments between sample pairs while incorporating RT drift structure information. Pass the ncGTWalign() output through adjustRT() to refine and validate the warping coefficients, then replace the original xcmsSet@rt$corrected retention times with ncGTW-derived warping functions. Finally, re-execute XCMS peak-filling and feature regrouping steps using the updated RT corrections to produce the final aligned feature matrix.

## Related tools

- **ncGTW** (Computes neighbor-wise compound-specific graphical time warping functions and detects/corrects XCMS misalignments; applies dynamic time warping with RT drift structure constraints across neighboring samples) — https://github.com/ChiungTingWu/ncGTW
- **xcms** (Produces initial LC-MS feature alignment and RT correction; ncGTW acts as a plug-in to detect and replace XCMS-derived RT corrections with improved warping functions)
- **R** (Execution environment for ncGTW and xcms packages)

## Examples

```
ncGTWalign_obj <- ncGTWalign(ncGTWinputs, xcmsSet_obj, parSamp=4, bpParam=BiocParallel::MulticoreParam(4)); adjusted_rt <- adjustRT(ncGTWalign_obj); xcmsSet_obj@rt$corrected <- adjusted_rt; xcmsSet_refined <- xcms::fillPeaks(xcmsSet_obj); xcmsSet_refined <- xcms::group(xcmsSet_refined)
```

## Evaluation signals

- ncGTWalign() successfully processes ncGTWinputs and xcmsSet objects without memory or convergence errors; parallel execution completes within expected time using specified bpParam workers.
- adjustRT() output warping functions are numerically valid (no NaN, Inf, or out-of-range RT values) and differ meaningfully from original XCMS @rt$corrected values in regions identified as misaligned.
- After replacement of @rt$corrected and re-running xcms::fillPeaks() and xcms::group(), feature intensity distributions show reduced scatter in extracted ion chromatograms and improved correlation between replicates compared to XCMS-only alignment.
- P-value statistics from ncGTW misalignment detection show significant features (p < threshold) in sample subsets overlap with features flagged as problematic in exploratory alignment QC plots.
- Peak count and feature intensity statistics remain stable or improve (e.g., total feature count does not drop >10%, median peak width stays within historical range) after RT correction replacement.

## Limitations

- ncGTW assumes that neighboring samples share RT drift trends; performance may degrade if samples are randomized or acquired under highly variable conditions without temporal structure.
- Individualized warping functions per compound increase computational cost and memory usage proportional to number of unique m/z bins; large datasets (>500 samples or >10,000 features) may require high-performance computing resources and careful worker/memory tuning.
- ncGTW detection of misaligned features relies on p-value thresholds and disjoint sample subset criteria; results are sensitive to parameter selection and may miss subtle misalignments or false-positive corrections in datasets with extreme RT drift.
- The workflow replaces XCMS RT corrections globally; if only a subset of feature groups are misaligned, selective re-alignment or hybrid approaches may be preferable but are not described in the current documentation.

## Evidence

- [intro] ncGTW uses individualized warping functions for different compounds and assigns constraint edges on warping functions of neighboring samples.: "ncGTW uses individualized warping functions for different compounds and assigns constraint edges on warping functions of neighboring samples"
- [other] ncGTWalign() accepts loaded profile data (ncGTWinputs) and an xcmsSet object, applies alignment with configurable parallel sample grouping (parSamp parameter) and workers (bpParam parameter), then adjustRT() generates new RT warping functions that replace xcmsLargeWin@rt$corrected for downstream peak-filling and regrouping.: "ncGTWalign() accepts loaded profile data (ncGTWinputs) and an xcmsSet object, applies alignment with configurable parallel sample grouping (parSamp parameter) and workers (bpParam parameter), then"
- [intro] ncGTW can detect misaligned features produced by xcms due to the assumption that all m/z bins in the same sample share the same warping function, which often fails with hundreds of samples or data acquisition longer than a week.: "ncGTW can detect misaligned features produced by xcms due to the assumption that all m/z bins in the same sample share the same warping function, which often fails with hundreds of samples or data"
- [readme] ncGTW detects the misaligned features with two criterions. First, ncGTW algorithm estimates the p-value of each feature using higher resolution alignment result. Second, we identifies all features with sufficiently small p-values and disjoint sample subsets.: "ncGTW detects the misaligned features with two criterions. First, ncGTW algorithm estimates the p-value of each feature using higher resolution alignment result. Second, we identifies all features"
- [readme] After that, XCMS can use the realigned data from XCMS for more accurate grouping and peak-filling.: "After that, XCMS can use the realigned data from XCMS for more accurate grouping and peak-filling"
