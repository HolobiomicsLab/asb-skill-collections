# Evaluation Strategy

## Direct Checks

- verify file interim/tables/0_original/structure/smiles.tsv.gz exists in lotusnprod/lotus-processor repository
- verify file interim/tables/1_translated/structure/unique.tsv.gz exists in lotusnprod/lotus-processor repository after running the transformation pipeline
- file_format_is interim/tables/0_original/structure/smiles.tsv.gz as gzip-compressed tab-separated values
- file_format_is interim/tables/1_translated/structure/unique.tsv.gz as gzip-compressed tab-separated values
- script_runs smiles.py with interim/tables/0_original/structure/smiles.tsv.gz as input without errors
- script_runs sanitizing.py with output from smiles.py as input without errors
- field_present in interim/tables/1_translated/structure/unique.tsv.gz: column headers match expected sanitized structure identifier schema
- row_count_equals interim/tables/1_translated/structure/unique.tsv.gz greater than zero (robust to parameter choices for valid sanitization)

## Expert Review

- verify that SMILES strings in interim/tables/0_original/structure/smiles.tsv.gz are syntactically valid chemical notation
- verify that sanitization and translation applied by smiles.py and sanitizing.py produce chemically valid and standardized structures
- verify that unique.tsv.gz contains only unique structural identifiers with no unintended duplicates after deduplication
- verify that the transformation preserves chemical validity and does not introduce structural artifacts or loss of stereochemical information except where expected
