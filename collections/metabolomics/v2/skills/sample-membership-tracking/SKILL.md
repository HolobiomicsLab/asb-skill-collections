---
name: sample-membership-tracking
description: Use when when aligning detected features across multiple LC-IMS-MS/MS
  samples and you need to identify which input samples contributed to each consensus
  feature cluster, especially to filter out spurious or low-confidence alignments,
  validate clustering completeness, or perform sample-specific.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3938
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

# sample-membership-tracking

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Track which samples contributed each aligned feature across multiple LC-IMS-MS/MS datasets by assigning cluster membership flags during N-dimensional feature alignment. This enables downstream filtering, validation, and cross-sample feature interpretation.

## When to use

When aligning detected features across multiple LC-IMS-MS/MS samples and you need to identify which input samples contributed to each consensus feature cluster, especially to filter out spurious or low-confidence alignments, validate clustering completeness, or perform sample-specific downstream analyses (e.g., isotope detection, CCS calibration) on subsets of aligned features.

## When NOT to use

- Input is already a curated, non-redundant feature list with known sample origins — membership tracking adds redundancy and computational overhead.
- Single-sample analysis: membership tracking is only meaningful when aligning across two or more samples.
- Real-time streaming acquisition with no fixed sample boundaries: membership tracking assumes discrete, pre-defined sample cohorts.

## Inputs

- Multiple detected feature tables (HDF5 or mzML format) with columns: mz, drift_time, retention_time, intensity, and sample identifier
- N-dimensional distance-based clusters from feature alignment (cluster_id assignments in mz, drift_time, retention_time space)
- User-defined tolerances for each dimension and optional minimum sample-membership threshold

## Outputs

- Aligned feature table with columns: original_mz, original_drift_time, original_retention_time, consensus_mz, consensus_drift_time, consensus_retention_time, intensity, cluster_id, sample_membership_vector
- Sample-membership summary (cluster_id → set of contributing sample IDs or binary membership array)

## How to apply

During the cross-sample feature alignment workflow, after N-dimensional distance-based clustering groups features across samples in (mz, drift_time, retention_time) space, assign a sample-membership vector to each cluster that records which input samples contributed at least one feature to that cluster. Represent this vector as a binary indicator array (or equivalent sparse representation) with length equal to the number of input samples. Optionally apply a minimum sample-membership threshold (e.g., 'only report clusters present in ≥2 samples') to filter out singleton or instrument-artifact features before output. Validate that each feature row is assigned exactly one cluster ID and that the membership vector is consistent with the cluster's constituent features.

## Related tools

- **DEIMoS** (N-dimensional feature alignment and clustering engine; handles feature detection, alignment, and cluster assignment before membership tracking) — https://github.com/pnnl/deimos
- **Python** (Programming language for implementing sample-membership vector assignment, threshold filtering, and validation logic)
- **numpy** (Efficient array operations for constructing and manipulating binary or sparse sample-membership vectors)
- **ProteoWizard** (Converts LC-IMS-MS/MS data from proprietary formats (e.g. .raw, .d) to mzML before DEIMoS ingestion)

## Examples

```
import deimos; import numpy as np
data_A = deimos.load('example_alignment.h5', key='A')
data_B = deimos.load('example_alignment.h5', key='B')
aligned = deimos.align(data_A, data_B, tol_mz=10, tol_dt=5, tol_rt=10)
print(aligned[['cluster_id', 'sample_membership']].head())
```

## Evaluation signals

- Output feature table contains exactly one cluster_id per row and all rows have a sample_membership_vector assigned (no orphaned features).
- Total number of output rows ≥ input feature count (no features lost during clustering and membership assignment).
- Each cluster's membership vector is consistent: the set of samples listed in the vector matches the set of sample origins for all features in that cluster.
- If minimum sample-membership threshold is applied, all output clusters have ≥ threshold members; if threshold = 2, no singleton clusters remain in final output.
- Row count and membership statistics match expected values from controlled test data (e.g., example_alignment.h5) with known ground truth.

## Limitations

- Sample-membership tracking accuracy depends on prior feature detection and alignment quality; clustering errors will propagate to membership assignments.
- Membership vectors assume discrete, non-overlapping sample cohorts; they do not capture within-sample technical replication or pooled/mixed samples.
- High-dimensional (>4D) alignment may suffer from the curse of dimensionality, leading to loose or spurious clusters with mixed sample membership despite low tolerance thresholds.
- Minimum sample-membership thresholds can discard genuine low-abundance features present in few samples, creating a bias toward high-abundance analytes.

## Evidence

- [methods] Clusters are formed and membership tracked during cross-sample alignment.: "For each cluster, compute consensus coordinates (weighted mean or median) and assign cluster membership flags to track which samples contributed each feature."
- [methods] Sample-membership output is a key deliverable of the alignment workflow.: "Output the aligned feature table with original coordinates, consensus coordinates, cluster ID, and sample-membership vector; optionally filter clusters below a minimum sample-membership threshold."
- [methods] Validation includes checking that membership tracking is complete and consistent.: "Validation: confirm that output contains expected columns (mz, drift_time, retention_time, cluster_id, sample_membership), row count equals or exceeds input feature count, and no features are"
- [readme] DEIMoS is instrument-agnostic and operates on multi-dimensional data using cluster-based alignment.: "DEIMoS operates on N-dimensional data, largely agnostic to acquisition instrumentation; algorithm implementations simultaneously utilize all dimensions to (ii) increase alignment/feature matching"
