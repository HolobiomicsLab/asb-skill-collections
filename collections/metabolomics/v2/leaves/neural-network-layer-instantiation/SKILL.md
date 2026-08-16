---
name: neural-network-layer-instantiation
description: Use when when you have a neural network layer definition (parameters,
  weight initialization, embedding dimension) from a trained or pretrained model checkpoint
  and need to generate embeddings or activations for a new batch of chemical formulas
  or spectrum fragments.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3372
  tools:
  - MIST
  - SCARF
  - MIST-CF
  - PyTorch
  license_tier: open
derived_from:
- doi: 10.1021/acs.jcim.3c01082
  title: mistcf
evidence_spans:
- an extension of MIST for annotating MS1 precursor masses from MS/MS data
- Utilizing sinusoidal formula embeddings as developed in our previous work SCARF
- MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum
  using an end-to-end energy based modeling approach
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mistcf
    doi: 10.1021/acs.jcim.3c01082
    title: mistcf
  dedup_kept_from: coll_mistcf
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jcim.3c01082
  all_source_dois:
  - 10.1021/acs.jcim.3c01082
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Neural Network Layer Instantiation

## Summary

Instantiate a configured neural network layer (e.g., sinusoidal formula embeddings) with its specified dimensionality and invoke its forward pass on a batch of input data to produce learned representations. This skill is essential for setting up transformer and deep learning components that encode domain-specific inputs (chemical formulas, mass spectra features) into continuous vector spaces for downstream model tasks.

## When to use

When you have a neural network layer definition (parameters, weight initialization, embedding dimension) from a trained or pretrained model checkpoint and need to generate embeddings or activations for a new batch of chemical formulas or spectrum fragments. Specifically apply this when reproducing transformer-based feature extraction (as in MIST-CF's sinusoidal formula embeddings derived from SCARF) or validating that a layer implementation matches reference outputs.

## When NOT to use

- Layer weights or configuration are not available or not documented—you cannot instantiate from scratch without hyperparameters or pretrained weights.
- Input data format does not match the expected tokenization or encoding scheme for the layer (e.g., raw SMILES strings instead of atom-level token IDs).
- The downstream task requires only formula ranking or adduct assignment scores, not intermediate learned representations—use the full model's predict method instead of extracting individual layer outputs.

## Inputs

- Layer configuration dictionary (embedding_dim, initialization parameters)
- Pretrained model checkpoint or weight file
- Batch of encoded chemical formula representations (token IDs, atom counts, or structural descriptors)
- Input tensor with shape (batch_size, sequence_length) or (batch_size, formula_feature_dim)

## Outputs

- Embedding vectors with shape (batch_size, sequence_length, embedding_dim) or (batch_size, embedding_dim)
- Structured file (JSON, CSV, HDF5) containing embedding vectors and validation metrics
- Validation report with L2 distances from reference outputs and range statistics

## How to apply

Obtain the layer configuration (embedding dimension, initialization scheme) from the model checkpoint or source code. Instantiate the layer with these parameters, ensuring the framework (PyTorch, TensorFlow) and device (CPU/GPU) are set correctly. Prepare input data in the expected format—for sinusoidal formula embeddings, this is encoded chemical formula tokens or atom counts. Call the layer's forward method on the input batch to compute embedding vectors. Verify output dimensionality matches the configured embedding_dim parameter and that numerical values fall within the expected range (typically [-1, 1] for sinusoidal embeddings). Compare outputs against reference embeddings from the official repository using a numerical tolerance (e.g., L2 distance < 1e-6) to confirm reproducibility and correct implementation.

## Related tools

- **MIST-CF** (Source model containing the sinusoidal formula embedding layer to be instantiated and evaluated) — https://github.com/samgoldman97/mist-cf
- **SCARF** (Prior work defining sinusoidal formula embedding technique adopted by MIST-CF) — https://arxiv.org/abs/2303.06470
- **PyTorch** (Framework for instantiating and executing neural network layers)

## Examples

```
from mist_cf.models import MistCFModel; model = MistCFModel.load_checkpoint('pretrained_mist_cf.ckpt'); embeddings = model.formula_embedding(formula_tokens); assert embeddings.shape == (batch_size, seq_len, embedding_dim) and embeddings.min() >= -1.0 and embeddings.max() <= 1.0
```

## Evaluation signals

- Output embedding tensor dimensionality equals configured embedding_dim parameter (e.g., shape is [batch_size, sequence_length, 512])
- All embedding values fall within expected numerical range; for sinusoidal embeddings, verify min/max values are within [-1, 1]
- L2 distance between produced embeddings and reference outputs from the official MIST-CF repository is below numerical tolerance threshold (< 1e-6)
- Embedding vectors are non-zero and exhibit expected statistical properties (e.g., mean near 0, standard deviation consistent with sinusoidal initialization)
- Forward pass completes without numerical errors (NaN, Inf) and memory footprint is consistent with (batch_size × sequence_length × embedding_dim) tensor size

## Limitations

- Sinusoidal formula embeddings are specialized to chemical formula tokens; applying this layer to non-chemistry sequential data (e.g., raw mass-to-charge ratios without formula context) will produce meaningless embeddings.
- The layer assumes input chemical formulas have been correctly encoded (e.g., as token IDs from a predefined vocabulary); malformed or out-of-vocabulary inputs will not be detected at instantiation and will produce corrupted embeddings.
- Reference outputs for validation are only available from the official MIST-CF repository (samgoldman97/mist-cf); reproducing embeddings from other implementations or frameworks may differ due to floating-point precision, random seed differences, or initialization scheme variations.
- The embedding layer depends on the correct device placement (CPU vs GPU); instantiating on a different device than the checkpoint was saved for may cause dtype or shape mismatches.

## Evidence

- [other] Instantiate the sinusoidal embedding layer with its configured dimensionality and invoke the forward pass on each formula to produce embedding vectors.: "Instantiate the sinusoidal embedding layer with its configured dimensionality and invoke the forward pass on each formula to produce embedding vectors."
- [other] Verify embedding vector dimensionality matches the configured embedding dimension parameter and verify all embedding values fall within the expected numerical range (typically [-1, 1] for sinusoidal embeddings).: "Verify embedding vector dimensionality matches the configured embedding dimension parameter. 5. Verify all embedding values fall within the expected numerical range (typically [-1, 1] for sinusoidal"
- [other] Compare produced embeddings against reference outputs from the MIST-CF repository using numerical tolerance to confirm reproducibility.: "Compare produced embeddings against reference outputs from the MIST-CF repository using numerical tolerance (e.g., L2 distance < 1e-6) to confirm reproducibility."
- [other] MIST-CF incorporates sinusoidal formula embeddings, a technique developed in prior work (SCARF), as an advance to the chemical formula transformer architecture.: "MIST-CF incorporates sinusoidal formula embeddings, a technique developed in prior work (SCARF), as an advance to the chemical formula transformer architecture for improved representation of chemical"
- [readme] Utilizing sinusoidal formula embeddings as developed in our previous work SCARF.: "Utilizing sinusoidal *formula* embeddings as developed in our previous work [SCARF](https://arxiv.org/abs/2303.06470)"
