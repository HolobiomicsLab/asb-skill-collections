---
name: nontargeted-analysis-workflow-execution
description: Use when you have UPLC-HRMS data from ThermoFisher, Agilent, or other vendor instruments (converted via MSConvert if needed), organized as batch-processed files ready for MSThunder input, and you need to identify unknown organic pollutants with deep learning-assisted structure prediction and.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3172
  tools:
  - MSThunder
  - Windows
  - MSConvert
  - GNPS
  - Ubuntu 20.04 (Linux environment)
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

# nontargeted-analysis-workflow-execution

## Summary

Execute a deep learning-based nontargeted analytical workflow in MSThunder to identify unknown organic pollutants in UPLC-HRMS data by matching precursor ions, retention times, and MS2 spectra against learned candidate structures and spectral libraries. Use this skill when you have batch-processed mass spectrometry data and need to rapidly assign compound identities with confidence scores to unknowns in water or similar matrices.

## When to use

You have UPLC-HRMS data from ThermoFisher, Agilent, or other vendor instruments (converted via MSConvert if needed), organized as batch-processed files ready for MSThunder input, and you need to identify unknown organic pollutants with deep learning-assisted structure prediction and spectral matching—especially when high-throughput nontargeted screening for water contaminants is the analytical goal.

## When NOT to use

- Your mass spectrometry data are in a non-standard vendor format and cannot be converted via MSConvert or processed in a Linux environment before MSThunder analysis.
- You require offline processing of raw UPLC-HRMS data; the current MSThunder version does not support offline raw data processing and requires files to be pre-processed in a Linux system.
- Your analysis goal is targeted screening (e.g., quantification of known compounds at specific m/z with scheduled MRM); MSThunder is designed for nontargeted discovery of unknown contaminants, not targeted quantification.

## Inputs

- batch-processed UPLC-HRMS data files (ThermoFisher, Agilent, or vendor format; pre-converted to mzML or equivalent via MSConvert if required)
- precursor m/z and retention time (RT) values for target unknowns
- ion mode specification (Positive or Negative)

## Outputs

- compound identifications with IUPAC or common names
- candidate structure predictions (SMILES notation)
- confidence/ranking scores for top-10 candidate structures
- matched spectral library annotations (MS2 similarity metrics)
- molecular formulas and precursor m/z assignments

## How to apply

First, ensure your Windows environment has 16 GB RAM and a 2 GB NVIDIA GPU, then decompress msthunder.rar and msthunderfile.rar (available at doi.org/10.5281/zenodo.12602805) with msthunderfile extracted into the msthunder folder. Place your batch-processed mass spectrometry files in the MSThunder directory and launch the interface. Use the Input button to load your file and select ion mode (Positive or Negative). For each unknown precursor/retention time pair, use the Precursor/RT button to retrieve the TIC and MS2 spectrum. In the Candidate section, double-click the retention time to load the corresponding MS1 spectrum, then double-click the precursor formula to invoke deep learning-based structure prediction; inspect the Ranking list (top-10 candidates) and cross-reference any matches in the MS2-candidate section against spectral libraries. Export the final compound names, confidence scores, and matched library annotations from the output interface. The workflow's success depends on accurate precursor formula assignment and on whether a true reference spectrum appears in the top-10 ranking.

## Related tools

- **MSThunder** (Primary deep learning-based interface for nontargeted identification of unknown organic pollutants via precursor/MS2 matching and structure prediction) — https://github.com/LQZ0123/MSThunder
- **MSConvert** (Converts vendor-specific raw mass spectrometry data (ThermoFisher, Agilent, etc.) to mzML or equivalent formats compatible with MSThunder)
- **GNPS** (Online spectral library database for reference compound matching and validation of MSThunder candidate rankings)
- **Ubuntu 20.04 (Linux environment)** (Pre-processing environment in which raw UPLC-HRMS data files are batch-processed before return to MSThunder for Windows-based analysis)

## Evaluation signals

- Reference spectra (when available) appear in the top-10 candidate ranking output, validating the deep learning model's predictive power for known unknowns.
- Exported compound identifications include non-null confidence scores, SMILES structures, and molecular formulas for all analyzed precursors.
- MS2-candidate section successfully displays spectral similarity metrics (cosine or similar) between query and library spectra, confirming library matching was performed.
- Structure diagrams render correctly in the Structure section for all ranked candidates, indicating successful SMILES-to-image conversion via RDKit.
- Output file contains matched retention times, precursor m/z, and candidate ranking order consistent with input precursor/RT specifications and MS1 spectra retrieved.

## Limitations

- Current version does not support offline processing of raw data; raw files must be pre-processed in a Linux system and returned as batch-processed files before MSThunder analysis.
- Online processing capability for UPLC-HRMS raw data is still under development; for non-Pesticides case files, users must either email raw files to the developers ([redacted-email]) or upload to Zenodo/GNPS for manual batch processing.
- Hardware requirements (16 GB RAM, 2 GB NVIDIA GPU) limit deployment to equipped Windows systems; no CPU-only or lower-memory configurations are documented.
- Requires MSConvert pre-conversion for non-ThermoFisher/Agilent instruments; compatibility with other vendor formats depends on MSConvert availability.
- Deep learning candidate ranking depends on training data; identification confidence may be reduced for compounds structurally distant from the training set.

## Evidence

- [readme] MSThunder provide a deep learning-based nontargeted analytical framework for the accurate and rapid identification of unknown organic pollutants in water.: "MSThunder provide a deep learning-based nontargeted analytical framework for the accurate and rapid identification of unknown organic pollutants in water"
- [readme] A case file named "Pesticides" can be run in the Windows environment equipped with 16 GB of RAM and a 2 GB NVIDIA GPU.: "A case file named "Pesticides" can be run in the Windows environment equipped with 16 GB of RAM and a 2 GB NVIDIA GPU"
- [readme] The interface mode of MSThunder is available by decompressing in the file in RAR format (msthunder.rar and msthunderfile.rar) (doi.org/10.5281/zenodo.12602805).: "The interface mode of MSThunder is available by decompressing in the file in RAR format (msthunder.rar and msthunderfile.rar) (doi.org/10.5281/zenodo.12602805)"
- [readme] Due to environment configuration issues, the current version does not yet support offline processing of raw data.: "Due to environment configuration issues, the current version does not yet support offline processing of raw data"
- [readme] The current version is compatible with ThermoFisher, Agilent, and other vendors whose raw data can be converted via MSConvert.: "The current version is compatible with ThermoFisher, Agilent, and other vendors whose raw data can be converted via MSConvert"
- [readme] Double-click on any row of data to view the precursor, retention time, ISMILES, and candidate precursor formula in the Candidate section.: "Double-click on any row of data to view the precursor, retention time, ISMILES, and candidate precursor formula in the Candidate section"
- [readme] Double-click the precursor formula to execute the structure prediction function for that molecular formula; the candidate score information will be displayed in Ranking.: "Double-click the precursor formula to execute the structure prediction function for that molecular formula; the candidate score information will be displayed in Ranking"
- [readme] If a reference spectrum is found among the top 10 candidates, the spectrum matching result will be shown in MS2-candidate.: "If a reference spectrum is found among the top 10 candidates, the spectrum matching result will be shown in MS2-candidate"
