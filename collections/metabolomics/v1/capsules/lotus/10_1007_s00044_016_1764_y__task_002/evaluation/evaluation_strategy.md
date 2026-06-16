# Evaluation Strategy

## Direct Checks

- Load the published LOTUS flat file (2D structures dataset); verify file_exists and file_format_is (CSV or TSV)
- Parse the 2D structure-organism pairs table; verify row_count_equals the total number of unique structure-organism pairs reported in EnrichedIndex (484174)
- Group unique 2D structures by organism count; verify the four bin counts match exactly: structures appearing in exactly 1 organism = 89903, structures in 1–10 organisms = 45640, structures in 10–100 organisms = 3990, structures in >100 organisms = 403 (byte-for-byte exact match required)
- Verify the four counts sum to the total unique 2D structure count (89903 + 45640 + 3990 + 403 = 139936)

## Expert Review

- Confirm the binning logic is scientifically meaningful: verify that the boundaries (1, 1–10, 10–100, >100) are clearly defined and that overlaps or off-by-one errors in interval definition do not occur
- Assess whether the reported counts are consistent with the documented curation pipeline (steps 1_gathering through 4_visualizing) and the organism/structure quality assurance steps
