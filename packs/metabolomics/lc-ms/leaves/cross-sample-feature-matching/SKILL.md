---
name: cross-sample-feature-matching
description: Use when you have detected feature tables from two or more LC-IMS-MS/MS
  samples and need to establish correspondence between features across samples to
  enable quantitative comparison, statistical analysis, or consensus feature calling.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - DEIMoS
  - numpy
  - ProteoWizard msconvert
  - conda
  techniques:
  - LC-MS
  - ion-mobility-MS
  license_tier: open
  provenance_tier: literature
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

# cross-sample-feature-matching

## Summary

Aligns detected features across multiple LC-IMS-MS/MS samples by clustering features in N-dimensional (mz, drift_time, retention_time) space within user-defined tolerances, producing a unified feature table with cluster IDs and sample-membership vectors. This skill is essential when analyzing multi-sample metabolomics or proteomics datasets where instrument drift and calibration variation must be compensated for to enable robust downstream comparative analysis.

## When to use

Apply this skill when you have detected feature tables from two or more LC-IMS-MS/MS samples and need to establish correspondence between features across samples to enable quantitative comparison, statistical analysis, or consensus feature calling. Specifically, use this skill after feature detection (when each sample has its own mz, drift_time, retention_time, and intensity columns) but before quantitative downstream analysis (e.g., abundance comparison, pathway analysis) that assumes features are matched across the study cohort.

## When NOT to use

