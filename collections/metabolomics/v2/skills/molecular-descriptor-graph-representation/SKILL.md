---
name: molecular-descriptor-graph-representation
description: Use when when you need to train or evaluate a graph neural network for molecular property prediction (collision cross section, ion mobility, or related descriptors) and have access to SMILES strings and/or 3D conformer coordinates.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0337
  edam_topics:
  - http://edamontology.org/topic_3373
  - http://edamontology.org/topic_3674
  - http://edamontology.org/topic_0602
  tools:
  - Mol2CCS
  - train-test.py
  - Poetry (dependency manager)
derived_from:
- doi: 10.1186/s13321-024-00899-w
  title: mol2ccs
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mol2ccs_cq
    doi: 10.1186/s13321-024-00899-w
    title: mol2ccs
  dedup_kept_from: coll_mol2ccs_cq
schema_version: 0.2.0
---

# molecular-descriptor-graph-representation

## Summary

Convert molecular structures into graph neural network–compatible representations by encoding SMILES strings and optional 3D coordinates as node–edge graphs, enabling learned feature extraction for collision cross section prediction and generalizability evaluation.

## When to use

When you need to train or evaluate a graph neural network for molecular property prediction (collision cross section, ion mobility, or related descriptors) and have access to SMILES strings and/or 3D conformer coordinates. This skill is essential when reproducing GNN generalizability studies across different molecular databases (e.g., METLIN-CCS, CCSBase).

## When NOT to use

- Input data lacks SMILES or other structural representation (e.g., only precomputed descriptors or images).
- Molecular set is too small (<100 compounds) or highly imbalanced across adduct types, risking overfitting without cross-database validation.
- Ground truth CCS values are missing or predominantly NA; the model cannot learn without continuous regression targets.

## Inputs

- SMILES strings (column in parquet/CSV dataset)
- 3D coordinates (optional; column in parquet/CSV dataset, e.g., 'coordinates')
- Adduct type labels (column in dataset, e.g., '[M+H]+', '[M-H]-')
- Collision cross section ground truth values (column in dataset, e.g., 'ccs')
- Training and test dataset files (parquet format)

## Outputs

- Graph-encoded molecular representations (internal to trained GNN model)
- Trained graph neural network model (HDF5 file, e.g., 'model/train-metlin-test-metlin.h5')
- CCS predictions on test set (parquet/CSV with predicted vs. ground truth)
- Performance metrics (MAE, R², RMSE, per-adduct error statistics)

## How to apply

Begin by loading training and validation datasets in parquet format with columns for SMILES, adduct type, CCS ground truth, and optionally pre-computed 3D coordinates. The training pipeline accepts a `--coordinates-present` flag: if coordinates are provided (in a column named by `--coordinates-column-name`, e.g., 'coordinates'), the graph encoder uses them directly; if absent, the model generates 3D coordinates from SMILES automatically. Pass the formatted datasets through the Mol2CCS wrapper's training function, specifying the column names for SMILES (`--smiles-column-name`), adduct (`--adduct-column-name`), and CCS target (`--ccs-column-name`). The resulting graph representations encode molecular topology and geometry as learnable node and edge features, which are then fed to the GNN backbone. Monitor training loss and validation metrics (MAE, R²) across epochs (typically 400) to ensure the graph encoding captures predictive signal. Verify generalizability by evaluating on held-out test sets from different source databases (e.g., train on METLIN, test on CCSBase).

## Related tools

- **Mol2CCS** (Wrapper module for graph encoding, training, and prediction; encapsulates SMILES-to-graph conversion and optional 3D coordinate generation.) — https://github.com/enveda/ccs-prediction
- **train-test.py** (Core training script that orchestrates graph representation creation, GNN model training, and validation metric computation.) — https://github.com/enveda/ccs-prediction
- **Poetry (dependency manager)** (Manages Python environment and reproducible package versions for graph neural network and molecular processing libraries.) — https://github.com/enveda/ccs-prediction

## Examples

```
poetry run python scripts/train-test.py --prefix "train-metlin-test-ccsbase" --train-input-file "ccs-prediction/metlin_train_3d.parquet" --test-input-file "ccs-prediction/ccsbase_3d.parquet" --parameter-path "parameter/parameter-train-metlin-test-metlin.json" --model-output-file "model/train-metlin-test-metlin.h5" --coordinates-column-name "coordinates" --coordinates-present --smiles-column-name "smiles" --adduct-column-name "adduct" --ccs-column-name "ccs" --dropout-rate 0.1 --epochs 400
```

## Evaluation signals

- Parquet dataset loads without error and contains expected columns (smiles, ccs, adduct, coordinates) with correct data types and non-null counts.
- GNN model training converges (training loss decreases monotonically or plateaus; validation loss does not diverge wildly).
- Trained model file (.h5) is created and can be loaded; model layer dimensions match the input graph feature size and output dimension (1 for CCS regression).
- Predictions on test set span a reasonable range (e.g., 50–500 Ų for CCS) and correlate with ground truth (R² > 0.7 for in-database validation; R² > 0.5 for cross-database generalization).
- Cross-database evaluation shows that a model trained on METLIN predicts CCSBase test compounds with consistent MAE and R² (per-adduct breakdowns reveal no systematic bias).

## Limitations

- Model generalizability degrades significantly when test compounds contain adducts or chemical scaffolds underrepresented in training (e.g., rare adduct types or novel functional groups).
- 3D coordinate generation from SMILES (when not provided) introduces an additional hyperparameter (conformer sampling method) and potential stereochemistry ambiguity.
- Performance is sensitive to training hyperparameters (dropout rate, epochs, learning rate); the README provides one example set (dropout=0.1, epochs=400) but does not systematically explore sensitivity.
- Missing original datasets (METLIN, CCSBase) must be downloaded separately and licensed; the repository does not ship raw data, only pre-split parquets and predictions (available via Zenodo).

## Evidence

- [other] Load the deposited training and validation datasets according to the repository's data format specifications. Load the pre-trained graph neural network model or retrain it using the provided training pipeline and hyperparameters. Generate collision cross section predictions on the validation or test set.: "Load the deposited training and validation datasets according to the repository's data format specifications. Load the pre-trained graph neural network model or retrain it using the provided training"
- [readme] coordinates-column-name column name of the 3d coordinates for each smiles; coordinates-present if the coordinates are present (if not given, the model will use the smiles to generate the 3d coordinates); smiles-column-name column name of the smiles; adduct-column-name column name of the adduct; ccs-column-name column name of the ccs: "coordinates-column-name column name of the 3d coordinates for each smiles; coordinates-present if the coordinates are present (if not given, the model will use the smiles to generate the 3d"
- [readme] Train the model based on your own training dataset with [wrapper_train] and predict with [wrapper_predict] function.: "Train the model based on your own training dataset with [wrapper_train] and predict with [wrapper_predict] function."
- [readme] Each notebook reads the csv/excel and formats it according to the input of Mol2CCS.: "Each notebook reads the csv/excel and formats it according to the input of Mol2CCS."
- [other] Compute reported performance metrics (e.g., mean absolute error, R², or other regression statistics) and save results to a metrics file.: "Compute reported performance metrics (e.g., mean absolute error, R², or other regression statistics) and save results to a metrics file."
