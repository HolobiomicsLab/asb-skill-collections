# Evaluation Strategy

## Direct Checks

- verify file interim/tables/2_cleaned/organism/cleaned.tsv.gz exists in lotusnprod/lotus-processor repository
- verify file 5_addingOTL.R exists in lotusnprod/lotus-processor repository
- verify script 5_addingOTL.R runs without error when executed with R, using interim/tables/2_cleaned/organism/cleaned.tsv.gz as input
- verify at least one output file matching pattern interim/dictionaries/organism/*.tsv is produced after script execution
- verify output file(s) in interim/dictionaries/organism/ are in TSV format (tab-separated values, .tsv extension)
- verify output TSV file(s) contain at least two columns: one for organism identifiers and one for Open Tree of Life identifiers, robust to column naming conventions

## Expert Review

- assess whether Open Tree of Life identifier mappings in output dictionary are semantically correct for a representative sample of organism entries
- assess whether the script appropriately handles missing or ambiguous organism names in the cleaned input table
