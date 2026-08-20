---
name: lc-ms-peak-feature-engineering
description: Use when you have LC-MS feature tables with m/z and retention time coordinates
  paired with raw .mzXML or .mzML data files, and you need to systematically assess
  which features correspond to genuine chromatographic peaks versus noise or artifacts.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - pyEVA
  - Python
  - XCMS
  - Anaconda
  techniques:
  - LC-MS
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

# LC-MS Peak Feature Engineering

## Summary

Engineer and validate chromatographic peak quality features from LC-MS data using a convolutional neural network trained to discriminate true from false extracted ion chromatogram (EIC) plots. This skill automates the laborious process of manual EIC fidelity assessment in metabolomics feature tables.

## When to use

Apply this skill when you have LC-MS feature tables with m/z and retention time coordinates paired with raw .mzXML or .mzML data files, and you need to systematically assess which features correspond to genuine chromatographic peaks versus noise or artifacts. Use it as a quality-control gate before downstream metabolomics analysis to improve feature set fidelity.

## When NOT to use

- Input feature table is already manually curated or has been pre-filtered by established peak-picking algorithms and validated—reapplying CNN classification risks redundant computation.
- Raw mass spectrometry files are in non-standard formats (e.g., vendor-proprietary .raw or .d without conversion to mzXML/mzML)—pyEVA requires open formats.
- Analysis goal is targeted quantitation of known compounds with pre-established m/z and rt windows; use the CNN when comprehensive, unbiased peak quality assessment across the full feature space is needed.

## Inputs

- LC-MS feature table (CSV): first two columns m/z and rt, additional columns for other feature properties
- Raw mass spectrometry data files (.mzXML or .mzML format)
- Pre-trained CNN model weights (provided in pyEVA checkpoint)

## Outputs

- FinalTable.csv: original feature table annotated with peak quality scores and fidelity predictions
- PredictionOutcomes.csv: Boolean classification for each feature (true/false peak)
- EICplots folder: rendered extracted ion chromatogram images for visual verification

## How to apply

Load your LC-MS feature table (CSV format with m/z and rt columns) and corresponding mass spectrometry data files (.mzXML or .mzML) into the pyEVA input directory. Initialize the pre-trained CNN model from the pyEVA checkpoint to extract EIC plots for each feature at the specified m/z and retention time. Process EICs through optional smoothing levels (0, 1, or 2) to denoise before CNN inference. Run the forward pass to compute peak quality predictions, which output Boolean classification (true/false peak) and confidence scores. Export results as FinalTable.csv with quality annotations and PredictionOutcomes.csv with binary verdicts for downstream filtering.

## Related tools

- **pyEVA** (Python-based CNN inference framework; loads pre-trained deep-learning model, orchestrates EIC extraction from raw data, performs forward pass to predict peak quality, and exports classification results) — https://github.com/HuanLab/pyEVA
- **XCMS** (R package for upstream LC-MS feature detection and peak picking; generates initial feature table that pyEVA then refines via CNN-based fidelity checking)
- **Anaconda** (Python environment and package manager; required to set up isolated pyEVA conda environment with pinned dependency versions)

## Examples

```
python main.py
```

## Evaluation signals

- Schema validation: FinalTable.csv and PredictionOutcomes.csv contain exactly one row per input feature and Boolean/numeric values conform to expected ranges (confidence scores 0–1, predictions True/False).
- Consistency check: All features in PredictionOutcomes.csv have a corresponding row in FinalTable.csv with matching m/z and rt values.
- Visual spot-check: A random sample of EICplots output images should display well-resolved, Gaussian-like peak shapes for features predicted True and noisy or multipeak patterns for features predicted False.
- Convergence: Running the same input data twice produces identical predictions, verifying deterministic model inference.
- Benchmarking (if validation set available): Compute precision, recall, and F1-score of CNN predictions against manually labeled peak/no-peak ground truth to confirm the model performs within documented accuracy bounds.

## Limitations

- CNN model accuracy depends on the representativeness of its training set (Guo et al. 2021); peak quality predictions may degrade for LC-MS modes, ionization techniques, or chromatographic conditions not well represented in training data.
- EIC extraction and rendering require exact m/z and retention time coordinates; features with poor mass accuracy or misaligned rt values may produce uninformative or empty EIC plots, leading to unreliable predictions.
- The method is computationally intensive for very large feature tables; processing time scales with the number of features and the resolution of raw data files.
- Smoothing level (0, 1, 2) is a manual hyperparameter; suboptimal smoothing may suppress weak true peaks or amplify noise, affecting classifier confidence; no automated selection is provided.

## Evidence

- [readme] pyEVA is a Python-based program developed for mass-spectrometry-based research, meant to aid in fidelity checking of EIC plots from feature tables.: "pyEVA is a Python-based program developed for mass-spectrometry-based research, meant to aid in fidelity checking of EIC plots from feature tables."
- [readme] Through pyEVA's use of deep learning tools, the process of identifying EIC plots as true or false can be automated, greatly speeding up the mass spectrometry pipeline of work.: "Through pyEVA's use of deep learning tools, the process of identifying EIC plots as true or false can be automated, greatly speeding up the mass spectrometry pipeline of work."
- [readme] In `input` place a .csv file with the first two columns being `m/z` and `rt` (followed by the relevant data in successive columns), along with the related .mzXML or .mzML files.: "In `input` place a .csv file with the first two columns being `m/z` and `rt` (followed by the relevant data in successive columns), along with the related .mzXML or .mzML files."
- [readme] Choose the level of smoothing (0, 1, 2), and wait for the EICs to be output to the `EICplots` folder under `classifier`. In `output` there should be a .csv named `FinalTable.csv` with the results of the analysis, and a .csv called `PredictionOutcomes.csv` with Boolean values for the data input.: "Choose the level of smoothing (0, 1, 2), and wait for the EICs to be output to the `EICplots` folder under `classifier`. In `output` there should be a .csv named `FinalTable.csv` with the results of"
- [other] EVA is a convolutional neural network-based platform designed to evaluate chromatographic peak quality for feature fidelity in LC-MS-based metabolomics.: "EVA is a convolutional neural network-based platform designed to evaluate chromatographic peak quality for feature fidelity in LC-MS-based metabolomics."
