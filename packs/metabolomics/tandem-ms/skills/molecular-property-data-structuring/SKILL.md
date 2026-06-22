---
name: molecular-property-data-structuring
description: Use when you have a CSV file with rows of molecule definitions (chemical formulas, retention times, intensities, or other peak properties) and need to feed them into SMITER's simulation workflow.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - SMITER
  - Python
  techniques:
  - LC-MS
  - tandem-MS
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

# molecular-property-data-structuring

## Summary

Convert tabular CSV files containing molecule definitions into the dictionary data structure required by SMITER's LC-MS/MS simulation pipeline. This skill bridges raw molecular input data and the in-memory format consumed by fragmentation, noise, and mzML generation modules.

## When to use

You have a CSV file with rows of molecule definitions (chemical formulas, retention times, intensities, or other peak properties) and need to feed them into SMITER's simulation workflow. Use this skill as the first step before selecting a fragmentor, noise generator, or running mzML synthesis—the peak properties dictionary is a mandatory input to all downstream simulation functions.

## When NOT to use

- Peak properties dictionary is already in memory or already deserialized from a pickle/JSON file—skip directly to fragmentor selection.
- Input CSV does not contain required columns (e.g., chemical formula, retention time) or has incompatible schema—validate and reformat the CSV first.
- You need to perform custom transformations or filtering on the molecule definitions before structuring—preprocess the CSV independently, then apply this skill.

## Inputs

- CSV file with molecule definitions (path or file object)
- Column specification or schema mapping CSV headers to peak property keys (optional; function may use defaults)

## Outputs

- Python dictionary: peak properties keyed by molecule identifier
- Serialized peak properties dictionary (pickle or JSON file) for downstream simulation steps

## How to apply

Load the CSV file using standard Python file I/O, then apply the smiter.lib.csv_to_peak_properties function to transform the tabular data into a nested dictionary keyed by molecule identifiers and containing peak property values (e.g., m/z, intensity, retention time, chemical formula). Validate the resulting dictionary structure by verifying that all required keys are present and that values conform to expected types and ranges (e.g., m/z > 0, intensity ≥ 0). Serialize the validated dictionary to a Python pickle (.pkl) or JSON file for use in the next workflow step. The function abstracts away the row-to-dict conversion, ensuring the output is compatible with SMITER's modular simulation architecture.

## Related tools

- **SMITER** (Python library providing the csv_to_peak_properties conversion function and downstream simulation pipeline (fragmentors, noise injection, mzML writing)) — https://github.com/LeidelLab/SMITER
- **Python** (Required runtime and language for executing the csv_to_peak_properties function and file I/O)

## Examples

```
from smiter.lib import csv_to_peak_properties; peak_dict = csv_to_peak_properties('example_data.csv'); import pickle; pickle.dump(peak_dict, open('peak_properties.pkl', 'wb'))
```

## Evaluation signals

- Resulting dictionary keys match molecule identifiers from the CSV input and are consistently ordered or hashable.
- All required peak property keys (e.g., chemical_formula, m/z, intensity, retention_time) are present in every dictionary entry; no missing or None values in mandatory fields.
- Numeric values (m/z, intensity, retention_time) are within physically plausible ranges (m/z > 0, intensity ≥ 0, retention_time ≥ 0).
- Serialized pickle or JSON file can be loaded and deserialized back into an identical dictionary without data loss.
- The peak properties dictionary can be passed without error to downstream SMITER functions (e.g., fragmentors, write_mzml) and produces valid mzML output.

## Limitations

- Function assumes CSV input is well-formed and complete; malformed rows or missing required columns will cause conversion failure or silent data loss.
- No built-in support for custom retention-time prediction or isotopic pattern refinement—those require separate modules or post-processing.
- Abstraction to chemical formulas means all calculations lose isotope-specific or conformational information beyond the formula; molecules differing only in 3D structure will be indistinguishable.
- Large CSV files may consume significant memory when converted to an in-memory dictionary; no streaming or chunking mode documented.

## Evidence

- [other] create the peak properties dict (You can convert a csv file (as in example_data) to csv using `smiter.lib.csv_to_peak_properties`): "You can convert a csv file (as in example_data) to csv using `smiter.lib.csv_to_peak_properties`"
- [other] 1. Load the CSV file containing molecule definitions (e.g., from example_data) using standard Python file I/O. 2. Apply the smiter.lib.csv_to_peak_properties conversion function to transform the tabular data into a peak properties dictionary structure.: "Load the CSV file containing molecule definitions (e.g., from example_data) using standard Python file I/O. 2. Apply the smiter.lib.csv_to_peak_properties conversion function to transform the tabular"
- [other] Validate that the resulting dictionary contains the required keys and structure expected by SMITER's simulation functions.: "Validate that the resulting dictionary contains the required keys and structure expected by SMITER's simulation functions."
- [other] Serialize the peak properties dictionary to a Python pickle or JSON file for use in subsequent simulation steps.: "Serialize the peak properties dictionary to a Python pickle or JSON file for use in subsequent simulation steps."
- [readme] SMITER (Synthetic mzML writer) is a python-based command-line tool designed to simulate LC-MS/MS runs.: "SMITER (Synthetic mzML writer) is a python-based command-line tool designed to simulate LC-MS/MS runs."
- [readme] As SMITER features a modular design, noise and fragmentation models can easily be implemented or adapted.: "As SMITER features a modular design, noise and fragmentation models can easily be implemented or adapted."
