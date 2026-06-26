---
name: reactant-ion-peak-exclusion
description: Use when when performing peak detection on Gas Chromatography–Ion Mobility
  Spectrometry samples where the Reactant Ion Peak (a high-intensity background signal
  from the ion source) would otherwise be misidentified as an analyte peak, causing
  false positives in the peak list.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_0121
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

# reactant-ion-peak-exclusion

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Suppress detection of Reactant Ion Peaks (RIP) during GCIMS peak detection to avoid false positives from instrument noise. RIP exclusion is a filtering parameter applied during the CWT-based findPeaks step to ensure only true analyte peaks are retained in the peak_list output.

## When to use

When performing peak detection on Gas Chromatography–Ion Mobility Spectrometry samples where the Reactant Ion Peak (a high-intensity background signal from the ion source) would otherwise be misidentified as an analyte peak, causing false positives in the peak list.

## When NOT to use

- When RIP signal itself is the analytical target (e.g., studying ion source behavior or instrument diagnostics)
- When working with datasets where RIP has already been removed by hardware filtering or preprocessing steps
- On non-ion-mobility or non-GCIMS data where the concept of a Reactant Ion Peak does not apply

## Inputs

- aligned GCIMSDataset object (post-alignment in both drift time and retention time)
- CWT algorithm parameters (noise_level, exclude0scaleAmpThresh, extension factors)

## Outputs

- peak_list table with RIP-free detected peaks (columns: retention time, drift time, intensity)

## How to apply

Set the exclude_rip parameter to TRUE when invoking the findPeaks function with CWT algorithm on an aligned GCIMSDataset object. This suppresses RIP detection during the peak-finding phase across all samples in the dataset. The RIP typically appears as a strong signal at characteristic drift and retention times and, without exclusion, would dominate the peak list and interfere with downstream peak clustering and compound identification. Apply this setting consistently across all samples to ensure comparable peak detection.

## Related tools

- **GCIMS** (R package providing the findPeaks function with exclude_rip parameter) — https://github.com/sipss/GCIMS
- **R** (Execution environment for GCIMS and peak detection workflow)

## Examples

```
library(GCIMS); peak_list <- findPeaks(aligned_dataset, exclude_rip = TRUE, noise_level = <optimized_value>)
```

## Evaluation signals

- Peak list does not contain high-intensity signals at the characteristic RIP retention and drift time coordinates
- Number of detected peaks is reduced compared to peak detection without RIP exclusion (exclude_rip = FALSE)
- Downstream peak clustering results in distinct, chemically interpretable compound clusters without a dominant high-intensity outlier
- Per-sample peak intensity distributions show removal of the characteristic RIP intensity spike
- Output peak_list schema validation passes with all required columns (retention time, drift time, intensity) and no unexpected RIP markers

## Limitations

- RIP exclusion requires prior knowledge or empirical determination of RIP position in drift and retention time space; misidentification of RIP coordinates can lead to loss of genuine analyte peaks
- Effectiveness depends on proper prior alignment of the dataset in both drift time and retention time; misaligned data may place RIP at varying positions, reducing exclusion effectiveness
- Cannot distinguish RIP from very early-eluting, high-abundance analytes if they co-localize in drift–retention time space; user must validate peak assignments

## Evidence

- [intro] Apply the findPeaks function with CWT algorithm and documented noise_level parameter optimization on the first sample to determine optimal settings.: "Apply the findPeaks function with CWT algorithm and documented noise_level parameter optimization"
- [intro] Execute findPeaks across all samples in the aligned dataset using the optimized CWT parameters and exclude_rip = TRUE to suppress Reactant Ion Peak detection.: "Execute findPeaks across all samples in the aligned dataset using the optimized CWT parameters and exclude_rip = TRUE to suppress Reactant Ion Peak detection"
- [intro] Exclude RIP (Reactant Ion Peak) during peak detection: "Exclude RIP (Reactant Ion Peak) during peak detection"
- [intro] Generate the per-sample peak_list table as structured output containing detected peaks with retention time, drift time, and intensity annotations.: "Generate the per-sample peak_list table as structured output containing detected peaks with retention time, drift time, and intensity annotations"
