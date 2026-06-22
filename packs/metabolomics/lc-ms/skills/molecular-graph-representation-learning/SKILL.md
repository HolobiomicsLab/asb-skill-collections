---
name: molecular-graph-representation-learning
description: Use when when you have molecular structures (SMILES or chemical graphs) from a database like PubChem and need to predict molecular properties (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3372
  - http://edamontology.org/topic_2275
  - http://edamontology.org/topic_0154
  tools:
  - PubChem
  - ms-pred (coleygroup)
  - MAGMa algorithm
  techniques:
  - LC-MS
derived_from:
- doi: 10.1038/s42256-024-00816-8
  title: ICEBERG
evidence_spans:
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

# molecular-graph-representation-learning

## Summary

Learning molecular representations by encoding chemical structures as graphs using graph neural networks (GNNs), enabling end-to-end training on downstream tasks like spectrum prediction. This approach captures atomic connectivity and bond topology to produce learned embeddings suitable for property prediction and molecular comparison.

## When to use

When you have molecular structures (SMILES or chemical graphs) from a database like PubChem and need to predict molecular properties (e.g., tandem mass spectra) in an equivalent-settings comparison framework where all models must use identical covariates and hyperparameter sweeps for fair benchmarking.

## When NOT to use

- Input spectra lack chemical structure information or SMILES annotations—GNN encoding requires explicit graph topology.
- Molecules are too large or have excessive branching that causes memory overflow during graph convolution operations.
- The task does not require cross-model fairness or equivalent-settings comparison; simpler FFN or template-based methods may suffice.

## Inputs

- molecular structures (SMILES strings or chemical graphs)
- experimental mass spectra with chemical formula and collision energy annotations
- molecule–spectrum training/validation/test splits
- hyperparameter configuration (learning rate, batch size, number of GNN layers, hidden dimensions)

## Outputs

- trained GNN encoder model weights
- learned molecular representations (embedding vectors)
- spectrum predictions (m/z and intensity values)
- evaluation metrics (top-1 retrieval accuracy, prediction error distributions)
- comparison statistics versus FFN and other baseline encoders

## How to apply

Load molecular datasets with associated chemical structures and experimental labels (e.g., mass spectra) from a source like PubChem. Construct a GNN encoder that learns molecular representations directly from chemical graphs by encoding atomic features and bond connectivity. Train the GNN encoder end-to-end on the spectrum prediction task using the same dataset splits and hyperparameter configurations applied to all comparison models. During training, ensure consistent feature normalization and optimizer settings across all baseline variants (e.g., FFN and GNN encoders). Evaluate on a held-out test set and compute prediction accuracy and retrieval metrics to validate that the GNN-learned representations are competitive with or superior to alternative encoding schemes.

## Related tools

- **PubChem** (Source of molecular structures, SMILES strings, and chemical metadata for GNN input)
- **ms-pred (coleygroup)** (Reference implementation and benchmark suite for spectrum prediction models with equivalent-settings GNN and FFN encoder comparison) — https://github.com/coleygroup/ms-pred
- **MAGMa algorithm** (Annotates molecular substructures and fragmentation pathways to support GNN training on fragment-level spectrum prediction)

## Examples

```
python src/ms_pred/dag_pred/train_gen.py --config configs/iceberg/iceberg_train_gen.yaml --dataset nist20 --split split_1_rnd1
```

## Evaluation signals

- GNN-encoder model achieves competitive or superior top-1 retrieval accuracy on held-out test set compared to FFN encoder baseline under identical hyperparameter sweeps.
- Learned molecular embeddings cluster chemically similar compounds and separate dissimilar ones, verified by embedding space visualization or nearest-neighbor analysis.
- Prediction error distributions (e.g., cosine similarity between predicted and experimental spectra) are consistent across random seeds and dataset splits.
- Model training converges within expected number of epochs and validation loss plateaus, indicating stable gradient flow through the GNN encoder.
- Ablation studies (e.g., removing GNN layers or changing aggregation functions) show systematic degradation in retrieval metrics, confirming that graph structure is being learned.

## Limitations

- GNN encoders require sufficient GPU memory (≥24 GB tested on NVIDIA A5000) for training on large datasets like NIST'20; smaller GPUs may need reduced batch sizes or skipping of contrastive finetuning.
- Performance depends on the quality and coverage of molecular structures in the input dataset; incomplete or malformed SMILES strings will corrupt graph construction and degrade representation learning.
- GNN encoders are sensitive to hyperparameter choices (number of layers, hidden dimensions, aggregation function); equivalent-settings comparison requires extensive sweeps across all models to avoid unfair benchmarking.
- Contrastive finetuning (e.g., using PubChem-SMILES mappings) is optional but improves retrieval performance; omitting it may reduce downstream accuracy compared to reported baselines.

## Evidence

- [other] construct_gnn: "Construct a graph neural network (GNN) encoder to learn molecular representations from chemical graphs."
- [other] equivalent_settings: "NEIMS baseline is implemented with both FFN and GNN encoder variants as part of an equivalent-settings comparison framework where all models use the same covariates and hyperparameter sweeps."
- [other] end_to_end_training: "Train the GNN encoder end-to-end on the spectrum prediction task using the dataset split and hyperparameters specified for the baseline comparison."
- [other] evaluation_metrics: "Evaluate the trained GNN-encoder NEIMS model on the held-out test set, computing prediction accuracy and comparison metrics against ms-pred reference results."
- [readme] pubchem_source: "Load the molecular dataset and chemical structures from PubChem with associated experimental mass spectra."
- [readme] gnn_vs_ffn_comparison: "we implement a number of baselines and alternative models using equivalent settings across models (i.e., same covariates, hyperparameter sweeps for each, etc.): 1. *NEIMS* using both FFN and GNN"
- [readme] gpu_memory_requirement: "You need two GPUs with at least 24GB RAM to train ICEBERG (we used NVIDIA A5000 for development)."