- Input is already a pre-aligned feature matrix (e.g., from a previous alignment run or vendor software)—use this skill only on raw detected feature tables.
- Single-sample analysis where cross-sample matching is not required (e.g., characterizing one sample's chemical composition).
- Datasets with severely misaligned retention time or drift time axes (e.g., different LC column configurations or ion mobility calibrations not yet corrected)—alignment quality depends on relatively consistent instrumental conditions.

## Inputs

- Detected feature tables from multiple samples (HDF5, mzML, or tabular format)
- mz column (mass-to-charge ratio, typically in Da)
- drift_time column (ion mobility dimension, typically in milliseconds or reduced mobility units)
- retention_time column (chromatographic dimension, typically in seconds)
- intensity column (signal intensity for each feature)

## Outputs

- Aligned feature table (HDF5 or tabular format) containing: original mz, drift_time, retention_time, intensity per sample
- Consensus coordinates (weighted mean or median mz, drift_time, retention_time) for each cluster
- cluster_id column (unique identifier for each feature cluster)
- sample_membership vector (binary or count vector indicating which samples contributed to each cluster)
- Optional: filtered feature set (clusters meeting minimum sample-membership threshold)

## How to apply

Load detected feature tables from all samples using the deimos.load() API, extracting mz, drift_time, retention_time, and intensity columns. Normalize feature coordinates across samples to a common reference frame (either a designated reference sample or global coordinate system) to account for instrument drift and calibration variation. Apply N-dimensional distance-based clustering in (mz, drift_time, retention_time) space to group features occupying the same region across samples, using configurable tolerances for each dimension (e.g., 10 ppm for mz, ±10 drift_time units, ±30 s retention_time) to define matching windows. For each resulting cluster, compute consensus coordinates (weighted mean or median) and assign cluster membership flags tracking which samples contributed each feature. Output the aligned feature table with original coordinates, consensus coordinates, cluster ID, and a sample-membership vector; optionally filter clusters below a minimum sample-membership threshold (e.g., require features to be present in ≥2 samples) to focus on reproducible detections.

## Related tools

- **DEIMoS** (Core Python API and command-line tool providing N-dimensional feature alignment, distance-based clustering, and normalized coordinate output via deimos.load() and alignment functions) — https://github.com/pnnl/deimos
- **ProteoWizard msconvert** (Format conversion utility to prepare raw mass spectrometry data (various vendor formats) to mzML for DEIMoS input)
- **numpy** (N-dimensional array operations and distance calculations in feature clustering)
- **conda** (Virtual environment and dependency management for DEIMoS installation and execution)

## Examples

```
import deimos
data_A = deimos.load('sample_A_features.h5', key='ms1', columns=['mz', 'drift_time', 'retention_time', 'intensity'])
data_B = deimos.load('sample_B_features.h5', key='ms1', columns=['mz', 'drift_time', 'retention_time', 'intensity'])
aligned = deimos.alignment.align([data_A, data_B], mz_tol=10, dt_tol=10, rt_tol=30)
aligned.to_hdf5('aligned_features.h5')
```

## Evaluation signals

- Output feature table contains all expected columns: original mz, drift_time, retention_time, intensity, consensus coordinates, cluster_id, and sample_membership vector.
- Row count in output is equal to or exceeds the total input feature count (no features are dropped or orphaned).
- Each row is assigned exactly one cluster_id; no features appear in multiple clusters.
- Cluster membership vectors are consistent (e.g., if a feature's sample_membership indicates it came from samples A and B, those samples' original feature tables must contain entries within the tolerance windows of the consensus coordinates).
- Consensus coordinates fall within the range of original feature coordinates contributed to each cluster (no consensus drift outside contributor range).

## Limitations

- Alignment quality depends on user-defined tolerances for each dimension; tolerances that are too loose may create spurious feature clusters, while tolerances that are too tight may fragment true biological features into multiple clusters.
- Reference-based and cross-sample alignment approaches both assume relatively consistent instrumental conditions across samples; severe instrument drift or calibration shifts not pre-corrected will reduce matching confidence.
- The method is agnostic to tandem mass spectra and isotopic signatures—for more robust feature annotation and validation, consider combining this skill with DEIMoS isotope detection and MS/MS spectral deconvolution (post-alignment).
- No changelog is available for DEIMoS, limiting traceability of algorithm changes across versions.

## Evidence

- [other] Reference-based alignment defines corresponding features between two samples by minimum distance in the dimension of interest using selected tolerances to accommodate potentially complex nonlinear relationships, while cross-sample alignment matches corresponding features across datasets within user-defined tolerance.: "Reference-based alignment defines corresponding features between two samples by minimum distance in the dimension of interest using selected tolerances to accommodate potentially complex nonlinear"
- [other] Both approaches adjust feature coordinates to account for instrument variation such as drift and calibration.: "Both approaches adjust feature coordinates to account for instrument variation such as drift and calibration."
- [other] Apply N-dimensional distance-based clustering in (mz, drift_time, retention_time) space to group features across samples that occupy the same region; use configurable tolerances for each dimension to define matching windows.: "Apply N-dimensional distance-based clustering in (mz, drift_time, retention_time) space to group features across samples that occupy the same region; use configurable tolerances for each dimension to"
- [other] For each cluster, compute consensus coordinates (weighted mean or median) and assign cluster membership flags to track which samples contributed each feature.: "For each cluster, compute consensus coordinates (weighted mean or median) and assign cluster membership flags to track which samples contributed each feature."
- [other] Output the aligned feature table with original coordinates, consensus coordinates, cluster ID, and sample-membership vector; optionally filter clusters below a minimum sample-membership threshold.: "Output the aligned feature table with original coordinates, consensus coordinates, cluster ID, and sample-membership vector; optionally filter clusters below a minimum sample-membership threshold."
- [other] Confirm that output contains expected columns (mz, drift_time, retention_time, cluster_id, sample_membership), row count equals or exceeds input feature count, and no features are orphaned (each row assigned exactly one cluster ID).: "Confirm that output contains expected columns (mz, drift_time, retention_time, cluster_id, sample_membership), row count equals or exceeds input feature count, and no features are orphaned (each row"
- [intro] algorithm implementations simultaneously utilize all dimensions to (ii) increase alignment/feature matching confidence among datasets: "algorithm implementations simultaneously utilize all dimensions to (ii) increase alignment/feature matching confidence among datasets"
- [other] Load detected feature tables from multiple samples using the deimos.load() API, extracting mz, drift_time, retention_time, and intensity columns.: "Load detected feature tables from multiple samples using the deimos.load() API, extracting mz, drift_time, retention_time, and intensity columns."
