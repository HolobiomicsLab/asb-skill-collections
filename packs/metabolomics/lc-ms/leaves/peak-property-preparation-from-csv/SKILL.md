---
name: peak-property-preparation-from-csv
description: Use when you have a CSV file containing nucleoside or peptide molecular data (formulas, identifiers, retention times, intensities) that you want to simulate as LC-MS/MS runs. Use this skill as the mandatory first step before selecting a fragmentation model and noise injector in SMITER.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - SMITER
  - Python
  techniques:
  - LC-MS
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# peak-property-preparation-from-csv

## Summary

Convert tabular nucleoside or peptide molecular data from CSV format into a peak properties dictionary compatible with SMITER's LC-MS/MS simulation pipeline. This preparation step abstracts chemical formulas and molecular identifiers into SMITER's internal representation, enabling downstream fragmentation modeling and synthetic spectrum generation.

## When to use

You have a CSV file containing nucleoside or peptide molecular data (formulas, identifiers, retention times, intensities) that you want to simulate as LC-MS/MS runs. Use this skill as the mandatory first step before selecting a fragmentation model and noise injector in SMITER.

## When NOT to use

- Input data is already in SMITER's native peak properties format (skip conversion).
- Molecular data lacks chemical formula information (SMITER's fragmentation is formula-based).
- CSV schema does not align with SMITER's expected columns (consult example_data in the repository for the required schema).

## Inputs

- CSV file with molecular data (chemical formulas, identifiers, peak properties)
- SMITER library module (smiter.lib)

## Outputs

- Peak properties dictionary (Python dict or SMITER-compatible object)
- Validated molecular metadata ready for fragmentation and noise injection

## How to apply

Organize your input CSV with columns for molecular identifiers, chemical formulas, and peak properties (e.g., retention time, intensity). Call `smiter.lib.csv_to_peak_properties` on the CSV file to deserialize and validate the data into SMITER's peak properties dictionary format. This dictionary then becomes the input to downstream workflow steps: fragmentation model selection, noise injection, and gradient-parameter definition. The conversion abstracts the tabular format into SMITER's internal object model, allowing the modular fragmentation interface to select between nucleoside and peptide fragmentors without data re-formatting.

## Related tools

- **SMITER** (LC-MS/MS simulation platform providing the csv_to_peak_properties conversion function and downstream fragmentation and noise models) — https://github.com/LeidelLab/SMITER
- **Python** (Runtime environment for SMITER library and CSV I/O operations)

## Examples

```
from smiter.lib import csv_to_peak_properties; peak_props = csv_to_peak_properties('example_data.csv')
```

## Evaluation signals

- Peak properties dictionary is non-empty and contains all expected molecular entries from the input CSV.
- Each entry in the dictionary has valid chemical formula strings (parseable by SMITER's formula engine).
- Dictionary keys and structure match SMITER's expected format for downstream fragmentation model input (e.g., accessible via `smiter.synthetic_mzml.write_mzml`).
- No validation errors or exceptions are raised during conversion; the function returns successfully.
- Downstream fragmentation model (PeptideFragmentor or NucleosideFragmentor) accepts the dictionary without schema errors.

## Limitations

- Conversion relies on CSV schema correctness; malformed or missing columns will cause silent data loss or exceptions.
- Chemical formula validation is deferred to SMITER's fragmentation modules; invalid formulas may only be detected later in the simulation.
- The function does not perform retention time prediction or normalization; intensities and retention times are passed through as-is from the CSV.
- No support for metadata beyond chemical formulas and peak properties; additional experimental context (e.g., instrument parameters, quantification standards) must be handled separately.

## Evidence

- [other] You can convert a csv file (as in example_data) to csv using `smiter.lib.csv_to_peak_properties`: "You can convert a csv file (as in example_data) to csv using `smiter.lib.csv_to_peak_properties`"
- [other] create the peak properties dict: "1. create the peak properties dict (You can convert a csv file (as in example_data) to csv using `smiter.lib.csv_to_peak_properties`)"
- [readme] It enables the simulation of any biomolecule since all calculations are based on the chemical formulas.: "It enables the simulation of any biomolecule since all calculations are based on the chemical formulas."
- [readme] SMITER offers several methods for peptide fragmentation and two models for nucleoside fragmentation: "By default, SMITER uses an established noise model and offers several methods for peptide fragmentation or two models for nucleoside fragmentation."
