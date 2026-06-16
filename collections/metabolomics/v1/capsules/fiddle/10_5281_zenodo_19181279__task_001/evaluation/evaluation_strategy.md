# Evaluation Strategy

## Direct Checks

- Verify file config/fiddle_tcn_orbitrap.yml exists
- Verify file config/fiddle_tcn_orbitrap.yml contains the substring 'ftms' within the gnps_orbitrap instrument allowlist
- Verify file config/fiddle_tcn_orbitrap.yml contains the substring 'gnps_orbitrap' (allowlist definition present)
- Script runs: execute the data preparation pipeline (prepare_augment_rescore.py or equivalent TCN dataset loader) with the updated config/fiddle_tcn_orbitrap.yml as input
- Verify output training split row count equals 28,751 compounds (exact match required)
- Verify output test split row count equals 3,195 compounds (exact match required)
- Verify that the only instrument type change between the config baseline and updated config is the addition of 'ftms' to gnps_orbitrap allowlist (no other modifications introduced)

## Expert Review

- Confirm that 'ftms' is a valid Orbitrap instrument designation in GNPS ontology and that its addition is scientifically appropriate for the Orbitrap dataset
- Verify that the compound count increase from the prior baseline to 28,751 training / 3,195 test is solely attributable to inclusion of 'ftms' spectra, with no other data filtering or augmentation changes
- Confirm that the reported split (28,751 / 3,195) represents a reproducible and deterministic outcome given a fixed random seed or deterministic train-test split logic
