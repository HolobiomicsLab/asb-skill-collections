# Evaluation Strategy

## Direct Checks

- verify file exists at the documented example input JSON location
- verify protocol table exists in the input JSON
- verify str directive with parameters for_each=True, test='type=sample_prep', sort_by=['id'], sort_order='ascending', delimiter=' ' can be applied to the protocol table
- verify concatenated SAMPLEPREP_SUMMARY string output matches the expected output shown in the For Each section, byte-for-byte

## Expert Review

- confirm that the directive application logic correctly filters rows where type=sample_prep
- confirm that the sorting by 'id' in ascending order is correctly applied before concatenation
- confirm that the delimiter ' ' is correctly inserted between concatenated values
