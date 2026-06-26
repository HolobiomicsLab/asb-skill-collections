---
name: machine-learning-model-inference
description: Use when you have molecular descriptors or fingerprints for a set of
  compounds (e.g., from LC-MS metabolomics) and need to predict a continuous property—such
  as HPLC retention time—to support compound identification or filter out false positive
  annotations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3837
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - Retip
  - Retip (R package)
  - pyRetip (Python package)
  - Retip app
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.9b05765
  title: Retip
evidence_spans:
- github.com__oloBion__Retip
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_retip_cq
    doi: 10.1021/acs.analchem.9b05765
    title: Retip
  dedup_kept_from: coll_retip_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.9b05765
  all_source_dois:
  - 10.1021/acs.analchem.9b05765
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# machine-learning-model-inference

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Apply a pre-trained machine learning model to molecular descriptor inputs to generate quantitative predictions (e.g., retention times) for compound annotation in metabolomics. This skill transforms chemical features into physico-chemical or chromatographic properties without retraining.

## When to use

You have molecular descriptors or fingerprints for a set of compounds (e.g., from LC-MS metabolomics) and need to predict a continuous property—such as HPLC retention time—to support compound identification or filter out false positive annotations. Use this when a validated pre-trained model is available and you do not need to retrain on new data.

## When NOT to use

- Your input is already a feature table with pre-computed retention times; inference is unnecessary.
- You need to train or retrain a model on new retention time data; use model training/validation instead.
- Your compounds fall outside the chemical space (e.g., very high molecular weight, exotic functional groups) used to train the pre-trained model; prediction accuracy will degrade.

## Inputs

- Molecular descriptors (fingerprints, physicochemical properties) for compounds
- Pre-trained machine learning model (Retip or equivalent)
- Compound identifiers or SMILES strings
- Optional: biochemical database records (HMDB, KNApSAcK, ChEBI, DrugBank, etc.) for structural input

## Outputs

- Predicted retention time (RT) values for each compound
- Structured output table with compound IDs and predicted RTs
- Confidence or uncertainty estimates (if model provides them)

## How to apply

Load the pre-trained Retip model (trained on retention time data using one of six machine learning algorithms: Random Forest, BRNN, XGBoost, lightGBM, Keras, or H2O autoML) and supply molecular descriptor features (e.g., fingerprints, physicochemical properties) as input. The model generates predicted retention time (RT) values for each compound. Export predictions as a structured table and compare predicted RTs against observed RTs from your chromatography run to validate compound identities or remove false positive annotations. The rationale is that retention time is an orthogonal descriptor that improves annotation confidence when combined with mass spectral data.

## Related tools

- **Retip (R package)** (Pre-trained retention time prediction model using six ensemble machine learning algorithms; accepts molecular descriptors and outputs predicted RT values for metabolomic compound annotation) — https://github.com/olobion/Retip
- **pyRetip (Python package)** (Python implementation of Retip for retention time prediction inference) — https://github.com/oloBion/pyRetip
- **Retip app** (Web interface for interactive retention time prediction and tutorial usage) — https://www.retip.app/

## Examples

```
devtools::install_github('olobion/Retip'); library(Retip); predictions <- predict_RT(molecules, model='ensemble'); write.csv(predictions, 'predicted_retention_times.csv')
```

## Evaluation signals

- Predicted retention times fall within the observed RT range of your chromatographic run (e.g., 0–60 min for typical HPLC).
- Predicted RTs correlate with observed RTs; compute Pearson/Spearman correlation or root mean square error (RMSE) against validation compounds with known RTs.
- Compounds with predicted RTs far from observed RTs are flagged as potential false annotations or require manual review.
- Output table is complete (no missing or NaN values) and contains all input compounds with one RT prediction per compound.
- Predicted RTs cluster appropriately by molecular structure or physicochemical class (e.g., hydrophobic compounds elute later than hydrophilic ones in reverse-phase HPLC).

## Limitations

- Model predictions are only valid for small molecules in HPLC–MS; retention time varies by column chemistry, gradient, temperature, and mobile phase composition, so predictions must be recalibrated or validated per laboratory method.
- Retip was trained on a specific chemical space (reflected in its integrated biochemical databases: HMDB, KNApSAcK, ChEBI, etc.); compounds outside this space (e.g., novel synthetic compounds, very large peptides) may have poor prediction accuracy.
- Pre-trained model does not account for method-specific or sample matrix effects; predicted RTs are a reference point only and should always be compared to observed data.
- Requires R 4.4.0, Java JDK, and Python 3.10 for Keras support; installation complexity may limit reproducibility in resource-constrained environments.

## Evidence

- [readme] Retip is a tool for predicting Retention Time (RT) for small molecules in a high pressure liquid chromatography (HPLC) Mass Spectrometry analysis: "Retip is a tool for predicting Retention Time (RT) for small molecules in a high pressure liquid chromatography (HPLC) Mass Spectrometry analysis"
- [readme] The R package uses six different machine learning algorithms to built a stable, accurate and fast RT prediction model: Random Forest, BRNN, XGBoost, lightGBM, Keras, H2O autoML: "The R package uses six different machine learning algorithms to built a stable, accurate and fast RT prediction model: Random Forest, BRNN, XGBoost, lightGBM, Keras, H2O autoML"
- [readme] Retention time calculation can be useful in identifying unknowns and removing false positive annotations.: "Retention time calculation can be useful in identifying unknowns and removing false positive annotations."
- [other] Load molecular descriptor features for compounds (e.g., fingerprints, physicochemical properties). Apply the Retip predictive model trained on retention time data to generate retention time predictions for each compound. Format and export predicted retention times as a structured output table.: "Load molecular descriptor features for compounds (e.g., fingerprints, physicochemical properties). Apply the Retip predictive model trained on retention time data to generate retention time"
- [other] Retip is a retention time prediction tool designed for metabolomics that performs compound annotation by predicting retention times from molecular input data.: "Retip is a retention time prediction tool designed for metabolomics that performs compound annotation by predicting retention times from molecular input data."
