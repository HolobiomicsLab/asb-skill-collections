---
name: multidimensional-feature-annotation
description: Use when you have a peak-picked feature table (HDF5 format) from high-dimensional
  MS data (m/z, drift_time, retention_time, intensity) and need to identify and label
  isotopic signatures to distinguish monoisotopic peaks from isotopologues, reduce
  feature redundancy, and support multi-dimensional.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3648
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - deimos
  - HDF5
  techniques:
  - LC-MS
  - ion-mobility-MS
  license_tier: open
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Multidimensional Feature Annotation

## Summary

Annotate detected mass spectrometry features with isotopologue labels and membership metadata by identifying C13 isotopic substitution patterns across m/z, drift time, and retention time dimensions. This enriches feature tables with monoisotopic designation, isotope count, and offset mass information for downstream filtering and interpretation.

## When to use

Apply this skill when you have a peak-picked feature table (HDF5 format) from high-dimensional MS data (m/z, drift_time, retention_time, intensity) and need to identify and label isotopic signatures to distinguish monoisotopic peaks from isotopologues, reduce feature redundancy, and support multi-dimensional alignment confidence.

## When NOT to use

- Input is already a deconvoluted or charge-state-assigned feature table; isotope detection assumes raw peak-picked data.
- Analysis targets multiply-charged species (z > 1) without explicit charge-state constraints; DEIMoS isotope detection parameters are optimized for singly charged ions.
- Retention time or drift time dimensions are missing or unreliable; multi-dimensional tolerance constraints require all three dimensions for robust matching.

## Inputs

- Peak-picked feature table in HDF5 format with columns: m/z, drift_time, retention_time, intensity
- Charge state constraints (e.g., +1 for singly charged species)

## Outputs

- Annotated feature table (HDF5) with added columns: isotopologue label, monoisotopic designation, isotope count, offset mass
- Filtered isotopic signature membership (≥3 members per signature)

## How to apply

Load the peak-picked feature table from HDF5 using deimos.load() with explicit columns for m/z, drift_time, retention_time, and intensity. Apply deimos.isotopes() to enumerate C13 isotopologue patterns by computing mass offsets (1.003355 Da per substitution, up to 5 substitutions for singly charged species) and constraining matches within m/z tolerance, drift time tolerance, and retention time tolerance before applying a maximum m/z error of 50 ppm for final downselection. Filter detected isotopic signatures to retain only those with at least 3 members using a membership threshold criterion to reduce false positives. Annotate the feature table with new columns encoding the monoisotopic designation, isotope count (0 = monoisotopic, 1+ = isotopologue member), and offset mass, then export the enriched table as HDF5 with isotope metadata columns preserved for subsequent analysis.

## Related tools

- **deimos** (Python API and command-line tool for isotope detection and feature annotation via deimos.isotopes() and deimos.load()) — http://github.com/pnnl/deimos
- **Python** (Scripting language for loading, filtering, and annotating feature tables)
- **HDF5** (Data format for storing and retrieving peak-picked features and annotated results)

## Examples

```
ms1_peaks = deimos.load('example_data_peaks.h5', key='ms1', columns=['mz', 'drift_time', 'retention_time', 'intensity']); ms1_peaks = deimos.isotopes(ms1_peaks); ms1_peaks = ms1_peaks[ms1_peaks['isotope_count'] >= 0]; ms1_peaks.to_hdf5('annotated_features.h5', key='ms1')
```

## Evaluation signals

- All detected isotopic signatures have ≥ 3 member peaks; no signatures with 1–2 members remain in the output.
- Monoisotopic designation is consistent: exactly one peak per isotopic signature is labeled as monoisotopic (isotope count = 0); all others have isotope count ≥ 1.
- Mass offsets match expected C13 substitution pattern: each member peak differs from monoisotopic by n × 1.003355 Da (n = isotope count) within 50 ppm m/z error.
- Annotated feature table retains all original columns (m/z, drift_time, retention_time, intensity) plus new isotope metadata columns without data loss.
- Feature count increases or remains stable after annotation (no false positive isotope linkages should cause loss of valid monoisotopic peaks).

## Limitations

- Isotope detection is optimized for singly charged species (z = +1); extension to multiply-charged ions requires explicit charge-state constraints and mass offset recalculation.
- Detection sensitivity depends on intensity threshold applied before isotope detection; weak isotopologue members may be missed if below the threshold (e.g., threshold=1000 is more stringent than threshold=100).
- M/z tolerance (50 ppm maximum), drift time tolerance, and retention time tolerance must be tuned for the specific mass spectrometry platform and acquisition method; mismatch will cause false negatives (missed isotopologues) or false positives (erroneous linkages).
- Multi-dimensional approach assumes drift time and retention time are reliable and well-calibrated; poor drift time resolution or time-alignment artifacts will degrade isotope pattern coherence.

## Evidence

- [other] DEIMoS isotope detection enumerates C13 isotopologue offsets by specifying an m/z delta of 1.003355 Da with up to 5 isotopic substitutions for singly charged species, using m/z tolerance, drift time tolerance, and retention time tolerance to constrain the search before applying a maximum m/z error of 50 ppm for final downselection.: "DEIMoS isotope detection enumerates C13 isotopologue offsets by specifying an m/z delta of 1.003355 Da with up to 5 isotopic substitutions for singly charged species, using m/z tolerance, drift time"
- [other] Load peak-picked feature table from HDF5 file using deimos.load() with columns for m/z, drift_time, retention_time, and intensity. Apply deimos.isotopes to detect C13 isotopologue patterns, computing mass offsets between monoisotopic and isotopically substituted peaks for charge state +1.: "Load peak-picked feature table from HDF5 file using deimos.load() with columns for m/z, drift_time, retention_time, and intensity. Apply deimos.isotopes to detect C13 isotopologue patterns, computing"
- [other] Filter detected isotopic signatures to retain only those with at least 3 members using a membership threshold criterion.: "Filter detected isotopic signatures to retain only those with at least 3 members using a membership threshold criterion."
- [other] Annotate the feature table with isotopologue labels (monoisotopic designation, isotope count, offset mass) and export as HDF5 with isotope metadata columns.: "Annotate the feature table with isotopologue labels (monoisotopic designation, isotope count, offset mass) and export as HDF5 with isotope metadata columns."
- [readme] Functionality includes feature detection, feature alignment, collision cross section (CCS) calibration, isotope detection, and MS/MS spectral deconvolution: "Functionality includes feature detection, feature alignment, collision cross section (CCS) calibration, isotope detection, and MS/MS spectral deconvolution"
