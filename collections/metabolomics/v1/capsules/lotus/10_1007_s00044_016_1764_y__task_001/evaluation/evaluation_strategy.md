# Evaluation Strategy

## Direct Checks

- retrieve LOTUS dataset deposit from GitHub (lotusnprod/lotus-processor) or Zenodo; verify file_exists for primary flat-file tables (structure, organism, reference)
- row_count_equals for unique referenced structure-organism pairs (3D): 588,694
- row_count_equals for unique referenced structure-organism pairs (2D): 484,174
- row_count_equals for unique curated structures (3D): 231,330
- row_count_equals for unique curated structures (2D): 153,956
- row_count_equals for unique organisms: 42,166
- value_in_range for source database count: 31 (or contains_substring if reported in metadata file)

## Expert Review

- verify that row counts represent the correct unit of analysis (e.g., unique pairs after deduplication, not raw records)
- confirm that 3D/2D distinction in structure counts is applied consistently across reported figures
- assess whether reported organism count includes valid taxonomic filtering and does not double-count synonyms
