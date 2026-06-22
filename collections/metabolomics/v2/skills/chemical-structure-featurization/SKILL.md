---
name: chemical-structure-featurization
description: Use when when you have molecular structures (SMILES, SDF, or molecular graphs) and need to train a spectrum prediction or molecular property model, and you want to learn task-specific representations rather than use fixed descriptors.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3680
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3307
  - http://edamontology.org/topic_3372
  - http://edamontology.org/topic_0091
  tools:
  - PubChem
  - ms-pred (coleygroup)
  - NEIMS
  - RDKit
derived_from:
- doi: 10.1038/s42256-024-00816-8
  title: ICEBERG
- doi: 10.1021/acs.analchem.3c05019
  title: ''
evidence_spans:
- By inputting the chemical formula and your experimental spectrum, the WebUI will rank it against all candidates from PubChem.
- the WebUI will rank it against all candidates from PubChem
- jhhung/PS2MS
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_iceberg_cq
    doi: 10.1038/s42256-024-00816-8
    title: ICEBERG
  - build: coll_ps2ms
    doi: 10.1021/acs.analchem.3c05019
    title: ps2ms
  dedup_kept_from: coll_iceberg_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s42256-024-00816-8
  all_source_dois:
  - 10.1038/s42256-024-00816-8
  - 10.1021/acs.analchem.3c05019
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# chemical-structure-featurization

## Summary

Convert molecular chemical structures into learned numerical representations using graph neural network (GNN) encoders that capture connectivity and atomic properties for downstream prediction tasks like mass spectrum forecasting. This approach replaces hand-crafted molecular fingerprints with end-to-end learned embeddings optimized for the target task.

## When to use

When you have molecular structures (SMILES, SDF, or molecular graphs) and need to train a spectrum prediction or molecular property model, and you want to learn task-specific representations rather than use fixed descriptors. Use this skill when comparing multiple models under equivalent settings to ensure fair performance comparison with the same learned feature space.

## When NOT to use

- Input structures are already pre-computed fixed molecular fingerprints or descriptor tables—use the GNN only if you have raw molecular graphs or SMILES.
- You need interpretable hand-crafted features for regulatory or transparency reasons; GNN embeddings are learned latent representations and not directly human-interpretable.
- Computational budget is extremely constrained; GNN training and inference are more expensive than fixed fingerprint lookups.

## Inputs

- molecular structures in SDF or SMILES format
- chemical graphs with atomic types and bond connectivity
- training dataset with molecular structures and target labels (e.g., experimental mass spectra)
- train/test split indices

## Outputs

- trained GNN encoder weights
- learned molecular embeddings (vector representations)
- end-to-end trained spectrum prediction model
- prediction accuracy and comparison metrics vs. reference baselines

## How to apply

Load molecular chemical structures from PubChem or your dataset in SDF format and convert to graph representations. Construct a GNN encoder (e.g., message-passing neural network) to process the molecular graph and learn node/graph-level embeddings. Train the GNN encoder end-to-end jointly with the downstream prediction head (e.g., spectrum prediction) using your dataset split and hyperparameter sweep. The learned embeddings automatically capture atomic connectivity, valence, and task-relevant substructural patterns. Evaluate by comparing prediction accuracy against fixed-feature baselines (e.g., FFN encoders with hand-crafted covariates) on the same test set; superior performance of the learned GNN representation indicates effective task-specific featurization.

## Related tools

- **PubChem** (source of molecular chemical structures and structures dataset in SDF format)
- **ms-pred (coleygroup)** (reference implementation of GNN encoder variants (FFN and GNN) for spectrum prediction baseline comparison) — https://github.com/coleygroup/ms-pred
- **NEIMS** (baseline model providing both FFN and GNN encoder implementations for equivalent-settings comparison)

## Examples

```
python src/ms_pred/dag_pred/train_gen.py --dataset nist20 --model iceberg --encoder gnn --batch_size 32 --num_epochs 100
```

## Evaluation signals

- GNN-encoder model achieves higher prediction accuracy or comparable performance to fixed-feature FFN baseline on held-out test set
- Learned embeddings cluster chemically similar molecules together in embedding space (visualizable via t-SNE or UMAP)
- Model weights are saved and reproducible; predictions match across multiple runs with same random seed
- Comparison metrics (e.g., top-1 retrieval accuracy, spectrum prediction loss) are computed and reported against ms-pred reference results on the same test partition
- Hyperparameter sweep for GNN (learning rate, hidden dimension, message-passing layers) covers the same range as FFN baseline to ensure fair comparison

## Limitations

- GNN requires large training datasets and computational resources (GPUs with ≥24 GB RAM recommended); performance may degrade on small datasets due to overfitting.
- GNN embeddings are not interpretable in the way hand-crafted descriptors are; understanding which structural features drive predictions requires additional attention mechanism or gradient-based analysis.
- Performance depends critically on graph construction (bond types, aromaticity perception, 3D conformation handling); errors in SDF parsing or chemical sanitization propagate to learned representations.
- Training time is significantly longer than fixed-feature baselines; end-to-end optimization across encoder and prediction head requires careful hyperparameter tuning and multiple runs for statistical significance.

## Evidence

- [other] Construct a graph neural network (GNN) encoder to learn molecular representations from chemical graphs.: "Construct a graph neural network (GNN) encoder to learn molecular representations from chemical graphs."
- [other] NEIMS baseline is implemented with both FFN and GNN encoder variants as part of an equivalent-settings comparison framework where all models use the same covariates and hyperparameter sweeps.: "NEIMS baseline is implemented with both FFN and GNN encoder variants as part of an equivalent-settings comparison framework where all models use the same covariates and hyperparameter sweeps."
- [other] Load the molecular dataset and chemical structures from PubChem with associated experimental mass spectra.: "Load the molecular dataset and chemical structures from PubChem with associated experimental mass spectra."
- [other] Train the GNN encoder end-to-end on the spectrum prediction task using the dataset split and hyperparameters specified for the baseline comparison.: "Train the GNN encoder end-to-end on the spectrum prediction task using the dataset split and hyperparameters specified for the baseline comparison."
- [other] Evaluate the trained GNN-encoder NEIMS model on the held-out test set, computing prediction accuracy and comparison metrics against ms-pred reference results.: "Evaluate the trained GNN-encoder NEIMS model on the held-out test set, computing prediction accuracy and comparison metrics against ms-pred reference results."
- [readme] ICEBERG predicts spectra at the level of molecular fragments, whereas SCARF predicts spectra at the level of chemical formula.: "ICEBERG predicts spectra at the level of molecular fragments, whereas SCARF predicts spectra at the level of chemical formula."
- [readme] You need two GPUs with at least 24GB RAM to train ICEBERG (we used NVIDIA A5000 for development).: "You need two GPUs with at least 24GB RAM to train ICEBERG (we used NVIDIA A5000 for development)."
