---
name: tandem-mass-spectra-embedding-generation
description: Use when you have tandem mass spectra (in .msp or compatible format) from instruments like Orbitrap, and you need to compute library matching scores, cluster spectra by chemical similarity, or embed spectra into a learned vector space for downstream similarity or clustering tasks.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - Anaconda
  - Git
  - MSBERT
  - PyTorch
  - matchms
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
---

# tandem-mass-spectra-embedding-generation

## Summary

Generate chemically rational embedding vectors from tandem mass spectra (MS/MS) using a pretrained transformer encoder (MSBERT) trained via mask learning and contrastive learning. This skill converts raw or processed MS/MS data into fixed-dimensional representations suitable for library matching, clustering, and structural similarity computation.

## When to use

You have tandem mass spectra (in .msp or compatible format) from instruments like Orbitrap, and you need to compute library matching scores, cluster spectra by chemical similarity, or embed spectra into a learned vector space for downstream similarity or clustering tasks. Use this skill when cosine similarity or other spectral dot-product methods are insufficient or when you need to leverage a learned chemical representation trained on GNPS data.

## When NOT to use

- Input spectra are from instrument types not represented in GNPS Orbitrap training set (model was trained specifically on Orbitrap, not all MS instruments equally).
- You require interpretable per-peak feature importance or peak-by-peak attribution (MSBERT embeddings are latent and not directly interpretable as peak contributions).
- Input is already a pretrained embedding or feature vector; use this skill on raw spectra only.

## Inputs

- tandem mass spectra in .msp format (m/z-intensity pairs with metadata)
- pretrained MSBERT model checkpoint (.pkl file)
- optional: SMILES annotations (extracted from .msp headers)

## Outputs

- embedding vectors (shape [n_spectra, 512], float32)
- pairwise similarity matrix (cosine similarity scores)
- optionally: library matching results (top-k identifications)

## How to apply

Load a pretrained MSBERT model checkpoint (PyTorch .pkl format) initialized with vocabulary size 100002, embedding dimension 512, 6 transformer layers, and 16 attention heads. Parse input MS/MS spectra from .msp files using the provided ProcessMSP utility to extract m/z-intensity pairs and SMILES. Pass the processed spectra through the MSBERT encoder in batches (e.g., batch size 16) to generate embedding vectors. The model automatically performs no masking during inference (masking is only applied during training for contrastive learning pretraining). Validate tensor shapes through the forward pass (input: [batch, spectrum_length] → output: [batch, 512]). Save embeddings as arrays and compute pairwise cosine similarity or other distance metrics for matching or clustering tasks.

## Related tools

- **MSBERT** (Pretrained transformer encoder model that encodes MS/MS spectra into 512-dimensional embeddings via masked reconstruction and contrastive learning) — https://github.com/zhanghailiangcsu/MSBERT
- **PyTorch** (Deep learning framework used to load the model and perform forward inference passes to generate embeddings) — https://pytorch.org/
- **Anaconda** (Python environment manager for creating isolated Python 3.12 environment with dependencies) — https://www.anaconda.com
- **matchms** (Workflow framework for integrating MSBERT similarity computation into spectrum processing pipelines) — https://github.com/zhanghailiangcsu/MSBERT/tree/main/matchms_workflow

## Examples

```
import torch
from model.MSBERTModel import MSBERT
from model.utils import ModelEmbed, ProcessMSP, MSBERTSimilarity
model = MSBERT(100002, 512, 6, 16, 0, 100, 3)
model.load_state_dict(torch.load('model/MSBERT.pkl'))
demo_data, demo_smiles = ProcessMSP('example/demo.msp')
demo_arr = ModelEmbed(model, demo_data, 16)
similarity = MSBERTSimilarity(demo_arr, demo_arr)
```

## Evaluation signals

- Output embedding vectors have shape [n_spectra, 512] and contain no NaN or Inf values.
- Pairwise cosine similarity matrix is symmetric and has diagonal values ≈ 1.0 (self-similarity).
- Top-k library matching accuracy on Orbitrap test set matches reported values: top-1 ≥ 0.7871, top-5 ≥ 0.8950, top-10 ≥ 0.9080.
- Dimensionality reduction (t-SNE or UMAP) of embeddings shows chemical cluster structure; spectra with similar SMILES group together.
- Structural similarity (Tanimoto) computed on Tanimoto fingerprints correlates positively with cosine similarity of MSBERT embeddings (Pearson r > 0.6, indicative of chemical rationality).

## Limitations

- Model was trained exclusively on GNPS Orbitrap dataset; performance on other instrument types (e.g., Q-TOF, TOF-TOF) is not validated and may degrade.
- Embeddings reflect chemical structure information learned from the GNPS training set; novel chemical classes or post-translational modifications not well-represented in GNPS may produce less informative embeddings.
- Input spectra must be cleaned and normalized according to GNPS preprocessing standards (handled by ProcessMSP utility); raw, uncleaned spectra may yield poor embeddings.
- Model hyperparameters (6 transformer layers, 16 attention heads, 512 embedding dim) are fixed in the public checkpoint; retraining on custom data requires access to training script and original contrastive loss implementation.

## Evidence

- [readme] MSBERT used the transformer encoder as the backbone and take advantage of the randomness of the mask to construct positive samples for contrastive learning.: "MSBERT used the transformer encoder as the backbone and take advantage of the randomness of the mask to construct positive samples for contrastive learning."
- [intro] MSBERT achieved top-1, top-5, and top-10 library matching accuracies of 0.7871, 0.8950, and 0.9080 respectively on the Orbitrap test dataset.: "MSBERT had a stronger ability in library matching, with top 1, top5, and top 10 were 0.7871, 0.8950, and 0.9080 on Orbitrap test dataset."
- [intro] Run the model on the test spectra to generate embeddings and perform library matching. Compute top-1, top-5, and top-10 matching accuracies by comparing predicted library identifications against ground truth labels.: "Run the model on the test spectra to generate embeddings and perform library matching. Compute top-1, top-5, and top-10 matching accuracies by comparing predicted library identifications against"
- [readme] Load model with torch.load and ProcessMSP function to process .msp files, then ModelEmbed to generate embedding vectors.: "model = MSBERT(100002, 512, 6, 16, 0,100,3)
model.load_state_dict(torch.load(model_file))
demo_data,demo_smiles = ProcessMSP(demo_file)
demo_arr = ModelEmbed(model,demo_data,16)"
- [readme] The rationality of embedding was demonstrated by reducing the dimensionality of the embedding vectors, calculating structural similarity, and spectra clustering.: "The rationality of embedding was demonstrated by reducing the dimensionality of the embedding vectors, calculating structural similarity, and spectra clustering."
