# Evaluation Strategy

## Direct Checks

- file_exists: verify that a LOTUS flat file (2D structure-organism pairs) is accessible at a public deposit (GitHub release, Zenodo, or documented URL from lotusnprod/lotus-processor)
- script_runs: execute a computational script (R, Python, or similar) that loads the flat file, groups unique organisms by cardinality of distinct 2D structures (bins: 1, 1–10, 10–100, >100), and outputs four counts
- output_matches_reference: verify that the four computed counts are exactly 7,354 / 21,490 / 10,683 / 374, byte-for-byte, in that order

## Expert Review

- Confirm that the binning logic correctly interprets 'distinct 2D structures per organism' (e.g., handling duplicate or isomeric structures, SMILES normalization, and structure deduplication method) aligns with LOTUS curation standards
