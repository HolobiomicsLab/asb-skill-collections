---
name: peak-detection-cwt-optimization
description: Use when when you have a pre-aligned GCIMSDataset and need to systematically
  identify and annotate chromatographic peaks across multiple samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3630
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
  tools:
  - R
  - GCIMS
  techniques:
  - GC-MS
  - ion-mobility-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1016/j.chemolab.2023.104938
  title: GCIMS
evidence_spans:
- library(ggplot2) library(cowplot) library(GCIMS)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_gcims_cq
    doi: 10.1016/j.chemolab.2023.104938
    title: GCIMS
  dedup_kept_from: coll_gcims_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1016/j.chemolab.2023.104938
  all_source_dois:
  - 10.1016/j.chemolab.2023.104938
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# peak-detection-cwt-optimization

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Optimize Continuous Wavelet Transform (CWT) parameters and peak detection settings to accurately identify peaks across Gas Chromatography–Ion Mobility Spectrometry (GCIMS) samples. This skill determines noise thresholds and algorithmic parameters that maximize peak detection sensitivity while minimizing false positives in both drift time and retention time dimensions.

## When to use

When you have a pre-aligned GCIMSDataset and need to systematically identify and annotate chromatographic peaks across multiple samples. Use this skill after alignment has corrected for retention time and drift time misalignment caused by pressure/temperature fluctuations or column degradation, and before peak clustering or downstream feature extraction.

## When NOT to use

- Input data is unaligned in retention time or drift time; alignment must precede peak detection.
- Peak detection has already been performed on the same dataset; re-running risks duplicating or contradicting previous annotations.
- The dataset contains only raw, unsmoothed GCIMS matrices; apply Savitzky–Golay filtering and decimation before peak detection to improve signal-to-noise ratio.

## Inputs

- pre-aligned GCIMSDataset object (in-memory R object from library(GCIMS))
- optimized noise_level parameter (numeric, determined from single-sample tuning)
- aligned retention time and drift time dimensions (post-alignment ranges, typically 0–1100 s and 5–16 ms respectively)

## Outputs

- peak_list table (per-sample tabular output with retention time, drift time, and intensity annotations)
- CWT parameter configuration (reproducible settings: exclude0scaleAmpThresh, extension factors, RIP exclusion flag, IOU threshold)

## How to apply

Begin by loading the aligned GCIMSDataset in R using library(GCIMS). Apply findPeaks with CWT algorithm on a single representative sample to optimize the noise_level parameter empirically, observing the trade-off between detection sensitivity and noise suppression. Once noise_level is tuned, execute findPeaks across all samples using consistent CWT parameters: exclude0scaleAmpThresh=TRUE for both drift time and retention time dimensions, extension factors of 0, RIP exclusion enabled (exclude_rip=TRUE to suppress Reactant Ion Peak artifacts), and an Intersection-over-Union overlap threshold of 0.2 to avoid redundant peak assignments. The function generates a per-sample peak_list table containing retention time, drift time, and intensity annotations for each detected peak.

## Related tools

- **GCIMS** (R package providing findPeaks function with CWT algorithm, dataset alignment, and peak annotation infrastructure) — https://github.com/sipss/GCIMS
- **R** (Host language for GCIMS library and peak detection workflow execution)

## Examples

```
findPeaks(dataset, noise_level = 0.05, exclude0scaleAmpThresh = TRUE, extension = 0, exclude_rip = TRUE, iou_threshold = 0.2)
```

## Evaluation signals

- peak_list table is non-empty and contains valid retention time (0–1100 s range), drift time (5–16 ms range), and positive intensity values for all samples.
- Reproducibility check: re-running findPeaks with identical noise_level and CWT parameters on the same sample produces identical peak_list output.
- RIP exclusion is effective: Reactant Ion Peak artifacts (typically at characteristic drift time values near 0 ms) are absent from the peak_list when exclude_rip=TRUE; peaks reappear if flag is set to FALSE.
- IOU overlap threshold (0.2) prevents peak redundancy: no two peaks in the same sample have Intersection-over-Union > 0.2 in the (retention time, drift time) feature space.
- Parameter consistency across samples: noise_level, exclude0scaleAmpThresh, extension factors, and IOU threshold are uniform across all samples in the dataset.

## Limitations

- Peak detection accuracy depends critically on prior alignment quality; misalignments in retention or drift time propagate into false negatives or shifted peak annotations.
- The noise_level parameter requires manual empirical tuning on representative samples; no automatic parameter optimization algorithm is documented in the article.
- CWT parameters (exclude0scaleAmpThresh, extension factors, IOU threshold) are fixed in the article; their sensitivity to different sample classes, ionization conditions, or column chemistries is not explored.
- Reactant Ion Peak exclusion (exclude_rip=TRUE) assumes RIP occurs at known drift time values; atypical RIP behavior or shifted RIP location due to instrumental drift may not be fully suppressed.

## Evidence

- [other] Peak detection in the aligned GCIMS dataset is performed using findPeaks with CWT parameters including exclude0scaleAmpThresh=TRUE for both drift time and retention time dimensions, extension factors of 0, RIP exclusion enabled, and an IOU overlap threshold of 0.2: "Peak detection in the aligned GCIMS dataset is performed using findPeaks with CWT parameters including exclude0scaleAmpThresh=TRUE for both drift time and retention time dimensions, extension factors"
- [other] Apply the findPeaks function with CWT algorithm and documented noise_level parameter optimization on the first sample to determine optimal settings: "Apply the findPeaks function with CWT algorithm and documented noise_level parameter optimization on the first sample to determine optimal settings"
- [other] Execute findPeaks across all samples in the aligned dataset using the optimized CWT parameters and exclude_rip = TRUE to suppress Reactant Ion Peak detection: "Execute findPeaks across all samples in the aligned dataset using the optimized CWT parameters and exclude_rip = TRUE to suppress Reactant Ion Peak detection"
- [other] Generate the per-sample peak_list table as structured output containing detected peaks with retention time, drift time, and intensity annotations: "Generate the per-sample peak_list table as structured output containing detected peaks with retention time, drift time, and intensity annotations"
- [intro] Pressure and temperature fluctuations as well as degradation of the chromatographic column are some of the causes of misalignments in the data, both in retention and drift time: "Pressure and temperature fluctuations as well as degradation of the chromatographic column are some of the causes of misalignments in the data, both in retention and drift time"
