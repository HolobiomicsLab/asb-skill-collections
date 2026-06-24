---
name: 4d-lcimmsms-feature-extraction
description: Use when you have raw LC-IM-MS/MS data files from sterol lipid analysis
  and need to identify unsaturated sterol isomers by matching experimental collision
  cross section values against a quantum chemistry calculation-assisted CCS prediction
  database.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - Jupyter Notebook
  - RDKit
  - scikit-learn
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

# 4D LC-IM-MS/MS Feature Extraction

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Extract four-dimensional features (retention time, m/z, drift time, intensity) from raw LC-IM-MS/MS data to enable collision cross section matching and sterol isomer identification. This skill is essential for converting raw instrument output into annotated molecular features with stereochemical and structural metadata.

## When to use

Apply this skill when you have raw LC-IM-MS/MS data files from sterol lipid analysis and need to identify unsaturated sterol isomers by matching experimental collision cross section values against a quantum chemistry calculation-assisted CCS prediction database. The skill is specifically designed for N-Me derived unsaturated sterol lipids with known double-bond positions.

## When NOT to use

- Input is already a processed feature table or identified metabolite table (skip directly to quantification or statistical analysis)
- Data come from saturated sterols or non-N-Me lipid classes (the RDKit fragmentation model is validated only for sterols with C=C bonds)
- Raw data lack drift time dimension (IM-MS/MS orthogonal separation is required for CCS calculation and isomer resolution)

## Inputs

- Raw LC-IM-MS/MS data files (instrument binary or vendor format)
- Quantum chemistry calculation-assisted CCS prediction database for N-Me derived unsaturated sterols
- MS/MS fragmentation pattern reference library (calculated from RDKit-based fragmentation rules)
- Sample metadata (tissue type, biological replicate identifier)

## Outputs

- Annotated 4D feature table with retention time, m/z, drift time, and intensity
- Sterol identification records with double-bond position and stereochemistry assignments
- Confidence scores per feature (CCS tolerance match quality, MS/MS spectral similarity)
- Tissue-specific quantitative sterol abundance data
- Unidentified feature table (features not matching CCS or spectral criteria)

## How to apply

Load raw LC-IM-MS/MS data and apply 4D feature extraction using Python to extract retention time, m/z, drift time, and intensity dimensions. Match detected m/z values against a quantum chemistry calculation-assisted CCS prediction database of N-Me derived unsaturated sterol lipids. Filter candidate identifications by CCS tolerance and MS/MS fragmentation pattern matching against calculated N-Me fragmentation patterns. Annotate matched features with sterol structure (including double-bond position and stereochemistry) and assign confidence scores based on CCS match quality and spectral similarity. Generate output records linking each identified sterol feature to tissue-specific quantitative intensity data.

## Related tools

- **Python** (Language for implementing 4D feature extraction, CCS matching, and annotation logic)
- **Jupyter Notebook** (Interactive environment for executing feature extraction workflows and data inspection) — https://github.com/Chen-micslab/QCCAssisted4DSterol
- **RDKit** (Cheminformatics toolkit for recognizing double-bond positions and generating N-Me MS/MS fragmentation patterns)
- **scikit-learn** (Machine learning library used for CCS prediction model (SVR with LASSO feature selection) that supports candidate filtering)

## Evaluation signals

- All raw LC-IM-MS/MS data points are assigned to a 4D feature (retention time, m/z, drift time, intensity) or explicitly flagged as noise/artifact
- Extracted CCS values from drift time fall within expected range (typically 100–500 Ų for sterol lipids) and show monotonic increase with m/z within isomer series
- MS/MS fragmentation patterns of matched features contain expected N-Me cleavage ions (diagnostic fragment m/z values) with intensity ratios consistent with structure
- Confidence scores are inversely correlated with CCS prediction database match error and MS/MS spectral cosine similarity; features with score > 0.7 are manually spot-checked against reference standards when available
- Annotated sterols show tissue-specific distribution patterns (e.g., cholesterol predominance in brain tissue, phytosterol enrichment in plant-derived samples) consistent with prior literature

## Limitations

- The RDKit fragmentation model is validated only for sterol lipids with C=C bonds; saturated sterols or other lipid classes are not reliably fragmented
- CCS prediction accuracy depends on the size and chemical diversity of the training dataset; out-of-domain lipid structures may have poor CCS predictions
- Isomers with identical m/z and very similar CCS values (e.g., positional double-bond isomers differing by <2% CCS) may not be fully resolved and require manual spectral inspection
- Feature extraction requires tuning of retention time, m/z, drift time, and intensity thresholds; suboptimal threshold selection leads to missed low-abundance features or false positives
- Tissue-specific quantification assumes equal ionization efficiency across sterol isomers; differential ionization of regioisomers may introduce systematic bias

## Evidence

- [other] Load raw LC-IM-MS/MS data and apply 4D feature extraction (retention time, m/z, drift time, intensity) using Python.: "Load raw LC-IM-MS/MS data and apply 4D feature extraction (retention time, m/z, drift time, intensity) using Python."
- [other] Match detected m/z values against a quantum chemistry calculation-assisted CCS prediction database of N-Me derived unsaturated sterol lipids.: "Match detected m/z values against a quantum chemistry calculation-assisted CCS prediction database of N-Me derived unsaturated sterol lipids."
- [other] Filter candidate identifications by CCS tolerance and MS/MS fragmentation pattern matching.: "Filter candidate identifications by CCS tolerance and MS/MS fragmentation pattern matching."
- [other] Annotate matched features with sterol structure (including double-bond position and stereochemistry) and assign confidence scores based on CCS and spectral match quality.: "Annotate matched features with sterol structure (including double-bond position and stereochemistry) and assign confidence scores based on CCS and spectral match quality."
- [readme] The script recognises double bond positions and generates MS/MS based on N-Me fragmentation patterns.: "The script  recognises double bond positions and generates MS/MS based on N-Me fragmentation patterns."
- [readme] The CCS prediction process in the paper is implemented using the scikit-learn API. It employs LASSO for feature selection and uses cross-validation to select the best hyperparameters for the SVR model.: "The CCS prediction process in the paper is implemented using the scikit-learn API. It employs LASSO for feature selection and uses cross-validation to select the best hyperparameters for the SVR"
- [readme] All functions are implemented in jupyter notebook: "All functions are implemented in jupyter notebook"
