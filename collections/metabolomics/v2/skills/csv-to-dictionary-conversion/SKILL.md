---
name: csv-to-dictionary-conversion
description: Use when you have a CSV file containing molecule definitions (chemical formula, m/z, intensity, retention time, or other peak properties) and need to prepare it for SMITER's simulation workflow.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3750
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3370
  tools:
  - SMITER
  - Python
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3390/genes12030396
  all_source_dois:
  - 10.3390/genes12030396
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# csv-to-dictionary-conversion

## Summary

Convert a CSV file of molecule definitions into a peak properties dictionary structure required by SMITER's LC-MS/MS simulation pipeline. This transformation bridges tabular input data to the nested dictionary format consumed by fragmentors, noise generators, and mzML writers.

## When to use

You have a CSV file containing molecule definitions (chemical formula, m/z, intensity, retention time, or other peak properties) and need to prepare it for SMITER's simulation workflow. This skill is required as the first step before choosing a fragmentor, noise generator, and running the synthetic mzML generation.

## When NOT to use

- The input is already in peak properties dictionary format (no conversion needed)
- The CSV file lacks required columns such as chemical formula or m/z (conversion will fail or produce incomplete output)
- You are simulating molecules using only SMITER's default parameters without custom peak definitions

## Inputs

- CSV file containing molecule definitions (from example_data or user-generated)
- CSV schema with columns for chemical formula, m/z, intensity, retention time, or equivalent peak properties

## Outputs

- Peak properties dictionary (Python dict) with required nested structure
- Pickled or JSON serialization of the peak properties dictionary for use in simulation

## How to apply

Use SMITER's `smiter.lib.csv_to_peak_properties` function to convert the tabular CSV data into a nested peak properties dictionary. Load the CSV file using standard Python file I/O, apply the conversion function, and validate that the resulting dictionary contains the required keys (e.g., molecule identifiers, chemical formulas, peak properties) expected by SMITER's fragmentation and noise injection functions. Serialize the validated dictionary to pickle or JSON format for consumption by downstream simulation steps (fragmentor selection, noise injection, and mzML synthesis).

## Related tools

- **SMITER** (Provides the csv_to_peak_properties conversion function within smiter.lib; orchestrates the complete LC-MS/MS simulation pipeline after dictionary creation) — https://github.com/LeidelLab/SMITER
- **Python** (Runtime environment for executing SMITER library functions and file I/O operations)
- **pyQms** (Enables highly-accurate isotopic pattern calculations used in peak property calculations downstream) — https://github.com/pyQms/pyqms

## Examples

```
from smiter.lib import csv_to_peak_properties; peak_dict = csv_to_peak_properties('example_data.csv'); import pickle; pickle.dump(peak_dict, open('peak_properties.pkl', 'wb'))
```

## Evaluation signals

- Dictionary keys match SMITER's expected schema (validate against fragmentation and noise injection function signatures)
- All required molecule properties (chemical formula, m/z, intensity, retention time) are present and non-null in the output dictionary
- Pickle or JSON serialization completes without errors and can be deserialized without data loss
- Dictionary structure passes validation before being passed to fragmentation function (e.g., fragmentation_functions.PeptideFragmentor)
- Molecule counts and property value ranges (e.g., m/z > 0, intensity >= 0) match the input CSV

## Limitations

- CSV schema must match SMITER's expected column names and data types; non-standard formats will cause conversion failure
- Conversion does not validate chemical formula correctness or plausibility; invalid formulas will propagate into the dictionary
- No automatic handling of missing or malformed values in the CSV; preprocessing is required before conversion
- Dictionary size is bounded by available system memory; very large CSV files may cause memory exhaustion

## Evidence

- [other] SMITER provides the csv_to_peak_properties function within its library to convert CSV files containing molecule definitions into the peak properties dictionary format consumed by the simulation workflow.: "You can convert a csv file (as in example_data) to csv using `smiter.lib.csv_to_peak_properties`"
- [other] Peak properties dictionary is the first required step in the SMITER simulation workflow, followed by fragmentor and noise generator selection.: "1. create the peak properties dict (You can convert a csv file (as in example_data) to csv using `smiter.lib.csv_to_peak_properties`)"
- [abstract] SMITER enables simulation of any biomolecule via chemical formula abstraction, which is reflected in the peak properties dictionary structure.: "It enables the simulation of any biomolecule since all calculations are based on the chemical formulas."
- [other] The resulting dictionary must be serialized for use in subsequent simulation steps.: "Serialize the peak properties dictionary to a Python pickle or JSON file for use in subsequent simulation steps."
