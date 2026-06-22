---
name: metabolite-level-expression-summarization
description: Use when after loading spatial metabolomics data (from CSV, imzML, or merged positive/negative mode files) into an AnnData object and before filtering or integrating with spatial transcriptomics.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3520
  tools:
  - spatialMETA
  techniques:
  - MS-imaging
derived_from:
- doi: 10.1038/s41467-025-63915-z
  title: SpatialMETA
evidence_spans:
- spatialMETA is a method for integrating spatial multi-omics data
- spatialmeta.pp.calculate_qc_metrics_sm
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_spatialmeta_cq
    doi: 10.1038/s41467-025-63915-z
    title: SpatialMETA
  dedup_kept_from: coll_spatialmeta_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-025-63915-z
  all_source_dois:
  - 10.1038/s41467-025-63915-z
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-level-expression-summarization

## Summary

Compute per-metabolite quality control and summary metrics on spatial metabolomics AnnData objects, including detection frequency and average intensity. This skill enables filtering and prioritization of metabolites for downstream cross-modal integration in spatial multi-omics workflows.

## When to use

Apply this skill after loading spatial metabolomics data (from CSV, imzML, or merged positive/negative mode files) into an AnnData object and before filtering or integrating with spatial transcriptomics. Use it when you need to characterize metabolite-level coverage, abundance patterns, or detection rates across the spatial sample to decide which metabolites to retain for joint analysis.

## When NOT to use

- Input data is not in AnnData format or has not been loaded via SpatialMETA I/O functions.
- Metabolite filtering has already been completed upstream; applying this skill again would be redundant unless re-computing metrics after data transformation.
- The analysis does not require metabolite-level filtering and proceeds directly to spot alignment or cross-modal integration.

## Inputs

- AnnData object containing spatial metabolomics data (from spatialmeta.pp.read_sm_csv_as_anndata, read_sm_imzml_as_anndata, or merge_sm_pos_neg)

## Outputs

- AnnData object with per-metabolite QC metrics stored in adata.var columns (e.g., detection_frequency, average_intensity)

## How to apply

Load a spatial metabolomics AnnData object prepared by read_sm_csv_as_anndata, read_sm_imzml_as_anndata, or merge_sm_pos_neg. Call spatialmeta.pp.calculate_qc_metrics_sm on the object to compute per-metabolite metrics such as detection frequency (the fraction of spots in which a metabolite was detected) and average intensity per metabolite. These metrics are stored as columns in adata.var, allowing subsequent filtering via filter_metabolites_sm based on these thresholds. The rationale is that metabolites with very low detection or intensity across the spatial field carry little signal and should be excluded before alignment and integration with spatial transcriptomics data.

## Related tools

- **spatialMETA** (Provides calculate_qc_metrics_sm function to compute per-spot and per-metabolite QC metrics on spatial metabolomics AnnData objects) — https://github.com/WanluLiuLab/SpatialMETA

## Examples

```
import spatialmeta as sm; adata = sm.pp.read_sm_csv_as_anndata('metabolomics.csv', spatial_coords='coords.csv'); sm.pp.calculate_qc_metrics_sm(adata); print(adata.var.head())
```

## Evaluation signals

- adata.var contains new columns for per-metabolite metrics (detection_frequency, average_intensity, or similar)
- Metric ranges are reasonable: detection_frequency ∈ [0, 1], average_intensity ≥ 0
- Metabolite count and spot count in adata are preserved (no rows or columns dropped by QC computation itself)
- Downstream filter_metabolites_sm can be applied using the computed metrics without errors
- QC metrics show expected patterns (e.g., high-abundance metabolites have high detection frequency; low-abundance metabolites have low detection frequency)

## Limitations

- QC metrics depend on the input data quality and normalization state; metrics should be computed on preprocessed data with consistent units and artifact removal to be meaningful.
- The choice of thresholds for filtering (e.g., minimum detection frequency or average intensity) is not automated and must be set by the user based on domain knowledge and downstream integration goals.
- No validation that per-metabolite metrics align with mass spectrometry best practices or that threshold choices are statistically justified.

## Evidence

- [other] Apply spatialmeta.pp.calculate_qc_metrics_sm to compute QC metrics at the spot level (e.g., total intensity, number of detected metabolites per spot) and metabolite level (e.g., detection frequency, average intensity per metabolite).: "Apply spatialmeta.pp.calculate_qc_metrics_sm to compute QC metrics at the spot level (e.g., total intensity, number of detected metabolites per spot) and metabolite level (e.g., detection frequency,"
- [other] Store computed metrics in adata.obs (per-spot) and adata.var (per-metabolite) columns.: "Store computed metrics in adata.obs (per-spot) and adata.var (per-metabolite) columns."
- [other] SpatialMETA includes a calculate_qc_metrics_sm preprocessing function that computes quality control metrics at the per-spot and per-metabolite level on spatial metabolomics AnnData objects as part of the integrated workflow.: "SpatialMETA includes a calculate_qc_metrics_sm preprocessing function that computes quality control metrics at the per-spot and per-metabolite level on spatial metabolomics AnnData objects as part of"
