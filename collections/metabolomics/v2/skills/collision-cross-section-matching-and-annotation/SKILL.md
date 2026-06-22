---
name: collision-cross-section-matching-and-annotation
description: Use when when you have LC-IM-MS/MS data with measured collision cross section (CCS) values and m/z assignments, and you need to disambiguate sterol isomers (particularly N-Me derived unsaturated sterols) by matching against a curated database of predicted CCS values and MS/MS fragmentation patterns.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - Jupyter Notebook
  - scikit-learn
  techniques:
  - LC-MS
  - ion-mobility-MS
  - tandem-MS
derived_from:
- doi: 10.1002/anie.202507483
  title: NA
evidence_spans:
- collection of Python scripts
- All functions are implemented in jupyter notebook
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_na_cq
    doi: 10.1002/anie.202507483
    title: NA
  dedup_kept_from: coll_na_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1002/anie.202507483
  all_source_dois:
  - 10.1002/anie.202507483
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# collision-cross-section-matching-and-annotation

## Summary

Match experimental LC-IM-MS/MS 4D features (retention time, m/z, drift time, intensity) against a quantum chemistry calculation-assisted CCS prediction database to identify and annotate sterol isomers with structural detail (double-bond position, stereochemistry) and confidence scores.

## When to use

When you have LC-IM-MS/MS data with measured collision cross section (CCS) values and m/z assignments, and you need to disambiguate sterol isomers (particularly N-Me derived unsaturated sterols) by matching against a curated database of predicted CCS values and MS/MS fragmentation patterns. Use this skill after 4D feature extraction but before final quantitative reporting.

## When NOT to use

- Input data lacks drift time information or ion mobility separation (CCS matching requires IM-MS data, not LC-MS/MS alone)
- Sterol lipids have already been matched and annotated in a previous workflow step
- CCS prediction database is unavailable or not calibrated for the experimental instrument and sterol class

## Inputs

- 4D feature table with retention time (RT), m/z, drift time (DT), and intensity
- Quantum chemistry calculation-assisted CCS prediction database (N-Me derived unsaturated sterols)
- Experimental MS/MS fragmentation spectra

## Outputs

- Annotated sterol identifications with structure (double-bond position, stereochemistry)
- Matched feature records with CCS and spectral match quality scores
- Tissue-specific quantitative sterol data
- Confidence scores per identification

## How to apply

Load the detected m/z and drift time values from the 4D feature extraction step. Look up each detected m/z in a quantum chemistry-assisted CCS prediction database of N-Me derived unsaturated sterol lipids to retrieve candidate structures and predicted CCS values. Filter candidate identifications by applying a CCS tolerance window (exact threshold from the paper's workflow); retain only matches within this window. Cross-validate the remaining candidates by comparing observed MS/MS fragmentation patterns against the database records using spectral similarity scoring. Assign confidence scores to each matched feature based on both CCS match quality and MS/MS spectral match quality. Annotate the final matches with sterol structure information (double-bond position and stereochemistry) and tissue-specific quantitative data.

## Related tools

- **Python** (Primary programming language for implementing 4D feature matching, CCS tolerance filtering, and spectral similarity scoring logic)
- **Jupyter Notebook** (Interactive notebook environment for executing matching workflow steps, visualizing candidate matches, and generating annotated output tables) — github.com/Chen-micslab/QCCAssisted4DSterol
- **scikit-learn** (Provides SVR model and LASSO feature selection used in the underlying CCS prediction training; matching references predictions from this model)

## Evaluation signals

- All matched features report both CCS match quality and MS/MS spectral match quality scores; no matches lack either component
- Matched sterol annotations include explicit double-bond position and stereochemistry; check that structure fields are not empty or generic
- CCS tolerance filtering is applied consistently: verify that all reported matches fall within the stated CCS tolerance window of the database
- Tissue-specific quantitative data is populated for each matched sterol; no quantitative records are NULL or missing for validated matches
- Confidence scores correlate with CCS and spectral match quality: matches with poor CCS alignment or low spectral similarity should receive lower scores

## Limitations

- Workflow is optimized for N-Me derived unsaturated sterol lipids; applicability to other sterol modifications or lipid classes is untested
- Matching accuracy depends critically on the quality and completeness of the CCS prediction database; under-represented structural variants may not match or may be assigned to incorrect isomers
- CCS tolerance threshold must be tuned to the specific LC-IM-MS/MS instrument and calibration; the paper does not explicitly state the tolerance value used
- MS/MS fragmentation pattern matching requires clean, well-resolved spectra; noisy or contaminated spectra may fail to match or produce false identifications

## Evidence

- [other] Match detected m/z values against a quantum chemistry calculation-assisted CCS prediction database of N-Me derived unsaturated sterol lipids: "Match detected m/z values against a quantum chemistry calculation-assisted CCS prediction database of N-Me derived unsaturated sterol lipids."
- [other] Filter candidate identifications by CCS tolerance and MS/MS fragmentation pattern matching: "Filter candidate identifications by CCS tolerance and MS/MS fragmentation pattern matching."
- [other] Annotate matched features with sterol structure (including double-bond position and stereochemistry) and assign confidence scores based on CCS and spectral match quality: "Annotate matched features with sterol structure (including double-bond position and stereochemistry) and assign confidence scores based on CCS and spectral match quality."
- [readme] LC-IM-MS/MS based 4D sterolomics data processing and identification: "LC-IM-MS/MS based 4D streolomics data processing and identification"
- [other] Load raw LC-IM-MS/MS data and apply 4D feature extraction (retention time, m/z, drift time, intensity) using Python: "Load raw LC-IM-MS/MS data and apply 4D feature extraction (retention time, m/z, drift time, intensity) using Python."
