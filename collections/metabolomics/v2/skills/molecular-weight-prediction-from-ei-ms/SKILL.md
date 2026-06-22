---
name: molecular-weight-prediction-from-ei-ms
description: Use when you have EI-MS spectrum data (m/z and intensity pairs) from a sample and need a direct, model-based prediction of molecular weight.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - Python
  - Git
  - rdkit
  - Anaconda
  - MWFormer
  - PyTorch
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
---

# molecular-weight-prediction-from-ei-ms

## Summary

Use the MWFormer transformer model to directly predict molecular mass from electron ionization mass spectrometry (EI-MS) data by loading a pre-trained model and running forward inference on parsed m/z and intensity spectrum values. This skill enables rapid, direct mass inference without manual spectral interpretation or fragmentation pattern analysis.

## When to use

Apply this skill when you have EI-MS spectrum data (m/z and intensity pairs) from a sample and need a direct, model-based prediction of molecular weight. This is most appropriate when you want to leverage transformer-based learned patterns over EI-MS instead of manual spectral interpretation, and when you have access to a pre-trained MWFormer model checkpoint.

## When NOT to use

- Input spectrum is from a non-EI ionization source (e.g. ESI, APCI, MALDI) — MWFormer is trained specifically on electron ionization mass spectra.
- Input spectrum is already a processed feature vector or embedding — this skill expects raw or normalized m/z and intensity pairs.
- You have no access to a pre-trained MWFormer model and cannot train one — the skill assumes a trained model is available.

## Inputs

- EI-MS spectrum data (m/z and intensity value pairs)
- Pre-trained MWFormer model checkpoint (.pt or .pth file)
- Spectrum configuration or normalization parameters matching model training

## Outputs

- Predicted molecular weight (scalar mass value)
- Inference confidence or probability (if model outputs uncertainty)

## How to apply

Set up a conda environment with Python 3.9, PyTorch 1.12 with CUDA 11.8 support, and rdkit. Clone the MWFormer repository from GitHub and install dependencies from requirements.txt. Load the pre-trained MWFormer model checkpoint from the repository. Parse your input EI-MS spectrum as m/z and intensity values, then prepare it as a tensor matching the model's expected input format (typically normalized spectrum data). Run forward inference through the MWFormer transformer to generate a direct molecular weight prediction. The output is a single predicted molecular mass value; success is indicated by a numerically valid mass prediction and absence of NaN or out-of-range outputs.

## Related tools

- **MWFormer** (Pre-trained transformer neural network model that accepts EI-MS spectrum tensors and outputs molecular weight predictions) — https://github.com/zhanghailiangcsu/MWFormer
- **PyTorch** (Deep learning framework used to load the model and execute forward inference) — https://pytorch.org/
- **Python** (Programming language for environment setup, data parsing, and inference orchestration)
- **Anaconda** (Environment and dependency manager for Python 3.9 and conda packages (rdkit)) — https://www.anaconda.com
- **rdkit** (Cheminformatics toolkit (optional utility for validation or post-processing of predicted molecular weights))

## Evaluation signals

- Predicted molecular weight is a positive real number within chemically plausible range (e.g. 10–2000 Da for most organic molecules).
- Forward inference completes without NaN, infinity, or runtime errors on valid EI-MS input tensors.
- Spectrum tensor shape and dtype match model input specification (e.g. batch, m/z bins, intensity values).
- Output molecular weight is consistent across multiple runs with identical input (deterministic given fixed model and input).
- If ground-truth molecular weights are available, compare predicted values to known masses; check for systematic bias or outliers beyond expected model error margins.

## Limitations

- MWFormer is trained specifically on EI-MS data; it is not expected to generalize to spectra from other ionization methods (ESI, MALDI, APCI, etc.).
- Model performance depends on spectrum quality and preprocessing (normalization, m/z alignment) matching the training protocol — deviations may degrade accuracy.
- No changelog is provided in the repository, making version history and model updates opaque.
- Prediction is a single mass value; the model does not report confidence intervals, uncertainty estimates, or alternative candidates.
- The README does not specify input spectrum dimensions, preprocessing requirements, or acceptable m/z and intensity ranges; users must infer these from example code or model source.

## Evidence

- [readme] MWFormer: Direct Prediction of Molecular Mass from Electron lonization Mass Spectrum by Transformer: "MWFormer: Direct Prediction of Molecular Mass from Electron lonization Mass Spectrum by Transformer"
- [other] The MWFormer model accepts electron ionization mass spectrum data as input and outputs a direct prediction of the molecular weight through a forward inference operation.: "The MWFormer model accepts electron ionization mass spectrum data as input and outputs a direct prediction of the molecular weight through a forward inference operation."
- [other] Parse the input EI-MS spectrum data (m/z and intensity values). Prepare the spectrum as a tensor input matching the model's expected input format. Run forward inference through the MWFormer transformer to generate the predicted molecular weight.: "Parse the input EI-MS spectrum data (m/z and intensity values). Prepare the spectrum as a tensor input matching the model's expected input format. Run forward inference through the MWFormer"
- [readme] conda create -n MWFormer python=3.9
conda activate MWFormer
git clone https://github.com/zhanghailiangcsu/MWFormer.git
pip install -r requirements.txt
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
conda install -c conda-forge rdkit: "conda create -n MWFormer python=3.9
conda activate MWFormer
git clone https://github.com/zhanghailiangcsu/MWFormer.git
pip install -r requirements.txt
pip3 install torch torchvision torchaudio"
- [readme] You can download the trained model on Github. Then refer to the example to use the model for prediction, and directly obtain the molecular weight from EI-MS.: "You can download the trained model on Github. Then refer to the example to use the model for prediction, and directly obtain the molecular weight from EI-MS."
