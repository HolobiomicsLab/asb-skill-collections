---
name: side-chain-representation-learning
description: Use when working with natural product molecules where conventional synthetic-molecule representations fail to capture synthesis patterns, and you need to encode both scaffold topology and the diverse chemical substituents (side chains) that distinguish natural product variants.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_2275
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3474
  tools:
  - Git
  - PyTorch or equivalent deep learning framework (inferred from GNN/contrastive learning context)
  - PyTorch
  - PyG (PyTorch Geometric)
  - PyTorch Lightning
  - RDKit (inferred from SMILES standardization)
derived_from:
- doi: 10.1002/anie.202507483
  title: NA
evidence_spans:
- Fork the repository
- Our method integrates contrastive learning with masked graph modeling
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

# side-chain-representation-learning

## Summary

Learn dense vector representations of molecular side-chain information in natural products by integrating masked graph modeling with contrastive learning objectives. This skill encodes the structural and chemical diversity of side chains alongside scaffold-derived evolutionary patterns to improve downstream task generalization.

## When to use

Apply this skill when working with natural product molecules where conventional synthetic-molecule representations fail to capture synthesis patterns, and you need to encode both scaffold topology and the diverse chemical substituents (side chains) that distinguish natural product variants. Use it when you have access to SMILES strings or molecular graphs and require a single pre-trained model capable of generalizing across multiple downstream tasks (taxonomy classification, bioactivity prediction, virtual screening).

## When NOT to use

- Input molecules are purely synthetic and already well-represented by existing pre-trained models (e.g., ChemBERTa, MolBERT trained on large synthetic databases); conventional supervised learning will suffice.
- Side-chain information is not chemically meaningful or is absent (e.g., highly simplified scaffold-only representations); masked modeling will add noise rather than signal.
- Computational resources are severely limited; the dual-objective training with 6-layer GNNs and contrastive mining is memory-intensive and slower than single-task supervised baselines.

## Inputs

- SMILES strings (standard molecular notation as CSV or pickle format)
- Molecular graphs (node and edge tensors with atomic and bond features)
- Pre-training dataset: natural product structure collection (e.g., pretrain_smiles.pkl)
- Downstream task annotations (class labels, bioactivity values, or taxonomy hierarchies)

## Outputs

- Pre-trained molecular encoder weights (PyTorch checkpoint, .ckpt format)
- Dense molecular embeddings (1024-dimensional vectors per molecule)
- Fine-tuned model checkpoints for classification/regression tasks
- Predictions on downstream tasks (CSV with molecule ID and predicted label/value)

## How to apply

Construct a dual pre-training objective that combines masked graph modeling (random masking of nodes and edges in the molecular graph, then predicting their features and connectivity) with contrastive learning (pulling together augmented views of the same molecule while pushing apart different molecules). Feed preprocessed SMILES or graph representations through a graph neural network (GNN) with 6 layers and 1024 embedding dimension. The masked modeling component recovers hidden side-chain features, while the contrastive loss (cosine similarity with temperature-scaled softmax) ensures the learned embeddings capture functional and structural diversity. Train jointly on these objectives until convergence, then freeze the encoder and fine-tune on downstream tasks. The key rationale is that masked modeling alone would neglect evolutionary relationships, while contrastive learning alone would not exploit the rich structural information in side-chain masking.

## Related tools

- **PyTorch** (Deep learning framework for implementing dual-objective pre-training loop (contrastive and masked modeling forward passes, gradient computation, checkpoint management))
- **PyG (PyTorch Geometric)** (Graph neural network library for constructing GNN layers, handling molecular graph inputs, and computing graph convolutions on side-chain and scaffold substructures) — https://data.pyg.org/whl/torch-2.4.0+cu121.html
- **PyTorch Lightning** (Training loop abstraction and distributed training orchestration for managing the dual pre-training objectives and checkpoint saving)
- **RDKit (inferred from SMILES standardization)** (Molecular parsing and graph construction from SMILES; side-chain feature extraction and scaffold decomposition)

## Examples

```
python train.py --conf examples/Pretrain.yml
```

## Evaluation signals

- Verify that masked node/edge predictions reach >85% accuracy on held-out test set, indicating the model has learned meaningful side-chain patterns.
- Confirm contrastive loss converges (temperature-scaled cosine similarity of augmented pairs >> dissimilar pairs) and embedding space cluster score (silhouette or Davies–Bouldin index) improves over training.
- Validate that downstream task performance (accuracy on taxonomy classification, RMSE on bioactivity regression) on NaFM pre-trained weights exceeds baseline models trained on synthetic molecules by ≥5–10%.
- Check that fine-tuned model generalizes to external/unseen natural product datasets with <20% performance drop compared to in-distribution validation performance.
- Ensure molecular embeddings from the learned encoder separate by known structural properties (e.g., scaffold class, side-chain functional group) via t-SNE or UMAP visualization.

## Limitations

- Pre-training requires a large, curated natural product dataset (pretrain_smiles.pkl); results may degrade if the training set is small (<10k unique scaffolds) or biased toward a narrow taxonomic range.
- Masked modeling assumes random masking strategies are informative; if masking removes critical side-chain atoms that define bioactivity, recovery will be difficult and contrastive learning must compensate.
- The method is tailored to small-molecule natural products with explicit SMILES representation; applicability to macrocycles, proteins, or other polymeric natural products is limited.
- Hyperparameter sensitivity: contrastive loss temperature, masking ratio, and embedding dimension (1024) were tuned on the reported datasets; transfer to domains with different side-chain complexity may require re-tuning.
- Models pre-trained on natural products do not necessarily capture synthetic chemical space; downstream tasks on synthetically-derived bioactivity data may show limited benefit over synthetic pre-training.

## Evidence

- [intro] Our method integrates contrastive learning with masked graph modeling, effectively encoding scaffold-derived evolutionary patterns alongside diverse side-chain information: "Our method integrates contrastive learning with masked graph modeling, effectively encoding scaffold-derived evolutionary patterns alongside diverse side-chain information"
- [intro] most deep learning approaches in natural product research are based on supervised learning tailored to specific downstream tasks. However, the one-model-one-task paradigm often lacks generalization: "most deep learning approaches in natural product research are based on supervised learning tailored to specific downstream tasks. However, the one-model-one-task paradigm often lacks generalization"
- [intro] conventional molecular representation techniques are not well-suited to the unique structural and evolutionary features of natural products: "conventional molecular representation techniques are not well-suited to the unique structural and evolutionary features of natural products"
- [intro] The proposed framework achieves state-of-the-art (SOTA) performance across a wide range of downstream tasks in natural product mining and drug discovery: "The proposed framework achieves state-of-the-art (SOTA) performance across a wide range of downstream tasks in natural product mining and drug discovery"
- [readme] conda install pytorch==2.4.1 torchvision==0.19.1 torchaudio==2.4.1 pytorch-cuda=12.1 -c pytorch -c nvidia: "conda install pytorch==2.4.1 torchvision==0.19.1 torchaudio==2.4.1 pytorch-cuda=12.1 -c pytorch -c nvidia"
- [readme] pip install torch_geometric; pip install pyg_lib torch_scatter torch_sparse torch_cluster torch_spline_conv -f https://data.pyg.org/whl/torch-2.4.0+cu121.html: "pip install torch_geometric; pip install pyg_lib torch_scatter torch_sparse torch_cluster torch_spline_conv -f https://data.pyg.org/whl/torch-2.4.0+cu121.html"
