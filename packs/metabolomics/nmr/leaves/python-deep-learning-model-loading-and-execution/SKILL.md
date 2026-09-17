---
name: python-deep-learning-model-loading-and-execution
description: Use when when you have a pre-trained deep learning model checkpoint (saved
  in PyTorch format) and new 1D 1H NMR spectral data in CSV and peak-list TXT formats,
  and you need to generate peak-to-metabolite assignments or other structured outputs
  from that model without modification of model weights.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3445
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
  tools:
  - Python
  - PyTorch
  - NumPy
  - Pandas
  - SciPy
  - NMRformer
  techniques:
  - NMR
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.4c05632
  title: NMRformer
evidence_spans:
- python 3.9.13
- torch 1.10.0+cu113
- pip install numpy==1.26.4
- pip install pandas==1.5.1
- pip install scipy
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_nmrformer_cq
    doi: 10.1021/acs.analchem.4c05632
    title: NMRformer
  dedup_kept_from: coll_nmrformer_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c05632
  all_source_dois:
  - 10.1021/acs.analchem.4c05632
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# python-deep-learning-model-loading-and-execution

## Summary

Load a pre-trained Transformer-based deep learning model in PyTorch and execute inference on spectroscopic input data (spectrum and peak lists) to generate structured predictions. This skill is essential for applying trained neural networks to new NMR data without retraining.

## When to use

When you have a pre-trained deep learning model checkpoint (saved in PyTorch format) and new 1D 1H NMR spectral data in CSV and peak-list TXT formats, and you need to generate peak-to-metabolite assignments or other structured outputs from that model without modification of model weights.

## When NOT to use

- Input peak list contains many unrecognized or noisy peaks and has not been pre-filtered; model output accuracy will be compromised.
- You need to retrain or fine-tune the model on new data; this skill performs inference only, not model training.
- The input data is in a format other than 1D 1H NMR (e.g., 2D NMR, mass spectrometry); the model is specific to 1D 1H spectra.

## Inputs

- Pre-trained PyTorch model checkpoint (NMRformer weights)
- CSV file containing 1D 1H NMR spectrum (chemical shift and intensity columns)
- TXT file containing peak list (one chemical shift value per row)
- Python environment with PyTorch, NumPy, and Pandas installed

## Outputs

- output.csv file containing metabolite identifications with probability scores for each detected peak
- Peak-to-metabolite assignment predictions from the Transformer model

## How to apply

Load the pre-trained NMRformer model using PyTorch within a Jupyter notebook (NMRformer.ipynb). Import the spectrum data from a CSV file (columns: chemical shift, 1H NMR spectrum intensity) and peak-list data from a TXT file (one chemical shift per row) using Pandas and NumPy. Before inference, filter the input peak list to remove unrecognized or noisy peaks, as these negatively affect model output quality. Pass the cleaned spectrum and peak data through the loaded Transformer model to generate peak-to-metabolite assignments with probability scores. Export the results (metabolites and their associated probabilities) to an output CSV file.

## Related tools

- **PyTorch** (Deep learning framework for loading and executing the pre-trained Transformer model)
- **Pandas** (CSV import and data frame manipulation for spectrum and output metabolite data)
- **NumPy** (Numerical array operations for spectral data handling and peak filtering)
- **NMRformer** (Pre-trained Transformer model for peak assignment and metabolite identification) — https://github.com/zza1211/NMRformer

## Evaluation signals

- output.csv file is generated successfully with valid metabolite names and probability scores (0.0–1.0 range) for each peak.
- Number of rows in output.csv matches the number of peaks in the filtered input peak list (one-to-one mapping).
- Model execution completes without runtime errors or out-of-memory exceptions.
- Metabolite predictions are chemically reasonable and correspond to expected compounds in the sample context.
- Probability scores reflect model confidence; high-probability assignments correspond to well-resolved peaks in the input spectrum.

## Limitations

- Noisy peaks or unrecognized peaks in the input spectral peak list negatively affect model output; pre-filtering is strongly recommended.
- Model performance is specific to 1D 1H NMR spectra; other NMR experiments or modalities are not supported.
- The pre-trained model is frozen; it cannot adapt to new metabolite classes or spectral distributions not seen during training.
- Input data must conform to the expected schema (CSV with chemical shift and intensity columns; TXT with one peak per row) or data loading will fail.

## Evidence

- [other] Load the pre-trained NMRformer model in NMRformer.ipynb using PyTorch: "Load the pre-trained NMRformer model in NMRformer.ipynb using PyTorch"
- [other] Import the spectrum data from the input CSV file and peak-list data from the input TXT file using Pandas and NumPy: "Import the spectrum data from the input CSV file and peak-list data from the input TXT file using Pandas and NumPy"
- [other] Filter the peak list to remove unrecognized or noisy peaks as recommended by the model: "Verify and filter the peak list to remove unrecognized or noisy peaks as recommended by the model"
- [readme] When you input peaks that cannot be recognized or noisy peaks into the model, it will affect the output of the model, so please try to filter the peaks in the input spectral peak list as much as possible: "When you input peaks that cannot be recognized or noisy peaks into the model, it will affect the output of the model, so please try to filter the peaks in the input spectral peak list as much as"
- [readme] In NMRformer.ipynb, you can load the model and input data, resulting in an output.csv file that contains the corresponding metabolites and probabilities for each peak: "In NMRformer.ipynb, you can load the model and input data, resulting in an output.csv file that contains the corresponding metabolites and probabilities for each peak"
