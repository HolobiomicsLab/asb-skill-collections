---
name: spectral-feature-annotation-and-labeling
description: Use when you have a detected feature table (m/z, drift_time, retention_time, intensity) and need to identify and label C13 isotopic clusters for singly-charged features (z=+1).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0630
  tools:
  - DEIMoS
  - Python
  - numpy
  - ProteoWizard msconvert
derived_from:
- doi: 10.1021/acs.analchem.1c05017
  title: deimos
evidence_spans:
- Functionality includes feature detection, feature alignment, collision cross section (CCS) calibration, isotope detection, and MS/MS spectral deconvolution
- import deimos
- DEIMoS is a Python application programming interface
- DEIMoS is a Python application programming interface and command-line tool
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

# spectral-feature-annotation-and-labeling

## Summary

Assign isotopic group identifiers to detected mass spectrometry features by enumerating C13 singly-charged isotopologues and clustering matches within m/z, drift time, and retention time tolerances. This skill enables systematic labeling of isotopic clusters in high-dimensional MS data, improving feature characterization and downstream analysis confidence.

## When to use

Apply this skill when you have a detected feature table (m/z, drift_time, retention_time, intensity) and need to identify and label C13 isotopic clusters for singly-charged features (z=+1). This is especially valuable when working with LC-IMS-MS/MS data where multidimensional separation improves isotopic signature confidence, or when you want to filter features by isotopic membership (e.g., monoisotope vs. satellite isotopologues) before downstream annotation or quantification.

## When NOT to use

- Input features are multiply-charged (z > 1); this workflow is restricted to singly-charged species and does not enumerate multiply-charged isotopic patterns.
- Feature table already contains pre-assigned isotope labels or has been filtered to monoisotopes only; re-annotation risks inconsistency.
- Raw spectral data rather than detected features; use feature detection workflow first.

## Inputs

- Feature table (HDF5 or mzML format) containing detected features with columns: m/z, drift_time, retention_time, intensity

## Outputs

- Annotated feature table with isotope group identifiers assigned to each feature
- Isotopic cluster membership (monoisotope vs. isotopologue designation)

## How to apply

Load the detected feature table using deimos.load() specifying columns ['mz', 'drift_time', 'retention_time', 'intensity']. For each feature, calculate expected m/z values for C13 isotopologues using an m/z delta of 1.003355 Da per carbon substitution, with a maximum of 5 isotopic substitutions and constraint to singly-charged features (z=+1). Search within a user-defined m/z tolerance window (typically constrained by expected delta and max m/z error of 50 ppm) for matching peaks in the feature list. Apply secondary filters on drift time and retention time tolerances to form isotopic clusters. Retain only isotopic signatures containing at least 3 members (monoisotope plus ≥2 isotopologues) to avoid spurious assignments. Assign unique isotope group identifiers to each cluster and export the annotated feature table using deimos.save().

## Related tools

- **DEIMoS** (Core API for loading feature tables, enumerating isotopic m/z offsets, filtering by multidimensional tolerances, and exporting annotated feature tables) — https://github.com/pnnl/deimos
- **numpy** (Numerical computation for vectorized m/z delta enumeration and tolerance filtering across feature arrays)
- **ProteoWizard msconvert** (Convert raw MS data formats to mzML before DEIMoS feature detection and isotope annotation)

## Examples

```
import deimos; ms1 = deimos.load('example_data.h5', key='ms1', columns=['mz', 'drift_time', 'retention_time', 'intensity']); isotopes = deimos.isotope_detection(ms1, delta=1.003355, max_charge=1, mz_tol=0.05, max_isotopes=5); annotated = isotopes[isotopes.groupby('isotope_id').size() >= 3]; deimos.save(annotated, 'annotated_features.h5', key='ms1')
```

## Evaluation signals

- All assigned isotopic clusters contain at least 3 members (monoisotope + ≥2 isotopologues); verify cluster size distribution.
- m/z differences within each cluster match the expected 1.003355 Da per C13 substitution within the specified 50 ppm error tolerance.
- Drift time and retention time differences between cluster members are within the user-specified tolerance thresholds; check for temporal coherence across dimensions.
- No feature is assigned to multiple isotope groups; verify unique membership (one isotope group ID per feature).
- Monoisotope features have the lowest m/z within each cluster; validate isotopic ordering consistent with natural abundance patterns.

## Limitations

- Workflow is restricted to singly-charged features (z=+1); multiply-charged isotopologues require separate enumeration logic.
- Assumes C13 isotopic substitution only; does not account for other isotopologues (e.g., N15, S34, chlorine/bromine isotopes).
- Minimum cluster size (3 members) may exclude low-abundance isotopic species or high-mass compounds with sparse C13 representation.
- Performance and accuracy depend critically on input m/z measurement accuracy and specified tolerance windows; miscalibrated data may result in missed or false-positive cluster assignments.

## Evidence

- [other] DEIMoS detects C13 isotopologues by specifying an m/z delta of 1.003355 Da, a maximum of 5 isotopic substitutions, and maximum charge of 1: "DEIMoS detects C13 isotopologues by specifying an m/z delta of 1.003355 Da, a maximum of 5 isotopic substitutions, and maximum charge of 1"
- [other] initial constraint by m/z tolerance from expected delta, followed by drift time and retention time tolerances, and final downselection by maximum m/z error of 50 ppm: "initial constraint by m/z tolerance from expected delta, followed by drift time and retention time tolerances, and final downselection by maximum m/z error of 50 ppm"
- [other] Filter isotopic signatures to retain only those with at least 3 members (monoisotope plus ≥2 isotopologues): "Filter isotopic signatures to retain only those with at least 3 members (monoisotope plus ≥2 isotopologues)"
- [other] Assign isotope group identifiers and export the annotated feature table with isotopic group membership using deimos.save(): "Assign isotope group identifiers and export the annotated feature table with isotopic group membership using deimos.save()"
- [readme] Functionality includes feature detection, feature alignment, collision cross section (CCS) calibration, isotope detection, and MS/MS spectral deconvolution: "Functionality includes feature detection, feature alignment, collision cross section (CCS) calibration, isotope detection, and MS/MS spectral deconvolution"
- [readme] algorithm implementations simultaneously utilize all dimensions to (ii) increase alignment/feature matching confidence among datasets: "algorithm implementations simultaneously utilize all dimensions to (ii) increase alignment/feature matching confidence among datasets"
