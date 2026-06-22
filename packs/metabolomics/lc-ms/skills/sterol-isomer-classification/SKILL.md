---
name: sterol-isomer-classification
description: Use when you have LC-IM-MS/MS raw data from sterol-containing tissue samples and need to assign detected peaks to specific structural isomers (e.g., distinct double bond positions or saturation patterns in C27–C29 sterols).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0602
  tools:
  - Python
  - Jupyter Notebook
  - RDKit
  - scikit-learn (LASSO, SVR, cross-validation)
  - Graph Neural Network (retention_time_gnn)
  - Python, Jupyter Notebook
  techniques:
  - LC-MS
  - ion-mobility-MS
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

# sterol-isomer-classification

## Summary

Classify and identify structural isomers of N-Me derived unsaturated sterols using LC-IM-MS/MS 4D data (retention time, m/z, drift time, MS/MS fragments) combined with quantum chemistry-predicted CCS values and machine-learned retention time models. This skill enables tissue-specific sterol distribution analysis at the isomer level by matching experimental 4D signatures to predicted physicochemical properties.

## When to use

Apply this skill when you have LC-IM-MS/MS raw data from sterol-containing tissue samples and need to assign detected peaks to specific structural isomers (e.g., distinct double bond positions or saturation patterns in C27–C29 sterols). Use it when experimental CCS and retention time alone are insufficient for disambiguation and you have access to a pre-trained CCS prediction model and RT-GNN model calibrated on your lipid class.

## When NOT to use

- Input contains only MS1 (precursor m/z) data without MS/MS fragmentation patterns or drift time — this skill requires multi-dimensional discrimination.
- Target lipids are saturated sterols or lipids not containing C=C double bonds, as the MS/MS fragmentation rules and CCS prediction model are specific to unsaturated N-Me sterols.
- No pre-trained CCS prediction model or RT-GNN model is available and training data (quantum chemistry features or RT standards) is insufficient to build one.
- Isomers of interest do not differ in double bond position or saturation but only in stereochemistry (e.g., 5α vs. 5β) — the current workflow does not discriminate stereoisomers.

## Inputs

- LC-IM-MS/MS raw data files (e.g., .raw or vendor format) from tissue samples
- Predicted CCS dataset indexed by lipid identifier and structural isomer class (tabular format, e.g., CSV with columns: isomer_id, CCS_predicted, m/z, structure_SMILES)
- Pre-trained SVR-based CCS prediction model (scikit-learn joblib or pickle object)
- Pre-trained graph neural network RT prediction model (referenced from retention_time_gnn repository)
- MS/MS fragmentation pattern library for N-Me derived unsaturated sterols (RDKit-generated or reference database)
- Sample metadata (tissue type, replicate ID, acquisition parameters)

## Outputs

- Annotated 4D feature table with columns: retention_time, m/z, drift_time, CCS_experimental, CCS_predicted, isomer_id, double_bond_position(s), confidence_score, MS/MS_match_score
- Tissue-level sterol composition summary table (isomer abundance by tissue type)
- Isomer assignment validation report (cross-replicate consistency, reference standard matches)
- Visualization: 2D scatter plots (RT vs. m/z, CCS vs. m/z) colored by assigned isomer class

## How to apply

First, process LC-IM-MS/MS data to extract 4D feature tables (retention time, m/z, drift time, MS/MS fragment patterns) for each detected sterol peak. Second, apply MS/MS fragmentation pattern matching to infer double bond positions using RDKit-based N-Me fragmentation rules. Third, retrieve or compute the predicted CCS value for each candidate isomer using the QCC-assisted CCS prediction model (trained via LASSO feature selection and SVR with cross-validation on quantum chemistry features). Fourth, predict retention time using a graph neural network model pre-trained on sterol RT standards. Fifth, score candidate isomers by multi-dimensional similarity: cosine similarity on MS/MS fragments, CCS prediction error, and RT prediction error. Assign the peak to the isomer with the highest combined score, subject to a threshold (exact threshold not specified in the paper but cross-validation error on hold-out isomers is a rational choice). Validate assignments by checking consistency across tissue replicates and comparing to reference standards where available.

