---
name: batch-generation-and-validation
description: Use when you have raw mzML files and a feature table (CSV) from LCMS
  data processed by tools like mzMine, and you need to create train/test/validation
  batches with specific matrix dimensions (120 × 2) and verified margin/peak signal
  separation before training or evaluating a neural network.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3315
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

# Batch generation and validation

## Summary

Generate peak matrix batches from raw LCMS data and feature tables using NeatMS's NN_handler, then validate that the resulting matrices match documented shape, dimensionality, and margin/peak encoding specifications. This skill ensures that preprocessed data is correctly formatted before neural network training.

## When to use

You have raw mzML files and a feature table (CSV) from LCMS data processed by tools like mzMine, and you need to create train/test/validation batches with specific matrix dimensions (120 × 2) and verified margin/peak signal separation before training or evaluating a neural network classifier.

## When NOT to use

- Your input feature table is not in a supported format (NeatMS expects mzMine or similar; verify compatibility first).
- You have fewer than ~500–1000 labeled peaks total; batch creation will succeed but training may be unreliable without sufficient data.
- Your raw mzML files and feature table are misaligned or contain no peaks meeting the min_scan_num threshold; create_batches() will fail or produce empty batches.

## Inputs

- raw mzML files (LC-MS data)
- feature table (CSV format, e.g., from mzMine output)
- feature table format specification (string, e.g., 'mzmine')

## Outputs

- training batch arrays (peak matrices)
- test batch arrays (peak matrices)
- validation batch arrays (peak matrices)
- batch metadata (split ratios, peak counts, class distribution)

## How to apply

Load raw mzML files and the corresponding feature table into a NeatMS Experiment object, specifying the input format (e.g., 'mzmine'). Instantiate a NN_handler with batch-creation parameters: matrice_size=120 (the scan window length), margin=1 (the margin region around the peak apex), and min_scan_num=5 (minimum scans per peak). Call create_batches() with desired split ratios (e.g., 80% training, 10% test, 10% validation) and set normalise_class=False unless you need balanced class representation. Inspect the resulting batch arrays to verify: (1) each peak matrix has shape 2 × 120 (binary dimension × scan dimension); (2) the first 40 and last 40 values encode margin regions (0) and the middle 40 values encode peak signal (1); and (3) the split counts match the requested ratios. This validation step confirms the preprocessing pipeline is functioning as documented before proceeding to model training.

## Related tools

- **NeatMS** (Provides the Experiment and NN_handler classes to load data, create batches, and manage preprocessing parameters) — https://github.com/bihealth/NeatMS
- **NumPy** (Supports array inspection and shape validation of batch matrices)
- **pandas** (Enables loading and parsing of CSV feature tables)
- **Python** (Runtime environment for NeatMS and batch inspection scripts)

## Examples

```
from neatms import Experiment, NN_handler; exp = Experiment(path_to_mzml='./raw_data/', path_to_feature_table='./features.csv', peak_detection='mzmine'); nn = NN_handler(exp, matrice_size=120, margin=1, min_scan_num=5); batches = nn.create_batches(split_ratio=[0.8, 0.1, 0.1], normalise_class=False); print(batches['train'].shape, batches['test'].shape)
```

## Evaluation signals

- Each peak matrix in the batch has exact shape (2, 120), confirming matrice_size and binary encoding are correct.
- The first 40 and last 40 values of each peak matrix correspond to margin regions (encoded as 0) and the middle 40 values correspond to peak signal (encoded as 1).
- Training, test, and validation batch counts match the requested split ratios (e.g., 80%–10%–10% or custom values).
- The number of peaks retained after min_scan_num=5 filtering is consistent with expected data (i.e., no unexpected zero-peak batches).
- No NaN or out-of-range values appear in the peak matrix arrays; all values are valid binary (0 or 1) or normalized signal intensities.

## Limitations

- NeatMS requires mzML raw files and a matching feature table in a supported format (e.g., mzMine CSV); if files are misaligned or in an incompatible format, batch creation will fail silently or produce empty batches.
- The min_scan_num=5 threshold filters out peaks with fewer than 5 data points; if your dataset has very few or very short peaks, this may result in severe data loss.
- Batch creation assumes the raw mzML files and feature table IDs are consistent and traceable; manually edited or partially processed data may cause ID mismatches.
- The documented result_matrix_shape (2 × 120 per peak) is fixed; if you need different matrix sizes, you must adjust matrice_size and re-validate the margin/peak split accordingly.

## Evidence

- [intro] NeatMS is an open source python package for untargeted LCMS signal labelling and filtering: "NeatMS is an open source python package for untargeted LCMS signal labelling and filtering"
- [other] Create a NeatMS Experiment object by loading raw mzML files from the example data folder and the corresponding feature table (csv format) from the github repository, specifying the input format as 'mzmine': "Create a NeatMS Experiment object by loading raw mzML files from the example data folder and the corresponding feature table (csv format) from the github repository, specifying the input format as"
- [other] Instantiate a NN_handler (Neural Network Handler) object with the experiment and default batch-creation parameters (matrice_size=120, margin=1, min_scan_num=5): "Instantiate a NN_handler (Neural Network Handler) object with the experiment and default batch-creation parameters (matrice_size=120, margin=1, min_scan_num=5)"
- [other] Call create_batches() with default split ratios (80% training, 10% test, 10% validation) and normalise_class=False to generate peak matrix batches: "Call create_batches() with default split ratios (80% training, 10% test, 10% validation) and normalise_class=False to generate peak matrix batches"
- [other] Validate that the first and last 40 values correspond to margin portions and the middle 40 values correspond to peak signal, matching the documented result_matrix_shape: "Validate that the first and last 40 values correspond to margin portions and the middle 40 values correspond to peak signal, matching the documented result_matrix_shape"
- [readme] NeatMS enables automated filtering of false positive MS1 peaks reported by commonly used LCMS data processing pipelines: "NeatMS enables automated filtering of false positive MS<sup>1</sup> peaks reported by commonly used LCMS data processing pipelines"
