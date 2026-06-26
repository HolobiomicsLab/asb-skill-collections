---
name: file-format-handling-csv-excel
description: Use when you have molecular descriptor data in CSV or EXCEL format and
  need to pass it to BitterPredict.m or another descriptor-based classifier.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3373
  tools:
  - BitterPredict.m
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.jafc.3c09767
  title: bittermass
evidence_spans:
- BitterPredict.m gets as input CSV or EXCEL files with required descriptors of molecules,
  and calucautes a predictions if each molecule is bitter or not
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_bittermass_cq
    doi: 10.1021/acs.jafc.3c09767
    title: bittermass
  dedup_kept_from: coll_bittermass_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jafc.3c09767
  all_source_dois:
  - 10.1021/acs.jafc.3c09767
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# file-format-handling-csv-excel

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Load and parse CSV or EXCEL files containing molecular descriptors into a structured table format suitable for classifier input. This skill bridges raw descriptor data files and machine-learning prediction workflows by ensuring proper file I/O and data integrity.

## When to use

You have molecular descriptor data in CSV or EXCEL format and need to pass it to BitterPredict.m or another descriptor-based classifier. The input files must contain required molecular descriptors (columns) and one row per molecule, with molecule identifiers preserved for downstream output annotation.

## When NOT to use

- Input is already a parsed descriptor table in memory; file I/O is unnecessary.
- Input files lack required molecular descriptor columns; validate schema before loading.
- Molecule identifiers are missing or non-unique; BitterPredict.m requires traceable per-molecule predictions.

## Inputs

- CSV file with molecular descriptors and molecule identifiers
- EXCEL file with molecular descriptors and molecule identifiers

## Outputs

- In-memory descriptor table (pandas DataFrame or equivalent)
- Structured output file with molecule identifiers and predicted class labels

## How to apply

Load the CSV or EXCEL file using pandas (Python) or equivalent file I/O library, ensuring all required descriptor columns are present and non-empty. Validate that the table has one row per molecule and that identifiers (molecule names or IDs) are preserved as a column or index. Pass the resulting descriptor table directly to the BitterPredict.m classifier, which will iterate over rows to generate per-molecule predictions. Compile predictions alongside the original molecule identifiers into a structured output file (CSV or EXCEL) for downstream analysis or reporting.

## Related tools

- **BitterPredict.m** (Classifier that accepts the loaded descriptor table and generates binary bitterness predictions per molecule) — https://github.com/Niv-Lab/BitterPredict1

## Examples

```
import pandas as pd; descriptors = pd.read_csv('molecules.csv'); predictions = BitterPredict(descriptors); predictions.to_csv('bitter_predictions.csv')
```

## Evaluation signals

- All required molecular descriptor columns are present and non-null in the loaded table.
- Number of rows equals number of molecules; no rows are dropped or duplicated during parsing.
- Molecule identifiers are preserved and match 1:1 with rows in the descriptor table.
- Output file contains one prediction per input molecule, with identifiers intact.
- Predictions are binary (bitter or not bitter) with no missing or invalid values.

## Limitations

- Full code availability is conditional on publication; early-stage adoption may encounter undocumented descriptor requirements.
- No changelog is available; version compatibility and format evolution are unclear.
- Descriptor schema is not explicitly specified in the publication; users must refer to examples in the BitterPredict.m file itself.

## Evidence

- [readme] BitterPredict.m gets as input CSV or EXCEL files with required descriptors of molecules, and calucautes a predictions if each molecule is bitter or not.: "BitterPredict.m gets as input CSV or EXCEL files with required descriptors of molecules, and calucautes a predictions if each molecule is bitter or not"
- [other] Load the input CSV or EXCEL file containing molecular descriptors using appropriate file I/O (pandas or equivalent).: "Load the input CSV or EXCEL file containing molecular descriptors using appropriate file I/O (pandas or equivalent)"
- [other] Compile predictions into a structured output file with molecule identifiers and predicted class labels.: "Compile predictions into a structured output file with molecule identifiers and predicted class labels"
- [readme] Details and examples of how to use the code is avalibale inside bitterPredict.m file.: "Details and examples of how to use the code is avalibale inside bitterPredict.m file"
