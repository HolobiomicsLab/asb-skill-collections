---
name: mass-spectrometry-dataset-handling-preprocessing
description: Use when you have raw or semi-processed MS/MS spectra in MSP format (e.g., from GNPS, Orbitrap instruments) and need to feed them into MSBERT or similar transformer-based embedding models for library matching, clustering, or similarity scoring.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - Anaconda
  - Git
  - ProcessMSP
  - ModelEmbed
  - MakeTrainData
  - PyTorch 2.2
  - Python 3.12 with Anaconda
  techniques:
  - LC-MS
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-dataset-handling-preprocessing

## Summary

Load, parse, and preprocess tandem mass spectrometry (MS/MS) data from MSP format files into structured arrays suitable for neural embedding models. This skill bridges raw spectral data and machine learning pipelines by standardizing spectra representation, extracting chemical metadata (SMILES), and preparing batches for model inference.

## When to use

You have raw or semi-processed MS/MS spectra in MSP format (e.g., from GNPS, Orbitrap instruments) and need to feed them into MSBERT or similar transformer-based embedding models for library matching, clustering, or similarity scoring. The input spectra may contain variable peak intensities, precursor m/z values, and SMILES annotations that must be normalized and aligned to a fixed vocabulary size (e.g., 100,002 m/z bins).

## When NOT to use

- Input is already a pre-computed embedding matrix or feature table; skip directly to similarity/matching steps.
- Spectra are in non-MSP formats (raw mzML, mzXML, raw proprietary formats) without prior conversion to MSP.
- SMILES annotations are absent and structural ground truth is required for evaluation; consider retrieving SMILES from external databases first.

## Inputs

- MSP format spectral files (.msp)
- Spectra with peaks (m/z, intensity pairs)
- SMILES strings or chemical structure annotations
- Pre-trained MSBERT model state dictionary (.pkl)

## Outputs

- Preprocessed spectral numpy arrays or tensors
- MSBERT embedding vectors (shape: num_spectra × 512)
- SMILES metadata aligned to spectra
- Cosine similarity matrices (when MSBERTSimilarity is applied)

## How to apply

Parse MSP files using the ProcessMSP utility to extract spectral peak arrays and corresponding SMILES strings. Convert each spectrum into a fixed-length numerical representation (e.g., binned m/z intensities over a defined mass range with vocabulary size 100,002) aligned to the model's input embedding dimension. Pass the preprocessed spectral arrays through ModelEmbed to generate embeddings at a specified batch size (e.g., 16 spectra per batch). Validate that output embedding vectors match the model's latent dimension (e.g., 512 dimensions for MSBERT) and that no spectra were dropped or corrupted during the conversion. Store embeddings and retain SMILES metadata for downstream similarity calculations or validation against structural ground truth.

## Related tools

- **ProcessMSP** (Parse MSP files and extract spectral peaks and SMILES; foundational data loading utility) — https://github.com/zhanghailiangcsu/MSBERT
- **ModelEmbed** (Convert preprocessed spectral arrays into fixed-dimension MSBERT embedding vectors at specified batch size) — https://github.com/zhanghailiangcsu/MSBERT
- **MakeTrainData** (Prepare and augment training datasets from raw GNPS data; used when retraining on custom datasets) — https://github.com/zhanghailiangcsu/MSBERT
- **PyTorch 2.2** (Tensor computation and model loading backend for embedding generation) — https://pytorch.org/
- **Python 3.12 with Anaconda** (Runtime environment and dependency management) — https://www.anaconda.com

## Examples

```
import pickle
import torch
from model.utils import ModelEmbed, ProcessMSP
model_file = 'model/MSBERT.pkl'
model = torch.load(model_file)
demo_data, demo_smiles = ProcessMSP('example/demo.msp')
demo_arr = ModelEmbed(model, demo_data, 16)
```

## Evaluation signals

- Preprocessed spectral arrays have shape (num_spectra, vocab_size=100,002) with non-negative intensity values summing to expected norms per spectrum.
- MSBERT embeddings have exact shape (num_spectra, 512) with no NaN or Inf values; all tensors are on the same device (CPU/GPU).
- SMILES metadata count matches preprocessed spectra count; no spectra are dropped or duplicated during conversion.
- Cosine similarity scores computed via MSBERTSimilarity fall in [−1, 1] range; diagonal values (self-similarity) are ≥0.99, confirming embedding stability.
- Reprocessed demo.msp spectra produce identical embeddings to those in the provided example, confirming pipeline reproducibility.

## Limitations

- Requires MSP format input; other spectral formats (mzML, mzXML, HDF5) must be pre-converted to MSP.
- Fixed vocabulary size (100,002 m/z bins) is tuned to GNPS Orbitrap data; retraining on different mass ranges or instruments may require vocabulary re-calibration.
- SMILES annotations are optional for embedding but required for downstream structural similarity validation; spectra without SMILES will pass preprocessing but cannot be validated against chemical ground truth.
- Batch size (e.g., 16) must fit in available GPU/CPU memory; very large spectra batches or high embedding dimensions may require smaller batch sizes or data sharding.

## Evidence

- [readme] demo_data,demo_smiles = ProcessMSP(demo_file): "demo_file = 'example/demo.msp'
demo_data,demo_smiles = ProcessMSP(demo_file)"
- [readme] demo_arr = ModelEmbed(model,demo_data,16): "demo_arr = ModelEmbed(model,demo_data,16)"
- [readme] MSBERT(100002, 512, 6, 16, 0,100,3): "model = MSBERT(100002, 512, 6, 16, 0,100,3)"
- [intro] Load the pre-trained MSBERT model and the GNPS-derived Orbitrap test dataset.: "Load the pre-trained MSBERT model and the GNPS-derived Orbitrap test dataset."
- [other] MSBERT was trained and tested on GNPS dataset.: "MSBERT was trained and tested on GNPS dataset."
- [readme] The filtered GNPS dataset used in this experiment was uploaded to Zenodo: "The filtered GNPS dataset used in this experiment was uploaded to [Zenodo](https://zenodo.org/records/13722644)."
