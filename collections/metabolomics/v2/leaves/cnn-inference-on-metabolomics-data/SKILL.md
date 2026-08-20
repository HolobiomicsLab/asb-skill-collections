---
name: cnn-inference-on-metabolomics-data
description: Use when you have LC-MS feature tables (with m/z and retention time columns)
  paired with raw .mzXML or .mzML files, and you need to automatically validate which
  detected features correspond to genuine chromatographic peaks versus false positives
  or noise.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3439
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3674
  tools:
  - pyEVA
  - Python
  - XCMS
  - ggplot2
  - Anaconda
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1021/acs.analchem.1c01309
  title: EVA
evidence_spans:
- EVA now has a python version that can be easily installed and used on Mac, PC, and
  Linux systems. Please check out pyEVA
- EVA now has a python version that can be easily installed and used on Mac, PC, and
  Linux systems
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_eva_cq
    doi: 10.1021/acs.analchem.1c01309
    title: EVA
  dedup_kept_from: coll_eva_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c01309
  all_source_dois:
  - 10.1021/acs.analchem.1c01309
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# CNN inference on metabolomics data

## Summary

Apply a pre-trained convolutional neural network to evaluate chromatographic peak quality and assess feature fidelity in LC-MS-based metabolomics datasets. This skill automates the classification of extracted ion chromatogram (EIC) plots as true or false features, replacing manual inspection.

## When to use

Use this skill when you have LC-MS feature tables (with m/z and retention time columns) paired with raw .mzXML or .mzML files, and you need to automatically validate which detected features correspond to genuine chromatographic peaks versus false positives or noise. Apply it as a quality-control gate before downstream metabolite annotation or statistical analysis.

## When NOT to use

- Input is already a validated, manually curated feature list with confirmed peak quality
- Raw mass spectrometry files (.mzXML/.mzML) are unavailable or not paired with the feature table
- Feature table lacks m/z and retention time columns in the required format (first two columns)

## Inputs

- Feature table (.csv): m/z, retention time (rt), and feature intensity columns
- Raw mass spectrometry data files (.mzXML or .mzML format)
- Smoothing parameter selection (0, 1, or 2)

## Outputs

- FinalTable.csv: feature table with CNN-derived peak quality scores
- PredictionOutcomes.csv: Boolean classification (true/false feature) for each input feature
- EIC plots (.png): extracted ion chromatograms visualized for quality inspection

## How to apply

Load the pre-trained CNN model from pyEVA and initialize it with the trained checkpoint weights. Prepare your feature table as a .csv file with m/z and rt as the first two columns, and co-locate the corresponding .mzXML or .mzML files in the input directory. Run pyEVA's main pipeline (python main.py), selecting a smoothing level (0, 1, or 2) to match your EIC preprocessing preference. The CNN performs forward inference on each feature's chromatographic signature, outputting a quality score and Boolean classification (true/false feature) for each input. Retrieve the final predictions from FinalTable.csv and PredictionOutcomes.csv in the output folder, which contain per-feature CNN scores and fidelity assignments.

## Related tools

- **pyEVA** (Python-based deep learning framework that wraps the pre-trained CNN model and orchestrates EIC extraction, preprocessing, inference, and result aggregation) — https://github.com/HuanLab/pyEVA
- **XCMS** (R package used (via RStudio) for upstream mass spectrometry feature detection and EIC plot generation)
- **ggplot2** (R package for visualizing EIC plots and diagnostic graphics)
- **Anaconda** (Python environment manager for isolating and activating the pyEVA conda environment (pyEVA))

## Examples

```
python main.py
```

## Evaluation signals

- Output files (FinalTable.csv, PredictionOutcomes.csv) are generated without runtime errors and contain the same number of rows as the input feature table
- Boolean predictions in PredictionOutcomes.csv are binary (True/False) and not null for any feature
- Peak quality scores in FinalTable.csv fall within a bounded range (e.g., [0, 1] or log-likelihood scale) and show variance across features
- EIC plots are generated and visually correspond to the input m/z and retention time values, confirming correct feature extraction
- Manual spot-check of 10–20 EIC plots and their corresponding CNN classifications agrees with domain expertise (high-confidence features show characteristic peak shapes; low-confidence features show baseline noise, shoulder peaks, or multi-modal distributions)

## Limitations

- CNN model was trained on a specific LC-MS dataset and instrument type; performance may degrade on significantly different instrument platforms, ionization modes, or chromatographic methods
- Smoothing parameter (0, 1, 2) choice affects EIC appearance and downstream CNN inference; no automated selection is provided; user must empirically validate which level is appropriate for their data
- Requires installation of external dependencies (Anaconda, R, R packages, Python packages), which may create environment conflicts on some systems
- CNN classifies peaks as binary (true/false) without confidence intervals or soft probability scores; borderline cases may not be distinguishable

## Evidence

- [intro] EVA is a convolutional neural network-based platform designed to evaluate chromatographic peak quality for feature fidelity in LC-MS-based metabolomics: "A Convolutional Neural Network-Based Platform to Evaluate Chromatographic Peak Quality for Feature Fidelity in LC-MS-based Metabolomics"
- [readme] pyEVA automates EIC classification through deep learning: "Through pyEVA's use of deep learning tools, the process of identifying EIC plots as true or false can be automated, greatly speeding up the mass spectrometry pipeline of work."
- [readme] Input format specification for pyEVA: "In `input` place a .csv file with the first two columns being `m/z` and `rt` (followed by the relevant data in successive columns), along with the related .mzXML or .mzML files."
- [readme] Output files and their contents: "In `output` there should be a .csv named `FinalTable.csv` with the results of the analysis, and a .csv called `PredictionOutcomes.csv` with Boolean values for the data input."
- [readme] Smoothing parameter choice and inference workflow: "In the PyCharm terminal, type: `python main.py`. This should start your program. Choose the level of smoothing (0, 1, 2), and wait for the EICs to be output to the `EICplots` folder"
- [intro] EVA Python availability: "EVA now has a python version that can be easily installed and used on Mac, PC, and Linux systems. Please check out pyEVA at https://github.com/HuanLab/pyEVA"
