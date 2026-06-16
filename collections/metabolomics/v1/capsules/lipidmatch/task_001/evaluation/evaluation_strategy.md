# Evaluation Strategy

## Direct Checks

- verify file exists at github:GarrettLab-UF/LipidMatch in .csv format containing lipid library data
- file_format_is .csv for all lipid library files retrieved from the repository
- row_count_equals or exceeds 500,000 across all distinct lipid species entries in aggregated library files
- field_present: lipid-type or category column exists in library .csv files
- value_in_range: count of distinct lipid-type categories is >= 60 (exact count reported)
- script_runs: computational agent can load, parse, and aggregate .csv files without errors
- output_matches_reference: reported threshold values (500,000 species, 60 types) are met or exceeded by direct enumeration from files

## Expert Review

- Verify that the lipid species and lipid-type definitions used in the .csv files align with standard lipidomics nomenclature and the article's stated scope
- Confirm that the aggregation method (e.g., de-duplication logic, category consolidation) correctly captures 'distinct' species as intended by the authors
