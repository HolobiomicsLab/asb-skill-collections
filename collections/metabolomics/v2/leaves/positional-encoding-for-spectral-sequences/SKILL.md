---
name: positional-encoding-for-spectral-sequences
description: Use when preparing mass spectrum input tensors for transformer encoder
  layers in IDSL_MINT.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0226
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
  tools:
  - RDKit
  - Python
  - PyTorch
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1186/s13321-024-00804-5
  title: idslmint
evidence_spans:
- Powered by RDKit
- Python versions badge
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_idslmint
    doi: 10.1186/s13321-024-00804-5
    title: idslmint
  dedup_kept_from: coll_idslmint
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-024-00804-5
  all_source_dois:
  - 10.1186/s13321-024-00804-5
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# positional-encoding-for-spectral-sequences

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Positional encoding embeds ordinal and sequential information into mass spectrum m/z-intensity pairs so that transformer self-attention layers can distinguish their position in the spectrum. This is essential for transformer-based MS/MS interpretation, where attention mechanisms otherwise treat all spectrum peaks as an unordered set.

## When to use

Use this skill when preparing mass spectrum input tensors for transformer encoder layers in IDSL_MINT. Specifically, apply positional encoding after vectorizing m/z and intensity features but before passing them through multi-head self-attention blocks, to preserve the sequential structure of spectral peaks and enable the model to learn position-dependent fragmentation patterns.

## When NOT to use

- When spectrum peaks have already been aggregated into a fixed fingerprint or histogram representation — positional encoding assumes sequential peak order.
- When using non-transformer architectures (e.g., CNN, GRU, simple MLPs) that do not rely on multi-head self-attention or that include their own position-aware layers.
- When spectrum data is pre-normalized to a canonical sorted order unrelated to actual peak positions in the acquired spectrum.

## Inputs

- Input spectrum feature tensor (batch_size × num_peaks × feature_dim)
- Model dimension (d_model) — embedding/feature vector size
- Maximum spectrum length (number of peaks)

## Outputs

- Spectrum tensor with positional encoding added (batch_size × num_peaks × feature_dim)
- Positional encoding matrix (num_peaks × feature_dim) for reuse

## How to apply

Positional encoding adds position-dependent sinusoidal signals to each spectrum feature vector at index i. Following the 'Attention is All You Need' paradigm, compute sinusoidal position encodings for each dimension d of the feature vector: PE(pos,2d) = sin(pos / 10000^(2d/d_model)) and PE(pos,2d+1) = cos(pos / 10000^(2d/d_model)). Add these encodings element-wise to the input spectrum embeddings before feeding them into the transformer encoder. This allows the model to infer relative and absolute peak positions within the spectrum, improving its ability to learn position-sensitive fragmentation patterns and peak relationships. The encoding is typically computed once and broadcasted across the batch dimension for efficiency.

## Related tools

- **PyTorch** (Implements multi-head self-attention transformer encoder blocks that consume positionally encoded spectrum tensors; handles tensor operations for sinusoidal encoding computation and broadcasting.) — https://github.com/pytorch/pytorch
- **RDKit** (Generates molecular fingerprints and canonical SMILES from chemical structures that may be correlated with spectral peak positions; supports validation of spectrum-to-structure predictions.) — https://www.rdkit.org/

## Examples

```
import torch; import math; d_model=512; max_len=1000; pos = torch.arange(0, max_len).unsqueeze(1); div_term = torch.exp(torch.arange(0, d_model, 2) * -(math.log(10000.0) / d_model)); pe = torch.zeros(max_len, d_model); pe[:, 0::2] = torch.sin(pos * div_term); pe[:, 1::2] = torch.cos(pos * div_term); spectrum_embedded = spectrum_tensor + pe[:spectrum_tensor.size(1), :].unsqueeze(0)
```

## Evaluation signals

- Positional encoding tensor has shape (num_peaks, d_model) with sinusoidal values bounded to [-1, 1]; no NaN or Inf values present.
- After addition to input embeddings, output tensor shape is preserved (batch_size × num_peaks × feature_dim) with numerical stability maintained (no overflow or underflow).
- Visualization or inspection of encoding matrix shows periodic sinusoidal patterns with different frequencies across dimensions, confirming correct computation of PE(pos, 2d) and PE(pos, 2d+1) terms.
- Transformer model forward pass completes without shape mismatch or gradient computation errors when positional encoding is included in the input pipeline.
- Ablation study (comparison of model with and without positional encoding) shows improvement in prediction accuracy for fingerprints, SMILES, or MS/MS spectra, indicating that position information is leveraged by the model.

## Limitations

- Sinusoidal positional encoding assumes a fixed maximum sequence length during training; spectra longer than the training maximum may require interpolation or truncation.
- Encoding is absolute (tied to input position indices) rather than relative; does not capture physical m/z distance between peaks, only ordinal sequence.
- The 'Attention is All You Need' formulation uses fixed sinusoidal encoding; learned or relative positional encodings may offer better performance for mass spectra but are not discussed in the IDSL_MINT README.
- Positional encoding alone does not account for m/z and intensity scales; preprocessing (normalization, scaling) of spectrum features is still required for stable training.

## Evidence

- [other] Implement positional encoding for the input spectrum features.: "Implement positional encoding for the input spectrum features."
- [readme] transformer models delineated in the seminal paper, 'Attention is all you need': "constructed upon the transformer models delineated in the seminal paper, [*'Attention is all you need'*]"
- [other] multi-head self-attention and feed-forward layers following the 'Attention is All You Need' paradigm: "Define the transformer encoder architecture with multi-head self-attention and feed-forward layers following the 'Attention is All You Need' paradigm."
- [other] Create a PyTorch module that stacks transformer encoder blocks.: "Create a PyTorch module that stacks transformer encoder blocks."
- [other] Verify output tensor shape and numerical stability (no NaN or Inf values).: "Verify output tensor shape and numerical stability (no NaN or Inf values)."
