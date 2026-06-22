---
name: charge-state-specific-peak-matching
description: Use when you have peak-picked features with m/z, drift_time, retention_time, and intensity columns, and you need to identify monoisotopic peaks and their charge-state-specific isotopologue members (e.g., singly charged C13-substituted species).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3643
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - DEIMoS
  - ProteoWizard msconvert
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
---

# charge-state-specific-peak-matching

## Summary

Detect and match isotopologue patterns within a single charge state by enumerating mass offsets (e.g., C13 substitutions) and applying multi-dimensional tolerances on m/z, drift time, and retention time. This skill ensures that isotopic signatures are correctly attributed to their charge state, improving feature annotation accuracy in high-dimensional mass spectrometry workflows.

## When to use

Apply this skill when you have peak-picked features with m/z, drift_time, retention_time, and intensity columns, and you need to identify monoisotopic peaks and their charge-state-specific isotopologue members (e.g., singly charged C13-substituted species). Use this skill especially when analyzing datasets where isotopic fine structure must be resolved within defined charge states to avoid cross-charge-state artifact matching.

## When NOT to use

- Input is already a fully annotated feature table with isotope assignments — re-running charge-state-specific matching would risk double-annotation.
- Charge state is unknown or highly variable across the feature set — use untargeted isotope detection without charge state constraint first.
- Mass tolerance window (m/z tolerance, drift_time tolerance, retention_time tolerance) is not compatible with instrument resolution or calibration — validate instrument parameters before applying fixed tolerances.

## Inputs

- peak-picked feature table (HDF5 format) with columns: m/z, drift_time, retention_time, intensity
- charge state specification (integer, e.g., +1 for singly charged species)
- isotope mass offset delta (e.g., 1.003355 Da for C13)
- maximum number of isotopic substitutions (e.g., 5 for C13)

## Outputs

- annotated feature table (HDF5 format) with added columns: isotopologue_label, monoisotopic_designation, isotope_count, offset_mass
- filtered isotopic signature set (membership ≥ 3 members per signature)
- charge-state-specific isotope match statistics (e.g., m/z error per match)

## How to apply

Load peak-picked feature data from HDF5 using deimos.load() with explicit columns for m/z, drift_time, retention_time, and intensity. Call deimos.isotopes() to enumerate isotopologue patterns for a specified charge state (e.g., +1), which computes mass offsets (e.g., m/z delta of 1.003355 Da per C13 substitution, up to 5 substitutions) and applies m/z tolerance, drift_time tolerance, and retention_time tolerance constraints to narrow the search space. Filter detected isotopic signatures to retain only those with at least 3 members (a standard screening threshold to reject spurious single or double peaks). Validate the match by verifying that the maximum m/z error between observed and expected offset masses does not exceed 50 ppm. Annotate the feature table with isotopologue labels (monoisotopic designation, isotope count, offset mass) and export the augmented table as HDF5 with isotope metadata columns for downstream analysis.

## Related tools

- **DEIMoS** (Python API and CLI for multi-dimensional MS data analysis; provides deimos.isotopes() for charge-state-specific isotope detection and deimos.load()/deimos.threshold() for data input and filtering) — http://github.com/pnnl/deimos
- **Python** (Programming language in which DEIMoS is implemented and invoked for isotope detection workflows)
- **ProteoWizard msconvert** (Format conversion utility for converting raw MS data to mzML prior to loading into DEIMoS)

## Examples

```
ms1_peaks = deimos.load('example_data_peaks.h5', key='ms1', columns=['mz', 'drift_time', 'retention_time', 'intensity']); iso_peaks = deimos.isotopes(ms1_peaks, charge=1); iso_filtered = iso_peaks[iso_peaks.groupby('isotope_id').transform('size') >= 3].copy()
```

## Evaluation signals

- All detected isotopic signatures have at least 3 members; signatures with fewer members are filtered out.
- Maximum m/z error across all isotopologue matches is ≤ 50 ppm (downselection threshold).
- Monoisotopic peak and isotope count are correctly labeled and stored in output metadata columns.
- Drift time and retention time offsets between monoisotopic and isotopologue members are within the specified tolerances (not reported in detail in the article, but implicitly validated during isotope detection).
- Output HDF5 table preserves all original columns (m/z, drift_time, retention_time, intensity) and adds new isotope annotation columns without duplication or data loss.

## Limitations

- Isotope detection is specific to a single charge state per run; multi-charge-state analysis requires running the skill separately for each charge state and merging results carefully to avoid conflicts.
- The fixed m/z offset delta (1.003355 Da for C13) and up to 5 isotopic substitutions assume a limited chemical space; non-standard isotopes or highly modified molecules may not be detected.
- Membership threshold (≥ 3 members) is a heuristic screening criterion and may exclude legitimate but weak isotopic patterns in low-abundance features.
- The 50 ppm m/z error cutoff is a post-hoc downselection step and depends on instrument calibration; miscalibrated data may yield false negatives.

## Evidence

- [other] DEIMoS isotope detection enumerates C13 isotopologue offsets by specifying an m/z delta of 1.003355 Da with up to 5 isotopic substitutions for singly charged species: "DEIMoS isotope detection enumerates C13 isotopologue offsets by specifying an m/z delta of 1.003355 Da with up to 5 isotopic substitutions for singly charged species"
- [other] using m/z tolerance, drift time tolerance, and retention time tolerance to constrain the search before applying a maximum m/z error of 50 ppm for final downselection: "using m/z tolerance, drift time tolerance, and retention time tolerance to constrain the search before applying a maximum m/z error of 50 ppm for final downselection"
- [other] Load peak-picked feature table from HDF5 file using deimos.load() with columns for m/z, drift_time, retention_time, and intensity: "Load peak-picked feature table from HDF5 file using deimos.load() with columns for m/z, drift_time, retention_time, and intensity"
- [other] Filter detected isotopic signatures to retain only those with at least 3 members using a membership threshold criterion: "Filter detected isotopic signatures to retain only those with at least 3 members using a membership threshold criterion"
- [other] Annotate the feature table with isotopologue labels (monoisotopic designation, isotope count, offset mass) and export as HDF5 with isotope metadata columns: "Annotate the feature table with isotopologue labels (monoisotopic designation, isotope count, offset mass) and export as HDF5 with isotope metadata columns"
- [readme] Functionality includes feature detection, feature alignment, collision cross section (CCS) calibration, isotope detection, and MS/MS spectral deconvolution: "Functionality includes feature detection, feature alignment, collision cross section (CCS) calibration, isotope detection, and MS/MS spectral deconvolution"
- [other] A good first screening is to only consider those isotopic signatures with at least 3 members: "A good first screening is to only consider those isotopic signatures with at least 3 members"
