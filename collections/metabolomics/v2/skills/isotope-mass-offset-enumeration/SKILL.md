---
name: isotope-mass-offset-enumeration
description: Use when you have a detected feature table (m/z, drift_time, retention_time, intensity) from LC-IMS-MS or similar multidimensional MS data and want to identify and annotate isotopic families (e.g., singly-charged C13 patterns).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
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

# isotope-mass-offset-enumeration

## Summary

Detects isotopic variants (e.g., C13 substitutions) in mass spectrometry feature tables by enumerating expected m/z offsets and matching them against observed peaks within specified mass, drift time, and retention time tolerances. This approach improves feature annotation confidence by explicitly grouping monoisotopes with their heavier isotopologues.

## When to use

Apply this skill when you have a detected feature table (m/z, drift_time, retention_time, intensity) from LC-IMS-MS or similar multidimensional MS data and want to identify and annotate isotopic families (e.g., singly-charged C13 patterns). Use it before downstream analysis such as compound identification or quantification to avoid treating monoisotopes and isotopologues as independent features.

## When NOT to use

- Input is already an annotated or pre-processed feature table with isotopic assignments.
- Data is from a single-dimension MS instrument (e.g., ESI-MS without IMS or LC separation) where drift time and retention time filtering would be unavailable or uninformative.
- Expected isotopic mass delta is unknown or highly variable across the sample (e.g., complex mixed-charge-state data without explicit charge-state constraints).

## Inputs

- Feature table (HDF5 or mzML format) containing detected peaks with m/z, drift_time, retention_time, intensity columns
- Isotopic mass delta (e.g., 1.003355 Da for C13)
- Maximum number of isotopic substitutions (e.g., 5)
- Charge state constraint (e.g., z=+1 for singly-charged features)
- m/z tolerance (ppm), drift time tolerance, retention time tolerance

## Outputs

- Annotated feature table with isotope group identifiers
- Isotopic cluster membership assignments (monoisotope label and isotopogue count)
- Filtered feature list retaining only isotopic signatures ≥3 members

## How to apply

Load detected features from HDF5 or mzML using deimos.load() with columns m/z, drift_time, retention_time, and intensity. For each feature, calculate expected m/z values for isotopologues by adding multiples of the isotopic mass delta (1.003355 Da per C13 substitution, up to a maximum number of substitutions, typically 5). Search for matching peaks within the specified m/z tolerance window (typically constrained by expected delta and refined to ≤50 ppm m/z error). Apply secondary filters on drift time and retention time alignment to confirm isotopic membership. Retain only isotopic signatures with at least 3 members (monoisotope plus ≥2 isotopologues) to minimize false positives. Assign isotope group identifiers and export the annotated feature table using deimos.save().

## Related tools

- **DEIMoS** (Core Python API and CLI tool for executing isotope detection via m/z offset enumeration; provides deimos.load(), deimos.save(), and isotope filtering functions) — https://github.com/pnnl/deimos
- **Python** (Programming language in which DEIMoS is implemented and in which the workflow (load, calculate m/z offsets, search, filter) is scripted)
- **numpy** (Numerical operations for vectorized m/z offset calculations and tolerance-based matching)
- **ProteoWizard msconvert** (Utility to convert raw MS data into mzML format before loading into DEIMoS)

## Examples

```
import deimos; ms1 = deimos.load('example_data_peaks.h5', key='ms1', columns=['mz', 'drift_time', 'retention_time', 'intensity']); isotopes = deimos.isotope_detect(ms1, mz_delta=1.003355, max_isotopes=5, max_charge=1, mz_tol=50); deimos.save(isotopes, 'annotated_isotopes.h5', key='ms1')
```

## Evaluation signals

- Monoisotope and isotopogue peaks align within specified m/z tolerance (≤50 ppm error reported).
- Isotopic clusters contain ≥3 members (monoisotope plus ≥2 isotopologues); clusters with <3 members are filtered out.
- Drift time and retention time of matched isotopologues are within defined tolerance windows of the monoisotope, indicating co-elution and co-mobility.
- Intensity ratios among isotopologues follow expected natural abundance patterns (e.g., C13 peak ~1% of monoisotope for singly-charged species).
- Output feature table contains new isotope group identifier columns and can be validated by spot-checking a sample of annotated clusters in visualization (e.g., matplotlib plots of m/z vs. drift_time colored by group).

## Limitations

- Requires explicit specification of isotopic mass delta and maximum substitution count; does not auto-detect novel isotopic patterns (e.g., uncommon heavy isotopes like N15, S34).
- Performance degrades on highly congested m/z regions where many overlapping peaks compete for isotopic assignment; tolerance windows must be chosen carefully to balance sensitivity and specificity.
- Assumes features are within a single charge state; mixed-charge data must be pre-separated or processed in multiple passes with different charge-state constraints.
- No explicit handling of modified isotopes (e.g., deuteration) without manual recalibration of mass delta.
- Clustering algorithm depends on sequential peak matching; order of feature processing and overlap handling in congested regions may influence final isotope group assignments.

## Evidence

- [other] DEIMoS detects C13 isotopologues by specifying an m/z delta of 1.003355 Da, a maximum of 5 isotopic substitutions, and maximum charge of 1, with initial constraint by m/z tolerance from expected delta, followed by drift time and retention time tolerances, and final downselection by maximum m/z error of 50 ppm.: "DEIMoS detects C13 isotopologues by specifying an m/z delta of 1.003355 Da, a maximum of 5 isotopic substitutions, and maximum charge of 1, with initial constraint by m/z tolerance from expected"
- [intro] Functionality includes feature detection, feature alignment, collision cross section (CCS) calibration, isotope detection, and MS/MS spectral deconvolution: "Functionality includes feature detection, feature alignment, collision cross section (CCS) calibration, isotope detection, and MS/MS spectral deconvolution"
- [results] A good first screening is to only consider those isotopic signatures with at least 3 members: "A good first screening is to only consider those isotopic signatures with at least 3 members"
- [readme] DEIMoS operates on N-dimensional data, largely agnostic to acquisition instrumentation: "DEIMoS operates on N-dimensional data, largely agnostic to acquisition instrumentation"
- [readme] algorithm implementations simultaneously utilize all dimensions to (i) offer greater separation between features, thus improving detection sensitivity, (ii) increase alignment/feature matching confidence among datasets, and (iii) mitigate convolution artifacts in tandem mass spectra: "algorithm implementations simultaneously utilize all dimensions to (i) offer greater separation between features, thus improving detection sensitivity"
