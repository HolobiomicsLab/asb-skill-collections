---
name: peak-property-validation
description: Use when after converting a CSV file of molecule definitions into a peak properties dictionary using csv_to_peak_properties, or after loading a serialized peak properties dictionary from pickle/JSON storage, before passing it to SMITER simulation functions (e.g., smiter.synthetic_mzml.write_mzml).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0769
  tools:
  - SMITER
  - Python
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

# peak-property-validation

## Summary

Validate that a peak properties dictionary contains the required keys and structure expected by SMITER's LC-MS/MS simulation pipeline. This skill ensures data integrity before consuming the dictionary in downstream simulation functions like write_mzml.

## When to use

After converting a CSV file of molecule definitions into a peak properties dictionary using csv_to_peak_properties, or after loading a serialized peak properties dictionary from pickle/JSON storage, before passing it to SMITER simulation functions (e.g., smiter.synthetic_mzml.write_mzml). This skill is essential whenever the origin or integrity of the peak properties structure is uncertain.

## When NOT to use

- Peak properties dictionary is known to originate from a trusted, recently validated source with no intermediate serialization steps
- Input is a raw CSV file — use csv_to_peak_properties conversion first
- Validation is not part of your workflow and the downstream simulation tool will be run with error handling enabled

## Inputs

- peak_properties dictionary (dict)
- peak_properties serialized to pickle or JSON file

## Outputs

- validation report (boolean or exception)
- annotated dictionary with schema conformance metadata

## How to apply

Inspect the peak properties dictionary to confirm it contains all required keys and hierarchical structure expected by SMITER's simulation pipeline. Verify that molecule entries include chemical formulas, retention times, and intensity parameters compatible with the chosen fragmentor and noise injector. Check that data types match expectations (e.g., strings for formulas, floats for times/intensities). Perform a schema validation by attempting to instantiate or partially execute a simulation component (e.g., the fragmentor) with a subset of the dictionary to catch structural mismatches before full pipeline execution. Log or raise an exception if required keys are missing or values fall outside expected ranges.

## Related tools

- **SMITER** (Simulation framework that consumes the validated peak properties dictionary and requires its structure to match the expected format for fragmentor and noise injector compatibility) — https://github.com/LeidelLab/SMITER
- **Python** (Language used to implement dictionary inspection, schema validation, and integration with SMITER's lib functions)

## Examples

```
import pickle; import smiter.lib; peak_props = pickle.load(open('peak_properties.pkl', 'rb')); assert all(k in peak_props for k in ['molecules']), 'Missing required keys'; assert all(isinstance(m.get('formula'), str) for m in peak_props['molecules']), 'Formula must be string'
```

## Evaluation signals

- Presence of all required top-level keys in the dictionary (confirmed by iterating keys and comparing against SMITER library schema)
- Each molecule entry contains mandatory fields (chemical formula, retention time, intensity) with correct data types (string, float, float respectively)
- Dictionary can be successfully passed to smiter.synthetic_mzml.write_mzml or a test fragmentor instantiation without TypeError or KeyError
- Serialized and deserialized dictionary (pickle/JSON round-trip) retains identical structure and values
- No out-of-range values (e.g., negative retention times, zero or negative intensities, invalid chemical formula characters)

## Limitations

- Validation does not verify correctness of chemical formulas or retention time predictions — only structural integrity
- Validation assumes SMITER library schema is stable; updates to SMITER may require corresponding updates to validation rules
- Dictionary does not include optional fragmentation or noise model parameters; validation cannot catch incompatibility with chosen fragmentor/noise generator until runtime
- CSV source data quality issues (e.g., missing fields, malformed formulas) are not caught by validation but should be prevented at conversion time

## Evidence

- [other] Validate that the resulting dictionary contains the required keys and structure expected by SMITER's simulation functions.: "Validate that the resulting dictionary contains the required keys and structure expected by SMITER's simulation functions."
- [other] Apply the smiter.lib.csv_to_peak_properties conversion function to transform the tabular data into a peak properties dictionary structure.: "Apply the smiter.lib.csv_to_peak_properties conversion function to transform the tabular data into a peak properties dictionary structure."
- [other] create the peak properties dict (You can convert a csv file (as in example_data) to csv using `smiter.lib.csv_to_peak_properties`): "create the peak properties dict (You can convert a csv file (as in example_data) to csv using `smiter.lib.csv_to_peak_properties`)"
- [other] Run the simulation and write the resulting mzML using `smiter.synthetic_mzml.write_mzml`: "Run the simulation and write the resulting mzML using `smiter.synthetic_mzml.write_mzml`"
- [other] Serialize the peak properties dictionary to a Python pickle or JSON file for use in subsequent simulation steps.: "Serialize the peak properties dictionary to a Python pickle or JSON file for use in subsequent simulation steps."
