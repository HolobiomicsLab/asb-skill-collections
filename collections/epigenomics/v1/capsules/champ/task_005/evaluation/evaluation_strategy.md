# Evaluation Strategy

## Direct Checks

- verify file exists: ChAMP package repository at github:YuanTian1991__ChAMP contains champ.SVD() function definition
- script_runs: load HumanMethylation450 test dataset (8 samples) from ChAMPdata package and execute champ.SVD() on normalized beta matrix without errors
- script_runs: execute champ.SVD() on GSE40279 beta matrix (if publicly accessible via GEO) without errors
- output_matches_reference: when champ.SVD() is run on a normalized beta matrix where Random Matrix Theory detects >20 latent components, verify returned component count is capped at exactly 20 (robust to different input datasets, parameter-sensitive to RMT detection threshold)

## Expert Review

- verify that the capping behavior at 20 components is correctly implemented in champ.SVD() source code and matches the stated methods description
- confirm that Random Matrix Theory detection is functioning as intended prior to the cap being applied
