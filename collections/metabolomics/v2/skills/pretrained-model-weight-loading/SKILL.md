---
name: pretrained-model-weight-loading
description: Use when you have a pretrained PyTorch model checkpoint (e.g., JESTR weights for NPLIB1) and wish to apply it to rank candidate molecules or score spectra without modifying model parameters.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - pip
  - CUDA
  - PyTorch
  - conda
  - CUDA 11.8
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1093/bioinformatics/btaf354
  title: JESTR
evidence_spans:
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btaf354
  all_source_dois:
  - 10.1093/bioinformatics/btaf354
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# pretrained-model-weight-loading

## Summary

Load pre-trained neural network weights into a PyTorch model to enable immediate inference on a target dataset without retraining. This skill is essential when you have access to published pretrained weights and want to rank or score new samples using a frozen, trained model.

## When to use

You have a pretrained PyTorch model checkpoint (e.g., JESTR weights for NPLIB1) and wish to apply it to rank candidate molecules or score spectra without modifying model parameters. This applies when the pretrained weights are compatible with your GPU environment (CUDA version, PyTorch version) and your input data matches the format the model was trained on.

## When NOT to use

- Your input data comes from a fundamentally different domain or is in an incompatible format (e.g., different metabolomics platform, different m/z calibration, incompatible graph representation); the pretrained weights encode assumptions about the training data distribution that will not transfer.
- Your environment cannot meet the GPU and CUDA requirements (released JESTR weights are GPU-trained models only); CPU inference with GPU-trained weights may fail or produce incorrect results.
- You need to fine-tune or adapt the model to your dataset; weight loading is for frozen inference, not transfer learning or domain adaptation.

## Inputs

- pretrained model checkpoint file (PyTorch .pt or .pth format)
- initialized PyTorch model architecture matching the checkpoint
- input dataset formatted to match training data (e.g., NPLIB1 spectra with m/z, intensity, and molecule graphs)
- environment with compatible CUDA version and dependencies

## Outputs

- model object with loaded pretrained weights in evaluation mode
- ranking scores or predictions for each query-candidate pair
- structured output file (e.g., CSV or pickle) with rankings and confidence scores

## How to apply

First, verify that your computational environment matches the original training setup: confirm CUDA 11.8 compatibility and install dependencies from jestr_requirements.txt using conda/pip. Load the pretrained model weights into the initialized PyTorch model architecture using the appropriate checkpoint file path. Verify weight loading by checking that model parameters are not randomly initialized (compare parameter norms before/after loading). Place the model in evaluation mode (.eval()) to disable dropout and batch normalization training behavior. Execute forward passes on your prepared input features to generate rankings or scores. The pretrained weights represent a frozen feature space, so no backpropagation or gradient updates should occur during inference.

## Related tools

- **PyTorch** (framework for loading model weights, managing GPU tensors, and executing forward inference passes) — https://pytorch.org
- **conda** (environment manager to install and pin dependency versions specified in jestr_requirements.txt) — http://docs.conda.io/latest/
- **pip** (alternative package manager for installing PyTorch and dependencies) — https://pip.pypa.io/en/stable/cli/pip_install/
- **CUDA 11.8** (GPU acceleration layer required for the released pretrained weights to execute correctly)

## Examples

```
python cand_rank_canopus.py
```

## Evaluation signals

- Verify model parameters are loaded (e.g., check that model.state_dict() keys match checkpoint keys, and parameter values are non-random)
- Confirm model is in evaluation mode by checking model.training == False and observing no dropout or batch norm randomness during repeated forward passes on identical inputs
- Compare output ranking scores against reference outputs (if available from the README or publication); identical inputs should produce identical scores
- Check that output rankings and scores fall within expected ranges (e.g., similarity scores between 0 and 1, ranking positions correspond to candidate count)
- Verify that the model produces valid rankings for all query spectra in the dataset with no NaN, Inf, or shape mismatches in outputs

## Limitations

- The released weights are GPU-trained models only; CPU inference is not supported and may fail or give incorrect results.
- Weights are specific to the NPLIB1 dataset; other datasets (e.g., MassBank, MoNA) are under licensing agreements and pretrained weights are not publicly released; transfer to such datasets requires retraining or fine-tuning.
- The code has been tested on specific package versions in jestr_requirements.txt; compatibility with significantly newer versions of PyTorch or CUDA is not guaranteed.
- The pretrained weights encode the learned embedding space and molecule ranking strategy from NPLIB1; performance on out-of-distribution spectra or unseen chemical scaffolds may degrade.

## Evidence

- [other] Load the pretrained NPLIB1 weights into the JESTR PyTorch model.: "Load the pretrained NPLIB1 weights into the JESTR PyTorch model."
- [readme] The model was trained and tested on GPU nVidia A100 with CUDA 11.8. The released weights are also for GPU trained models.: "The model was trained and tested on GPU nVidia A100 with CUDA 11.8. The released weights are also for GPU trained models."
- [readme] We have released the dataset and pretrained weights for the NPLIB1 dataset. The other datasets are under licensing agreements that prohibit their public release.: "We have released the dataset and pretrained weights for the NPLIB1 dataset. The other datasets are under licensing agreements that prohibit their public release."
- [readme] All code runs under the PyTorch framework. The code and the models have been tested on the package versions mentioned in the jestr_requirements.txt file, but it is likely the code will work on newer versions of the packages as well.: "All code runs under the PyTorch framework. The code and the models have been tested on the package versions mentioned in the jestr_requirements.txt file, but it is likely the code will work on newer"
- [readme] To use the pretrained model and rank a target molecule against its candidates on a given spectrum, please run the code in the notebook JESTR.ipynb.: "To use the pretrained model and rank a target molecule against its candidates on a given spectrum, please run the code in the notebook JESTR.ipynb."
