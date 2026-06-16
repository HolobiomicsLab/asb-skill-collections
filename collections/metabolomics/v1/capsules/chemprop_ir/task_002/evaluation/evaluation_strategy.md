# Evaluation Strategy

## Direct Checks

- verify file exists at github.com/chemprop/chemprop-IR or equivalent public repository URL
- verify repository contains README or documentation describing spectral features component
- verify repository contains executable Python code or scripts for spectral feature extraction
- script_runs: execute spectral feature extraction code with a valid molecular input (SMILES or molecular graph format) and confirm no runtime errors
- output_matches_reference: extracted spectral feature vector has expected dimensionality and numeric type (float array or similar) — robust to parameter choices across reasonable molecular inputs

## Expert Review

- chemist or computational chemistry expert: verify that extracted spectral features are chemically sensible and match the named features described in the paper (e.g., functional group indicators, bond type distributions)
- expert: confirm that spectral feature construction aligns with standard infrared spectroscopy principles and the chemprop-IR methodology
- expert: review whether the implementation correctly translates molecular structure (via SMILES or graph) into feature space claimed in the paper
