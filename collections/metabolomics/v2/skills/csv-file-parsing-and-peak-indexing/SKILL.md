---
name: csv-file-parsing-and-peak-indexing
description: Use when you have a metabolomics dataset (CSV format) containing detected peaks with m/z values and optionally retention time windows, and you need to filter a Pickaxe-generated compound expansion to keep only compounds whose masses match these observed peaks within a specified mass tolerance.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - RDKit
  - Python
  - pandas (implied)
derived_from:
- doi: 10.1186/s12859-023-05149-8
  title: Pickaxe
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pickaxe_cq
    doi: 10.1186/s12859-023-05149-8
    title: Pickaxe
  dedup_kept_from: coll_pickaxe_cq
schema_version: 0.2.0
---

# csv-file-parsing-and-peak-indexing

## Summary

Parse a CSV file of detected metabolomics peaks to extract m/z values and optional retention time windows, then index these peaks for mass-tolerance-based compound matching during reaction network filtering. This skill prepares raw peak-list data for downstream metabolomics filter operations that retain only generated compounds whose adduct-adjusted masses fall within a specified Da tolerance of observed peaks.

## When to use

You have a metabolomics dataset (CSV format) containing detected peaks with m/z values and optionally retention time windows, and you need to filter a Pickaxe-generated compound expansion to keep only compounds whose masses match these observed peaks within a specified mass tolerance. This is the prerequisite parsing step before implementing mass-matching logic in a MetabolomicsFilter subclass.

## When NOT to use

- Peak data is already in memory as a pre-parsed data structure and does not need CSV I/O.
- You are filtering against identified peaks (known compound assignments); the metabolomics filter is designed for unidentified peaks only.
- The metabolomics data is in a format other than CSV (e.g., mzML, NetCDF); use a format-specific parser instead.

## Inputs

- CSV file of detected metabolomics peaks with m/z column
- Optional retention time window column(s) in the same CSV
- Peak-list file path (string)

## Outputs

- Indexed peak data structure (e.g., list of dicts or DataFrame) containing m/z values
- Optional indexed retention time windows keyed by peak identity
- Set of unidentified peak indices for filtering logic

## How to apply

Read the peak-list CSV file to extract m/z column(s) and optional retention time columns. Store the peaks in a data structure (e.g., list of dictionaries or pandas DataFrame) indexed by m/z for rapid lookup. Parse retention time windows if present—these will constrain matching to compounds whose predicted or observed RT falls within the tolerance window. Document the CSV schema (column names, units for m/z and RT) as instance attributes in the Filter subclass's __init__ method. This parsed peak index is then queried in _choose_cpds_to_filter by iterating over compound dictionaries, computing their adduct-adjusted neutral masses using RDKit molecular weight from SMILES, and checking whether each mass falls within mass_tolerance of any indexed peak m/z. Return the set of compound IDs whose masses do not match any peak.

## Related tools

- **RDKit** (Compute molecular weight from SMILES to derive adduct-adjusted masses for matching against parsed peak m/z values) — https://rdkit.org/docs/api-docs.html
- **Python** (Implement CSV parsing logic and data structure indexing within Filter subclass)
- **pandas (implied)** (Optional—load and manipulate CSV peak-list with column extraction and filtering)

## Evaluation signals

- Peak CSV parses without errors and all m/z values are extracted as numeric types.
- Parsed peak index size matches the number of rows in the input CSV (excluding header).
- Retention time windows, if present, are correctly extracted and stored with proper unit consistency.
- Querying the peak index with a known m/z returns the correct peak record within mass_tolerance threshold.
- Unidentified peaks are correctly flagged; identified peaks (if present in the CSV) are excluded from the filter index per metabolomics filter specification.

## Limitations

- CSV schema is assumed to be consistent (e.g., m/z column name and data type); parsing will fail silently if column names differ or m/z values are non-numeric.
- Large peak-list files (>100k peaks) may require memory-efficient indexing (e.g., hash map or spatial index) to avoid slowdowns during _choose_cpds_to_filter iteration.
- Retention time prediction relies on mordred descriptors; if RT windows are provided but the Pickaxe run does not include RT model training, RT filtering will be skipped.
- Peak m/z and retention time units are assumed to match filter configuration (Da and seconds, respectively); mismatched units will cause incorrect matches.

## Evidence

- [other] 1. Parse the metabolomics peak-list CSV to extract m/z values and (optionally) retention time windows.: "Parse the metabolomics peak-list CSV to extract m/z values and (optionally) retention time windows."
- [other] 2. The metabolomics filter requires four core parameters: (1) met_data_path specifying a CSV of detected peaks; (2) possible_adducts listing adducts to add to each mass; (3) mass_tolerance in Da defining the matching window; and optionally (4) retention time prediction using mordred descriptors. Only unidentified peaks in the metabolomics data are used for filtering.: "metabolomics filter requires four core parameters: (1) met_data_path specifying a CSV of detected peaks; (2) possible_adducts listing adducts to add to each mass; (3) mass_tolerance in Da defining"
- [intro] It will force pickaxe to only keep compounds with masses (and, optionally, retention time (RT)) within a set tolerance of a list of peaks: "It will force pickaxe to only keep compounds with masses (and, optionally, retention time (RT)) within a set tolerance of a list of peaks"
- [other] Default filters are created using [RDKit](https://rdkit.org/docs/api-docs.html), a python library providing a collection of cheminformatic tools.: "Default filters are created using RDKit, a python library providing a collection of cheminformatic tools."
