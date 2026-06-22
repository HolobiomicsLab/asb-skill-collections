---
name: feature-table-consensus-aggregation
description: Use when you have detected feature tables from multiple LC-IMS-MS/MS samples and need to establish a unified feature catalog in which each row represents a distinct molecular entity observed across one or more samples, with harmonized m/z, drift time, and retention time coordinates.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - DEIMoS
  - numpy
  - ProteoWizard msconvert
  techniques:
  - ion-mobility-MS
  - tandem-MS
  - NMR
derived_from:
- doi: 10.1021/acs.analchem.1c05017
  title: deimos
evidence_spans:
- DEIMoS is a Python application programming interface
- DEIMoS is a Python application programming interface and command-line tool
- Functionality includes feature detection, feature alignment, collision cross section (CCS) calibration, isotope detection, and MS/MS spectral deconvolution
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# feature-table-consensus-aggregation

## Summary

Aggregate aligned multi-sample LC-IMS-MS/MS features into consensus coordinates and cluster memberships to produce a unified, deduplicated feature table suitable for downstream quantitation and comparison. This skill reconciles instrument drift and calibration variation by computing weighted means or medians across clustered features in (mz, drift_time, retention_time) space.

## When to use

You have detected feature tables from multiple LC-IMS-MS/MS samples and need to establish a unified feature catalog in which each row represents a distinct molecular entity observed across one or more samples, with harmonized m/z, drift time, and retention time coordinates. Apply this skill after cross-sample feature alignment but before quantitative comparison or statistical testing.

## When NOT to use

- Input is already a deduplicated feature table or consensus feature list from a prior run.
- Samples have been processed using orthogonal clustering or consensus methods incompatible with tolerance-based N-dimensional distance matching.
- Tolerances cannot be reasonably estimated from instrument calibration data or pilot data; clustering will produce spurious or oversplit clusters.

## Inputs

- Multiple detected feature tables (HDF5 .h5 format or mzML) with columns: mz, drift_time, retention_time, intensity
- Reference sample or global coordinate system for normalization
- User-defined tolerance thresholds for each dimension (mz_tol, drift_time_tol, retention_time_tol)

## Outputs

- Aligned feature table with columns: original_mz, original_drift_time, original_retention_time, consensus_mz, consensus_drift_time, consensus_retention_time, cluster_id, sample_membership, intensity (or intensity aggregates)
- Cluster membership assignments (which samples contributed to each consensus feature)
- Optional: cluster statistics (number of members, coordinate variance, weighted mean/median basis)

## How to apply

After loading detected feature tables from multiple samples using deimos.load() with columns [mz, drift_time, retention_time, intensity], normalize feature coordinates to a common reference frame (either a designated reference sample or global coordinate system) to correct for instrument drift and calibration. Apply N-dimensional distance-based clustering in (mz, drift_time, retention_time) space using user-defined tolerances (e.g., mz_tol, drift_time_tol, retention_time_tol) to group features that occupy the same region across samples. For each cluster, compute consensus coordinates as a weighted mean or median of member features (weights may reflect intensity or sample membership rank). Assign a unique cluster_id and sample-membership vector to track which samples contributed each feature. Optionally filter clusters below a user-defined minimum sample-membership threshold (e.g., require presence in ≥2 samples). Output the aligned feature table with original coordinates, consensus coordinates, cluster_id, and sample_membership columns. The rationale is that consensus aggregation leverages the full dimensionality of drift time and retention time to distinguish true features from noise and instrument artifacts, improving both detection sensitivity and alignment confidence across datasets.

## Related tools

- **DEIMoS** (Python API and CLI for N-dimensional feature detection, alignment, and consensus aggregation via deimos.load() and clustering workflows) — https://github.com/pnnl/deimos
- **numpy** (N-dimensional array operations and distance-based clustering (e.g., for computing pairwise distances and grouping features))
- **ProteoWizard msconvert** (Conversion of raw vendor LC-IMS-MS/MS formats to mzML for input to DEIMoS)

## Examples

```
import deimos; data_A = deimos.load('sample_A.h5', key='ms1', columns=['mz', 'drift_time', 'retention_time', 'intensity']); data_B = deimos.load('sample_B.h5', key='ms1', columns=['mz', 'drift_time', 'retention_time', 'intensity']); aligned = deimos.alignment.align_features([data_A, data_B], mz_tol=0.01, dt_tol=2.0, rt_tol=10.0)
```

## Evaluation signals

- Output feature table contains expected columns (consensus_mz, consensus_drift_time, consensus_retention_time, cluster_id, sample_membership) with correct data types and no missing values.
- Row count in output equals the number of unique clusters; verify no features are orphaned (each row has exactly one cluster_id and a valid sample_membership vector).
- Consensus coordinates fall within the range of original feature coordinates for each cluster; detect outliers or coordinate flips that indicate clustering failure.
- Sample-membership vectors are correctly populated; each sample that contributed a feature to a cluster is listed in that cluster's sample_membership field.
- Cluster statistics (e.g., r-squared of fit to consensus coordinates, coordinate variance within clusters) meet expected thresholds from validation data (article reports r² ≈ 0.9999 for alignment tasks).

## Limitations

- Tolerance parameters are instrument- and dataset-specific; misspecified tolerances lead to over-clustering (merged true features) or under-clustering (split features into multiple clusters).
- N-dimensional distance-based clustering can be computationally expensive for very large feature tables (thousands of features × many samples); scalability depends on sample count and tolerance widths.
- Consensus coordinate computation assumes features within a cluster share a common molecular identity; violations (e.g., co-eluting isotopologs or isobars) can corrupt consensus values.
- The method assumes instrument drift and calibration are the primary source of coordinate variation; systematic biases or sample-specific chemical shifts may not be fully corrected by simple normalization.

## Evidence

- [other] Reference-based alignment defines corresponding features between two samples by minimum distance in the dimension of interest using selected tolerances to accommodate potentially complex nonlinear relationships, while cross-sample alignment matches corresponding features across datasets within user-defined tolerance.: "Reference-based alignment defines corresponding features between two samples by minimum distance in the dimension of interest using selected tolerances to accommodate potentially complex nonlinear"
- [other] Apply N-dimensional distance-based clustering in (mz, drift_time, retention_time) space to group features across samples that occupy the same region; use configurable tolerances for each dimension to define matching windows.: "Apply N-dimensional distance-based clustering in (mz, drift_time, retention_time) space to group features across samples that occupy the same region; use configurable tolerances for each dimension to"
- [other] For each cluster, compute consensus coordinates (weighted mean or median) and assign cluster membership flags to track which samples contributed each feature.: "For each cluster, compute consensus coordinates (weighted mean or median) and assign cluster membership flags to track which samples contributed each feature."
- [readme] algorithm implementations simultaneously utilize all dimensions to (i) offer greater separation between features, thus improving detection sensitivity, (ii) increase alignment/feature matching confidence among datasets: "algorithm implementations simultaneously utilize all dimensions to (i) offer greater separation between features, thus improving detection sensitivity, (ii) increase alignment/feature matching"
- [other] Validation: confirm that output contains expected columns (mz, drift_time, retention_time, cluster_id, sample_membership), row count equals or exceeds input feature count, and no features are orphaned (each row assigned exactly one cluster ID).: "Validation: confirm that output contains expected columns (mz, drift_time, retention_time, cluster_id, sample_membership), row count equals or exceeds input feature count, and no features are"
