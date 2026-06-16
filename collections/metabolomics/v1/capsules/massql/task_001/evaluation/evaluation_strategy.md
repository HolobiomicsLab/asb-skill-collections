# Evaluation Strategy

## Direct Checks

- verify file exists at github:mwang87__MassQueryLanguage containing parser implementation or grammar definition
- script_runs: execute parser on a valid MassQL query string and confirm it produces structured output (AST or JSON), not an error
- output_matches_reference: parser output for a canonical MassQL query example (if provided in repository) matches the documented or reference AST/JSON structure
- format_is: parser output is valid JSON or valid tree-serialized AST format with labeled nodes
- contains_substring: parser implementation or grammar file contains explicit handling of mass-spectrometry-specific constructs (e.g., precursor mass, fragment ion, spectrum, scan, tolerance keywords or operators beyond standard SQL)

## Expert Review

- Does the parser grammar or implementation satisfy all four stated design principles (Expressiveness, Precision, Scalability, Relatively Natural) as applied to the specific MassQL constructs it handles?
- Does the parser correctly handle the extension of SQL syntax with mass-spectrometry-specific operators and constraints (e.g., mass ranges, spectral similarity, retention time windows)?
- Are there edge cases or ambiguous MassQL syntax patterns that the parser does not resolve, contradicting the Precision principle?
- Does the parser implementation scale appropriately from single-spectrum to repository-scale queries without fundamental architectural limits?
