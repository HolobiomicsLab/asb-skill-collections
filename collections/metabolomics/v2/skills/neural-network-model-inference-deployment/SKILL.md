---
name: neural-network-model-inference-deployment
description: Use when you have a pre-trained neural network model (e.g., MSBERT weights in .
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
  - PyTorch
  - MSBERT
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

# neural-network-model-inference-deployment

## Summary

Deploy a pre-trained neural network model to perform inference on new data and generate embeddings or predictions. This skill validates model reproducibility and enables practical application of learned representations to unseen spectra or similar inputs.

## When to use

You have a pre-trained neural network model (e.g., MSBERT weights in .pkl format) and need to: (1) load it into a runtime environment, (2) run inference on new tandem mass spectra or similar input data, (3) generate embeddings or similarity scores, and (4) benchmark against reported accuracy metrics (e.g., top-1/5/10 library matching accuracies) to confirm the model achieves published performance.

## When NOT to use

- Model weights are not available or model architecture is not documented — you cannot instantiate the architecture without hyperparameters.
- Input spectra are in incompatible formats (e.g., raw instrument binary formats not convertible to .msp or compatible pre-processing) — inference requires standardized input preparation.
- You need to retrain or fine-tune the model on new data — this skill covers inference only, not model training.
- Ground truth labels are unavailable and you only need embeddings for downstream clustering or visualization without accuracy validation.

## Inputs

- Pre-trained model weights (.pkl file)
- Tandem mass spectra data (.msp format or ProcessMSP-compatible format)
- Model hyperparameters (vocabulary size, embedding dimension, encoder layers, attention heads)
- Reference library spectra (for library matching evaluation)

## Outputs

- Embedding vectors (dense numerical representations of input spectra)
- Similarity scores (e.g., cosine similarity matrix between query and reference embeddings)
- Library matching predictions (ranked candidate identifications)
- Accuracy metrics (top-1, top-5, top-10 matching accuracies)

## How to apply

Set up a Python environment with required dependencies (PyTorch 2.2, Anaconda Python 3.12). Clone the model repository and install requirements.txt. Load the pre-trained model weights from the .pkl file into the neural network architecture (instantiate the model class with published hyperparameters, then load_state_dict). Prepare input data using provided utility functions (e.g., ProcessMSP for .msp files). Run the model in inference mode (no gradient computation) to generate embeddings. For library matching tasks, compute pairwise similarities (e.g., cosine similarity) between query and reference embeddings. Evaluate accuracy by comparing predicted library identifications against ground truth labels at multiple ranking thresholds (top-1, top-5, top-10). Compare results against published benchmarks to verify deployment correctness.

## Related tools

- **PyTorch** (Deep learning framework for loading and executing the pre-trained MSBERT model in inference mode) — https://pytorch.org/
- **Anaconda** (Environment manager for isolating Python 3.12 runtime and dependencies (PyTorch, torch utilities)) — https://www.anaconda.com
- **MSBERT** (Pre-trained transformer-encoder model for embedding tandem mass spectra; provides model class, utilities (ProcessMSP, ModelEmbed, MSBERTSimilarity), and trained weights) — https://github.com/zhanghailiangcsu/MSBERT
- **Git** (Version control to clone the MSBERT repository and access model code and example scripts) — https://git-scm.com/downloads
- **matchms** (Optional workflow integration framework for computing MSBERT similarities within spectral matching pipelines) — https://github.com/zhanghailiangcsu/MSBERT/tree/main/matchms_workflow

## Examples

```
import torch
from model.MSBERTModel import MSBERT
from model.utils import ProcessMSP, ModelEmbed, MSBERTSimilarity

model = MSBERT(100002, 512, 6, 16, 0, 100, 3)
model.load_state_dict(torch.load('model/MSBERT.pkl'))
demo_data, _ = ProcessMSP('example/demo.msp')
demo_arr = ModelEmbed(model, demo_data, 16)
cos_sim = MSBERTSimilarity(demo_arr, demo_arr)
```

## Evaluation signals

- Loaded model produces embedding vectors with expected dimensionality (512 for MSBERT) and numerical range (floating-point bounded output).
- Model inference completes without runtime errors (backward pass is disabled; memory consumption is reduced vs. training).
- Computed top-1, top-5, and top-10 library matching accuracies match or exceed published benchmarks (0.7871, 0.8950, 0.9080 on Orbitrap test set) to within numerical precision tolerances.
- Cosine similarity scores between embedding pairs fall in expected range [−1, 1]; high similarity scores correspond to spectra with similar chemical structures or annotations.
- Prediction rankings are reproducible across runs (same random seed or deterministic model loading); no unexplained variance in accuracy metrics.
- Output embeddings cluster by instrument type, compound class, or structure when visualized (e.g., t-SNE or UMAP) — evidence of chemically rational embedding space.

## Limitations

- Model was trained and evaluated only on GNPS dataset filtered by instrument type (Orbitrap); performance on other instruments or external datasets not reported in provided context.
- Inference requires exact hyperparameter match (vocabulary size 100002, embedding dimension 512, 6 encoder layers, 16 attention heads); mismatch will raise shape errors.
- Input spectra must be preprocessed into .msp format or compatible format using ProcessMSP utility; raw binary or unsupported formats will cause parsing failures.
- Library matching accuracy depends on reference library quality and coverage; sparse or biased reference sets may reduce top-1 accuracy despite correct embedding.
- No changelog or version history provided; compatibility with future PyTorch or Python releases is not guaranteed.

## Evidence

- [other] Load the pre-trained model and the GNPS-derived Orbitrap test dataset. Run the model on the test spectra to generate embeddings and perform library matching. Compute top-1, top-5, and top-10 matching accuracies by comparing predicted library identifications against ground truth labels.: "Load the pre-trained MSBERT model and the GNPS-derived Orbitrap test dataset. Run the model on the test spectra to generate embeddings and perform library matching. Compute top-1, top-5, and top-10"
- [other] MSBERT achieved top-1, top-5, and top-10 library matching accuracies of 0.7871, 0.8950, and 0.9080 respectively on the Orbitrap test dataset.: "MSBERT achieved top-1, top-5, and top-10 library matching accuracies of 0.7871, 0.8950, and 0.9080 respectively on the Orbitrap test dataset."
- [other] Create conda environment for Python 3.12, activate MSBERT conda environment, clone MSBERT repository from GitHub, and install dependencies from requirements.txt.: "conda create -n MSBERT python=3.12 and conda activate MSBERT and git clone https://github.com/zhanghailiangcsu/MSBERT.git and pip install -r requirements.txt"
- [readme] model_file = 'model/MSBERT.pkl' and model = MSBERT(100002, 512, 6, 16, 0,100,3) and model.load_state_dict(torch.load(model_file)): "model_file = 'model/MSBERT.pkl'
model = MSBERT(100002, 512, 6, 16, 0,100,3)
model.load_state_dict(torch.load(model_file))"
- [readme] demo_data,demo_smiles = ProcessMSP(demo_file) and demo_arr = ModelEmbed(model,demo_data,16) and cos = MSBERTSimilarity(demo_arr,demo_arr): "demo_data,demo_smiles = ProcessMSP(demo_file)
demo_arr = ModelEmbed(model,demo_data,16)
cos = MSBERTSimilarity(demo_arr,demo_arr)"
- [readme] MSBERT had a stronger ability in library matching, with top 1, top5, and top 10 were 0.7871, 0.8950, and 0.9080 on Orbitrap test dataset.: "MSBERT had a stronger ability in library matching, with top 1, top5, and top 10 were 0.7871, 0.8950, and 0.9080 on Orbitrap test dataset."
- [readme] [Pytorch](https://pytorch.org/) 2.2 and [Anaconda](https://www.anaconda.com) for Python 3.12: "[Pytorch](https://pytorch.org/) 2.2 and [Anaconda](https://www.anaconda.com) for Python 3.12"
