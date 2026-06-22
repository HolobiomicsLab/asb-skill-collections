---
name: singly-charged-ion-mass-calculation
description: Use when you have detected monoisotopic features (m/z, drift_time, retention_time, intensity) from LC-IMS-MS/MS data and need to identify and cluster their C13 isotopologues for charge state z=+1.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - DEIMoS
  - Python
  - numpy
  - ProteoWizard msconvert
  techniques:
  - LC-MS
  - ion-mobility-MS
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# singly-charged-ion-mass-calculation

## Summary

Calculate expected m/z values for C13 isotopologues of singly-charged ions by applying a fixed m/z delta (1.003355 Da per carbon substitution) to detected monoisotopic features. This skill is essential for enumerating and matching isotopic clusters in high-resolution mass spectrometry data.

## When to use

Apply this skill when you have detected monoisotopic features (m/z, drift_time, retention_time, intensity) from LC-IMS-MS/MS data and need to identify and cluster their C13 isotopologues for charge state z=+1. Use it as the first step in isotope detection workflows to systematically search for isotopic variants before applying retention time, drift time, and m/z error filters.

## When NOT to use

- Input features are already annotated with isotope group membership or have been pre-filtered to monoisotopes only.
- The sample or compound set contains ions with charge state z ≠ +1 (e.g., doubly-charged or multiply-charged species); this skill assumes singly-charged m/z deltas and will produce incorrect predictions for higher charges.
- Mass spectrometry data lacks sufficient resolution or accuracy to reliably detect the 1.003355 Da isotopic shift (e.g., low-resolution TOF or Orbitrap at <50 ppm accuracy).

## Inputs

- Detected feature table (HDF5 .h5 format with columns: m/z, drift_time, retention_time, intensity)
- Monoisotopic m/z values for each feature
- Charge state specification (z=+1 for singly-charged ions)

## Outputs

- Annotated feature table with isotope group identifiers assigned to each feature
- Isotopic cluster membership records (monoisotope + isotopologues grouped by isotope ID)
- Filtered feature set containing only isotopic signatures with ≥3 members

## How to apply

For each detected feature with known monoisotopic m/z, calculate expected m/z values for up to 5 carbon-13 substitutions by incrementing m/z by 1.003355 Da per isotopic substitution (the mass difference between C13 and C12 in singly-charged form). Search the feature list for peaks matching each calculated m/z within a specified m/z tolerance window (typically constrained by expected delta and refined by maximum m/z error of 50 ppm). Group matching peaks as isotopic clusters and filter to retain only signatures with at least 3 members (monoisotope plus ≥2 isotopologues) to reduce spurious assignments. The rationale is that monoisotopic and isotopic variants co-localize in drift time and retention time, so multi-dimensional filtering improves confidence in isotopic group membership.

## Related tools

- **DEIMoS** (Python API and command-line tool that implements isotope detection by m/z offset enumeration; provides deimos.load() and deimos.save() functions for feature table I/O and isotope group assignment.) — https://github.com/pnnl/deimos
- **Python** (Runtime environment for DEIMoS; enables vector operations on m/z arrays and isotope cluster enumeration.)
- **numpy** (Numerical library used within DEIMoS for efficient array operations on m/z deltas and isotopic mass calculations.)
- **ProteoWizard msconvert** (Converts raw mass spectrometry data from vendor formats to mzML, which can then be loaded into DEIMoS for isotope detection.)

## Examples

```
ms1 = deimos.load('example_data_peaks.h5', key='ms1', columns=['mz', 'drift_time', 'retention_time', 'intensity']); isotopes = deimos.isotopes(ms1, mz_delta=1.003355, max_charge=1, max_isotopes=5, isotope_filter=3); deimos.save(isotopes, 'isotopes_annotated.h5', key='ms1')
```

## Evaluation signals

- Isotopic clusters contain exactly the expected monoisotopic m/z and calculated isotopic m/z values within 50 ppm mass error tolerance.
- All retained isotopic signatures have ≥3 members; no clusters with <3 members remain in the output.
- Monoisotope and all assigned isotopologues co-localize in drift time (no drift time outliers) and retention time within specified tolerances.
- Output feature table schema includes isotope group identifier column and all input features are accounted for (either assigned to a cluster or marked as non-clustered).
- R² of predicted vs. observed m/z for isotopic members is ≥0.9999 (per DEIMoS validation), indicating no systematic m/z calibration drift across isotopic series.

## Limitations

- The skill assumes charge state z=+1; it will fail or produce incorrect results for multiply-charged ions, which have different m/z deltas (e.g., 0.5015 Da per carbon for z=+2).
- Isotope detection relies on sufficient intensity and signal-to-noise ratio for isotopologues; very low-abundance minor isotopes may not be detected even if present.
- The fixed m/z delta of 1.003355 Da assumes natural isotope abundance patterns; heavily labeled or synthetic isotope-enriched samples may not follow the assumed distribution.
- Multi-dimensional filtering (m/z, drift time, retention time) can fail if features are highly congested or if co-eluting isobars occupy the same m/z, drift time, and retention time space.
- The minimum cluster size threshold (≥3 members) is heuristic; small molecules or unusual isotopic patterns with <3 expected isotopologues may be excluded.

## Evidence

- [other] DEIMoS detects C13 isotopologues by specifying an m/z delta of 1.003355 Da, a maximum of 5 isotopic substitutions, and maximum charge of 1, with initial constraint by m/z tolerance from expected delta, followed by drift time and retention time tolerances, and final downselection by maximum m/z error of 50 ppm.: "DEIMoS detects C13 isotopologues by specifying an m/z delta of 1.003355 Da, a maximum of 5 isotopic substitutions, and maximum charge of 1"
- [other] For each feature, calculate expected m/z values for C13 isotopologues (monoisotope + 1.003355 Da per carbon, assuming singly charged z=+1): "For each feature, calculate expected m/z values for C13 isotopologues (monoisotope + 1.003355 Da per carbon, assuming singly charged z=+1)"
- [other] Filter isotopic signatures to retain only those with at least 3 members (monoisotope plus ≥2 isotopologues): "Filter isotopic signatures to retain only those with at least 3 members (monoisotope plus ≥2 isotopologues)"
- [results] A good first screening is to only consider those isotopic signatures with at least 3 members: "A good first screening is to only consider those isotopic signatures with at least 3 members"
- [readme] Functionality includes feature detection, feature alignment, collision cross section (CCS) calibration, isotope detection, and MS/MS spectral deconvolution: "Functionality includes feature detection, feature alignment, collision cross section (CCS) calibration, isotope detection, and MS/MS spectral deconvolution"
