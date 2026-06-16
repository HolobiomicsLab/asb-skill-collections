# Evaluation Strategy

## Direct Checks

- verify file exists in github:Niv-Lab__BitterPredict1 repository containing descriptor calculation code (e.g. descriptor_calculator.m, descriptor_*.py, or equivalent)
- verify that code accepts raw molecular input in at least one of: SMILES string format, SDF file format, or other standard molecular structure representation
- verify that code produces output in CSV or Excel format
- verify that output file contains at least one named molecular descriptor column with numeric or categorical values
- script_runs: execute descriptor conversion code with a small test dataset (e.g. 5–10 molecules in SMILES or SDF format) and verify no runtime errors
- output_matches_reference: confirm output descriptor file structure is compatible with BitterPredict.m by checking column names match the documented required descriptor set (if documented in repo)
- file_format_is: verify output file is valid CSV or Excel (robust to whitespace and minor formatting variations)
- row_count_equals: verify output file has one row per input molecule, plus header row

## Expert Review

- evaluate whether the named descriptor set computed is chemically and informatically sound for bitter taste prediction (domain expertise required to assess descriptor choice and molecular relevance)
- assess completeness: does the descriptor set include established molecular features known to correlate with bitterness perception, or is it limited to generic cheminformatics descriptors?
