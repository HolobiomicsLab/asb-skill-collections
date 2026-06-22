---
name: natural-product-model-application
description: Use when you have (1) a collection of natural product or drug candidate molecules in SMILES format, (2) a downstream task (classification at Class/Superclass/Pathway levels, bioactivity regression, or virtual screening ranking), (3) access to pre-trained NaFM weights, and (4) a need to leverage.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_3373
  - http://edamontology.org/topic_0154
  tools:
  - PyTorch
  - Git
  - PyTorch Lightning
  - PyTorch Geometric
  - scikit-learn
  - NaFM-Official
derived_from:
- doi: 10.1002/anie.202507483
  title: NA
evidence_spans:
- github.com/TomAIDD/NaFM-Official
- Fork the repository
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_nafm_cq
    doi: 10.1002/anie.202507483
    title: NA
  dedup_kept_from: coll_nafm_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1002/anie.202507483
  all_source_dois:
  - 10.1002/anie.202507483
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# natural-product-model-application

## Summary

Apply a pre-trained foundation model (NaFM) to downstream natural product tasks—including taxonomy classification, bioactivity prediction, and virtual screening—by loading pre-trained weights, preparing task-specific datasets, and fine-tuning or running inference on molecular SMILES inputs. This skill leverages the model's learned evolutionary and structural patterns to generate embeddings and predictions for novel bioactive compounds.

## When to use

Use this skill when you have (1) a collection of natural product or drug candidate molecules in SMILES format, (2) a downstream task (classification at Class/Superclass/Pathway levels, bioactivity regression, or virtual screening ranking), (3) access to pre-trained NaFM weights, and (4) a need to leverage learned evolutionary patterns rather than training a task-specific model from scratch. Especially applicable when conventional representations tailored to synthetic molecules are insufficient for capturing natural synthesis patterns.

## When NOT to use

- Input molecules are already in graph or fingerprint format rather than SMILES strings—NaFM expects canonical SMILES as primary input.
- Task involves synthetic small molecules where conventional SMILES-based models (trained on ChEMBL or similar) are the established baseline; NaFM is optimized for natural products and may not outperform synthetic-optimized alternatives.
- Downstream dataset contains fewer than ~50–100 labeled examples; fine-tuning risks overfitting and transfer learning may provide minimal benefit over task-specific training.

## Inputs

- Pre-trained model checkpoint (NaFM.ckpt)
- Molecular SMILES strings (CSV file with 'SMILES' column)
- Downstream dataset (CSV files with labels for classification or bioactivity values for regression)
- Hyperparameter configuration file (YAML format, e.g., examples/Finetune.yml)

## Outputs

- Fine-tuned model checkpoint (PyTorch Lightning .ckpt file)
- Predictions CSV file (predictions.csv with SMILES and predicted class/bioactivity)
- Molecular embeddings (1024-dimensional vectors for each input molecule)
- Evaluation metrics (classification accuracy, regression MAE/RMSE, ranking scores for virtual screening)

## How to apply

First, set up the Python environment with PyTorch 2.4.1, PyTorch Geometric, and Lightning 2.4.0 using the provided conda recipe or manual installation. Download pre-trained weights (NaFM.ckpt) from Zenodo and organize datasets (Ontology, Regression, Lotus, Bgc, or External) into the downstream_data directory structure. For classification tasks, run `python train.py --task finetune` with the appropriate dataset flag (e.g., `--dataset Ontology --dataset-arg Class`), learning rate (typically 1.0e-4 for classification, 5.0e-5 for regression), and embedding dimension (1024). For inference on new molecules, prepare a CSV with a SMILES column and call `python inference.py --task classification` or `--task regression`, specifying the fine-tuned checkpoint path. Monitor early stopping (patience typically 50 epochs) and adjust hyperparameters (learning rate, dropout, batch size) based on dataset size and downstream task characteristics. Save and validate predictions against known benchmarks or held-out test sets.

## Related tools

- **PyTorch** (Deep learning framework for model training and inference)
- **PyTorch Lightning** (High-level training and checkpoint management abstraction; version 2.4.0 specified)
- **PyTorch Geometric** (Graph neural network library for molecular graph encoding and masked graph modeling)
- **scikit-learn** (Metrics computation and evaluation (e.g., classification accuracy, regression scoring))
- **NaFM-Official** (Official repository containing pre-trained weights, training/inference scripts, and downstream task examples) — github.com/TomAIDD/NaFM-Official

## Examples

