# Evaluation Strategy

## Direct Checks

- verify file_exists: metadataMASST aggregation script or entry point in github.com/mwang87/GNPS_MASST or Zenodo 492844724
- verify script_runs: aggregation script accepts as input one or more MASST search output files (JSON, CSV, or native MASST format) and executes without error on test data
- verify file_format_is: aggregation script produces a single named output file in a documented format (e.g., JSON, CSV, HTML, interactive visualization artifact)
- verify contains_substring: output artifact contains merged or concatenated records from all input search outputs (robust to record order and field names)
- verify output_matches_reference: aggregated summary matches structure and field names shown in metadataMASST web application UI (if UI screenshot or schema is available in repository)

## Expert Review

- Confirm that the aggregation logic correctly handles overlapping spectra, duplicate entries, or conflicting annotations across multiple domain-specific MASST runs without data loss or silent conflicts
- Evaluate whether the combined visualization artifact is usable and interpretable by a domain scientist (visual hierarchy, labeling, interactivity match the live metadataMASST web application)
- Assess whether the aggregation preserves provenance or metadata indicating which domain-specific MASST (microbeMASST, plantMASST, etc.) contributed each result
