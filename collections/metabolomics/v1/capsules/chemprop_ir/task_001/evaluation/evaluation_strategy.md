# Evaluation Strategy

## Direct Checks

- verify file exists: github.com/chemprop/chemprop base repository is accessible and contains core message passing neural network implementation
- verify file exists: github:gfm-collab__chemprop-IR repository contains model architecture definition files (e.g., model.py, layers.py, or equivalent)
- script_runs: instantiate chemprop-IR model class with documented hyperparameters without raising exceptions
- script_runs: execute forward pass on a sample molecule (SMILES string or molecular graph) through instantiated model and obtain tensor output
- verify output_matches_reference: forward pass output tensor has expected shape and dtype (e.g., matches documented spectral feature dimension)

## Expert Review

- confirm that spectral features module integration preserves base chemprop message passing mechanism and does not corrupt gradient flow
- verify architectural design: spectral features module is correctly positioned in the extended architecture relative to base message passing layers
- assess whether model instantiation and forward pass are consistent with the architecture description claimed in the paper
