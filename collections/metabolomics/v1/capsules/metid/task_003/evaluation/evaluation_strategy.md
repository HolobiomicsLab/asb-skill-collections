# Evaluation Strategy

## Direct Checks

- verify that Met-ID repository (github:pbjarterot/Met-ID) contains configuration or plugin code (file or directory) that defines or registers derivatizing matrices
- verify file_exists for a second derivatizing matrix configuration file (e.g. TAHS.json, tahs_config.py, or equivalent) in the repository
- verify script_runs: execute Met-ID's matrix registration or initialization code with the new matrix configuration without errors
- verify file_format_is: the new matrix configuration adheres to the documented schema used by the first (existing) derivatizing matrix in the codebase
- verify output_matches_reference: run Met-ID with the second matrix on a test metabolite and confirm the output contains adduct annotations (e.g. [M+matrix_adduct]+) distinct from the baseline matrix
- verify contains_substring: adduct annotation strings in Met-ID output include the expected ion form for the second matrix (e.g. presence of TAHS-related ion notation if TAHS is chosen)

## Expert Review

- assess whether the second derivatizing matrix is a real, publicly documented reagent with known derivatization chemistry
- evaluate whether the adduct annotations produced by Met-ID for the second matrix are chemically correct and consistent with the reagent's known reaction mechanism
- judge whether the implementation is genuinely extensible (i.e. a new user could add a third matrix following the same pattern without modifying core code)
- assess the clarity and completeness of any documentation or comments in the configuration/plugin code that enable future matrix additions
