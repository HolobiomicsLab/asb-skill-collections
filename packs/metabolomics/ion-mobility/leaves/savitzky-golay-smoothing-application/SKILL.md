---
name: savitzky-golay-smoothing-application
description: Use when after filtering retention time and drift time ranges on raw GCIMS samples but before decimation and alignment.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3562
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - R
  - GCIMS
  - ggplot2
  - cowplot
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# savitzky-golay-smoothing-application

## Summary

Apply Savitzky-Golay polynomial smoothing independently to both drift time and retention time dimensions of Gas Chromatography–Ion Mobility Spectrometry data to reduce noise while preserving signal features prior to alignment. This is a preprocessing step that removes high-frequency noise without over-smoothing peaks or distorting the underlying chromatographic and ion mobility structure.

## When to use

After filtering retention time and drift time ranges on raw GCIMS samples but before decimation and alignment. Use this skill when the Total Ion Spectra or 2D heatmaps show visible noise artifacts or fluctuations that could degrade downstream peak detection or sample-to-sample alignment accuracy.

## When NOT to use

- Input data has already been decimated to very coarse resolution; smoothing a pre-decimated matrix may introduce artifacts.
- Peak detection will be applied directly without alignment; verify that smoothing does not artificially broaden or shift peak positions before using.
- The GCIMS dataset has not yet been filtered to the target retention time (0–1100 s) and drift time (5–16 ms) ranges; apply filtering first.

## Inputs

- GCIMSDataset object (filtered in retention time and drift time)

## Outputs

- GCIMSDataset object with Savitzky-Golay smoothed intensity matrix in both drift time and retention time dimensions

## How to apply

Apply Savitzky-Golay smoothing separately in the drift time dimension and the retention time dimension of the GCIMSDataset object using GCIMS library functions. The filter preserves local signal structure (peaks, transitions) by fitting low-degree polynomials (typically 2–3) to small sliding windows across each dimension. The choice of window length and polynomial order affects the trade-off between noise reduction and feature preservation; smaller windows preserve finer structure but leave residual noise, while larger windows smooth more aggressively but may blur narrow peaks. After smoothing, visually inspect Total Ion Spectra and Reverse Ion Chromatogram plots to confirm that noise has been reduced and peaks remain sharp and aligned in position before proceeding to decimation and inter-sample alignment.

## Related tools

- **GCIMS** (R package providing the Savitzky-Golay smoothing functions applied in drift time and retention time dimensions of GCIMS preprocessing pipeline) — https://github.com/sipss/GCIMS
- **R** (Execution environment for GCIMS library and smoothing operations)
- **ggplot2** (Visualization of Total Ion Spectra and Reverse Ion Chromatogram plots to assess smoothing quality)
- **cowplot** (Multi-panel arrangement of smoothed spectra for visual inspection and comparison)

## Examples

```
library(GCIMS); dataset_smoothed <- dataset %>% filterRt(rt = c(0, 1100)) %>% filterDt(dt = c(5, 16)) # then apply smoothing in GCIMS workflow
```

## Evaluation signals

- Total Ion Spectra plot shows reduced noise spikes and smoother baseline while retaining peak positions and shapes
- Reverse Ion Chromatogram plot exhibits continuous, aligned traces across samples without artificial broadening or peak position drift
- Drift time and retention time dimensions show comparable smoothing quality; no dimension is over-smoothed relative to the other
- Comparison of pre- and post-smoothing heatmaps confirms noise reduction without loss of subtle ion mobility or chromatographic structure
- Subsequent alignment step converges without excessive warping, indicating that smoothing preserved genuine sample features

## Limitations

- Savitzky-Golay smoothing is a local operation; it does not address global misalignments caused by pressure and temperature fluctuations or chromatographic column degradation—alignment must follow.
- Window length and polynomial order are user-selected hyperparameters; suboptimal choices can under-smooth (leaving noise) or over-smooth (blurring peaks). The article does not provide explicit parameter recommendations for the threeketones dataset.
- Smoothing in both drift time and retention time independently may not account for correlations between the two dimensions in ion mobility behavior.
- GCIMS uses delayed evaluation for efficiency, so smoothing operations may not be executed until a later step in the pipeline (e.g., decimation or alignment); actual memory and runtime effects depend on pipeline composition.

## Evidence

- [intro] You can remove noise from your sample using a Savitzky-Golay filter, applied both in drift time and in retention time.: "You can remove noise from your sample using a Savitzky-Golay filter, applied both in drift time and in retention time."
- [other] After applying filtering, Savitzky-Golay smoothing, decimation, and alignment operations to the threeketones dataset, the Total Ion Spectra and Reverse Ion Chromatogram plots show visual alignment of samples across both drift time and retention time dimensions.: "After applying filtering, Savitzky-Golay smoothing, decimation, and alignment operations to the threeketones dataset, the Total Ion Spectra and Reverse Ion Chromatogram plots show visual alignment of"
- [intro] Pressure and temperature fluctuations as well as degradation of the chromatographic column are some of the causes of misalignments in the data, both in retention and drift time: "Pressure and temperature fluctuations as well as degradation of the chromatographic column are some of the causes of misalignments in the data, both in retention and drift time"
- [readme] GCIMS is an R package implementing a preprocessing pipeline for Gas Chromatography – Ion Mobility Spectrometry samples.: "GCIMS is an R package implementing a preprocessing pipeline for Gas Chromatography – Ion Mobility Spectrometry samples."
- [intro] The alignment will happen first in drift time and afterwards in retention time.: "The alignment will happen first in drift time and afterwards in retention time."
