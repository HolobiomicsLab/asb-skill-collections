---
name: retention-time-prediction-modeling
description: Use when you have a set of small-molecule compounds (e.g., from MS/MS library matching or database annotation) that require retention time validation or ranking to resolve ambiguous identifications.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3803
  edam_topics:
  - http://edamontology.org/topic_0102
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3407
  tools:
  - Retip
  - Retip (R package)
  - pyRetip (Python package)
  - Retiplib
  - rcdk / rcdklibs
  techniques:
  - LC-MS
  - GC-MS
  - CE-MS
  - direct-infusion-MS
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

# retention-time-prediction-modeling

## Summary

Build and apply machine learning models to predict liquid chromatography retention times (RT) for small molecules from molecular descriptors, enabling compound annotation and false positive filtering in untargeted metabolomics workflows. Retip integrates six ensemble algorithms (Random Forest, BRNN, XGBoost, lightGBM, Keras, H2O AutoML) trained on reference RT data to generate predictive RT scores that disambiguate structural isomers and validate MS-based identifications.

## When to use

Apply this skill when you have a set of small-molecule compounds (e.g., from MS/MS library matching or database annotation) that require retention time validation or ranking to resolve ambiguous identifications. Use it specifically when you possess (or can compute) molecular descriptors (fingerprints, physicochemical properties) and have access to reference RT training data or a pre-trained RT model for your chromatographic method. This is particularly valuable in untargeted metabolomics where RT prediction can remove false positives and improve compound annotation confidence.

## When NOT to use

- Input compounds are from a non-chromatographic analysis (e.g., direct infusion MS, GC-MS with temperature-programmed retention index) — Retip is trained specifically for HPLC and may not generalize to other separation modes.
- Molecular descriptors are unavailable or cannot be reliably computed from the provided chemical identifiers.
- The retention time training data or reference model is from a substantially different chromatographic method (different column, mobile phase, pH, temperature) — RT predictions will be method-specific and poor generalization is likely.

## Inputs

- SMILES strings or InChI keys for compounds to be annotated
- Molecular descriptor matrix (fingerprints, physicochemical properties)
- Reference retention time training dataset (compound ID, descriptors, measured RT)
- Observed retention times from LC-MS analysis
- Pre-trained Retip model (optional; algorithm selection if training de novo)

## Outputs

- Predicted retention time values per compound
- Prediction confidence scores or model ensemble agreement
- Annotation ranking table (compound ID, predicted RT, observed RT, residual, confidence)
- Validated or filtered compound annotation list
- Model performance metrics (R², RMSE, MAE on held-out test set)

## How to apply

Load molecular descriptor features (e.g., SMILES-derived fingerprints, molecular weight, LogP, polar surface area) for your compound set into the Retip package (R or Python). Select or train a predictive model using one or more of the six ensemble algorithms; the R package trains all six simultaneously for robustness. Feed the descriptor matrix into the trained model to generate predicted RT values and associated confidence scores for each compound. Compare predicted RTs against observed (measured) RTs from your LC-MS analysis: compounds with predicted RT within experimental error (typically ±5–10% depending on method) are retained as true annotations, while outliers are flagged as likely false positives or misidentifications. Export the ranked annotation table with RT predictions, experimental RTs, and prediction residuals for downstream validation and reporting.

## Related tools

- **Retip (R package)** (Implements retention time prediction using ensemble machine learning (Random Forest, BRNN, XGBoost, lightGBM, Keras, H2O AutoML); trains, evaluates, and applies predictive models to descriptor matrices.) — https://github.com/olobion/Retip
- **pyRetip (Python package)** (Python implementation of Retip for retention time prediction; enables integration into Python-based metabolomics pipelines.) — https://github.com/oloBion/pyRetip
- **Retiplib** (Core library of pre-computed molecular descriptors and biochemical database integration (HMDB, ChEBI, DrugBank, LipidMAPS, etc.) for rapid RT model application to known compounds.) — https://github.com/olobion/Retiplib
- **rcdk / rcdklibs** (R bindings to the Chemistry Development Kit for computing molecular descriptors (fingerprints, physicochemical properties) from SMILES or chemical structures.)

