---
name: transformer-model-inference-on-spectral-data
description: Use when you have a 1D 1H NMR spectrum represented as chemical shift vs. intensity values, a corresponding list of detected peak positions, and you need to assign metabolite identities to those peaks.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - PyTorch
  - NumPy
  - Pandas
  - SciPy
  - NMRformer
derived_from:
- doi: 10.1021/acs.analchem.4c05632
  title: NMRformer
evidence_spans:
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# transformer-model-inference-on-spectral-data

## Summary

Apply a pre-trained Transformer model to 1D 1H NMR spectral data (chemical shift and intensity pairs) and peak lists to perform peak-to-metabolite assignment. This skill generates probabilistic metabolite identifications for each detected peak in the spectrum.

## When to use

You have a 1D 1H NMR spectrum represented as chemical shift vs. intensity values, a corresponding list of detected peak positions, and you need to assign metabolite identities to those peaks. Use this skill when manual peak interpretation is infeasible or when you want consistent, data-driven metabolite assignment across multiple spectra.

## When NOT to use

- Input peak list contains unfiltered or high-noise peaks without prior quality assessment — the model output will be unreliable.
- Input spectrum is 2D or multi-dimensional NMR data (COSY, HSQC, etc.) — NMRformer is designed only for 1D 1H NMR.
- You require real-time inference or deployment on resource-constrained hardware — the full Transformer model may be computationally expensive.

## Inputs

- CSV file: two columns (chemical shift in ppm, 1H NMR spectrum intensity)
- TXT file: one detected peak chemical shift value per row (in ppm)
- Pre-trained NMRformer PyTorch model checkpoint

## Outputs

- CSV file: metabolite identities and probability scores for each input peak

## How to apply

Load the pre-trained NMRformer Transformer model using PyTorch (e.g., torch.load()). Prepare your inputs: a CSV file with chemical shift in column 1 and 1H NMR intensity in column 2, and a TXT file with one peak chemical shift value per row. Filter the peak list to remove unrecognized or noisy peaks before inference, as the model's output quality degrades when spurious peaks are included. Pass the spectrum data (via NumPy/Pandas) and filtered peak list through the NMRformer model in the provided NMRformer.ipynb notebook. The model outputs peak-to-metabolite assignments with associated probability scores. Export these assignments to output.csv for downstream analysis or validation.

## Related tools

- **NMRformer** (Pre-trained Transformer-based model for peak-to-metabolite assignment in 1D 1H NMR spectroscopy) — https://github.com/zza1211/NMRformer
- **PyTorch** (Deep learning framework for loading and executing the pre-trained Transformer model)
- **Pandas** (Data manipulation library for loading CSV spectrum files and organizing tabular peak data)
- **NumPy** (Numerical array library for spectrum data handling and preprocessing)
- **SciPy** (Scientific computing library for spectral filtering and signal processing support)

## Evaluation signals

- Output CSV contains one row per input peak with non-empty metabolite assignments and valid probability scores (0–1 range).
- The number of rows in output.csv equals the number of filtered peaks in the input TXT file.
- Metabolite names correspond to known NMR chemical shift regions (e.g., amino acids, organic acids appear in expected ppm ranges).
- Probability scores are highest for peaks at spectral positions matching known reference metabolite shifts, and lower for ambiguous or noise-like peaks.
- Re-running inference on the same input data produces identical output.csv (model is deterministic given a fixed checkpoint).

## Limitations

- Model performance is sensitive to peak list quality; noisy or unrecognized peaks degrade assignment accuracy.
- NMRformer is trained only for 1D 1H NMR; it cannot handle 2D/multi-dimensional spectra or other nuclei (13C, 31P, etc.).
- Output quality depends on the diversity of metabolites in the model's training set; rare or novel metabolites may not be reliably identified.
- No explicit uncertainty quantification or confidence intervals are provided; probability scores reflect model confidence but not external validation.

## Evidence

- [readme] Metabolite identification from 1D 1H NMR spectra is a major challenge in NMR-based metabolomics: "Metabolite identification from 1D 1H NMR spectra is a major challenge in NMR-based metabolomics"
- [readme] NMRformer is a Transformer-based deep learning framework for accurate peak assignment and metabolite identification in 1D 1H NMR spectroscopy: "NMRformer, a Transformer-based deep learning framework for accurate peak assignment and metabolite identification in 1D 1H NMR spectroscopy"
- [readme] The input CSV file has chemical shift in the first column and 1H NMR spectrum in the second; peak positions are in a TXT file: "csv file, the first column is the chemical shift, and the second column is the 1H NMR spectrum. 2. txt file, one data per row, representing the chemical shift of the peak in the spectrum"
- [readme] Noisy or unrecognized peaks in the input peak list negatively affect model output: "When you input peaks that cannot be recognized or noisy peaks into the model, it will affect the output of the model, so please try to filter the peaks in the input spectral peak list as much as"
- [readme] The model produces an output.csv file with metabolite assignments and probabilities for each peak: "output.csv file that contains the corresponding metabolites and probabilities for each peak"
