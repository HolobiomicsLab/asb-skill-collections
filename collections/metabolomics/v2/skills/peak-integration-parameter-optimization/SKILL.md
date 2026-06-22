---
name: peak-integration-parameter-optimization
description: Use when after peak detection and clustering have been completed on aligned and baseline-corrected GC-IMS data, and before imputation or statistical analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - R
  - GCIMS
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

# peak-integration-parameter-optimization

## Summary

Optimize peak integration parameters—specifically fixed-size integration method and RIP saturation threshold—to produce a well-formed peak intensity matrix with minimal missing values. This skill bridges peak detection and feature table construction in GC-IMS preprocessing.

## When to use

After peak detection and clustering have been completed on aligned and baseline-corrected GC-IMS data, and before imputation or statistical analysis. Apply this skill when you need to decide whether to use fixed-size integration (uniform region around detected peaks) versus other methods, and when you must set the RIP saturation threshold to balance inclusion of valid peaks against reactant ion peak contamination.

## When NOT to use

- If input data has not yet been aligned and baseline-corrected; integratePeaks requires clean, spatially registered data.
- If peak detection has not been completed or peak clustering has not been performed; integratePeaks operates on detected and clustered peaks, not raw spectra.
- If the goal is exploratory comparison of multiple integration methods; this skill assumes fixed-size integration is the method of choice and focuses on threshold tuning rather than method selection.

## Inputs

- preprocessed GC-IMS dataset (after alignment and baseline correction)
- peak detection and clustering results
- integration_size_method parameter (set to 'fixed_size')
- rip_saturation_threshold parameter (numeric, e.g., 0.1)

## Outputs

- peak_table_matrix (rows=clusters/peaks, columns=samples, values=intensity with NA entries)
- integratePeaks result object (passed to peakTable)

## How to apply

Load the preprocessed GC-IMS dataset (post-alignment and baseline correction) into R using the GCIMS package. Call integratePeaks with integration_size_method='fixed_size' and rip_saturation_threshold set to a value (e.g., 0.1) that excludes RIP-contaminated peaks while retaining genuine analyte signals. The threshold parameter filters peaks whose saturation (relative intensity from the reactant ion peak) exceeds this cutoff. Execute peakTable on the integration result to extract a peak_table_matrix with rows as clusters and columns as samples. Inspect the resulting matrix for the proportion and pattern of NA entries; high NA counts suggest the threshold is too stringent or the fixed-size window is poorly calibrated. Iteratively adjust the rip_saturation_threshold upward (more permissive) or downward (stricter) based on domain knowledge and the downstream imputation requirements.

## Related tools

- **GCIMS** (R package providing integratePeaks and peakTable functions for fixed-size peak integration and matrix extraction) — https://github.com/sipss/GCIMS
- **R** (Runtime environment for executing GCIMS functions and parameter optimization workflow)

## Examples

```
# Load data and perform peak detection/clustering
library(GCIMS)
dataset <- loadGCIMSDataset('preprocessed_data.rds')
integration_result <- integratePeaks(dataset, integration_size_method='fixed_size', rip_saturation_threshold=0.1)
peak_table_matrix <- peakTable(integration_result)
```

## Evaluation signals

- Peak table matrix dimensions match expected counts: rows = number of clustered peaks, columns = number of samples.
- Proportion of NA entries in the peak_table_matrix is reasonable (typically <20–30% for well-tuned thresholds); excessive NAs indicate over-stringent RIP threshold.
- Intensity values in non-NA cells fall within expected ranges for the instrument and sample type (no negative or physically implausible values).
- RIP saturation threshold of 0.1 excludes known contaminated peaks (visual inspection of chromatograms or comparison with quality control standards) while retaining analyte signals.
- Peak table can be successfully passed to downstream imputation and statistical analysis steps without structural errors or unexpected data type mismatches.

## Limitations

- Fixed-size integration assumes all peaks have similar spatial extent in the drift-time × retention-time plane; peaks with unusual or variable shapes may be poorly integrated or excluded.
- RIP saturation threshold is dataset- and instrument-specific; a threshold of 0.1 may not generalize across different GC-IMS platforms or sample types without re-optimization.
- No guidance is provided in the article on how to choose the optimal RIP saturation threshold a priori; threshold selection requires iterative refinement or domain expertise.
- NA entries in the resulting peak table indicate missing or below-threshold peaks in specific samples and require imputation before statistical analysis; the skill does not address imputation strategy.

## Evidence

- [other] Execute integratePeaks function with integration_size_method set to 'fixed_size' and rip_saturation_threshold parameter set to 0.1: "Execute integratePeaks function with integration_size_method set to 'fixed_size' and rip_saturation_threshold parameter set to 0.1 to integrate detected peaks across all samples."
- [other] peakTable produces peak_table_matrix with rows representing clusters and columns representing samples, containing intensity values with some entries as NA: "The peakTable function produces a peak_table_matrix with rows representing clusters and columns representing samples, containing intensity values with some entries as NA that require imputation."
- [other] Load preprocessed GC-IMS dataset after alignment and baseline correction: "Load the preprocessed GC-IMS dataset (after alignment and baseline correction) into R using the GCIMS package."
- [intro] Pressure and temperature fluctuations as well as degradation of the chromatographic column are causes of misalignments: "Pressure and temperature fluctuations as well as degradation of the chromatographic column are some of the causes of misalignments in the data, both in retention and drift time."
- [readme] GCIMS is an R package implementing a preprocessing pipeline for GC-IMS samples: "GCIMS is an R package implementing a preprocessing pipeline for Gas Chromatography – Ion Mobility Spectrometry samples."
