# Evaluation Strategy

## Direct Checks

- verify file artifact_chemical_tree exists in q2-qemistree pipeline outputs
- file_format_is artifact_chemical_tree one of: Newick (.nwk), QIIME 2 artifact (.qza), or text representation
- verify artifact_chemical_tree is non-empty (file size > 0 bytes)
- script_runs: load artifact_chemical_tree using QIIME 2 artifact API or standard Newick parser without errors
- verify artifact_chemical_tree contains tree structure with at least one internal node (not a single leaf)
- field_present: artifact_chemical_tree metadata includes feature/node identifiers
- robust to parameter choices: node count and branch structure remain consistent across multiple parse attempts

## Expert Review

- assess whether node labels and edge weights (if present) are chemically meaningful and correctly derived from input mass-spectrometry features
- evaluate tree topology for biological plausibility given the input metabolomic dataset (e.g., chemical similarity reflected in clustering)
- review whether tree structure supports the stated goal of 'chemically-informed comparison' as intended by q2-qemistree design
