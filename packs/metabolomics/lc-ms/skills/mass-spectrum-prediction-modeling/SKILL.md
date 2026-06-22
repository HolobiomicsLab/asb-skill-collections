---
name: mass-spectrum-prediction-modeling
description: Use when you have a collection of molecular structures (SMILES or chemical graphs) with paired experimental tandem mass spectra and want to build or benchmark a predictive model.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3375
  tools:
  - PyTorch
  - TensorFlow
  - PubChem
  - ms-pred (ICEBERG, SCARF, NEIMS, MassFormer implementations)
  - NIST'20 dataset
  - MassSpecGym
  techniques:
  - LC-MS
derived_from:
- doi: 10.1038/s42256-024-00816-8
  title: ICEBERG
evidence_spans:
- _No usage/docs found._
- By inputting the chemical formula and your experimental spectrum, the WebUI will rank it against all candidates from PubChem.
- the WebUI will rank it against all candidates from PubChem
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_iceberg_cq
    doi: 10.1038/s42256-024-00816-8
    title: ICEBERG
  dedup_kept_from: coll_iceberg_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s42256-024-00816-8
  all_source_dois:
  - 10.1038/s42256-024-00816-8
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrum-prediction-modeling

## Summary

Train and evaluate neural network models (FFN, GNN, or graph transformers) to predict tandem mass spectra from molecular structures, using standardized benchmark datasets and equivalent hyperparameter settings to enable fair comparison across spectrum prediction approaches.

## When to use

You have a collection of molecular structures (SMILES or chemical graphs) with paired experimental tandem mass spectra and want to build or benchmark a predictive model. Use this skill when you need to evaluate multiple spectrum prediction architectures (ICEBERG, SCARF, NEIMS, MassFormer, etc.) under controlled conditions with the same covariates and hyperparameter sweeps, or when you are implementing a baseline model as part of a comparative study.

## When NOT to use

- Your molecular structures lack associated experimental spectra for training supervision.
- You only need to predict spectra for a single query molecule without benchmarking against multiple models — use a pre-trained ICEBERG WebUI or inference-only script instead.
- Your spectra are already in a fully processed feature matrix format and you do not need end-to-end training from raw molecular structures.

## Inputs

- molecular structures (SMILES strings or SDF format)
- experimental tandem mass spectra (MGF or HDF5 format with m/z and intensity pairs)
- chemical formula annotations
- collision energy metadata (if available)
- train/validation/test split definitions

## Outputs

- trained model checkpoint (PyTorch or TensorFlow weights)
- predicted spectra (fragment masses and intensities in JSON or CSV format)
- evaluation metrics (cosine similarity, spectral match score, top-1/top-k retrieval accuracy)
- prediction files for benchmark comparison

## How to apply

