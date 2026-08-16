---
name: chromatography-data-preprocessing
description: Use when you have raw spectra files from a liquid chromatography experiment (in-house or external database) and need to adapt a pretrained GNN-RT model to predict retention times for your molecules. Preprocessing is the mandatory first step before any model training or transfer learning can proceed.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3429
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3407
  tools:
  - Python
  - Anaconda
  - Preprocess.py
  - RDKit
  techniques:
  - LC-MS
  - GC-MS
derived_from:
- doi: 10.1021/acs.analchem.0c04071
  title: GNN-RT
evidence_spans:
- Anaconda for python 3.6
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_gnn_rt_cq
    doi: 10.1021/acs.analchem.0c04071
    title: GNN-RT
  dedup_kept_from: coll_gnn_rt_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.0c04071
  all_source_dois:
  - 10.1021/acs.analchem.0c04071
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# chromatography-data-preprocessing

## Summary

Standardize raw liquid chromatography spectra files into molecular graphs and retention time labels required for training or transfer-learning of graph neural network retention time (GNN-RT) models. This preprocessing step converts unstructured spectral data into structured, model-ready molecular representations.

## When to use

You have raw spectra files from a liquid chromatography experiment (in-house or external database) and need to adapt a pretrained GNN-RT model to predict retention times for your molecules. Preprocessing is the mandatory first step before any model training or transfer learning can proceed.

## When NOT to use

- Your data is already in the form of pre-computed molecular graphs with labeled retention times — skip to model training.
- You are applying a model to new spectra for prediction only (inference mode) — preprocessing is not needed if graphs are already available.
- Your spectra come from a fundamentally different analytical modality (e.g., gas chromatography instead of liquid chromatography) — GNN-RT preprocessing assumes LC data.

## Inputs

- spectra files (raw LC spectral data in data directory)
- molecular structure information embedded in or accompanying spectra

## Outputs

- standardized molecular graphs
- retention time labels aligned to molecular graphs
- preprocessed dataset ready for model training or transfer learning

## How to apply

Place all spectra files into the designated data directory. Run Preprocess.py to parse the spectra files and generate standardized molecular graphs (via RDKit) with their corresponding liquid chromatography retention time labels. This produces a clean, labeled dataset ready for downstream model training. The preprocessing standardizes molecular representations so that downstream GNN training receives consistent graph-structured inputs with aligned retention time targets, which is critical for accurate GNN-RT model performance.

## Related tools

- **Preprocess.py** (main preprocessing script that parses spectra files and generates molecular graphs with retention time labels) — https://github.com/Qiong-Yang/GNN-RT
- **RDKit** (generates standardized molecular graph representations from molecular structure data)
- **Python** (scripting environment for running Preprocess.py)
- **Anaconda** (dependency and environment management for Python 3.6 runtime)

## Examples

```
python Preprocess.py
```

## Evaluation signals

- Preprocess.py completes without errors and generates output files in the expected format (molecular graphs and retention time labels).
- Output molecular graphs are valid RDKit objects with correct node and edge connectivity for the input chemical structures.
- Retention time labels are numeric values aligned one-to-one with each preprocessed molecular graph.
- Downstream model training (Train.py) accepts the preprocessed dataset without schema or format errors.
- Comparison of input spectra count matches output graph count (no records dropped unexpectedly).

## Limitations

- Preprocessing assumes spectra files are properly formatted and contain valid molecular structure information; malformed or incomplete spectra may be silently dropped or cause parsing errors.
- The standardization applied by Preprocess.py is tightly coupled to the GNN-RT architecture — preprocessing for other retention time prediction models may require different molecular graph generation or feature engineering.
- No changelog is provided, making it unclear whether preprocessing behavior or output format has changed between repository versions.

## Evidence

- [intro] Preprocess.py standardizes spectra into molecular graphs and retention time labels: "put your spectra files in to data directory and run [Preprocess.py]"
- [readme] Preprocessing is the first mandatory step before training or transfer learning: "If you want to train a model based on your in-house database, please put your spectra files in to **data** directory and run [Preprocess.py]"
- [readme] GNN-RT uses molecular graphs as input and RDKit is a dependency for graph generation: "conda install -c rdkit rdkit"
- [intro] The three-step workflow requires preprocessing before training or transfer learning: "The transfer-learning workflow requires three sequential steps: (1) place spectra files in the data directory, (2) run Preprocess.py to prepare the data, (3) run Train.py to train the model, and (4)"
