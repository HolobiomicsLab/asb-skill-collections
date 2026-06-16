# Evaluation Strategy

## Direct Checks

- file_exists: verify that HMDB database file is accessible from glasgowcompbio/vimms-data repository (hmdb_metabolites.zip or equivalent raw HMDB download)
- script_runs: verify that DatabaseFormulaSampler can be instantiated and executed on the downloaded HMDB file with parameters min_mz=100, max_mz=1000 without runtime errors
- value_in_range: verify that the count of unique formulas returned by DatabaseFormulaSampler after filtering is exactly 73,822
- file_format_is: verify that HMDB input file is in expected format (pickle, CSV, or ZIP archive as used by vimms.ChemicalSamplers.DatabaseFormulaSampler)

## Expert Review

- Confirm that the filtering logic applied by DatabaseFormulaSampler (m/z range 100–1000 and any intensity or other thresholds) matches the documented formula-filtering step in the methods
- Validate that the count of 73,822 unique formulas is reproducible across multiple runs (no randomness or database state dependency affecting the output)
