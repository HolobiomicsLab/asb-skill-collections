---
name: m-z-tolerance-window-matching
description: Use when when you have detected features with m/z, drift time, and retention time dimensions and need to associate peaks into isotopic groups (e.g., monoisotopes with C13 substitutions) or align features across multiple LC-IMS-MS/MS samples.
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
---

# m/z-tolerance-window-matching

## Summary

Identifies matching peaks within a specified m/z tolerance window to form isotopic clusters or align features across datasets. This skill is essential for grouping chemically related ions (e.g., isotopologues) and improving feature matching confidence in N-dimensional mass spectrometry workflows.

## When to use

When you have detected features with m/z, drift time, and retention time dimensions and need to associate peaks into isotopic groups (e.g., monoisotopes with C13 substitutions) or align features across multiple LC-IMS-MS/MS samples. Specifically use this skill when the input is a feature table with m/z values and you want to resolve isotopic fine structure or cross-sample correspondence within a defined m/z accuracy budget (e.g., ±50 ppm or instrument-specific tolerance).

## When NOT to use

- Input is a raw mass spectrum (centroided or profile mode) rather than an aligned feature table; use feature detection first.
- m/z tolerance window is not defined or is unrealistic for the instrument (e.g., >500 ppm for high-resolution MS); calibration or validation is required.
- Peak intensity or signal-to-noise ratios are insufficient to distinguish true isotopologues from noise; apply intensity filtering upstream.

## Inputs

- Feature table (HDF5 or mzML format) with columns: m/z, drift_time, retention_time, intensity
- Expected m/z delta(s) for isotopologues or aligned features (e.g., 1.003355 Da for C13)
- m/z tolerance window (ppm or Da units)
- Charge state (z) or range of charge states
- Maximum number of isotopic substitutions (if applicable)

## Outputs

- Annotated feature table with isotopic group identifiers or cluster membership
- Isotopic signature clusters (monoisotope + ≥2 isotopologues meeting filtering criteria)
- Feature groups filtered by m/z, drift time, and retention time tolerances

## How to apply

For each feature in the input table, calculate the expected m/z values for candidate isotopologues or aligned features based on the mass delta (e.g., 1.003355 Da per C13 substitution for singly charged ions). Search the feature list for peaks within the specified m/z tolerance window around each expected m/z; the tolerance is typically initialized by expected delta and refined by instrument calibration or mass accuracy (e.g., 50 ppm error threshold). Group matching peaks by m/z proximity, then apply secondary filters on drift time and retention time dimensions to increase confidence. Retain only clusters that meet a minimum membership criterion (e.g., ≥3 members: monoisotope plus ≥2 isotopologues) to reduce false positives. Assign cluster or group identifiers and export the annotated feature table with membership annotations.

## Related tools

- **DEIMoS** (Python API and CLI tool for executing isotope detection and feature matching workflows; encapsulates m/z tolerance windowing and clustering logic within deimos.load() and deimos.save() I/O and filtering functions) — https://github.com/pnnl/deimos
- **numpy** (Numerical array operations for vectorized m/z delta calculations and tolerance comparisons across features)
- **ProteoWizard msconvert** (Format conversion utility to prepare raw mass spectrometry data (e.g., vendor formats) into mzML for subsequent feature detection and m/z matching workflows)

## Examples

```
ms1 = deimos.load('example_data_peaks.h5', key='ms1', columns=['mz', 'drift_time', 'retention_time', 'intensity']); isotopes = deimos.isotopes(ms1, mz_delta=1.003355, max_charge=1, mz_tol=0.01, dt_tol=3.0, rt_tol=0.5); isotopes_filtered = isotopes[isotopes.groupby('isotope_id').size() >= 3]; deimos.save(isotopes_filtered, 'isotopes_annotated.h5')
```

## Evaluation signals

- All features in output isotopic clusters satisfy the m/z tolerance criterion (observed m/z within tolerance window of expected m/z for stated charge and isotopic substitution count).
- Cluster membership includes monoisotope plus ≥2 additional members; no singleton or 2-member clusters remain after filtering (threshold of 3 enforced).
- Intensity ratios of isotopologues within clusters follow expected natural abundance patterns for the detected element (e.g., C13 ~1.1% natural abundance).
- Secondary drift time and retention time filters are applied consistently; no clusters with drift time or retention time outliers remain.
- Maximum m/z error across all matched features is ≤50 ppm (or stated instrument accuracy threshold).

## Limitations

- Requires accurate m/z calibration; systematic offsets larger than the tolerance window will cause misses or false matches.
- Performance degrades in high-complexity samples where many features occupy overlapping m/z ranges; feature detection resolution and m/z accuracy directly impact grouping success.
- No intrinsic handling of multiply-charged species without explicit charge state specification; user must define or enumerate expected charge states.
- Isotopic pattern inference relies on natural abundance assumptions; non-natural or enriched isotope ratios will violate intensity ratio expectations and may be filtered incorrectly.
- Algorithm is agnostic to instrument type, but m/z tolerance window must be tuned per instrument and acquisition mode (e.g., Orbitrap vs. TOF resolution).

## Evidence

- [other] For each feature, calculate expected m/z values for C13 isotopologues (monoisotope + 1.003355 Da per carbon, assuming singly charged z=+1): "For each feature, calculate expected m/z values for C13 isotopologues (monoisotope + 1.003355 Da per carbon, assuming singly charged z=+1)."
- [other] Search within a specified m/z tolerance window for matching peaks in the feature list to form isotopic clusters.: "Search within a specified m/z tolerance window for matching peaks in the feature list to form isotopic clusters."
- [other] Filter isotopic signatures to retain only those with at least 3 members (monoisotope plus ≥2 isotopologues).: "Filter isotopic signatures to retain only those with at least 3 members (monoisotope plus ≥2 isotopologues)."
- [readme] algorithm implementations simultaneously utilize all dimensions to (ii) increase alignment/feature matching confidence among datasets: "algorithm implementations simultaneously utilize all dimensions to (ii) increase alignment/feature matching confidence among datasets"
- [results] A good first screening is to only consider those isotopic signatures with at least 3 members: "A good first screening is to only consider those isotopic signatures with at least 3 members"
- [other] DEIMoS detects C13 isotopologues by specifying an m/z delta of 1.003355 Da, a maximum of 5 isotopic substitutions, and maximum charge of 1, with initial constraint by m/z tolerance from expected delta, followed by drift time and retention time tolerances, and final downselection by maximum m/z error of 50 ppm.: "DEIMoS detects C13 isotopologues by specifying an m/z delta of 1.003355 Da, a maximum of 5 isotopic substitutions, and maximum charge of 1, with initial constraint by m/z tolerance from expected"
