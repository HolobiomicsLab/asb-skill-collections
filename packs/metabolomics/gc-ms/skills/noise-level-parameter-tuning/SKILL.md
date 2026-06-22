---
name: noise-level-parameter-tuning
description: Use when when you have an aligned GCIMS dataset and need to configure the findPeaks function with CWT algorithm to detect peaks across retention time and drift time dimensions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3627
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3370
  tools:
  - R
  - GCIMS
  techniques:
  - GC-MS
  - ion-mobility-MS
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

# noise-level-parameter-tuning

## Summary

Optimize the noise_level parameter for CWT-based peak detection in GCIMS samples by iterative testing on a representative sample before applying to the full dataset. This parameter controls the sensitivity threshold for distinguishing true peaks from noise in Gas Chromatography–Ion Mobility Spectrometry data.

## When to use

When you have an aligned GCIMS dataset and need to configure the findPeaks function with CWT algorithm to detect peaks across retention time and drift time dimensions. Tuning is necessary because noise_level directly affects peak detection sensitivity and specificity, and optimal values vary with instrument settings, sample composition, and preprocessing (smoothing, decimation) applied to your specific dataset.

## When NOT to use

- Input data has not been aligned in drift time and retention time — alignment must precede peak detection parameter optimization.
- Peak detection parameters are already specified by external validated protocols or prior publications for your exact instrument and sample type — reuse published settings instead of re-tuning.
- You are performing exploratory screening where approximate peak lists are acceptable; noise_level tuning is necessary only when reproducible, calibrated peak detection is required.

## Inputs

- aligned GCIMSDataset object (R object with preprocessed, decimated, smoothed, and aligned samples)
- representative sample index or sample name for parameter tuning

## Outputs

- optimized noise_level parameter value (numeric)
- per-sample peak_list table with detected peaks (columns: retention time, drift time, intensity)

## How to apply

Load the aligned GCIMSDataset object in R and apply the findPeaks function with CWT parameters to a single representative sample from your dataset. Systematically vary the noise_level parameter while inspecting the resulting peak_list output to identify the threshold that maximizes true peak detection while suppressing RIP and noise artifacts. Document the optimal noise_level value, then execute findPeaks across all samples in the aligned dataset using the tuned noise_level together with other CWT settings (exclude0scaleAmpThresh=TRUE, extension factors=0, exclude_rip=TRUE, IOU threshold=0.2). Validate that the per-sample peak_list tables show consistent peak annotations across samples with expected retention time and drift time ranges.

## Related tools

- **GCIMS** (R package providing findPeaks function with CWT algorithm and noise_level parameter for peak detection on aligned GCIMS datasets) — https://github.com/sipss/GCIMS
- **R** (Computing environment for loading GCIMSDataset, executing findPeaks with parameter sweeps, and iteratively inspecting peak_list outputs)

## Examples

```
library(GCIMS); data(threeketones); findPeaks(threeketones[[1]], noise_level=500, exclude_rip=TRUE)
```

## Evaluation signals

- Peak detection produces a non-empty peak_list table for the test sample with peaks present in expected retention time and drift time ranges.
- RIP (Reactant Ion Peak) artifacts are suppressed in the peak_list when exclude_rip=TRUE is applied with the tuned noise_level.
- Peaks detected across all samples show consistent retention time and drift time annotations (within expected variance from sample-to-sample alignment accuracy).
- Visual inspection of the peak_list overlaid on the heatmap of the aligned 2D GC×IMS data confirms peaks are localized to genuine chemical signal regions and not noise-dominated zones.
- Comparing peak_list from two adjacent samples (e.g., technical replicates) shows high overlap in detected peak positions, indicating the noise_level threshold is appropriately calibrated for signal/noise separation.

## Limitations

- Optimal noise_level is dataset- and instrument-specific; values tuned on one sample may not generalize if instrumental conditions, column degradation, or sample composition differ significantly across the batch.
- No automated algorithm is provided for noise_level selection; tuning requires manual inspection and iterative testing, which can be time-consuming for datasets with many samples or high dimensionality.
- The article does not specify quantitative metrics (e.g., sensitivity, specificity, false discovery rate) for validating noise_level choice; success relies on visual or domain-expert judgment of the peak_list.
- Interaction effects between noise_level and other CWT parameters (exclude0scaleAmpThresh, extension factors, IOU threshold) are not explicitly characterized; simultaneous optimization of multiple parameters is not addressed.

## Evidence

- [intro] First try one sample and optimize the `noise_level` parameter there.: "First try one sample and optimize the `noise_level` parameter there."
- [other] Apply the findPeaks function with CWT algorithm and documented noise_level parameter optimization on the first sample to determine optimal settings.: "Apply the findPeaks function with CWT algorithm and documented noise_level parameter optimization on the first sample to determine optimal settings."
- [other] Execute findPeaks across all samples in the aligned dataset using the optimized CWT parameters and exclude_rip = TRUE to suppress Reactant Ion Peak detection.: "Execute findPeaks across all samples in the aligned dataset using the optimized CWT parameters and exclude_rip = TRUE to suppress Reactant Ion Peak detection."
- [other] Generate the per-sample peak_list table as structured output containing detected peaks with retention time, drift time, and intensity annotations.: "Generate the per-sample peak_list table as structured output containing detected peaks with retention time, drift time, and intensity annotations."
- [readme] GCIMS is an R package implementing a preprocessing pipeline for Gas Chromatography – Ion Mobility Spectrometry samples.: "GCIMS is an R package implementing a preprocessing pipeline for Gas Chromatography – Ion Mobility Spectrometry samples."
