---
name: mass-chromatogram-alignment
description: Use when after chromatographic peak detection on preprocessed LC-MS data, when you have detected features (peaks) in multiple samples and need to establish which peaks across samples represent the same molecular species.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0091
  tools:
  - MsFeatures
  - xcms
  - MsExperiment
  - Spectra
  techniques:
  - LC-MS
  - GC-MS
  - tandem-MS
derived_from:
- doi: 10.1021/ac051437y
  title: XCMS
evidence_spans:
- General MS feature grouping functionality if defined by the `r Biocpkg("MsFeatures")` package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_xcms
    doi: 10.1021/ac051437y
    title: XCMS
  dedup_kept_from: coll_xcms
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

# mass-chromatogram-alignment

## Summary

Align extracted ion chromatograms (EICs) across multiple LC-MS samples to enable feature correspondence and abundance quantification. This skill groups features detected in different samples by matching their m/z and retention time coordinates, producing a unified feature matrix suitable for statistical and metabolomic analysis.

## When to use

After chromatographic peak detection on preprocessed LC-MS data, when you have detected features (peaks) in multiple samples and need to establish which peaks across samples represent the same molecular species. This is essential when building a feature abundance table for comparative analysis across sample groups (e.g., wild-type vs. knockout mice).

## When NOT to use

- If input is already a feature table with abundances already aligned across samples; alignment has been completed.
- If only a single sample is being analyzed; correspondence requires multiple samples to group and match features.
- If chromatographic peaks have not yet been detected; peak detection must precede alignment.

## Inputs

- XcmsExperiment or xcmsSet object with detected chromatographic peaks
- Numerical m/z values and retention time coordinates of detected peaks
- Feature abundance (intensity) values across all samples
- Raw or centroided mass spectrometry data (mzML, netCDF, or other xcms-supported format)

## Outputs

- Feature group assignments (mapping of features to groups)
- Feature group table (rows: features/groups; columns: samples; values: integrated peak intensities)
- Count and distribution of features per group
- Gap-filled abundance matrix with missing values recovered

## How to apply

Load the xcms result object (XcmsExperiment or xcmsSet) containing detected chromatographic peaks. Apply a multi-stage grouping strategy: (1) perform initial retention time-based grouping using SimilarRtimeParam with a window appropriate to your chromatographic resolution (e.g., 20 seconds for typical LC-MS); (2) refine grouped features by correlating their abundance patterns across samples using AbundanceSimilarityParam to split false positives; (3) further validate groups by computing extracted ion chromatogram (EIC) similarity using EicSimilarityParam. Extract the resulting feature group assignments and compute summary statistics (total group count, features per group) to verify the grouping produced a reasonable distribution. Perform gap-filling to integrate missing signal from m/z–retention time ranges defined by detected peaks in samples where peaks were not detected, recovering absent feature abundances.

## Related tools

- **xcms** (Primary package providing groupFeatures() method, SimilarRtimeParam, AbundanceSimilarityParam, EicSimilarityParam, and gap-filling functionality for LC-MS feature alignment and correspondence) — https://github.com/sneumann/xcms
- **MsFeatures** (Provides general MS feature grouping functionality and parameter classes for retention time, abundance correlation, and EIC similarity-based alignment)
- **MsExperiment** (Data container for preprocessed LC-MS experiments and feature groups, enabling flexible representation of aligned features and metadata)
- **Spectra** (Backend for storing and accessing MS2 spectra associated with aligned chromatographic peaks and feature groups)

## Examples

```
groupFeatures(xe, SimilarRtimeParam(20)) %>% groupFeatures(AbundanceSimilarityParam()) %>% groupFeatures(EicSimilarityParam()) # Align features by retention time (20s window), then refine by abundance correlation and EIC similarity
```

## Evaluation signals

- Total number of feature groups matches expected reference values or remains within reasonable bounds (e.g., fewer groups than input features due to consolidation).
- Distribution of feature counts per group shows predominantly singleton and small groups, with larger groups representing isotopes and adducts of the same compound.
- Gap-filled feature abundance table has no missing values in the m/z–retention time windows defined by detected peaks.
- Features within each group have highly correlated abundance patterns across samples (high Pearson/Spearman correlation in AbundanceSimilarityParam refinement step).
- EIC similarity analysis (EicSimilarityParam) does not split groups further, indicating robust alignment; if further splitting occurs, groups may be too loose and benefit from tighter retention time tolerance.

## Limitations

- Retention time-based grouping may oversplit true feature groups if retention time shifts occur across samples or underfitting occurs due to long window width; subsequent abundance and EIC similarity refinement help mitigate this but cannot fully recover oversplit groups.
- For some samples, chromatographic peaks are not detected at feature locations even though signal is present in raw data, necessitating gap-filling; gap-filling assumes signal intensity from the defined m/z–retention time window is homogeneous and may not recover heavily suppressed or completely absent peaks.
- The choice of retention time window (e.g., 20 seconds) is data- and instrument-dependent; a fixed threshold may fail on high-resolution or drift-prone LC systems; user must validate window choice against their chromatographic stability.
- EIC similarity computation is computationally expensive for large datasets; parallel processing via BiocParallel is available but memory/CPU scaling is implementation-dependent.

## Evidence

- [intro] Retention time-based grouping is the first step; parameters and rationale: "SimilarRtimeParam: perform an initial grouping based on similar retention time."
- [intro] Abundance correlation used to refine and split oversized groups: "AbundanceSimilarityParam: perform a feature grouping based on correlation of feature abundances (values) across samples."
- [intro] EIC similarity provides additional validation and sub-grouping: "EicSimilarityParam: perform a feature grouping based on correlation of EICs."
- [intro] Gap-filling workflow for missing feature abundances: "for samples in which no chromatographic peak for a feature was detected, all signal from the m/z - retention time range defined based on the detected chromatographic peaks was integrated."
- [intro] Multi-stage grouping results in progressive refinement: "Grouping by similar retention time grouped the in total features into feature groups. Many of the larger retention time-based feature groups have been splitted into two or more sub-groups based on"
- [readme] xcms package provides core alignment functionality: "The *xcms* R package provides functionality to efficiently preprocess LC-MS (as well as GC-MS and LC-MS/MS) data."
- [readme] Version 4 integration with MsExperiment and Spectra for flexible alignment: "Version 4 adds native support for the [Spectra] package to `xcms` and allows to perform the pre-processing on `MsExperiment` objects"
