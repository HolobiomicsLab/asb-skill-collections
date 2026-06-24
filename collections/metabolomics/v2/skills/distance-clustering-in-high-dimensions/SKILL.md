---
name: distance-clustering-in-high-dimensions
description: Use when when you have detected feature tables from two or more LC-IMS-MS/MS
  samples and need to establish correspondence between features across samples (i.e.,
  which features in sample A match which features in sample B).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - DEIMoS
  - numpy
  - ProteoWizard
  techniques:
  - LC-MS
  - ion-mobility-MS
  license_tier: open
derived_from:
- doi: 10.1021/acs.analchem.1c05017
  title: deimos
evidence_spans:
- DEIMoS is a Python application programming interface
- DEIMoS is a Python application programming interface and command-line tool
- Functionality includes feature detection, feature alignment, collision cross section
  (CCS) calibration, isotope detection, and MS/MS spectral deconvolution
- import deimos
- import numpy as np
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_deimos_cq
    doi: 10.1021/acs.analchem.1c05017
    title: deimos
  dedup_kept_from: coll_deimos_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c05017
  all_source_dois:
  - 10.1021/acs.analchem.1c05017
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# distance-clustering-in-high-dimensions

## Summary

Cluster detected features across multiple LC-IMS-MS/MS samples by applying N-dimensional distance-based grouping in (mz, drift_time, retention_time) space with user-defined tolerances. This skill enables cross-sample feature matching and alignment by identifying features that occupy the same region across dimensions, accounting for instrument drift and calibration variation.

## When to use

When you have detected feature tables from two or more LC-IMS-MS/MS samples and need to establish correspondence between features across samples (i.e., which features in sample A match which features in sample B). Apply this skill after feature detection but before consensus feature assignment, especially when dealing with instrument variation such as drift or calibration shifts that affect feature coordinates non-uniformly.

## When NOT to use

- Input is already a pre-aligned consensus feature table with cluster assignments; re-clustering would duplicate work and risk degrading consensus coordinates.
- Single-sample analysis: cross-sample alignment requires at least two samples; use single-sample peak detection instead.
- Tolerance values are unknown or unmeasurable: clustering quality depends critically on appropriate dimension-specific tolerances; proceed only after empirical characterization of instrument variation.

## Inputs

- Multiple detected feature tables (HDF5 .h5 format or mzML) from LC-IMS-MS/MS samples
- Feature columns: mz, drift_time, retention_time, intensity
- User-defined tolerance values for each dimension (mz_tol, drift_time_tol, retention_time_tol)
- Optional reference sample for coordinate normalization

## Outputs

- Aligned feature table with columns: mz, drift_time, retention_time, intensity, cluster_id, sample_membership
- Consensus coordinates (mean or median) per cluster
- Sample-membership vector indicating which samples contributed to each cluster
- Row count equal to or exceeding input feature count (no feature loss)

## How to apply

Load detected feature tables from all samples using deimos.load(), extracting mz, drift_time, retention_time, and intensity columns. Normalize feature coordinates across samples to a common reference frame (either a designated reference sample or a global coordinate system) to account for instrument variation. Apply N-dimensional distance-based clustering in (mz, drift_time, retention_time) space using configurable tolerances for each dimension to define matching windows; features within these tolerance windows in all dimensions are grouped into clusters. For each cluster, compute consensus coordinates (weighted mean or median) and assign cluster membership flags to track which samples contributed each feature. Filter clusters below a minimum sample-membership threshold if desired, then output the aligned feature table with original coordinates, consensus coordinates, cluster ID, and sample-membership vector.

## Related tools

- **DEIMoS** (Python API and command-line tool providing N-dimensional distance-based clustering implementation and feature alignment workflow) — https://github.com/pnnl/deimos
- **Python** (Programming language in which DEIMoS is implemented; used for scripting clustering workflows)
- **numpy** (Numerical computing library used for N-dimensional distance calculations and coordinate normalization)
- **ProteoWizard** (Converts mzML and other mass spectrometry formats for loading into DEIMoS)

## Examples

```
data_a = deimos.load('sample_a.h5', key='features', columns=['mz', 'drift_time', 'retention_time', 'intensity']); data_b = deimos.load('sample_b.h5', key='features', columns=['mz', 'drift_time', 'retention_time', 'intensity']); aligned = deimos.alignment.align([data_a, data_b], mz_tol=0.01, drift_time_tol=2.0, retention_time_tol=30.0)
```

## Evaluation signals

- Output feature table contains all required columns: mz, drift_time, retention_time, cluster_id, sample_membership; validate schema before downstream analysis.
- Row count in output equals or exceeds input row count; no features are orphaned (each row assigned exactly one cluster ID).
- Cluster membership is consistent across dimensions: features assigned to the same cluster should fall within user-defined tolerances in mz, drift_time, and retention_time simultaneously.
- Sample-membership vector captures expected sample composition; clusters with too few samples (below threshold) are filtered out if threshold was specified.
- Consensus coordinates (weighted mean or median) per cluster lie within the convex hull of input feature coordinates in that cluster, indicating valid aggregation.

## Limitations

- Clustering quality is sensitive to tolerance selection; poorly chosen tolerances will produce either over-fragmented clusters (tolerances too tight) or conflated features (tolerances too loose); tolerances must be empirically tuned to instrument and dataset characteristics.
- Non-linear coordinate variation (e.g., nonlinear drift across retention time or m/z) may not be fully captured by simple tolerance windows; DEIMoS uses reference-based and cross-sample alignment strategies to mitigate this, but extreme nonlinearity may require per-region tolerance adjustment.
- Clusters with only one contributing sample are retained in output; post-hoc filtering by sample-membership threshold is required if cross-sample features are needed.
- Algorithm assumes all samples are in a common coordinate system; if samples use different instrument calibrations or acquisition parameters, normalization to a reference frame is mandatory prior to clustering.

## Evidence

- [other] N-dimensional distance-based clustering in (mz, drift_time, retention_time) space: "Apply N-dimensional distance-based clustering in (mz, drift_time, retention_time) space to group features across samples that occupy the same region; use configurable tolerances for each dimension to"
- [other] Feature coordinate normalization to account for instrument variation: "Normalize feature coordinates across samples to a common reference frame (either a designated reference sample or a global coordinate system). 3. Apply N-dimensional distance-based clustering in (mz,"
- [other] Consensus coordinate calculation and output structure: "For each cluster, compute consensus coordinates (weighted mean or median) and assign cluster membership flags to track which samples contributed each feature. 5. Output the aligned feature table with"
- [other] Validation criteria for aligned feature output: "Validation: confirm that output contains expected columns (mz, drift_time, retention_time, cluster_id, sample_membership), row count equals or exceeds input feature count, and no features are"
- [readme] N-dimensional algorithmic advantage for alignment confidence: "algorithm implementations simultaneously utilize all dimensions to (ii) increase alignment/feature matching confidence among datasets"
