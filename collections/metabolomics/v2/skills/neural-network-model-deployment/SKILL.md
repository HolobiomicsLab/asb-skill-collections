---
name: neural-network-model-deployment
description: Use when you have LC-MS feature tables (m/z and retention time columns)
  and corresponding .mzXML or .mzML files, and you need to automatically classify
  whether extracted ion chromatograms represent genuine metabolomic features or false
  positives.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3375
  tools:
  - pyEVA
  - Python
  - Anaconda
  - PyCharm or VS Code
  - R with xcms, ggplot2, scales, dplyr
  techniques:
  - LC-MS
  - GC-MS
  - NMR
  license_tier: open
  provenance_tier: literature
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

# neural-network-model-deployment

## Summary

Deploy a trained convolutional neural network (CNN) model to perform inference on LC-MS chromatographic peak data, scoring peak quality and feature fidelity without retraining. This skill automates the assessment of extracted ion chromatogram (EIC) plots as true or false features in metabolomics pipelines.

## When to use

You have LC-MS feature tables (m/z and retention time columns) and corresponding .mzXML or .mzML files, and you need to automatically classify whether extracted ion chromatograms represent genuine metabolomic features or false positives. Use this skill after feature detection but before downstream metabolite identification, when manual EIC inspection becomes a bottleneck.

## When NOT to use

- You are performing model training or hyperparameter tuning; this skill deploys only pre-trained checkpoints.
- Your input is not LC-MS data (e.g., GC-MS, NMR, or other modalities without mzXML/mzML format support).
- You lack the .mzXML or .mzML raw data files corresponding to your feature table; the CNN requires extracted ion signals, not summary statistics alone.

## Inputs

- .csv feature table with m/z and rt columns
- .mzXML or .mzML mass spectrometry raw data file
- Pre-trained CNN model checkpoint (included in pyEVA)

## Outputs

- FinalTable.csv (feature quality scores and predictions)
- PredictionOutcomes.csv (Boolean classification per feature)
- EICplots folder (visual extracted ion chromatograms)

## How to apply

Load the pre-trained CNN model weights from pyEVA's checkpoint. Prepare your input as a .csv file with m/z and rt in the first two columns, paired with the corresponding .mzXML or .mzML mass spectrometry data files. Run the forward inference pass through the CNN by executing `python main.py` from the pyEVA environment, specifying the smoothing level (0, 1, or 2) if needed. The model will generate EIC plots and output two results files: FinalTable.csv (quality scores for each feature) and PredictionOutcomes.csv (Boolean pass/fail classifications for peak quality). This approach replaces manual visual inspection, significantly accelerating the metabolomics workflow.

## Related tools

- **pyEVA** (Python package providing pre-trained CNN model, inference engine, and EIC visualization for chromatographic peak quality scoring) — https://github.com/HuanLab/pyEVA
- **Anaconda** (Environment and package manager for setting up the Python interpreter and dependencies)
- **PyCharm or VS Code** (Integrated development environment for executing pyEVA's main.py inference pipeline)
- **R with xcms, ggplot2, scales, dplyr** (Optional downstream statistical and visualization support for metabolomics analysis results)

## Examples

```
python main.py
```

## Evaluation signals

- FinalTable.csv and PredictionOutcomes.csv are generated in the output folder with row counts matching the input feature table.
- EICplots folder contains one PNG or plot file per input feature, visually confirming EIC extraction succeeded.
- PredictionOutcomes.csv contains only Boolean values (True/False); any NaN or invalid entries indicate inference failure or data format issues.
- Quality scores in FinalTable.csv fall within the expected model output range (typically 0–1 or 0–100 depending on scaling); extreme outliers suggest data corruption.
- Runtime completes without memory errors or unhandled exceptions; execution logs confirm the correct smoothing level was applied.

## Limitations

- The CNN model was trained on a specific set of LC-MS instrumental and methodological conditions; performance may degrade on data from different platforms, ionization modes, or chromatographic columns.
- Requires both .mzXML/.mzML raw data and feature table; missing either file will cause execution failure.
- The model does not retrain; if your data distribution differs substantially from the training set, prediction accuracy may be compromised.
- Visual inspection of EIC plots is still recommended for high-stakes applications (e.g., biomarker validation) as the CNN is a screening tool, not a replacement for expert review.

## Evidence

- [readme] pyEVA is a Python-based program developed for mass-spectrometry-based research, meant to aid in fidelity checking of EIC plots from feature tables.: "pyEVA is a Python-based program developed for mass-spectrometry-based research, meant to aid in fidelity checking of EIC plots from feature tables."
- [readme] Through pyEVA's use of deep learning tools, the process of identifying EIC plots as true or false can be automated, greatly speeding up the mass spectrometry pipeline of work.: "Through pyEVA's use of deep learning tools, the process of identifying EIC plots as true or false can be automated, greatly speeding up the mass spectrometry pipeline of work."
- [readme] In `input` place a .csv file with the first two columns being `m/z` and `rt` (followed by the relevant data in successive columns), along with the related .mzXML or .mzML files.: "In `input` place a .csv file with the first two columns being `m/z` and `rt` (followed by the relevant data in successive columns), along with the related .mzXML or .mzML files."
- [readme] In the PyCharm terminal, type: `python main.py`. This should start your program. Choose the level of smoothing (0, 1, 2), and wait for the EICs to be output to the `EICplots` folder under `classifier`. In `output` there should be a .csv named `FinalTable.csv` with the results of the analysis, and a .csv called `PredictionOutcomes.csv` with Boolean values for the data input.: "In the PyCharm terminal, type: `python main.py`. This should start your program. Choose the level of smoothing (0, 1, 2), and wait for the EICs to be output to the `EICplots` folder under"
- [intro] EVA is a convolutional neural network-based platform designed to evaluate chromatographic peak quality for feature fidelity in LC-MS-based metabolomics.: "EVA is a convolutional neural network-based platform designed to evaluate chromatographic peak quality for feature fidelity in LC-MS-based metabolomics."
- [other] Initialize the trained CNN model weights from the pre-trained checkpoint provided in pyEVA.: "Initialize the trained CNN model weights from the pre-trained checkpoint provided in pyEVA."
