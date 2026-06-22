---
name: sterol-lipid-isomer-characterization
description: Use when you have LC-IM-MS/MS experimental data (raw mzML or vendor format) containing signals from N-Me derived unsaturated sterol lipids and need to assign double-bond positions and stereochemistry to individual sterol isomers rather than sum compositions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3172
  tools:
  - Python
  - Jupyter Notebook
  - RDKit
  - scikit-learn
  - Graph Neural Network (GNN) retention time predictor
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
---

# sterol-lipid-isomer-characterization

## Summary

LC-IM-MS/MS based 4D sterolomics workflow that identifies sterol isomers by matching experimental retention time, m/z, and drift time against a quantum chemistry calculation-assisted collision cross section (CCS) prediction database, enabling tissue-specific sterol distribution analysis at the level of double-bond position and stereochemistry.

## When to use

Apply this skill when you have LC-IM-MS/MS experimental data (raw mzML or vendor format) containing signals from N-Me derived unsaturated sterol lipids and need to assign double-bond positions and stereochemistry to individual sterol isomers rather than sum compositions. The workflow is triggered when you have both ion mobility and tandem MS data and access to a trained CCS prediction model for your sterol class.

## When NOT to use

- Input data lack ion mobility dimension (standard LC-MS/MS without IM cannot resolve isomers by CCS difference)
- Sterol lipids are not N-Me derivatized or fragmentation pattern does not match trained database (workflow is specific to N-Me derivatives)
- No access to a trained CCS prediction model or quantum chemistry reference database for your sterol class

## Inputs

- Raw LC-IM-MS/MS data (vendor format or mzML)
- Quantum chemistry calculation-assisted CCS prediction database for N-Me derived unsaturated sterols
- Trained CCS prediction model (SVR with LASSO feature selection)
- Tissue sample metadata and sample folder structure

## Outputs

- Annotated sterol feature table with retention time, m/z, drift time, intensity
- Sterol isomer identifications with double-bond position and stereochemistry assignments
- Confidence scores per identification (CCS match and MS/MS spectral match quality)
- Tissue-specific quantitative sterol abundance records

## How to apply

Load raw LC-IM-MS/MS data and extract four-dimensional features: retention time, m/z, drift time, and intensity. Match detected m/z values against a CCS prediction database of N-Me derived unsaturated sterol lipids built from quantum chemistry calculations and training data (using scikit-learn LASSO for feature selection and SVR with cross-validation for the model). Filter candidate identifications using CCS tolerance thresholds and MS/MS fragmentation pattern matching based on RDKit-derived N-Me fragmentation signatures. Annotate matched features with sterol structure (including double-bond position and stereochemistry) and assign confidence scores based on CCS match quality and spectral similarity. Generate final sterol records paired with tissue-specific quantitative data.

## Related tools

- **Python** (Core implementation language for 4D feature extraction, CCS database matching, and spectral annotation logic) — github.com/Chen-micslab/QCCAssisted4DSterol
- **Jupyter Notebook** (Environment for implementing all LC-IM-MS/MS data processing and sterol identification functions) — github.com/Chen-micslab/QCCAssisted4DSterol
- **RDKit** (MS/MS calculation and fragmentation pattern generation for N-Me derived unsaturated sterols based on double-bond position recognition)
- **scikit-learn** (CCS prediction model training using LASSO feature selection and SVR with cross-validation hyperparameter tuning)
- **Graph Neural Network (GNN) retention time predictor** (Auxiliary RT prediction to support feature matching and annotation) — https://github.com/seokhokang/retention_time_gnn/

## Examples

```
# Load 4D features, query CCS database, and annotate sterols; see Jupyter notebooks in github.com/Chen-micslab/QCCAssisted4DSterol/Search/tissue/ for complete workflow. Example Python snippet: features = extract_4d_features(raw_lcimms_data); candidates = query_ccs_db(features['m/z'], trained_ccs_model, tolerance=2.0); identifications = filter_by_fragmentation(candidates, features['ms_ms'], rdk_patterns); annotated = assign_sterol_structure(identifications, confidence_threshold=0.8)
```

## Evaluation signals

- CCS prediction error is within tolerance thresholds specified in the database (quantify: compare predicted CCS to experimental CCS; expect ≤ 2–3% deviation for validated assignments)
- MS/MS fragmentation pattern matches known N-Me sterol fragmentation signature (RDKit-derived theoretical spectra; compare cosine similarity or custom match score against threshold)
- Sterol assignments are consistent across replicate tissue samples (same isomer identifications and relative quantitation in biological replicates)
- Double-bond position and stereochemistry assignments resolve distinct isomers with different retention times and drift times (verify separation in 4D feature space)
- Quantitative sterol values show tissue-specific distributions consistent with biological literature (e.g., cholesterol dominant in brain, ergosterol in fungi if applicable)

## Limitations

- Workflow is currently validated only for N-Me derived unsaturated sterol lipids; applicability to other lipid modifications or saturated sterols is unconfirmed
- Accuracy depends on the completeness and accuracy of the quantum chemistry calculation-assisted CCS reference database; rare or novel isomers not in training data cannot be reliably identified
- Ion mobility and tandem MS data quality must be high (sufficient resolution and signal intensity); low-abundance isomers may fall below detection thresholds
- Confidence scores are based on CCS and MS/MS match quality but do not provide statistical significance testing or false discovery rate control across multiple identifications

## Evidence

- [other] Load raw LC-IM-MS/MS data and apply 4D feature extraction (retention time, m/z, drift time, intensity) using Python. Match detected m/z values against a quantum chemistry calculation-assisted CCS prediction database of N-Me derived unsaturated sterol lipids.: "Load raw LC-IM-MS/MS data and apply 4D feature extraction (retention time, m/z, drift time, intensity) using Python. Match detected m/z values against a quantum chemistry calculation-assisted CCS"
- [other] Filter candidate identifications by CCS tolerance and MS/MS fragmentation pattern matching. Annotate matched features with sterol structure (including double-bond position and stereochemistry) and assign confidence scores based on CCS and spectral match quality.: "Filter candidate identifications by CCS tolerance and MS/MS fragmentation pattern matching. Annotate matched features with sterol structure (including double-bond position and stereochemistry) and"
- [readme] The CCS prediction process in the paper is implemented using the scikit-learn API. It employs LASSO for feature selection and uses cross-validation to select the best hyperparameters for the SVR model.: "The CCS prediction process in the paper is implemented using the scikit-learn API. It employs LASSO for feature selection and uses cross-validation to select the best hyperparameters for the SVR"
- [readme] The script is written on the basis of RDkit's built-in functions. The script recognises double bond positions and generates MS/MS based on N-Me fragmentation patterns.: "The script is written on the basis of RDkit's built-in functions. The script recognises double bond positions and generates MS/MS based on N-Me fragmentation patterns."
- [intro] LC-IM-MS/MS based 4D streolomics data processing and identification: "LC-IM-MS/MS based 4D streolomics data processing and identification"
