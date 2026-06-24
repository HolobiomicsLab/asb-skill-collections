---
name: virtual-screening-ranking
description: Use when you have a library of natural product compounds (encoded as
  SMILES strings) and wish to rank them by predicted bioactivity or fitness for a
  downstream task.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3572
  - http://edamontology.org/topic_0209
  tools:
  - PyTorch
  - Git
  - inference.py
  - PyTorch Geometric (PyG)
  license_tier: restricted
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# virtual-screening-ranking

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Apply a pre-trained natural product foundation model to rank and prioritize compounds in virtual screening campaigns, generating molecular embeddings and bioactivity predictions to identify novel bioactive natural product candidates. This skill leverages NaFM's learned evolutionary patterns to evaluate screening compound libraries against target properties.

## When to use

You have a library of natural product compounds (encoded as SMILES strings) and wish to rank them by predicted bioactivity or fitness for a downstream task. Virtual screening is the appropriate choice when you need to prioritize computational exploration of large natural product libraries before experimental validation, particularly when models pre-trained on synthetic molecules have failed to capture synthesis patterns or when you require predictions grounded in evolutionary and taxonomic structure.

## When NOT to use

- Your compounds are synthetic molecules with no natural product context; models pre-trained on synthetic data may be more appropriate.
- Your screening library has already been experimentally validated and ranked; use this skill only to prioritize unscreened or weakly characterized compounds.
- You require sub-millisecond latency or have hardware constraints incompatible with PyTorch/GPU inference.

## Inputs

- Pre-trained NaFM checkpoint (.ckpt file)
- Compound library CSV with 'SMILES' column
- Optional: ground-truth bioactivity labels for validation

## Outputs

- Predictions CSV (NaFM/predictions.csv) with ranked compounds and predicted scores
- Molecular embeddings (1024-dimensional vectors per compound)
- Ranking metrics (hit rate, retrieval accuracy, or other screening performance statistics)

## How to apply

Load the pre-trained NaFM checkpoint and your compound library (a CSV file with a 'SMILES' column). Run the inference.py script with task='classification' or task='regression' depending on your target property (taxonomy class or bioactivity value). The model will generate molecular embeddings via masked graph modeling and contrastive learning, encoding scaffold-derived evolutionary patterns and side-chain diversity. Compute ranking metrics (e.g., retrieval accuracy, hit rates, or ranking scores) by comparing predicted rankings against ground-truth bioactivity labels or experimental validation results if available. Save predictions to output CSV for downstream analysis. Parameters like embedding dimension (default 1024) and number of layers (default 6) can be adjusted if finetuning on task-specific data; for inference on pre-trained weights, use defaults unless the model was explicitly retrained.

## Related tools

- **PyTorch** (Deep learning framework for loading pre-trained NaFM model, computing embeddings, and inference)
- **inference.py** (NaFM inference script that applies the pre-trained model to new SMILES and generates predictions) — https://github.com/TomAIDD/NaFM-Official
- **PyTorch Geometric (PyG)** (Graph neural network library for masked graph modeling and molecular representation learning)

## Examples

```
python inference.py --task regression --downstream-data screening_compounds.csv --checkpoint-path NaFM.ckpt
```

## Evaluation signals

- Predictions CSV is non-empty, contains all input compounds, and has numeric scores in a plausible range (e.g., 0–1 for classification confidence or biochemically meaningful values for regression bioactivity).
- Ranking order matches or exceeds reported hit rates and retrieval accuracy in the paper when evaluated against known natural product bioactivity benchmarks (Ontology, Regression, Lotus, or External datasets).
- Molecular embeddings have expected dimensionality (1024-D by default) and pass validation that compounds with similar SMILES scaffolds have higher cosine similarity in embedding space.
- Inference completes without crashes and logs confirm model weights were loaded from the checkpoint file.
- Predictions for compounds not seen during pretraining show diversity and are not dominated by a single class or score value, indicating meaningful learned patterns rather than memorization.

## Limitations

- The model is specialized for natural products; performance on synthetic or semi-synthetic compounds may degrade or be inferior to synthetic-molecule baselines.
- Virtual screening predictions are computational approximations; experimental validation is required to confirm bioactivity predictions before resource-intensive synthesis or assays.
- The README notes that test.py is a 'minimal demonstration template rather than the exact production evaluation pipeline' used to generate benchmark results, so inference outputs should be calibrated against original benchmark datasets if absolute performance is critical.
- Hyperparameters such as learning rate, batch size, and early stopping patience may require tuning for downstream tasks; default config is provided but may need adjustment for your specific dataset.
- SMILES must be valid and standardized; the repository's filter.py script removes salts and duplicates, but input quality depends on upstream data preparation.

## Evidence

- [abstract] Apply NaFM to virtual screening tasks, showing its potential to provide meaningful molecular representations and facilitate the discovery of novel bioactive compounds.: "Finally, we apply NaFM to virtual screening tasks, showing its potential to provide meaningful molecular representations and facilitate the discovery of novel bioactive compounds"
- [intro] The proposed framework achieves state-of-the-art performance across a wide range of downstream tasks in natural product mining and drug discovery.: "The proposed framework achieves state-of-the-art (SOTA) performance across a wide range of downstream tasks in natural product mining and drug discovery"
- [intro] Integration of contrastive learning with masked graph modeling encodes scaffold-derived evolutionary patterns and side-chain information.: "Our method integrates contrastive learning with masked graph modeling, effectively encoding scaffold-derived evolutionary patterns alongside diverse side-chain information"
- [readme] For inference on new molecules, run the inference script with CSV input containing a SMILES column and save results to predictions.csv.: "For inference on new molecules (CSV with a "SMILES" column): python inference.py --task classification --downstream-data [data location] --checkpoint-path [your finetuned model path]. Results will be"
- [other] Compute screening performance metrics including ranking, retrieval accuracy, and hit rates as reported in the paper.: "Compute screening performance metrics (e.g., ranking, retrieval accuracy, or hit rates as reported in the paper)"
