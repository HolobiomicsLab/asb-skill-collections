---
name: feature-fidelity-prediction
description: Use when you have a feature table (CSV with m/z and retention time columns)
  and corresponding .mzXML or .mzML mass spectrometry files from an LC-MS metabolomics
  experiment, and you need to filter out false or low-quality chromatographic peaks
  before downstream analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3678
  tools:
  - pyEVA
  - Python
  - XCMS (R package)
  - Anaconda
  - PyCharm / VS Code
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

# feature-fidelity-prediction

## Summary

Use a pre-trained convolutional neural network to automatically classify chromatographic peaks from LC-MS data as true or false features, assigning quality scores to assess feature fidelity. This skill accelerates metabolomics pipelines by replacing manual EIC (extracted ion chromatogram) inspection with deep learning-based automated peak quality assessment.

## When to use

You have a feature table (CSV with m/z and retention time columns) and corresponding .mzXML or .mzML mass spectrometry files from an LC-MS metabolomics experiment, and you need to filter out false or low-quality chromatographic peaks before downstream analysis. Apply this skill when manual visual inspection of EIC plots is impractical due to dataset size or when you need reproducible, automated quality control of feature detection.

## When NOT to use

- Input data are already manually curated or pre-filtered for feature fidelity; CNN re-scoring adds no new information.
- Mass spectrometry data are in unsupported formats (not .mzXML or .mzML); pre-convert or use alternative tools.
- Feature table lacks m/z and retention time columns or is in a non-CSV tabular format; reformat first.

## Inputs

- CSV feature table with m/z and rt columns (first two columns), followed by additional feature metadata
- .mzXML or .mzML mass spectrometry data files (corresponding to the feature table)

## Outputs

- FinalTable.csv — feature table annotated with quality scores and predictions
- PredictionOutcomes.csv — Boolean predictions (true/false) for each input feature
- EICplots/ folder — visual chromatogram plots for inspection and validation

## How to apply

Install pyEVA and its dependencies (Anaconda, PyCharm or VS Code, R with XCMS/ggplot2/scales/dplyr packages) following the README setup instructions. Place your feature table (CSV with m/z and rt columns) and .mzXML/.mzML files in the Input folder. Run `python main.py` and select a smoothing level (0, 1, or 2)—this controls preprocessing of the EIC chromatograms before CNN inference. The trained CNN model automatically evaluates each peak's morphology and signal characteristics, outputting a Boolean classification (true/false feature) and quality scores. The rationale is that the CNN has learned to distinguish genuine peaks from noise or artifacts by training on labeled EIC plots, thereby automating what was previously a manual, subjective step.

## Related tools

- **pyEVA** (Python-based CNN platform that loads pre-trained model weights and runs forward inference to score chromatographic peak quality) — https://github.com/HuanLab/pyEVA
- **Python** (Execution environment for pyEVA; version 3.7.12 or compatible)
- **XCMS (R package)** (Preprocessing and feature extraction from raw mass spectrometry data; used in the pyEVA pipeline to generate EIC plots)
- **Anaconda** (Conda environment manager for dependency installation and virtual environment setup)
- **PyCharm / VS Code** (IDE for running pyEVA main.py and managing the project workflow)

## Examples

```
python main.py
```

## Evaluation signals

- FinalTable.csv is produced in the Output folder with the same row count as the input feature table and new quality/prediction columns.
- PredictionOutcomes.csv contains only Boolean values (true/false) with no missing entries for any input feature.
- EICplots/ folder contains PNG or equivalent visualizations for a representative subset of peaks, allowing manual spot-check of CNN predictions against visual chromatogram quality.
- Quality scores fall within the expected range (e.g., 0–1 or 0–100) without extreme outliers or NaN values.
- Runtime completes without errors and logs smoothing level chosen and total features processed.

## Limitations

- The CNN model is trained on specific types of LC-MS peak patterns; performance may degrade on data from different instrument platforms, ionization methods, or metabolite classes not represented in training data.
- Smoothing level (0, 1, 2) is a user-selected parameter; suboptimal choice may reduce classification accuracy. No automatic tuning is provided.
- Requires installation of multiple dependencies (R, PyCharm/VS Code, Anaconda, R packages); setup complexity may be a barrier for users unfamiliar with conda environments.
- The tool is designed for feature-level assessment and does not perform sample-level or compound-level filtering; output must be integrated into downstream pipelines manually.
- Pre-trained model weights are fixed and not updated during use; retraining on new datasets is not documented in the README.

## Evidence

- [readme] pyEVA is a Python-based program developed for mass-spectrometry-based research, meant to aid in fidelity checking of EIC plots from feature tables.: "pyEVA is a Python-based program developed for mass-spectrometry-based research, meant to aid in fidelity checking of EIC plots from feature tables."
- [readme] Through pyEVA's use of deep learning tools, the process of identifying EIC plots as true or false can be automated, greatly speeding up the mass spectrometry pipeline of work.: "Through pyEVA's use of deep learning tools, the process of identifying EIC plots as true or false can be automated, greatly speeding up the mass spectrometry pipeline"
- [readme] In `input` place a .csv file with the first two columns being `m/z` and `rt` (followed by the relevant data in successive columns), along with the related .mzXML or .mzML files.: "In `input` place a .csv file with the first two columns being `m/z` and `rt` (followed by the relevant data in successive columns), along with the related .mzXML or .mzML files."
- [readme] In the PyCharm terminal, type: `python main.py`. This should start your program. Choose the level of smoothing (0, 1, 2), and wait for the EICs to be output to the `EICplots` folder under `classifier`.: "In the PyCharm terminal, type: `python main.py`. This should start your program. Choose the level of smoothing (0, 1, 2), and wait for the EICs to be output to the `EICplots` folder"
- [readme] In `output` there should be a .csv named `FinalTable.csv` with the results of the analysis, and a .csv called `PredictionOutcomes.csv` with Boolean values for the data input.: "In `output` there should be a .csv named `FinalTable.csv` with the results of the analysis, and a .csv called `PredictionOutcomes.csv` with Boolean values for the data input."
- [intro] EVA is a convolutional neural network-based platform designed to evaluate chromatographic peak quality for feature fidelity in LC-MS-based metabolomics.: "EVA is a convolutional neural network-based platform designed to evaluate chromatographic peak quality for feature fidelity in LC-MS-based metabolomics."
- [readme] Initially written in C# and published by Guo et al. in 2021 as EVA, to aid in ease-of-use and multi-platform usage we have rewritten it in Python.: "Initially written in C# and published by Guo et al. in 2021 as EVA, to aid in ease-of-use and multi-platform usage we have rewritten it in Python."
