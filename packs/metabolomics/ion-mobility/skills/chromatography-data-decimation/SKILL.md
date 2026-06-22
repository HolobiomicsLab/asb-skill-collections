---
name: chromatography-data-decimation
description: Use when working with large GCIMS matrices where computational speed or memory constraints are a concern, after filtering retention time (e.g., 0–1100 s) and drift time (e.g., 5–16 ms) ranges and applying Savitzky-Golay smoothing. Use it as a preprocessing step before alignment operations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3565
  edam_topics:
  - http://edamontology.org/topic_3520
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# chromatography-data-decimation

## Summary

Reduce memory footprint and computational cost of Gas Chromatography–Ion Mobility Spectrometry (GCIMS) data by systematically subsampling the drift time and retention time dimensions. Decimation is applied after filtering and smoothing to enable faster downstream alignment and peak detection without losing essential spectral structure.

## When to use

Apply this skill when working with large GCIMS matrices where computational speed or memory constraints are a concern, after filtering retention time (e.g., 0–1100 s) and drift time (e.g., 5–16 ms) ranges and applying Savitzky-Golay smoothing. Use it as a preprocessing step before alignment operations.

## When NOT to use

- Input data has not yet been smoothed; apply Savitzky-Golay filtering first to avoid aliasing artifacts.
- Downstream analysis requires peak-level precision at sub-millisecond drift time or sub-second retention time resolution; decimation may lose critical fine structure.
- Dataset is already small or memory/speed is not a constraint; decimation trades resolution for performance and should not be applied unnecessarily.

## Inputs

- GCIMSDataset object (filtered and Savitzky-Golay smoothed)
- Drift time points (Nd: subsampling interval)
- Retention time points (Nr: subsampling interval)

## Outputs

- Decimated GCIMSDataset object (reduced matrix dimensions in drift time and retention time)

## How to apply

Decimate the GCIMS matrix by taking 1 every Nd points in the drift time dimension and 1 every Nr points in the retention time dimension. The choice of Nd and Nr should balance memory reduction against loss of temporal resolution; typical workflows subsample both dimensions uniformly. Apply decimation after noise removal (Savitzky-Golay smoothing) but before alignment, as the smoothing step makes intermediate points redundant. The decimation exploits GCIMS's delayed-evaluation architecture, ensuring modifications execute efficiently without excessive RAM consumption. Verify that decimated data retain alignment quality in subsequent drift time and retention time alignment steps by visual inspection of Total Ion Spectra and Reverse Ion Chromatogram plots.

## Related tools

- **GCIMS** (R package providing decimation functionality and delayed-evaluation matrix operations for GCIMS data) — https://github.com/sipss/GCIMS
- **R** (Runtime environment for GCIMS package and decimation workflow)

## Examples

```
# After filtering and smoothing, decimate the GCIMSDataset
# dataset <- filterRt(dataset, rt = c(0, 1100))
# dataset <- filterDt(dataset, dt = c(5, 16))
# dataset <- smoothGCMS(dataset, ...) # Savitzky-Golay smoothing
# dataset_decimated <- decimateDataset(dataset, Nd = 5, Nr = 10)
```

## Evaluation signals

- Decimated dataset dimensions in drift time and retention time are reduced by expected factors (Nd and Nr respectively).
- Total Ion Spectra and Reverse Ion Chromatogram plots from decimated data show visual alignment consistency with pre-decimation filtered data.
- Subsequent alignment (drift time, then retention time) on decimated data converges without significant residual misalignment.
- Memory consumption and computational runtime are measurably reduced compared to non-decimated workflow.
- Peak detection and clustering metrics on decimated data remain consistent with or show acceptable degradation relative to full-resolution data.

## Limitations

- Decimation is lossy; choosing Nd and Nr too aggressively will discard information and degrade downstream alignment quality.
- The skill assumes input data have already been smoothed; applying decimation to raw or insufficiently smoothed data may introduce aliasing.
- No guidance provided in the article for data-driven selection of optimal Nd and Nr values; practitioners must tune empirically per dataset.
- Decimation efficacy depends on the structure of misalignments; severe pressure/temperature-induced drift or column degradation may require finer resolution than decimation allows.

## Evidence

- [intro] One way to speed up calculations and reduce the memory requirements is to decimate the matrix, by taking 1 every Nd points in drift time and 1 every Nr points in retention time.: "One way to speed up calculations and reduce the memory requirements is to decimate the matrix, by taking 1 every Nd points in drift time and 1 every Nr points in retention time."
- [intro] GCIMS uses delayed evaluations were possible, so dataset modifications can be executed in a more efficient way and without using too much RAM.: "GCIMS uses delayed evaluations were possible, so dataset modifications can be executed in a more efficient way and without using too much RAM."
- [intro] You can remove noise from your sample using a Savitzky-Goyal filter, applied both in drift time and in retention time.: "You can remove noise from your sample using a Savitzky-Golay filter, applied both in drift time and in retention time."
- [intro] The alignment will happen first in drift time and afterwards in retention time.: "The alignment will happen first in drift time and afterwards in retention time."
- [other] After applying filtering, Savitzky-Golay smoothing, decimation, and alignment operations to the threeketones dataset, the Total Ion Spectra and Reverse Ion Chromatogram plots show visual alignment of samples across both drift time and retention time dimensions.: "After applying filtering, Savitzky-Golay smoothing, decimation, and alignment operations to the threeketones dataset, the Total Ion Spectra and Reverse Ion Chromatogram plots show visual alignment of"
