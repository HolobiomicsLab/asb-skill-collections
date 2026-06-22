---
name: metabolite-ion-consolidation
description: Use when after chromatographic peak detection in LC-MS data, when you have hundreds or thousands of features and need to consolidate ions presumed to originate from the same metabolite.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0091
  tools:
  - MsFeatures
  - xcms
  - MSnbase
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/ac051437y
  title: XCMS
evidence_spans:
- General MS feature grouping functionality if defined by the `r Biocpkg("MsFeatures")` package with additional functionality being implemented
- VignetteDepends{xcms,BiocStyle,faahKO,pheatmap,MsFeatures}
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_xcms_cq
    doi: 10.1021/ac051437y
    title: XCMS
  dedup_kept_from: coll_xcms_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/ac051437y
  all_source_dois:
  - 10.1021/ac051437y
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-ion-consolidation

## Summary

Group multiple ion features representing the same metabolite across LC-MS samples by iteratively applying retention time similarity, abundance correlation, and EIC peak shape matching. This reduces data complexity and improves annotation by consolidating redundant signals from different ionization states or adducts of the same compound.

## When to use

After chromatographic peak detection in LC-MS data, when you have hundreds or thousands of features and need to consolidate ions presumed to originate from the same metabolite. Apply this skill when features exhibit similar retention times, correlated abundance patterns across samples, and similar extracted ion chromatogram peak shapes but represent different m/z values (e.g., [M+H]+, [M+Na]+, isotopes).

## When NOT to use

- Input data contains only singly-ionized compounds with no isotopes or adducts; grouping will not improve annotation.
- Feature detection has not yet been performed (no chromatographic peaks extracted).
- Samples have drastically different ionization conditions or chromatographic performance; abundance correlation and EIC similarity become unreliable.

## Inputs

- XcmsExperiment object with detected chromatographic peaks (output from findChromPeaks)
- Feature table with m/z, retention time, and intensity across samples
- Missing value-filled abundance matrix (from fillChromPeaks)

## Outputs

- Grouped XcmsExperiment object with consolidated feature groups
- Feature group membership table (mapping original features to group IDs)
- Count of distinct feature groups post-consolidation

## How to apply

Execute a three-stage hierarchical grouping workflow on an XcmsExperiment object. First, group features by retention time similarity using SimilarRtimeParam with a time window (typically 10 seconds). Second, refine these groups by correlation of feature abundances across samples using AbundanceSimilarityParam with a threshold (e.g., 0.7) on log2-transformed, missing-value-filled abundance data. Third, further consolidate by EIC similarity using EicSimilarityParam(threshold=0.7, n=2) to match extracted ion chromatogram peak shapes. Each stage reduces the feature group count as ions from the same compound are consolidated. Threshold selection (0.7 for correlation and EIC similarity) balances specificity and sensitivity; lower thresholds group more features but risk false positives, while higher thresholds demand stricter evidence. The rationale is that true metabolite ions co-elute, co-vary in abundance, and share peak morphology; false groupings are progressively eliminated by the combination of orthogonal criteria.

## Related tools

- **xcms** (Primary tool for LC-MS preprocessing, peak detection, and groupFeatures() implementation) — https://github.com/sneumann/xcms
- **MsFeatures** (Provides general MS feature grouping functionality and parameter classes (SimilarRtimeParam, AbundanceSimilarityParam, EicSimilarityParam))
- **MSnbase** (Defines base classes (XcmsExperiment, spectra containers) extended by xcms for grouping operations)

## Examples

```
groupFeatures(xmse, param = SimilarRtimeParam(10)); groupFeatures(xmse, AbundanceSimilarityParam(threshold = 0.7, transform = log2), filled = TRUE); groupFeatures(xmse, EicSimilarityParam(threshold = 0.7, n = 2))
```

## Evaluation signals

- Feature group count decreases monotonically through each refinement stage (e.g., retention time → abundance correlation → EIC similarity); verify final count matches expected consolidation.
- All features within a group share retention time within the specified window (e.g., ±10 seconds) and correlation coefficient ≥ threshold (0.7).
- Extracted ion chromatogram peak shapes for features in the same group are visually or quantitatively similar; EIC similarity score ≥ 0.7 threshold.
- Check that expected adducts/isotopes of known metabolites are grouped together (e.g., [M+H]+ and [M+Na]+ for the same m/z span); compare against reference standards if available.
- Validate that the final feature group count is reasonable relative to the sample matrix complexity and instrument resolution (e.g., 2289 features → 589 groups is ~75% consolidation, consistent with typical redundancy in untargeted LC-MS).

## Limitations

- Threshold selection (e.g., 0.7 for correlation and EIC similarity) is empirical and may require tuning for different metabolite classes, ionization modes, or chromatographic conditions.
- EIC similarity grouping with n=2 (top 2 samples per group) may fail to detect group members present in only one sample or at very low intensity.
- Missing or poorly detected chromatographic peaks in some samples can inflate apparent group heterogeneity if fillChromPeaks is not applied beforehand.
- Grouping assumes linear ion response and stable ionization; non-linear suppression effects or matrix-dependent ionization may violate abundance correlation assumptions.
- No changelog available to track algorithmic changes or parameter sensitivity across xcms versions.

## Evidence

- [intro] Features (ions) of the same compound should have similar retention time, similar abundance patterns across samples, and similar peak shapes of extracted ion chromatograms: "Features (ions) of the same compound should have similar retention time. - The abundance of features"
- [intro] Compounding aims at grouping such features presumably representing signal from the same originating compound to reduce data set complexity: "*Compounding* aims now at grouping such features presumably representing signal from the same originating compound to reduce data set complexity (and to aid in subsequent annotation steps)."
- [intro] Group features by retention time similarity, then refine by abundance correlation, then by EIC similarity using successive groupFeatures() calls: "- Group features by similar retention time within specified time window  [section=intro; evidence='groupFeatures(xmse, param = SimilarRtimeParam(10))'] - Refine feature groups based on correlation of"
- [other] The grouping based on EIC correlation resulted in the 2289 features being grouped into 589 distinct feature groups: "The grouping based on EIC correlation resulted in the 2289 features being grouped into 589 distinct feature groups."
- [readme] Version 4 of xcms adds native support for Spectra and MsExperiment objects with easier integration with MsFeatures for flexible feature grouping: "Version 4 adds native support for the [Spectra](https://github.com/RforMassSpectrometry/Spectra) package to `xcms` and allows to perform the pre-processing on `MsExperiment` objects (from the"
