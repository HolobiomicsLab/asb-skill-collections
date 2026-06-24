---
name: multidimensional-coordinate-alignment
description: Use when you have detected feature tables from two or more LC-IMS-MS/MS
  samples (each containing m/z, drift_time, retention_time, and intensity measurements)
  and need to identify which features correspond to the same chemical compound across
  samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
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

# multidimensional-coordinate-alignment

## Summary

Aligns detected features across multiple LC-IMS-MS/MS samples by clustering them in N-dimensional space (m/z, drift time, retention time) using configurable tolerances, producing consensus coordinates and sample-membership vectors. This skill is essential when matching corresponding chemical features across datasets to account for instrument drift, calibration variation, and nonlinear retention-time shifts.

## When to use

Apply this skill when you have detected feature tables from two or more LC-IMS-MS/MS samples (each containing m/z, drift_time, retention_time, and intensity measurements) and need to identify which features correspond to the same chemical compound across samples. Specifically, when reference-based alignment (matching against a single reference sample) or cross-sample alignment (matching all features within user-defined windows) is required to combine multi-sample datasets for downstream analysis such as comparative metabolomics or biomarker discovery.

## When NOT to use

- Input is already an aligned feature table from a single sample or prior alignment step; skip to downstream analysis (e.g., isotope detection, CCS calibration).
- Samples contain only a single feature or fewer than two samples to align; alignment requires cross-sample correspondence.
- Feature coordinates are already in a normalized, consensus space; re-alignment would introduce redundant normalization.
- Raw MS data (mzML/mzXML) has not yet been processed through feature detection; run feature detection first.

## Inputs

- Detected feature table (HDF5 or mzML format) with columns: m/z, drift_time, retention_time, intensity
- Multiple sample datasets (≥2 samples for cross-sample alignment)
- User-defined tolerances for each dimension (m/z ppm, drift_time ms, retention_time min)
- Optional: reference sample designation or global coordinate frame definition

## Outputs

- Aligned feature table (HDF5 format) with columns: original_mz, original_drift_time, original_retention_time, intensity, consensus_mz, consensus_drift_time, consensus_retention_time, cluster_id, sample_membership_vector
- Cluster-level metadata: cluster ID, consensus coordinates, per-sample contribution counts
- Optional: filtered feature table (clusters meeting minimum sample-membership threshold)

## How to apply

Load detected feature tables from each sample using the deimos.load() API, extracting m/z, drift_time, retention_time, and intensity columns. Normalize feature coordinates across samples to a common reference frame (either a designated reference sample or a global coordinate system) to correct for instrument variation such as drift and calibration shifts. Apply N-dimensional distance-based clustering in (m/z, drift_time, retention_time) space using configurable tolerances (e.g., ppm for m/z, ms for drift_time, min for retention_time) to group features that occupy the same region across samples. For each cluster, compute consensus coordinates using weighted mean or median, and assign a cluster ID and sample-membership vector tracking which samples contributed each feature. Filter clusters below a minimum sample-membership threshold if desired (e.g., retain only clusters present in ≥2 samples). Output the aligned feature table with original coordinates, consensus coordinates, cluster ID, and sample-membership vector.

## Related tools

- **DEIMoS** (N-dimensional feature detection and alignment API; executes distance-based clustering in multidimensional space and computes consensus coordinates) — https://github.com/pnnl/deimos
- **Python** (Programming language for DEIMoS API scripting and data manipulation)
- **numpy** (Numerical computation for coordinate transformation, distance metrics, and weighted mean/median calculations)
- **ProteoWizard msconvert** (Format conversion to mzML for input to DEIMoS; enables reading of raw MS data from vendor instruments)

## Examples

```
import deimos
data_A = deimos.load('sample_A.h5', key='ms1', columns=['mz', 'drift_time', 'retention_time', 'intensity'])
data_B = deimos.load('sample_B.h5', key='ms1', columns=['mz', 'drift_time', 'retention_time', 'intensity'])
aligned = deimos.align([data_A, data_B], mz_tol=10, drift_time_tol=0.5, retention_time_tol=1.0)
```

## Evaluation signals

- Output feature table contains all expected columns: original_mz, original_drift_time, original_retention_time, consensus_mz, consensus_drift_time, consensus_retention_time, cluster_id, sample_membership_vector.
- Row count in output ≥ row count in input (no features orphaned or lost).
- Each output row is assigned exactly one cluster_id; no features belong to multiple clusters or zero clusters.
- Consensus coordinates lie within the bounding box of the original coordinates for each cluster; no wildly displaced centroids.
- Sample-membership vectors correctly reflect which input samples contributed to each cluster (binary or count vector with expected cardinality).
- r-squared between reference and consensus coordinates is ≥ 0.99 (indicating high fidelity of alignment; article reports r² ≈ 0.9999).

## Limitations

- Alignment accuracy depends critically on user-defined tolerance thresholds; overly loose tolerances lead to false positives (merging distinct features), while overly tight tolerances cause false negatives (missed alignments). No automatic tolerance selection is provided.
- N-dimensional clustering assumes that corresponding features occupy nearby regions in all dimensions simultaneously; complex nonlinear relationships (e.g., time-dependent drift or calibration shifts) may require pre-normalization or reference-sample-based alignment to account for systematic offsets.
- Consensus coordinate computation (weighted mean or median) may not reflect the true molecular m/z or CCS if samples have systematic biases; validation against external standards is recommended.
- DEIMoS is largely agnostic to instrumentation but assumes input features have been correctly detected; poor feature detection upstream will propagate errors into alignment.
- No changelog is available, limiting visibility into version-to-version changes or known issues.

## Evidence

- [other] Reference-based alignment defines corresponding features between two samples by minimum distance in the dimension of interest using selected tolerances to accommodate potentially complex nonlinear relationships: "Reference-based alignment defines corresponding features between two samples by minimum distance in the dimension of interest using selected tolerances to accommodate potentially complex nonlinear"
- [other] Apply N-dimensional distance-based clustering in (mz, drift_time, retention_time) space to group features across samples that occupy the same region; use configurable tolerances for each dimension: "Apply N-dimensional distance-based clustering in (mz, drift_time, retention_time) space to group features across samples that occupy the same region; use configurable tolerances for each dimension"
- [other] For each cluster, compute consensus coordinates (weighted mean or median) and assign cluster membership flags to track which samples contributed each feature: "For each cluster, compute consensus coordinates (weighted mean or median) and assign cluster membership flags to track which samples contributed each feature"
- [other] Output the aligned feature table with original coordinates, consensus coordinates, cluster ID, and sample-membership vector; optionally filter clusters below a minimum sample-membership threshold: "Output the aligned feature table with original coordinates, consensus coordinates, cluster ID, and sample-membership vector; optionally filter clusters below a minimum sample-membership threshold"
- [other] Load detected feature tables from multiple samples using the deimos.load() API, extracting mz, drift_time, retention_time, and intensity columns: "Load detected feature tables from multiple samples using the deimos.load() API, extracting mz, drift_time, retention_time, and intensity columns"
- [readme] DEIMoS operates on N-dimensional data, largely agnostic to acquisition instrumentation: "DEIMoS operates on N-dimensional data, largely agnostic to acquisition instrumentation"
- [readme] algorithm implementations simultaneously utilize all dimensions to (i) offer greater separation between features, thus improving detection sensitivity, (ii) increase alignment/feature matching confidence among datasets: "algorithm implementations simultaneously utilize all dimensions to (i) offer greater separation between features, thus improving detection sensitivity, (ii) increase alignment/feature matching"
