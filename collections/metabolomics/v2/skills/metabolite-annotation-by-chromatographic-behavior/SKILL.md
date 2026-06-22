---
name: metabolite-annotation-by-chromatographic-behavior
description: Use when when you have an untargeted metabolomics dataset from HPLC–MS (e.g., mzML, NetCDF) with detected peaks of unknown identity, and you need to disambiguate or validate tentative compound annotations by comparing observed retention time against machine-learning predicted retention time.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3903
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0154
  tools:
  - Retip
  - Retip (R package)
  - pyRetip (Python package)
  - Retip app
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
---

# metabolite-annotation-by-chromatographic-behavior

## Summary

Predict retention times for small molecules in HPLC–MS analysis using machine learning models trained on molecular descriptors, enabling compound annotation and false positive removal in untargeted metabolomics workflows. Retip accepts fingerprints and physicochemical properties as input and outputs predicted retention times (in minutes or normalized units) for comparison against observed chromatographic behavior.

## When to use

When you have an untargeted metabolomics dataset from HPLC–MS (e.g., mzML, NetCDF) with detected peaks of unknown identity, and you need to disambiguate or validate tentative compound annotations by comparing observed retention time against machine-learning predicted retention time. Particularly useful when false positive annotations are a concern or when retention time is a discriminating feature among structural isomers.

## When NOT to use

- Your dataset is from GC–MS or other gas-phase separation where HPLC retention time models do not apply.
- You lack molecular structure information (e.g., only accurate mass available, no spectral library match).
- Your chromatography method or column chemistry is drastically different from the training data (e.g., hydrophilic interaction chromatography vs. reverse-phase); Retip was trained on standard reverse-phase HPLC protocols and may not generalize to orthogonal methods.

## Inputs

- molecular descriptors (SMILES, InChI, fingerprints, or physicochemical properties)
- candidate compound identifiers (e.g., from spectral library matching)
- observed retention time values from HPLC chromatogram

## Outputs

- predicted retention time for each candidate compound
- structured output table with input compounds, descriptors, and predictions
- confidence or ensemble model agreement metrics (if available)

## How to apply

Load molecular descriptors (e.g., SMILES strings, InChI keys, or pre-computed fingerprints such as ECFP) for candidate compounds into Retip. The tool applies one or more trained ensemble models (Random Forest, XGBoost, lightGBM, BRNN, Keras, or H2O AutoML) to generate predicted retention time values. Compare predicted retention times against experimentally observed retention times from your chromatography run; large deviations (threshold depends on chromatographic method and column, typically >0.5–1 min) suggest misannotation. Retip includes biochemical databases (HMDB, ChEBI, DrugBank, LipidMAPS, etc.) to facilitate lookup of molecular properties; use the ensemble model predictions to rank or filter annotations before confirming with orthogonal methods (MS/MS, standards).

## Related tools

- **Retip (R package)** (Ensemble machine learning framework for retention time prediction; trains and applies six ML algorithms (Random Forest, BRNN, XGBoost, lightGBM, Keras, H2O AutoML) to transform molecular descriptors into predicted retention times) — https://github.com/olobion/Retip
- **pyRetip (Python package)** (Python implementation of Retip retention time prediction for integration into Python-based metabolomics pipelines) — https://github.com/oloBion/pyRetip
- **Retip app** (Web interface for interactive retention time prediction and annotation validation without local installation) — https://www.retip.app/

## Examples

```
devtools::install_github('olobion/Retip'); library(Retip); predictions <- RetipPredictions(compounds_df, model='ensemble'); head(predictions[, c('compound_id', 'predicted_RT', 'observed_RT')])
```

## Evaluation signals

- Predicted retention time values fall within the expected range (0–30 min for typical reverse-phase HPLC) and match observed chromatogram retention times within method-specific tolerance (typically ±0.5–1 min).
- Ensemble model agreement: if multiple ML algorithms are used, high consensus (e.g., ≥5 of 6 models predict within ±0.3 min) increases confidence in the prediction.
- Biochemical plausibility: predicted retention times for chemically similar compounds (by structure or lipophilicity) cluster nearby, and outliers are investigated for annotation errors.
- Validation with standards: compare predictions for known reference compounds to empirical retention times; R² > 0.90 between observed and predicted across a diverse set of validation compounds.
- Absence of implausible predictions (e.g., retention times for very hydrophobic lipids < 5 min, or very hydrophilic small metabolites > 20 min on standard reverse-phase columns).

## Limitations

- Retip was trained primarily on reverse-phase HPLC data; predictions may not be reliable for orthogonal chromatography modes (HILIC, normal phase, ion-pairing RP).
- Model performance depends on the chemical diversity and quality of the training set; compounds with unusual structural features or those absent from training data may receive less accurate predictions.
- Requires valid molecular structure input (SMILES, InChI, or precomputed descriptors); cannot predict retention times for unknown structures or from mass alone.
- Installation requires R 4.4.0, Java JDK, Python 3, and multiple machine learning dependencies (rJava, caret, keras, h2o); cannot run in conda environments due to rJava compatibility with NVIDIA drivers.
- Column chemistry, temperature, solvent gradient, and flow rate all affect absolute retention times; predictions are most reliable when the experimental method closely matches the training data distribution.

## Evidence

- [readme] Retip is a tool for predicting Retention Time (RT) for small molecules in a high pressure liquid chromatography (HPLC) Mass Spectrometry analysis: "Retip is a tool for predicting Retention Time (RT) for small molecules in a high pressure liquid chromatography (HPLC) Mass Spectrometry analysis"
- [readme] Retention time calculation can be useful in identifying unknowns and removing false positive annotations: "Retention time calculation can be useful in identifying unknowns and removing false positive annotations"
- [readme] The R package uses six different machine learning algorithms to built a stable, accurate and fast RT prediction model: Random Forest, BRNN, XGBoost, lightGBM, Keras, H2O autoML: "The R package uses six different machine learning algorithms to built a stable, accurate and fast RT prediction model: Random Forest, BRNN, XGBoost, lightGBM, Keras, H2O autoML"
- [readme] Retip also includes useful biochemical databases like: HMDB, KNApSAcK, ChEBI, DrugBank, SMPDB, YMDB, T3DB, FooDB: "Retip also includes useful biochemical databases like: HMDB, KNApSAcK, ChEBI, DrugBank, SMPDB, YMDB, T3DB, FooDB"
- [other] Load molecular descriptor features for compounds (e.g., fingerprints, physicochemical properties). Apply the Retip predictive model trained on retention time data to generate retention time predictions: "Load molecular descriptor features for compounds (e.g., fingerprints, physicochemical properties). Apply the Retip predictive model trained on retention time data to generate retention time"
- [other] Retip is a retention time prediction tool designed for metabolomics that performs compound annotation by predicting retention times from molecular input data: "Retip is a retention time prediction tool designed for metabolomics that performs compound annotation by predicting retention times from molecular input data"
