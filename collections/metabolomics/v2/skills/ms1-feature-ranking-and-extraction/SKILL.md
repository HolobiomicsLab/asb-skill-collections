---
name: ms1-feature-ranking-and-extraction
description: Use when when you have raw LC-MS data files and need to identify which
  compounds were actually detected at high abundance during a gradient run, prior
  to evaluating whether the gradient provided good separation across the chemical
  space.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3645
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - Python
  - Jupyter Notebook
  - bago
  - pyopenms
  - MZmine 3
  - XCMS
  techniques:
  - LC-MS
  - ion-mobility-MS
  license_tier: restricted
derived_from:
- doi: 10.1101/2023.09.08.556930
  title: BAGO
- doi: 10.1002/9780470508183
  title: ''
evidence_spans:
- Download and install Python 3.8 or later from `python.org`
- model.computeNextGradient()
- A Jupyter Notebook is provided to help you get started with the LC gradient optimization
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_bago_cq
    doi: 10.1101/2023.09.08.556930
    title: BAGO
  dedup_kept_from: coll_bago_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2023.09.08.556930
  all_source_dois:
  - 10.1101/2023.09.08.556930
  - 10.1002/9780470508183
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# MS1 Feature Ranking and Extraction

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Identifies and ranks the most abundant MS1 features from raw LC-MS data, extracting their retention times for downstream separation efficiency evaluation. This skill bridges raw instrument data to omics-scale compound separation metrics used in gradient optimization.

## When to use

When you have raw LC-MS data files and need to identify which compounds were actually detected at high abundance during a gradient run, prior to evaluating whether the gradient provided good separation across the chemical space. Specifically, apply this skill when you want to encode separation performance at omics scale by ranking detected features rather than assuming all theoretical compounds are resolved.

## When NOT to use

- Input is already a processed feature table or peak list; use this skill only on raw instrument data.
- You are interested in targeted analysis of a known list of compounds; this skill ranks by abundance, not by compound identity.
- The LC-MS run produced no detectable signals above noise; extraction will fail or return an empty feature set.

## Inputs

- Raw LC-MS data file (mzML, mzXML, or vendor binary format)
- Gradient time range (rtRange: start and end time in minutes)

## Outputs

- List of top MS1 features (feature objects or m/z–retention time pairs)
- Retention time sequence (rtSeq) sorted by feature abundance or elution order
- Ranked feature metadata (m/z, intensity, scan number, retention time)

## How to apply

Read the raw LC-MS data file into an MSExperiment object using readRawData. Extract all MS1 scans and convert them to ms1Spectrum objects using extractMS1. Apply the findTopSignals function to identify the most intense signals in the MS1 data, which are the compounds actually detected. Collect the retention times of these top-ranked features into a sequence (rtSeq) aligned with the gradient time range (rtRange). The rationale is that only features present above background noise contribute to separation efficiency; ranking by intensity ensures the metric reflects realistic compound detection and avoids biasing the separation score toward theoretical but undetectable species.

## Related tools

- **bago** (Provides ms1Spectrum objects, findTopSignals, extractMS1, and readRawData functions for MS1 feature extraction and ranking.) — https://github.com/huaxuyu/bago
- **pyopenms** (Supplies MSExperiment data structure for loading and manipulating raw LC-MS data.)
- **MZmine 3** (Alternative tool for MS1 feature detection and ranking in graphical environment.) — http://mzmine.github.io/
- **XCMS** (Alternative R-based tool for MS1 peak detection and feature extraction.) — https://www.bioconductor.org/packages/release/bioc/html/xcms.html

## Examples

```
from bago import readRawData, extractMS1, findTopSignals; exp = readRawData('sample.mzML'); ms1_spectra = extractMS1(exp); top_features = findTopSignals(ms1_spectra); rtSeq = [f.retention_time for f in top_features]
```

## Evaluation signals

- The returned rtSeq contains only finite, positive retention times within the specified rtRange; no NaN or out-of-range values.
- Feature count is non-zero and represents a realistic subset of the total m/z × time grid (e.g., 10–1000 features for a typical untargeted metabolomics run).
- Retention times are sorted monotonically or match the order of MS1 scans; features with higher intensity appear first or are flagged as 'top'.
- Each feature object or tuple includes m/z, retention time, and intensity; metadata is complete and consistent with the raw data file header.
- The rtSeq can be successfully passed to the downstream sepEfficiency function without type or range errors, confirming encoding compatibility.

## Limitations

- Feature extraction depends on signal-to-noise ratio thresholds, which may vary by instrument and sample matrix; low-abundance compounds are missed.
- Ranking by intensity alone does not account for mass accuracy, isotope pattern validation, or chemical plausibility; chemical noise peaks may rank highly.
- Retention time precision is limited by MS scan frequency; dense gradients with many features may yield artifactually coarse rtSeq spacing.
- The approach assumes LC-MS1 data; it is not applicable to MS/MS-only data or ion mobility spectrometry without adaptation.

## Evidence

- [methods] Function to find the top signals in the raw LCMS data: "findTopSignals - find top signals in MS1 data"
- [methods] Extract MS1 scans and convert to spectrum objects: "extractMS1 - extract MS1 scans and convert to ms1Spectrum objects"
- [methods] Read raw data into MSExperiment object: "readRawData - read raw LC-MS data into MSExperiment object"
- [methods] Separation efficiency uses retention times from top detected features: "Extract or receive a series of retention times (rtSeq) from the top detected MS1 features"
- [intro] Omics-scale separation evaluation rationale: "Separation efficiency was defined to evaluate the performance of a gradient."
