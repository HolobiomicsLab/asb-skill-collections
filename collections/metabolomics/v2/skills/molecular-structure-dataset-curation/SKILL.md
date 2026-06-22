---
name: molecular-structure-dataset-curation
description: Use when you have a collection of molecular structures (with SMILES strings, InChI, or similar identifiers) and corresponding experimentally determined or reference CCS values, and you need to format and validate them as input to a machine learning CCS prediction model.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3172
  tools:
  - Google Colaboratory
  - Python
  - Sklearn (scikit-learn) V1.0.2+
  - Jupyter Lab / Jupyter Notebook
  - CCSP 2.0
  techniques:
  - ion-mobility-MS
derived_from:
- doi: 10.1021/acs.analchem.2c03491
  title: CCS Predictor 2.0
- doi: 10.1101/2022.08.09.503345
  title: ''
evidence_spans:
- a Google Colaboratory Jupyter notebook that is well suited for beginners
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ccs_predictor_2_0_cq
    doi: 10.1021/acs.analchem.2c03491
    title: CCS Predictor 2.0
  dedup_kept_from: coll_ccs_predictor_2_0_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.2c03491
  all_source_dois:
  - 10.1021/acs.analchem.2c03491
  - 10.1101/2022.08.09.503345
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# molecular-structure-dataset-curation

## Summary

Preparation and validation of molecular structure datasets paired with known collision cross section (CCS) values for training machine learning models in ion-mobility metabolomics workflows. This skill ensures that training data meet quality and format requirements before use in CCSP 2.0 or similar predictive models.

## When to use

You have a collection of molecular structures (with SMILES strings, InChI, or similar identifiers) and corresponding experimentally determined or reference CCS values, and you need to format and validate them as input to a machine learning CCS prediction model. Specifically, when preparing data for CCSP 2.0 training on ≤10,000 molecules or when integrating molecular structure data into a larger metabolomics analysis workflow.

## When NOT to use

- Input dataset already exceeds 10,000 molecules and you are using the Google Colab variant; use the local Jupyter Lab version instead.
- Molecular structures lack experimentally validated or high-confidence CCS reference values; curation cannot substitute for instrumental measurement or trusted literature values.
- CCS values are intended only for a single specific instrument/condition and generalization to other platforms is not desired; curated datasets are instrument-agnostic and may not transfer reliably.

## Inputs

- Molecular structure identifiers (SMILES strings, InChI, IUPAC names, or chemical structure files)
- Experimentally determined or reference collision cross section values (numeric CCS in Ų or equivalent units)
- Optional: metadata such as ionization mode, charge state, or adduct type

## Outputs

- Curated training dataset file (CSV or delimited text format) with columns for molecular identifiers and corresponding CCS values
- Data quality report or validation log (implicit from successful notebook execution)

## How to apply

Assemble your molecular structures and their corresponding known CCS values into a single tabular format (CSV or compatible delimited file) with columns for molecular identifiers (e.g., name, SMILES, InChI) and CCS values. Verify that all rows contain both structure and CCS information with no missing values in critical fields. Validate that CCS values are numeric and within the expected range for your instrument and ionization mode. Organize the curated dataset in a format that CCSP 2.0 can ingest directly (as specified in the embedded notebook instructions). If using the Google Colab variant, ensure the dataset is ≤10,000 molecules and prepare to upload it via the Colab file interface; if using the local Jupyter Lab variant, place the file in an accessible directory for import by the notebook.

## Related tools

- **Python** (Programming language for data manipulation, validation, and format conversion of molecular structure and CCS datasets)
- **Sklearn (scikit-learn) V1.0.2+** (Machine learning library that processes the curated training dataset to train CCS prediction models)
- **Google Colaboratory** (Cloud-hosted Jupyter notebook environment for dataset upload, import, and direct use in CCSP 2.0 for small-scale (≤10,000 molecule) workflows) — https://colab.research.google.com/
- **Jupyter Lab / Jupyter Notebook** (Local notebook environment for dataset import and integration with CCSP 2.0 for larger-scale or production workflows) — https://jupyter.org/
- **CCSP 2.0** (Collision Cross Section Predictor notebook that consumes the curated training dataset to fit and apply machine learning models) — https://github.com/facundof2016/CCSP2.0

## Evaluation signals

- All rows in the curated dataset contain both a molecular identifier and a numeric CCS value with no missing entries in critical columns.
- CCS values are numeric, positive, and fall within the expected range for the ionization mode and instrument type used.
- The dataset file parses without encoding, delimiter, or format errors when imported by the CCSP 2.0 notebook.
- For Google Colab: dataset row count is ≤10,000 and file size is compatible with browser upload and Google hosted storage limits.
- The curated dataset successfully trains a machine learning model in CCSP 2.0 without convergence warnings or loss of records due to data quality issues.

## Limitations

- Google Colab variant is limited to continuous operation of 12 hours and will disconnect after ~20 minutes of idle time; long-running curation or validation tasks may be interrupted.
- Google Colab does not require local Python installation but depends on stable internet connectivity and browser compatibility; offline curation workflows are not supported.
- CCSP 2.0 requires Sklearn V1.0.2 or later; curated datasets must be compatible with this version's input schema and data types.
- CCS prediction accuracy depends critically on training dataset quality, representativeness, and size; small or biased datasets may produce poor generalization to novel molecules.
- The notebook does not provide automated quality scoring or outlier detection for CCS values; manual review or external validation of reference values is the responsibility of the curator.

## Evidence

- [readme] Collision Cross Section Predictor 2.0 is an open source Python notebook intended to help ion-mobility scientists predict collision cross sections with user-curated training sets: "Collision Cross Section Predictor 2.0 is an open source Python notebook intended to help ion-mobility scientists predict collision cross sections with user-curated training sets"
- [intro] The Google Colab variant operates on datasets ≤10,000 molecules: "If you plan to use CCSP 2.0 only to make small scale predictions (<10,000 molecules) and export your results to your local computer, the Google Colab option is recommended."
- [readme] Google Colab requires no local Python or package installation: "This route does not require you to install Python or any of the packages required to run the code, as all calculations are performed through Google hosted services"
- [readme] Sklearn V1.0.2 or later is required: "The current version of CCSP 2.0 requires Sklearn V1.0.2 or later. A full list of package requirements is available in the requirements.txt file."
- [readme] Google Colab session limits and idle disconnection: "Google Colab will only allow continuous notebook operation for up to 12 hours and will disconnect after ~20 minutes if left idle."
- [intro] Workflow includes dataset upload and configuration: "Upload or import the user-curated training dataset containing molecular structures and known collision cross section values"
