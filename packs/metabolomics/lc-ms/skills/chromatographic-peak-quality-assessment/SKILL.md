---
name: chromatographic-peak-quality-assessment
description: Use when when you have a feature table (CSV with m/z and retention time columns) and corresponding LC-MS raw data files (.mzXML or .mzML) from an untargeted metabolomics experiment, and need to filter out spurious peaks before downstream statistical or biological interpretation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3643
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3172
  tools:
  - pyEVA
  - Python
  - XCMS
  - Anaconda
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.1c01309
  title: EVA
evidence_spans:
- EVA now has a python version that can be easily installed and used on Mac, PC, and Linux systems. Please check out pyEVA
- EVA now has a python version that can be easily installed and used on Mac, PC, and Linux systems
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# chromatographic-peak-quality-assessment

## Summary

Employ a convolutional neural network to automatically classify extracted ion chromatogram (EIC) peaks as true or false features in LC-MS-based metabolomics data, replacing manual curation and accelerating feature table validation. This skill evaluates whether detected peaks represent genuine metabolite signals or false positives based on peak morphology and fidelity.

## When to use

When you have a feature table (CSV with m/z and retention time columns) and corresponding LC-MS raw data files (.mzXML or .mzML) from an untargeted metabolomics experiment, and need to filter out spurious peaks before downstream statistical or biological interpretation. Use this skill after feature detection (e.g., XCMS output) but before biological analysis when manual peak inspection is infeasible or you need reproducible, high-throughput quality assessment.

## When NOT to use

- If your input is already a manually curated or experimentally validated feature table; the CNN is designed for automated triage of unfiltered feature detection output.
- If you lack the corresponding raw .mzXML or .mzML files; the model requires EIC extraction from original MS data and cannot work on peak intensity tables alone.
- If your LC-MS data comes from a radically different instrument class or chromatographic protocol than the training data; the CNN may not generalize to markedly different peak morphologies or baseline noise profiles.

## Inputs

- CSV feature table with m/z and retention time in first two columns
- .mzXML or .mzML mass spectrometry raw data files
- Smoothing parameter (integer: 0, 1, or 2)

## Outputs

- EIC plots (PNG/visual format in EICplots folder)
- FinalTable.csv with quality scores for each feature
- PredictionOutcomes.csv with Boolean true/false classifications

## How to apply

Load the pyEVA CNN model and pre-trained weights from the GitHub repository. Prepare your feature table as a CSV with m/z and retention time in the first two columns, followed by relevant data columns; co-locate the corresponding .mzXML or .mzML mass spectrometry files in the input folder. Select a smoothing level (0, 1, or 2) and run the forward pass through the CNN, which generates extracted ion chromatogram (EIC) plots and outputs a Boolean classification (true/false) for each peak. The model produces two output CSVs: FinalTable.csv (with quality scores) and PredictionOutcomes.csv (with Boolean classifications), allowing you to filter the feature table to retain only high-confidence peaks. The CNN architecture learned peak morphology patterns from training data, so the rationale is that peaks with characteristic shapes and intensity profiles are more likely to be true signals.

## Related tools

- **pyEVA** (Python implementation of the CNN model for automated EIC peak quality classification; runs forward inference and outputs quality scores and Boolean predictions) — https://github.com/HuanLab/pyEVA
- **XCMS** (R package for upstream feature detection in LC-MS data; pyEVA typically receives feature tables from XCMS output)
- **Python** (Runtime environment for executing pyEVA; version 3.7.12 or later required)
- **Anaconda** (Conda environment manager for dependency and package installation)

## Examples

```
python main.py
```

## Evaluation signals

- Output CSV files (FinalTable.csv, PredictionOutcomes.csv) are generated without errors and contain entries for all input features.
- EIC plot images are created in the EICplots folder; visual inspection confirms that peaks classified as 'true' have characteristic Gaussian-like shapes while 'false' peaks show baseline noise or jagged morphology.
- Boolean predictions in PredictionOutcomes.csv are binary (true/false) with no null or out-of-range values.
- When compared to manual curation (if available), the CNN's classifications show reasonable sensitivity and specificity for the target MS platform; disagreements should be traceable to genuine ambiguities rather than systematic bias.
- Feature count reduction after filtering matches expected noise ratio; typically 20–40% of raw features are expected to be false positives in untargeted metabolomics.

## Limitations

- The CNN was trained on LC-MS peak morphology patterns from a specific set of instruments and chromatographic conditions; transfer to markedly different MS platforms or column chemistries may degrade performance.
- Requires co-located raw .mzXML or .mzML files with matching feature identifiers; incomplete or misaligned raw data will cause processing failures or incorrect EIC extraction.
- Smoothing parameter (0, 1, 2) choice is user-specified and not adaptive; suboptimal smoothing can affect EIC quality and downstream CNN inference.
- The model outputs Boolean classifications without confidence scores or probability calibration in the standard output, limiting nuanced filtering at intermediate thresholds.

## Evidence

- [readme] pyEVA is a Python-based program developed for mass-spectrometry-based research, meant to aid in fidelity checking of EIC plots from feature tables.: "pyEVA is a Python-based program developed for mass-spectrometry-based research, meant to aid in fidelity checking of EIC plots from feature tables."
- [readme] Through pyEVA's use of deep learning tools, the process of identifying EIC plots as true or false can be automated, greatly speeding up the mass spectrometry pipeline of work.: "Through pyEVA's use of deep learning tools, the process of identifying EIC plots as true or false can be automated, greatly speeding up the mass spectrometry pipeline of work."
- [readme] In `input` place a .csv file with the first two columns being `m/z` and `rt` (followed by the relevant data in successive columns), along with the related .mzXML or .mzML files.: "In `input` place a .csv file with the first two columns being `m/z` and `rt` (followed by the relevant data in successive columns), along with the related .mzXML or .mzML files."
- [readme] In `output` there should be a .csv named `FinalTable.csv` with the results of the analysis, and a .csv called `PredictionOutcomes.csv` with Boolean values for the data input.: "In `output` there should be a .csv named `FinalTable.csv` with the results of the analysis, and a .csv called `PredictionOutcomes.csv` with Boolean values for the data input."
- [other] EVA is a convolutional neural network-based platform designed to evaluate chromatographic peak quality for feature fidelity in LC-MS-based metabolomics.: "EVA is a convolutional neural network-based platform designed to evaluate chromatographic peak quality for feature fidelity in LC-MS-based metabolomics."
- [readme] Choose the level of smoothing (0, 1, 2), and wait for the EICs to be output to the `EICplots` folder under `classifier`.: "Choose the level of smoothing (0, 1, 2), and wait for the EICs to be output to the `EICplots` folder under `classifier`."
