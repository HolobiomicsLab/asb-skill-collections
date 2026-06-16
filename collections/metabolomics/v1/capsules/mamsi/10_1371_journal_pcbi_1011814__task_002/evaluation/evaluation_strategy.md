# Evaluation Strategy

## Direct Checks

- verify that kopeckylukas/py-mamsi repository contains a MamsiStructSearch class or module
- verify that MamsiStructSearch has a load_lcms() method accepting a list or array-like input
- verify that MamsiStructSearch produces a named artifact (file, object, or data structure) representing structural clusters
- verify that the implementation searches for isotopologue signatures using mass difference of 1.00335 Da
- verify that the implementation searches for common adduct signatures via electrospray ionisation adducts
- verify that the implementation merges overlapping adduct and isotopologue clusters
- verify that the implementation supports cross-assay cluster linking using [M+H]+/[M-H]- references
- script_runs: execute a minimal MamsiStructSearch workflow on sample LC-MS features (m/z, RT columns) from kopeckylukas/py-mamsi-tutorials and confirm no runtime errors — solution_space: multiple defensible sample inputs valid
- output_matches_reference: verify that structural cluster output format is documented or demonstrated in tutorials repository

## Expert Review

- evaluate whether the adduct and correlation-clustering logic correctly implements the description in the repository README and methods section
- evaluate whether the mass tolerance thresholds and RT window parameters for isotopologue and adduct detection are biochemically appropriate
- evaluate whether the merging strategy for overlapping clusters (adduct + isotopologue) is statistically sound and avoids over-clustering
