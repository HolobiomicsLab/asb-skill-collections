# Evaluation Strategy

## Direct Checks

- verify that github:GarrettLab-UF__LipidMatch repository is accessible and contains a batch file or configuration file for MZmine integration
- verify file_exists for the MZmine batch file artifact in the repository (any of the following formats acceptable: .xml, .properties, .conf, .bat, or documented batch configuration file)
- verify file_exists for LipidMatch conversion or dispatch script(s) that accept peak-picker output as input
- verify file_format_is for the specified input file format from MZmine output (expected format: .csv, .tsv, .txt, or MZmine native export format — multiple defensible approaches depending on MZmine version)
- verify script_runs: execute the documented file-format conversion step with a minimal valid MZmine output file as input, robust to parameter choices in file paths
- verify output_matches_reference: the conversion output file matches the expected LipidMatch input schema (field names, column order, required columns) — solution_space: no canonical answer without access to detailed specification document or reference output file

## Expert Review

- confirm that the batch file and conversion scripts are current, maintained, and functionally compatible with recent MZmine versions
- assess whether the documented dispatch mechanism correctly handles edge cases (empty peak lists, malformed input rows, missing required columns)
- evaluate whether the hand-off interface preserves all necessary metadata (retention time, m/z, intensity, ion mode) required for downstream LipidMatch matching
