---
name: molecular-graph-neural-network-adaptation
description: Use when you have an in-house collection of liquid chromatography spectra and retention time measurements for small molecules, and you want to improve structural identification accuracy by predicting retention times.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3474
  tools:
  - Python
  - Anaconda
  - Preprocess.py
  - Transferlearning.py
  - PyTorch
  - RDKit
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# molecular-graph-neural-network-adaptation

## Summary

Adapt a pretrained graph neural network (GNN-RT) to predict liquid chromatography retention times on a new in-house molecular database via transfer learning. This skill enables practitioners to leverage a data-driven GNN model trained on public data and fine-tune it on proprietary spectra and retention time measurements without retraining from scratch.

## When to use

You have an in-house collection of liquid chromatography spectra and retention time measurements for small molecules, and you want to improve structural identification accuracy by predicting retention times. You have access to the pretrained GNN-RT model and wish to adapt it to your database without training a model de novo.

## When NOT to use

- Your spectra files are already preprocessed into graph representations — skip Preprocess.py and proceed directly to Transferlearning.py.
- You have no retention time labels for your molecules — transfer learning requires paired spectra and ground-truth retention times to supervise fine-tuning.
- Your molecular database is radically different from the pretraining domain (e.g., very large macromolecules or isotopically labeled compounds) — the pretrained GNN may not generalize and retraining from scratch may be more appropriate.

## Inputs

- spectra files (raw chromatography data in data directory)
- in-house molecular database with retention time labels
- pretrained GNN-RT model (PyTorch checkpoint)

## Outputs

- standardized molecular graphs (from Preprocess.py)
- fine-tuned GNN-RT model weights (adapted to in-house database)
- retention time predictions on validation set
- prediction accuracy and loss metrics

## How to apply

First, organize your spectra files in a designated data directory and run Preprocess.py to standardize molecular graphs and retention time labels using RDKit. Second, load the pretrained GNN-RT PyTorch model and configure transfer-learning hyperparameters (learning rate, batch size, number of epochs). Third, run Transferlearning.py to fine-tune the pretrained GNN weights on your target database, which updates only the model parameters relevant to your data distribution rather than training all weights from random initialization. Finally, evaluate the adapted model on a held-out validation set from your database and record prediction accuracy and loss metrics to confirm that retention time prediction has improved.

## Related tools

- **Preprocess.py** (Standardizes spectra files and generates molecular graph representations and retention time labels from in-house database) — https://github.com/Qiong-Yang/GNN-RT
- **Transferlearning.py** (Fine-tunes pretrained GNN-RT model weights on the target in-house molecular database) — https://github.com/Qiong-Yang/GNN-RT
- **PyTorch** (Deep learning framework for loading, configuring, and fine-tuning the GNN model)
- **RDKit** (Converts molecular structures to standardized graph representations during preprocessing)
- **Anaconda** (Python environment manager for installing dependencies (Python 3.6, PyTorch, RDKit))

## Examples

```
python Preprocess.py && python Transferlearning.py
```

## Evaluation signals

- Preprocess.py successfully generates standardized molecular graph files and retention time labels with no errors or missing values.
- Transferlearning.py completes without convergence failures, and loss metrics decrease over epochs, indicating the model is learning from the in-house data.
- Prediction accuracy on the held-out validation set from the in-house database meets or exceeds a domain-relevant threshold (e.g., mean absolute error in retention time units acceptable for structural identification).
- Adapted model predictions show reduced error compared to the pretrained model evaluated on the same in-house validation set, confirming that transfer learning improved task-specific performance.
- No data leakage: validation set retention time predictions are computed only on samples not used during fine-tuning.

## Limitations

- Transfer learning performance depends on the similarity between the pretraining dataset and your in-house database; large domain shifts may reduce benefit.
- Requires paired ground-truth retention time labels for all or most in-house samples; sparse labeling reduces fine-tuning effectiveness.
- No changelog or version history documented in the repository; reproducibility and compatibility across updates may be limited.
- GNN-RT is designed for small molecules; applicability to macromolecules, peptides, or proteins is not addressed.

## Evidence

- [intro] The transfer-learning workflow and its sequential steps: "put your spectra files in to data directory and run [Preprocess.py], [Train.py] and [Transferlearning.py]"
- [other] The role of Preprocess.py in preparing data for transfer learning: "Prepare the user-supplied database using Preprocess.py to generate standardized molecular graphs and retention time labels."
- [other] The core operation of Transferlearning.py: fine-tuning pretrained weights: "Run Transferlearning.py to fine-tune the pretrained GNN weights on the target database."
- [other] Validation methodology for adapted model: "Evaluate the adapted model on a held-out validation set from the target database and record prediction accuracy and loss metrics."
- [readme] GNN-RT use case: improving structural identification via retention time prediction: "GNN-RT method, which is proved to be an effective way to predict small molecule LC retention time and improve the accuracy of structural identification of small molecules"
- [readme] Required dependencies and Python version: "Anaconda for python 3.6, conda install pytorch, conda install -c rdkit rdkit"
