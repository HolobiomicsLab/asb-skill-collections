---
name: transformer-architecture-inference
description: Use when you have acquired or generated multi-modal spectroscopic data (integrated NMR, HSQC, COSY, IR spectra) in the model's expected input format, a pre-trained MultiModalSpectralTransformer checkpoint is available, and you need to predict molecular structures from these spectra without.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2929
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_2258
  - http://edamontology.org/topic_3344
  tools:
  - MultiModalSpectralTransformer
  - PyTorch
  - RDKit
  - SGNN (Spectral Graph Neural Network)
  - Chemprop-IR
derived_from:
- doi: 10.1002/ange.202517611
  title: MMST
- doi: 10.1021/acs.jcim.1c00055
  title: ''
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
  - 10.1021/acs.jcim.1c00055
  - 10.5281/zenodo.14712886
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# transformer-architecture-inference

## Summary

Execute a pre-trained transformer model on multi-modal spectroscopic input data (NMR, HSQC, COSY, IR) to generate automated molecular structure predictions. This skill operationalizes the MultiModalSpectralTransformer architecture for inference on new or reference spectral datasets.

## When to use

You have acquired or generated multi-modal spectroscopic data (integrated NMR, HSQC, COSY, IR spectra) in the model's expected input format, a pre-trained MultiModalSpectralTransformer checkpoint is available, and you need to predict molecular structures from these spectra without retraining. Use this when validating model performance against reference datasets or applying the model to novel spectroscopic inputs.

## When NOT to use

- Input spectra are raw, unpreprocessed files not yet aligned to the model's expected tensor shape or normalization scheme.
- You lack a pre-trained model checkpoint or the model was trained on incompatible spectroscopic modalities or molecular domains (e.g., a model trained only on NMR cannot reliably infer from IR-only data).
- The goal is to train or fine-tune the transformer on new data; use a training workflow instead.

## Inputs

- Multi-modal spectroscopic data files (NMR, HSQC, COSY, IR in model-compatible format)
- Pre-trained MultiModalSpectralTransformer model checkpoint (PyTorch .pt or .pth)
- Preprocessed spectral tensors aligned to model input shape expectations
- Optional: reference molecular structures (SMILES or molecular graphs) for validation

## Outputs

- Predicted molecular structures (SMILES strings or molecular graph representations)
- Structure prediction confidence scores or attention weights
- Structural similarity metrics (e.g., Tanimoto coefficient, exact-match rate)
- Comparison report documenting prediction accuracy and discrepancies

## How to apply

First, ensure your spectroscopic data (NMR, HSQC, COSY, IR files) is preprocessed into the transformer model's input format as documented in the ESI Section 3. Load the pre-trained model checkpoint from the `models/mmst/` directory using PyTorch. Execute forward inference by passing the multi-modal spectral tensor through the transformer encoder-decoder architecture; the model will emit predicted molecular structures (typically as SMILES strings or molecular graphs). Retrieve reference structures (from Zenodo deposits or ground truth annotations) and compute structural similarity metrics (e.g., Tanimoto or exact SMILES match) to quantify prediction accuracy. Document prediction confidence scores and any structural discrepancies for downstream analysis or model refinement.

## Related tools

- **MultiModalSpectralTransformer** (Core transformer-based inference engine that integrates NMR, HSQC, COSY, and IR modalities to predict molecular structures from integrated spectroscopic input) — https://github.com/mpriessner/MultiModalSpectralTransformer
- **PyTorch** (Deep learning framework for loading and executing the pre-trained transformer model checkpoint during inference)
- **RDKit** (Molecular informatics library for parsing predicted SMILES strings, computing structural similarity metrics (Tanimoto, fingerprints), and validating molecular structures)
- **SGNN (Spectral Graph Neural Network)** (Sub-component used for NMR data generation and validation within the multi-modal pipeline) — https://pubs.rsc.org/en/content/articlelanding/2022/cp/d2cp04542g
- **Chemprop-IR** (Sub-component used for IR spectral prediction and validation within the multi-modal pipeline) — https://pubs.acs.org/doi/abs/10.1021/acs.jcim.1c00055

## Examples

