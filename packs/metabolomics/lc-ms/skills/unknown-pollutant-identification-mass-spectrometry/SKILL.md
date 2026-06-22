---
name: unknown-pollutant-identification-mass-spectrometry
description: Use when you have UPLC-HRMS raw data (ThermoFisher, Agilent, or compatible vendor format) from water samples or environmental matrices containing unknown organic pollutants, a Windows environment with ≥16 GB RAM and ≥2 GB NVIDIA GPU, and you need compound identification with confidence scores and.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0154
  tools:
  - MSThunder
  - Windows
  - MSConvert
  - GNPS
  techniques:
  - LC-MS
derived_from:
- doi: 10.1016/j.enceco.2025.07.022
  title: MSThunder
- doi: 10.5281/zenodo.12602805
  title: ''
evidence_spans:
- MSThunder provide a deep learning-based nontargeted analytical framework for the accurate and rapid identification of unknown organic pollutants in water
- A case file named “Pesticides” can be run in the Windows environment
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_msthunder_cq
    doi: 10.1016/j.enceco.2025.07.022
    title: MSThunder
  dedup_kept_from: coll_msthunder_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1016/j.enceco.2025.07.022
  all_source_dois:
  - 10.1016/j.enceco.2025.07.022
  - 10.5281/zenodo.12602805
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# unknown-pollutant-identification-mass-spectrometry

## Summary

Execute MSThunder's deep learning-based nontargeted analytical workflow to identify unknown organic pollutants in UPLC-HRMS data by matching precursor ions, MS/MS spectra, and molecular formulas against trained models and spectral libraries. Use this skill when analyzing water samples or environmental matrices for unidentified contaminants where reference standards are unavailable.

## When to use

You have UPLC-HRMS raw data (ThermoFisher, Agilent, or compatible vendor format) from water samples or environmental matrices containing unknown organic pollutants, a Windows environment with ≥16 GB RAM and ≥2 GB NVIDIA GPU, and you need compound identification with confidence scores and matched spectral library annotations rather than targeted screening against a known compound list.

## When NOT to use

- Raw UPLC-HRMS data from non-standard vendors or formats not compatible with MSConvert — current version does not support offline raw data processing and requires pre-conversion.
- Analysis goal is targeted quantification or screening against a pre-defined compound list — MSThunder is designed for nontargeted identification of unknowns, not targeted screening.
- Hardware unavailable: Windows environment with <16 GB RAM or no NVIDIA GPU — the interface requires these specifications and will not run on Linux or macOS natively.

## Inputs

- UPLC-HRMS raw data files (ThermoFisher .raw, Agilent .d, or MSConvert-converted format)
- Batch-processed mass spectrometry data files (placed in MSThunder directory)
- Precursor m/z and retention time specifications
- Ion mode selection (Positive or Negative)

## Outputs

- Candidate compound names ranked by deep learning prediction score
- Molecular formula predictions
- MS/MS spectrum matches to spectral library entries
- Structure diagrams (SMILES rendering)
- Confidence/matching scores for each candidate

## How to apply

Decompress msthunder.rar and msthunderfile.rar from Zenodo (doi.org/10.5281/zenodo.12602805) into a Windows environment meeting hardware requirements. If working with raw vendor data, first convert to MSConvert-compatible format using a Linux system (Ubuntu 20.04), send the converted file to the MSThunder developers, or upload to GNPS/Zenodo; the developers will return pre-processed files ready for analysis. Load batch-processed files into the MSThunder interface, specify ion mode (Positive or Negative), then execute the deep learning structure prediction workflow: input precursor m/z and retention time, retrieve MS1 and MS2 spectra, predict molecular formulas, and rank candidate structures using the trained model. The interface returns compound name candidates ranked by score, reference spectrum matches (if found in top 10), and structure diagrams. Judge success by presence of high-confidence candidates (reference spectra matched), chemical plausibility of predicted structures, and consistency between MS1 mass accuracy and proposed molecular formula.

## Related tools

- **MSThunder** (Deep learning-based nontargeted analytical interface for executing structure prediction and candidate ranking on MS/MS data) — https://github.com/LQZ0123/MSThunder
- **MSConvert** (Convert raw mass spectrometry data from ThermoFisher, Agilent, and other vendors into formats compatible with MSThunder preprocessing)
- **GNPS** (Online spectral library database for uploading raw UPLC-HRMS data for preprocessing and candidate reference spectrum matching)

## Evaluation signals

- MSThunder returns ≥1 candidate compound with reference spectrum matched in top 10 ranked structures and confidence score displayed in Ranking section
- Predicted molecular formula is chemically plausible (mass accuracy ≤5 ppm deviation from observed precursor m/z) and consistent across multiple MS1 scans at the specified retention time
- MS2 spectrum similarity between observed fragmentation pattern and library reference is visualized in MS2-candidate panel with visible peak matches
- Structure diagram renders without errors in SMILES/Structure sections and matches expected chemical class (e.g., pesticide, pharmaceutical)
- Ion mode selection (Positive/Negative) produces candidate formulas with appropriate charge state and isotope pattern (M+H or M−H)

## Limitations

- Current version does not support offline processing of raw UPLC-HRMS data; users must convert via external tools (MSConvert in Linux) or send raw files to developers for preprocessing.
- Windows-only interface mode; Ubuntu 20.04 training and code are available but the interactive GUI requires Windows with NVIDIA GPU.
- Online processing capability for raw UPLC-HRMS data is under development; interim workflow requires manual file transfer to developers or public database (GNPS/Zenodo).
- Image display may fail at high screen resolutions; workaround is to decrease computer display ratio to render structure diagrams and spectral plots correctly.
- No changelog or version history documented; updates to deep learning model, spectral library, and Python dependencies are not tracked.

## Evidence

- [readme] deep learning-based nontargeted analytical framework for the accurate and rapid identification of unknown organic pollutants in water: "MSThunder provide a deep learning-based nontargeted analytical framework for the accurate and rapid identification of unknown organic pollutants in water."
- [readme] Pesticides case file runs on Windows with 16 GB RAM and 2 GB NVIDIA GPU: "A case file named "Pesticides" can be run in the Windows environment equipped with 16 GB of RAM and a 2 GB NVIDIA GPU."
- [readme] Decompression of RAR files from Zenodo required for interface access: "The interface mode of MSThunder is available by decompressing in the file in RAR format (msthunder.rar and msthunderfile.rar) (doi.org/10.5281/zenodo.12602805)."
- [readme] Current version does not support offline raw data processing: "Due to environment configuration issues, the current version does not yet support offline processing of raw data."
- [readme] MSConvert required for vendor data conversion; Linux preprocessing workflow needed before MSThunder analysis: "The current version is compatible with ThermoFisher, Agilent, and other vendors whose raw data can be converted via MSConvert. Then, you can subsequently analyze the data using MSThunder after our"
- [readme] Double-click workflows to execute structure prediction and view ranking results: "Double-click the precursor formula to execute the structure prediction function for that molecular formula; the candidate score information will be displayed in Ranking."
- [readme] Online processing capability is under active development: "We are developing the relevant functionality and will make it available online as soon as possible."
