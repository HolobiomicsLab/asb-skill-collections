# Evaluation Strategy

## Direct Checks

- verify file exists: model checkpoint or weights file for trained NMR2Struct model in github:MarklandGroup__NMR2Struct
- verify file exists: test set artifact (dataset file, CSV, or HDF5 containing test molecules with 1H NMR, 13C NMR, or combined spectra)
- verify file_format_is: test set is machine-readable (CSV, JSON, HDF5, or similar structured format)
- verify script_runs: evaluation script that loads trained model and test set, filters or masks input modalities (1H only, 13C only, 1H+13C), and produces per-modality accuracy metrics
- value_in_range: accuracy or F1 score for each modality condition is between 0 and 1 (or 0 and 100 if percentages); no canonical answer — multiple defensible accuracy thresholds may be considered reasonable
- field_present: output table or file contains separate accuracy columns for '1H_only', '13C_only', and 'combined' conditions
- output_matches_reference: if accuracy values are reported in article text or supplement, reproduction script output matches reported values (robust to rounding to 2 decimal places)

## Expert Review

- evaluate whether test set composition (size, molecular complexity, functional group diversity, atom count distribution) is appropriate and whether masking procedure (zeroing or removing one modality while preserving the other) is scientifically sound
- assess whether reported accuracy differences across modalities are chemically interpretable (e.g., whether 13C-only performance reflects expected discriminatory power for connectivity, or 1H-only reflects integration challenges)
- review whether evaluation controls for potential confounds: does the model architecture handle missing or masked modality inputs in a principled way, or does masking introduce artifacts?