```
# After environment setup and downloading models from Zenodo, run inference in Python:
import torch
from utils_MMT import load_preprocessed_spectra, load_model
model = load_model('models/mmst/checkpoint.pt')
spectra_tensor = load_preprocessed_spectra('data/test_data/sample_nmr_hsqc_cosy_ir.h5')
predicted_smiles = model.infer(spectra_tensor)
print(f"Predicted structure: {predicted_smiles}")
```

## Evaluation signals

- Predicted SMILES strings are valid (RDKit can parse them without errors) and the inferred molecular structures match reference structures using exact SMILES or Tanimoto similarity > 0.9 on reference validation sets.
- Model output tensors match expected shape and data type; confidence scores are normalized to [0, 1] range with interpretable probability distributions across predicted structure space.
- Comparison report shows exact-match or structural similarity metrics consistent with those reported in the reference datasets (Zenodo 16076914, 16257786, 17284940); any discrepancies are documented with molecular class or spectral modality attribution.
- Inference completes without GPU out-of-memory errors or model loading failures when using the specified hardware requirements (NVIDIA GPU with CUDA 11.1, ≥16GB RAM).
- For subset of predictions, visual inspection of attention weights from the transformer encoder shows meaningful alignment between predicted structural features and input spectral regions (e.g., aromatic protons in NMR correlate with aromatic ring predictions).

## Limitations

- Requires a high-performance GPU with CUDA 11.1 support (NVIDIA V100 or K80 recommended); CPU-only inference is computationally prohibitive.
- Prediction accuracy is bounded by the training data domains (IBM, PubChem, ZINC datasets); model may fail or hallucinate structures for molecules outside these domains or with unusual functional groups not well-represented in training.
- Multi-modal integration assumes all four spectroscopic modalities (NMR, HSQC, COSY, IR) are available and preprocessed; missing or corrupted modalities may degrade or prevent inference.
- Model was designed and validated on molecules up to a certain size/complexity; very large molecules or highly branched structures not in training set may exceed model capacity.
- Preprocessing and normalization steps must exactly match those applied during training; deviations in spectral alignment, binning, or intensity scaling can introduce systematic prediction errors.

## Evidence

- [readme] MultiModalSpectralTransformer is a transformer-based architecture that integrates various spectroscopic modalities (NMR, HSQC, COSY, IR) for automated molecular structure prediction: "MultiModalSpectralTransformer is a transformer-based architecture that integrates various spectroscopic modalities (NMR, HSQC, COSY, IR) for automated molecular structure prediction"
- [other] Load and preprocess the multi-modal spectroscopic data into the transformer model's expected input format. Execute the transformer-based architecture to generate predicted molecular structures: "Load and preprocess the multi-modal spectroscopic data into the transformer model's expected input format. 4. Execute the transformer-based architecture to generate predicted molecular structures"
- [other] Retrieve reference molecular structure predictions from the GitHub repository or Zenodo deposits. Compare predicted structures against reference outputs using structural similarity metrics: "Retrieve reference molecular structure predictions from the GitHub repository or Zenodo deposits. 6. Compare predicted structures against reference outputs using structural similarity metrics"
- [readme] Step-by-step guide for data preparation. Instructions for model training and fine-tuning. Tutorial on using the improvement cycle. Guide for interpreting model outputs and explanations: "Step-by-step guide for data preparation. Instructions for model training and fine-tuning. Tutorial on using the improvement cycle. Guide for interpreting model outputs"
- [readme] Download the necessary files from our Zenodo repository: https://doi.org/10.5281/zenodo.14712886. Download `models.zip` and extract its contents into the `models` directory: "Download the necessary files from our Zenodo repository: https://doi.org/10.5281/zenodo.14712886. Download `models.zip` and extract its contents into the `models` directory"
- [readme] GPU: A high-performance GPU is necessary. We recommend using an NVIDIA GPU with CUDA 11.1 support (e.g., NVIDIA V100 or K80). Memory: At least 16GB RAM: "GPU: A high-performance GPU is necessary. We recommend using an NVIDIA GPU with CUDA 11.1 support (e.g., NVIDIA V100 or K80). Memory: At least 16GB RAM"
