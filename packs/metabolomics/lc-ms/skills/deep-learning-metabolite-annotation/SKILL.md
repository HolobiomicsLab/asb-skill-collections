---
name: deep-learning-metabolite-annotation
description: Use when you have UPLC-HRMS data (ThermoFisher, Agilent, or MSConvert-compatible format) from a water sample, a precursor m/z and retention time of interest, and want to annotate an unknown compound by predicting its molecular formula, structure, and name using deep learning scoring rather than.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3520
  tools:
  - MSThunder
  - Windows
  - MSConvert
  - Linux preprocessing environment (Ubuntu 20.04)
  techniques:
  - LC-MS
  - NMR
derived_from:
- doi: 10.1016/j.enceco.2025.07.022
  title: MSThunder
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# deep-learning-metabolite-annotation

## Summary

Use MSThunder's deep learning-based nontargeted analytical framework to identify unknown organic pollutants in UPLC-HRMS water samples by matching experimental MS1/MS2 spectra against learned representations and candidate chemical libraries. This skill enables rapid, accurate compound annotation when reference spectra are unavailable or when targeting unknown contaminants.

## When to use

You have UPLC-HRMS data (ThermoFisher, Agilent, or MSConvert-compatible format) from a water sample, a precursor m/z and retention time of interest, and want to annotate an unknown compound by predicting its molecular formula, structure, and name using deep learning scoring rather than traditional spectral library matching alone. Use this when reference standards are unavailable or when nontargeted discovery is the goal.

## When NOT to use

- Input is already a reference spectrum or curated metabolite annotation from a targeted assay — use direct library matching instead.
- Raw UPLC-HRMS data in offline mode: MSThunder currently requires Linux preprocessing and email submission to developers ([redacted-email]) or upload to Zenodo/GNPS; online processing of raw data is under development.
- Data is from non-mass-spectrometry platforms (e.g., NMR, chromatography-only) or instruments not compatible with MSConvert.

## Inputs

- batch-processed mzML or vendor raw data files (ThermoFisher, Agilent) converted via MSConvert
- precursor m/z (or precursor m/z + retention time pair)
- retention time of interest
- candidate precursor molecular formula (or allow deep learning to predict from MS1)

## Outputs

- ranked list of candidate compound structures with deep learning confidence scores
- matched reference spectrum annotation (if top 10 includes library hit)
- compound name and SMILES
- MS1 and MS2 spectrum visualizations
- candidate molecular formula

## How to apply

Load batch-processed MS1/MS2 files into MSThunder on a Windows machine (16 GB RAM, 2 GB NVIDIA GPU). Specify the precursor m/z and retention time to retrieve the corresponding TIC and MS2 spectrum. Enter or confirm the candidate precursor molecular formula; MSThunder's deep learning model will generate a ranked list of structure predictions scored by fit to the experimental MS2. If a reference spectrum appears in the top 10 candidates, MSThunder displays spectrum matching results alongside the deep learning ranking. Export the top-ranked compound name, confidence score, and matched spectral library annotations. Validate by checking MS1 monoisotopic mass accuracy and MS2 fragment ion assignments against the predicted structure.

## Related tools

- **MSThunder** (Deep learning-based interface for executing nontargeted analytical workflow; loads batch-processed MS files, ranks structure predictions by deep learning score, and exports annotated candidates with spectral matching results.) — https://github.com/LQZ0123/MSThunder
- **MSConvert** (Converts raw mass spectrometry data from ThermoFisher, Agilent, and other vendors into MSThunder-compatible format.)
- **Linux preprocessing environment (Ubuntu 20.04)** (Required for offline raw data processing prior to MSThunder analysis; raw files are processed in Linux and converted files returned for Windows-based interface analysis.)

## Evaluation signals

- MS1 monoisotopic mass of top-ranked candidate matches experimental precursor m/z within instrument mass accuracy tolerance (typically <5 ppm for high-resolution HRMS).
- MS2 fragment ions in the experimental spectrum are assigned to neutral losses or characteristic fragments of the predicted structure.
- If a reference spectrum is identified in the top 10 candidates, spectrum matching score (e.g., cosine similarity or dot-product) is reported and visually confirmed in MS2-candidate output.
- Confidence score (deep learning rank score) is reported and improves monotonically as candidate rank improves.
- SMILES structure representation can be viewed in the Structure pane and is chemically valid (parseable by RDKit).

## Limitations

- Current version does not yet support offline processing of raw data; users must submit raw UPLC-HRMS files to developers or upload to Zenodo/GNPS, with processed results returned for analysis in MSThunder.
- Online processing capability for raw UPLC-HRMS data is under development and not yet available.
- Requires Windows environment with 16 GB RAM and 2 GB NVIDIA GPU; interface was developed and tested on Windows and may have compatibility issues on other platforms.
- Deep learning model training and candidate library composition are not fully documented; model performance on novel compound classes or rare pollutants is not characterized.
- If image display encounters rendering issues, workaround requires decreasing the computer's display ratio, indicating potential UI limitations on high-resolution monitors.

## Evidence

- [readme] MSThunder provide a deep learning-based nontargeted analytical framework for the accurate and rapid identification of unknown organic pollutants in water.: "MSThunder provide a deep learning-based nontargeted analytical framework for the accurate and rapid identification of unknown organic pollutants in water"
- [readme] A case file named 'Pesticides' can be run in the Windows environment equipped with 16 GB of RAM and a 2 GB NVIDIA GPU.: "A case file named "Pesticides" can be run in the Windows environment equipped with 16 GB of RAM and a 2 GB NVIDIA GPU"
- [readme] Due to environment configuration issues, the current version does not yet support offline processing of raw data.: "Due to environment configuration issues, the current version does not yet support offline processing of raw data"
- [readme] The current version is compatible with ThermoFisher, Agilent, and other vendors whose raw data can be converted via MSConvert.: "The current version is compatible with ThermoFisher, Agilent, and other vendors whose raw data can be converted via MSConvert"
- [readme] Double-click the precursor formula to execute the structure prediction function for that molecular formula; the candidate score information will be displayed in Ranking.: "Double-click the precursor formula to execute the structure prediction function for that molecular formula; the candidate score information will be displayed in Ranking"
- [readme] If a reference spectrum is found among the top 10 candidates, the spectrum matching result will be shown in MS2-candidate.: "If a reference spectrum is found among the top 10 candidates, the spectrum matching result will be shown in MS2-candidate"
- [readme] We are developing the relevant functionality and will make it available online as soon as possible.: "We are developing the relevant functionality and will make it available online as soon as possible"
