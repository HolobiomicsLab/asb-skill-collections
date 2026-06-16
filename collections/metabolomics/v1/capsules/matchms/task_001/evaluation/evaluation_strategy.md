# Evaluation Strategy

## Direct Checks

- verify file exists at github.com/matchms/matchms repository
- verify matchms package can be imported in Python environment
- verify at least one spectral data file (MGF or MSP format) is available in the repository or can be downloaded from a public source (e.g., Zenodo, MetaboLights, MassIVE)
- script_runs: Python script that instantiates matchms metadata cleaning filters executes without errors
- script_runs: Python script that applies metadata filters to a loaded spectral dataset completes execution
- file_exists: cleaned spectrum collection output file is generated
- file_format_is: output file matches expected format (MGF, MSP, JSON, or matchms native format)
- row_count_equals or field_present: output collection contains spectra records with metadata fields (robust to various field schemas used across spectral formats)
- contains_substring: output file or collection object contains evidence of applied filter transformations (e.g., modified metadata entries, removed invalid entries, or validation logs)
- output_matches_reference: if matchms repository includes example cleaned spectral outputs or test fixtures, byte-for-byte or structural equivalence check against reference deposit

## Expert Review

- Assess whether metadata cleaning operations (e.g., field standardization, missing value handling, invalid entry removal) conform to metabolomics/mass spectrometry best practices and matchms design intent
- Evaluate whether cleaned metadata is chemically and informatically valid (e.g., precursor m/z values in plausible ranges, molecular weight consistency, retained spectrum count is reasonable relative to input)
