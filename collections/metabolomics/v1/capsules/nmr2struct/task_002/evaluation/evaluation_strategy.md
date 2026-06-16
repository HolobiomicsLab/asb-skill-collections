# Evaluation Strategy

## Direct Checks

- file_exists: verify that the deposited dataset github:MarklandGroup__NMR2Struct contains at least one file listing molecular fragments paired with ground-truth assembled structures
- file_format_is: verify that fragment-structure pair data is in a machine-readable format (CSV, JSON, pickle, or HDF5)
- script_runs: verify that a Python script can load the transformer module checkpoint from the repository and execute forward inference on a test fragment set without errors
- output_matches_reference: compare model-generated assembled structures (SMILES or graph representation) against ground-truth structures from the deposited dataset using exact string matching or molecular graph isomorphism, with >0% of outputs matching, no canonical answer (multiple valid SMILES representations exist for same molecule)
- field_present: verify that model outputs include both connectivity graph and atomic formula for each assembled candidate structure

## Expert Review

- Assess whether the assembled structures are chemically valid (valence rules satisfied, no impossible bonds)
- Evaluate fragment assembly accuracy: does the model correctly combine fragments without dangling bonds or mismatched atom types?
- Judge whether the isolated fragment assembly module's performance is meaningful in isolation or whether it relies on upstream spectral encoding that is not present in this evaluation
