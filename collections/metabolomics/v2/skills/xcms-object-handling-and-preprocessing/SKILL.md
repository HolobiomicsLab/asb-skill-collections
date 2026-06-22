---
name: xcms-object-handling-and-preprocessing
description: Use when you have raw gas or liquid chromatography–mass spectrometry data (in NetCDF or mzML format) and need to detect features, align them across samples by retention time and mass-to-charge ratio, correct for retention time drift, and fill missing values before downstream metabolite clustering.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - RAMClustR
  - dynamicTreeCut
  - XCMS
  - R
  - InterpretMSSpectrum
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/ac501530d
  title: RAMClust
evidence_spans:
- ramclustR function is built to use xcms data
- RC <- ramclustR(xcmsObj = xset, ExpDes=experiment)
- submitting this score matrix for heirarchical clustering, and then cutting the resulting dendrogram into neat chunks using the dynamicTreeCut package
- cutting the resulting dendrogram into neat chunks using the dynamicTreeCut package
- XCMS is a commonly used tool to detect all the signals from a metabolomics dataset, generating aligned features
- XCMS is a commonly used tool to detect all the signals from a metabolomics dataset
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ramclust_cq
    doi: 10.1021/ac501530d
    title: RAMClust
  dedup_kept_from: coll_ramclust_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/ac501530d
  all_source_dois:
  - 10.1021/ac501530d
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# xcms-object-handling-and-preprocessing

## Summary

Prepare raw mass spectrometry data for downstream metabolomics analysis by applying XCMS feature detection, alignment, retention time correction, and missing value imputation. This preprocessing pipeline transforms raw NetCDF/mzML files into a grouped feature matrix suitable for clustering and annotation.

## When to use

You have raw gas or liquid chromatography–mass spectrometry data (in NetCDF or mzML format) and need to detect features, align them across samples by retention time and mass-to-charge ratio, correct for retention time drift, and fill missing values before downstream metabolite clustering or annotation.

## When NOT to use

- Input is already a preprocessed feature table or intensity matrix (e.g., CSV with features as rows and samples as columns) — skip directly to clustering.
- Data has already undergone XCMS processing and retention time correction — avoid re-running to prevent over-alignment artifacts.
- Instrument data is in proprietary vendor formats not supported by XCMS (e.g., raw Bruker .d or Waters .raw without prior conversion) — convert to open formats first.

## Inputs

- Raw mass spectrometry data files (NetCDF, mzML, or CDF format)
- Sample metadata or experiment design (optional, but recommended for downstream steps)

## Outputs

- XCMS xcmsSet object containing grouped and aligned features
- Feature-by-sample intensity matrix with filled missing values
- Feature metadata including retention time, m/z, and sample groupings

## How to apply

Execute the XCMS preprocessing workflow in sequence: (1) Load raw instrument files using xcmsSet() to perform centroid feature detection across all samples. (2) Group features across samples by retention time and m/z using group() with default parameters (mass tolerance ~0.015 Da, retention time window ~60 s). (3) Correct for systematic retention time drift across the analytical run using retcor() with symmetric family setting to align features between samples. (4) Regroup features after retention time correction using group() again with slightly relaxed bandwidth (bw = 10) to account for post-correction variation. (5) Impute missing values using fillPeaks() to ensure a complete feature-by-sample intensity matrix. The output xcmsSet object contains aligned, grouped features ready for unsupervised clustering methods like RAMClustR that rely on consistent retention time and intensity correlation structure.

## Related tools

- **XCMS** (Core tool for feature detection, grouping, and retention time correction of raw mass spectrometry data)
- **dynamicTreeCut** (Used by downstream tools (e.g., RAMClustR) for hierarchical clustering of aligned features; not directly part of preprocessing but depends on XCMS preprocessing output)

## Examples

```
xset <- xcmsSet(cdffiles); xset <- group(xset); xset <- retcor(xset, family="symmetric", plottype=NULL); xset <- group(xset, bw=10); xset <- fillPeaks(xset)
```

## Evaluation signals

- xcmsSet object contains non-zero feature count and feature matrix dimensions match expected (features × samples)
- Retention time values across samples show tight clustering after retcor() and regroup() for features from the same compound (typically ±10 s)
- Missing value rate after fillPeaks() is zero or near-zero; SpecAbund matrix has no NA values
- Feature intensity distributions before and after fillPeaks() are comparable (filled intensities do not dominate or skew global statistics)
- xcmsSet can be successfully passed to downstream tools (e.g., ramclustR(xcmsObj = xset)) without schema errors

## Limitations

- Retention time correction assumes that the majority of detected features are real signals; high background or contamination can distort alignment.
- Missing value imputation via fillPeaks() uses zero or minimum intensity logic and may introduce bias for features genuinely absent in some samples.
- XCMS parameters (mass tolerance, retention time window, bandwidth) are heuristic and may require optimization for different instrument types or sample complexity.
- No built-in changelog or version history documented; breaking changes between XCMS versions may affect reproducibility.

## Evidence

- [intro] Feature detection and grouping workflow overview: "xset <- xcmsSet(cdffiles)  # detect features"
- [intro] Retention time grouping step: "xset <- group(xset)  # group features across samples by retention time and mass"
- [intro] Retention time drift correction: "xset <- retcor(xset, family = "symmetric", plottype = NULL)  # correct for drive in retention time"
- [intro] Regroup after retention time correction: "xset <- group(xset, bw = 10)  # regroup following rt correction"
- [intro] Missing value imputation: "xset <- fillPeaks(xset)  # 'fillPeaks' to remove missing values in final dataset"
- [intro] XCMS purpose and integration: "XCMS is a commonly used tool to detect all the signals from a metabolomics dataset, generating aligned features"
- [intro] Features from same compound alignment property: "two features derived from the same compound with have (approximately) the same retention time"
