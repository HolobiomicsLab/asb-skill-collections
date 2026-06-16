# Evaluation Strategy

## Direct Checks

- verify file significant_matches.tsv exists in Dereplicator output directory
- verify file significant_matches.tsv exists in VarQuest output directory
- verify file significant_matches.tsv exists in Dereplicator+ output directory
- file_format_is: each significant_matches.tsv is tab-separated with at least columns for match_id, score, and query_spectrum
- row_count_equals or value_in_range: compare row counts across three pipelines' significant_matches.tsv outputs (no canonical answer — different tools may return different numbers of hits)
- contains_substring: verify each significant_matches.tsv contains at least one row of hit data (not header-only)
- verify input spectra MSV000080102-derived test dataset is accessible and identical across all three pipeline runs
- script_runs: NPDtools 2.5.0 Dereplicator pipeline executes without error on test spectra
- script_runs: NPDtools 2.5.0 VarQuest pipeline executes without error on test spectra
- script_runs: NPDtools 2.5.0 Dereplicator+ pipeline executes without error on test spectra

## Expert Review

- assess whether differences in significant_matches.tsv hit counts across pipelines reflect genuine algorithmic differences or implementation artifacts
- evaluate whether blind mode vs. standard mode differences in hit detection are consistent with documented tool design goals
- judge whether the three pipelines' hit signatures (which compounds are detected under which conditions) are chemically and statistically reasonable given the spectra source material
