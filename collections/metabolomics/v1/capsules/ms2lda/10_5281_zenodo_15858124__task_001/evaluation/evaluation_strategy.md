# Evaluation Strategy

## Direct Checks

- verify that the MS2LDA repository (github:vdhooftcompmet__MS2LDA) is accessible and contains a COMP-PREPROCESSING module or equivalent preprocessing code
- verify file_exists: check that the repository contains documented support for .mgf, .msp, and .mzML input formats in the preprocessing stage
- verify script_runs: load a minimal example .mgf, .msp, or .mzML file from the repository's test data or documentation and confirm the preprocessing ingestion code executes without error
- verify output_matches_reference: confirm that the bag-of-fragments output structure (format, fields, fragment representation) matches the documented schema in the repository or methods section
- verify file_format_is: confirm that the intermediate output from format-ingestion is serializable (e.g., JSON, pickle, CSV) and conforms to the expected bag-of-fragments structure before LDA training
- verify contains_substring: check that preprocessing code or documentation references fragment binning, neutral loss extraction, or noise filtering as documented in the workflow steps

## Expert Review

- assess whether the fragment-binning strategy (mass tolerance, binning method) is appropriate for MS/MS fragmentation data and consistent with standard proteomics/metabolomics practice
- assess whether the noise-filtering thresholds and criteria are biologically/chemically justified and whether they risk removing genuine low-abundance fragments
- assess whether the bag-of-fragments representation (e.g., term frequency, binary presence/absence, weighted counts) is suitable as input to LDA and matches the model's documented assumptions
