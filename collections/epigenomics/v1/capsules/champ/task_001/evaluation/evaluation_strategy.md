# Evaluation Strategy

## Direct Checks

- verify file exists at github:YuanTian1991__ChAMP containing ChAMP package source code
- verify file exists at github:YuanTian1991__ChAMPdata containing test datasets (HumanMethylation450 and EPICSimData)
- script_runs: execute champ.load() or champ.import() on HumanMethylation450 test dataset without errors
- script_runs: execute champ.load() or champ.import() on EPICSimData test dataset without errors
- value_in_range: probe count returned from HumanMethylation450 pre-filter equals 485,512 (exact match required)
- value_in_range: probe count returned from EPICSimData pre-filter equals 867,531 (exact match required)

## Expert Review

- Verify that the test datasets (HumanMethylation450 and EPICSimData) are legitimate reference datasets appropriate for validating ChAMP loading functionality
- Confirm that pre-filter probe counts reported in documentation or package vignette match the expected values of 485,512 for 450K and 867,531 for EPIC
