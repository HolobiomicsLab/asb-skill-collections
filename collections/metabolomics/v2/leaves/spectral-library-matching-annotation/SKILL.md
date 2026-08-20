---
name: spectral-library-matching-annotation
description: Use when you have MS2 spectral data (precursor m/z, retention time, and
  fragment ion patterns) from UPLC-HRMS analysis of environmental or biological samples
  and need to assign compound identities by comparing against known reference spectra.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_0089
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - MSThunder
  - Windows
  - GNPS
  - MSConvert
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1016/j.enceco.2025.07.022
  title: MSThunder
evidence_spans:
- MSThunder provide a deep learning-based nontargeted analytical framework for the
  accurate and rapid identification of unknown organic pollutants in water
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-library-matching-annotation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Match experimental MS2 spectra against reference spectral libraries and retrieve compound annotations with confidence scores using deep learning-based candidate ranking. This skill is essential for identifying unknown organic pollutants in nontargeted mass spectrometry workflows where reference spectra are available in GNPS or similar databases.

## When to use

Apply this skill when you have MS2 spectral data (precursor m/z, retention time, and fragment ion patterns) from UPLC-HRMS analysis of environmental or biological samples and need to assign compound identities by comparing against known reference spectra. Use it after peak detection and MS2 acquisition but before reporting final compound identifications, particularly when analyzing complex mixtures like pesticides, pollutants, or metabolites where multiple candidate structures may match a single precursor mass.

## When NOT to use

- If raw UPLC-HRMS data has not yet been converted to mzML or batch-processed format — MSThunder requires pre-processed ion chromatograms and does not currently support offline raw data ingestion.
- If no reference spectral library or candidate formula is available — the matching step requires either a known molecular formula to predict structures or pre-existing reference spectra in GNPS/online databases.
- If the sample was acquired on a vendor instrument (ThermoFisher, Agilent) without prior conversion via MSConvert — MSThunder is compatible only with converted formats.

## Inputs

- Batch-processed MS2 spectral data files (precursor m/z, retention time, fragment ion m/z and intensities)
- Candidate molecular formula (either system-predicted or user-specified)
- Reference spectral library (GNPS or equivalent database)
- MS1 spectrum at the target retention time

## Outputs

- Ranked list of candidate structures (top 10) with confidence scores
- MS2-candidate spectrum matching result (if reference spectrum found in top 10)
- Compound name, SMILES notation, and molecular structure diagram
- Spectral library annotation metadata

## How to apply

Load batch-processed MS2 data into the MSThunder interface specifying precursor m/z and retention time. For each precursor, the system retrieves candidate molecular formulas and executes structure prediction against the deep learning model trained on spectral library data. The workflow ranks candidate structures by a learned similarity score and returns the top 10 matches; if a reference spectrum is found among these candidates, the spectrum matching result (cosine similarity or equivalent metric) is displayed. Verify results by inspecting whether matched reference spectra show reasonable MS2 fragment patterns (neutral losses, base peaks) consistent with the proposed chemical structure, and cross-check high-confidence matches (top rank with reference spectrum hit) against chemical plausibility for the sample matrix.

## Related tools

- **MSThunder** (Deep learning-based interface for spectral matching, structure prediction, and candidate ranking; executes MS2-to-reference spectrum matching and returns top-ranked compounds with confidence scores.) — https://github.com/LQZ0123/MSThunder
- **GNPS** (Online spectral library and reference database used to populate candidate structures and reference spectra for matching.)
- **MSConvert** (Converts vendor raw data (ThermoFisher, Agilent) to standardized format compatible with MSThunder preprocessing pipeline.)

## Evaluation signals

- Top-ranked candidate structure appears in the top 10 matches and displays a reference spectrum match in the MS2-candidate panel.
- MS2 fragment pattern of the matched reference spectrum shows logical neutral losses and base peak assignments consistent with the proposed molecular structure (e.g., loss of water or CO₂ for polar compounds).
- Candidate ranking score is reproducible across multiple runs on the same precursor m/z and retention time; scores do not depend on UI rendering artifacts.
- Matched compound names are chemical plausible for the sample matrix (e.g., pesticide names for environmental water samples) and match entries in public chemical databases (PubChem).
- If a user replaces the system-predicted molecular formula with a corrected formula and re-runs prediction (double-click → enter formula → double-click Ranking), the new set of candidates re-ranks correctly without crashing.

## Limitations

- Current version does not support offline processing of raw data; users must send raw UPLC-HRMS files to the development team ([redacted-email]) or upload to Zenodo/GNPS for centralized preprocessing and subsequent MSThunder analysis.
- Online processing capability for raw UPLC-HRMS data is under development and not yet available; currently requires manual file transfer and Linux-based conversion step.
- Matching accuracy depends on the completeness and quality of the reference spectral library; compounds absent from GNPS or other indexed databases cannot be identified even if precursor mass is correct.
- System requires Windows environment with 16 GB RAM and 2 GB NVIDIA GPU; performance on lower-spec hardware or alternative operating systems has not been validated.
- If candidate structure images fail to render in the GUI, users may need to lower the display resolution setting to view MS2-candidate spectra and structure diagrams.

## Evidence

- [readme] MSThunder provide a deep learning-based nontargeted analytical framework for the accurate and rapid identification of unknown organic pollutants in water: "MSThunder provide a deep learning-based nontargeted analytical framework for the accurate and rapid identification of unknown organic pollutants in water."
- [readme] If a reference spectrum is found among the top 10 candidates, the spectrum matching result will be shown in MS2-candidate: "If a reference spectrum is found among the top 10 candidates, the spectrum matching result will be shown in MS2-candidate."
- [readme] Double-click the precursor formula to execute the structure prediction function for that molecular formula; the candidate score information will be displayed in Ranking: "Double-click the precursor formula to execute the structure prediction function for that molecular formula; the candidate score information will be displayed in Ranking."
- [readme] The current version is compatible with ThermoFisher, Agilent, and other vendors whose raw data can be converted via MSConvert: "The current version is compatible with ThermoFisher, Agilent, and other vendors whose raw data can be converted via MSConvert."
- [readme] Due to environment configuration issues, the current version does not yet support offline processing of raw data: "Due to environment configuration issues, the current version does not yet support offline processing of raw data."
