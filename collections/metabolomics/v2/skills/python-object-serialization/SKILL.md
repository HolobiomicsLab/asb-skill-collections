---
name: python-object-serialization
description: Use when after constructing a peak properties dictionary via csv_to_peak_properties or other data transformation steps, and before passing the dictionary to subsequent SMITER simulation functions (fragmentor selection, noise injection, mzML generation).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0335
  edam_topics:
  - http://edamontology.org/topic_3674
  tools:
  - Python
  - SMITER
  - Python pickle module
  - Python json module
derived_from:
- doi: 10.3390/genes12030396
  title: SMITER
evidence_spans:
- https://pypi.python.org/pypi
- SMITER (Synthetic mzML writer) is a python-based command-line tool
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

# python-object-serialization

## Summary

Serialize structured Python objects (dictionaries, data structures) to persistent storage formats (pickle, JSON) for reuse in downstream computational workflows. This skill ensures that in-memory data structures from SMITER's simulation pipeline can be reliably stored and retrieved across analysis sessions.

## When to use

After constructing a peak properties dictionary via csv_to_peak_properties or other data transformation steps, and before passing the dictionary to subsequent SMITER simulation functions (fragmentor selection, noise injection, mzML generation). Use this skill when you need to checkpoint intermediate results, share data between pipeline stages, or avoid recomputing expensive transformations.

## When NOT to use

- Input is already serialized (file on disk); deserialize instead of re-serializing.
- Peak properties dictionary has not been validated for required keys/schema; validate before serialization to catch structural errors early.
- Workflow does not require intermediate checkpointing or data sharing between pipeline stages; serialization adds I/O overhead.

## Inputs

- peak properties dictionary (Python dict object with molecule definitions and properties)
- file path (string) specifying output location

## Outputs

- serialized pickle file (.pkl)
- serialized JSON file (.json)

## How to apply

After the peak properties dictionary is validated (contains required keys and structure expected by SMITER simulation functions), select a serialization format based on downstream tool compatibility: pickle for Python-native workflows with no interoperability requirement, or JSON for human-readability and cross-language compatibility. Serialize the dictionary using Python's built-in `pickle.dump()` or `json.dumps()` functions to write to disk. Verify serialization succeeded by reading the file back and performing a schema or key-presence check to ensure all required peak properties fields are intact.

## Related tools

- **Python pickle module** (built-in serialization to binary format for checkpoint storage)
- **Python json module** (built-in serialization to JSON text format for human inspection and cross-language compatibility)
- **SMITER** (consumes deserialized peak properties dictionary in simulation pipeline (csv_to_peak_properties, fragmentation, noise, mzML writing)) — https://github.com/LeidelLab/SMITER

## Examples

```
import pickle; from smiter.lib import csv_to_peak_properties; peak_props = csv_to_peak_properties('example_data/molecules.csv'); pickle.dump(peak_props, open('peak_properties.pkl', 'wb'))
```

## Evaluation signals

- Serialized file exists at specified output path and has non-zero file size.
- Deserialization round-trip succeeds: read the file back and verify the reconstructed dictionary is type `dict` with all keys present from the original.
- Schema validation: reconstructed dictionary contains expected top-level keys (e.g., molecule identifiers, peak properties, chemical formulas) matching the SMITER pipeline requirements.
- Downstream consumption: deserialized dictionary is successfully passed to SMITER simulation functions (e.g., fragmentation, noise injection) without key-not-found or type mismatch errors.

## Limitations

- Pickle format is Python-specific; not suitable for cross-language pipelines or long-term archival without version pinning.
- JSON serialization requires all dictionary values to be JSON-serializable (strings, numbers, lists, nested dicts); complex Python objects (custom classes, functions) require custom encoder.
- No built-in schema enforcement during serialization; structural validation must be performed before or after serialization to detect malformed dictionaries.
- Large dictionaries (many molecules or high-dimensional peak properties) may result in large file sizes; compression (gzip) may be needed for storage efficiency.

## Evidence

- [other] Serialize the peak properties dictionary to a Python pickle or JSON file for use in subsequent simulation steps.: "Serialize the peak properties dictionary to a Python pickle or JSON file for use in subsequent simulation steps."
- [other] Validate that the resulting dictionary contains the required keys and structure expected by SMITER's simulation functions.: "Validate that the resulting dictionary contains the required keys and structure expected by SMITER's simulation functions."
- [other] Run the simulation and write the resulting mzML using `smiter.synthetic_mzml.write_mzml`: "Run the simulation and write the resulting mzML using `smiter.synthetic_mzml.write_mzml`"
