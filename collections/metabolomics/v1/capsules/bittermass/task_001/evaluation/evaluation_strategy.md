# Evaluation Strategy

## Direct Checks

- verify that github:Niv-Lab__BitterPredict1 repository is accessible and contains BitterPredict.m file
- file_exists: BitterPredict.m in the repository
- script_runs: BitterPredict.m executes without error when provided a valid CSV or Excel input file containing required molecular descriptors
- output_matches_reference: per-molecule predictions (binary bitter/not-bitter labels) are produced for all input molecules; no canonical answer for prediction values themselves without reference dataset, but output structure must be complete and non-null for all rows

## Expert Review

- verify that the descriptor columns present in the input file match those documented as 'required' by BitterPredict.m (descriptor names and roles are domain-specific chemical/computational knowledge)
- assess whether the binary predictions are internally consistent with the classifier's decision logic as documented in the repository README or code comments
