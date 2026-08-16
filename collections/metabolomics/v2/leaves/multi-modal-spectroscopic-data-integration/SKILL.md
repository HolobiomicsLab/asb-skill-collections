---
name: multi-modal-spectroscopic-data-integration
description: Use when you have acquired complementary spectroscopic measurements (NMR,
  HSQC, COSY, IR) for the same molecular sample and need to combine them for structure
  elucidation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_3169
  tools:
  - MultiModalSpectralTransformer
  - SGNN (Spectral Graph Neural Network)
  - Chemprop-IR
  - RDKit
  techniques:
  - NMR
  license_tier: restricted
derived_from:
- doi: 10.1002/ange.202517611
  title: MMST
- doi: 10.5281/zenodo.14712886
  title: ''
evidence_spans:
- github.com/mpriessner/MultiModalSpectralTransformer
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mmst_cq
    doi: 10.1002/ange.202517611
    title: MMST
  dedup_kept_from: coll_mmst_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1002/ange.202517611
  all_source_dois:
  - 10.1002/ange.202517611
  - 10.5281/zenodo.14712886
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# multi-modal-spectroscopic-data-integration

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Integrate heterogeneous spectroscopic modalities (NMR, HSQC, COSY, IR) into a unified transformer-based input representation for automated molecular structure prediction. This skill bridges disparate spectral formats and measurement domains into a common learned feature space.

## When to use

You have acquired complementary spectroscopic measurements (NMR, HSQC, COSY, IR) for the same molecular sample and need to combine them for structure elucidation. Use this skill when single modalities are insufficient for disambiguation and you require joint inference across all available spectra; do not use if only one spectroscopic modality is available or if spectra come from different molecules.

## When NOT to use

- Input is only a single spectroscopic modality (e.g., 1H NMR alone); use single-modality models instead.
- Spectroscopic data comes from different molecular samples or compound classes; integration assumes spectra are from the same unknown.
- Spectra have not been preprocessed to common coordinate systems (e.g., unaligned ppm scales or wavenumber bins); preprocessing must precede integration.

## Inputs

- NMR spectral data (1D 1H or 13C NMR)
- HSQC 2D spectral matrix (heteronuclear single quantum coherence)
- COSY 2D spectral matrix (correlated spectroscopy)
- IR spectrum (wavenumber vs. transmittance or absorbance)
- Molecular reference structure (SMILES string or MDL MOL file for validation)

## Outputs

- Predicted molecular structure (SMILES string or graph representation)
- Per-atom probability scores or confidence maps
- Multi-head attention weight matrices (explainability overlay on input spectra)
- Comparison report (predicted vs. reference structure similarity metric)

## How to apply

Load each spectroscopic modality (NMR, HSQC, COSY, IR data) from its native input format into preprocessed tensors matching the MultiModalSpectralTransformer's expected input schema. Normalize and align spectral features (chemical shifts, coupling constants, absorption bands) into a common coordinate system—e.g., aligning NMR chemical shift ranges to parts-per-million (ppm) and IR wavenumbers to standardized bins. Concatenate or stack the preprocessed modality tensors along a feature or modality dimension, ensuring temporal or spatial alignment where spectral peaks correspond across modalities. Pass the integrated tensor through the transformer encoder, which learns cross-modal attention weights to identify which spectral regions in one modality are most informative for predicting atomic environments reflected in others. The transformer's multi-head attention mechanism automatically discovers inter-modality dependencies without manual feature engineering.

## Related tools

- **MultiModalSpectralTransformer** (Transformer-based encoder-decoder architecture that jointly embeds NMR, HSQC, COSY, and IR spectra into a shared latent space and decodes molecular structure predictions with cross-modal attention.) — https://github.com/mpriessner/MultiModalSpectralTransformer
- **SGNN (Spectral Graph Neural Network)** (Generates simulated NMR data for training and validation of the spectral modality encoders; used in data augmentation pipeline.)
- **Chemprop-IR** (Produces simulated IR spectral data; complements experimental IR measurements for training multi-modal model.)
- **RDKit** (Converts predicted SMILES strings to molecular graphs and computes structural similarity metrics for validation and explainability.)