## Examples

```
devtools::install_github('olobion/Retip'); library(Retip); model <- retip_train(training_data, methods=c('RF','XGBoost','lightGBM')); predictions <- predict(model, test_descriptors); rt_validation <- data.frame(compound_id, predicted_rt=predictions, observed_rt, residual=abs(predicted_rt-observed_rt))
```

## Evaluation signals

- Predicted RT values fall within ±5–10% of observed RTs for a validation subset (typical acceptable tolerance for HPLC-based methods); check R² and RMSE of predictions vs. measured RTs.
- Ensemble model agreement: when multiple algorithms disagree significantly on RT prediction for a compound, confidence is lower and the annotation may warrant manual review.
- Annotation rank stability: compounds with small predicted–observed RT residuals rank higher in the final annotation list and are prioritized; compounds with large residuals are flagged as false positives.
- Cross-validation or held-out test set performance: model achieves reported accuracy metrics (e.g., RMSE < 0.5 min on test compounds) before applying to unknown annotations.
- Biochemical plausibility check: predicted RTs should follow expected trends (e.g., increasing RT with increasing LogP for similar compound classes) and should not violate known chromatographic behavior.

## Limitations

- Retip models are trained on specific HPLC methods and do not automatically transfer to different chromatographic systems, columns, or mobile phases; method-specific retraining may be required.
- Prediction accuracy depends on the availability and representativeness of training data; compounds in chemical space distant from the training set will have higher prediction uncertainty.
- Molecular descriptor quality is critical; SMILES errors, unspecified stereochemistry, or missing tautomers can introduce descriptor artifacts and degrade predictions.
- Retip 2.0 requires R ≥ 4.4.0, Java JDK, and Python 3.10+ (for Keras models); complex dependency chains (rJava, h2o, reticulate) may cause installation challenges, especially in conda environments.
- RT prediction alone cannot distinguish between constitutional isomers if they co-elute; it improves but does not replace MS/MS fragmentation matching or orthogonal separation techniques.

## Evidence

- [readme] Retip is a tool for predicting Retention Time (RT) for small molecules in a high pressure liquid chromatography (HPLC) Mass Spectrometry analysis: "Retip is a tool for predicting Retention Time (RT) for small molecules in a high pressure liquid chromatography (HPLC) Mass Spectrometry analysis"
- [readme] The R package uses six different machine learning algorithms to built a stable, accurate and fast RT prediction model: Random Forest, BRNN, XGBoost, lightGBM, Keras, H2O autoML: "The R package uses six different machine learning algorithms to built a stable, accurate and fast RT prediction model: Random Forest, BRNN, XGBoost, lightGBM, Keras, H2O autoML"
- [other] Retention time prediction tool designed for metabolomics that performs compound annotation by predicting retention times from molecular input data: "Retip is a retention time prediction tool designed for metabolomics that performs compound annotation by predicting retention times from molecular input data"
- [other] Load molecular descriptor features for compounds (e.g., fingerprints, physicochemical properties). Apply the Retip predictive model trained on retention time data to generate retention time predictions for each compound: "Load molecular descriptor features for compounds (e.g., fingerprints, physicochemical properties). Apply the Retip predictive model trained on retention time data to generate retention time"
- [readme] Retip also includes useful biochemical databases like: HMDB, KNApSAcK, ChEBI, DrugBank, SMPDB, YMDB, T3DB, FooDB, NANPDB: "Retip also includes useful biochemical databases like: HMDB, KNApSAcK, ChEBI, DrugBank, SMPDB, YMDB, T3DB, FooDB, NANPDB"
- [readme] It is not possible to install Retip in conda environment because rJava requires NVIDIA drivers: "It is not possible to install Retip in conda environment because rJava requires NVIDIA drivers"