## Related tools

- **RDKit** (Generate 3D conformers, recognize double bond positions in SMILES, and execute MS/MS fragmentation pattern simulation for N-Me sterols)
- **scikit-learn (LASSO, SVR, cross-validation)** (Train CCS prediction model: LASSO for feature selection on quantum chemistry descriptors, SVR for regression, cross-validation for hyperparameter tuning)
- **Graph Neural Network (retention_time_gnn)** (Predict retention time for sterol isomers from molecular graph structure) — https://github.com/seokhokang/retention_time_gnn/
- **Python, Jupyter Notebook** (Implement all classification, prediction, and visualization functions) — https://github.com/Chen-micslab/QCCAssisted4DSterol

## Evaluation signals

- Cross-replicate assignment consistency: ≥ 90% of peaks assigned to the same isomer across tissue replicates of the same type, indicating reproducibility.
- CCS prediction residual (|CCS_experimental − CCS_predicted|) is within ±2% for isomers with reference experimental CCS values.
- MS/MS fragment pattern cosine similarity between observed and predicted (RDKit-generated) fragmentation is ≥ 0.7 for confidently assigned peaks.
- Tissue-level sterol composition reflects known biology: sterol profiles differ significantly between tissue types (e.g., liver vs. brain) as quantified by Euclidean distance or Bray–Curtis dissimilarity.
- RT prediction error (|RT_experimental − RT_predicted|) is <2 minutes on held-out validation isomers, indicating GNN model generalization.

## Limitations

- CCS prediction model is trained on quantum chemistry features derived from N-Me derivatized unsaturated sterols; model accuracy on novel double bond positions or lipid congeners not in the training set is not characterized.
- MS/MS fragmentation pattern simulation (RDKit-based) is tuned and tested on sterol lipids only; applicability to other lipid classes with C=C bonds is theoretical.
- Stereoisomers (e.g., 5α vs. 5β configurations) are not discriminated by the current 4D workflow; additional orthogonal methods (e.g., ion mobility resolution ≥ 100 FWHM) or multi-stage MS would be required.
- RT-GNN model performance depends on the quality and coverage of the training set; tissue-specific or instrument-specific retention time drift could degrade predictions if not accounted for.
- The skill assumes that each detected peak corresponds to a single isomer; co-elution of structurally similar isomers in both LC and IM dimensions could lead to misassignment.

## Evidence

- [intro] The project implements a QCC-assisted dataset CCS prediction workflow as one of three main components, following MS/MS calculations for N-Me derived unsaturated sterol lipids and preceding LC-IM-MS/MS based 4D sterolomics data processing.: "The project implements a QCC-assisted dataset CCS prediction workflow as one of three main components, following MS/MS calculations for N-Me derived unsaturated sterol lipids and preceding"
- [readme] The script is written on the basis of RDkit's built-in functions. The script recognises double bond positions and generates MS/MS based on N-Me fragmentation patterns.: "The script is written on the basis of RDkit's built-in functions. The script  recognises double bond positions and generates MS/MS based on N-Me fragmentation patterns."
- [readme] The CCS prediction process in the paper is implemented using the scikit-learn API. It employs LASSO for feature selection and uses cross-validation to select the best hyperparameters for the SVR model.: "The CCS prediction process in the paper is implemented using the scikit-learn API. It employs LASSO for feature selection and uses cross-validation to select the best hyperparameters for the SVR"
- [intro] Apply machine-learning CCS prediction model trained on quantum chemistry features to estimate CCS values for the full lipid dataset.: "Apply machine-learning CCS prediction model trained on quantum chemistry features to estimate CCS values for the full lipid dataset."
- [readme] The RT prediction process referenced the 'Retention Time Prediction through Learning from a Small Training Data Set with a Pretrained Graph Neural Network'.: "The RT prediction process referenced the "Retention Time Prediction through Learning from a Small Training Data Set with a Pretrained Graph Neural Network"."
