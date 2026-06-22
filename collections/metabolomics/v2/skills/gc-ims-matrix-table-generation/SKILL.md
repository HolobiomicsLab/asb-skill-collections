---
name: gc-ims-matrix-table-generation
description: Use when after integratePeaks has been executed with a chosen integration method (e.g., fixed_size with RIP saturation threshold of 0.1) on a clustered, baseline-corrected GC-IMS dataset.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3800
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
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

# gc-ims-matrix-table-generation

## Summary

Extract and format integrated peak intensities from Gas Chromatography–Ion Mobility Spectrometry samples into a peak_table_matrix where rows represent clusters and columns represent samples. This skill produces the quantitative feature table required for downstream statistical or multivariate analysis.

## When to use

After integratePeaks has been executed with a chosen integration method (e.g., fixed_size with RIP saturation threshold of 0.1) on a clustered, baseline-corrected GC-IMS dataset. Use this skill when you need to convert peak integration results into a rectangular matrix format suitable for statistical or machine learning workflows.

## When NOT to use

- integratePeaks has not yet been run — you must first integrate peaks across samples
- Peak clustering (clusterPeaks) has not been performed — peakTable requires clustered peak definitions
- Input data has not undergone baseline correction and alignment — pre-processing is mandatory

## Inputs

- integration result object from integratePeaks (with fixed_size or other integration method and RIP saturation threshold applied)
- preprocessed GC-IMS dataset (after alignment, baseline correction, and peak detection/clustering)

## Outputs

- peak_table_matrix: rows = peak clusters, columns = samples, values = intensity (some NA)

## How to apply

Call the peakTable function on the integration result object returned by integratePeaks. The function extracts intensity values for each detected peak cluster across all samples and arranges them into a matrix where rows correspond to peak clusters and columns correspond to samples. Some entries will be NA (missing intensities for peaks not detected in certain samples), which signals that imputation or missing-value handling must follow. The output structure is designed to feed directly into statistical or multivariate analysis pipelines after NA handling.

## Related tools

- **GCIMS** (R package providing integratePeaks and peakTable functions for peak integration and matrix generation) — https://github.com/sipss/GCIMS
- **R** (Runtime environment for GCIMS package execution)

## Examples

```
peak_table_matrix <- peakTable(integratePeaks(clustered_peaks, integration_size_method='fixed_size', rip_saturation_threshold=0.1))
```

## Evaluation signals

- peak_table_matrix has dimensions [n_clusters × n_samples] with no unexpected transpose or dimension mismatch
- Row names correspond to detected peak cluster identifiers; column names correspond to sample IDs
- Intensity values are numeric; NA entries are present only where peaks were not detected in specific samples
- Sum of intensities per sample is positive and within expected range for the instrument and RIP threshold used
- No rows or columns are entirely NA or zero-valued (indicates successful detection in at least some samples)

## Limitations

- NA entries require downstream imputation or omission strategies before statistical analysis — peakTable does not perform imputation itself
- Fixed-size integration with RIP saturation threshold = 0.1 may produce different peak counts and intensity distributions than other integration methods; method choice affects matrix dimensions
- GCIMS uses delayed evaluations to save RAM; very large datasets may still cause memory issues during matrix materialization
- Peak clustering quality directly affects row definitions in the matrix — poor clustering produces ambiguous or redundant rows

## Evidence

- [other] peakTable function produces a peak_table_matrix with rows representing clusters and columns representing samples: "The peakTable function produces a peak_table_matrix with rows representing clusters and columns representing samples, containing intensity values with some entries as NA that require imputation."
- [other] Fixed-size integration method with RIP saturation threshold setting: "Execute integratePeaks function with integration_size_method set to 'fixed_size' and rip_saturation_threshold parameter set to 0.1 to integrate detected peaks across all samples."
- [other] GCIMS preprocessing pipeline involves alignment and baseline correction before peak integration: "Load the preprocessed GC-IMS dataset (after alignment and baseline correction) into R using the GCIMS package."
- [readme] GCIMS is an R package implementing a preprocessing pipeline for Gas Chromatography – Ion Mobility Spectrometry samples: "GCIMS is an R package implementing a preprocessing pipeline for Gas Chromatography – Ion Mobility Spectrometry samples."
