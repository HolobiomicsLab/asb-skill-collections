# Evaluation Strategy

## Direct Checks

- verify file 'MassBank_example.msp' exists in package root or data/ directory
- script_runs: execute mspToLib function with inputs={MassBank_example.msp, noise=0.005, mpeaksScore=0.9, mpeaksThres=0.1} without errors
- file_exists: output CSV library file(s) are created with naming pattern matching per-spectrum convention
- file_format_is: output CSV contains expected column headers for MS/MS library format (e.g., precursor_mz, fragment_mz, intensity, or equivalent)
- contains_substring: output filenames or metadata contain ionization mode suffix (e.g., '_pos' or '_neg') for each spectrum entry
- row_count_equals: at least one CSV output row per input spectrum from MassBank_example.msp (robust to parameter choices in noise/threshold range)
- verify output CSV structure is consistent with documented per-spectrum library entry format — no malformed rows or truncated records

## Expert Review

- confirm peak-picking thresholds (noise=0.005, mpeaksScore=0.9, mpeaksThres=0.1) produce chemically reasonable fragment ion lists (e.g., no spurious low-intensity artifacts, retention of true fragment ions)
- assess positive/negative mode suffix assignment accuracy — verify ionization mode annotations in output match input spectra metadata
- evaluate whether per-spectrum CSV entries conform to MassBank or standard metabolomics library format conventions
