# Evaluation Strategy

## Direct Checks

- verify that the repository github:enveda/ccs-prediction contains a preprocessing script or module that accepts SMILES strings as input
- verify that the preprocessing pipeline produces a serialized graph dataset file in a standard format (.pt, .pkl, or equivalent)
- verify that the output graph objects contain node features (atom features) and edge features (bond features) as tensors or array-like structures
- script_runs: execute the preprocessing pipeline on a subset of the CCS dataset and confirm it completes without errors
- verify that the generated graph dataset file is not empty and contains at least one graph object
- verify that graph objects are compatible with a standard GNN framework (PyTorch Geometric, DGL, or equivalent) by attempting to load and inspect one example graph

## Expert Review

- assess whether the atom/bond feature engineering choices (feature dimensionality, encoding scheme, normalization) are appropriate for collision cross section prediction
- evaluate whether the graph construction methodology (bond connectivity rules, handling of implicit hydrogens, stereochemistry encoding) correctly represents the molecular structure
- review whether the dataset preprocessing preserves the chemical validity and integrity of the original SMILES representations
