---
name: spectral-tensor-representation-and-preprocessing
description: 'Use when when preparing MS/MS spectra from .msp files for transformer-based deep learning models in IDSL_MINT. Specifically: you have raw spectral data with variable peak counts and need fixed-size tensor inputs;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3474
  tools:
  - RDKit
  - Python
  - PyTorch
  - IDSL_MINT
  techniques:
  - tandem-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-tensor-representation-and-preprocessing

## Summary

Convert mass spectrometry MS/MS spectral peak data into fixed-dimension tensor representations suitable for transformer model input, with positional encoding of spectrum features. This preprocessing step bridges raw .msp spectral records into PyTorch-compatible numerical formats that preserve peak intensity and m/z relationships.

## When to use

When preparing MS/MS spectra from .msp files for transformer-based deep learning models in IDSL_MINT. Specifically: you have raw spectral data with variable peak counts and need fixed-size tensor inputs; you intend to train or perform inference with a transformer encoder that expects positional information; and your downstream task is molecular fingerprint prediction, canonical SMILES generation, or reverse spectrum prediction from molecular descriptors.

## When NOT to use

- Input spectra are already in pre-computed tensor or deep learning-ready format (e.g., pre-extracted embeddings).
- Your analysis goal does not require transformer model input (e.g., simple spectral similarity search, direct library matching, or classical fingerprinting without neural networks).
- Peak intensity values are missing, malformed, or cannot be reliably normalized to a bounded range.

## Inputs

- .msp spectral blocks with PrecursorMZ, Num Peaks, and peak m/z–intensity pairs
- Raw peak lists (m/z and intensity columns)
- Spectral dataset parameters: maximum peak count threshold, intensity normalization strategy

## Outputs

- PyTorch tensors with shape [batch_size, num_peaks, embedding_dim] ready for transformer encoder
- Positionally-encoded spectrum feature tensors
- Fixed-dimension tensor representations of variable-length spectra

## How to apply

Extract m/z and intensity pairs from .msp file entries (identified by PrecursorMZ row and Num Peaks/spectrum block structure). Normalize intensities (e.g., by maximum peak intensity) to [0, 1] range or similar bounded scale. Construct a 2D array where each row is a peak (m/z, normalized intensity). Apply positional encoding to each peak position using sinusoidal functions (as per 'Attention is All You Need' paradigm) to encode ordinal peak position information. Pad or truncate the peak array to a fixed maximum dimension (e.g., max peaks observed in training set) to produce a uniform tensor shape. Stack encoded peaks with their positional encodings along the feature dimension. Convert to PyTorch tensor format with appropriate dtype (float32) and shape [batch_size, num_peaks, feature_dim] for transformer encoder input.

## Related tools

- **PyTorch** (Construct and manipulate tensor representations; build transformer encoder blocks; manage batch processing and GPU device allocation) — https://github.com/pytorch
- **RDKit** (Parse canonical SMILES and InChI entries from .msp files to validate molecular metadata and support downstream fingerprint/structure prediction) — https://www.rdkit.org
- **IDSL_MINT** (Integrated framework managing .msp file parsing, YAML configuration, and end-to-end transformer training/inference pipeline leveraging preprocessed tensors) — https://github.com/idslme/IDSL_MINT

## Examples

```
# Example: preprocess .msp spectra into tensors for IDSL_MINT training
MINT_workflow --yaml MINT_MS2FP_trainer.yaml  # YAML file configures preprocessing, tensor dimensions, and positional encoding
```

## Evaluation signals

- Output tensor shape matches expected [batch_size, num_peaks, embedding_dim] with no dimension mismatches or broadcast errors.
- No NaN or Inf values in output tensor; all values in bounded range (e.g., [0, 1] for normalized intensities; reasonable positional encoding magnitudes).
- Positional encoding values vary smoothly across peak positions and frequency dimensions (sine/cosine patterns visible upon inspection).
- Fixed-dimension padding preserves spectral information order (peaks remain in ascending m/z order post-padding) and does not corrupt peak identity.
- Batch processing maintains consistent tensor shapes across all samples in a batch despite variable raw peak counts.

## Limitations

- Fixed maximum peak dimension may truncate spectra with more peaks than the selected threshold, losing high-mass fragments or low-intensity noise.
- Padding with zeros or masking tokens can introduce artificial features; downstream transformer attention may learn spurious patterns from padding boundaries.
- Intensity normalization method (e.g., max normalization vs. sum normalization vs. log-scale) affects relative peak emphasis; choice should match training data preprocessing and be consistent across train/test splits.
- Positional encoding assumes peak order significance; reordering peaks (e.g., by intensity) alters model input semantics and may reduce performance if training assumed m/z ordering.
- Variable-length spectra in small datasets may not span the full dynamic range of the fixed tensor dimension, reducing effective model capacity utilization.

## Evidence

- [other] 1. Define the transformer encoder architecture with multi-head self-attention and feed-forward layers following the 'Attention is All You Need' paradigm. 2. Implement positional encoding for the input spectrum features.: "Implement positional encoding for the input spectrum features."
- [readme] This innovative approach for mass spectrometry data processing has been constructed upon the transformer models delineated in the seminal paper, 'Attention is all you need'.: "constructed upon the transformer models delineated in the seminal paper, 'Attention is all you need'."
- [other] 4. Generate or load a representative mass spectrum input tensor with appropriate dimensions. 5. Instantiate the model with declared hyperparameters and initialize weights.: "Generate or load a representative mass spectrum input tensor with appropriate dimensions."
- [readme] Compatibility with *.msp* file formats.: "Compatibility with *.msp* file formats."
- [readme] MSP blocks must include `PrecursorMZ: ` row entries.: "MSP blocks must include `PrecursorMZ: ` row entries."
