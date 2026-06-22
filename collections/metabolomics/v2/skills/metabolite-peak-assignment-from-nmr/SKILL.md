---
name: metabolite-peak-assignment-from-nmr
description: Use when you have a 1D ¹H NMR spectrum (as chemical shift vs. intensity) and a corresponding peak list (chemical shift values), and you need to identify which metabolites are responsible for each detected peak.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3860
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
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

# metabolite-peak-assignment-from-nmr

## Summary

Apply a Transformer-based deep learning model (NMRformer) to assign chemical peaks in 1D ¹H NMR spectra to their corresponding metabolites. This skill automates the challenging task of peak-to-metabolite mapping by processing filtered spectral data through a learned neural network, producing probability-ranked metabolite identifications.

## When to use

You have a 1D ¹H NMR spectrum (as chemical shift vs. intensity) and a corresponding peak list (chemical shift values), and you need to identify which metabolites are responsible for each detected peak. Use this skill when manual peak assignment is infeasible or when you want to leverage learned patterns from large NMR training data to improve assignment accuracy and consistency.

## When NOT to use

- Input peak list is already known to contain many unfiltered, noisy, or artifact peaks—preprocess with domain expertise or signal-processing filters before invoking this skill.
- You are analyzing a different NMR experiment type (e.g., 2D COSY, HSQC, or ¹³C NMR)—NMRformer is trained on 1D ¹H NMR only.
- Your spectral data is in a non-standard format (e.g., raw instrument binary, netCDF, Bruker FID) and has not been converted to the required CSV/TXT format.

## Inputs

- CSV file with two columns: chemical shift (ppm) and ¹H NMR spectral intensity
- TXT file with one peak chemical shift (ppm) per row
- Pre-trained NMRformer PyTorch model checkpoint

## Outputs

- output.csv file containing metabolite identifications, chemical shift assignments, and probability scores for each input peak

## How to apply

Load the pre-trained NMRformer PyTorch model from the repository. Import your spectrum as a CSV file (first column: chemical shift, second column: intensity) and peak list as a TXT file (one chemical shift per row). Before passing data to the model, filter the peak list to remove unrecognized or noisy peaks—the model's output is sensitive to spurious peaks, so this curation step is critical. Pass the cleaned spectrum and peak data through the NMRformer Transformer encoder to generate peak-to-metabolite assignments with associated probabilities. Export the results to output.csv, which will contain metabolite names and confidence scores for each input peak.

## Related tools

- **NMRformer** (Transformer-based neural network model that encodes filtered peak and spectrum data to predict metabolite assignments) — https://github.com/zza1211/NMRformer
- **PyTorch** (Deep learning framework for loading and executing the pre-trained NMRformer model)
- **Pandas** (Data import and manipulation for reading CSV spectrum files and structuring output results)
- **NumPy** (Numerical computation and array operations on spectral intensity and peak data)
- **SciPy** (Signal processing utilities for optional peak filtering and noise detection)

## Examples

```
# In NMRformer.ipynb: load model, import spectrum from example_data/spectrum.csv and peaks from example_data/peaks.txt, filter peaks, pass through model, export output.csv
```

## Evaluation signals

- output.csv contains one row per input peak with non-null metabolite identifications and probability scores between 0 and 1
- Metabolite assignments match known reference standards or prior manual curation for a subset of test peaks (e.g., validation accuracy > 80%)
- No rows in output.csv have missing or NaN metabolite names or probability values
- Peak chemical shifts in output.csv match the input peak list within floating-point precision (±1e-6 ppm)
- Probability scores are sorted or ranked consistently (e.g., highest-confidence metabolite listed first per peak)

## Limitations

- Model performance degrades significantly when input peak lists contain unrecognized or noisy peaks; manual pre-filtering is essential.
- NMRformer is trained exclusively on 1D ¹H NMR spectra; applicability to other modalities (2D, ¹³C, DEPT) is unknown.
- Output probabilities reflect model confidence, not ground-truth accuracy; results should be validated against experimental standards or orthogonal methods.
- No changelog or version history is provided, making it unclear how model performance may vary across updates or different checkpoint versions.
- Performance on metabolites outside the training set or in complex biological matrices with many co-eluting compounds is not characterized.

## Evidence

- [readme] Metabolite identification from 1D 1H NMR spectra is a major challenge in NMR-based metabolomics.: "Metabolite identification from 1D 1H NMR spectra is a major challenge in NMR-based metabolomics"
- [readme] NMRformer is a Transformer-based deep learning framework for accurate peak assignment and metabolite identification in 1D 1H NMR spectroscopy.: "NMRformer, a Transformer-based deep learning framework for accurate peak assignment and metabolite identification in 1D 1H NMR spectroscopy"
- [readme] When you input peaks that cannot be recognized or noisy peaks into the model, it will affect the output of the model, so please try to filter the peaks in the input spectral peak list as much as possible.: "When you input peaks that cannot be recognized or noisy peaks into the model, it will affect the output of the model, so please try to filter the peaks in the input spectral peak list as much as"
- [readme] In NMRformer.ipynb, you can load the model and input data, resulting in an output.csv file that contains the corresponding metabolites and probabilities for each peak.: "In NMRformer.ipynb, you can load the model and input data, resulting in an output.csv file that contains the corresponding metabolites and probabilities for each peak"
- [readme] The uploaded files include: 1. csv file, the first column is the chemical shift, and the second column is the 1H NMR spectrum. 2. txt file, one data per row, representing the chemical shift of the peak in the spectrum.: "csv file, the first column is the chemical shift, and the second column is the 1H NMR spectrum. 2. txt file, one data per row, representing the chemical shift of the peak"
