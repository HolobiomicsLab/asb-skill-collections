---
name: reference-based-vs-global-coordinate-registration
description: Use when you have detected feature tables from multiple LC-IMS-MS/MS
  samples (each with mz, drift_time, retention_time, and intensity columns) and need
  to match corresponding features across datasets to enable cross-sample quantitation
  or cohort analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - DEIMoS
  - numpy
  - ProteoWizard msconvert
  techniques:
  - LC-MS
  - ion-mobility-MS
  license_tier: restricted
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

# reference-based-vs-global-coordinate-registration

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

A skill for choosing and applying either reference-sample-based or global-coordinate alignment strategies when normalizing multi-dimensional LC-IMS-MS/MS feature coordinates across multiple samples. The choice affects how instrument drift and calibration variation are accommodated during feature matching.

## When to use

You have detected feature tables from multiple LC-IMS-MS/MS samples (each with mz, drift_time, retention_time, and intensity columns) and need to match corresponding features across datasets to enable cross-sample quantitation or cohort analysis. Use this skill when you must decide whether to align all samples to a single designated reference sample (reference-based) or to a unified coordinate frame derived from all samples (global), especially when instrument drift or calibration variation is suspected.

## When NOT to use

- Input is already an aligned, consensus feature table with cluster IDs assigned
- Single-sample LC-IMS-MS/MS data requiring no cross-sample alignment
- When a reference sample is unavailable and global coordinate consensus cannot be reliably computed from the sample cohort

## Inputs

- Feature table(s) from one or more LC-IMS-MS/MS samples (HDF5, mzML, or other deimos-supported format)
- Per-sample columns: mz, drift_time, retention_time, intensity
- User-defined tolerance thresholds for each dimension (mz_tolerance, drift_time_tolerance, retention_time_tolerance)

## Outputs

- Aligned feature table with original and consensus coordinates
- Cluster ID (unique identifier for each matched feature cluster)
- Sample-membership vector (flags indicating which samples contributed to each cluster)
- Filtered or unfiltered clusters based on minimum sample-membership threshold

## How to apply

Load detected feature tables from each sample using deimos.load() and extract the (mz, drift_time, retention_time) coordinate columns. For reference-based alignment, designate one sample as the reference and compute feature-to-feature distances (in the three coordinate dimensions) between the reference and each other sample, using user-defined tolerances in each dimension to identify matches; adjust coordinates in non-reference samples to minimize distance to matched features in the reference. For global-coordinate alignment, compute consensus coordinates (e.g., weighted mean or median of all samples' coordinates for each matched feature cluster) and normalize all sample coordinates toward this unified frame. Both approaches then apply N-dimensional distance-based clustering to group features across samples within the same tolerance windows, compute final consensus coordinates for each cluster, and assign cluster membership flags. The choice between reference-based and global depends on whether a stable reference sample exists and whether you prefer sample-to-reference correction (reference-based) versus collaborative consensus correction (global).

## Related tools

- **DEIMoS** (Python API and CLI tool providing deimos.load() for loading multi-dimensional feature tables, N-dimensional distance-based clustering for feature matching, and coordinate normalization and consensus calculation) — https://github.com/pnnl/deimos
- **numpy** (Numerical computation library used for distance calculations, clustering, and consensus coordinate calculations (weighted mean/median))
- **ProteoWizard msconvert** (Optional utility for format conversion to mzML before DEIMoS processing)

## Examples

```
import deimos; import numpy as np
data_A = deimos.load('example_alignment.h5', key='A')
data_B = deimos.load('example_alignment.h5', key='B')
aligned = deimos.alignment.reference_based(data_A, data_B, mz_tol=0.01, drift_time_tol=2.0, retention_time_tol=30.0)
```

## Evaluation signals

- Output feature table contains exactly the expected columns: original mz, drift_time, retention_time, intensity; consensus mz, drift_time, retention_time; cluster_id; and sample_membership vector
- Row count in aligned output is greater than or equal to the input row count (no features lost during clustering)
- Every feature row is assigned exactly one cluster ID; no orphaned features exist
- For reference-based alignment: features in the reference sample map to themselves (distance ≈ 0); for global alignment: consensus coordinates lie within the observed range of all input samples' coordinates
- Cluster membership vectors are consistent: each cluster contains at least one sample (or meets the user-defined minimum sample-membership threshold); clusters with insufficient membership are filtered if thresholding is applied

## Limitations

- Reference-based alignment depends on choosing a suitable reference sample; a poor choice (e.g., one with severe instrumental artifacts) can bias the entire alignment
- Global-coordinate alignment assumes that a meaningful consensus coordinate can be computed across all samples; if samples are highly heterogeneous (e.g., different instruments or calibrations), consensus may not be representative
- User-defined tolerances (mz_tolerance, drift_time_tolerance, retention_time_tolerance) must be carefully chosen; overly loose tolerances cause false matches, while overly tight tolerances cause feature fragmentation and orphaning
- Nonlinear instrumental drift or calibration effects within a sample cannot be corrected by coordinate normalization alone; DEIMoS's approach assumes piecewise-linear or smooth variation that can be captured by sample-level offset/scaling

## Evidence

- [methods] Reference-based and cross-sample alignment strategies: "Reference-based alignment defines corresponding features between two samples by minimum distance in the dimension of interest using selected tolerances to accommodate potentially complex nonlinear"
- [methods] Coordinate normalization and consensus calculation: "Both approaches adjust feature coordinates to account for instrument variation such as drift and calibration."
- [methods] N-dimensional clustering approach: "Apply N-dimensional distance-based clustering in (mz, drift_time, retention_time) space to group features across samples that occupy the same region"
- [methods] Consensus coordinate computation and cluster membership: "For each cluster, compute consensus coordinates (weighted mean or median) and assign cluster membership flags to track which samples contributed each feature."
- [methods] Validation requirements: "Validation: confirm that output contains expected columns (mz, drift_time, retention_time, cluster_id, sample_membership), row count equals or exceeds input feature count, and no features are"
- [results] DEIMoS input API: "Load detected feature tables from multiple samples using the deimos.load() API, extracting mz, drift_time, retention_time, and intensity columns."
- [readme] N-dimensional algorithmic advantages: "algorithm implementations simultaneously utilize all dimensions to (i) offer greater separation between features, thus improving detection sensitivity, (ii) increase alignment/feature matching"
