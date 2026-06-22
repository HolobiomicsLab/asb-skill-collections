---
name: mass-spectra-embedding-extraction
description: Use when you have tandem mass spectra (MS/MS) in .msp format and need dense, chemically meaningful vector representations for library matching, similarity computation, or structural clustering. Apply this when comparing spectra across large reference databases (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - Anaconda
  - Git
  - MSBERT
  - PyTorch
  - ProcessMSP
  - ModelEmbed
  - MSBERTSimilarity
  - matchms
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.4c02426
  title: MSBERT
evidence_spans:
- '[Anaconda](https://www.anaconda.com) for Python 3.12'
- Install [Git](https://git-scm.com/downloads)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_msbert_cq
    doi: 10.1021/acs.analchem.4c02426
    title: MSBERT
  dedup_kept_from: coll_msbert_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c02426
  all_source_dois:
  - 10.1021/acs.analchem.4c02426
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Mass spectra embedding extraction

## Summary

Extract dense vector embeddings from tandem mass spectra using a pre-trained MSBERT transformer model trained on mask learning and contrastive learning. These embeddings encode chemical rationality and enable downstream library matching, similarity scoring, and structural clustering of MS/MS data.

## When to use

You have tandem mass spectra (MS/MS) in .msp format and need dense, chemically meaningful vector representations for library matching, similarity computation, or structural clustering. Apply this when comparing spectra across large reference databases (e.g., GNPS) or when cosine similarity on raw peaks is insufficient for your matching or discovery task.

## When NOT to use

- Input spectra lack metadata or are severely fragmented (embedding quality depends on sufficient and consistent peak patterns)
- You require real-time or on-device inference on very large datasets without GPU acceleration (model inference is memory-intensive for batch processing)
- Your task requires interpretable peak-level attribution rather than holistic spectrum similarity (embeddings are learned representations, not rule-based features)

## Inputs

- tandem mass spectra in .msp format (ion m/z and intensity pairs with metadata)
- pre-trained MSBERT model checkpoint (PyTorch .pkl file)

## Outputs

- embedding vectors (512-dimensional dense float arrays per spectrum)
- pairwise cosine similarity matrix (spectrum-to-spectrum scores)
- structured array suitable for downstream clustering or dimensionality reduction

## How to apply

Load the pre-trained MSBERT model checkpoint (MSBERT.pkl) using PyTorch, parse your MS/MS data from .msp format using the ProcessMSP utility, and pass the processed spectra through the MSBERT encoder to obtain fixed-dimensional embedding vectors (512 dimensions in the reference model). The model uses a transformer encoder backbone with 6 layers and 16 attention heads. Feed embeddings in batches (batch size 16 in examples) to ModelEmbed for efficient extraction. The resulting embeddings can then be compared using cosine similarity (MSBERTSimilarity) or subjected to dimensionality reduction (t-SNE, UMAP) and clustering (k-means, hierarchical) to validate chemical coherence.

## Related tools

- **MSBERT** (pre-trained transformer model for embedding tandem mass spectra into chemically rational space) — https://github.com/zhanghailiangcsu/MSBERT
- **PyTorch** (deep learning framework for loading and executing the MSBERT transformer model) — https://pytorch.org/
- **ProcessMSP** (utility to parse and preprocess .msp mass spectrum files into model-ready format) — https://github.com/zhanghailiangcsu/MSBERT
- **ModelEmbed** (wrapper function to batch-process spectra through the model and extract embedding vectors) — https://github.com/zhanghailiangcsu/MSBERT
- **MSBERTSimilarity** (compute pairwise cosine similarity between embedding vectors for spectrum matching) — https://github.com/zhanghailiangcsu/MSBERT
- **matchms** (workflow framework for integrating MSBERT similarity calculation into spectral processing pipelines) — https://github.com/zhanghailiangcsu/MSBERT/tree/main/matchms_workflow

## Examples

```
import torch
from model.MSBERTModel import MSBERT
from model.utils import ModelEmbed, ProcessMSP
model = MSBERT(100002, 512, 6, 16, 0, 100, 3)
model.load_state_dict(torch.load('model/MSBERT.pkl'))
demo_data, demo_smiles = ProcessMSP('example/demo.msp')
demo_arr = ModelEmbed(model, demo_data, 16)
```

## Evaluation signals

- Embedding vectors have correct dimensionality (512 floats) and are non-zero and finite
- Cosine similarity scores between spectra fall in the valid range [−1, 1] with expected distribution (MSBERT achieved top-1 matching accuracy of 0.7871 on Orbitrap test data, significantly outperforming Spec2Vec and raw cosine similarity)
- Dimensionality-reduced embeddings (t-SNE/UMAP 2D/3D projections) show spatial clustering that aligns with known chemical families or structural classes in GNPS annotations
- Spectral clustering (k-means or hierarchical) produces coherent groups validated against reference chemical classifications, confirming 'rationality' of the embedding space
- Library matching performance: top-1, top-5, top-10 retrieval rates meet or exceed reported benchmarks (0.7871, 0.8950, 0.9080 on Orbitrap data)

## Limitations

- Model was trained exclusively on the GNPS dataset filtered by instrument type; performance on out-of-distribution spectra (e.g., different instruments or ionization modes not well-represented in GNPS) is not quantified
- Embedding extraction requires GPU-accelerated PyTorch for practical batch processing; CPU-only inference is substantially slower
- The 512-dimensional embedding space is learned and opaque; no peak-level interpretability or feature attribution is provided
- No changelog or versioning scheme documented; model updates or retraining procedures not explicitly versioned

## Evidence

- [readme] MSBERT based on mask learning and contrastive learning was proposed to get a reasonable embedding representation of MS/MS.: "MSBERT based on mask learning and contrastive learning was proposed to get a reasonable embedding representation of MS/MS."
- [intro] Load pre-trained MSBERT embedding vectors from the model checkpoint, apply dimensionality reduction, compute pairwise structural similarity, and perform spectral clustering.: "1. Load pre-trained MSBERT embedding vectors from the model checkpoint. 2. Apply dimensionality reduction (t-SNE or UMAP) to project high-dimensional embeddings into 2D or 3D space for visualization."
- [readme] MSBERT had a stronger ability in library matching, with top 1, top5, and top 10 were 0.7871, 0.8950, and 0.9080 on Orbitrap test dataset.: "MSBERT had a stronger ability in library matching, with top 1, top5, and top 10 were 0.7871, 0.8950, and 0.9080 on Orbitrap test dataset."
- [readme] The rationality of embedding was demonstrated by reducing the dimensionality of the embedding vectors, calculating structural similarity, and spectra clustering.: "The rationality of embedding was demonstrated by reducing the dimensionality of the embedding vectors, calculating structural similarity, and spectra clustering."
- [readme] model = MSBERT(100002, 512, 6, 16, 0,100,3); demo_arr = ModelEmbed(model,demo_data,16): "model = MSBERT(100002, 512, 6, 16, 0,100,3); demo_arr = ModelEmbed(model,demo_data,16)"
