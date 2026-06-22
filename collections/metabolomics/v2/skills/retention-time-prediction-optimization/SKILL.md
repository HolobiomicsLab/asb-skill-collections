---
name: retention-time-prediction-optimization
description: Use when when you have a retention-time dataset (e.g., SMRT or Eawag_XBridgeC18_364) in .xlsx format and need to train or adapt a graph neural network model to predict chromatographic retention times for new compounds.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3372
  - http://edamontology.org/topic_3474
  tools:
  - Python
  - PyG
  - RDKit
  - Pandas
  - torch-scatter
  - torch-sparse
  - torch-cluster
  - NumPy
  - PyTorch
  - PyG (PyTorch Geometric)
  - TorchMetrics
  - torch-scatter, torch-sparse, torch-cluster
  techniques:
  - LC-MS
  - GC-MS
derived_from:
- doi: 10.1021/acs.jcim.4c02179
  title: ABCoRT
evidence_spans:
- '**Python**'
- '**PyG**'
- '**RDKit**'
- '- **RDKit**'
- '**Pandas**'
- '**torch-scatter**'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_abcort_cq
    doi: 10.1021/acs.jcim.4c02179
    title: ABCoRT
  dedup_kept_from: coll_abcort_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jcim.4c02179
  all_source_dois:
  - 10.1021/acs.jcim.4c02179
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# retention-time-prediction-optimization

## Summary

Train and optimize graph neural network models to predict liquid chromatography retention times for small molecules using the ABCoRT framework. This skill enables fine-tuning of pre-trained models on domain-specific retention-time datasets via transfer learning, improving prediction accuracy for chemical compound characterization.

## When to use

When you have a retention-time dataset (e.g., SMRT or Eawag_XBridgeC18_364) in .xlsx format and need to train or adapt a graph neural network model to predict chromatographic retention times for new compounds. Use this skill when baseline model performance is insufficient and transfer learning from a pre-trained checkpoint can accelerate convergence.

## When NOT to use

- Input dataset is not in .xlsx format or lacks expected column structure (SMILES, retention time labels)
- Pre-trained checkpoint is unavailable or corrupted and baseline model training is not feasible
- Retention-time data is from an entirely different chromatographic platform (e.g., GC-MS instead of LC) not covered by pre-training or transfer-learning datasets

## Inputs

- Pre-trained model checkpoint (PyTorch .pt or .pth file)
- Retention-time dataset in .xlsx format (e.g., Eawag_XBridgeC18_364.xlsx or SMRT.xlsx)
- SMILES or molecular structure representations (processed via RDKit)
- Command-line arguments specifying dataset path and optional hyperparameters

## Outputs

- Fine-tuned model checkpoint saved to disk
- Training logs and metrics (loss, validation accuracy) per epoch
- Inference predictions on test or validation splits
- TorchMetrics monitoring artifacts

## How to apply

Execute the training or transfer-learning workflow using Python entry points. For baseline training on the SMRT retention-time dataset, run 'python train_SMRT.py' to instantiate the PyTorch + PyG graph neural network and train from scratch, monitoring loss and validation metrics via TorchMetrics over epochs. For domain adaptation, run 'python train_transfer_FE.py --DataSet <dataset_name>.xlsx' to load a pre-trained checkpoint, fine-tune on your target dataset, and save the adapted model. Monitor training metrics (loss, validation accuracy) to detect convergence; save the final model checkpoint and logs upon completion. The choice between baseline and transfer training depends on data availability: transfer learning is preferred when fine-tuning datasets are small relative to the pre-training corpus.

## Related tools

- **PyTorch** (Deep learning framework for graph neural network model training and optimization)
- **PyG (PyTorch Geometric)** (Graph neural network library for molecular graph construction and message passing)
- **RDKit** (Cheminformatics toolkit for converting SMILES to molecular graphs and feature extraction)
- **Pandas** (Data loading and preprocessing for retention-time .xlsx files)
- **TorchMetrics** (Real-time training metrics monitoring (loss, validation accuracy) during fine-tuning)
- **torch-scatter, torch-sparse, torch-cluster** (GPU-accelerated graph operations for efficient PyG tensor aggregation and sampling)

## Examples

```
python train_transfer_FE.py --DataSet Eawag_XBridgeC18_364.xlsx
```

## Evaluation signals

- Training loss decreases monotonically or plateaus at a minimum over epochs, indicating model convergence
- Validation metrics (e.g., mean absolute error on held-out retention times) improve or stabilize, showing generalization
- Saved checkpoint file exists and is loadable by PyTorch without schema errors
- Inference predictions on test set fall within the expected retention-time range (e.g., 1–30 min for typical LC) and match literature or experimental references
- TorchMetrics logs record non-NaN values for all tracked metrics at each epoch

## Limitations

- Transfer learning performance depends on similarity between pre-training data (SMRT) and target dataset; significant chromatographic differences may limit transfer gains
- Model assumes molecular structures are representable as graphs with RDKit; SMILES parsing failures will cause training to fail
- No explicit hyperparameter tuning guidance provided in README; optimal learning rate, batch size, and epochs must be determined empirically
- Thirteen transfer-learning datasets are mentioned but only one (Eawag_XBridgeC18_364.xlsx) is exemplified; dataset availability and format consistency are not guaranteed

## Evidence

- [readme] train_SMRT.py script entry point for baseline model training: "If you want to train the Model. Please command 
```
python train_SMRT.py
```"
- [readme] transfer learning workflow on thirteen datasets with dataset parameter: "If you want to run the transfer learning on thirteen transfer learning data sets, use:
```
python train_transfer_FE.py --DataSet  Eawag_XBridgeC18_364.xlsx
```"
- [intro] graph neural network architecture training on SMRT retention-time dataset: "Execute the training entry point using Python with the command 'python train_SMRT.py', which will instantiate the graph neural network architecture (PyTorch + PyG)"
- [intro] TorchMetrics monitoring during fine-tuning process: "Monitor training metrics via TorchMetrics during fine-tuning. 4. Save the fine-tuned model checkpoint and training logs."
- [intro] RDKit, PyTorch, and PyG as core tools for molecular representation and training: "Execute train_transfer_FE.py with the --DataSet parameter set to Eawag_XBridgeC18_364.xlsx using PyTorch and PyG for graph neural network operations."
