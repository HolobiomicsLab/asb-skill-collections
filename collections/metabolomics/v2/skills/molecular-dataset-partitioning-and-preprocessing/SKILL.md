---
name: molecular-dataset-partitioning-and-preprocessing
description: Use when you have raw molecular datasets (e.g., METLIN-CCS, CCSBase)
  with SMILES strings, 3D coordinates, adduct information, and ground-truth collision
  cross section labels, and you need to format them for GNN training and held-out
  test evaluation with consistent standardization.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3373
  - http://edamontology.org/topic_0602
  tools:
  - poetry (dependency/environment manager)
  - Python scripts/train-test.py
  - Jupyter notebooks (notebooks/data_processing/2_data_splits.ipynb)
  - Makefile commands (make train-metlin-test-metlin, etc.)
  - Mol2CCS library functions (mol2ccs/train_and_predict.py)
  techniques:
  - ion-mobility-MS
  license_tier: restricted
derived_from:
- doi: 10.1186/s13321-024-00899-w
  title: mol2ccs
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mol2ccs
    doi: 10.1186/s13321-024-00899-w
    title: mol2ccs
  dedup_kept_from: coll_mol2ccs
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-024-00899-w
  all_source_dois:
  - 10.1186/s13321-024-00899-w
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# molecular-dataset-partitioning-and-preprocessing

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Prepare molecular structure and collision cross section data for training and evaluating graph neural network models by applying standardized preprocessing and partitioning into train/validation/test splits. This skill ensures data consistency and reproducibility across GNN generalizability studies.

## When to use

You have raw molecular datasets (e.g., METLIN-CCS, CCSBase) with SMILES strings, 3D coordinates, adduct information, and ground-truth collision cross section labels, and you need to format them for GNN training and held-out test evaluation with consistent standardization.

## When NOT to use

- Data is already in standardized parquet format with verified column alignment — proceed directly to model training.
- You are evaluating a pre-trained GNN on predictions without retraining — load pre-computed prediction outputs instead.
- Input lacks ground-truth CCS labels or adduct information — preprocessing cannot proceed without complete molecular metadata.

## Inputs

- Raw molecular database (CSV/Excel format) — METLIN or CCSBase database
- SMILES strings for each molecule
- 3D coordinates (optional, generated from SMILES if not provided)
- Adduct type labels
- Ground-truth collision cross section values
- Parameter configuration file (JSON) specifying model hyperparameters

## Outputs

- Formatted training dataset (parquet file, e.g., metlin_train_3d.parquet)
- Formatted test dataset (parquet file, e.g., ccsbase_3d.parquet)
- Train/validation/test data splits with consistent column schema
- Preprocessed molecular features ready for GNN input

## How to apply

Load the raw molecular database (CSV/Excel) and reformat it according to the expected schema: SMILES column, optional 3D coordinates column, adduct column, and CCS label column (see notebooks/data_processing/2_data_splits.ipynb for format details). Apply any required preprocessing or standardization consistent with training (e.g., coordinate normalization, SMILES canonicalization, adduct encoding). Partition data into train/validation/test splits or load a pre-defined held-out test set. The repository provides wrapper functions and example commands in the Makefile that specify input/output parquet files, column names (smiles-column-name, coordinates-column-name, adduct-column-name, ccs-column-name), and preprocessing flags (coordinates-present) to standardize the workflow.

## Related tools

- **poetry (dependency/environment manager)** (Install development dependencies and runtime packages for data processing scripts) — https://github.com/enveda/ccs-prediction
- **Python scripts/train-test.py** (Execute train/test workflow with specified input files, preprocessing parameters, and output paths) — https://github.com/enveda/ccs-prediction
- **Jupyter notebooks (notebooks/data_processing/2_data_splits.ipynb)** (Interactive data exploration, format validation, and split verification for METLIN and CCSBase datasets) — https://github.com/enveda/ccs-prediction
- **Makefile commands (make train-metlin-test-metlin, etc.)** (Standardized shell invocations for reproducible preprocessing with fixed parameter sets) — https://github.com/enveda/ccs-prediction
- **Mol2CCS library functions (mol2ccs/train_and_predict.py)** (Wrapper for training dataset preprocessing and GNN model input preparation) — https://github.com/enveda/ccs-prediction

## Examples

```
poetry run python scripts/train-test.py --prefix "train-metlin-test-ccsbase" --train-input-file "ccs-prediction/metlin_train_3d.parquet" --test-input-file "ccs-prediction/ccsbase_3d.parquet" --smiles-column-name "smiles" --adduct-column-name "adduct" --ccs-column-name "ccs" --coordinates-column-name "coordinates" --coordinates-present
```

## Evaluation signals

- Output parquet files contain all required columns (smiles, coordinates/adduct, ccs) with no missing values in critical fields
- Row counts and data distributions in train/test splits match documented split ratios and match those used in reproducibility notebooks
- SMILES strings parse correctly and canonicalize consistently (no formatting drift across partitions)
- CCS values fall within expected ranges for the source database (e.g., METLIN vs. CCSBase ranges) with no outliers exceeding documented extrema
- Column names and data types match those specified in parameter configuration (e.g., coordinates-column-name, ccs-column-name) and are consistent with train-test.py invocation arguments

## Limitations

- Original METLIN-CCS and CCSBase datasets must be downloaded separately by the user under their respective licenses; the repository does not bundle them
- 3D coordinates are optionally generated from SMILES using an unspecified coordinate generation method if not pre-computed; results may vary by coordinate generation tool
- Preprocessing scripts assume specific input CSV/Excel structures; nonstandard database formats require manual schema mapping before partition scripts will execute correctly
- Data processing notebooks are exploratory and must be manually executed; no automated pipeline currently enforces version-controlled preprocessing across all raw datasets

## Evidence

- [readme] Each user should download the raw database (as excel/csv) and read them in the two notebooks for each database located at https://github.com/enveda/ccs-prediction/tree/main/notebooks/data_processing. Each notebook reads the csv/excel and formats it according to the input of Mol2CCS.: "Each user should download the raw database (as excel/csv) and read them in the two notebooks for each database located at https://github.com/enveda/ccs-prediction/tree/main/notebooks/data_processing."
- [other] Load the CCS dataset and apply any required preprocessing or standardization consistent with training. Partition data into train/validation/test splits or load the held-out test set as specified in the repository.: "Load the CCS dataset and apply any required preprocessing or standardization consistent with training. Partition data into train/validation/test splits or load the held-out test set as specified in"
- [readme] See the commands in the `Makefile` to train the models. Run them as `make train-metlin-test-metlin`: "See the commands in the `Makefile` to train the models. Run them as `make train-metlin-test-metlin`"
- [readme] **train-input-file** is the training set (see notebooks/data_processing/2_data_splits.ipynb for details on the format)/ **test-input-file** test set (see notebooks/data_processing/2_data_splits.ipynb for details on the format): "**train-input-file** is the training set (see notebooks/data_processing/2_data_splits.ipynb for details on the format)/"
- [readme] **smiles-column-name** column name of the smiles **adduct-column-name** column name of the adduct **ccs-column-name** column name of the ccs **coordinates-column-name** column name of the 3d coordinates for each smiles: "**smiles-column-name** column name of the smiles **adduct-column-name** column name of the adduct **ccs-column-name** column name of the ccs"
- [readme] **coordinates-present** if the coordinates are present (if not given, the model will use the smiles to generate the 3d coordinates): "**coordinates-present** if the coordinates are present (if not given, the model will use the smiles to generate the 3d coordinates)"
