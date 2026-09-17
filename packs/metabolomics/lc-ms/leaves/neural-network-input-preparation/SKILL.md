---
name: neural-network-input-preparation
description: Use when when you have annotated representative LCMS samples (raw mzML
  files + labeled feature tables in mzmine CSV format) and need to convert them into
  balanced or unbalanced peak matrix batches with fixed dimensions for neural network
  training.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3937
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - NeatMS
  - Python
  - NumPy
  - pandas
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
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

# neural-network-input-preparation

## Summary

Prepare peak matrix batches from raw LCMS data for neural network training by loading mzML and feature tables into a NeatMS Experiment, then instantiating a NN_handler to generate training/test/validation splits with configurable matrix dimensions, margin encoding, and class balancing. This skill ensures that input peak matrices conform to expected dimensions and class distributions before model training.

## When to use

When you have annotated representative LCMS samples (raw mzML files + labeled feature tables in mzmine CSV format) and need to convert them into balanced or unbalanced peak matrix batches with fixed dimensions for neural network training. Use this when you want to verify that preprocessing parameters (matrix_size, margin, min_scan_num) produce the expected peak matrix shape and class distribution before feeding data to a neural network trainer.

## When NOT to use

- Feature table is not in CSV format or not mzmine-compatible; use format conversion tools first
- Raw mzML files are missing or cannot be accessed; batch creation requires both raw data and metadata
- Peak annotations are incomplete or majority of peaks are unlabeled; minimum sample requirements (10–20 pooled representative samples recommended) must be met

## Inputs

- Raw mzML files (LCMS mass spectrometry data)
- Labeled feature table (CSV format, mzmine-compatible)
- Data folder path containing raw mzML files
- Feature table file path

## Outputs

- Training batch arrays (peak matrices with shape 2×120 per peak)
- Test batch arrays
- Validation batch arrays
- Batch metadata (peak counts per class per batch)
- Peak matrix with binary encoding (margin=0, peak=1)

## How to apply

Load raw mzML files and corresponding feature table (CSV format, mzmine-compatible) into a NeatMS Experiment object. Instantiate an NN_handler with specified matrix dimensions (matrice_size=120 by default), margin width (1 by default), and minimum scan threshold (min_scan_num=5 by default). Call create_batches() with split ratios (80% training, 10% test, 10% validation) and set normalise_class=False to preserve original class imbalance or normalise_class=True to equalize class counts (bounded by smallest class size). Inspect resulting batch arrays to verify that peak matrices are 2×120 (binary encoding margin vs. peak regions), with margin occupying first and last 40 values and peak signal in the middle 40 values. Validate class distributions match the normalise_class parameter setting.

## Related tools

- **NeatMS** (Core package providing Experiment, NN_handler, and batch creation methods for peak matrix generation and class normalization) — https://github.com/bihealth/NeatMS
- **NumPy** (Array manipulation and inspection of peak matrix dimensions and values)
- **pandas** (Feature table I/O and metadata handling)
- **Python** (Programming language for orchestrating Experiment and NN_handler objects)

## Examples

```
from neatms import Experiment, NN_handler
exp = Experiment('/path/to/raw_data', '/path/to/feature_table.csv', input_data_type='mzmine')
nn_handler = NN_handler(exp, matrice_size=120, margin=1, min_scan_num=5)
nn_handler.create_batches(validation_split=0.1, normalise_class=True)
```

## Evaluation signals

- Peak matrices have expected shape of 2×120 (binary dimension and scan dimension)
- First and last 40 values of each peak matrix correspond to margin regions (encoding value 0)
- Middle 40 values correspond to peak signal regions (encoding value 1)
- When normalise_class=True, all three classes have equal peak counts within each batch (count = smallest class size); when normalise_class=False, class counts reflect original dataset imbalance
- Training, test, and validation batches have correct sample counts reflecting 80%, 10%, 10% split ratios

## Limitations

- Default minimum scan requirement (min_scan_num=5) will filter out peaks with fewer scans; peaks below this threshold cannot be included in batch matrices
- Class normalization (normalise_class=True) discards peaks from larger classes to match the smallest class; this reduces effective training data size and may lose minority peak variants
- Requires at least 10–20 pooled representative samples for optimal training dataset construction; smaller datasets may not provide sufficient diversity for generalization
- Matrix size (matrice_size=120) is fixed at instantiation; different peak widths or scan resolutions may require re-instantiation with adjusted parameters

## Evidence

- [methods] Load raw mzML and feature table, instantiate NN_handler with matrix parameters, generate train/test/validation batches: "Create a NeatMS Experiment object by loading raw mzML files from the example data folder and the corresponding feature table (csv format) from the github repository, specifying the input format as"
- [methods] Peak matrices encode margin vs. peak regions as binary values: "confirm that the binary dimension correctly encodes margin (0) vs. peak (1) regions. 5. Validate that the first and last 40 values correspond to margin portions and the middle 40 values correspond to"
- [methods] normalise_class parameter controls class distribution in batches: "When normalise_class is set to True, the create_batches() method ensures that every class has an equal number of peaks in the resulting training batches, with the total number of peaks per class"
- [methods] min_scan_num filters peaks below threshold: "`min_scan_number` argument will filter out all peaks that have a number of point (scan) lower than this value. `5` is the default value"
- [readme] NeatMS is designed for untargeted LCMS peak filtering: "**NeatMS** is an open source python package for untargeted LCMS signal labelling and filtering. **NeatMS** enables automated filtering of false positive MS<sup>1</sup> peaks reported by commonly used"
