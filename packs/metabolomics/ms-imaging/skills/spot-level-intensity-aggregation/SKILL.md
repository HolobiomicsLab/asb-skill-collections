---
name: spot-level-intensity-aggregation
description: Use when after loading spatial metabolomics data (from CSV, imzML, or merged positive/negative ion modes) into an AnnData object, and before filtering or alignment steps.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3678
  tools:
  - spatialMETA
  - spatialmeta.pp.filter_cells_sm
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

# spot-level-intensity-aggregation

## Summary

Compute per-spot quality control metrics on spatial metabolomics AnnData objects, including total intensity and number of detected metabolites per spot. This skill quantifies data completeness and signal strength at each spatial location before downstream analysis.

## When to use

Apply this skill after loading spatial metabolomics data (from CSV, imzML, or merged positive/negative ion modes) into an AnnData object, and before filtering or alignment steps. Use it to characterize spot-level data quality—identifying which spots have sufficient metabolite detection and signal intensity to justify downstream processing.

## When NOT to use

- Input is already a quality-filtered or aggregated feature table (e.g., from external pre-processing).
- You are analyzing untargeted transcriptomics or proteomics data without spatial metabolomics component.
- Spot-level metrics are not relevant to your downstream analysis (e.g., if doing only global metabolite-level statistics).

## Inputs

- AnnData object with spatial metabolomics data (X matrix: m/z × spot)
- Metadata: spot coordinates, ion polarity mode

## Outputs

- adata.obs columns: per-spot QC metrics (total intensity, number of detected metabolites)
- Annotated AnnData object with QC metrics embedded

## How to apply

Load your spatial metabolomics AnnData object (prepared by read_sm_csv_as_anndata, read_sm_imzml_as_anndata, or merge_sm_pos_neg). Apply spatialmeta.pp.calculate_qc_metrics_sm, which computes per-spot metrics such as total intensity (sum of all metabolite signals at each spot) and detection frequency (number of detected metabolites per spot). The function stores these metrics in adata.obs columns for downstream filtering (e.g., via filter_cells_sm to remove low-quality spots). Rationale: spot-level aggregation reveals spatial heterogeneity in sample coverage and ionization efficiency, which is critical for identifying and excluding dead pixels, edge artifacts, or instrumental dropouts before joint integration with spatial transcriptomics.

## Related tools

- **spatialMETA** (Provides calculate_qc_metrics_sm function to compute per-spot and per-metabolite QC metrics on spatial metabolomics AnnData objects) — https://github.com/WanluLiuLab/SpatialMETA
- **spatialmeta.pp.filter_cells_sm** (Downstream filtering function to remove low-quality spots based on computed QC metrics) — https://github.com/WanluLiuLab/SpatialMETA

## Examples

```
import spatialmeta as smt
adata = smt.pp.read_sm_csv_as_anndata('metabolites.csv', 'coordinates.csv')
smt.pp.calculate_qc_metrics_sm(adata)
print(adata.obs[['total_intensity', 'n_detected_metabolites']].head())
```

## Evaluation signals

- adata.obs contains new columns for per-spot metrics (e.g., 'total_intensity', 'n_detected_metabolites') with numeric values matching spot count
- Per-spot total intensity values are non-negative and reflect sum of all m/z intensities at each location
- Detection frequency (number of metabolites per spot) is between 0 and total number of metabolites (adata.n_vars)
- Spatial distribution of metrics correlates with expected sample morphology (e.g., higher intensity in tissue core vs. edges)
- Downstream filter_cells_sm successfully identifies and flags outlier spots using these metrics

## Limitations

- Assumes metabolite intensities are already normalized or raw; does not perform ion suppression correction across spots.
- Per-spot aggregation loses fine-grained m/z-level variation; complements but does not replace per-metabolite QC (available in adata.var).
- Quality metric thresholds are data- and instrument-dependent; no universal cutoff for spot inclusion is provided.
- Works only on AnnData objects; requires prior conversion of raw imzML or CSV formats using read_sm_imzml_as_anndata or read_sm_csv_as_anndata.

## Evidence

- [other] The calculate_qc_metrics_sm function computes QC metrics at per-spot and per-metabolite level: "SpatialMETA includes a calculate_qc_metrics_sm preprocessing function that computes quality control metrics at the per-spot and per-metabolite level on spatial metabolomics AnnData objects"
- [other] Per-spot metrics include total intensity and number of detected metabolites: "compute QC metrics at the spot level (e.g., total intensity, number of detected metabolites per spot)"
- [other] Per-spot metrics are stored in adata.obs columns: "Store computed metrics in adata.obs (per-spot) and adata.var (per-metabolite) columns"
- [other] Input data preparation workflow prior to QC metric computation: "Load a spatial metabolomics AnnData object (prepared by read_sm_csv_as_anndata, read_sm_imzml_as_anndata, or merge_sm_pos_neg)"
