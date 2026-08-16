---
name: tissue-specific-metabolite-quantification
description: Use when you have LC-IM-MS/MS raw data from multiple tissue samples and
  need to identify and quantify unsaturated sterol lipids at the isomer level (distinguishing
  double-bond position and stereochemistry).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - Jupyter Notebook
  - RDKit
  - scikit-learn (SVR, LASSO)
  techniques:
  - LC-MS
  - ion-mobility-MS
  license_tier: restricted
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# tissue-specific-metabolite-quantification

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Quantify sterol isomers at the tissue level by matching LC-IM-MS/MS 4D features (retention time, m/z, drift time, intensity) against a quantum chemistry-assisted CCS prediction database, filtering by collision cross section tolerance and MS/MS fragmentation patterns, then assigning confidence scores and tissue-specific abundance values. This skill enables resolution of sterol structural isomers (double-bond position and stereochemistry) across different tissue samples.

## When to use

You have LC-IM-MS/MS raw data from multiple tissue samples and need to identify and quantify unsaturated sterol lipids at the isomer level (distinguishing double-bond position and stereochemistry). This skill is triggered when: (1) you have 4D feature data (retention time, m/z, drift time, intensity); (2) a reference CCS prediction database for the lipid class is available; (3) you need tissue-level abundance comparisons, not just bulk identification; and (4) structural isomers cannot be resolved by MS/MS fragmentation alone.

## When NOT to use

- Input is already a fully annotated feature matrix or quantified metabolite table — this skill is a feature-to-metabolite resolution step, not a post-identification aggregation step.
- You lack a reference CCS prediction database or MS/MS fragmentation rules for your lipid class — CCS matching is essential for isomer discrimination.
- Your mass spectrometry data does not include ion mobility (drift time) dimension — the 4D feature space is required for CCS-based matching.

## Inputs

- LC-IM-MS/MS raw data files (one or more tissue samples)
- 4D feature table (retention time, m/z, drift time, intensity)
- Quantum chemistry calculation-assisted CCS prediction database for N-Me derived unsaturated sterol lipids
- Theoretical MS/MS fragmentation pattern library for sterol isomers
- Tissue sample identifiers/metadata

## Outputs

- Annotated feature table with matched sterol identity (structure, double-bond position, stereochemistry)
- Confidence scores per identification (CCS and spectral match quality metrics)
- Tissue-specific quantitative sterol profiles (abundance by tissue and sterol isomer)
- Identified sterol records with tissue annotation

## How to apply

Load raw LC-IM-MS/MS data and extract 4D features using Python. For each detected feature, calculate or retrieve the theoretical CCS value from a quantum chemistry calculation-assisted CCS prediction database (built on N-Me derived unsaturated sterol lipids). Match observed m/z against the database and filter candidate identifications by CCS tolerance (typically within instrument calibration bounds). Cross-validate candidate structures by comparing experimental MS/MS fragmentation patterns against theoretical patterns derived from N-Me fragmentation rules. Assign a confidence score based on CCS match quality and spectral similarity. Annotate each matched feature with sterol structure (including double-bond position and stereochemistry) and tissue ID. Extract and aggregate intensity values by tissue and sterol identity to produce tissue-specific quantitative profiles.

## Related tools

- **Python** (Primary scripting language for loading raw LC-IM-MS/MS data, extracting 4D features, performing CCS matching, and filtering by MS/MS fragmentation patterns)
- **Jupyter Notebook** (Interactive notebook environment for implementing 4D sterolomics data processing and identification workflows)
- **RDKit** (Molecular toolkit for recognizing double bond positions in sterol structures and generating or validating MS/MS fragmentation patterns based on N-Me chemistry)
- **scikit-learn (SVR, LASSO)** (Machine learning library used to train CCS prediction models (LASSO for feature selection, SVR for regression with cross-validation hyperparameter tuning))

## Evaluation signals

- CCS match residuals between observed and predicted values fall within instrument calibration tolerance for all matched features.
- MS/MS fragmentation patterns of matched identifications show cosine similarity or spectral match score above a defined threshold (e.g., derived from cross-validation on training data).
- Confidence scores are correctly computed from CCS and spectral quality metrics and are consistent across replicate samples.
- Tissue-specific abundance profiles show expected biological patterns (e.g., tissue-dependent sterol composition consistent with literature or prior knowledge).
- Double-bond position and stereochemistry assignments are reproducible across replicates and consistent with retention time ordering (RTs should reflect structural isomer differences).

## Limitations

- The workflow is currently tested and validated only for unsaturated sterol lipids; applicability to other lipid classes with C=C bonds requires validation.
- CCS prediction accuracy depends on the quality and completeness of the reference database; lipids not well-represented in the training set may have higher prediction error.
- MS/MS fragmentation patterns are derived from N-Me derivatization chemistry; non-derivatized or differently derivatized samples may produce different fragmentation and will not match the database.
- Ion mobility resolution and CCS calibration quality directly impact isomer discrimination; instruments with poor drift time resolution may fail to resolve structural isomers that differ only slightly in CCS.
- The method assumes that CCS and MS/MS fragmentation are sufficient to disambiguate isomers; co-eluting isomers with identical CCS and MS/MS patterns cannot be resolved.

## Evidence

- [other] Load raw LC-IM-MS/MS data and apply 4D feature extraction (retention time, m/z, drift time, intensity) using Python. 2. Match detected m/z values against a quantum chemistry calculation-assisted CCS prediction database of N-Me derived unsaturated sterol lipids.: "Load raw LC-IM-MS/MS data and apply 4D feature extraction (retention time, m/z, drift time, intensity) using Python. 2. Match detected m/z values against a quantum chemistry calculation-assisted CCS"
- [other] Filter candidate identifications by CCS tolerance and MS/MS fragmentation pattern matching. 4. Annotate matched features with sterol structure (including double-bond position and stereochemistry) and assign confidence scores based on CCS and spectral match quality. 5. Generate identified sterol records with tissue-specific quantitative data.: "Filter candidate identifications by CCS tolerance and MS/MS fragmentation pattern matching. 4. Annotate matched features with sterol structure (including double-bond position and stereochemistry)"
- [intro] LC-IM-MS/MS based 4D sterolomics data processing and identification: "LC-IM-MS/MS based 4D sterolomics data processing and identification"
- [readme] All functions are implemented in jupyter notebook: "All functions are implemented in jupyter notebook"
- [readme] The CCS prediction process in the paper is implemented using the scikit-learn API. It employs LASSO for feature selection and uses cross-validation to select the best hyperparameters for the SVR model.: "The CCS prediction process in the paper is implemented using the scikit-learn API. It employs LASSO for feature selection and uses cross-validation"
- [readme] The script is written on the basis of RDkit's built-in functions. The script recognises double bond positions and generates MS/MS based on N-Me fragmentation patterns.: "The script is written on the basis of RDkit's built-in functions. The script recognises double bond positions and generates MS/MS based on N-Me fragmentation patterns."
