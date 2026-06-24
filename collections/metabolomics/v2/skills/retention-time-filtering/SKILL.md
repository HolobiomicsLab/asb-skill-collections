---
name: retention-time-filtering
description: Use when working with GCIMS datasets where retention time spans a wide
  range (e.g., 0–1500 s) but your analytes of interest are confined to a narrower
  window (e.g., 0–1100 s).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_3520
  tools:
  - R
  - GCIMS
  techniques:
  - GC-MS
  - ion-mobility-MS
  license_tier: restricted
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

# retention-time-filtering

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Restrict Gas Chromatography–Ion Mobility Spectrometry samples to a biologically or analytically relevant retention time window before downstream preprocessing. This reduces noise, memory consumption, and computation time by excluding regions with no informative signal.

## When to use

Apply this skill when working with GCIMS datasets where retention time spans a wide range (e.g., 0–1500 s) but your analytes of interest are confined to a narrower window (e.g., 0–1100 s). Use it as an early preprocessing step before smoothing, decimation, or alignment to reduce computational overhead and focus analysis on signal-bearing regions.

## When NOT to use

- Do not use if you are uncertain about the expected retention time range for your analytes; instead, visualize the full chromatogram first to inform your choice of bounds.
- Do not apply multiple overlapping retention time filters sequentially without re-inspecting the data, as this may inadvertently remove valid signal.
- Do not use if your analysis goal requires retention of the full temporal profile for baseline correction or drift time alignment verification across the entire acquisition range.

## Inputs

- GCIMSDataset object (loaded in R via GCIMS library)

## Outputs

- Filtered GCIMSDataset object with retention time restricted to specified range

## How to apply

Load your GCIMSDataset object and call the filterRt() function with a lower and upper retention time bound in seconds. The article demonstrates filtering the threeketones dataset to 0–1100 s using filterRt(dataset, rt = c(0, 1100)). This operation removes all data points outside the specified window. Apply this filter early in the preprocessing pipeline, after dataset creation but before applying Savitzky-Golay smoothing, decimation, or alignment, to maximize efficiency. The choice of retention time bounds should be informed by prior knowledge of your analyte's chromatographic behavior or preliminary inspection of total ion chromatograms.

## Related tools

- **GCIMS** (R package providing filterRt() function for retention time range restriction) — https://github.com/sipss/GCIMS
- **R** (Programming environment in which GCIMS and filterRt() are executed)

## Examples

```
filterRt(dataset, rt = c(0, 1100))
```

## Evaluation signals

- Verify that the filtered dataset contains no retention time values outside the specified range (e.g., min(rt) ≥ 0 and max(rt) ≤ 1100 for the example bounds).
- Confirm that downstream alignment plots (Total Ion Spectra, Reverse Ion Chromatogram) show signal only within the filtered retention time window with no edge artifacts.
- Check that memory usage is reduced after filtering compared to the unfiltered dataset, indicating successful data removal.
- Inspect the Total Ion Chromatogram before and after filtering to ensure no inadvertent loss of analyte signal.
- Validate that subsequent smoothing and alignment operations complete without errors and produce interpretable results within the filtered time window.

## Limitations

- Choosing retention time bounds requires prior knowledge or exploratory inspection; incorrect bounds may remove analyte signal or leave excessive noise.
- filterRt() operates on the entire dataset; it does not support per-sample retention time adjustments if individual samples are misaligned in retention time by large offsets.
- The article does not discuss how to handle datasets with multiple unresolved peaks or co-eluting compounds that span variable retention time windows across samples.

## Evidence

- [intro] Pressure and temperature fluctuations as well as degradation of the chromatographic column are some of the causes of misalignments in the data, both in retention and drift time: "Pressure and temperature fluctuations as well as degradation of the chromatographic column are some of the causes of misalignments in the data, both in retention and drift time"
- [intro] Filter the retention and drift time of your samples: "Filter the retention and drift time of your samples"
- [intro] filterRt(dataset, rt = c(0, 1100)) # in s: "filterRt(dataset, rt = c(0, 1100)) # in s"
- [intro] One way to speed up calculations and reduce the memory requirements is to decimate the matrix, by taking 1 every Nd points in drift time and 1 every Nr points in retention time: "One way to speed up calculations and reduce the memory requirements is to decimate the matrix"
- [intro] GCIMS uses delayed evaluations were possible, so dataset modifications can be executed in a more efficient way and without using too much RAM: "GCIMS uses delayed evaluations were possible, so dataset modifications can be executed in a more efficient way and without using too much RAM"
