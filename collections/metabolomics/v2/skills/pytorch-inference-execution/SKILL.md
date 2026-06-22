---
name: pytorch-inference-execution
description: Use when you have a pretrained PyTorch model with released weights (e.g., JESTR on NPLIB1), a prepared dataset with input features (spectra m/z–intensity arrays, molecular graphs), a GPU environment with CUDA 11.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0208
  tools:
  - PyTorch
  - pip
  - CUDA
  - Python
  - conda/pip
  - CUDA 11.8
derived_from:
- doi: 10.1093/bioinformatics/btaf354
  title: JESTR
evidence_spans:
- All code runs under the [PyTorch framework](https://pytorch.org)
- All code runs under the [PyTorch framework](https://pytorch.org).
- Please set up the environment as per this file using [conda](http://docs.condi.ioen/latest/)/[pip]
- The model was trained and tested on GPU nVidia A100 with CUDA 11.8
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_jestr_cq
    doi: 10.1093/bioinformatics/btaf354
    title: JESTR
  dedup_kept_from: coll_jestr_cq
schema_version: 0.2.0
---

# pytorch-inference-execution

## Summary

Execute inference on a pretrained PyTorch model to generate ranked predictions on a new dataset. This skill involves loading model weights, preparing input features, and executing the forward pass to produce scored outputs suitable for downstream analysis or annotation.

## When to use

You have a pretrained PyTorch model with released weights (e.g., JESTR on NPLIB1), a prepared dataset with input features (spectra m/z–intensity arrays, molecular graphs), a GPU environment with CUDA 11.8+ and matching PyTorch dependencies, and need to rank or score candidate molecules against query spectra without retraining.

## When NOT to use

- The model was trained on a different GPU architecture or CUDA version and you have not verified weight compatibility.
- Input data is in a different format than the NPLIB1 dataset structure (e.g., raw mzML files instead of preprocessed spectra dictionaries).
- You need to adapt or fine-tune the model; use pytorch-training or transfer-learning skills instead.

## Inputs

- Pretrained PyTorch model weights (file path)
- Configuration file (params.yaml with pretrained model path and batch_size)
- Dataset pickle files (data_dict.pkl, inchi_to_id_dict.pkl, cand_dict.pkl, molgraph_dict.pkl)
- Spectra with m/z and intensity arrays
- Candidate molecule lists indexed by target molecule InChiKey

## Outputs

- Ranked candidate molecule predictions per query spectrum
- Confidence scores or similarity metrics for each ranking
- Structured output file (CSV or pickle) with spectra ID, rank, candidate ID, score

## How to apply

First, verify your computational environment matches the model's training setup (CUDA 11.8, package versions in jestr_requirements.txt). Load the pretrained model weights into the PyTorch model object using the provided weight path parameter in the config file (params.yaml). Prepare input features by loading the dataset (spectra information, candidate dictionaries, precomputed molecular graphs from molgraph_dict.pkl) and formatting them according to the model's expected input schema. Execute the model's forward pass on batches of data with the batch_size parameter, collecting scores and rankings for each query–candidate pair. Export predictions and confidence scores to a structured output file (e.g., CSV or pickle) with spectra IDs, candidate rankings, and associated scores for validation.

## Related tools

- **PyTorch** (Framework for loading and executing the pretrained JESTR model inference.) — https://pytorch.org
- **Python** (Host language for running inference scripts and utilities.)
- **conda/pip** (Dependency and environment management to ensure reproducible package versions matching model training.) — http://docs.condi.ioen/latest/
- **CUDA 11.8** (GPU acceleration layer required for GPU-trained model weights.)

## Examples

```
python cand_rank_canopus.py
```

## Evaluation signals

- Verify output file contains all query spectra IDs with corresponding ranked candidate lists and scores.
- Inspect score distributions and ranking ranges (e.g., top candidate score > expected threshold) for sanity.
- Cross-check a sample of predicted rankings against known ground-truth annotations in test set to confirm ranking quality aligns with reported performance.
- Confirm batch processing completes without GPU out-of-memory errors and latency is consistent across batches.
- Validate that all candidates for each query spectrum are ranked exactly once (no duplicates or missing entries).

## Limitations

- Released weights are GPU-trained models on CUDA 11.8 and may not be directly compatible with CPU inference or other CUDA versions without additional weight adaptation.
- Code has been tested on specific package versions in jestr_requirements.txt; newer package versions may work but compatibility is not guaranteed.
- Inference assumes input data follow the NPLIB1 format (precomputed molecular graphs, candidate dictionaries); datasets under licensing agreements (e.g., MassBank, ReSpect) must be prepared separately and are not included.
- Performance depends on correctness of input feature preprocessing (spectra normalization, graph construction); malformed or missing candidate dictionaries will cause ranking failures or incomplete output.

## Evidence

- [intro] All code runs under the PyTorch framework: "All code runs under the [PyTorch framework](https://pytorch.org)"
- [intro] Model was trained and tested on GPU nVidia A100 with CUDA 11.8: "The model was trained and tested on GPU nVidia A100 with CUDA 11.8"
- [intro] Released weights are for GPU trained models: "The released weights are also for GPU trained models"
- [readme] To use the pretrained model and rank a target molecule against its candidates on a given spectrum, please run the code in the notebook JESTR.ipynb: "To use the pretrained model and rank a target molecule against its candidates on a given spectrum, please run the code in the notebook [JESTR.ipynb]"
- [readme] To rank candidates for the complete NPLIB1 dataset, use the command: python cand_rank_canopus.py: "To rank candidates for the complete NPLIB1 dataset, use the command: python cand_rank_canopus.py"
- [other] Load the pretrained NPLIB1 weights into the JESTR PyTorch model: "Load the pretrained NPLIB1 weights into the JESTR PyTorch model"
- [other] Execute the JESTR ranking inference to score and rank candidate molecules for each query spectrum: "Execute the JESTR ranking inference to score and rank candidate molecules for each query spectrum"
- [readme] The parameters set in this file are: exp: dataset to be used. If you create your own dataset, you need to update utils.py to load it; batch_size* - parameters to set the batch sizes during training and test; pretrained* - pretrained model weight path: "batch_size* - parameters to set the batch sizes during training and test; pretrained* - pretrained model weight path"