```
python train.py --task finetune --num-epochs 300 --emb-dim 1024 --feat-dim 512 --num-layer 6 --drop-ratio 0.15 --dataset Ontology --dataset-root downstream_data/Ontology --pretrained-path NaFM.ckpt --lr 1.0e-4 --batch-size 256 --early-stopping-patience 50 --dataset-arg Class --seed 0
```

## Evaluation signals

- Fine-tuned model achieves comparable or better performance (accuracy, MAE/RMSE, AUC) on held-out test sets compared to reported benchmarks in the paper (e.g., taxonomy classification outperforming models pre-trained on synthetic molecules).
- Generated embeddings cluster correctly by natural product class or bioactivity range when visualized (t-SNE or UMAP); evolutionary patterns are preserved (e.g., related scaffold types co-locate).
- Predictions CSV contains valid predictions for all input SMILES; no NaN or out-of-range values (classification: valid class labels; regression: bioactivity values within training data range).
- Virtual screening ranking correlates with known bioactivity or experimental hits when available; hit rates and retrieval metrics match or exceed reported SOTA values.
- Training loss converges smoothly; early stopping triggers within the patience window, indicating stable model optimization without divergence.

## Limitations

- The provided evaluation scripts (test.py) are minimal demonstration templates, not the exact production pipelines used to generate published benchmark results; hyperparameter tuning and downstream task specifics may require adjustment.
- Pre-training data is limited to natural products; the model's generalization to novel chemical spaces (e.g., highly engineered synthetic scaffolds or macrocycles not represented in training) is not fully characterized.
- Fine-tuning on small downstream datasets may suffer from overfitting; early stopping and regularization (dropout, learning rate scheduling) are critical but require dataset-specific calibration.
- SMILES canonicalization and salt removal occur during preprocessing (filter.py); non-standard or malformed SMILES may fail silently or produce spurious embeddings.

## Evidence

- [intro] The proposed framework achieves state-of-the-art (SOTA) performance across a wide range of downstream tasks in natural product mining and drug discovery: "The proposed framework achieves state-of-the-art (SOTA) performance across a wide range of downstream tasks in natural product mining and drug discovery"
- [intro] Our method integrates contrastive learning with masked graph modeling, effectively encoding scaffold-derived evolutionary patterns alongside diverse side-chain information: "Our method integrates contrastive learning with masked graph modeling, effectively encoding scaffold-derived evolutionary patterns alongside diverse side-chain information"
- [intro] We first benchmark NaFM on taxonomy classification against models pre-trained on synthetic molecules, demonstrating their inadequacy for capturing natural synthesis patterns: "We first benchmark NaFM on taxonomy classification against models pre-trained on synthetic molecules, demonstrating their inadequacy for capturing natural synthesis patterns"
- [intro] Finally, we apply NaFM to virtual screening tasks, showing its potential to provide meaningful molecular representations and facilitate the discovery of novel bioactive compounds: "Finally, we apply NaFM to virtual screening tasks, showing its potential to provide meaningful molecular representations and facilitate the discovery of novel bioactive compounds"
- [readme] conda install pytorch==2.4.1 torchvision==0.19.1 torchaudio==2.4.1 pytorch-cuda=12.1 -c pytorch -c nvidia; pip install lightning==2.4.0; pip install torch_geometric: "conda install pytorch==2.4.1 torchvision==0.19.1 torchaudio==2.4.1 pytorch-cuda=12.1 -c pytorch -c nvidia; conda install tensorboard; pip install lightning==2.4.0; pip install torch_geometric"
- [readme] For inference on new molecules (CSV with a 'SMILES' column): python inference.py --task classification --downstream-data [data location] --checkpoint-path [your finetuned model path]: "For inference on new molecules (CSV with a "SMILES" column): python inference.py --task classification --downstream-data [data location] --checkpoint-path [your finetuned model path]"
- [readme] The repository includes lightweight demonstration scripts intended to illustrate the basic inference workflow and input/output usage of NaFM. In particular, test.py should be regarded as a minimal demonstration template rather than the exact production evaluation pipeline used to generate the benchmark results reported in the paper.: "The repository includes lightweight demonstration scripts intended to illustrate the basic inference workflow and input/output usage of NaFM. test.py should be regarded as a minimal demonstration"
- [readme] Support for multiple datasets (Ontology, Regression, Lotus, Bgc, External): "Support for multiple datasets (Ontology, Regression, Lotus, Bgc, External)"
