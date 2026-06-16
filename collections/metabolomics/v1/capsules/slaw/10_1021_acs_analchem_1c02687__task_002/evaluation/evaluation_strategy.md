# Evaluation Strategy

## Direct Checks

- verify that the GitHub repository adelabriere/SLAW or zamboni-lab/SLAW contains a README or documentation file describing the post-picking grouping step
- verify that the repository contains executable code or a module that implements isotopologue and adduct grouping
- verify that example grouped feature output (table or file) exists in the repository, deposited dataset, or supplementary materials with at least one field representing feature groups
- file_exists: grouped feature output file in repository or supplementary materials
- field_present: grouped feature output contains identifiable fields for isotopologue group ID and/or adduct annotation
- script_runs: grouping module executes without error on provided test LC-MS feature input

## Expert Review

- verify that the implemented grouping algorithm correctly clusters detected features by isotopologue series (e.g., M, M+1, M+2 patterns)
- verify that the grouping algorithm correctly identifies and separates adduct forms (e.g., [M+H]+, [M+Na]+, [M-H]−)
- verify that grouped output is biologically and chemically sensible: isotopologue groups show expected mass deltas and adduct groups show expected mass shifts
