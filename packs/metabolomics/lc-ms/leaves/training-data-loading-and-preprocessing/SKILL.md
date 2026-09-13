---
name: training-data-loading-and-preprocessing
description: Use when you have downloaded raw LC-MS spectral peak data from a public
  repository (e.g., DOI 10.25345/C5FD2F) and need to ingest it into memory and prepare
  it in the format expected by a TensorFlow/Keras neural network classifier.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
  tools:
  - TensorFlow
  - Keras
  - EDML_deep_learning2.py
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.9b02983
  title: DNN peak classifier
- doi: 10.25345/C5FD2F
  title: ''
evidence_spans:
- Deep Neural Networks for Classification of LC-MS Spectral Peaks
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_dnn_peak_classifier_cq
    doi: 10.1021/acs.analchem.9b02983
    title: DNN peak classifier
  dedup_kept_from: coll_dnn_peak_classifier_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.9b02983
  all_source_dois:
  - 10.1021/acs.analchem.9b02983
  - 10.25345/C5FD2F
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# training-data-loading-and-preprocessing

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Load and prepare LC-MS spectral peak datasets from public repositories for deep neural network training. This skill bridges raw deposited data and model-ready tensors by implementing the data loading utilities and preprocessing pipeline required before neural network initialization.

## When to use

You have downloaded raw LC-MS spectral peak data from a public repository (e.g., DOI 10.25345/C5FD2F) and need to ingest it into memory and prepare it in the format expected by a TensorFlow/Keras neural network classifier. Use this skill when your goal is to train a DNN model from scratch on peak classification tasks and you need a reproducible, documented pathway from repository artifact to training-ready tensors.

## When NOT to use

- You are training on a pre-processed feature table or matrix that has already been vectorized and normalized by another pipeline.
- Your LC-MS data is in a different repository or format (e.g., mzML files or vendor-specific binary formats) not covered by the script's loading utilities.
- You are performing inference or prediction on a pre-trained model; use only the trained model weights, not the training data loading pipeline.

## Inputs

- Raw LC-MS spectral peak dataset files (downloaded from DOI 10.25345/C5FD2F)
- EDML_deep_learning2.py script with embedded data loading utilities

## Outputs

- In-memory tensor representation of LC-MS peaks ready for neural network input
- Associated class labels and metadata aligned with peak tensors

## How to apply

Execute the EDML_deep_learning2.py script, which contains purpose-built data loading utilities that ingest the LC-MS peak datasets from the specified DOI repository. The script handles format conversion, normalization, and tensor assembly in a single call. Before training begins, verify that the loaded data matches the expected schema (spectral peak features, class labels, and sample counts) by inspecting the shape and value ranges of the resulting tensors. The preprocessing logic is embedded in the script rather than exposed as separate parameters; reproducibility depends on using the unmodified script on the deposited dataset version.

## Related tools

- **TensorFlow** (Deep learning framework used to construct and train the neural network model on loaded LC-MS peak data)
- **Keras** (High-level API (integrated in TensorFlow) that defines the neural network architecture and training loop applied to preprocessed peak tensors)
- **EDML_deep_learning2.py** (Script containing the data loading utilities and preprocessing logic that transforms raw LC-MS datasets into model-ready tensors) — https://github.com/JainLab/Manuscript-DNNs-for-Classification-of-LCMS-Peaks

## Examples

```
python EDML_deep_learning2.py
```

## Evaluation signals

- Verify that the loaded tensor shape matches the expected number of samples and spectral features (no truncation or shape mismatch errors).
- Check that class labels are present and aligned 1:1 with peak samples; count per-class distribution and confirm no labels are missing or duplicated.
- Inspect value ranges of loaded spectral intensities; confirm they are positive and within expected magnitude (e.g., no NaN, Inf, or negative values indicating a loading error).
- Run the data loading section independently and confirm the script completes without exceptions and returns non-empty tensors.
- Trace the script's internal logging or print statements to confirm the correct dataset repository URL was accessed and file counts match the deposited manifest.

## Limitations

- The data loading utilities are hardcoded to the specific LC-MS peak dataset format and repository (DOI 10.25345/C5FD2F); they are not generalizable to other LC-MS repositories or data sources without modification.
- No changelog or version history is provided in the repository documentation, so it is unclear whether the script or dataset have been updated since publication; reproducibility may be affected by repository changes.
- The preprocessing pipeline (normalization, filtering, feature selection) is not exposed as separate, documented steps within the script; practitioners cannot easily inspect or modify individual preprocessing stages.

## Evidence

- [readme] For training the neural net model from scratch using the data sets that we used, first download the datasets from https://doi.org/doi:10.25345/C5FD2F. Then use the script EDML_deep_learning2.py.: "For training the neural net model from scratch using the data sets that we used, first download the datasets from https://doi.org/doi:10.25345/C5FD2F. Then use the script EDML_deep_learning2.py."
- [other] Load the LC-MS Peaks Dataset (from DOI 10.25345/C5FD2F) into memory using the data loading utilities provided in EDML_deep_learning2.py.: "Load the LC-MS Peaks Dataset (from DOI 10.25345/C5FD2F) into memory using the data loading utilities provided in EDML_deep_learning2.py."
- [other] Training the neural network model from scratch requires two sequential steps: first downloading the LC-MS datasets from the specified repository, then executing the EDML_deep_learning2.py script on those datasets.: "Training the neural network model from scratch requires two sequential steps: first downloading the LC-MS datasets from the specified repository, then executing the EDML_deep_learning2.py script on"
