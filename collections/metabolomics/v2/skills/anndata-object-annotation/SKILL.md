---
name: anndata-object-annotation
description: Use when after loading or merging spatial metabolomics data into an AnnData object (via read_sm_csv_as_anndata, read_sm_imzml_as_anndata, or merge_sm_pos_neg), and before filtering or normalization steps.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - spatialMETA
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

# anndata-object-annotation

## Summary

Embed computed quality control metrics into AnnData objects at per-spot and per-metabolite resolution for spatial metabolomics data. This skill enables systematic QC tracking and downstream filtering by storing derived metrics in standardized AnnData slots (adata.obs and adata.var).

## When to use

After loading or merging spatial metabolomics data into an AnnData object (via read_sm_csv_as_anndata, read_sm_imzml_as_anndata, or merge_sm_pos_neg), and before filtering or normalization steps. Use this skill when you need to compute intensity-based QC metrics (total intensity per spot, detection frequency per metabolite) and embed them as columns in the AnnData object for downstream quality control decisions.

## When NOT to use

- AnnData object is not derived from spatial metabolomics data (e.g., it is from spatial transcriptomics only or bulk metabolomics without spatial coordinates)
- QC metrics have already been computed and stored in adata.obs and adata.var by a prior workflow step
- Input data is not in AnnData format or lacks proper spot/metabolite dimensional structure

## Inputs

- Spatial metabolomics AnnData object (adata) with .X matrix populated and spot/metabolite identifiers in .obs_names and .var_names

## Outputs

- Annotated AnnData object with per-spot QC metrics in adata.obs columns (e.g., total_intensity, n_detected_metabolites)
- Annotated AnnData object with per-metabolite QC metrics in adata.var columns (e.g., detection_frequency, mean_intensity)

## How to apply

Load a spatial metabolomics AnnData object prepared by SpatialMETA's input functions. Apply spatialmeta.pp.calculate_qc_metrics_sm to compute per-spot metrics (e.g., total intensity, number of detected metabolites) and per-metabolite metrics (e.g., detection frequency, average intensity). The function automatically stores per-spot metrics as new columns in adata.obs and per-metabolite metrics as new columns in adata.var. Inspect the resulting annotated AnnData object to verify that QC metric columns are present and populated with numeric values before proceeding to filter_cells_sm or filter_metabolites_sm steps.

## Related tools

- **spatialMETA** (Provides the calculate_qc_metrics_sm function and integrated preprocessing workflow for spatial metabolomics quality control metric computation on AnnData objects) — https://github.com/WanluLiuLab/SpatialMETA

## Examples

```
import spatialmeta as sm; adata = sm.pp.read_sm_csv_as_anndata('metabolomics.csv'); adata = sm.pp.calculate_qc_metrics_sm(adata); print(adata.obs.head())
```

## Evaluation signals

- adata.obs contains new numeric columns (e.g., 'total_intensity', 'n_detected_metabolites') with non-null values for all spots
- adata.var contains new numeric columns (e.g., 'detection_frequency', 'mean_intensity') with non-null values for all metabolites
- Per-spot total intensity is non-negative and sums match the row-wise sum of adata.X
- Per-metabolite detection frequency is between 0 and 1 (or 0 and 100 if percentages), and correlates with sparsity patterns in adata.X
- Spot and metabolite metric columns are queryable and filterable for downstream QC workflows (e.g., filter_cells_sm or filter_metabolites_sm)

## Limitations

- Metrics are computed in-place on the full AnnData object; if metrics must be recomputed with different parameters or on subsets, the function must be re-run
- The function assumes the input AnnData object is well-formed with proper dimensionality; malformed or incomplete objects may produce NaN or misleading metric values
- Metrics are additive (total intensity, detection counts) and do not account for metabolite mass, retention time, or other chemical properties that may be relevant for domain-specific QC decisions

## Evidence

- [other] Apply spatialmeta.pp.calculate_qc_metrics_sm to compute QC metrics at the spot level (e.g., total intensity, number of detected metabolites per spot) and metabolite level (e.g., detection frequency, average intensity per metabolite).: "Apply spatialmeta.pp.calculate_qc_metrics_sm to compute QC metrics at the spot level (e.g., total intensity, number of detected metabolites per spot) and metabolite level (e.g., detection frequency,"
- [other] Store computed metrics in adata.obs (per-spot) and adata.var (per-metabolite) columns.: "Store computed metrics in adata.obs (per-spot) and adata.var (per-metabolite) columns."
- [other] SpatialMETA includes a calculate_qc_metrics_sm preprocessing function that computes quality control metrics at the per-spot and per-metabolite level on spatial metabolomics AnnData objects as part of the integrated workflow.: "SpatialMETA includes a calculate_qc_metrics_sm preprocessing function that computes quality control metrics at the per-spot and per-metabolite level on spatial metabolomics AnnData objects as part of"
