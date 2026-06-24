---
name: metabolite-detection-frequency-estimation
description: Use when after loading spatial metabolomics data (from CSV, imzML, or
  merged positive/negative ionization modes) into an AnnData object, and before filtering
  metabolites or performing cross-modal integration.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - spatialMETA
  techniques:
  - MS-imaging
  license_tier: open
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-detection-frequency-estimation

## Summary

Compute per-metabolite detection frequency as a quality control metric in spatial metabolomics AnnData objects. This metric quantifies the proportion of spatial spots in which each metabolite was detected, enabling identification of metabolites with sparse or ubiquitous spatial occurrence patterns.

## When to use

Apply this skill after loading spatial metabolomics data (from CSV, imzML, or merged positive/negative ionization modes) into an AnnData object, and before filtering metabolites or performing cross-modal integration. Use it when you need to assess which metabolites are reliably detected across the spatial array and to identify detection patterns that may confound downstream analyses or warrant quality-based filtering.

## When NOT to use

- Input is already a processed feature table with pre-computed QC metrics — skip to filtering or downstream analysis.
- Spatial metabolomics data is in raw vendor format (mzML, imzML, CSV) — first read and parse using read_sm_imzml_as_anndata or read_sm_csv_as_anndata.
- Analysis goal is only visualization or spatial pattern discovery without QC assessment — detection frequency is unnecessary if you are not filtering or validating data quality.

## Inputs

- spatial metabolomics AnnData object (adata) with .X matrix (spot × metabolite intensity)
- per-spot metadata in adata.obs (e.g., spatial coordinates, sample ID)
- per-metabolite metadata in adata.var (e.g., m/z, metabolite identifier)

## Outputs

- annotated AnnData object with per-metabolite detection frequency stored in adata.var columns
- per-metabolite QC metrics including detection frequency, average intensity, and other spot-level summaries

## How to apply

Call spatialmeta.pp.calculate_qc_metrics_sm on a prepared spatial metabolomics AnnData object. The function computes detection frequency at the per-metabolite level by counting the number of spots where each metabolite intensity exceeds background noise or a detection threshold, then normalizing by total spot count. The resulting per-metabolite detection frequency values are stored in adata.var columns alongside other metabolite-level QC metrics (e.g., average intensity). Use these frequency estimates to inform subsequent filtering decisions via spatialmeta.pp.filter_metabolites_sm, where metabolites with detection frequencies below a user-defined threshold (e.g., present in <10% of spots) may be excluded as uninformative or artefactual.

## Related tools

- **spatialMETA** (performs per-metabolite QC metric calculation including detection frequency on spatial metabolomics AnnData objects) — https://github.com/WanluLiuLab/SpatialMETA

## Examples

```
import spatialmeta as st; adata = st.pp.read_sm_csv_as_anndata('metabolomics.csv'); adata = st.pp.calculate_qc_metrics_sm(adata); print(adata.var[['detection_frequency', 'mean_intensity']])
```

## Evaluation signals

- adata.var contains a new column with detection frequency values (numeric, range 0–1 or 0–100%)
- Detection frequency distribution is reasonable for the dataset: metabolites with very low or very high frequencies are identified and can be justified (e.g., rare isotopologues vs. major peaks)
- Applying filter_metabolites_sm with a detection frequency threshold produces a reduced AnnData object with expected number of metabolites retained
- Per-metabolite detection frequencies correlate with visual patterns in spatial heatmaps (e.g., metabolites with low detection frequency show sparse, scattered spots)

## Limitations

- Detection frequency depends on the noise threshold or intensity cutoff used by calculate_qc_metrics_sm; no standardized threshold is specified in the README, so results may vary if internal thresholds are not documented or tuned.
- Spatial metabolomics data from different ionization modes (positive vs. negative) may have different effective detection frequencies; merging must occur before QC metric computation for consistent assessment.
- Detection frequency does not account for technical variation, instrumental drift, or sample-preparation bias — high frequency does not guarantee true biological signal.

## Evidence

- [other] SpatialMETA includes a calculate_qc_metrics_sm preprocessing function that computes quality control metrics at the per-spot and per-metabolite level on spatial metabolomics AnnData objects: "SpatialMETA includes a calculate_qc_metrics_sm preprocessing function that computes quality control metrics at the per-spot and per-metabolite level on spatial metabolomics AnnData objects as part of"
- [other] Apply spatialmeta.pp.calculate_qc_metrics_sm to compute QC metrics at the spot level and metabolite level (e.g., detection frequency, average intensity per metabolite): "Apply spatialmeta.pp.calculate_qc_metrics_sm to compute QC metrics at the spot level (e.g., total intensity, number of detected metabolites per spot) and metabolite level (e.g., detection frequency,"
- [other] Store computed metrics in adata.obs (per-spot) and adata.var (per-metabolite) columns: "Store computed metrics in adata.obs (per-spot) and adata.var (per-metabolite) columns."
- [other] spatialMETA is a method for integrating spatial multi-omics data: "spatialMETA is a method for integrating spatial multi-omics data. SMOI aligns ST and SM to a unified resolution"
