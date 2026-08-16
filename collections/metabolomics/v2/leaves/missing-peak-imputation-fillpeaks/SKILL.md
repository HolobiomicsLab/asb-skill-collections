---
name: missing-peak-imputation-fillpeaks
description: Use when apply fillPeaks after retention time alignment (whether XCMS
  or ncGTW) when feature matrices contain missing peaks across samples due to alignment
  gaps or detection failures.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - ncGTW
  - R
  - xcms
  - compCV
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

# Missing-peak imputation (fillPeaks)

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

fillPeaks is a peak-filling operation that imputes missing intensity values for aligned features across samples in LC-MS data, enabling coefficient-of-variation reduction after retention time warping. It is essential for completing feature matrices before statistical comparison of alignment quality.

## When to use

Apply fillPeaks after retention time alignment (whether XCMS or ncGTW) when feature matrices contain missing peaks across samples due to alignment gaps or detection failures. Use it specifically when you need to compute robust metrics like coefficient of variation (CV) across sample replicates to assess alignment accuracy, or before downstream peak-regrouping and statistical analysis.

## When NOT to use

- Input feature matrix is already complete (no missing values across samples).
- Downstream analysis requires preservation of original detection patterns (e.g., missingness as a biological signal).
- Alignment has not yet been performed; fillPeaks operates only on post-alignment feature objects.

## Inputs

- XCMS or ncGTW aligned feature object (xcmsSet or ncGTW output)
- Raw LC-MS data in mzML, mzXML, or netCDF format
- Feature group definitions from retention time alignment

## Outputs

- Feature matrix with imputed missing peak intensities
- Coefficient of variation (CV) values per feature (numeric vector)
- Comparison table of CV before/after fillPeaks (e.g., 0.369 → 0.229)

## How to apply

After performing either XCMS-based or ncGTW-based retention time alignment, apply the fillPeaks function to the aligned feature object to estimate and populate missing intensity values for features that were not detected in all samples. The function uses interpolation or peak integration strategies to infer missing signals. Compute the coefficient of variation for each feature (e.g., using compCV) before and after fillPeaks to quantify the reduction in CV, which indicates improved alignment quality. Compare CV improvements between competing alignment methods (e.g., XCMS vs. ncGTW) to validate which warping strategy produces more consistent feature detection across the sample cohort.

## Related tools

- **xcms** (Baseline alignment method; fillPeaks is applied to XCMS-aligned results for comparison baseline) — https://github.com/sneumann/xcms
- **ncGTW** (Improved alignment method whose fillPeaks results are compared against XCMS to validate retention time warping quality) — https://github.com/ChiungTingWu/ncGTW
- **compCV** (Function to compute coefficient of variation for quantifying fillPeaks imputation success) — https://github.com/ChiungTingWu/ncGTW
- **R** (Statistical computing environment for executing fillPeaks and CV comparison workflow)

## Examples

```
# After XCMS alignment, apply fillPeaks and compute CV:
xcms_filled <- fillPeaks(xcms_aligned)
cv_xcms_feature1 <- compCV(xcms_filled, featureID=1)
# After ncGTW realignment:
ncgtw_filled <- fillPeaks(ncgtw_aligned)
cv_ncgtw_feature1 <- compCV(ncgtw_filled, featureID=1)
```

## Evaluation signals

- Coefficient of variation decreases after fillPeaks application (e.g., feature 1: 0.369 → 0.229, feature 2: 0.351 → 0.119 in the ncGTW study).
- Feature matrix completeness increases: no missing NA or zero values for aligned features across all samples.
- CV reduction ratios are consistent and reproducible when comparing two alignment methods applied to the same dataset.
- Imputed peak intensities fall within expected intensity ranges relative to detected peaks in neighboring samples.
- Downstream statistical tests (e.g., ANOVA, fold-change quantification) show improved signal-to-noise ratio after fillPeaks vs. before.

## Limitations

- fillPeaks accuracy depends critically on upstream alignment quality; poor warping functions produce unreliable imputations.
- Imputation may mask true biological missingness (e.g., compound absence in specific samples) if not distinguished from technical gaps.
- fillPeaks behavior with very sparse feature matrices (many samples with no detection) is not documented; sparse imputation may fail.
- The algorithm assumes missing peaks follow predictable intensity patterns from detected peaks in neighboring samples, which may not hold for noisy or complex chromatography.

## Evidence

- [other] fillPeaks role in CV reduction workflow: "Apply fillPeaks to the XCMS-aligned results and compute CV values for feature 1 and feature 2 using compCV. Perform ncGTW-based alignment on the same dataset using individualized warping functions"
- [other] Quantified CV improvements post-fillPeaks: "ncGTW realignment reduced CV after peak-filling from 0.369 to 0.229 for feature 1 and from 0.351 to 0.119 for feature 2, compared to XCMS warping functions"
- [readme] ncGTW context for fillPeaks application: "After that, XCMS can use the realigned data from XCMS for more accurate grouping and peak-filling."
- [other] fillPeaks purpose in alignment quality assessment: "xcms may have misaligned features that can be identified and realigned with ncGTW for more accurate downstream analysis such as peak-regrouping or peak-filling"
