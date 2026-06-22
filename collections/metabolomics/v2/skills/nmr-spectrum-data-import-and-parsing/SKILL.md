---
name: nmr-spectrum-data-import-and-parsing
description: Use when you have raw 1D ¹H NMR spectroscopy output consisting of (1) a CSV file with chemical shift and intensity columns and (2) a TXT file listing detected peak chemical shifts, and you need to load and validate these into memory before passing them to a metabolite identification model like.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3501
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0769
  tools:
  - PyTorch
  - NumPy
  - Pandas
  - SciPy
  - NMRformer.ipynb
  techniques:
  - NMR
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

# nmr-spectrum-data-import-and-parsing

## Summary

Import and parse 1D ¹H NMR spectrum data and peak lists from CSV and TXT files into structured Python objects for downstream metabolite identification. This skill prepares raw NMR instrumental output for Transformer-based peak assignment by standardizing file formats and validating data integrity.

## When to use

You have raw 1D ¹H NMR spectroscopy output consisting of (1) a CSV file with chemical shift and intensity columns and (2) a TXT file listing detected peak chemical shifts, and you need to load and validate these into memory before passing them to a metabolite identification model like NMRformer.

## When NOT to use

- Peak list has already been manually curated and filtered by domain experts; skip to model inference.
- Input is 2D or higher-dimensional NMR (e.g., COSY, HSQC); this skill is specific to 1D ¹H NMR.
- Spectrum data is in a non-CSV format (e.g., raw instrument binary, NetCDF, Bruker FID) that requires vendor-specific parsers.

## Inputs

- CSV file with chemical shift (column 1) and 1H NMR spectrum intensity (column 2)
- TXT file with one peak chemical shift per row

## Outputs

- Parsed spectrum array (chemical shift, intensity pairs)
- Validated peak list array (chemical shift values)
- Filtered peak list (unrecognized and noisy peaks removed)

## How to apply

Use Pandas to read the CSV file (chemical shift in first column, spectrum intensity in second column) and NumPy to read the peak-list TXT file (one chemical shift per row). Combine these into structured arrays or DataFrames that preserve the mapping between chemical shift coordinates and spectral intensity values. Before proceeding to model inference, apply a peak-filtering step to remove unrecognized or noisy peaks from the peak list, as the README explicitly warns that such peaks 'will affect the output of the model'. Validation should confirm that all peak positions in the TXT file correspond to local maxima or significant intensity points in the CSV spectrum data.

## Related tools

- **Pandas** (Read and parse CSV spectrum file into DataFrame)
- **NumPy** (Load peak list TXT file and manipulate array structures)
- **SciPy** (Optional: signal processing for peak validation and noise detection)
- **NMRformer.ipynb** (Jupyter notebook that orchestrates model loading, data import, and inference) — https://github.com/zza1211/NMRformer

## Examples

```
import pandas as pd; import numpy as np; spectrum = pd.read_csv('input_spectrum.csv', header=None); peaks = np.loadtxt('input_peaks.txt'); peaks_filtered = peaks[(spectrum.iloc[np.searchsorted(spectrum[0], peaks), 1] > threshold).values]
```

## Evaluation signals

- CSV spectrum file loads without errors; verify shape is (n_chemical_shifts, 2) with numeric dtypes.
- Peak list TXT file loads without errors; all entries are numeric chemical shift values within expected range (typically 0–10 ppm for ¹H NMR).
- All peak chemical shifts in the filtered list correspond to local maxima or intensity thresholds in the spectrum array (no peaks assigned to zero or near-zero intensity regions).
- Peak list length after filtering is smaller than before; at least one noisy or unrecognized peak was removed.
- Output.csv file is successfully generated after model inference; contains metabolite assignments for each retained peak with associated probability scores.

## Limitations

- The skill does not perform automated baseline correction or solvent-peak removal; users must pre-process spectrum intensities externally if needed.
- Peak filtering is heuristic-based; the README warns that 'noisy peaks or unrecognized peaks' will degrade model output, but does not provide algorithmic thresholds (e.g., intensity cutoff, S/N ratio). Users must apply domain knowledge or manual curation.
- No built-in support for handling missing data, NaN values, or non-monotonic chemical shift columns in the CSV; data quality checks are the user's responsibility.
- Input files must be in exact CSV and TXT format as specified; no auto-detection of delimiters, encodings, or alternative formats is mentioned in the README.

## Evidence

- [intro] Import the spectrum data from the input CSV file and peak-list data from the input TXT file using Pandas and NumPy.: "Import the spectrum data from the input CSV file and peak-list data from the input TXT file using Pandas and NumPy."
- [readme] When you input peaks that cannot be recognized or noisy peaks into the model, it will affect the output of the model, so please try to filter the peaks in the input spectral peak list as much as possible.: "When you input peaks that cannot be recognized or noisy peaks into the model, it will affect the output of the model, so please try to filter the peaks in the input spectral peak list as much as"
- [readme] csv file, the first column is the chemical shift, and the second column is the 1H NMR spectrum.: "csv file, the first column is the chemical shift, and the second column is the 1H NMR spectrum."
- [readme] txt file, one data per row, representing the chemical shift of the peak in the spectrum.: "txt file, one data per row, representing the chemical shift of the peak in the spectrum."
- [readme] In NMRformer.ipynb, you can load the model and input data, resulting in an output.csv file that contains the corresponding metabolites and probabilities for each peak.: "In NMRformer.ipynb, you can load the model and input data, resulting in an output.csv file that contains the corresponding metabolites and probabilities for each peak."
