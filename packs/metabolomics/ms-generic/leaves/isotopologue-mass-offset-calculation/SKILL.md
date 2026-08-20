---
name: isotopologue-mass-offset-calculation
description: Use when you have a peak-picked feature table (HDF5 format with m/z, drift_time, retention_time, intensity columns) and need to identify and label isotopic signatures within singly charged species.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0157
  tools:
  - Python
  - DEIMoS
  - ProteoWizard msconvert
  techniques:
  - mass-spectrometry
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

# Isotopologue Mass Offset Calculation

## Summary

Detect and enumerate C13 isotopologue patterns in multidimensional mass spectrometry data by computing mass deltas between monoisotopic and isotopically substituted peaks, constrained by m/z, drift time, and retention time tolerances. This skill enables annotation of feature tables with isotope membership, count, and offset mass for improved metabolite characterization.

## When to use

Apply this skill when you have a peak-picked feature table (HDF5 format with m/z, drift_time, retention_time, intensity columns) and need to identify and label isotopic signatures within singly charged species. Use it to enrich feature annotations for downstream metabolite identification or to filter out isotopically redundant features before alignment or statistical analysis.

## When NOT to use

- Input is already a fully annotated metabolite table with isotope identities resolved — further enumeration would be redundant.
- Data originates from instruments with poor mass accuracy (>50 ppm m/z error) or low temporal resolution (drift time or retention time not reliably measured) — isotope detection will fail to constrain search space adequately.
- Analysis targets multiply charged species (z > 1) without adjusting m/z delta calculation for charge state — the 1.003355 Da offset applies only to singly charged ions.

## Inputs

- Peak-picked feature table in HDF5 format with columns: m/z, drift_time, retention_time, intensity
- Charge state specification (default +1 for singly charged species)
- Tolerance parameters: m/z tolerance, drift_time tolerance, retention_time tolerance

## Outputs

- Isotope-annotated feature table (HDF5 format) with added columns: monoisotopic label, isotope count, offset mass
- List of detected isotopic signatures with ≥3 member peaks

## How to apply

Load the peak-picked feature table into memory using deimos.load() specifying the required columns (m/z, drift_time, retention_time, intensity). Apply deimos.isotopes to enumerate C13 substitutions by specifying an m/z delta of 1.003355 Da (the monoisotopic mass difference), allowing up to 5 isotopic substitutions for charge state +1 species. The algorithm constrains the search using m/z tolerance, drift time tolerance, and retention time tolerance parameters, then applies a maximum m/z error of 50 ppm for final downselection of isotopic peaks. Filter the detected isotopic signatures to retain only those with at least 3 member peaks using a membership threshold criterion, to eliminate spurious isotope assignments. Annotate the feature table with isotope metadata columns (monoisotopic designation, isotope count, offset mass) and export the enriched table as HDF5.

## Related tools

- **DEIMoS** (Core Python API and CLI tool for isotope detection via deimos.isotopes(); loads and exports HDF5 feature tables) — http://github.com/pnnl/deimos
- **Python** (Runtime environment for deimos library and data manipulation)
- **ProteoWizard msconvert** (Optional upstream format conversion tool to standardize raw MS data to mzML before DEIMoS processing)

## Examples

```
ms1_peaks = deimos.load('example_data_peaks.h5', key='ms1', columns=['mz', 'drift_time', 'retention_time', 'intensity']); isotopes = deimos.isotopes(ms1_peaks, mz_tol=0.01, dt_tol=2, rt_tol=0.5); isotopes_filtered = isotopes[isotopes['isotope_count'] >= 2]
```

## Evaluation signals

- Isotope-annotated feature table contains no null values in isotope metadata columns (monoisotopic designation, isotope count, offset mass) for assigned peaks.
- All isotopic signatures retained in final output contain ≥3 member peaks; no spurious single or doublet isotope clusters remain.
- Monoisotopic peak mass + computed offset (isotope_count × 1.003355 Da) equals observed m/z of each isotopic member peak within stated 50 ppm m/z error threshold.
- Drift time and retention time differences between monoisotopic and isotopic member peaks remain within user-specified tolerance bounds (confirming they co-elute and are true isotopic pairs, not background noise).
- Downstream feature alignment or metabolite matching shows improved specificity (reduced false positive matches) when isotopically redundant features are filtered using the isotope count annotation.

## Limitations

- Isotope detection is constrained to singly charged species (z = +1); multiply charged ions require separate handling with charge-state-adjusted m/z deltas.
- The 1.003355 Da offset enumeration assumes C13 substitution only; other isotopes (N15, S34, O18) are not detected by this workflow without separate parameter specification.
- Search space filtering depends critically on accurate m/z, drift_time, and retention_time measurements; instruments with poor mass accuracy (>50 ppm) or weak multidimensional resolution will yield high false negative rates for isotope detection.
- The 3-member minimum threshold is heuristic and may filter true but low-intensity isotopic signatures in low-abundance metabolites; users must balance sensitivity against specificity for their study design.
- No changelog documented for version tracking and parameter evolution across DEIMoS releases.

## Evidence

- [other] DEIMoS isotope detection enumerates C13 isotopologue offsets by specifying an m/z delta of 1.003355 Da with up to 5 isotopic substitutions for singly charged species, using m/z tolerance, drift time tolerance, and retention time tolerance to constrain the search before applying a maximum m/z error of 50 ppm for final downselection.: "DEIMoS isotope detection enumerates C13 isotopologue offsets by specifying an m/z delta of 1.003355 Da with up to 5 isotopic substitutions for singly charged species, using m/z tolerance, drift time"
- [other] Load peak-picked feature table from HDF5 file using deimos.load() with columns for m/z, drift_time, retention_time, and intensity.: "Load peak-picked feature table from HDF5 file using deimos.load() with columns for m/z, drift_time, retention_time, and intensity."
- [other] Filter detected isotopic signatures to retain only those with at least 3 members using a membership threshold criterion.: "Filter detected isotopic signatures to retain only those with at least 3 members using a membership threshold criterion."
- [results] A good first screening is to only consider those isotopic signatures with at least 3 members.: "A good first screening is to only consider those isotopic signatures with at least 3 members."
- [readme] algorithm implementations simultaneously utilize all dimensions to (i) offer greater separation between features, thus improving detection sensitivity, (ii) increase alignment/feature matching confidence among datasets: "algorithm implementations simultaneously utilize all dimensions to (i) offer greater separation between features, thus improving detection sensitivity, (ii) increase alignment/feature matching"
