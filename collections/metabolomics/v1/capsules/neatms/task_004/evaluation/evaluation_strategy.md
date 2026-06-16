# Evaluation Strategy

## Direct Checks

- verify file exists at github:bihealth__NeatMS containing nn_handler module with create_batches() method
- script_runs: invoke nn_handler.create_batches() with normalise_class=True using default 80:10:10 split and confirm execution completes without error
- script_runs: invoke nn_handler.create_batches() with normalise_class=False using default 80:10:10 split and confirm execution completes without error
- file_exists: batch artifacts generated for normalise_class=True condition (train, test, validation batch files)
- file_exists: batch artifacts generated for normalise_class=False condition (train, test, validation batch files)
- value_in_range: verify train/test/validation split proportions are approximately 80:10:10 (±2 percentage points) for both conditions
- row_count_equals: sum of train + test + validation batch row counts equals total input dataset row count for both conditions

## Expert Review

- verify that class-normalized batches (normalise_class=True) satisfy equal-class-count constraint: all classes present in each batch have equal or near-equal peak counts as documented
- verify that non-normalized batches (normalise_class=False) preserve original class distribution without forced equalization
- assess whether batch creation parameters and output structure conform to NeatMS design specification for downstream neural network training
