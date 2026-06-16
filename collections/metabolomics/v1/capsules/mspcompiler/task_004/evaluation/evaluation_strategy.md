# Evaluation Strategy

## Direct Checks

- verify file exists: input MoNA EI library file (e.g., MoNA download .msp or .json format) from https://mona.fiehnlab.ucdavis.edu/downloads
- script_runs: reorganize_mona() function executes without error on valid MoNA input file
- file_format_is: output object is an R list (or equivalent serialized structure)
- field_present: output object contains all required fields expected by downstream mspcompiler pipeline steps (exact field names and structure require expert review of source code)
- row_count_equals: output object row/record count matches or correctly summarizes input MoNA library record count
- output_matches_reference: if mspcompiler repository includes test fixtures or example outputs, verify reorganize_mona() output structure and content match reference deposit or example in repo

## Expert Review

- verify that the internal list format produced by reorganize_mona() conforms to the schema expected by downstream pipeline functions (read_lib, assign_smiles, separate_polarity, etc.)
- verify that field mapping from MoNA source format to internal format is complete and semantically correct (e.g., metadata fields, spectral peak data, compound identifiers are preserved or correctly transformed)
- verify that no spectral information or compound metadata is lost or corrupted during reorganization
