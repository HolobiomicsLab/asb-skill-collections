---
name: peak-property-dictionary-construction
description: Use when when you have identified the set of analytes (peptides, nucleosides, or other biomolecules) you wish to simulate in silico, and you need to prepare their chemical properties (m/z, intensity, retention time) in a machine-readable format before applying fragmentation and noise injection.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - SMITER
  - pyQms
derived_from:
- doi: 10.3390/genes12030396
  title: SMITER
evidence_spans:
- SMITER (Synthetic mzML writer) is a python-based command-line tool designed to simulate LC-MS/MS runs.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_smiter_cq
    doi: 10.3390/genes12030396
    title: SMITER
  dedup_kept_from: coll_smiter_cq
schema_version: 0.2.0
---

# peak-property-dictionary-construction

## Summary

Construct or load a peak-property dictionary containing mass, intensity, and retention-time information for analytes as the foundational input to SMITER's synthetic mzML generation pipeline. This step abstracts chemical formulas and molecular properties into a structured format that enables downstream fragmentation and noise modeling.

## When to use

When you have identified the set of analytes (peptides, nucleosides, or other biomolecules) you wish to simulate in silico, and you need to prepare their chemical properties (m/z, intensity, retention time) in a machine-readable format before applying fragmentation and noise injection models to generate synthetic LC-MS/MS data.

## When NOT to use

- If you already have a pre-built peak-properties dictionary and are skipping directly to fragmentor/noise-model instantiation.
- If your input consists of raw mass spectrometry files (mzML, mzXML, NetCDF) rather than analyte property tables; use a file parser instead.
- If you do not have a priori knowledge of the analytes you wish to simulate; use a spectral library or database query first.

## Inputs

- CSV file with columns for analyte identifiers, chemical formulas, m/z values, intensities, and retention times
- Python dict or JSON object with analyte properties

## Outputs

- peak_properties dictionary (Python dict) with structure {analyte_id: {'mass': float, 'intensity': float, 'retention_time': float, ...}}

## How to apply

Begin by assembling analyte metadata in tabular form (e.g., CSV with columns for chemical formula, mass, intensity, retention time); alternatively, construct the dictionary programmatically in Python. Use the provided utility smiter.lib.csv_to_peak_properties to convert CSV input to the required peak-properties dictionary structure, or build it directly by instantiating a Python dict keyed by analyte identifiers and valued with nested dicts containing 'mass', 'intensity', and 'retention_time' fields. Validate that all numeric fields are present and that mass values are consistent with the intended chemical formulas. This structured dictionary then serves as the primary input to smiter.synthetic_mzml.write_mzml in step 5 of the simulation workflow.

## Related tools

- **SMITER** (Accepts peak-properties dictionary as input to the write_mzml function for synthetic mzML generation; provides csv_to_peak_properties utility for format conversion) — https://github.com/LeidelLab/SMITER
- **pyQms** (Enables highly-accurate isotopic pattern calculation based on chemical formulas, supporting mass derivation within peak properties) — https://github.com/pyQms/pyqms

## Examples

```
peak_properties = smiter.lib.csv_to_peak_properties('analytes.csv'); # or manually: peak_properties = {'pep1': {'mass': 1234.567, 'intensity': 1e6, 'retention_time': 15.3}, 'pep2': {'mass': 2345.789, 'intensity': 5e5, 'retention_time': 22.1}}
```

## Evaluation signals

- Peak-properties dictionary is valid Python dict with all required analytes present and no missing 'mass', 'intensity', or 'retention_time' fields.
- All mass values are positive floats and consistent with expected chemical formulas (e.g., within expected range for target analyte class).
- Intensity values span a reasonable range for the experimental context (e.g., not all identical, no negative values).
- Retention times are monotonically increasing or clustered as expected for the simulated LC gradient.
- CSV input, if used, converts without errors via smiter.lib.csv_to_peak_properties and produces valid dictionary structure.

## Limitations

- Peak-properties dictionary construction is agnostic to downstream fragmentation and noise model compatibility; validation of consistency between molecular formula and mass values must be performed by the user.
- Retention time prediction is not built into peak-properties construction; empirical RT values or an external RT prediction module must be provided by the user.
- The utility smiter.lib.csv_to_peak_properties expects a specific CSV schema; malformed or inconsistent column names will cause conversion failure.
- No changelog provided in the repository documentation, so breaking changes to the peak-properties schema across versions are not explicitly documented.

## Evidence

- [other] 1. Load or construct a peak properties dictionary containing mass, intensity, and retention-time information for analytes (optionally converting from CSV using smiter.lib.csv_to_peak_properties).: "Load or construct a peak properties dictionary containing mass, intensity, and retention-time information for analytes"
- [other] create the peak properties dict (You can convert a csv file (as in example_data) to csv using `smiter.lib.csv_to_peak_properties`): "create the peak properties dict (You can convert a csv file (as in example_data) to csv using `smiter.lib.csv_to_peak_properties`)"
- [readme] It enables the simulation of any biomolecule since all calculations are based on the chemical formulas.: "It enables the simulation of any biomolecule since all calculations are based on the chemical formulas."
- [readme] usage of highly-accurate isotopic patterns enabled by `pyQms`: "usage of highly-accurate isotopic patterns enabled by `pyQms`"
