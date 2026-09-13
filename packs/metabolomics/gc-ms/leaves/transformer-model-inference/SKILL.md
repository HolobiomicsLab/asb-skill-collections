---
name: transformer-model-inference
description: Use when you have electron ionization mass spectrum data (m/z and intensity
  pairs) and a pre-trained transformer model checkpoint, and you need to predict molecular
  weight directly from the spectrum without manual feature engineering or rule-based
  methods.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - Git
  - rdkit
  - Anaconda
  - PyTorch
  - MWFormer
  techniques:
  - GC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.4c03781
  title: MWFormer
evidence_spans:
- '[Anaconda](https://www.anaconda.com) for Python 3.9'
- Install [Git](https://git-scm.com/downloads)
- conda install -c conda-forge rdkit
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mwformer_cq
    doi: 10.1021/acs.analchem.4c03781
    title: MWFormer
  dedup_kept_from: coll_mwformer_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c03781
  all_source_dois:
  - 10.1021/acs.analchem.4c03781
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Transformer Model Inference

## Summary

Load a pre-trained transformer model and execute forward inference on structured input data to generate predictions. This skill applies deep learning transformer architectures to produce direct output predictions from raw instrumental data without post-processing.

## When to use

You have electron ionization mass spectrum data (m/z and intensity pairs) and a pre-trained transformer model checkpoint, and you need to predict molecular weight directly from the spectrum without manual feature engineering or rule-based methods.

## When NOT to use

- Input spectrum is already a feature vector or hand-engineered descriptor (model expects raw m/z–intensity pairs).
- You need uncertainty quantification or confidence intervals; the model outputs only a point prediction.
- The mass spectrum was acquired by ionization methods other than electron ionization (e.g., ESI, MALDI).

## Inputs

- electron ionization mass spectrum (m/z values and intensity values)
- pre-trained transformer model checkpoint (.pth or equivalent)
- spectrum tensor formatted to model input specification

## Outputs

- predicted molecular weight (scalar numeric value)
- molecular mass prediction

## How to apply

Set up a Python 3.9 environment with PyTorch 1.12 and necessary dependencies (rdkit). Clone and load the pre-trained MWFormer model from the repository. Parse your EI-MS spectrum as m/z and intensity arrays. Prepare the spectrum as a PyTorch tensor matching the model's expected input shape and format. Execute a forward pass through the transformer model. The model outputs a direct prediction of molecular mass; extract and record this scalar value. Verify the predicted mass is positive and within physically plausible range for the input spectrum's m/z range.

## Related tools

- **PyTorch** (Tensor operations and transformer model execution framework) — https://pytorch.org/
- **Python** (Programming language for environment setup and inference script)
- **Anaconda** (Environment and dependency management) — https://www.anaconda.com
- **rdkit** (Molecular data handling and validation) — https://www.rdkit.org/
- **MWFormer** (Pre-trained transformer model for direct molecular weight prediction from EI-MS) — https://github.com/zhanghailiangcsu/MWFormer

## Evaluation signals

- Predicted molecular weight is a positive scalar (mass must be > 0).
- Predicted mass is physically plausible given the input spectrum's maximum m/z value (molecular ion typically dominates or appears near spectrum upper bound).
- Model inference executes without CUDA/tensor shape errors, indicating correct input formatting.
- Output value is deterministic across repeated runs on identical input (reproducibility).
- Predicted mass aligns with known or reference molecular weights for validation spectra, if available.

## Limitations

- Model is trained and validated specifically on electron ionization mass spectra; performance on other ionization methods is unknown.
- The transformer outputs only a point estimate without calibrated uncertainty; high-stakes applications may require ensemble methods or Bayesian alternatives.
- Predictions depend critically on correct preprocessing and tensor formatting; malformed input silently produces incorrect output.
- No changelog or versioning information is documented in the repository, limiting reproducibility across time.
- Model generalization to novel or out-of-distribution spectra (e.g., from new instruments or rare chemical classes) is not characterized.

## Evidence

- [intro] MWFormer enables direct prediction of molecular mass from electron ionization mass spectrum using transformer architecture: "MWFormer: Direct Prediction of Molecular Mass from Electron lonization Mass Spectrum by Transformer"
- [other] Parse the input EI-MS spectrum data (m/z and intensity values). Prepare the spectrum as a tensor input matching the model's expected input format. Run forward inference through the MWFormer transformer to generate the predicted molecular weight.: "Parse the input EI-MS spectrum data (m/z and intensity values). Prepare the spectrum as a tensor input matching the model's expected input format. Run forward inference through the MWFormer"
- [intro] Create and activate conda environment with Python 3.9, PyTorch 1.12, and rdkit dependencies: "conda create -n MWFormer python=3.9"
- [readme] Load the pre-trained MWFormer model from the repository and execute forward pass: "You can download the trained model on Github. Then refer to the example to use the model for prediction, and directly obtain the molecular weight from EI-MS."
- [intro] Install PyTorch with CUDA 11.8 support for GPU acceleration: "pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118"
