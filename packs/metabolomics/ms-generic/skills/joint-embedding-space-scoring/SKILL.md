---
name: joint-embedding-space-scoring
description: Use when you have a mass spectrum from an untargeted metabolomics experiment and a set of candidate molecules (e.g., downloaded from PubChem) that may explain that spectrum. You want to rank these candidates by likelihood of correctness to prioritize manual annotation or further validation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - pip
  - CUDA
  - PyTorch
  - Python
  - conda / pip
  - CUDA 11.8
  - RDKit
  - DGL (Deep Graph Library)
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# joint-embedding-space-scoring

## Summary

Score and rank candidate molecules against a query mass spectrum using JESTR, a PyTorch-based joint embedding space model trained on natural products spectral libraries. This skill produces ranked candidate lists for annotation of untargeted metabolomics data.

## When to use

You have a mass spectrum from an untargeted metabolomics experiment and a set of candidate molecules (e.g., downloaded from PubChem) that may explain that spectrum. You want to rank these candidates by likelihood of correctness to prioritize manual annotation or further validation. The NPLIB1 pretrained weights are appropriate when your spectra derive from natural products or are compatible with the NPLIB1 training domain.

## When NOT to use

- Your spectra are from a domain or instrument substantially different from the NPLIB1 natural products library (e.g., lipidomics, synthetic pharmaceutical compounds); the pretrained weights may not transfer well.
- Candidates have not been properly formatted or preprocessed to match NPLIB1 input requirements (e.g., missing 3D coordinates, invalid SMILES).
- You need CPU-only inference; released weights are GPU-trained and may not perform as intended without CUDA 11.8 and GPU support.

## Inputs

- Pretrained JESTR model weights (PyTorch .pth file for NPLIB1 dataset)
- Query mass spectrum (m/z and intensity arrays)
- Candidate molecule structures (SMILES, InChI, or RDKit mol objects)
- Configuration file (params.yaml) specifying model hyperparameters and paths
- Data dictionaries (data_dict.pkl, mol_dict.pkl, molgraph_dict.pkl) for spectrum and molecule metadata

## Outputs

- Ranked list of candidate molecules scored by relevance to query spectrum
- Numerical ranking scores or similarity metrics for each candidate
- Structured output file (e.g., CSV or JSON) mapping query spectra to ranked candidates and scores

## How to apply

Load the pretrained JESTR PyTorch model weights (GPU-trained on NPLIB1) into the model architecture. Prepare your query spectrum as an m/z–intensity array and each candidate molecule as an RDKit mol object or DGL graph representation. Pass both through the joint embedding space to compute scoring vectors, then rank candidates by descending embedding similarity or learned relevance score. The model leverages contrastive training on spectrum–molecule pairs followed by MLP fine-tuning for ranking; ensure your input spectra and candidates match the preprocessing and feature extraction used during NPLIB1 training (refer to dataset.py and params.yaml for normalization and augmentation details). Export the ranked list with associated scores for downstream analysis or wet-lab prioritization.

## Related tools

- **PyTorch** (Deep learning framework for loading and executing the JESTR model and computing embedding scores) — https://pytorch.org
- **Python** (Primary language for model inference and utility functions (dataset loading, feature preprocessing))
- **conda / pip** (Package managers for environment setup and dependency installation per jestr_requirements.txt) — https://docs.conda.io / https://pip.pypa.io
- **CUDA 11.8** (GPU compute platform required for efficient inference with released pretrained weights)
- **RDKit** (Molecular structure parsing and graph representation generation for candidate molecules)
- **DGL (Deep Graph Library)** (Graph neural network framework for molecule graph representation and embedding computation)

## Examples

```
python cand_rank_canopus.py
```

## Evaluation signals

- Ranked candidates include known true metabolites (if available from validation set) within top-k positions (e.g., top 10); compare against gold-standard annotations.
- Ranking scores are in expected numerical range (e.g., similarity scores 0–1 or log probabilities); verify no NaN, infinite, or out-of-bounds values.
- Output file contains all query spectra with ≥1 ranked candidate per spectrum; check for missing or truncated entries.
- Embedding vectors for the same molecule across different spectra cluster similarly in embedding space; verify consistency via nearest-neighbor analysis.
- Reproducibility check: re-running inference on identical inputs with same model weights and random seed produces identical rankings and scores.

## Limitations

- Released pretrained weights are optimized for the NPLIB1 natural products dataset; performance on other metabolite classes (lipids, pharmaceuticals, environmental compounds) is not characterized.
- The model requires GPU compute with CUDA 11.8; CPU inference is not officially supported and may be slow or unsupported.
- Other datasets used in the paper are under licensing agreements that prohibit public release, limiting evaluation on external benchmarks.
- Ranking depends on the quality and completeness of the candidate set; if the true metabolite is not in the candidate pool, no ranking can recover it.
- The code has been tested on specific package versions in jestr_requirements.txt; compatibility with newer package versions is stated as likely but not guaranteed.

## Evidence

- [intro] Joint Embedding Space Technique for Ranking Candidate Molecules for the Annotation of Untargeted Metabolomics Data: "Joint Embedding Space Technique for Ranking Candidate Molecules for the Annotation of Untargeted Metabolomics Data"
- [intro] The model was trained and tested on GPU nVidia A100 with CUDA 11.8. The released weights are also for GPU trained models.: "The model was trained and tested on GPU nVidia A100 with CUDA 11.8. The released weights are also for GPU trained models."
- [intro] We have released the dataset and pretrained weights for the NPLIB1 dataset.: "We have released the dataset and pretrained weights for the NPLIB1 dataset."
- [readme] To use the pretrained model and rank a target molecule against its candidates on a given spectrum, please run the code in the notebook JESTR.ipynb. This notebook uses utility functions from python scripts explained below and data from NPLIB1.: "To use the pretrained model and rank a target molecule against its candidates on a given spectrum, please run the code in the notebook JESTR.ipynb."
- [readme] To rank candidates for the complete NPLIB1 dataset, use the command: python cand_rank_canopus.py: "To rank candidates for the complete NPLIB1 dataset, use the command: python cand_rank_canopus.py"
- [readme] All code runs under the PyTorch framework. The code and the models have been tested on the package versions mentioned in the jestr_requirements.txt file, but it is likely the code will work on newer versions of the packages as well.: "All code runs under the PyTorch framework. The code and the models have been tested on the package versions mentioned in the jestr_requirements.txt file"
- [readme] The other datasets are under licensing agreements that prohibit their public release.: "The other datasets are under licensing agreements that prohibit their public release."