Load the benchmark dataset (NIST'20, MassSpecGym, or PubChem-derived spectra) and preprocess molecular structures into fixed-length feature vectors (for FFN) or graph representations (for GNN/graph transformer encoders). Split data into train/validation/test sets using equivalent splits across all compared models. Construct the encoder architecture (feedforward, graph neural network, or transformer) with standardized hyperparameters (e.g., hidden layer sizes, activation functions, learning rate) and train end-to-end on the spectrum prediction task using mean squared error or equivalent loss functions with Adam or similar optimizers. Evaluate on the held-out test set by computing prediction accuracy metrics such as cosine similarity, spectral match score, or top-k retrieval accuracy. Save trained model checkpoints, predictions, and evaluation metrics to enable comparison with reference results from the ms-pred framework.

## Related tools

- **ms-pred (ICEBERG, SCARF, NEIMS, MassFormer implementations)** (primary framework for training and evaluating spectrum prediction models with equivalent settings) — https://github.com/coleygroup/ms-pred
- **PyTorch** (deep learning framework for constructing and training feedforward and graph neural network encoders)
- **TensorFlow** (alternative deep learning framework for encoder implementation)
- **PubChem** (source of molecular structures and chemical formula data for training and retrieval benchmarks)
- **NIST'20 dataset** (commercial benchmark dataset with collision energy annotations for model training and evaluation)
- **MassSpecGym** (public spectrum benchmark dataset for training when NIST'20 license unavailable)

## Examples

```
python src/ms_pred/dag_pred/train_gen.py --config configs/iceberg/iceberg_gen_train.yaml && python src/ms_pred/dag_pred/train_inten.py --config configs/iceberg/iceberg_inten_train.yaml
```

## Evaluation signals

- Prediction metrics (cosine similarity, spectral match score) computed on held-out test set match or exceed reported baseline performance from the ms-pred framework for the same dataset split.
- Trained model checkpoint saves successfully and weights can be loaded for inference without shape or dtype errors.
- Top-k retrieval accuracy (e.g., top-1 retrieval on [M+H]+ benchmarks ~40% on NIST'20) is consistent with published ICEBERG results when using equivalent hyperparameters and dataset splits.
- Predicted spectra produce valid output structures (JSON/CSV with fragment m/z and intensity pairs, no NaN or infinite values).
- Model architecture (hidden layer dimensions, activation functions, encoder type) matches the specification in the equivalent-settings comparison protocol across all compared models.

## Limitations

- NIST'20 is a commercial dataset requiring purchase; publicly available alternatives (MassSpecGym) have undergone less manual curation and yield different prediction performance.
- Training ICEBERG requires two GPUs with ≥24 GB RAM each; smaller GPU RAM requires reducing batch size and potentially skipping contrastive finetuning, which impacts model performance.
- SCARF predicts spectra at the chemical-formula granularity level, whereas ICEBERG predicts at the molecular-fragment level; these prediction granularities are not directly comparable and require separate evaluation protocols.
- Collision energy annotations are available only in NIST'20; other datasets may not support energy-dependent spectrum prediction.
- Contrastive finetuning for ICEBERG requires PubChem-SMILES mapping (pubchem_formulae_inchikey.hdf5), which is a separate download step not included in the base repository.

## Evidence

- [readme] equivalent-settings comparison: "In order to fairly compare various spectra models, we implement a number of baselines and alternative models using equivalent settings across models (i.e., same covariates, hyperparameter sweeps for"
- [other] FFN/GNN encoder training: "Construct a feedforward neural network encoder with standard hidden layers and ReLU activations. 4. Train the FFN encoder on the spectrum prediction task using mean squared error loss and an"
- [other] evaluation metrics: "Evaluate the model on a held-out test set, computing prediction accuracy metrics (e.g. cosine similarity, spectral match score)."
- [other] GNN encoder construction: "Construct a graph neural network (GNN) encoder to learn molecular representations from chemical graphs. 3. Train the GNN encoder end-to-end on the spectrum prediction task using the dataset split and"
- [readme] ICEBERG two-part training: "ICEBERG is trained in two parts: a learned fragment generator and an intensity predictor. The pipeline for training and evaluating this model can be accessed in `run_scripts/iceberg/`."
- [readme] NIST'20 commercial status: "``nist20`` is a commercial dataset available for purchase through several vendors worldwide. Given the scale of effort required to purchase samples, run experiments, and collect such a large amount"
- [readme] MassSpecGym curation note: "You can download the weights trained on the MassSpecGym dataset, publicly available via Dropbox. Please keep in mind that MassSpecGym has undergone less manual curation and quality control compared"
- [readme] GPU memory requirements: "You need two GPUs with at least 24GB RAM to train ICEBERG (we used NVIDIA A5000 for development). If you are trying to train the model on a smaller GPU, try cutting down the batch size and skipping"
- [readme] ICEBERG retrieval performance: "ICEBERG is our recommended model with a 40% top-1 retrieval accuracy with [M+H]+, benchmarked on the NIST'20 dataset."
- [readme] prediction granularity comparison: "ICEBERG predicts spectra at the level of molecular fragments, whereas SCARF predicts spectra at the level of chemical formula."
