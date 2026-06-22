---
name: drift-retention-time-alignment
description: Use when you have GCIMS samples exhibiting misalignment across drift time (typically 5–16 ms range) and retention time (typically 0–1100 s range) caused by pressure/temperature fluctuations or chromatographic column degradation, and you need to normalize sample positions before downstream peak.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
  tools:
  - R
  - GCIMS
  - ggplot2
  - cowplot
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# drift-retention-time-alignment

## Summary

Aligns Gas Chromatography–Ion Mobility Spectrometry (GCIMS) samples across both drift time and retention time dimensions to correct for instrument and column degradation-induced misalignments. This skill is essential for preprocessing GCIMS data before peak detection and clustering.

## When to use

Apply this skill when you have GCIMS samples exhibiting misalignment across drift time (typically 5–16 ms range) and retention time (typically 0–1100 s range) caused by pressure/temperature fluctuations or chromatographic column degradation, and you need to normalize sample positions before downstream peak detection or comparative analysis.

## When NOT to use

- Data is already peak-detected or peak-clustered; alignment operates on raw or lightly preprocessed ion matrices, not peak tables.
- Samples originate from different analytical methods or instruments with incompatible drift time / retention time scales.
- Retention time or drift time range is not known or meaningful (e.g., single-point measurements or non-temporal data).

## Inputs

- GCIMSDataset object (loaded from raw GCIMS data files)
- raw ion mobility spectrometry matrix with drift time and retention time dimensions
- sample annotation metadata (optional but recommended)

## Outputs

- aligned GCIMSDataset object with corrected drift time and retention time coordinates
- Total Ion Spectra (TIS) plot showing overlaid aligned samples
- Reverse Ion Chromatogram (RIC) plot showing aligned chromatographic profiles

## How to apply

First, filter the GCIMS dataset to the target retention time range (e.g., 0–1100 s) and drift time range (e.g., 5–16 ms) using filterRt() and filterDt(). Apply Savitzky-Golay smoothing independently in both the drift time and retention time dimensions to reduce noise and stabilize alignment features. Decimate the matrix by taking 1 every Nd points in drift time and 1 every Nr points in retention time to reduce computational cost and memory usage. Finally, perform sequential alignment: first align all samples in drift time, then align in retention time. Visual confirmation via Total Ion Spectra and Reverse Ion Chromatogram plots should show overlapped sample traces across both dimensions, indicating successful alignment.

## Related tools

- **GCIMS** (R package implementing the drift-time and retention-time alignment pipeline; provides filterRt(), filterDt(), Savitzky-Golay smoothing, decimation, and alignment functions) — https://github.com/sipss/GCIMS
- **R** (statistical computing environment in which GCIMS runs)
- **ggplot2** (visualization of aligned Total Ion Spectra and Reverse Ion Chromatogram plots for quality assessment)
- **cowplot** (multi-panel layout and arrangement of alignment diagnostic plots)

## Examples

```
filterDt(filterRt(dataset, rt = c(0, 1100)), dt = c(5, 16)) %>% smoothSG() %>% decimate(Nd = 10, Nr = 10) %>% alignDt() %>% alignRt()
```

## Evaluation signals

- Total Ion Spectra plots show visually overlapped sample traces across the full drift time and retention time ranges with minimal dispersion or skew.
- Reverse Ion Chromatogram plots display aligned chromatographic peaks at consistent retention time positions across all samples.
- Peak alignment consistency: after alignment, replicate or related samples show matching drift time and retention time coordinates for corresponding features (quantified by cross-correlation or peak-matching algorithms).
- Memory footprint reduction: decimated and aligned dataset occupies significantly less RAM than pre-decimation raw data, with no loss of interpretable structure.
- Downstream peak detection (via peakDetection) produces consistent peak lists across aligned samples with minimal noise-driven false positives.

## Limitations

- Alignment assumes that misalignment is caused by systematic instrumental/environmental drift; if samples have genuine chemical or biological differences in retention or drift time, over-alignment may obscure those differences.
- Choice of decimation factors (Nd, Nr) and Savitzky-Golay filter parameters (window length, polynomial order) requires manual tuning and optimization per dataset; no fully automated parameter selection is described.
- Alignment is sequential (drift time first, then retention time); this ordering may not be optimal for all datasets and could introduce coupling artifacts if the two dimensions are strongly dependent.
- No changelog or version history provided; reproducibility across GCIMS package versions is not documented.

## Evidence

- [intro] misalignment_causes: "Pressure and temperature fluctuations as well as degradation of the chromatographic column are some of the causes of misalignments in the data, both in retention and drift time."
- [intro] alignment_procedure: "The alignment will happen first in drift time and afterwards in retention time."
- [intro] filter_retention_time: "filterRt(dataset, rt = c(0, 1100)) # in s"
- [intro] filter_drift_time: "filterDt(dataset, dt = c(5, 16)) # in ms"
- [intro] smoothing_method: "You can remove noise from your sample using a Savitzky-Golay filter, applied both in drift time and in retention time."
- [intro] decimation_rationale: "One way to speed up calculations and reduce the memory requirements is to decimate the matrix, by taking 1 every Nd points in drift time and 1 every Nr points in retention time."
- [other] visual_validation: "the Total Ion Spectra and Reverse Ion Chromatogram plots show visual alignment of samples across both drift time and retention time dimensions."
- [intro] delayed_evaluation_efficiency: "GCIMS uses delayed evaluations were possible, so dataset modifications can be executed in a more efficient way and without using too much RAM."
- [readme] gcims_package_purpose: "GCIMS is an R package implementing a preprocessing pipeline for Gas Chromatography – Ion Mobility Spectrometry samples."
