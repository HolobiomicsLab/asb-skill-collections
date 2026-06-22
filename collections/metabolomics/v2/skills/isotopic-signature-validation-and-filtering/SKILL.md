---
name: isotopic-signature-validation-and-filtering
description: Use when after isotope detection has enumerated C13 isotopologue patterns across m/z, drift time, and retention time dimensions, and you need to reduce false positives by retaining only well-populated isotopic signature clusters before annotation or export.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - DEIMoS
derived_from:
- doi: 10.1021/acs.analchem.1c05017
  title: deimos
evidence_spans:
- is a Python application programming interface and command-line tool
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_deimos
    doi: 10.1021/acs.analchem.1c05017
    title: deimos
  dedup_kept_from: coll_deimos
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

# isotopic-signature-validation-and-filtering

## Summary

Filter and validate detected isotopologue signatures in multidimensional mass spectrometry feature tables by applying membership thresholds and annotating monoisotopic designations. This ensures only reliable isotopic patterns are retained for downstream analysis.

## When to use

After isotope detection has enumerated C13 isotopologue patterns across m/z, drift time, and retention time dimensions, and you need to reduce false positives by retaining only well-populated isotopic signature clusters before annotation or export. Apply this skill when isotope detection output requires quality control to distinguish signal from noise in complex samples.

## When NOT to use

- Input feature table has not yet undergone isotope detection — run deimos.isotopes() first.
- Isotopic signature clustering is not relevant to your analysis goal (e.g., you need to preserve all peaks for untargeted feature alignment).
- Sample does not contain isotopically enriched standards or natural-abundance C13 patterns (e.g., synthetic labeled compounds with non-standard isotope ratios).

## Inputs

- feature table with isotope detection results (HDF5 or pandas DataFrame with m/z, drift_time, retention_time, intensity, and isotope_group/membership columns)

## Outputs

- validated isotopic signature feature table (HDF5 with isotope metadata: monoisotopic label, isotope count, offset mass)
- filtered feature table containing only isotopic signatures with ≥3 members

## How to apply

Load the feature table output from deimos.isotopes() containing raw isotopic signature assignments. Apply a membership threshold filter to retain only isotopic signatures with at least 3 members (monoisotopic peak plus at least 2 isotopic variants), which is a standard screening criterion to exclude singleton or doublet detections that are likely artifacts. Annotate surviving signatures with isotopologue labels including monoisotopic designation, isotope count, and offset mass relative to the monoisotopic m/z. Export the validated and annotated feature table to HDF5 format with isotope metadata columns preserved for traceability.

## Related tools

- **DEIMoS** (Python API/CLI for isotope detection and multidimensional feature processing; provides deimos.isotopes() for initial isotopologue pattern enumeration and deimos.load()/export for HDF5 I/O) — https://github.com/pnnl/deimos
- **Python** (Runtime and pandas/numpy environment for iterative filtering, annotation, and table manipulation)

## Examples

```
ms1_peaks_filtered = ms1_peaks[ms1_peaks.groupby('isotope_group')['isotope_group'].transform('size') >= 3]; ms1_peaks_filtered = deimos.annotate_isotopes(ms1_peaks_filtered); deimos.dump(ms1_peaks_filtered, 'filtered_isotopes.h5', key='ms1')
```

## Evaluation signals

- Retained isotopic signatures contain exactly ≥3 distinct peaks (monoisotopic + ≥2 isotopic variants) with internally consistent m/z offsets matching C13 mass shift (1.003355 Da per substitution, ±50 ppm tolerance).
- All retained signatures are annotated with non-null monoisotopic label, isotope count, and offset mass columns; no missing or inconsistent metadata.
- Removed signatures (those with <3 members) are absent from final table; no orphaned isotopic variants remain.
- HDF5 export preserves all metadata columns and confirms schema matches input structure plus isotope annotation fields.
- Isotope count values range from 1 (monoisotopic) to ≤5 (observed maximum isotopic substitutions), consistent with enumeration parameters.

## Limitations

- Membership threshold (≥3 members) is empirically recommended but may require tuning for low-abundance features or high-noise acquisitions.
- Filtering is agnostic to charge state; if multi-charge features are present in the same table, apply separate filtering per charge state to avoid cross-charge isotope confusion.
- Does not account for peak intensity patterns or Expected isotope ratios (e.g., Gaussian envelope); membership-only filtering may retain anomalous patterns with unusual abundance ratios.
- Assumes C13 enumeration; does not validate other isotopologue types (e.g., S34, N15) if present in the sample.

## Evidence

- [other] Filter detected isotopic signatures to retain only those with at least 3 members using a membership threshold criterion.: "Filter detected isotopic signatures to retain only those with at least 3 members using a membership threshold criterion."
- [results] A good first screening is to only consider those isotopic signatures with at least 3 members.: "A good first screening is to only consider those isotopic signatures with at least 3 members."
- [other] Annotate the feature table with isotopologue labels (monoisotopic designation, isotope count, offset mass) and export as HDF5 with isotope metadata columns.: "Annotate the feature table with isotopologue labels (monoisotopic designation, isotope count, offset mass) and export as HDF5 with isotope metadata columns."
- [other] DEIMoS isotope detection enumerates C13 isotopologue offsets by specifying an m/z delta of 1.003355 Da with up to 5 isotopic substitutions for singly charged species, using m/z tolerance, drift time tolerance, and retention time tolerance to constrain the search before applying a maximum m/z error of 50 ppm for final downselection.: "m/z delta of 1.003355 Da with up to 5 isotopic substitutions for singly charged species, using m/z tolerance, drift time tolerance, and retention time tolerance to constrain the search before"
- [readme] Functionality includes feature detection, feature alignment, collision cross section (CCS) calibration, isotope detection, and MS/MS spectral deconvolution: "Functionality includes feature detection, feature alignment, collision cross section (CCS) calibration, isotope detection, and MS/MS spectral deconvolution"