## Evaluation signals

- Exact-match validation: predicted structure SMILES string matches reference SMILES exactly or canonical equivalents (after stereochemistry correction).
- Structural similarity metric: Tanimoto coefficient or other graph-edit distance between predicted and reference molecular graphs exceeds domain-specific threshold (e.g., >0.85).
- Per-atom assignment accuracy: fraction of correctly predicted atoms (element and connectivity) in predicted structure relative to reference; track false-positive and false-negative rates.
- Cross-modal consistency: attention weights should show correlated peaks across NMR and IR spectra at chemically expected shifts; atoms with strong COSY correlations should have corresponding HSQC signals.
- Ablation validation: remove one modality (e.g., omit IR or COSY) and re-run; accuracy drop quantifies that modality's contribution; if all modalities show near-zero contribution, integration may be redundant.

## Limitations

- Requires pre-trained models and substantial computational resources (NVIDIA V100/K80 GPU with CUDA 11.1, ≥16 GB RAM, ≥50 GB storage) as stated in README; not suitable for resource-constrained environments.
- Input spectra must be preprocessed to expected format and coordinate system; misaligned or noise-dominated spectra (signal-to-noise ratio <5:1) degrade performance.
- Model was trained on specific datasets (IBM, PubChem, ZINC); performance on out-of-domain molecular classes (e.g., polymers, macrocycles) is not characterized.
- Transformer architecture assumes spectral peaks are localized and learnable; heavily overlapped or baseline-dominated regions may be misinterpreted.
- No guidance provided for handling missing or incomplete spectroscopic modalities; all four modalities (NMR, HSQC, COSY, IR) are expected at inference time.

## Evidence

- [readme] MultiModalSpectralTransformer is a transformer-based architecture that integrates various spectroscopic modalities (NMR, HSQC, COSY, IR) for automated molecular structure prediction: "MultiModalSpectralTransformer is a transformer-based architecture that integrates various spectroscopic modalities (NMR, HSQC, COSY, IR) for automated molecular structure prediction"
- [readme] GPU: A high-performance GPU is necessary. We recommend using an NVIDIA GPU with CUDA 11.1 support (e.g., NVIDIA V100 or K80). Memory: At least 16GB RAM to handle datasets and model training. Storage: At least 50GB storage space for datasets, model checkpoints, and results.: "GPU: A high-performance GPU is necessary. We recommend using an NVIDIA GPU with CUDA 11.1 support (e.g., NVIDIA V100 or K80). Memory: At least 16GB RAM. Storage: At least 50GB storage space"
- [other] Load and preprocess the multi-modal spectroscopic data into the transformer model's expected input format. Execute the transformer-based architecture to generate predicted molecular structures for each input spectrum set. Retrieve reference molecular structure predictions from the GitHub repository or Zenodo deposits. Compare predicted structures against reference outputs using structural similarity metrics or exact-match validation.: "Load and preprocess the multi-modal spectroscopic data into the transformer model's expected input format. Execute the transformer-based architecture to generate predicted molecular structures."
- [readme] Step-by-step guide for data preparation. Instructions for model training and fine-tuning. Tutorial on using the improvement cycle. Guide for interpreting model outputs and explanations.: "Step-by-step guide for data preparation. Instructions for model training and fine-tuning. Guide for interpreting model outputs and explanations."
- [readme] Download the necessary files from our Zenodo repository: https://doi.org/10.5281/zenodo.14712886. You'll need to download the following files: 1. Models (Required): Download models.zip and extract its contents into the models directory. 2. Data (Required): Download data.zip and extract its contents into the data directory.: "Download the necessary files from our Zenodo repository. Models (Required): Download models.zip and extract its contents into the models directory. Data (Required): Download data.zip and extract its"
