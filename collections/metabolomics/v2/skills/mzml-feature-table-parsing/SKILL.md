---
name: mzml-feature-table-parsing
description: Use when you have raw LCMS data in mzML format and a feature table (CSV)
  from a peak detection pipeline (e.g., MZmine) and need to prepare these inputs for
  NeatMS preprocessing, batch creation, or peak classification. This skill is the
  mandatory entry point for any NeatMS workflow.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - NeatMS
  - Python
  - NumPy
  - pandas
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1021/acs.analchem.1c02220
  title: neatms
evidence_spans:
- NeatMS provides the necessary functions to do that, all we will have to do is create
  a `Neural network handler` object
- Calling the method `get_threshold()` will compute and return the optimal threshold
- After installation, you should be able to import NeatMS
- Import the required libraries first
- import numpy as np
- import pandas as pd
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_neatms
    doi: 10.1021/acs.analchem.1c02220
    title: neatms
  dedup_kept_from: coll_neatms
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c02220
  all_source_dois:
  - 10.1021/acs.analchem.1c02220
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mzML-feature-table parsing

## Summary

Load and parse raw LCMS data from mzML files and corresponding feature tables (CSV format) to instantiate a NeatMS Experiment object. This skill is essential for initializing the data pipeline before peak matrix generation and neural network-based peak filtering.

## When to use

You have raw LCMS data in mzML format and a feature table (CSV) from a peak detection pipeline (e.g., MZmine) and need to prepare these inputs for NeatMS preprocessing, batch creation, or peak classification. This skill is the mandatory entry point for any NeatMS workflow.

## When NOT to use

- mzML and feature table are already loaded into memory as a NeatMS Experiment object; skip directly to batch creation.
- Feature table is in a format other than CSV (e.g., TSV, Excel); convert first or verify parser compatibility.
- mzML files are missing or path is incorrect; validate file integrity and directory structure before parsing.

## Inputs

- Directory containing raw mzML files
- Feature table in CSV format (from MZmine or similar LCMS data processing pipeline)
- Peak detection format specification (e.g., 'mzmine')

## Outputs

- NeatMS Experiment object
- Parsed spectral data indexed by sample and feature
- Aligned mzML–feature table correspondence

## How to apply

Create a NeatMS Experiment object by specifying three required parameters: the path to the raw data folder containing mzML files, the path to the feature table (CSV format) or feature tables folder, and the peak detection format (e.g., 'mzmine'). The Experiment object will parse and align the mzML spectral data with the feature table, automatically matching samples across both inputs. This initialization enables downstream operations such as batch creation, annotation, and neural network training. The parsed data structure encodes retention time, m/z values, and scan-level intensity information from mzML alongside feature-level annotations from the CSV.

## Related tools

- **NeatMS** (Python package providing the Experiment class for loading and parsing mzML and feature table data) — https://github.com/bihealth/NeatMS
- **Python** (Runtime environment for NeatMS Experiment instantiation and data object manipulation)

## Examples

```
from NeatMS.Experiment import Experiment; exp = Experiment(path_raw_data='./example_data/', path_feature_table='./features.csv', peak_detection='mzmine')
```

## Evaluation signals

- Experiment object instantiation succeeds without file-not-found or format-parsing errors.
- Number of samples in Experiment matches number of mzML files in the input directory.
- Number of features in Experiment matches number of rows in the feature table CSV.
- Spectral data (m/z, retention time, intensity) are correctly indexed and accessible from the Experiment object.
- Sample names and feature IDs align consistently across mzML and CSV inputs (no missing or mismatched entries).

## Limitations

- Requires feature table in CSV format; other delimited or binary formats (e.g., TSV, Excel, mzTab) must be converted first.
- Peak detection format must be explicitly specified and match the source pipeline (e.g., 'mzmine'); incorrect format specification will cause misalignment or parsing failures.
- No built-in validation of chemical plausibility or peak quality at parse time; garbage-in–garbage-out behavior if the input CSV contains invalid m/z or retention time values.
- Large mzML files or high-dimensional feature tables may incur memory overhead; no streaming or lazy-loading option mentioned in the article.

## Evidence

- [methods] In order to create an experiment object, we need to set 3 parameters: The path to the raw data folder, The path to the feature table (.csv) or the feature tables folder, The peak detection: "In order to create an experiment object, we need to set 3 parameters: The path to the raw data folder, The path to the feature table (.csv) or the feature tables folder, The peak detection"
- [other] Create a NeatMS Experiment object by loading raw mzML files from the example data folder and the corresponding feature table (csv format) from the github repository, specifying the input format as 'mzmine'.: "Create a NeatMS Experiment object by loading raw mzML files from the example data folder and the corresponding feature table (csv format) from the github repository, specifying the input format as"
- [readme] NeatMS is an open source python package for untargeted LCMS signal labelling and filtering that enables automated filtering of false positive MS1 peaks reported by commonly used LCMS data processing pipelines.: "NeatMS is an open source python package for untargeted LCMS signal labelling and filtering that enables automated filtering of false positive MS1 peaks"
